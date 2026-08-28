"""Prompt Engine for loading, templating, and variable substitution.

This module provides the PromptEngine class which handles loading
prompts from YAML files, substituting variables, and integrating
with the existing template registry system.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

import yaml

from src.engine.ai_engine import GenerationRequest, GenerationResponse
from src.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


class PromptTemplateError(Exception):
    """Raised when a prompt template cannot be processed."""

    pass


def _looks_like_plain_text(text: str) -> bool:
    """Return True if *text* appears to be plain text rather than YAML.

    A file is treated as plain text when every non-empty, non-comment line
    lacks a ``:`` separator.  This intentionally avoids silently accepting
    malformed structured YAML.
    """
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" in stripped:
            return False
    return True


class PromptEngine:
    """Engine for loading and processing prompt templates.

    This class handles loading prompts from YAML files, substituting
    variables using Python string formatting, and integrating with
    the existing template registry system.

    Attributes
    ----------
    prompts_dir:
        Directory containing prompt YAML files.
    templates:
        Dictionary of loaded template names to template content.
    variables:
        Dictionary of variable names to their current values.
    """

    def __init__(self, prompts_dir: str | Path | None = None) -> None:
        self.prompts_dir = Path(prompts_dir) if prompts_dir else Path("config/prompts")
        self.templates: dict[str, str] = {}
        self.variables: dict[str, Any] = {}
        self._variable_pattern = re.compile(r"\{\{\s*(\w+)\s*\}\}")

    def load_template(self, name: str) -> str:
        """Load a prompt template by name.

        Parameters
        ----------
        name:
            Name of the template to load.

        Returns
        -------
        str
            The template content.

        Raises
        ------
        PromptTemplateError
            If the template cannot be loaded.
        """
        if name in self.templates:
            return self.templates[name]

        template_path = self.prompts_dir / f"{name}.yaml"
        if not template_path.exists():
            raise PromptTemplateError(f"Template not found: {template_path}")

        try:
            with open(template_path, "r", encoding="utf-8") as f:
                raw = f.read()
        except OSError as exc:
            raise PromptTemplateError(f"Failed to read template {name}: {exc}") from exc

        try:
            data = yaml.safe_load(raw)
            if isinstance(data, dict) and "prompt" in data:
                self.templates[name] = data["prompt"]
            elif isinstance(data, str):
                self.templates[name] = data
            else:
                raise PromptTemplateError(f"Invalid template format in {template_path}")
        except PromptTemplateError:
            raise
        except Exception as exc:
            if _looks_like_plain_text(raw):
                self.templates[name] = raw.strip()
            else:
                raise PromptTemplateError(
                    f"Failed to parse template {name}: {exc}"
                ) from exc

        logger.debug("Loaded template: %s", name)
        return self.templates[name]

    def load_all_templates(self) -> dict[str, str]:
        """Load all templates from the prompts directory.

        Returns
        -------
        dict[str, str]
            Dictionary of template names to content.
        """
        if not self.prompts_dir.exists():
            logger.warning("Prompts directory not found: %s", self.prompts_dir)
            return {}

        for template_file in self.prompts_dir.glob("*.yaml"):
            name = template_file.stem
            try:
                self.load_template(name)
            except PromptTemplateError as exc:
                logger.warning("Failed to load template %s: %s", name, exc)

        logger.info("Loaded %d templates from %s", len(self.templates), self.prompts_dir)
        return self.templates

    def set_variable(self, name: str, value: Any) -> None:
        """Set a variable value for template substitution.

        Parameters
        ----------
        name:
            Variable name.
        value:
            Variable value.
        """
        self.variables[name] = value

    def set_variables(self, variables: dict[str, Any]) -> None:
        """Set multiple variable values.

        Parameters
        ----------
        variables:
            Dictionary of variable names to values.
        """
        self.variables.update(variables)

    def get_variable(self, name: str, default: Any = None) -> Any:
        """Get a variable value.

        Parameters
        ----------
        name:
            Variable name.
        default:
            Default value if variable is not set.

        Returns
        -------
        Any
            The variable value or default.
        """
        return self.variables.get(name, default)

    def clear_variables(self) -> None:
        """Clear all set variables."""
        self.variables.clear()

    def substitute(self, template: str, variables: dict[str, Any] | None = None) -> str:
        """Substitute variables in a template string.

        Supports both {{variable}} and {variable} formats.

        Parameters
        ----------
        template:
            Template string with placeholders.
        variables:
            Optional dictionary of variables to use. If not provided,
            uses the instance's variable store.

        Returns
        -------
        str
            Template with variables substituted.

        Raises
        ------
        PromptTemplateError
            If a required variable is missing.
        """
        vars_to_use = variables if variables is not None else self.variables

        def replace_match(match: re.Match[str]) -> str:
            var_name = match.group(1).strip()
            if var_name in vars_to_use:
                return str(vars_to_use[var_name])
            raise PromptTemplateError(f"Missing variable: {var_name}")

        try:
            result = self._variable_pattern.sub(replace_match, template)
            # Also handle Python format strings as fallback
            if "{" in result and "}" in result:
                try:
                    result = result.format(**vars_to_use)
                except KeyError:
                    pass
            return result
        except PromptTemplateError:
            raise
        except Exception as exc:
            raise PromptTemplateError(f"Template substitution failed: {exc}") from exc

    def render(self, template_name: str, variables: dict[str, Any] | None = None) -> str:
        """Load a template and substitute variables.

        Parameters
        ----------
        template_name:
            Name of the template to render.
        variables:
            Optional dictionary of variables to use.

        Returns
        -------
        str
            Rendered template string.

        Raises
        ------
        PromptTemplateError
            If the template cannot be loaded or variables are missing.
        """
        template = self.load_template(template_name)
        return self.substitute(template, variables)

    def build_request(
        self,
        template_name: str,
        variables: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> GenerationRequest:
        """Build a GenerationRequest from a template.

        Parameters
        ----------
        template_name:
            Name of the template to use.
        variables:
            Variables for template substitution.
        **kwargs:
            Additional GenerationRequest parameters.

        Returns
        -------
        GenerationRequest
            The constructed request object.
        """
        prompt = self.render(template_name, variables)
        context = dict(variables) if variables else {}
        return GenerationRequest(prompt=prompt, context=context, **kwargs)

    def extract_variables(self, template: str) -> list[str]:
        """Extract variable names from a template string.

        Parameters
        ----------
        template:
            Template string to analyze.

        Returns
        -------
        list[str]
            List of variable names found in the template.
        """
        matches = self._variable_pattern.findall(template)
        return [match.strip() for match in matches]

    def validate_template(self, template_name: str) -> bool:
        """Validate that a template can be loaded and has no missing variables.

        Parameters
        ----------
        template_name:
            Name of the template to validate.

        Returns
        -------
        bool
            True if the template is valid.
        """
        try:
            template = self.load_template(template_name)
            variables = self.extract_variables(template)
            missing = [v for v in variables if v not in self.variables]
            if missing:
                logger.warning("Template %s is missing variables: %s", template_name, missing)
                return False
            return True
        except PromptTemplateError as exc:
            logger.error("Template validation failed for %s: %s", template_name, exc)
            return False

    def get_available_templates(self) -> list[str]:
        """Get list of available template names.

        Returns
        -------
        list[str]
            List of template names.
        """
        if not self.prompts_dir.exists():
            return []

        return [f.stem for f in self.prompts_dir.glob("*.yaml")]

    def __len__(self) -> int:
        return len(self.templates)

    def __contains__(self, name: str) -> bool:
        return name in self.templates
