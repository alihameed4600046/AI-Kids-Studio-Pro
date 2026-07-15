"""Tests for the SQLite database layer.

The tests exercise the public API of :class:`DatabaseManager` and verify
basic CRUD operations, transaction handling, and schema creation.
"""

import os
import yaml
from pathlib import Path
from datetime import datetime

import pytest

from src.database.database_manager import DatabaseManager
from config.config import Config


def _create_temp_config(tmp_path: Path) -> Path:
    cfg_path = tmp_path / "config.yaml"
    cfg = {
        "database": {"path": str(tmp_path / "test.db")},
    }
    cfg_path.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    return cfg_path


@pytest.fixture
def db(tmp_path: Path) -> DatabaseManager:
    cfg_path = _create_temp_config(tmp_path)
    # Ensure Config uses this file
    Config._instance = None  # reset singleton
    return DatabaseManager(cfg_path)


def test_database_creation(db: DatabaseManager):
    """Test that database file is created automatically."""
    assert db._db_path.exists()
    assert db._db_path.name == "test.db"


def test_schema_creation(db: DatabaseManager):
    """Test that all required tables are created."""
    tables = db.fetchall("SELECT name FROM sqlite_master WHERE type='table';")
    names = {row["name"] for row in tables}
    expected = {"projects", "settings", "history", "voices", "images", "videos", "schema_version"}
    assert expected.issubset(names)


def test_crud_operations(db: DatabaseManager):
    """Test insert, update, delete operations."""
    now = datetime.utcnow().isoformat()
    # Insert
    db.execute(
        "INSERT INTO projects (name, description, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        ("Test", "Desc", "draft", now, now),
    )
    proj = db.fetchall("SELECT * FROM projects WHERE name=?", ("Test",))[0]
    assert proj["name"] == "Test"
    proj_id = proj["id"]
    # Update
    db.execute("UPDATE projects SET status=? WHERE id=?", ("active", proj_id))
    updated = db.fetchall("SELECT status FROM projects WHERE id=?", (proj_id,))[0]
    assert updated["status"] == "active"
    # Delete
    db.execute("DELETE FROM projects WHERE id=?", (proj_id,))
    after = db.fetchall("SELECT * FROM projects WHERE id=?", (proj_id,))
    assert after == []


def test_fetchone(db: DatabaseManager):
    """Test fetchone method."""
    now = datetime.utcnow().isoformat()
    db.execute(
        "INSERT INTO projects (name, description, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        ("FetchOne", "Desc", "draft", now, now),
    )
    row = db.fetchone("SELECT * FROM projects WHERE name=?", ("FetchOne",))
    assert row is not None
    assert row["name"] == "FetchOne"
    # Test non-existent
    row = db.fetchone("SELECT * FROM projects WHERE name=?", ("NonExistent",))
    assert row is None


def test_fetchall(db: DatabaseManager):
    """Test fetchall method."""
    now = datetime.utcnow().isoformat()
    db.execute(
        "INSERT INTO projects (name, description, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        ("FetchAll1", "Desc", "draft", now, now),
    )
    db.execute(
        "INSERT INTO projects (name, description, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        ("FetchAll2", "Desc", "draft", now, now),
    )
    rows = db.fetchall("SELECT * FROM projects WHERE name LIKE ?", ("FetchAll%",))
    assert len(rows) == 2
    names = {row["name"] for row in rows}
    assert names == {"FetchAll1", "FetchAll2"}


def test_executemany(db: DatabaseManager):
    """Test executemany method."""
    now = datetime.utcnow().isoformat()
    data = [
        ("Many1", "Desc", "draft", now, now),
        ("Many2", "Desc", "draft", now, now),
        ("Many3", "Desc", "draft", now, now),
    ]
    db.executemany(
        "INSERT INTO projects (name, description, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        data,
    )
    rows = db.fetchall("SELECT name FROM projects WHERE name LIKE ?", ("Many%",))
    assert len(rows) == 3


def test_transaction_and_rollback(db: DatabaseManager):
    """Test transaction context manager with rollback on exception."""
    now = datetime.utcnow().isoformat()
    with pytest.raises(RuntimeError):
        with db.transaction() as cur:
            cur.execute(
                "INSERT INTO projects (name, description, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                ("Rollback", "Desc", "draft", now, now),
            )
            raise RuntimeError("abort")
    # Ensure rollback
    rows = db.fetchall("SELECT * FROM projects WHERE name=?", ("Rollback",))
    assert rows == []


def test_transaction_commit(db: DatabaseManager):
    """Test transaction context manager commits on success."""
    now = datetime.utcnow().isoformat()
    with db.transaction() as cur:
        cur.execute(
            "INSERT INTO projects (name, description, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            ("CommitTest", "Desc", "draft", now, now),
        )
    # Ensure commit
    rows = db.fetchall("SELECT * FROM projects WHERE name=?", ("CommitTest",))
    assert len(rows) == 1
    assert rows[0]["name"] == "CommitTest"


def test_commit_rollback_methods(db: DatabaseManager):
    """Test explicit commit and rollback methods."""
    now = datetime.utcnow().isoformat()
    # Test commit - use transaction context to test commit/rollback
    with db.transaction() as cur:
        cur.execute(
            "INSERT INTO projects (name, description, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            ("ExplicitCommit", "Desc", "draft", now, now),
        )
    # Transaction committed automatically
    rows = db.fetchall("SELECT * FROM projects WHERE name=?", ("ExplicitCommit",))
    assert len(rows) == 1

    # Test rollback - use transaction context
    with db.transaction() as cur:
        cur.execute(
            "INSERT INTO projects (name, description, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            ("ExplicitRollback", "Desc", "draft", now, now),
        )
        # Explicit rollback
        db.rollback()
    # Transaction rolled back
    rows = db.fetchall("SELECT * FROM projects WHERE name=?", ("ExplicitRollback",))
    assert rows == []


def test_open_close(db: DatabaseManager):
    """Test open and close methods."""
    # Close the connection
    db.close()
    assert db._conn is None

    # Reopen
    db.open()
    assert db._conn is not None

    # Verify it works after reopen
    now = datetime.utcnow().isoformat()
    db.execute(
        "INSERT INTO projects (name, description, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        ("ReopenTest", "Desc", "draft", now, now),
    )
    row = db.fetchone("SELECT * FROM projects WHERE name=?", ("ReopenTest",))
    assert row is not None
    assert row["name"] == "ReopenTest"


def test_context_manager(db: DatabaseManager):
    """Test DatabaseManager as context manager."""
    now = datetime.utcnow().isoformat()
    with DatabaseManager(db._config._path) as db_mgr:
        db_mgr.execute(
            "INSERT INTO projects (name, description, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            ("ContextTest", "Desc", "draft", now, now),
        )
    # Connection should be closed after context exit
    row = db.fetchone("SELECT * FROM projects WHERE name=?", ("ContextTest",))
    assert row is not None
    assert row["name"] == "ContextTest"


def test_foreign_keys_enabled(db: DatabaseManager):
    """Test that foreign keys are enabled."""
    # This test verifies foreign key constraints work
    now = datetime.utcnow().isoformat()
    # Insert a project
    db.execute(
        "INSERT INTO projects (name, description, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        ("FKTest", "Desc", "draft", now, now),
    )
    proj = db.fetchone("SELECT id FROM projects WHERE name=?", ("FKTest",))
    proj_id = proj["id"]

    # Insert an image referencing the project
    db.execute(
        "INSERT INTO images (project_id, prompt, file_path, created_at) VALUES (?, ?, ?, ?)",
        (proj_id, "test prompt", "/path/to/image.png", now),
    )
    img = db.fetchone("SELECT * FROM images WHERE project_id=?", (proj_id,))
    assert img is not None
    assert img["project_id"] == proj_id

    # Delete project should cascade delete image
    db.execute("DELETE FROM projects WHERE id=?", (proj_id,))
    img_after = db.fetchone("SELECT * FROM images WHERE project_id=?", (proj_id,))
    assert img_after is None


def test_settings_table(db: DatabaseManager):
    """Test settings table operations."""
    db.execute("INSERT INTO settings (key, value, updated_at) VALUES (?, ?, ?)", ("test_key", "test_value", datetime.utcnow().isoformat()))
    row = db.fetchone("SELECT * FROM settings WHERE key=?", ("test_key",))
    assert row is not None
    assert row["value"] == "test_value"

    # Update
    db.execute("UPDATE settings SET value=?, updated_at=? WHERE key=?", ("new_value", datetime.utcnow().isoformat(), "test_key"))
    row = db.fetchone("SELECT * FROM settings WHERE key=?", ("test_key",))
    assert row["value"] == "new_value"


def test_history_table(db: DatabaseManager):
    """Test history table operations."""
    now = datetime.utcnow().isoformat()
    db.execute("INSERT INTO history (action, details, created_at) VALUES (?, ?, ?)", ("test_action", "test_details", now))
    rows = db.fetchall("SELECT * FROM history WHERE action=?", ("test_action",))
    assert len(rows) == 1
    assert rows[0]["details"] == "test_details"


def test_voices_table(db: DatabaseManager):
    """Test voices table operations."""
    now = datetime.utcnow().isoformat()
    db.execute("INSERT INTO voices (name, provider, language, voice_id, created_at) VALUES (?, ?, ?, ?, ?)", ("TestVoice", "test_provider", "en", "voice_123", now))
    rows = db.fetchall("SELECT * FROM voices WHERE name=?", ("TestVoice",))
    assert len(rows) == 1
    assert rows[0]["provider"] == "test_provider"
    assert rows[0]["language"] == "en"


def test_videos_table(db: DatabaseManager):
    """Test videos table operations."""
    now = datetime.utcnow().isoformat()
    # First create a project
    db.execute(
        "INSERT INTO projects (name, description, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        ("VideoProject", "Desc", "draft", now, now),
    )
    proj = db.fetchone("SELECT id FROM projects WHERE name=?", ("VideoProject",))
    proj_id = proj["id"]
    
    db.execute(
        "INSERT INTO videos (project_id, title, file_path, duration, created_at) VALUES (?, ?, ?, ?, ?)",
        (proj_id, "Test Video", "/path/to/video.mp4", 120.5, now),
    )
    rows = db.fetchall("SELECT * FROM videos WHERE title=?", ("Test Video",))
    assert len(rows) == 1
    assert rows[0]["duration"] == 120.5
