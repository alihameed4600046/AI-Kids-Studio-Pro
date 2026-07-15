"""Project Manager implementation.

The :class:`ProjectManager` provides a high-level API for managing projects
in the application. It uses the :class:`DatabaseManager` for persistence
and the project's logging system for audit trails.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.database.database_manager import DatabaseManager
from src.logging.logger import get_logger

__all__ = ["ProjectManager"]


class ProjectManager:
    """Singleton-style manager for application projects.

    Parameters
    ----------
    config_path:
        Path to the configuration file. The manager will read the
        ``database.path`` value from :class:`~config.config.Config`.
    """

    _instance: "ProjectManager | None" = None

    def __new__(cls, config_path: str | Path | None = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init(config_path)
        return cls._instance

    def _init(self, config_path: str | Path | None):
        self._db = DatabaseManager(config_path)
        self._logger = get_logger("project")
        self._logger.debug("ProjectManager initialised")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def create_project(
        self,
        name: str,
        description: str = "",
        status: str = "draft",
    ) -> int:
        """Create a new project.

        Parameters
        ----------
        name:
            Project name (required).
        description:
            Optional project description.
        status:
            Project status (default: "draft").

        Returns
        -------
        int
            The ID of the newly created project.
        """
        now = datetime.utcnow().isoformat()
        cursor = self._db.execute(
            """
            INSERT INTO projects (name, description, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, description, status, now, now),
        )
        project_id = cursor.lastrowid
        self._logger.info("Created project %s (id=%s)", name, project_id)
        self._log_history(f"Created project '{name}' (id={project_id})")
        return project_id

    def get_project(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a project by ID.

        Parameters
        ----------
        project_id:
            The project ID to look up.

        Returns
        -------
        dict or None
            Project data as a dictionary, or None if not found.
        """
        row = self._db.fetchone(
            "SELECT * FROM projects WHERE id = ?", (project_id,)
        )
        if row:
            return dict(row)
        return None

    def get_project_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Retrieve a project by name.

        Parameters
        ----------
        name:
            The project name to look up.

        Returns
        -------
        dict or None
            Project data as a dictionary, or None if not found.
        """
        row = self._db.fetchone(
            "SELECT * FROM projects WHERE name = ?", (name,)
        )
        if row:
            return dict(row)
        return None

    def list_projects(
        self,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """List projects with optional filtering.

        Parameters
        ----------
        status:
            Optional status filter (e.g., "draft", "active", "completed").
        limit:
            Maximum number of projects to return.
        offset:
            Number of projects to skip.

        Returns
        -------
        list of dict
            List of project dictionaries.
        """
        if status:
            rows = self._db.fetchall(
                "SELECT * FROM projects WHERE status = ? ORDER BY updated_at DESC LIMIT ? OFFSET ?",
                (status, limit, offset),
            )
        else:
            rows = self._db.fetchall(
                "SELECT * FROM projects ORDER BY updated_at DESC LIMIT ? OFFSET ?",
                (limit, offset),
            )
        return [dict(row) for row in rows]

    def update_project(
        self,
        project_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
    ) -> bool:
        """Update a project.

        Parameters
        ----------
        project_id:
            The project ID to update.
        name:
            New name (optional).
        description:
            New description (optional).
        status:
            New status (optional).

        Returns
        -------
        bool
            True if the project was updated, False if not found.
        """
        project = self.get_project(project_id)
        if not project:
            return False

        updates = []
        params = []

        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        if status is not None:
            updates.append("status = ?")
            params.append(status)

        if not updates:
            return True

        updates.append("updated_at = ?")
        params.append(datetime.utcnow().isoformat())
        params.append(project_id)

        self._db.execute(
            f"UPDATE projects SET {', '.join(updates)} WHERE id = ?",
            params,
        )
        self._logger.info("Updated project %s", project_id)
        self._log_history(f"Updated project '{project['name']}' (id={project_id})")
        return True

    def delete_project(self, project_id: int) -> bool:
        """Delete a project and all associated data.

        Parameters
        ----------
        project_id:
            The project ID to delete.

        Returns
        -------
        bool
            True if the project was deleted, False if not found.
        """
        project = self.get_project(project_id)
        if not project:
            return False

        # Delete associated images and videos (cascaded by FK)
        self._db.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        self._logger.info("Deleted project %s", project_id)
        self._log_history(f"Deleted project '{project['name']}' (id={project_id})")
        return True

    def get_project_stats(self, project_id: int) -> Dict[str, int]:
        """Get statistics for a project.

        Parameters
        ----------
        project_id:
            The project ID.

        Returns
        -------
        dict
            Dictionary with counts of images, videos, etc.
        """
        project = self.get_project(project_id)
        if not project:
            return {}

        images = self._db.fetchone(
            "SELECT COUNT(*) as count FROM images WHERE project_id = ?",
            (project_id,),
        )
        videos = self._db.fetchone(
            "SELECT COUNT(*) as count FROM videos WHERE project_id = ?",
            (project_id,),
        )

        return {
            "images": images["count"] if images else 0,
            "videos": videos["count"] if videos else 0,
        }

    def search_projects(self, query: str) -> List[Dict[str, Any]]:
        """Search projects by name or description.

        Parameters
        ----------
        query:
            Search query string.

        Returns
        -------
        list of dict
            Matching projects.
        """
        search_term = f"%{query}%"
        rows = self._db.fetchall(
            """
            SELECT * FROM projects
            WHERE name LIKE ? OR description LIKE ?
            ORDER BY updated_at DESC
            """,
            (search_term, search_term),
        )
        return [dict(row) for row in rows]

    # ------------------------------------------------------------------
    # History logging
    # ------------------------------------------------------------------
    def _log_history(self, action: str, details: str = "") -> None:
        """Log an action to the history table."""
        now = datetime.utcnow().isoformat()
        self._db.execute(
            "INSERT INTO history (action, details, created_at) VALUES (?, ?, ?)",
            (action, details, now),
        )

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent history entries.

        Parameters
        ----------
        limit:
            Maximum number of entries to return.

        Returns
        -------
        list of dict
            History entries.
        """
        rows = self._db.fetchall(
            "SELECT * FROM history ORDER BY created_at DESC LIMIT ?",
            (limit,),
        )
        return [dict(row) for row in rows]

    # ------------------------------------------------------------------
    # Context manager support
    # ------------------------------------------------------------------
    def __enter__(self) -> "ProjectManager":
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[object],
    ) -> None:
        self._db.close()