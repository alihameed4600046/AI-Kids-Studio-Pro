"""Sidebar component for AI Kids Studio Pro.

This module provides the Sidebar component for the main application window.
"""

from __future__ import annotations

from typing import Optional

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
                hover_color=("gray85", "gray20"),
                border_width=0,
                anchor="w",
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

    @property
    def width(self) -> int:
        return self._width