"""Prompt service for managing Prompt lifecycle operations."""

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from src.prompt.prompt import Prompt
from src.prompt.prompt_repository import PromptRepository

logger = logging.getLogger(__name__)

DEFAULT_PROMPT_STORAGE = Path("data") / "prompts.json"


class PromptService:
    """Service layer for creating, updating, deleting, and retrieving prompts."""

    def __init__(
        self,
        repository: PromptRepository | None = None,
        storage_path: str | Path | None = None,
    ) -> None:
        """Initialize the prompt service.

        Args:
            repository: Optional PromptRepository instance.
            storage_path: Optional storage path to create a default repository.
        """
        self._repository = repository or PromptRepository(
            storage_path or DEFAULT_PROMPT_STORAGE
        )
        logger.info("PromptService initialized with repository %s", self._repository)

    def create_prompt(
        self,
        title: str,
        category: str,
        template: str,
        variables: Optional[dict[str, str]] = None,
    ) -> Prompt:
        """Create and persist a new prompt.

        Args:
            title: Prompt title.
            category: Prompt category.
            template: Prompt template.
            variables: Optional dictionary of template variables.

        Returns:
            Created Prompt instance.

        Raises:
            ValueError: If title, category, or template is empty.
        """
        if not title or not title.strip():
            raise ValueError("Prompt title cannot be empty")
        if not category or not category.strip():
            raise ValueError("Prompt category cannot be empty")
        if not template or not template.strip():
            raise ValueError("Prompt template cannot be empty")

        prompt = Prompt(
            title=title.strip(),
            category=category.strip(),
            template=template.strip(),
            variables=variables or {},
        )
        saved_prompt = self._repository.save(prompt)
        logger.info("Created prompt: %s", saved_prompt.id)
        return saved_prompt

    def update_prompt(
        self,
        prompt_id: str,
        title: Optional[str] = None,
        category: Optional[str] = None,
        template: Optional[str] = None,
        variables: Optional[dict[str, str]] = None,
    ) -> Prompt:
        """Update an existing prompt by ID.

        Args:
            prompt_id: ID of the prompt to update.
            title: Optional new title.
            category: Optional new category.
            template: Optional new template.
            variables: Optional new variables dictionary.

        Returns:
            Updated Prompt instance.

        Raises:
            ValueError: If title, category, or template is empty when provided.
        """
        if title is not None and (not title or not title.strip()):
            raise ValueError("Prompt title cannot be empty")
        if category is not None and (not category or not category.strip()):
            raise ValueError("Prompt category cannot be empty")
        if template is not None and (not template or not template.strip()):
            raise ValueError("Prompt template cannot be empty")

        prompt = self._repository.load(prompt_id)
        prompt.update(
            title=title.strip() if title is not None else None,
            category=category.strip() if category is not None else None,
            template=template.strip() if template is not None else None,
            variables=variables,
        )
        saved_prompt = self._repository.save(prompt)
        logger.info("Updated prompt: %s", saved_prompt.id)
        return saved_prompt

    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt by ID.

        Args:
            prompt_id: ID of the prompt to delete.

        Returns:
            True if deleted, False otherwise.
        """
        deleted = self._repository.delete(prompt_id)
        if deleted:
            logger.info("Deleted prompt: %s", prompt_id)
        else:
            logger.warning("Delete operation did not find prompt: %s", prompt_id)
        return deleted

    def get_prompt(self, prompt_id: str) -> Prompt:
        """Retrieve a prompt by ID.

        Args:
            prompt_id: ID of the prompt to retrieve.

        Returns:
            Prompt instance for the requested ID.
        """
        prompt = self._repository.load(prompt_id)
        logger.debug("Retrieved prompt: %s", prompt_id)
        return prompt

    def list_prompts(
        self,
        active_only: bool = False,
        category: Optional[str] = None,
    ) -> list[Prompt]:
        """List prompts from repository with optional filtering.

        Args:
            active_only: Ignored for now, preserved for future compatibility.
            category: Filter prompts by category.

        Returns:
            List of prompts.
        """
        prompts = self._repository.list_all(category=category)
        logger.debug(
            "Listed %d prompts from PromptService (category=%s)",
            len(prompts),
            category,
        )
        return prompts

    def get_categories(self) -> List[str]:
        """Return the available prompt categories.

        Returns:
            A list of built-in prompt categories.
        """
        categories = self._repository.get_categories()
        logger.debug("Retrieved %d categories from PromptService", len(categories))
        return categories

    def get_default_templates(self) -> Dict[str, str]:
        """Return the default prompt templates.

        Returns:
            A mapping of built-in categories to placeholder templates.
        """
        templates = self._repository.get_default_templates()
        logger.debug(
            "Retrieved %d default templates from PromptService",
            len(templates),
        )
        return templates

    def render_template(
        self,
        template: str,
        variables: dict[str, str],
    ) -> str:
        """Render a template by replacing placeholders with variable values.

        Replaces every {{variable}} placeholder with its matching value from
        the variables dictionary. If a variable has no value, the placeholder
        is left unchanged.

        Args:
            template: The template string containing {{variable}} placeholders.
            variables: Dictionary mapping variable names to their values.

        Returns:
            The rendered template string with placeholders replaced.
        """
        if not template:
            return ""

        rendered = template
        for var_name, var_value in variables.items():
            placeholder = f"{{{{{var_name}}}}}"
            rendered = rendered.replace(placeholder, var_value)

        logger.debug("Rendered template with %d variables", len(variables))
        return rendered


__all__ = ["PromptService"]
