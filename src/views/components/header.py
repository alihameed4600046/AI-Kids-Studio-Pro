"""Header component for AI Kids Studio Pro.

This module provides the Header component for the main application window.
"""

from __future__ import annotations

from typing import Optional, Callable

import customtkinter as ctk


__all__ = ["Header"]


class Header(ctk.CTkFrame):
    """Header component for the main application window.

    A fixed-height header frame with title, version, and action buttons.
    """

    def __init__(
        self,
        master,
        height: int = 60,
        logger=None,
        on_new_project: Optional[Callable[[], None]] = None,
        **kwargs,
    ):
        """Initialize the Header component.

        Args:
            master: Parent widget.
            height: Fixed height in pixels. Defaults to 60.
            logger: Optional logger instance.
            on_new_project: Optional callback when "New Project" button is clicked.
            **kwargs: Additional keyword arguments passed to CTkFrame.
        """
        super().__init__(
            master,
            height=height,
            corner_radius=0,
            fg_color="transparent",
            **kwargs
        )

        self.pack_propagate(False)
        self._on_new_project = on_new_project

        # Title label on the left
        self.title_label = ctk.CTkLabel(self, text="AI Kids Studio Pro")
        self.title_label.pack(side="left", padx=(10, 0))

        # New Project button
        self.new_project_button = ctk.CTkButton(
            self,
            text="New Project",
            height=32,
            corner_radius=6,
            command=self._handle_new_project,
        )
        self.new_project_button.pack(side="right", padx=(0, 10), pady=10)

        # Version label on the right
        self.version_label = ctk.CTkLabel(self, text="v1.0")
        self.version_label.pack(side="right", padx=(0, 10))

    def _handle_new_project(self) -> None:
        """Handle New Project button click and invoke callback if provided."""
        if self._on_new_project:
            self._on_new_project()