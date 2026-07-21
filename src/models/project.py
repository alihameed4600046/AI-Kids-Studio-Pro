"""Project data model for AI Kids Studio Pro.

This module provides a lightweight Project dataclass for representing
project metadata without any file operations or business logic.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


__all__ = ["Project"]


@dataclass
class Project:
    """Represents a project in AI Kids Studio Pro.

    Attributes:
        id: Unique identifier for the project.
        name: Human-readable project name.
        description: Brief description of the project.
        category: Project category/type.
        created_at: ISO format timestamp of creation.
        updated_at: ISO format timestamp of last update.
        project_path: Filesystem path to the project directory.
    """

    id: str
    name: str
    description: str
    category: str
    created_at: str
    updated_at: str
    project_path: str

    def to_dict(self) -> dict[str, Any]:
        """Return a serializable dictionary representation.

        Returns:
            Dictionary with all project fields.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Project:
        """Create a Project instance from a dictionary.

        Args:
            data: Dictionary containing project fields.

        Returns:
            New Project instance.
        """
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            category=data["category"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            project_path=data["project_path"],
        )