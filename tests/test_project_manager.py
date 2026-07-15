"""Tests for the Project Manager.

The tests exercise the public API of :class:`ProjectManager` and verify
basic CRUD operations, search, history logging, and statistics.
"""

import yaml
from pathlib import Path
from datetime import datetime

import pytest

from src.project.project_manager import ProjectManager
from config.config import Config


def _create_temp_config(tmp_path: Path) -> Path:
    cfg_path = tmp_path / "config.yaml"
    cfg = {
        "database": {"path": str(tmp_path / "test.db")},
    }
    cfg_path.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    return cfg_path


@pytest.fixture
def pm(tmp_path: Path) -> ProjectManager:
    cfg_path = _create_temp_config(tmp_path)
    # Ensure Config uses this file
    Config._instance = None  # reset singleton
    # Reset ProjectManager singleton to get a fresh instance with new config
    ProjectManager._instance = None
    # Also reset DatabaseManager singleton to get a fresh database connection
    from src.database.database_manager import DatabaseManager
    DatabaseManager._instance = None
    return ProjectManager(cfg_path)


def test_create_project(pm: ProjectManager):
    """Test creating a new project."""
    project_id = pm.create_project("Test Project", "A test description", "draft")
    assert project_id > 0

    project = pm.get_project(project_id)
    assert project is not None
    assert project["name"] == "Test Project"
    assert project["description"] == "A test description"
    assert project["status"] == "draft"


def test_get_project_by_name(pm: ProjectManager):
    """Test retrieving a project by name."""
    pm.create_project("Named Project", "Description", "active")
    project = pm.get_project_by_name("Named Project")
    assert project is not None
    assert project["name"] == "Named Project"
    assert project["status"] == "active"

    # Non-existent project
    project = pm.get_project_by_name("NonExistent")
    assert project is None


def test_list_projects(pm: ProjectManager):
    """Test listing projects with filters."""
    pm.create_project("Project 1", "Desc", "draft")
    pm.create_project("Project 2", "Desc", "active")
    pm.create_project("Project 3", "Desc", "completed")

    all_projects = pm.list_projects()
    assert len(all_projects) == 3

    draft_projects = pm.list_projects(status="draft")
    assert len(draft_projects) == 1
    assert draft_projects[0]["name"] == "Project 1"

    active_projects = pm.list_projects(status="active")
    assert len(active_projects) == 1
    assert active_projects[0]["name"] == "Project 2"


def test_update_project(pm: ProjectManager):
    """Test updating a project."""
    project_id = pm.create_project("Original Name", "Original Desc", "draft")

    # Update name
    result = pm.update_project(project_id, name="Updated Name")
    assert result is True
    project = pm.get_project(project_id)
    assert project["name"] == "Updated Name"

    # Update status
    result = pm.update_project(project_id, status="active")
    assert result is True
    project = pm.get_project(project_id)
    assert project["status"] == "active"

    # Update non-existent project
    result = pm.update_project(9999, name="Test")
    assert result is False


def test_delete_project(pm: ProjectManager):
    """Test deleting a project."""
    project_id = pm.create_project("To Delete", "Desc", "draft")
    assert pm.get_project(project_id) is not None

    result = pm.delete_project(project_id)
    assert result is True
    assert pm.get_project(project_id) is None

    # Delete non-existent project
    result = pm.delete_project(9999)
    assert result is False


def test_search_projects(pm: ProjectManager):
    """Test searching projects by name or description."""
    pm.create_project("Alpha Project", "First project", "draft")
    pm.create_project("Beta Project", "Second project", "active")
    pm.create_project("Gamma", "Alpha description", "completed")

    results = pm.search_projects("Alpha")
    assert len(results) == 2
    names = {p["name"] for p in results}
    assert names == {"Alpha Project", "Gamma"}

    results = pm.search_projects("Second")
    assert len(results) == 1
    assert results[0]["name"] == "Beta Project"

    results = pm.search_projects("NonExistent")
    assert len(results) == 0


def test_get_project_stats(pm: ProjectManager):
    """Test getting project statistics."""
    project_id = pm.create_project("Stats Project", "Desc", "draft")

    stats = pm.get_project_stats(project_id)
    assert stats == {"images": 0, "videos": 0}

    # Add some images and videos
    now = datetime.utcnow().isoformat()
    pm._db.execute(
        "INSERT INTO images (project_id, prompt, file_path, created_at) VALUES (?, ?, ?, ?)",
        (project_id, "prompt1", "/path/img1.png", now),
    )
    pm._db.execute(
        "INSERT INTO images (project_id, prompt, file_path, created_at) VALUES (?, ?, ?, ?)",
        (project_id, "prompt2", "/path/img2.png", now),
    )
    pm._db.execute(
        "INSERT INTO videos (project_id, title, file_path, duration, created_at) VALUES (?, ?, ?, ?, ?)",
        (project_id, "Video 1", "/path/vid1.mp4", 10.5, now),
    )

    stats = pm.get_project_stats(project_id)
    assert stats == {"images": 2, "videos": 1}

    # Non-existent project
    stats = pm.get_project_stats(9999)
    assert stats == {}


def test_history_logging(pm: ProjectManager):
    """Test that history is logged for project operations."""
    project_id = pm.create_project("History Test", "Desc", "draft")
    pm.update_project(project_id, status="active")
    pm.delete_project(project_id)

    history = pm.get_history(limit=10)
    assert len(history) >= 3

    actions = [h["action"] for h in history]
    assert any("Created project" in a for a in actions)
    assert any("Updated project" in a for a in actions)
    assert any("Deleted project" in a for a in actions)


def test_context_manager(pm: ProjectManager):
    """Test ProjectManager as context manager."""
    with ProjectManager(pm._db._config._path) as pm2:
        project_id = pm2.create_project("Context Project", "Desc", "draft")
        assert project_id > 0

    # Connection should be closed after context exit
    project = pm.get_project(project_id)
    assert project is not None
    assert project["name"] == "Context Project"


def test_singleton_behavior(pm: ProjectManager):
    """Test that ProjectManager behaves as a singleton."""
    pm2 = ProjectManager(pm._db._config._path)
    assert pm is pm2

    # Creating with different config path should still return same instance
    # (singleton is per class, not per config)
    pm3 = ProjectManager(None)
    assert pm is pm3