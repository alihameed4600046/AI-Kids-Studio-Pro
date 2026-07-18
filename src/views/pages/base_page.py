"""Base page class for AI Kids Studio Pro.

This module provides the BasePage abstract base class that all pages
in the navigation system must inherit from.
"""

from __future__ import annotations

import customtkinter as ctk
from typing import Any
from abc import ABC, abstractmethod

from src.logging.logger import get_logger


__all__ = ["BasePage"]


class BasePage(ctk.CTkFrame, ABC):
    """Base class for all pages in the navigation system.

    All pages must inherit from BasePage and implement the lifecycle hooks.
    """

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        navigation_manager: "NavigationManager",
        **kwargs: Any,
    ) -> None:
        """Initialize the base page.

        Args:
            master: Parent widget (typically the content container).
            navigation_manager: Reference to the NavigationManager instance.
            **kwargs: Additional arguments passed to CTkFrame.
        """
        super().__init__(master, **kwargs)
        self._navigation_manager = navigation_manager
        self._logger = get_logger(f"page.{self.__class__.__name__}")
        self._is_visible = False

    @property
    def navigation_manager(self) -> "NavigationManager":
        """Get the navigation manager instance."""
        return self._navigation_manager

    @property
    def is_visible(self) -> bool:
        """Check if the page is currently visible."""
        return self._is_visible

    @property
    def page_name(self) -> str:
        """Get the page name (class name by default)."""
        return self.__class__.__name__

    @abstractmethod
    def on_show(self) -> None:
        """Called when the page becomes visible.

        Override this method to perform initialization when the page is shown.
        """
        self._is_visible = True
        self._logger.debug("Page shown: %s", self.page_name)

    @abstractmethod
    def on_hide(self) -> None:
        """Called when the page is hidden.

        Override this method to perform cleanup when the page is hidden.
        """
        self._is_visible = False
        self._logger.debug("Page hidden: %s", self.page_name)

    def on_navigate_to(self, **kwargs: Any) -> None:
        """Called when navigating to this page with optional parameters.

        Args:
            **kwargs: Optional parameters passed during navigation.
        """
        self._logger.debug("Navigated to %s with params: %s", self.page_name, kwargs)

    def on_navigate_from(self) -> None:
        """Called when navigating away from this page."""
        self._logger.debug("Navigating from %s", self.page_name)