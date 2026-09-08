"""Settings page for AI Kids Studio Pro.

This module provides the SettingsPage class for configuring application
settings, including OpenRouter API configuration.
"""

from __future__ import annotations

import logging
from typing import Any

import customtkinter as ctk

from src.engine.openrouter_engine import OpenRouterEngine
from src.settings.manager import SettingsManager
from src.views.pages.base_page import BasePage

if __import__("typing").TYPE_CHECKING:
    from src.navigation.navigation_manager import NavigationManager


__all__ = ["SettingsPage"]


class SettingsPage(BasePage):
    """Settings page for application configuration.

    Provides UI for configuring OpenRouter API settings including
    API key, model selection, and base URL.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        navigation_manager: "NavigationManager",
        settings_manager: SettingsManager | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the settings page.

        Args:
            master: Parent widget.
            navigation_manager: Reference to the navigation manager.
            settings_manager: SettingsManager instance for persistence.
            **kwargs: Additional keyword arguments passed to CTkFrame.
        """
        super().__init__(master, navigation_manager, **kwargs)
        self._settings_manager = settings_manager
        self._logger = logging.getLogger(f"page.{self.__class__.__name__}")

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._create_header()
        self._create_openrouter_section()
        self._create_feedback_label()
        self._load_settings()

        self._logger.info("SettingsPage initialized")

    def _create_header(self) -> None:
        """Create the page header."""
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            header_frame,
            text="Settings",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title_label.grid(row=0, column=0, sticky="w", padx=15, pady=10)

    def _create_openrouter_section(self) -> None:
        """Create the OpenRouter configuration section."""
        scroll_frame = ctk.CTkScrollableFrame(self)
        scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        scroll_frame.grid_columnconfigure(1, weight=1)

        section_label = ctk.CTkLabel(
            scroll_frame,
            text="OpenRouter Configuration",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        section_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))

        info_label = ctk.CTkLabel(
            scroll_frame,
            text="Configure your OpenRouter API settings. Changes require an application restart to take effect.",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray70"),
            wraplength=500,
            justify="left",
        )
        info_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 10))

        self._api_key_var = ctk.StringVar(value="")
        self._model_var = ctk.StringVar(value="")
        self._base_url_var = ctk.StringVar(value="")

        fields = [
            ("API Key", self._api_key_var, "Your OpenRouter API key", True),
            ("Model", self._model_var, "e.g. openai/gpt-3.5-turbo", False),
            ("Base URL", self._base_url_var, "OpenRouter API base URL", False),
        ]

        for idx, (label_text, var, placeholder, is_sensitive) in enumerate(fields, start=2):
            label = ctk.CTkLabel(scroll_frame, text=label_text, anchor="w")
            label.grid(row=idx, column=0, sticky="w", padx=10, pady=(8, 2))

            entry = ctk.CTkEntry(
                scroll_frame,
                textvariable=var,
                placeholder_text=placeholder,
            )
            entry.grid(row=idx, column=1, sticky="ew", padx=10, pady=(8, 2))

            if is_sensitive:
                note = ctk.CTkLabel(
                    scroll_frame,
                    text="Stored locally in settings.json. Value is not masked in the UI.",
                    font=ctk.CTkFont(size=10),
                    text_color=("gray50", "gray70"),
                )
                note.grid(row=idx + 1, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 4))

        save_btn = ctk.CTkButton(
            scroll_frame,
            text="Save Settings",
            command=self._save_settings,
            width=200,
        )
        save_btn.grid(row=len(fields) + 3, column=0, columnspan=2, padx=10, pady=(15, 10))

    def _create_feedback_label(self) -> None:
        """Create the feedback label for save operations."""
        self._feedback_var = ctk.StringVar(value="")
        self._feedback_label = ctk.CTkLabel(
            self,
            textvariable=self._feedback_var,
            font=ctk.CTkFont(size=12),
        )
        self._feedback_label.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="w")

    def _load_settings(self) -> None:
        """Load current settings into the UI fields."""
        if self._settings_manager is None:
            return

        api_key = self._settings_manager.get("openrouter_api_key", "")
        model = self._settings_manager.get("openrouter_model", OpenRouterEngine.DEFAULT_MODEL)
        base_url = self._settings_manager.get("openrouter_base_url", OpenRouterEngine.DEFAULT_BASE_URL)

        if api_key:
            self._api_key_var.set(api_key)
        if model:
            self._model_var.set(model)
        if base_url:
            self._base_url_var.set(base_url)

    def _save_settings(self) -> None:
        """Save the current UI values to SettingsManager."""
        if self._settings_manager is None:
            self._show_feedback("Settings manager not available.", error=True)
            return

        api_key = self._api_key_var.get().strip()
        model = self._model_var.get().strip()
        base_url = self._base_url_var.get().strip()

        if not api_key:
            self._show_feedback("API Key is required.", error=True)
            return

        self._settings_manager.set("openrouter_api_key", api_key)
        self._settings_manager.set("openrouter_model", model if model else OpenRouterEngine.DEFAULT_MODEL)
        self._settings_manager.set("openrouter_base_url", base_url if base_url else OpenRouterEngine.DEFAULT_BASE_URL)

        self._show_feedback("Settings saved. Restart the application for changes to take effect.", error=False)
        self._logger.info("OpenRouter settings saved")

    def _show_feedback(self, message: str, error: bool = False) -> None:
        """Show a feedback message to the user.

        Args:
            message: Message text to display.
            error: If True, display as an error message.
        """
        self._feedback_var.set(message)
        if error:
            self._feedback_label.configure(text_color=("darkred", "red"))
        else:
            self._feedback_label.configure(text_color=("darkgreen", "green"))

    def on_show(self) -> None:
        """Called when the page becomes visible."""
        super().on_show()
        self._load_settings()

    def on_hide(self) -> None:
        """Called when the page is hidden."""
        super().on_hide()
        self._feedback_var.set("")
