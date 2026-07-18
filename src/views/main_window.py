"""Main application window implementation.

This module provides the main application window using CustomTkinter.
It creates the root window with proper configuration, theme integration,
and empty layout containers for future UI modules.
"""

from __future__ import annotations

import customtkinter as ctk
from typing import Optional
from pathlib import Path

from src.bootstrap import ApplicationBootstrap
from src.theme.theme_manager import ThemeManager
from src.theme.theme_models import ThemeSettings
from src.logging.logger import get_logger
from src.config import Config
from src.views.navigation import NavigationManager, HomePage


__all__ = ["MainWindow"]


class MainWindow(ctk.CTk):
    """Main application window using CustomTkinter.

    This class creates the root application window with:
    - Application title from configuration
    - Initial window size from settings
    - Minimum window size constraints
    - Centered window on startup
    - Maximize/restore support
    - ThemeManager integration for appearance
    - Empty layout containers for future UI modules:
        - Header Frame
        - Sidebar Container
        - Content Container
        - Status Bar Container

    Attributes:
        bootstrap: Application bootstrap instance for accessing managers.
        theme_manager: Theme manager for appearance handling.
        logger: Application logger.
    """

    def __init__(
        self,
        bootstrap: ApplicationBootstrap,
        config: Optional[Config] = None,
    ) -> None:
        """Initialize the main application window.

        Args:
            bootstrap: Initialized ApplicationBootstrap instance.
            config: Optional Config instance. If None, uses bootstrap.config.
        """
        # Initialize CustomTkinter root window
        super().__init__()

        self._bootstrap = bootstrap
        self._config = config or bootstrap.config
        self._theme_manager = bootstrap.theme_manager
        self._logger = get_logger("main_window")

        # Get window settings from settings manager
        window_settings = self._bootstrap.settings_manager.get("window", {"width": 1200, "height": 800})
        min_width = self._config.get("ui", "min_width", default=800)
        min_height = self._config.get("ui", "min_height", default=600)
        app_title = self._config.get("app", "title", default="AI Kids Studio Pro")

        # Configure window
        self.title(app_title)
        self.geometry(f"{window_settings['width']}x{window_settings['height']}")
        self.minsize(min_width, min_height)

        # Center window on screen
        self._center_window()

        # Apply theme from ThemeManager
        self._apply_theme()

        # Configure grid layout for main containers
        self._setup_layout()

        # Create empty layout containers
        self._create_containers()

        # Bind window events
        self._bind_events()

        # Save window geometry on close
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._logger.info("Main window initialized: %s (%dx%d)", app_title, window_settings['width'], window_settings['height'])

        # Initialize NavigationManager and register HomePage
        self._navigation_manager = NavigationManager(self.content_container, self._logger)
        self._navigation_manager.register_page("home", HomePage)
        self._navigation_manager.navigate_to("home")
        self._logger.info("NavigationManager initialized with HomePage")

    def _center_window(self) -> None:
        """Center the window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _apply_theme(self) -> None:
        """Apply theme settings from ThemeManager."""
        theme_settings: ThemeSettings = self._theme_manager.get_settings()

        # Set appearance mode
        mode = theme_settings.mode
        if mode == "system":
            ctk.set_appearance_mode("system")
        elif mode == "dark":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

        # Set default color theme (CustomTkinter built-in themes)
        # CustomTkinter supports "blue", "green", "dark-blue" themes
        # We map our accent color to the closest built-in theme
        accent = theme_settings.accent_color.lower()
        if "green" in accent or "#50e3c2" in accent.lower() or "#00ff00" in accent.lower():
            ctk.set_default_color_theme("green")
        elif "blue" in accent or "#0066ff" in accent.lower() or "#4a90e2" in accent.lower():
            ctk.set_default_color_theme("blue")
        else:
            ctk.set_default_color_theme("dark-blue")

        # Apply scaling
        scale = theme_settings.scale / 100.0
        ctk.set_widget_scaling(scale)
        ctk.set_window_scaling(scale)

        self._logger.debug("Theme applied: mode=%s, accent=%s, scale=%s", mode, accent, scale)

    def _setup_layout(self) -> None:
        """Configure the main grid layout for the window."""
        # Configure grid weights for responsive layout
        # Row 0: Header (fixed height)
        # Row 1: Main content area (sidebar + content) - expands
        # Row 2: Status bar (fixed height)
        self.grid_rowconfigure(0, weight=0)  # Header - fixed
        self.grid_rowconfigure(1, weight=1)  # Content area - expands
        self.grid_rowconfigure(2, weight=0)  # Status bar - fixed

        # Column 0: Sidebar (fixed width, will be set by sidebar module later)
        # Column 1: Content area - expands
        self.grid_columnconfigure(0, weight=0, minsize=0)  # Sidebar - fixed width
        self.grid_columnconfigure(1, weight=1)  # Content - expands

    def _create_containers(self) -> None:
        """Create empty layout containers for future UI modules.

        Creates four empty container frames:
        - Header Frame (row 0, spans both columns)
        - Sidebar Container (row 1, column 0)
        - Content Container (row 1, column 1)
        - Status Bar Container (row 2, spans both columns)

        All containers are empty placeholders for future phases.
        """
        theme_settings = self._theme_manager.get_settings()
        padding = theme_settings.padding
        radius = theme_settings.widget_radius

        # Header Frame - spans full width at top
        self.header_frame = ctk.CTkFrame(
            self,
            height=60,
            corner_radius=0,
            fg_color="transparent",
        )
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)
        self.header_frame.grid_propagate(False)  # Maintain fixed height
        self.header_frame.grid_columnconfigure(0, weight=1)

        # Sidebar Container - left side, fixed width
        self.sidebar_container = ctk.CTkFrame(
            self,
            width=260,
            corner_radius=0,
            fg_color="transparent",
        )
        self.sidebar_container.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar_container.grid_propagate(False)  # Maintain fixed width
        self.sidebar_container.grid_rowconfigure(0, weight=1)
        self.sidebar_container.grid_columnconfigure(0, weight=1)

        # Content Container - main area, expands
        self.content_container = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="transparent",
        )
        self.content_container.grid(row=1, column=1, sticky="nsew", padx=padding, pady=padding)
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        # Status Bar Container - bottom, spans full width
        self.status_bar_container = ctk.CTkFrame(
            self,
            height=30,
            corner_radius=0,
            fg_color="transparent",
        )
        self.status_bar_container.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)
        self.status_bar_container.grid_propagate(False)  # Maintain fixed height
        self.status_bar_container.grid_columnconfigure(0, weight=1)

        self._logger.debug("Layout containers created: header, sidebar, content, status_bar")

    def _bind_events(self) -> None:
        """Bind window events for state management."""
        self.bind("<Configure>", self._on_window_configure)
        self.bind("<Map>", self._on_window_map)

    def _on_window_configure(self, event: ctk.Event) -> None:
        """Handle window configure events (resize, move, maximize/restore).

        Args:
            event: The configure event.
        """
        # Only handle root window events, not child widgets
        if event.widget is self:
            # Save window geometry when resized/moved (but not minimized)
            if self.state() != "iconic":
                self._save_window_geometry()

    def _on_window_map(self, event: ctk.Event) -> None:
        """Handle window map event (window shown).

        Args:
            event: The map event.
        """
        if event.widget is self:
            # Ensure window is centered on first show
            self._center_window()

    def _save_window_geometry(self) -> None:
        """Save current window geometry to settings."""
        try:
            geometry = {
                "width": self.winfo_width(),
                "height": self.winfo_height(),
                "x": self.winfo_x(),
                "y": self.winfo_y(),
                "state": self.state(),
            }
            self._bootstrap.settings_manager.set("window", geometry)
            self._logger.debug("Window geometry saved: %s", geometry)
        except Exception as exc:
            self._logger.warning("Failed to save window geometry: %s", exc)

    def _on_close(self) -> None:
        """Handle window close event."""
        self._logger.info("Main window closing, saving geometry and shutting down")
        self._save_window_geometry()
        self._bootstrap.shutdown()
        self.destroy()

    # ------------------------------------------------------------------
    # Public API for future UI modules
    # ------------------------------------------------------------------

    def get_header_frame(self) -> ctk.CTkFrame:
        """Get the header frame container.

        Returns:
            The header frame for adding header UI components.
        """
        return self.header_frame

    def get_sidebar_container(self) -> ctk.CTkFrame:
        """Get the sidebar container.

        Returns:
            The sidebar container for adding navigation UI.
        """
        return self.sidebar_container

    def get_content_container(self) -> ctk.CTkFrame:
        """Get the main content container.

        Returns:
            The content container for adding page content.
        """
        return self.content_container

    def get_status_bar_container(self) -> ctk.CTkFrame:
        """Get the status bar container.

        Returns:
            The status bar container for adding status UI.
        """
        return self.status_bar_container

    def apply_theme(self) -> None:
        """Re-apply theme settings (call after theme changes)."""
        self._apply_theme()
        self._logger.info("Theme reapplied to main window")

    @property
    def bootstrap(self) -> ApplicationBootstrap:
        """Get the bootstrap instance."""
        return self._bootstrap

    @property
    def theme_manager(self) -> ThemeManager:
        """Get the theme manager instance."""
        return self._theme_manager

    @property
    def logger(self):
        """Get the logger instance."""
        return self._logger