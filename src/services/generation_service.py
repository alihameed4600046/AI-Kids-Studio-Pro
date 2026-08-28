"""Generation service bridging UI, prompts, and AI engines.

This module provides the GenerationService class which integrates
PromptEngine, ModelManager, and media engines with the UI layer.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Sequence

from src.engine.ai_engine import (
    AIEngineError,
    EngineConfig,
    GenerationRequest,
    GenerationResponse,
)
from src.engine.image_engine import ImageEngine, ImageConfig
from src.engine.model_manager import ModelManager, ProviderConfig, ProviderType, TaskType
from src.engine.prompt_engine import PromptEngine, PromptTemplateError
from src.engine.video_engine import VideoEngine, VideoConfig
from src.engine.voice_engine import VoiceEngine, VoiceConfig
from src.logging_config import configure_logging
from src.services.generation_repository import GenerationRepository

configure_logging()
logger = logging.getLogger(__name__)


class MediaType(Enum):
    """Types of media that can be generated."""

    TEXT = "text"
    IMAGE = "image"
    VOICE = "voice"
    VIDEO = "video"
    COMBINED = "combined"


class GenerationStatus(Enum):
    """Status of a generation job."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class GenerationJob:
    """Represents a generation job."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    category: str = ""
    template_name: str = ""
    variables: dict[str, Any] = field(default_factory=dict)
    media_types: list[MediaType] = field(default_factory=list)
    status: GenerationStatus = GenerationStatus.PENDING
    result: GenerationResponse | None = None
    error: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None
    duration_ms: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class GenerationService:
    """Service for managing AI generation workflows.

    This class integrates PromptEngine, ModelManager, and media engines
    to provide a unified interface for the UI layer.

    Attributes
    ----------
    prompt_engine:
        Engine for loading and rendering prompt templates.
    model_manager:
        Manager for AI providers and auto-fallback.
    """

    def __init__(
        self,
        prompt_engine: PromptEngine | None = None,
        model_manager: ModelManager | None = None,
        repository: GenerationRepository | None = None,
    ) -> None:
        self.prompt_engine = prompt_engine or PromptEngine()
        self.model_manager = model_manager or ModelManager()
        self.repository = repository or GenerationRepository()
        self._jobs: dict[str, GenerationJob] = {}
        self._progress_callbacks: list[Any] = []
        self._image_engine: ImageEngine | None = None
        self._voice_engine: VoiceEngine | None = None
        self._video_engine: VideoEngine | None = None

    def register_progress_callback(self, callback: Any) -> None:
        """Register a callback for progress updates.

        Parameters
        ----------
        callback:
            Callable that receives (job_id, progress, status).
        """
        self._progress_callbacks.append(callback)

    def _notify_progress(self, job_id: str, progress: float, status: str) -> None:
        """Notify all progress callbacks."""
        for callback in self._progress_callbacks:
            try:
                callback(job_id, progress, status)
            except Exception as exc:
                logger.warning("Progress callback failed: %s", exc)

    def set_image_engine(self, engine: ImageEngine) -> None:
        """Set the image generation engine."""
        self._image_engine = engine

    def set_voice_engine(self, engine: VoiceEngine) -> None:
        """Set the voice generation engine."""
        self._voice_engine = engine

    def set_video_engine(self, engine: VideoEngine) -> None:
        """Set the video generation engine."""
        self._video_engine = engine

    def create_job(
        self,
        category: str,
        template_name: str,
        variables: dict[str, Any],
        media_types: Sequence[MediaType] | None = None,
    ) -> GenerationJob:
        """Create a new generation job.

        Parameters
        ----------
        category:
            Content category (e.g., "Stories", "Images").
        template_name:
            Name of the template to use.
        variables:
            Variables for template substitution.
        media_types:
            Types of media to generate.

        Returns
        -------
        GenerationJob
            The created job.
        """
        job = GenerationJob(
            category=category,
            template_name=template_name,
            variables=dict(variables),
            media_types=list(media_types or [MediaType.TEXT]),
        )
        self._jobs[job.id] = job
        logger.info(
            "Created generation job %s for template %s", job.id, template_name
        )
        return job

    async def execute_job(self, job: GenerationJob) -> GenerationJob:
        """Execute a generation job.

        Parameters
        ----------
        job:
            The job to execute.

        Returns
        -------
        GenerationJob
            The updated job with results.

        Raises
        ------
        AIEngineError
            If generation fails.
        """
        job.status = GenerationStatus.RUNNING
        job.result = None
        job.error = None
        start_time = time.time()
        self._notify_progress(job.id, 0.0, "Starting generation...")

        try:
            # Step 1: Build prompt
            self._notify_progress(job.id, 0.1, "Building prompt...")
            request = self.prompt_engine.build_request(
                job.template_name, job.variables
            )

            # Step 2: Generate text
            self._notify_progress(job.id, 0.2, "Generating text...")
            response = await self.model_manager.generate(
                request, task_type=TaskType.TEXT_GENERATION
            )
            job.result = response

            # Step 3: Generate media if requested
            if MediaType.IMAGE in job.media_types and self._image_engine:
                self._notify_progress(job.id, 0.5, "Generating image...")
                image_request = GenerationRequest(
                    prompt=request.prompt,
                    metadata={"image_config": job.variables.get("image_config")},
                )
                image_response = await self._image_engine.generate(image_request)
                job.metadata["image_response"] = image_response.text

            if MediaType.VOICE in job.media_types and self._voice_engine:
                self._notify_progress(job.id, 0.7, "Generating voice...")
                voice_request = GenerationRequest(
                    prompt=request.prompt,
                    metadata={"voice_config": job.variables.get("voice_config")},
                )
                voice_response = await self._voice_engine.generate(voice_request)
                job.metadata["voice_response"] = voice_response.text

            if MediaType.VIDEO in job.media_types and self._video_engine:
                self._notify_progress(job.id, 0.8, "Generating video...")
                video_request = GenerationRequest(
                    prompt=request.prompt,
                    metadata={"video_config": job.variables.get("video_config")},
                )
                video_response = await self._video_engine.generate(video_request)
                job.metadata["video_response"] = video_response.text

            # Complete
            job.status = GenerationStatus.COMPLETED
            job.completed_at = datetime.now()
            job.duration_ms = (time.time() - start_time) * 1000
            self._notify_progress(job.id, 1.0, "Completed")
            self.repository.save(job)
            logger.info(
                "Job %s completed in %.0fms", job.id, job.duration_ms
            )

        except Exception as exc:
            job.status = GenerationStatus.FAILED
            job.error = str(exc)
            job.completed_at = datetime.now()
            job.duration_ms = (time.time() - start_time) * 1000
            self._notify_progress(job.id, 0.0, f"Failed: {exc}")
            self.repository.save(job)
            logger.error("Job %s failed: %s", job.id, exc)
            raise

        return job

    def get_recent_jobs(self, limit: int = 50) -> list[GenerationJob]:
        """Get recent generation jobs from the database.

        Parameters
        ----------
        limit:
            Maximum number of jobs to return.

        Returns
        -------
        list[GenerationJob]
            List of recent jobs.
        """
        generations = self.repository.load_recent(limit)
        return [self._model_to_job(gen) for gen in generations]

    def _model_to_job(self, gen: Any) -> GenerationJob:
        """Convert a Generation model to a GenerationJob."""
        job = GenerationJob(
            id=gen.id,
            category=gen.category,
            template_name=gen.template_name,
            variables=self._safe_json_loads(gen.variables, {}),
            media_types=[MediaType(mt) for mt in self._safe_json_loads(gen.media_types, [])] if gen.media_types else [MediaType.TEXT],
            status=GenerationStatus(gen.status),
            error=gen.error,
            created_at=gen.created_at,
            completed_at=gen.completed_at,
            duration_ms=gen.duration_ms,
            metadata=self._safe_json_loads(gen.metadata, {}),
        )
        return job

    @staticmethod
    def _safe_json_loads(value: str | None, default: Any) -> Any:
        """Safely parse JSON with fallback."""
        if not value:
            return default
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return default

    def get_job(self, job_id: str) -> GenerationJob | None:
        """Get a job by ID.

        Parameters
        ----------
        job_id:
            Job ID to look up.

        Returns
        -------
        GenerationJob | None
            The job, or None if not found.
        """
        return self._jobs.get(job_id)

    def get_all_jobs(self) -> list[GenerationJob]:
        """Get all jobs.

        Returns
        -------
        list[GenerationJob]
            List of all jobs.
        """
        return list(self._jobs.values())

    def cancel_job(self, job_id: str) -> bool:
        """Cancel a pending or running job.

        Parameters
        ----------
        job_id:
            Job ID to cancel.

        Returns
        -------
        bool
            True if the job was cancelled.
        """
        job = self._jobs.get(job_id)
        if job and job.status in (GenerationStatus.PENDING, GenerationStatus.RUNNING):
            job.status = GenerationStatus.CANCELLED
            job.completed_at = datetime.now()
            self._notify_progress(job_id, 0.0, "Cancelled")
            return True
        return False
