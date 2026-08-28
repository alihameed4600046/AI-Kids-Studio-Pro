"""Video generation engines for AI Kids Studio Pro.

This module provides video generation engines including Agnes AI
text-to-video generation.
"""

from __future__ import annotations

import asyncio
import base64
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Sequence

import aiohttp

from src.engine.ai_engine import (
    AIEngine,
    AIEngineError,
    AuthenticationError,
    ContentFilterError,
    EngineConfig,
    EngineState,
    GenerationRequest,
    GenerationResponse,
    RateLimitError,
)
from src.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


class VideoResolution(Enum):
    """Supported video resolutions."""

    SD = "640x480"
    HD = "1280x720"
    FULL_HD = "1920x1080"
    ULTRA_HD = "3840x2160"
    VERTICAL = "720x1280"
    SQUARE = "1080x1080"


class VideoFormat(Enum):
    """Supported video formats."""

    MP4 = "mp4"
    WEBM = "webm"
    AVI = "avi"
    MOV = "mov"


@dataclass
class VideoConfig:
    """Configuration for video generation."""

    duration: float = 5.0
    fps: int = 24
    resolution: VideoResolution = VideoResolution.HD
    format: VideoFormat = VideoFormat.MP4
    seed: int | None = None
    motion_scale: float = 1.0
    guidance_scale: float = 7.5

    def __post_init__(self) -> None:
        if self.duration < 1.0 or self.duration > 60.0:
            raise ValueError("Duration must be between 1 and 60 seconds")
        if self.fps not in (12, 15, 24, 25, 30, 48, 60):
            raise ValueError("FPS must be a standard frame rate")
        if self.motion_scale < 0.0 or self.motion_scale > 10.0:
            raise ValueError("Motion scale must be between 0 and 10")
        if self.guidance_scale < 0.0 or self.guidance_scale > 30.0:
            raise ValueError("Guidance scale must be between 0 and 30")


class VideoEngine(AIEngine, ABC):
    """Abstract base class for video generation engines."""

    def __init__(self, config: EngineConfig | None = None) -> None:
        super().__init__(config)
        self.video_config = VideoConfig()

    @abstractmethod
    async def generate_video(
        self,
        prompt: str,
        config: VideoConfig | None = None,
    ) -> bytes:
        """Generate a video from a text prompt.

        Parameters
        ----------
        prompt:
            Text description of the video to generate.
        config:
            Video generation configuration.

        Returns
        -------
        bytes
            Generated video data.
        """
        if self._state != EngineState.READY:
            raise EngineNotReadyError(
                f"Video engine {self.__class__.__name__} is not ready",
                provider=self._config.provider,
            )

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        """Generate a video from a GenerationRequest.

        Parameters
        ----------
        request:
            Generation request with prompt and metadata.

        Returns
        -------
        GenerationResponse
            Response with video data as base64-encoded string.
        """
        if self._state != EngineState.READY:
            raise EngineNotReadyError(
                f"Video engine {self.__class__.__name__} is not ready",
                provider=self._config.provider,
            )

        self._state = EngineState.GENERATING
        start_time = time.time()

        try:
            video_data = await self.generate_video(
                request.prompt,
                request.metadata.get("video_config"),
            )
            latency = (time.time() - start_time) * 1000

            video_b64 = base64.b64encode(video_data).decode("utf-8")
            self._record_success()
            self._state = EngineState.READY

            return GenerationResponse(
                text=f"data:video/mp4;base64,{video_b64}",
                model=request.model or self._config.model,
                provider=self._config.provider,
                tokens_used=len(request.prompt.split()),
                finish_reason="success",
                latency_ms=latency,
                metadata={"video_format": VideoFormat.MP4.value, "size": len(video_data)},
            )
        except Exception as exc:
            self._record_error(exc)
            self._state = EngineState.ERROR
            raise AIEngineError(
                f"Video generation failed: {exc}", provider=self._config.provider
            ) from exc

    async def stream(self, request: GenerationRequest):
        """Video engines don't support streaming."""
        raise NotImplementedError("Video generation does not support streaming")

    async def validate(self) -> bool:
        """Validate video engine connectivity."""
        return self._state == EngineState.READY


class AgnesVideoEngine(VideoEngine):
    """Agnes AI video generation engine.

    Agnes AI provides free text-to-video generation.
    """

    def __init__(self, config: EngineConfig | None = None) -> None:
        if config is None:
            config = EngineConfig(
                provider="agnes_ai",
                model="agnes-video",
                api_key=None,
                timeout=120.0,
            )
        super().__init__(config)
        self.base_url = "https://api.agnes-ai.com/v1"

    async def initialize(self) -> None:
        """Initialize the Agnes video engine."""
        self._state = EngineState.LOADING
        if not self._config.api_key:
            logger.warning("No API key provided for Agnes AI")
        self._state = EngineState.READY
        logger.info("Agnes video engine initialized")

    async def generate_video(
        self,
        prompt: str,
        config: VideoConfig | None = None,
    ) -> bytes:
        """Generate video using Agnes AI.

        Parameters
        ----------
        prompt:
            Text description of the video.
        config:
            Video generation configuration.

        Returns
        -------
        bytes
            Generated video data.
        """
        config = config or self.video_config
        self._state = EngineState.GENERATING

        headers = {
            "Authorization": f"Bearer {self._config.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "prompt": prompt,
            "duration": config.duration,
            "fps": config.fps,
            "resolution": config.resolution.value,
            "motion_scale": config.motion_scale,
            "guidance_scale": config.guidance_scale,
        }
        if config.seed is not None:
            payload["seed"] = config.seed

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/videos/generate",
                    json=payload,
                    headers=headers,
                    timeout=self._config.timeout,
                ) as response:
                    if response.status == 401:
                        raise AuthenticationError(
                            "Invalid Agnes AI key", provider=self._config.provider
                        )
                    if response.status == 429:
                        raise RateLimitError(
                            "Agnes AI rate limit exceeded",
                            provider=self._config.provider,
                        )
                    if response.status == 400:
                        error_text = await response.text()
                        raise ContentFilterError(
                            f"Content filtered: {error_text}",
                            provider=self._config.provider,
                        )

                    result = await response.json()
                    video_url = result.get("video_url") or result.get("url")

                    if not video_url:
                        raise AIEngineError(
                            "No video URL in response",
                            provider=self._config.provider,
                        )

                    async with session.get(video_url) as video_response:
                        video_data = await video_response.read()

                    self._record_success()
                    self._state = EngineState.READY
                    return video_data
        except AIEngineError:
            raise
        except Exception as exc:
            self._state = EngineState.ERROR
            raise AIEngineError(
                f"Agnes video generation failed: {exc}",
                provider=self._config.provider,
            ) from exc


class MockVideoEngine(VideoEngine):
    """Mock video engine for testing."""

    def __init__(self, config: EngineConfig | None = None) -> None:
        if config is None:
            config = EngineConfig(provider="mock", model="mock-video")
        super().__init__(config)
        self.latency_ms = 500.0

    async def initialize(self) -> None:
        """Initialize the mock video engine."""
        await asyncio.sleep(0.01)
        self._state = EngineState.READY
        logger.info("Mock video engine initialized")

    async def generate_video(
        self,
        prompt: str,
        config: VideoConfig | None = None,
    ) -> bytes:
        """Generate a mock video.

        Parameters
        ----------
        prompt:
            Text description of the video.
        config:
            Video generation configuration.

        Returns
        -------
        bytes
            Mock video data.
        """
        await asyncio.sleep(self.latency_ms / 1000.0)
        self._record_success()
        return b"MOCK_VIDEO_DATA"

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        """Generate a mock video response."""
        if self._state != EngineState.READY:
            raise EngineNotReadyError(
                "Mock video engine is not ready", provider=self._config.provider
            )

        self._state = EngineState.GENERATING
        start_time = time.time()

        try:
            video_data = await self.generate_video(
                request.prompt, request.metadata.get("video_config")
            )
            latency = (time.time() - start_time) * 1000
            self._record_success()
            self._state = EngineState.READY

            return GenerationResponse(
                text="[Mock video generated]",
                model=request.model or self._config.model,
                provider=self._config.provider,
                tokens_used=len(request.prompt.split()),
                finish_reason="success",
                latency_ms=latency,
                metadata={"mock": True},
            )
        except Exception as exc:
            self._record_error(exc)
            self._state = EngineState.ERROR
            raise
