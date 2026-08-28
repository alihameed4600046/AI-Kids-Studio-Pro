"""Tests for the generations database schema."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from config.config import Config
from src.database.database_manager import DatabaseManager


def _create_temp_config(tmp_path: Path, db_name: str = "test.db") -> Path:
    cfg_path = tmp_path / "config.yaml"
    cfg = {
        "database": {"path": str(tmp_path / db_name)},
    }
    cfg_path.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    return cfg_path


@pytest.fixture
def db(tmp_path: Path) -> DatabaseManager:
    cfg_path = _create_temp_config(tmp_path)
    DatabaseManager._instance = None
    return DatabaseManager(cfg_path)


def test_generations_table_exists(db: DatabaseManager) -> None:
    tables = db.fetchall(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='generations';"
    )
    assert len(tables) == 1
    assert tables[0]["name"] == "generations"


def test_generations_table_columns(db: DatabaseManager) -> None:
    columns = db.fetchall("PRAGMA table_info(generations);")
    column_names = {row["name"] for row in columns}
    expected = {
        "id",
        "category",
        "template_name",
        "variables",
        "media_types",
        "status",
        "result",
        "error",
        "created_at",
        "completed_at",
        "duration_ms",
        "metadata",
    }
    assert expected == column_names
