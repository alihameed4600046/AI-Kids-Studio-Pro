"""Prompt domain model for AI Kids Studio Pro."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Optional
from uuid import uuid4


@dataclass
class Prompt:
    """Domain model representing a reusable prompt template."""

    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    category: str = "general"
    template: str = ""
    variables: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        """Validate prompt data after initialization."""
        if not self.title:
            raise ValueError("Prompt title cannot be empty")
        if not self.template:
            raise ValueError("Prompt template cannot be empty")
        if self.created_at.tzinfo is None or self.updated_at.tzinfo is None:
            raise ValueError("Timestamps must include timezone information")

    def update(
        self,
        title: Optional[str] = None,
        category: Optional[str] = None,
        template: Optional[str] = None,
        variables: Optional[Dict[str, str]] = None,
    ) -> None:
        """Update prompt fields and refresh the update timestamp."""
        if title is not None:
            if not title:
                raise ValueError("Prompt title cannot be empty")
            self.title = title
        if category is not None:
            self.category = category
        if template is not None:
            if not template:
                raise ValueError("Prompt template cannot be empty")
            self.template = template
        if variables is not None:
            self.variables = variables
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        """Convert the prompt to a dictionary for serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "template": self.template,
            "variables": self.variables,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Prompt":
        """Create a Prompt instance from a dictionary."""
        payload = data.copy()
        payload["created_at"] = datetime.fromisoformat(payload["created_at"])
        payload["updated_at"] = datetime.fromisoformat(payload["updated_at"])
        return cls(**payload)

    def __str__(self) -> str:
        return f"Prompt(id={self.id}, title={self.title})"

    def __repr__(self) -> str:
        return (
            f"Prompt(id={self.id!r}, title={self.title!r}, "
            f"category={self.category!r})"
        )