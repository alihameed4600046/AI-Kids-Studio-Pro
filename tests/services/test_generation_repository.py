"""Tests for the GenerationRepository persistence layer."""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path

import pytest
import yaml

from config.config import Config
from src.database.database_manager import DatabaseManager
from src.database.models import Generation
from src.engine.ai_engine import GenerationResponse
from src.engine.mock_engine import MockModelManager
from src.engine.model_manager import ProviderConfig, ProviderType
from src.engine.prompt_engine import PromptEngine
from src.services.generation_repository import GenerationRepository
from src.services.generation_service import GenerationService, GenerationJob, MediaType, GenerationStatus


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


def _make_job(**overrides) -> GenerationJob:
    now = datetime.now()
    job = GenerationJob(
        id="job-1",
        category="stories",
        template_name="story",
        variables={"name": "Alice", "age": "10"},
        media_types=[MediaType.TEXT, MediaType.IMAGE],
        status=GenerationStatus.COMPLETED,
        result=GenerationResponse(
            text="Once upon a time...",
            model="mock",
            provider="mock",
        ),
        error=None,
        created_at=now,
        completed_at=now + timedelta(seconds=2),
        duration_ms=2000.0,
        metadata={"theme": "fantasy", "nested": {"key": "value"}},
    )
    for key, value in overrides.items():
        setattr(job, key, value)
    return job


class TestGenerationRepository:
    """Tests for GenerationRepository."""

    def test_save_generation_job(self, repository: GenerationRepository) -> None:
        job = _make_job()
        repository.save(job)

        row = repository.db.fetchone(
            "SELECT * FROM generations WHERE id = ?", (job.id,)
        )
        assert row is not None
        assert row["id"] == "job-1"
        assert row["category"] == "stories"
        assert row["template_name"] == "story"

    def test_load_generation_job(self, repository: GenerationRepository) -> None:
        job = _make_job()
        repository.save(job)
        loaded = repository.load(job.id)

        assert loaded is not None
        assert loaded.id == "job-1"
        assert loaded.category == "stories"
        assert loaded.template_name == "story"
        assert loaded.variables == '{"name": "Alice", "age": "10"}'
        assert loaded.media_types == '["text", "image"]'
        assert loaded.status == "completed"
        assert loaded.error is None
        assert isinstance(loaded.created_at, datetime)
        assert isinstance(loaded.completed_at, datetime)
        assert loaded.duration_ms == 2000.0
        assert loaded.metadata == '{"theme": "fantasy", "nested": {"key": "value"}}'

    def test_load_nonexistent_job(self, repository: GenerationRepository) -> None:
        loaded = repository.load("does-not-exist")
        assert loaded is None

    def test_load_recent(self, repository: GenerationRepository, tmp_path: Path) -> None:
        base_time = datetime.now()
        for i in range(5):
            job = _make_job(
                id=f"job-{i}",
                category="stories" if i < 3 else "images",
                created_at=base_time + timedelta(seconds=i),
            )
            repository.save(job)

        recent = repository.load_recent(limit=3)
        assert len(recent) == 3
        assert [r.id for r in recent] == ["job-4", "job-3", "job-2"]

    def test_load_by_category(self, repository: GenerationRepository) -> None:
        base_time = datetime.now()
        for i in range(4):
            job = _make_job(
                id=f"job-{i}",
                category="stories" if i < 2 else "images",
                created_at=base_time + timedelta(seconds=i),
            )
            repository.save(job)

        stories = repository.load_by_category("stories", limit=10)
        assert len(stories) == 2
        assert all(s.category == "stories" for s in stories)

        images = repository.load_by_category("images", limit=10)
        assert len(images) == 2
        assert all(i.category == "images" for i in images)

        empty = repository.load_by_category("videos", limit=10)
        assert len(empty) == 0

    def test_delete_generation_job(self, repository: GenerationRepository) -> None:
        job = _make_job()
        repository.save(job)

        deleted = repository.delete(job.id)
        assert deleted is True

        loaded = repository.load(job.id)
        assert loaded is None

        deleted_again = repository.delete(job.id)
        assert deleted_again is False

    def test_json_round_trip(self, repository: GenerationRepository) -> None:
        job = _make_job()
        repository.save(job)
        loaded = repository.load(job.id)

        assert loaded is not None
        variables = json.loads(loaded.variables)
        assert variables == {"name": "Alice", "age": "10"}
        metadata = json.loads(loaded.metadata)
        assert metadata == {"theme": "fantasy", "nested": {"key": "value"}}

    def test_enum_round_trip_via_service(self, tmp_path: Path) -> None:
        db = _create_isolated_db(tmp_path, "enum_test.db")
        try:
            repo = GenerationRepository(db_manager=db)
            prompts_dir = tmp_path / "prompts"
            prompts_dir.mkdir()
            (prompts_dir / "test.yaml").write_text('prompt: "Hello {{name}}!"', encoding="utf-8")
            prompt_engine = PromptEngine(prompts_dir=prompts_dir)
            prompt_engine.load_all_templates()

            service = GenerationService(
                prompt_engine=prompt_engine,
                model_manager=MockModelManager(),
                repository=repo,
            )
            job = GenerationJob(
                category="stories",
                template_name="test",
                variables={"name": "World"},
                media_types=[MediaType.TEXT, MediaType.IMAGE],
                status=GenerationStatus.COMPLETED,
            )
            repo.save(job)
            recent = service.get_recent_jobs(limit=1)
            assert len(recent) == 1
            assert recent[0].media_types == [MediaType.TEXT, MediaType.IMAGE]
            assert recent[0].status == GenerationStatus.COMPLETED
        finally:
            db.close()
            DatabaseManager._instance = None
