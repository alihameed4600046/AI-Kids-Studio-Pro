"""Sidebar component for AI Kids Studio Pro.

This module provides the Sidebar component for the main application window.
"""

from __future__ import annotations

import customtkinter as ctk
from typing import Optional

from src.logging.logger import get_logger


__all__ = ["Sidebar"]


class Sidebar(ctk.CTkFrame):
    """Sidebar component for the main application window.

    A fixed-width sidebar frame serving as a placeholder for future navigation.
    Fixed width, spans full height of content area.

    Attributes:
        DEFAULT_WIDTH: Default fixed width of the sidebar in pixels.
    """

    DEFAULT_WIDTH = 260

    def __init__(
        self,
        master: ctk.CTkFrame,
        width: Optional[int] = None,
        logger=None,
        **kwargs,
    ) -> None:
        """Initialize the Sidebar component.

        Args:
            master: Parent widget (typically the main window).
            width: Optional fixed width in pixels. Defaults to DEFAULT_WIDTH.
            logger: Optional logger instance.
            **kwargs: Additional keyword arguments passed to CTkFrame.
        """
        sidebar_width = width or self.DEFAULT_WIDTH

        super().__init__(
            master,
            width=sidebar_width,
            corner_radius=0,
            fg_color="transparent",
            **kwargs,
        )

        self._logger = logger or get_logger("sidebar")
        self._width = sidebar_width

        # Prevent frame from shrinking/expanding
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Placeholder label for empty sidebar
        self._placeholder_label = ctk.CTkLabel(
            self,
            text="Sidebar\n(Placeholder)",
            font=ctk.CTkFont(size=12),
            text_color="gray",
        )
        self._placeholder_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self._logger.debug("Sidebar initialized with width: %d", sidebar_width)

    @property
    def width(self) -> int:
        """Get the sidebar width.

        Returns:
            The fixed width of the sidebar in pixels.
        """
        return self._width

    def clear_placeholder(self) -> None:
        """Remove the placeholder label to allow adding custom content."""
        self._placeholder_label.grid_remove()
        self._logger.debug("Sidebar placeholder cleared")

    def set_placeholder_text(self, text: str) -> None:
        """Update the placeholder text.

        Args:
            text: New placeholder text to display.
        """
        self._placeholder_label.configure(text=text)
        self._logger.debug("Sidebar placeholder text updated: %s", text)