"""Prompt repository for JSON-based persistence."""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.prompt.prompt import Prompt

logger = logging.getLogger(__name__)


class PromptRepository:
    """JSON-based repository for Prompt persistence."""

    def __init__(self, storage_path: str | Path) -> None:
        """Initialize the prompt repository.

        Args:
            storage_path: Path to the JSON file for prompt storage.
        """
        self._storage_path = Path(storage_path)
        self._prompts: dict[str, Prompt] = {}
        self._loaded = False
        logger.info("PromptRepository initialized with storage: %s", self._storage_path)

    def _ensure_loaded(self) -> None:
        """Load prompts from storage if not already loaded."""
        if not self._loaded:
            self._load()

    def _load(self) -> None:
        """Load prompts from JSON storage file."""
        try:
            if self._storage_path.exists():
                with open(self._storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._prompts = {
                    prompt_data["id"]: Prompt.from_dict(prompt_data)
                    for prompt_data in data.get("prompts", [])
                }
                logger.info(
                    "Loaded %d prompts from %s", len(self._prompts), self._storage_path
                )
            else:
                self._prompts = {}
                logger.info(
                    "No existing storage file, starting with empty repository"
                )
            self._loaded = True
        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON from %s: %s", self._storage_path, e)
            raise ValueError(f"Failed to parse storage file: {e}") from e
        except OSError as e:
            logger.error("Failed to read storage file %s: %s", self._storage_path, e)
            raise OSError(f"Failed to read storage file: {e}") from e

    def _save(self) -> None:
        """Save prompts to JSON storage file."""
        try:
            self._storage_path.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "prompts": [prompt.to_dict() for prompt in self._prompts.values()]
            }
            with open(self._storage_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info("Saved %d prompts to %s", len(self._prompts), self._storage_path)
        except OSError as e:
            logger.error("Failed to write storage file %s: %s", self._storage_path, e)
            raise OSError(f"Failed to write storage file: {e}") from e

    def save(self, prompt: Prompt) -> Prompt:
        """Save a prompt to the repository.

        Args:
            prompt: The prompt to save.

        Returns:
            The saved prompt with updated timestamp.

        Raises:
            OSError: If saving fails.
        """
        self._ensure_loaded()
        prompt.updated_at = datetime.now(timezone.utc)
        self._prompts[prompt.id] = prompt
        self._save()
        logger.debug("Saved prompt: %s", prompt)
        return prompt

    def load(self, prompt_id: str) -> Prompt:
        """Load a prompt by ID.

        Args:
            prompt_id: The ID of the prompt to load.

        Returns:
            The loaded prompt.

        Raises:
            KeyError: If prompt with given ID is not found.
        """
        self._ensure_loaded()
        if prompt_id not in self._prompts:
            logger.warning("Prompt not found: %s", prompt_id)
            raise KeyError(f"Prompt not found: {prompt_id}")
        logger.debug("Loaded prompt: %s", prompt_id)
        return self._prompts[prompt_id]

    def list_all(
        self, active_only: bool = False, category: Optional[str] = None
    ) -> list[Prompt]:
        """List all prompts, optionally filtered.

        Args:
            active_only: If True, only return active prompts.
            category: If provided, filter by category.

        Returns:
            List of prompts matching the filters.
        """
        self._ensure_loaded()
        prompts = list(self._prompts.values())

        if category is not None:
            prompts = [p for p in prompts if p.category == category]

        prompts.sort(key=lambda p: p.updated_at, reverse=True)
        logger.debug(
            "Listed %d prompts (active_only=%s, category=%s)",
            len(prompts),
            active_only,
            category,
        )
        return prompts

    def delete(self, prompt_id: str) -> bool:
        """Delete a prompt by ID.

        Args:
            prompt_id: The ID of the prompt to delete.

        Returns:
            True if prompt was deleted, False if not found.
        """
        self._ensure_loaded()
        if prompt_id not in self._prompts:
            logger.warning("Attempted to delete non-existent prompt: %s", prompt_id)
            return False

        del self._prompts[prompt_id]
        self._save()
        logger.info("Deleted prompt: %s", prompt_id)
        return True

    def exists(self, prompt_id: str) -> bool:
        """Check if a prompt exists.

        Args:
            prompt_id: The ID to check.

        Returns:
            True if prompt exists, False otherwise.
        """
        self._ensure_loaded()
        return prompt_id in self._prompts

    def count(self) -> int:
        """Count prompts in repository.

        Returns:
            Number of prompts.
        """
        self._ensure_loaded()
        return len(self._prompts)