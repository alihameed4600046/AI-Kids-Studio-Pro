"""Home page for AI Kids Studio Pro.

This module provides the HomePage class, a placeholder home page
for the application.
"""

from __future__ import annotations

import customtkinter as ctk
from typing import Any, TYPE_CHECKING

from src.views.pages.base_page import BasePage

if TYPE_CHECKING:
    from src.navigation.navigation_manager import NavigationManager


__all__ = ["HomePage"]


class HomePage(BasePage):
    """Placeholder home page for the application.

    This is a lightweight placeholder page that displays a simple label.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        navigation_manager: "NavigationManager",
        **kwargs: Any,
    ) -> None:
        """Initialize the home page.

        Args:
            master: Parent widget.
            navigation_manager: Reference to the NavigationManager instance.
            **kwargs: Additional arguments passed to CTkFrame.
        """
        super().__init__(master, navigation_manager, **kwargs)

        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a simple label
        self._label = ctk.CTkLabel(
            self,
            text="AI Kids Studio Pro\nHome Page",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self._label.grid(row=0, column=0, padx=20, pady=20)

    def on_show(self) -> None:
        """Called when the home page becomes visible."""
        super().on_show()
        self._logger.info("Home page displayed")

    def on_hide(self) -> None:
        """Called when the home page is hidden."""
        super().on_hide()
        self._logger.info("Home page hidden")

    def on_navigate_to(self, **kwargs: Any) -> None:
        """Called when navigating to the home page."""
        super().on_navigate_to(**kwargs)
        self._label.configure(text=f"AI Kids Studio Pro\nHome Page\n\nParams: {kwargs}")