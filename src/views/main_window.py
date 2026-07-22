"""Main application window implementation.

This module provides the main application window using CustomTkinter.
It creates the root window with proper configuration, theme integration,
and layout using reusable UI components.
"""

from __future__ import annotations

import customtkinter as ctk
from tkinter import filedialog
from typing import Optional

from src.bootstrap import ApplicationBootstrap
from src.theme.theme_manager import ThemeManager
from src.theme.theme_models import ThemeSettings
from src.logging.logger import get_logger
from src.config import Config
from src.views.navigation import NavigationManager, HomePage
from src.views.components import Header, Sidebar, StatusBar
from src.views.dialogs.create_project_dialog import CreateProjectDialog
from src.project.project_service import ProjectService


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
        self._project_service = ProjectService()
        self.current_project = None

        # Get window settings from settings manager
        window_settings = self._bootstrap.settings_manager.get("window", {"width": 1200, "height": 800})
        min_width = self._config.get("ui", "min_width", default=800)
        min_height = self._config.get("ui", "min_height", default=600)
        self._app_title = self._config.get("app", "title", default="AI Kids Studio Pro")

        # Configure window
        self.title(self._app_title)
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

        self._logger.info("Main window initialized: %s (%dx%d)", self._app_title, window_settings['width'], window_settings['height'])

        # Initialize NavigationManager and register HomePage
        self._navigation_manager = NavigationManager(self.content_container, self._logger)
        self._navigation_manager.register_page("home", HomePage)
        self._navigation_manager.register_page("projects", HomePage)
        self._navigation_manager.register_page("prompts", HomePage)
        self._navigation_manager.register_page("voices", HomePage)
        self._navigation_manager.register_page("settings", HomePage)
        self._navigation_manager.navigate_to("home")
        self._logger.info("NavigationManager initialized with HomePage")

        # Initialize recent projects display
        self._refresh_recent_projects()

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
        """Create layout containers using reusable UI components.

        Creates four container components:
        - Header (row 0, spans both columns)
        - Sidebar (row 1, column 0)
        - Content Container (row 1, column 1)
        - Status Bar (row 2, spans both columns)
        """
        theme_settings = self._theme_manager.get_settings()
        padding = theme_settings.padding

        # Header - spans full width at top
        self.header = Header(self, height=60, on_new_project=self._open_create_project_dialog)
        self.header.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)

        # Sidebar - left side, fixed width
        self.sidebar = Sidebar(self, width=260, on_nav_click=self._on_sidebar_navigation)
        self.sidebar.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        # Content Container - main area, expands
        self.content_container = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="transparent",
        )
        self.content_container.grid(row=1, column=1, sticky="nsew", padx=padding, pady=padding)
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        # Status Bar - bottom, spans full width
        self.status_bar = StatusBar(self, height=30)
        self.status_bar.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)

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

    def _on_sidebar_navigation(self, page_name: str) -> None:
        """Handle sidebar navigation callback.

        Args:
            page_name: Name of the page to navigate to.
        """
        try:
            self._navigation_manager.navigate_to(page_name.lower())
        except KeyError:
            # Ignore gracefully if page is not registered
            self._logger.debug("Page '%s' not registered, ignoring navigation", page_name)

    def _open_create_project_dialog(self) -> None:
        """Open the Create Project dialog as a modal window.

        Creates the dialog, makes it modal using grab_set() and wait_window(),
        and handles the result after the dialog closes.
        """
        dialog = CreateProjectDialog(self)
        dialog.grab_set()
        self.wait_window(dialog)

        # After dialog closes, check if a project was created
        if dialog.created_project is not None:
            self.current_project = dialog.created_project
            project_name = dialog.created_project.name
            self.status_bar.set_status(f"Project created: {project_name}")
            self.title(f"{self._app_title} - {project_name}")
            self._logger.info("Project created: %s", project_name)
            self._project_service.add_recent_project(dialog.created_project)
            self._refresh_recent_projects()
        else:
            self._logger.debug("Create Project dialog cancelled")

    def _open_existing_project(self) -> None:
        """Open an existing project from a folder selection dialog.

        Opens a folder selection dialog for the user to choose a project directory.
        If the user cancels, returns immediately.
        Attempts to open the project using ProjectService.open_project().
        On success, updates the current project, window title, status bar, and logs success.
        On FileNotFoundError, shows an error dialog.
        On other exceptions, logs the exception and shows a friendly error dialog.
        """
        # Ask user to select a project folder
        selected_folder = filedialog.askdirectory(
            parent=self,
            title="Open Project - Select Project Folder"
        )

        # User cancelled
        if not selected_folder:
            self._logger.debug("Open Project dialog cancelled by user")
            return

        try:
            # Open the project
            project = self._project_service.open_project(selected_folder)

            # On success
            self.current_project = project
            project_name = project.name
            self.title(f"{self._app_title} - {project_name}")
            self.status_bar.set_status(f"Project opened: {project_name}")
            self._logger.info("Project opened: %s", project_name)
            self._refresh_recent_projects()

        except FileNotFoundError:
            # Show error dialog for missing project.json
            self._logger.warning("Project file not found in: %s", selected_folder)
            ctk.CTkMessagebox(
                title="Project Not Found",
                message="No project.json found in the selected folder.",
                icon="cancel",
                option_1="OK"
            )
        except Exception as exc:
            # Log exception and show friendly error dialog
            self._logger.exception("Failed to open project: %s", exc)
            ctk.CTkMessagebox(
                title="Error Opening Project",
                message=f"An error occurred while opening the project:\n{str(exc)}",
                icon="cancel",
                option_1="OK"
            )

    def _refresh_recent_projects(self) -> None:
        """Refresh the recent projects display on the Home page.

        Reads recent projects from ProjectService and updates the Home page
        placeholder area with a simple vertical list of recent project names.
        If no recent projects exist, shows "No recent projects".
        """
        try:
            recent_paths = self._project_service.get_recent_projects()

            # Get the current home page instance
            home_page = self._navigation_manager.get_current_page()
            if home_page and hasattr(home_page, '_recent_projects_frame'):
                # Update existing display
                self._update_recent_projects_display(home_page, recent_paths)
            else:
                # Home page doesn't have the recent projects frame yet, create it
                self._create_recent_projects_display(home_page, recent_paths)

        except Exception as exc:
            self._logger.warning("Failed to refresh recent projects: %s", exc)

    def _create_recent_projects_display(self, home_page, recent_paths: list[str]) -> None:
        """Create the recent projects display on the Home page.

        Args:
            home_page: The HomePage instance.
            recent_paths: List of recent project paths.
        """
        if not home_page:
            return

        import customtkinter as ctk

        # Clear existing content
        for widget in home_page.winfo_children():
            widget.destroy()

        # Configure grid
        home_page.grid_rowconfigure(0, weight=1)
        home_page.grid_columnconfigure(0, weight=1)

        # Create a frame for recent projects
        recent_frame = ctk.CTkFrame(home_page, fg_color="transparent")
        recent_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        recent_frame.grid_columnconfigure(0, weight=1)

        # Title label
        title_label = ctk.CTkLabel(
            recent_frame,
            text="Recent Projects",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w"
        )
        title_label.grid(row=0, column=0, sticky="ew", pady=(0, 15))

        # Store reference for updates
        home_page._recent_projects_frame = recent_frame
        home_page._recent_project_labels = []

        # Display recent projects
        self._update_recent_projects_display(home_page, recent_paths)

    def _update_recent_projects_display(self, home_page, recent_paths: list[str]) -> None:
        """Update the recent projects display.

        Args:
            home_page: The HomePage instance.
            recent_paths: List of recent project paths.
        """
        if not home_page or not hasattr(home_page, '_recent_projects_frame'):
            return

        import customtkinter as ctk
        from pathlib import Path

        recent_frame = home_page._recent_projects_frame

        # Clear existing project labels
        for label in getattr(home_page, '_recent_project_labels', []):
            label.destroy()
        home_page._recent_project_labels = []

        if not recent_paths:
            # Show "No recent projects" message
            no_projects_label = ctk.CTkLabel(
                recent_frame,
                text="No recent projects",
                font=ctk.CTkFont(size=14),
                anchor="w",
                text_color="gray"
            )
            no_projects_label.grid(row=1, column=0, sticky="ew", pady=10)
            home_page._recent_project_labels.append(no_projects_label)
        else:
            # Display each recent project
            for i, project_path in enumerate(recent_paths):
                project_name = Path(project_path).name
                project_label = ctk.CTkLabel(
                    recent_frame,
                    text=f"• {project_name}",
                    font=ctk.CTkFont(size=14),
                    anchor="w",
                    cursor="hand2"
                )
                project_label.grid(row=i + 1, column=0, sticky="ew", pady=2)
                home_page._recent_project_labels.append(project_label)

    # ------------------------------------------------------------------
    # Public API for future UI modules
    # ------------------------------------------------------------------

    def get_header_frame(self) -> ctk.CTkFrame:
        """Get the header frame container.

        Returns:
            The header frame for adding header UI components.
        """
        return self.header

    def get_sidebar_container(self) -> ctk.CTkFrame:
        """Get the sidebar container.

        Returns:
            The sidebar container for adding navigation UI.
        """
        return self.sidebar

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
        return self.status_bar

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