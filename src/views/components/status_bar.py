"""Status Bar component for AI Kids Studio Pro.

This module provides the StatusBar component for the main application window.
"""

from __future__ import annotations

import customtkinter as ctk
from typing import Optional

from src.logging.logger import get_logger


__all__ = ["StatusBar"]


class StatusBar(ctk.CTkFrame):
    """Status Bar component for the main application window.

    A fixed-height status bar at the bottom of the window displaying status messages.
    Default text: "Ready"

    Attributes:
        DEFAULT_HEIGHT: Default fixed height of the status bar in pixels.
        DEFAULT_TEXT: Default status text.
    """

    DEFAULT_HEIGHT = 30
    DEFAULT_TEXT = "Ready"

    def __init__(
        self,
        master: ctk.CTkFrame,
        height: Optional[int] = None,
        initial_text: Optional[str] = None,
        logger=None,
        **kwargs,
    ) -> None:
        """Initialize the StatusBar component.

        Args:
            master: Parent widget (typically the main window).
            height: Optional fixed height in pixels. Defaults to DEFAULT_HEIGHT.
            initial_text: Optional initial status text. Defaults to DEFAULT_TEXT.
            logger: Optional logger instance.
            **kwargs: Additional keyword arguments passed to CTkFrame.
        """
        bar_height = height or self.DEFAULT_HEIGHT
        status_text = initial_text or self.DEFAULT_TEXT

        super().__init__(
            master,
            height=bar_height,
            corner_radius=0,
            fg_color="transparent",
            **kwargs,
        )

        self._logger = logger or get_logger("status_bar")
        self._height = bar_height

        # Prevent frame from shrinking
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)

        # Create status label
        self.status_label = ctk.CTkLabel(
            self,
            text=status_text,
            font=ctk.CTkFont(size=11),
            anchor="w",
        )
        self.status_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self._logger.debug("StatusBar initialized with text: %s", status_text)

    @property
    def height(self) -> int:
        """Get the status bar height.

        Returns:
            The fixed height of the status bar in pixels.
        """
        return self._height

    def set_status(self, text: str) -> None:
        """Update the status bar text.

        Args:
            text: New status text to display.
        """
        self.status_label.configure(text=text)
        self._logger.debug("Status updated: %s", text)

    def set_ready(self) -> None:
        """Set status to default 'Ready' state."""
        self.set_status(self.DEFAULT_TEXT)

    def set_busy(self, message: str = "Working...") -> None:
        """Set status to busy state with custom message.

        Args:
            message: Busy message to display.
        """
        self.set_status(message)