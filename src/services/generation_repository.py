"""Repository for generation job persistence."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any

from src.database.database_manager import DatabaseManager
from src.database.models import Generation
from src.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


class GenerationRepository:
    """Repository for saving and loading generation jobs."""

    def __init__(self, db_manager: DatabaseManager | None = None) -> None:
        self.db = db_manager or DatabaseManager()

    def save(self, job: Any) -> None:
        """Save a generation job to the database.

        Parameters
        ----------
        job:
            GenerationJob instance to save.
        """
        try:
            self.db.execute(
                """
                INSERT OR REPLACE INTO generations
                (id, category, template_name, variables, media_types, status,
                 result, error, created_at, completed_at, duration_ms, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job.id,
                    job.category,
                    job.template_name,
                    json.dumps(job.variables),
                    json.dumps([mt.value for mt in job.media_types]),
                    job.status.value,
                    job.result.text if job.result else None,
                    job.error,
                    job.created_at.isoformat(),
                    job.completed_at.isoformat() if job.completed_at else None,
                    job.duration_ms,
                    json.dumps(job.metadata),
                ),
            )
            logger.debug("Saved generation job %s", job.id)
        except Exception as exc:
            logger.error("Failed to save generation job %s: %s", job.id, exc)

    def load(self, job_id: str) -> Generation | None:
        """Load a generation job by ID.

        Parameters
        ----------
        job_id:
            Job ID to load.

        Returns
        -------
        Generation | None
            Generation model or None if not found.
        """
        row = self.db.fetchone(
            "SELECT * FROM generations WHERE id = ?", (job_id,)
        )
        if not row:
            return None

        return self._row_to_generation(row)

    def load_recent(self, limit: int = 50) -> list[Generation]:
        """Load recent generation jobs.

        Parameters
        ----------
        limit:
            Maximum number of jobs to load.

        Returns
        -------
        list[Generation]
            List of recent generation jobs.
        """
        rows = self.db.fetchall(
            "SELECT * FROM generations ORDER BY created_at DESC LIMIT ?",
            (limit,),
        )
        return [self._row_to_generation(row) for row in rows]

    def load_by_category(self, category: str, limit: int = 50) -> list[Generation]:
        """Load generation jobs by category.

        Parameters
        ----------
        category:
            Category to filter by.
        limit:
            Maximum number of jobs to load.

        Returns
        -------
        list[Generation]
            List of generation jobs in the category.
        """
        rows = self.db.fetchall(
            "SELECT * FROM generations WHERE category = ? ORDER BY created_at DESC LIMIT ?",
            (category, limit),
        )
        return [self._row_to_generation(row) for row in rows]

    def delete(self, job_id: str) -> bool:
        """Delete a generation job.

        Parameters
        ----------
        job_id:
            Job ID to delete.

        Returns
        -------
        bool
            True if deleted, False if not found.
        """
        cursor = self.db.execute(
            "DELETE FROM generations WHERE id = ?", (job_id,)
        )
        return cursor.rowcount > 0

    def _row_to_generation(self, row: Any) -> Generation:
        """Convert a database row to a Generation model."""
        return Generation(
            id=row["id"],
            category=row["category"],
            template_name=row["template_name"],
            variables=row["variables"],
            media_types=row["media_types"],
            status=row["status"],
            result=row["result"],
            error=row["error"],
            created_at=datetime.fromisoformat(row["created_at"]),
            completed_at=(
                datetime.fromisoformat(row["completed_at"])
                if row["completed_at"]
                else None
            ),
            duration_ms=row["duration_ms"],
            metadata=row["metadata"],
        )
