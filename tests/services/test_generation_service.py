"""Tests for the GenerationService orchestration layer."""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
import yaml

from config.config import Config
from src.database.database_manager import DatabaseManager
from src.engine.ai_engine import (
    AIEngineError,
    EngineConfig,
    EngineState,
    GenerationRequest,
    GenerationResponse,
)
from src.engine.mock_engine import MockModelManager, MockScenario
from src.engine.model_manager import ModelManager, ProviderConfig, ProviderType
from src.engine.prompt_engine import PromptEngine
from src.services.generation_repository import GenerationRepository
from src.services.generation_service import (
    GenerationJob,
    GenerationService,
    MediaType,
    GenerationStatus,
)


def _create_temp_config(tmp_path: Path, db_name: str = "test.db") -> Path:
    cfg_path = tmp_path / "config.yaml"
    cfg = {
        "database": {"path": str(tmp_path / db_name)},
    }
    cfg_path.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    return cfg_path


def _create_isolated_db(tmp_path: Path, db_name: str = "test.db") -> DatabaseManager:
    cfg_path = _create_temp_config(tmp_path, db_name)
    DatabaseManager._instance = None
    return DatabaseManager(cfg_path)


@pytest.fixture
def db(tmp_path: Path):
    database = _create_isolated_db(tmp_path)
    yield database
    database.close()
    DatabaseManager._instance = None


@pytest.fixture
def repository(db: DatabaseManager) -> GenerationRepository:
    return GenerationRepository(db_manager=db)


@pytest.fixture
def prompt_engine(tmp_path: Path) -> PromptEngine:
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    (prompts_dir / "story.yaml").write_text(
        'prompt: "Once upon a time, {{name}} went on an adventure!"',
        encoding="utf-8",
    )
    engine = PromptEngine(prompts_dir=prompts_dir)
    engine.load_all_templates()
    return engine


@pytest.fixture
def model_manager() -> MockModelManager:
    return MockModelManager()


@pytest.fixture
def service(
    tmp_path: Path,
    prompt_engine: PromptEngine,
    model_manager: MockModelManager,
    repository: GenerationRepository,
) -> GenerationService:
    return GenerationService(
        prompt_engine=prompt_engine,
        model_manager=model_manager,
        repository=repository,
    )


class FakeImageEngine:
    async def generate(self, request):
        return GenerationResponse(text="mock_image_data", model="mock", provider="mock")


class FakeVoiceEngine:
    async def generate(self, request):
        return GenerationResponse(text="mock_voice_data", model="mock", provider="mock")


class FakeVideoEngine:
    async def generate(self, request):
        return GenerationResponse(text="mock_video_data", model="mock", provider="mock")


class TestGenerationService:
    """Tests for GenerationService."""

    def test_create_job(self, service: GenerationService) -> None:
        job = service.create_job(
            category="stories",
            template_name="story",
            variables={"name": "Alice"},
            media_types=[MediaType.TEXT],
        )
        assert job.id is not None
        assert job.category == "stories"
        assert job.template_name == "story"
        assert job.variables == {"name": "Alice"}
        assert job.media_types == [MediaType.TEXT]
        assert job.status == GenerationStatus.PENDING
        assert service.get_job(job.id) == job

    def test_get_all_jobs(self, service: GenerationService) -> None:
        job1 = service.create_job("stories", "story", {"name": "Alice"})
        job2 = service.create_job("images", "prompt", {"style": "cartoon"})
        all_jobs = service.get_all_jobs()
        assert len(all_jobs) == 2
        assert job1 in all_jobs
        assert job2 in all_jobs

    @pytest.mark.asyncio
    async def test_execute_job_success(self, service: GenerationService, tmp_path: Path) -> None:
        job = service.create_job(
            category="stories",
            template_name="story",
            variables={"name": "Alice"},
            media_types=[MediaType.TEXT],
        )
        completed = await service.execute_job(job)

        assert completed.status == GenerationStatus.COMPLETED
        assert completed.result is not None
        assert completed.result.text == "This is a mock response from the AI engine."
        assert completed.error is None
        assert completed.completed_at is not None
        assert completed.duration_ms is not None
        assert completed.duration_ms >= 0

        loaded = service.repository.load(job.id)
        assert loaded is not None
        assert loaded.status == "completed"

    @pytest.mark.asyncio
    async def test_execute_job_failure(self, service: GenerationService) -> None:
        service.model_manager.mock_engine.set_scenario(MockScenario.RATE_LIMIT)
        job = service.create_job(
            category="stories",
            template_name="story",
            variables={"name": "Alice"},
        )

        with pytest.raises(Exception, match="rate limit"):
            await service.execute_job(job)

        assert job.status == GenerationStatus.FAILED
        assert job.error is not None
        assert "rate limit" in job.error.lower()
        assert job.completed_at is not None
        assert job.duration_ms is not None

        loaded = service.repository.load(job.id)
        assert loaded is not None
        assert loaded.status == "failed"

    @pytest.mark.asyncio
    async def test_progress_callbacks(self, service: GenerationService) -> None:
        progress_log: list[tuple[str, float, str]] = []
        service.register_progress_callback(lambda jid, progress, status: progress_log.append((jid, progress, status)))

        job = service.create_job("stories", "story", {"name": "Alice"})
        await service.execute_job(job)

        statuses = [status for _, _, status in progress_log]
        assert "Starting generation..." in statuses
        assert "Building prompt..." in statuses
        assert "Generating text..." in statuses
        assert "Completed" in statuses
        assert job.status == GenerationStatus.COMPLETED

    def test_get_recent_jobs(self, service: GenerationService, tmp_path: Path) -> None:
        base_time = datetime.now()
        for i in range(3):
            job = GenerationJob(
                id=f"recent-{i}",
                category="stories",
                template_name="story",
                variables={"name": str(i)},
                media_types=[MediaType.TEXT],
                status=GenerationStatus.COMPLETED,
                created_at=base_time + timedelta(seconds=i),
            )
            service.repository.save(job)

        recent = service.get_recent_jobs(limit=2)
        assert len(recent) == 2
        assert recent[0].id == "recent-2"
        assert recent[1].id == "recent-1"

    def test_get_job(self, service: GenerationService) -> None:
        job = service.create_job("stories", "story", {"name": "Alice"})
        assert service.get_job(job.id) == job
        assert service.get_job("nonexistent") is None

    def test_cancel_job(self, service: GenerationService) -> None:
        pending_job = service.create_job("stories", "story", {"name": "Alice"})
        assert service.cancel_job(pending_job.id) is True
        assert pending_job.status == GenerationStatus.CANCELLED

        running_job = service.create_job("stories", "story", {"name": "Bob"})
        running_job.status = GenerationStatus.RUNNING
        assert service.cancel_job(running_job.id) is True
        assert running_job.status == GenerationStatus.CANCELLED

        completed_job = service.create_job("stories", "story", {"name": "Carol"})
        completed_job.status = GenerationStatus.COMPLETED
        assert service.cancel_job(completed_job.id) is False
        assert completed_job.status == GenerationStatus.COMPLETED

        assert service.cancel_job("nonexistent") is False

    @pytest.mark.asyncio
    async def test_text_only_generation(self, service: GenerationService) -> None:
        job = service.create_job(
            category="stories",
            template_name="story",
            variables={"name": "Alice"},
            media_types=[MediaType.TEXT],
        )
        await service.execute_job(job)
        assert job.status == GenerationStatus.COMPLETED
        assert "image_response" not in job.metadata
        assert "voice_response" not in job.metadata
        assert "video_response" not in job.metadata

    @pytest.mark.asyncio
    async def test_image_branch(self, service: GenerationService) -> None:
        service.set_image_engine(FakeImageEngine())
        job = service.create_job(
            category="images",
            template_name="story",
            variables={"name": "Alice"},
            media_types=[MediaType.TEXT, MediaType.IMAGE],
        )
        await service.execute_job(job)
        assert job.status == GenerationStatus.COMPLETED
        assert "image_response" in job.metadata
        assert job.metadata["image_response"] == "mock_image_data"

    @pytest.mark.asyncio
    async def test_voice_branch(self, service: GenerationService) -> None:
        service.set_voice_engine(FakeVoiceEngine())
        job = service.create_job(
            category="audio",
            template_name="story",
            variables={"name": "Alice"},
            media_types=[MediaType.TEXT, MediaType.VOICE],
        )
        await service.execute_job(job)
        assert job.status == GenerationStatus.COMPLETED
        assert "voice_response" in job.metadata
        assert job.metadata["voice_response"] == "mock_voice_data"

    @pytest.mark.asyncio
    async def test_video_branch(self, service: GenerationService) -> None:
        service.set_video_engine(FakeVideoEngine())
        job = service.create_job(
            category="videos",
            template_name="story",
            variables={"name": "Alice"},
            media_types=[MediaType.TEXT, MediaType.VIDEO],
        )
        await service.execute_job(job)
        assert job.status == GenerationStatus.COMPLETED
        assert "video_response" in job.metadata
        assert job.metadata["video_response"] == "mock_video_data"

    @pytest.mark.asyncio
    async def test_combined_media(self, service: GenerationService) -> None:
        service.set_image_engine(FakeImageEngine())
        service.set_voice_engine(FakeVoiceEngine())
        service.set_video_engine(FakeVideoEngine())
        job = service.create_job(
            category="combined",
            template_name="story",
            variables={"name": "Alice"},
            media_types=[MediaType.TEXT, MediaType.IMAGE, MediaType.VOICE, MediaType.VIDEO],
        )
        await service.execute_job(job)
        assert job.status == GenerationStatus.COMPLETED
        assert job.metadata["image_response"] == "mock_image_data"
        assert job.metadata["voice_response"] == "mock_voice_data"
        assert job.metadata["video_response"] == "mock_video_data"


class TestGenerationServiceEngineLifecycle:
    """Tests for engine lifecycle management in GenerationService."""

    @pytest.mark.asyncio
    async def test_execute_job_shuts_down_lazily_initialized_engine(
        self,
        tmp_path: Path,
        db: DatabaseManager,
        repository: GenerationRepository,
        prompt_engine: PromptEngine,
    ) -> None:
        """execute_job shuts down engines that were lazily initialized during the job."""
        mock_engine = MagicMock()
        mock_engine.is_ready = False
        mock_engine.state = EngineState.IDLE

        def _make_ready() -> None:
            mock_engine.is_ready = True
            mock_engine.state = EngineState.READY

        mock_engine.initialize = AsyncMock(side_effect=_make_ready)
        mock_engine.generate = AsyncMock(
            return_value=GenerationResponse(
                text="mock response", model="mock", provider="mock"
            )
        )
        mock_engine.shutdown = AsyncMock()

        mm = ModelManager()
        mm.register_provider(
            ProviderConfig(
                provider_type=ProviderType.OPENROUTER,
                api_key="test-key",
                base_url="http://mock",
                models=["mock"],
                enabled=True,
                priority=1,
                metadata={"supported_tasks": ["text_generation"]},
            )
        )
        mm.register_engine(ProviderType.OPENROUTER, mock_engine)

        service = GenerationService(
            prompt_engine=prompt_engine,
            model_manager=mm,
            repository=repository,
        )

        job = service.create_job(
            category="stories",
            template_name="story",
            variables={"name": "Alice"},
            media_types=[MediaType.TEXT],
        )
        completed = await service.execute_job(job)

        assert completed.status == GenerationStatus.COMPLETED
        mock_engine.initialize.assert_called_once()
        mock_engine.shutdown.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_job_does_not_shut_down_already_ready_engine(
        self,
        tmp_path: Path,
        db: DatabaseManager,
        repository: GenerationRepository,
        prompt_engine: PromptEngine,
    ) -> None:
        """execute_job does not shut down engines that were already ready before the job."""
        mock_engine = MagicMock()
        mock_engine.is_ready = True
        mock_engine.state = EngineState.READY
        mock_engine.initialize = AsyncMock()
        mock_engine.generate = AsyncMock(
            return_value=GenerationResponse(
                text="mock response", model="mock", provider="mock"
            )
        )
        mock_engine.shutdown = AsyncMock()

        mm = ModelManager()
        mm.register_provider(
            ProviderConfig(
                provider_type=ProviderType.OPENROUTER,
                api_key="test-key",
                base_url="http://mock",
                models=["mock"],
                enabled=True,
                priority=1,
                metadata={"supported_tasks": ["text_generation"]},
            )
        )
        mm.register_engine(ProviderType.OPENROUTER, mock_engine)

        service = GenerationService(
            prompt_engine=prompt_engine,
            model_manager=mm,
            repository=repository,
        )

        job = service.create_job(
            category="stories",
            template_name="story",
            variables={"name": "Alice"},
            media_types=[MediaType.TEXT],
        )
        completed = await service.execute_job(job)

        assert completed.status == GenerationStatus.COMPLETED
        mock_engine.initialize.assert_not_called()
        mock_engine.shutdown.assert_not_called()

    @pytest.mark.asyncio
    async def test_execute_job_shuts_down_engine_on_failure(
        self,
        tmp_path: Path,
        db: DatabaseManager,
        repository: GenerationRepository,
        prompt_engine: PromptEngine,
    ) -> None:
        """execute_job shuts down lazily initialized engines even when generation fails."""
        mock_engine = MagicMock()
        mock_engine.is_ready = False
        mock_engine.state = EngineState.IDLE

        def _make_ready() -> None:
            mock_engine.is_ready = True
            mock_engine.state = EngineState.READY

        mock_engine.initialize = AsyncMock(side_effect=_make_ready)
        mock_engine.generate = AsyncMock(
            side_effect=AIEngineError("mock error", provider="mock")
        )
        mock_engine.shutdown = AsyncMock()

        mm = ModelManager()
        mm.register_provider(
            ProviderConfig(
                provider_type=ProviderType.OPENROUTER,
                api_key="test-key",
                base_url="http://mock",
                models=["mock"],
                enabled=True,
                priority=1,
                metadata={"supported_tasks": ["text_generation"]},
            )
        )
        mm.register_engine(ProviderType.OPENROUTER, mock_engine)

        service = GenerationService(
            prompt_engine=prompt_engine,
            model_manager=mm,
            repository=repository,
        )

        job = service.create_job(
            category="stories",
            template_name="story",
            variables={"name": "Alice"},
            media_types=[MediaType.TEXT],
        )

        with pytest.raises(AIEngineError):
            await service.execute_job(job)

        mock_engine.initialize.assert_called_once()
        mock_engine.shutdown.assert_called_once()
