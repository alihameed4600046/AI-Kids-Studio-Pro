"""Project repository for saving and loading Project objects as JSON."""

import json
from pathlib import Path

from src.models.project import Project


class ProjectRepository:
    """Lightweight repository for persisting Project objects to JSON files."""

    def __init__(self, logger=None) -> None:
        """Initialize the repository.

        Args:
            logger: Optional logger instance for debugging.
        """
        self._logger = logger

    def save(self, project: Project, file_path: Path) -> None:
        """Save a Project to a JSON file.

        Args:
            project: Project instance to serialize.
            file_path: Destination file path.
        """
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(project.to_dict(), f, indent=4)

        if self._logger:
            self._logger.debug("Project saved to %s", file_path)

    def load(self, file_path: Path) -> Project:
        """Load a Project from a JSON file.

        Args:
            file_path: Source file path.

        Returns:
            Project instance reconstructed from JSON.
        """
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if self._logger:
            self._logger.debug("Project loaded from %s", file_path)

        return Project.from_dict(data)

    def exists(self, file_path: Path) -> bool:
        """Check if a project file exists.

        Args:
            file_path: Path to check.

        Returns:
            True if file exists, False otherwise.
        """
        return file_path.exists()


__all__ = ["ProjectRepository"]