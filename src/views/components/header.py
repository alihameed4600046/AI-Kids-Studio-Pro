"""Header component for AI Kids Studio Pro.

This module provides the Header component for the main application window.
"""

from __future__ import annotations

import customtkinter as ctk
from typing import Optional

from src.config import Config
from src.logging.logger import get_logger


__all__ = ["Header"]


class Header(ctk.CTkFrame):
    """Header component for the main application window.

    A simple header frame containing only the application title label.
    Fixed height, spans full width of the window.

    Attributes:
        title_label: The label displaying the application title.
    """

    def __init__(
        self,
        master: ctk.CTkFrame,
        config: Optional[Config] = None,
        logger=None,
        height: int = 60,
        **kwargs,
    ) -> None:
        """Initialize the Header component.

        Args:
            master: Parent widget (typically the main window).
            config: Optional Config instance for getting app title.
            logger: Optional logger instance.
            height: Fixed height of the header in pixels. Defaults to 60.
            **kwargs: Additional keyword arguments passed to CTkFrame.
        """
        super().__init__(master, height=height, corner_radius=0, fg_color="transparent", **kwargs)

        self._logger = logger or get_logger("header")
        self._config = config

        # Prevent frame from shrinking
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)

        # Get app title from config or use default
        app_title = "AI Kids Studio Pro"
        if self._config:
            app_title = self._config.get("app", "title", default=app_title)

        # Create title label
        self.title_label = ctk.CTkLabel(
            self,
            text=app_title,
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w",
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=20, pady=10)

        self._logger.debug("Header initialized with title: %s", app_title)

    def set_title(self, title: str) -> None:
        """Update the header title.

        Args:
            title: New title text to display.
        """
        self.title_label.configure(text=title)
        self._logger.debug("Header title updated: %s", title)