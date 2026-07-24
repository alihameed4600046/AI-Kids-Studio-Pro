"""Prompt Editor page for AI Kids Studio Pro.

This module provides the PromptsPage class for managing prompt templates
with a live preview panel.
"""

from __future__ import annotations

import customtkinter as ctk
import logging
from typing import Any, TYPE_CHECKING

from src.prompt.prompt_service import PromptService
from src.views.pages.base_page import BasePage

if TYPE_CHECKING:
    from src.navigation.navigation_manager import NavigationManager


__all__ = ["PromptsPage"]


class PromptsPage(BasePage):
    """Prompt Editor page with live preview functionality.

    This page provides a UI for managing prompt templates with categories,
    templates, a template editor, variables input, and live preview.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        navigation_manager: "NavigationManager",
        prompt_service: PromptService | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the Prompts page.

        Args:
            master: Parent widget (typically the content container).
            navigation_manager: Reference to the NavigationManager instance.
            prompt_service: Optional PromptService instance for data access.
            **kwargs: Additional arguments passed to CTkFrame.
        """
        super().__init__(master, navigation_manager, **kwargs)
        self._prompt_service = prompt_service or PromptService()
        self._logger = logging.getLogger(f"page.{self.__class__.__name__}")

        # Configure grid layout for the page
        self.grid_rowconfigure(0, weight=0)  # Toolbar row
        self.grid_rowconfigure(1, weight=0)  # Title row
        self.grid_rowconfigure(2, weight=1)  # Template editor row (expands)
        self.grid_rowconfigure(3, weight=0)  # Variables row
        self.grid_rowconfigure(4, weight=1)  # Live preview row (expands)
        self.grid_columnconfigure(0, weight=1)

        # Initialize UI components
        self._create_toolbar()
        self._create_title_entry()
        self._create_template_editor()
        self._create_variables_entry()
        self._create_live_preview()

        # Load initial data
        self._load_categories()
        self._load_templates()

        self._logger.info("PromptsPage initialized")

    def _create_toolbar(self) -> None:
        """Create the toolbar with category, template dropdowns and action buttons."""
        toolbar_frame = ctk.CTkFrame(self)
        toolbar_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        toolbar_frame.grid_columnconfigure(0, weight=0)  # Category label
        toolbar_frame.grid_columnconfigure(1, weight=1)  # Category dropdown
        toolbar_frame.grid_columnconfigure(2, weight=0)  # Template label
        toolbar_frame.grid_columnconfigure(3, weight=1)  # Template dropdown
        toolbar_frame.grid_columnconfigure(4, weight=0)  # New button
        toolbar_frame.grid_columnconfigure(5, weight=0)  # Save button
        toolbar_frame.grid_columnconfigure(6, weight=0)  # Delete button

        # Category label and dropdown
        category_label = ctk.CTkLabel(toolbar_frame, text="Category:")
        category_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")

        self._category_var = ctk.StringVar()
        self._category_dropdown = ctk.CTkComboBox(
            toolbar_frame,
            variable=self._category_var,
            values=[],
            state="readonly",
            command=self._on_category_changed,
        )
        self._category_dropdown.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")

        # Template label and dropdown
        template_label = ctk.CTkLabel(toolbar_frame, text="Template:")
        template_label.grid(row=0, column=2, padx=(10, 5), pady=10, sticky="w")

        self._template_var = ctk.StringVar()
        self._template_dropdown = ctk.CTkComboBox(
            toolbar_frame,
            variable=self._template_var,
            values=[],
            state="readonly",
            command=self._on_template_changed,
        )
        self._template_dropdown.grid(row=0, column=3, padx=(0, 10), pady=10, sticky="ew")

        # Action buttons
        self._new_button = ctk.CTkButton(
            toolbar_frame,
            text="New",
            width=80,
            command=self._on_new_clicked,
        )
        self._new_button.grid(row=0, column=4, padx=(0, 5), pady=10)

        self._save_button = ctk.CTkButton(
            toolbar_frame,
            text="Save",
            width=80,
            command=self._on_save_clicked,
        )
        self._save_button.grid(row=0, column=5, padx=(0, 5), pady=10)

        self._delete_button = ctk.CTkButton(
            toolbar_frame,
            text="Delete",
            width=80,
            command=self._on_delete_clicked,
        )
        self._delete_button.grid(row=0, column=6, padx=(0, 10), pady=10)

    def _create_title_entry(self) -> None:
        """Create the prompt title entry field."""
        title_frame = ctk.CTkFrame(self)
        title_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 5))
        title_frame.grid_columnconfigure(1, weight=1)

        title_label = ctk.CTkLabel(title_frame, text="Prompt Title:")
        title_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")

        self._title_var = ctk.StringVar()
        self._title_entry = ctk.CTkEntry(
            title_frame,
            textvariable=self._title_var,
            placeholder_text="Enter prompt title...",
        )
        self._title_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")

    def _create_template_editor(self) -> None:
        """Create the large multiline template editor."""
        editor_frame = ctk.CTkFrame(self)
        editor_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(5, 5))
        editor_frame.grid_rowconfigure(0, weight=1)
        editor_frame.grid_columnconfigure(0, weight=1)

        editor_label = ctk.CTkLabel(editor_frame, text="Prompt Template Editor:")
        editor_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")

        self._template_editor = ctk.CTkTextbox(
            editor_frame,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word",
        )
        self._template_editor.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

    def _create_variables_entry(self) -> None:
        """Create the variables entry field (comma separated)."""
        variables_frame = ctk.CTkFrame(self)
        variables_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(5, 5))
        variables_frame.grid_columnconfigure(1, weight=1)

        variables_label = ctk.CTkLabel(variables_frame, text="Variables (comma separated):")
        variables_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")

        self._variables_var = ctk.StringVar()
        self._variables_var.trace_add("write", lambda *_: self._update_preview())
        self._variables_entry = ctk.CTkEntry(
            variables_frame,
            textvariable=self._variables_var,
            placeholder_text="e.g., topic, letter, numbers, subject",
        )
        self._variables_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")

    def _create_live_preview(self) -> None:
        """Create the live preview textbox (read-only)."""
        preview_frame = ctk.CTkFrame(self)
        preview_frame.grid(row=4, column=0, sticky="nsew", padx=10, pady=(5, 10))
        preview_frame.grid_rowconfigure(0, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)

        preview_label = ctk.CTkLabel(preview_frame, text="Live Preview:")
        preview_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")

        self._preview_textbox = ctk.CTkTextbox(
            preview_frame,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word",
            state="disabled",  # Read-only
        )
        self._preview_textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

    def _load_categories(self) -> None:
        """Load categories from PromptService and populate the category dropdown."""
        try:
            categories = self._prompt_service.get_categories()
            self._category_dropdown.configure(values=categories)
            if categories:
                self._category_var.set(categories[0])
                self._logger.debug("Loaded %d categories", len(categories))
        except Exception as e:
            self._logger.error("Failed to load categories: %s", e)

    def _load_templates(self) -> None:
        """Load default templates from PromptService and populate the template dropdown."""
        try:
            templates = self._prompt_service.get_default_templates()
            template_names = list(templates.keys())
            self._template_dropdown.configure(values=template_names)
            if template_names:
                self._template_var.set(template_names[0])
                self._on_template_changed(template_names[0])
            self._logger.debug("Loaded %d default templates", len(templates))
        except Exception as e:
            self._logger.error("Failed to load templates: %s", e)

    def _on_category_changed(self, category: str) -> None:
        """Handle category dropdown selection change.

        Args:
            category: The selected category name.
        """
        self._logger.debug("Category changed to: %s", category)
        # Could filter templates by category in the future
        self._update_preview()

    def _on_template_changed(self, template_name: str) -> None:
        """Handle template dropdown selection change.

        Args:
            template_name: The selected template name.
        """
        self._logger.debug("Template changed to: %s", template_name)
        try:
            templates = self._prompt_service.get_default_templates()
            if template_name in templates:
                template_text = templates[template_name]
                self._template_editor.delete("1.0", "end")
                self._template_editor.insert("1.0", template_text)
                self._title_var.set(template_name)
                # Extract variables from template (simple extraction of {{...}})
                variables = self._extract_variables(template_text)
                self._variables_var.set(", ".join(variables))
                self._update_preview()
        except Exception as e:
            self._logger.error("Failed to load template: %s", e)

    def _on_new_clicked(self) -> None:
        """Handle New button click - clear the form for a new prompt."""
        self._logger.info("New button clicked")
        self._title_var.set("")
        self._template_editor.delete("1.0", "end")
        self._variables_var.set("")
        self._update_preview()

    def _on_save_clicked(self) -> None:
        """Handle Save button click - placeholder for future implementation."""
        self._logger.info("Save button clicked (not implemented)")
        # TODO: Implement save functionality using PromptService

    def _on_delete_clicked(self) -> None:
        """Handle Delete button click - placeholder for future implementation."""
        self._logger.info("Delete button clicked (not implemented)")
        # TODO: Implement delete functionality using PromptService

    def _parse_variables(self, variables_text: str) -> dict[str, str]:
        """Parse variables from key=value format.

        Args:
            variables_text: Comma-separated key=value pairs (e.g., "animal=Panda,place=Forest").

        Returns:
            Dictionary mapping variable names to their values. Invalid entries are ignored.
        """
        variables: dict[str, str] = {}
        if not variables_text.strip():
            return variables

        for pair in variables_text.split(","):
            pair = pair.strip()
            if not pair:
                continue
            if "=" not in pair:
                self._logger.debug("Ignoring invalid variable entry: %s", pair)
                continue
            key, value = pair.split("=", 1)
            key = key.strip()
            value = value.strip()
            if key:
                variables[key] = value
            else:
                self._logger.debug("Ignoring variable with empty key: %s", pair)

        return variables

    def _extract_variables(self, template_text: str) -> list[str]:
        """Extract variable names from template text using simple string scanning.

        Args:
            template_text: Template text containing {{variable}} placeholders.

        Returns:
            List of variable names found in the template.
        """
        variables: list[str] = []
        start = 0
        while True:
            # Find the next {{ pattern
            open_idx = template_text.find("{{", start)
            if open_idx == -1:
                break
            # Find the closing }} pattern
            close_idx = template_text.find("}}", open_idx + 2)
            if close_idx == -1:
                break
            # Extract the variable name between {{ and }}
            var_name = template_text[open_idx + 2 : close_idx].strip()
            if var_name and var_name not in variables:
                variables.append(var_name)
            start = close_idx + 2
        return variables

    def _update_preview(self) -> None:
        """Update the live preview with the current template and variables."""
        template = self._template_editor.get("1.0", "end-1c")
        variables_text = self._variables_var.get()

        # Parse variables from key=value format
        variables = self._parse_variables(variables_text)

        # Render template using PromptService
        preview_text = self._prompt_service.render_template(template, variables)

        # Update preview textbox
        self._preview_textbox.configure(state="normal")
        self._preview_textbox.delete("1.0", "end")
        self._preview_textbox.insert("1.0", preview_text)
        self._preview_textbox.configure(state="disabled")

    def on_show(self) -> None:
        """Called when the page becomes visible."""
        super().on_show()
        self._logger.info("Prompts page displayed")
        self._update_preview()

    def on_hide(self) -> None:
        """Called when the page is hidden."""
        super().on_hide()
        self._logger.info("Prompts page hidden")

    def on_navigate_to(self, **kwargs: Any) -> None:
        """Called when navigating to this page with optional parameters.

        Args:
            **kwargs: Optional parameters passed during navigation.
        """
        super().on_navigate_to(**kwargs)
        self._logger.debug("Navigated to PromptsPage with params: %s", kwargs)

    def on_navigate_from(self) -> None:
        """Called when navigating away from this page."""
        super().on_navigate_from()
        self._logger.debug("Navigating from PromptsPage")