"""Navigation framework for AI Kids Studio Pro.

This module provides the NavigationManager class for managing page navigation,
page registration, page switching, and page lifecycle hooks.
"""

from __future__ import annotations

import customtkinter as ctk
from typing import Dict, Optional, Type, Callable, Any
import logging

from src.logging.logger import get_logger
from src.views.pages.base_page import BasePage


__all__ = ["NavigationManager"]


class NavigationManager:
    """Manages page navigation for the application.

    The NavigationManager handles:
    - Page registration (registering page classes)
    - Page instantiation and caching
    - Page switching with lifecycle hooks
    - Current page tracking
    - Safe navigation with duplicate prevention
    - Page lifecycle hooks (on_show, on_hide, on_navigate_to, on_navigate_from)

    The NavigationManager attaches to the MainWindow's content container.
    """

    def __init__(
        self,
        content_container: ctk.CTkFrame,
        logger: logging.Logger | None = None,
        shared_dependencies: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the NavigationManager.

        Args:
            content_container: The content container frame from MainWindow.
            logger: Optional logger instance. If None, creates a default logger.
            shared_dependencies: Shared dependencies to be passed to page instances.
        """
        self._content_container = content_container
        self._logger = logger or get_logger("navigation")
        self._shared_dependencies = shared_dependencies or {}

        # Page registry: page_name -> page_class
        self._page_registry: Dict[str, Type[BasePage]] = {}

        # Page instances: page_name -> page_instance
        self._page_instances: Dict[str, BasePage] = {}

        # Current page tracking
        self._current_page: Optional[BasePage] = None
        self._current_page_name: Optional[str] = None

        # Navigation history for potential back navigation
        self._history: list[str] = []

        # Navigation callbacks
        self._on_page_changed: Optional[Callable[[str, str], None]] = None

        # Configure content container grid
        self._content_container.grid_rowconfigure(0, weight=1)
        self._content_container.grid_columnconfigure(0, weight=1)

        self._logger.info("NavigationManager initialized")

    # ------------------------------------------------------------------
    # Page Registration
    # ------------------------------------------------------------------

    def register_page(self, page_name: str, page_class: Type[BasePage]) -> None:
        """Register a page class with the navigation manager.

        Args:
            page_name: Unique name for the page (used for navigation).
            page_class: The page class (must inherit from BasePage).

        Raises:
            ValueError: If page_name is already registered or page_class
                doesn't inherit from BasePage.
        """
        if page_name in self._page_registry:
            raise ValueError(f"Page '{page_name}' is already registered")

        if not issubclass(page_class, BasePage):
            raise ValueError(f"Page class must inherit from BasePage, got {page_class}")

        self._page_registry[page_name] = page_class
        self._logger.info("Registered page: %s -> %s", page_name, page_class.__name__)

    def unregister_page(self, page_name: str) -> None:
        """Unregister a page class.

        Args:
            page_name: Name of the page to unregister.

        Raises:
            KeyError: If page_name is not registered.
        """
        if page_name not in self._page_registry:
            raise KeyError(f"Page '{page_name}' is not registered")

        # Also remove instance if it exists
        if page_name in self._page_instances:
            self._page_instances[page_name].destroy()
            del self._page_instances[page_name]

        del self._page_registry[page_name]
        self._logger.info("Unregistered page: %s", page_name)

    def is_page_registered(self, page_name: str) -> bool:
        """Check if a page is registered.

        Args:
            page_name: Name of the page to check.

        Returns:
            True if the page is registered, False otherwise.
        """
        return page_name in self._page_registry

    def get_registered_pages(self) -> list[str]:
        """Get list of registered page names.

        Returns:
            List of registered page names.
        """
        return list(self._page_registry.keys())

    # ------------------------------------------------------------------
    # Page Instantiation
    # ------------------------------------------------------------------

    def _get_or_create_page(self, page_name: str) -> BasePage:
        """Get an existing page instance or create a new one.

        Args:
            page_name: Name of the page to get or create.

        Returns:
            The page instance.

        Raises:
            KeyError: If page_name is not registered.
        """
        if page_name not in self._page_registry:
            raise KeyError(f"Page '{page_name}' is not registered")

        if page_name not in self._page_instances:
            page_class = self._page_registry[page_name]
            if page_name == "prompts":
                self._page_instances[page_name] = page_class(
                    self._content_container,
                    self,
                    variable_registry=self._shared_dependencies["variable_registry"],
                    template_registry=self._shared_dependencies["template_registry"],
                )
            else:
                self._page_instances[page_name] = page_class(
                    self._content_container,
                    self,
                )
            self._logger.debug("Created page instance: %s", page_name)

        return self._page_instances[page_name]

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def navigate_to(self, page_name: str, **kwargs: Any) -> bool:
        """Navigate to a page.

        Args:
            page_name: Name of the page to navigate to.
            **kwargs: Optional parameters to pass to the page's on_navigate_to.

        Returns:
            True if navigation was successful, False if already on that page
                (duplicate prevention).

        Raises:
            KeyError: If page_name is not registered.
        """
        if not self.is_page_registered(page_name):
            raise KeyError(f"Page '{page_name}' is not registered")

        # Duplicate page prevention
        if self._current_page_name == page_name:
            self._logger.debug("Already on page '%s', skipping navigation", page_name)
            # Still call on_navigate_to with new params
            if self._current_page:
                self._current_page.on_navigate_to(**kwargs)
            return False

        # Get or create the target page
        target_page = self._get_or_create_page(page_name)

        # Call on_navigate_from on current page
        if self._current_page:
            self._current_page.on_navigate_from()
            self._current_page.on_hide()
            self._current_page.grid_remove()

        # Update history
        if self._current_page_name:
            self._history.append(self._current_page_name)

        # Show new page
        target_page.grid(row=0, column=0, sticky="nsew")
        target_page.on_navigate_to(**kwargs)
        target_page.on_show()

        # Update current page tracking
        previous_page = self._current_page_name
        self._current_page = target_page
        self._current_page_name = page_name

        # Notify page change callback
        if self._on_page_changed and previous_page:
            self._on_page_changed(previous_page, page_name)

        self._logger.info("Navigated from '%s' to '%s'", previous_page or "none", page_name)
        return True

    def navigate_back(self) -> bool:
        """Navigate back to the previous page in history.

        Returns:
            True if navigation was successful, False if no history.
        """
        if not self._history:
            self._logger.debug("No history to navigate back to")
            return False

        previous_page = self._history.pop()
        return self.navigate_to(previous_page)

    def get_current_page(self) -> Optional[BasePage]:
        """Get the currently displayed page.

        Returns:
            The current page instance, or None if no page is shown.
        """
        return self._current_page

    def get_current_page_name(self) -> Optional[str]:
        """Get the name of the currently displayed page.

        Returns:
            The current page name, or None if no page is shown.
        """
        return self._current_page_name

    def is_on_page(self, page_name: str) -> bool:
        """Check if currently on a specific page.

        Args:
            page_name: Name of the page to check.

        Returns:
            True if currently on that page, False otherwise.
        """
        return self._current_page_name == page_name

    # ------------------------------------------------------------------
    # Page Lifecycle
    # ------------------------------------------------------------------

    def show_page(self, page_name: str) -> bool:
        """Show a page without adding to history (for programmatic show).

        Args:
            page_name: Name of the page to show.

        Returns:
            True if shown, False if already shown.
        """
        return self.navigate_to(page_name)

    def hide_current_page(self) -> None:
        """Hide the current page without navigating to another."""
        if self._current_page:
            self._current_page.on_hide()
            self._current_page.grid_remove()
            self._current_page = None
            self._current_page_name = None
            self._logger.debug("Current page hidden")

    def destroy_page(self, page_name: str) -> None:
        """Destroy a page instance (will be recreated on next navigate).

        Args:
            page_name: Name of the page to destroy.

        Raises:
            KeyError: If page_name is not registered.
        """
        if page_name not in self._page_registry:
            raise KeyError(f"Page '{page_name}' is not registered")

        if page_name in self._page_instances:
            page = self._page_instances[page_name]
            if page is self._current_page:
                self.hide_current_page()
            page.destroy()
            del self._page_instances[page_name]
            self._logger.info("Destroyed page instance: %s", page_name)

    def clear_history(self) -> None:
        """Clear navigation history."""
        self._history.clear()
        self._logger.debug("Navigation history cleared")

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------

    def set_page_changed_callback(
        self, callback: Callable[[str, str], None]
    ) -> None:
        """Set a callback to be called when page changes.

        Args:
            callback: Function(previous_page_name, new_page_name) -> None
        """
        self._on_page_changed = callback

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def content_container(self) -> ctk.CTkFrame:
        """Get the content container frame."""
        return self._content_container

    @property
    def current_page(self) -> Optional[BasePage]:
        """Get the current page instance."""
        return self._current_page

    @property
    def current_page_name(self) -> Optional[str]:
        """Get the current page name."""
        return self._current_page_name

    @property
    def history(self) -> list[str]:
        """Get navigation history (copy)."""
        return self._history.copy()

    @property
    def registered_pages(self) -> list[str]:
        """Get list of registered page names."""
        return list(self._page_registry.keys())