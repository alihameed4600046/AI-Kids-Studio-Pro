"""Sidebar component for AI Kids Studio Pro.

This module provides the Sidebar component for the main application window.
"""

from __future__ import annotations

from typing import Optional, Callable

import customtkinter as ctk

from src.logging.logger import get_logger


__all__ = ["Sidebar"]


class Sidebar(ctk.CTkFrame):
    """Sidebar component for the main application window.

    A fixed-width sidebar frame that renders a vertical button list.
    """

    DEFAULT_WIDTH = 260

    def __init__(
        self,
        master: ctk.CTkFrame,
        width: Optional[int] = None,
        logger=None,
        on_nav_click: Optional[Callable[[str], None]] = None,
        **kwargs,
    ) -> None:
        """Initialize the Sidebar component.

        Args:
            master: Parent widget (typically the main window).
            width: Optional fixed width in pixels. Defaults to DEFAULT_WIDTH.
            logger: Optional logger instance.
            on_nav_click: Optional callback when a nav button is clicked.
                Receives the nav item name as argument.
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
        self._on_nav_click = on_nav_click

        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)

        self.nav_buttons: list[ctk.CTkButton] = []

        nav_items = [
            "Home",
            "Projects",
            "Prompts",
            "Images",
            "Voices",
            "Videos",
            "Settings",
        ]

        for index, item in enumerate(nav_items):
            button = ctk.CTkButton(
                self,
                text=item,
                height=40,
                corner_radius=8,
                fg_color="transparent",
                hover_color=("gray80", "gray25"),
                text_color=("black", "white"),
                font=ctk.CTkFont(size=15, weight="bold"),
                border_width=0,
                anchor="w",
                command=lambda name=item: self._on_button_click(name),
            )
            button.grid(
                row=index,
                column=0,
                padx=18,
                pady=(0 if index == 0 else 6),
                sticky="ew",
            )
            self.nav_buttons.append(button)

        self._logger.debug("Sidebar initialized with width: %d", sidebar_width)

    def _on_button_click(self, name: str) -> None:
        """Handle nav button click and invoke callback if provided."""
        if self._on_nav_click:
            self._on_nav_click(name)
        self._logger.debug("Nav button clicked: %s", name)

    @property
    def width(self) -> int:
        return self._width