"""Application bootstrap module.

This module provides centralized initialization for the AI Kids Studio Pro
application. It handles the startup sequence, initializes all core managers,
and provides a clean entry point for the application.

The bootstrap follows a specific initialization order:
1. Configuration loading
2. Logging initialization
3. Settings Manager
4. Theme Manager
5. Database Manager
6. Project Manager
7. File Manager
8. Model Manager (with OpenRouter provider)

This order ensures that dependencies are available when needed (e.g., logging
is available for all subsequent initializations, database is ready before
Project Manager, etc.).
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Optional

from config.config import Config
from src.engine.model_manager import ModelManager, ProviderConfig, ProviderType, TaskType
from src.engine.mock_engine import MockEngine
from src.engine.openrouter_engine import OpenRouterEngine
from src.logging.logger import get_logger
from src.logging_config import configure_logging
from src.services.generation_repository import GenerationRepository
from src.services.generation_service import GenerationService
from src.settings.manager import SettingsManager
from src.theme.theme_manager import ThemeManager
from src.database.database_manager import DatabaseManager
from src.file_manager.file_manager import FileManager
from src.project.project_manager import ProjectManager

__all__ = ["ApplicationBootstrap", "bootstrap"]


class BootstrapError(Exception):
    """Exception raised during application bootstrap."""

    pass


class ApplicationBootstrap:
    """Centralized application bootstrap manager.

    This class orchestrates the initialization of all core application
    components in the correct order, handles errors gracefully, and provides
    access to initialized managers.

    Attributes:
        config: Application configuration.
        logger: Application logger.
        settings_manager: Settings manager instance.
        theme_manager: Theme manager instance.
        database_manager: Database manager instance.
        project_manager: Project manager instance.
        file_manager: File manager instance.
        model_manager: Model manager with registered AI providers.
        generation_service: Generation service wired with the model manager.
    """

    def __init__(self, config_path: Optional[str | Path] = None) -> None:
        """Initialize the bootstrap manager.

        Args:
            config_path: Optional path to configuration file. If None, uses
                default configuration locations.
        """
        self._config_path = config_path
        self._config: Optional[Config] = None
        self._logger: Optional[logging.Logger] = None
        self._settings_manager: Optional[SettingsManager] = None
        self._theme_manager: Optional[ThemeManager] = None
        self._database_manager: Optional[DatabaseManager] = None
        self._project_manager: Optional[ProjectManager] = None
        self._file_manager: Optional[FileManager] = None
        self._model_manager: Optional[ModelManager] = None
        self._generation_service: Optional[GenerationService] = None
        self._initialized = False

    # ------------------------------------------------------------------
    # Properties for accessing initialized components
    # ------------------------------------------------------------------
    @property
    def config(self) -> Config:
        """Get the application configuration."""
        if self._config is None:
            raise BootstrapError("Configuration not initialized. Call initialize() first.")
        return self._config

    @property
    def logger(self) -> logging.Logger:
        """Get the application logger."""
        if self._logger is None:
            raise BootstrapError("Logger not initialized. Call initialize() first.")
        return self._logger

    @property
    def settings_manager(self) -> SettingsManager:
        """Get the settings manager."""
        if self._settings_manager is None:
            raise BootstrapError("Settings manager not initialized. Call initialize() first.")
        return self._settings_manager

    @property
    def theme_manager(self) -> ThemeManager:
        """Get the theme manager."""
        if self._theme_manager is None:
            raise BootstrapError("Theme manager not initialized. Call initialize() first.")
        return self._theme_manager

    @property
    def database_manager(self) -> DatabaseManager:
        """Get the database manager."""
        if self._database_manager is None:
            raise BootstrapError("Database manager not initialized. Call initialize() first.")
        return self._database_manager

    @property
    def project_manager(self) -> ProjectManager:
        """Get the project manager."""
        if self._project_manager is None:
            raise BootstrapError("Project manager not initialized. Call initialize() first.")
        return self._project_manager

    @property
    def file_manager(self) -> FileManager:
        """Get the file manager."""
        if self._file_manager is None:
            raise BootstrapError("File manager not initialized. Call initialize() first.")
        return self._file_manager

    @property
    def model_manager(self) -> ModelManager:
        """Get the model manager with registered AI providers."""
        if self._model_manager is None:
            raise BootstrapError("Model manager not initialized. Call initialize() first.")
        return self._model_manager

    @property
    def generation_service(self) -> GenerationService:
        """Get the generation service wired with the model manager."""
        if self._generation_service is None:
            raise BootstrapError("Generation service not initialized. Call initialize() first.")
        return self._generation_service

    @property
    def is_initialized(self) -> bool:
        """Check if bootstrap has been completed."""
        return self._initialized

    # ------------------------------------------------------------------
    # Initialization methods
    # ------------------------------------------------------------------
    def initialize(self) -> None:
        """Run the complete bootstrap sequence.

        This method initializes all components in the correct order.
        If any step fails, it logs the error and raises BootstrapError.

        Raises:
            BootstrapError: If any initialization step fails.
        """
        if self._initialized:
            self.logger.warning("Bootstrap already initialized, skipping re-initialization")
            return

        try:
            self._initialize_config()
            self._initialize_logging()
            self._initialize_settings_manager()
            self._initialize_theme_manager()
            self._initialize_database_manager()
            self._initialize_project_manager()
            self._initialize_file_manager()
            self._initialize_model_manager()

            self._initialized = True
            self.logger.info("Application bootstrap completed successfully")

        except Exception as exc:
            # Use basic logging if logger not yet initialized
            if self._logger:
                self._logger.exception("Bootstrap failed: %s", exc)
            else:
                logging.basicConfig(level=logging.ERROR)
                logging.getLogger(__name__).exception("Bootstrap failed: %s", exc)
            raise BootstrapError(f"Application bootstrap failed: {exc}") from exc

    def _initialize_config(self) -> None:
        """Load application configuration."""
        self._config = Config(self._config_path)
        # Use basic logging for this early stage
        logging.basicConfig(level=logging.INFO)
        logging.getLogger(__name__).info("Configuration loaded from %s", self._config_path or "defaults")

    def _initialize_logging(self) -> None:
        """Configure application logging."""
        log_level = self._config.get("log", "level", default="INFO")
        log_file = self._config.get("log", "file", default="logs/app.log")

        # Ensure log directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # Configure logging with the specified level
        level = getattr(logging, log_level.upper(), logging.INFO)
        configure_logging(level=level)

        self._logger = get_logger("bootstrap")
        self._logger.info("Logging initialized (level=%s, file=%s)", log_level, log_file)

    def _initialize_settings_manager(self) -> None:
        """Initialize the settings manager."""
        settings_path = self._config.get("paths", "settings", default="config/settings.json")
        settings_path = Path(settings_path)
        settings_path.parent.mkdir(parents=True, exist_ok=True)

        default_settings = {
            "theme": {},
            "window": {"width": 1200, "height": 800},
            "recent_projects": [],
            "openrouter_model": OpenRouterEngine.DEFAULT_MODEL,
            "openrouter_base_url": OpenRouterEngine.DEFAULT_BASE_URL,
        }

        self._settings_manager = SettingsManager(settings_path, default_settings)
        self._logger.info("Settings manager initialized: %s", settings_path)

    def _initialize_theme_manager(self) -> None:
        """Initialize the theme manager."""
        theme_path = self._config.get("paths", "theme", default="config/theme.json")
        theme_path = Path(theme_path)
        theme_path.parent.mkdir(parents=True, exist_ok=True)

        self._theme_manager = ThemeManager(theme_path)
        self._logger.info("Theme manager initialized: %s", theme_path)

    def _initialize_database_manager(self) -> None:
        """Initialize the database manager."""
        db_path = self._config.get("database", "path", default="db.sqlite3")
        db_path = Path(db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)

        # Create a config file for the database manager if needed
        db_config_path = self._config_path or Path.cwd() / "config.yaml"
        self._database_manager = DatabaseManager(db_config_path)
        self._logger.info("Database manager initialized: %s", db_path)

    def _initialize_project_manager(self) -> None:
        """Initialize the project manager."""
        # Project manager uses the same config path as database manager
        db_config_path = self._config_path or Path.cwd() / "config.yaml"
        self._project_manager = ProjectManager(db_config_path)
        self._logger.info("Project manager initialized")

    def _initialize_file_manager(self) -> None:
        """Initialize the file manager."""
        base_path = self._config.get("paths", "root", default=str(Path.cwd()))
        base_path = Path(base_path)
        base_path.mkdir(parents=True, exist_ok=True)

        self._file_manager = FileManager(base_path)
        self._logger.info("File manager initialized with base path: %s", base_path)

    def _initialize_model_manager(self) -> None:
        """Initialize the model manager with registered AI providers.

        Registers OpenRouter as a text-generation provider using configuration
        from the settings manager. The OpenRouterEngine is created via its
        ``from_settings`` classmethod so that the API key, model, and base URL
        all come from the existing settings/configuration system.

        When the ``AI_KIDS_STUDIO_MOCK`` environment variable is set to ``1``,
        a Mock provider is also registered for local UI smoke testing without
        real API credentials.
        """
        self._model_manager = ModelManager()

        api_key = self._settings_manager.get("openrouter_api_key")
        model = self._settings_manager.get("openrouter_model", OpenRouterEngine.DEFAULT_MODEL)
        base_url = self._settings_manager.get("openrouter_base_url", OpenRouterEngine.DEFAULT_BASE_URL)

        engine = None
        if api_key:
            engine = OpenRouterEngine.from_settings(
                settings_manager=self._settings_manager,
            )

        self._model_manager.register_provider(
            ProviderConfig(
                provider_type=ProviderType.OPENROUTER,
                api_key=api_key,
                base_url=base_url,
                models=[model],
                enabled=bool(api_key),
                priority=1,
                metadata={"supported_tasks": [TaskType.TEXT_GENERATION.value]},
            )
        )
        if engine is not None:
            self._model_manager.register_engine(ProviderType.OPENROUTER, engine)

        if os.environ.get("AI_KIDS_STUDIO_MOCK") == "1":
            mock_engine = MockEngine()
            self._model_manager.register_provider(
                ProviderConfig(
                    provider_type=ProviderType.MOCK,
                    api_key=None,
                    base_url=None,
                    models=["mock-model"],
                    enabled=True,
                    priority=100,
                    metadata={"supported_tasks": [TaskType.TEXT_GENERATION.value]},
                )
            )
            self._model_manager.register_engine(ProviderType.MOCK, mock_engine)
            self._logger.info("Mock provider registered for development")

        repository = GenerationRepository(db_manager=self._database_manager)
        self._generation_service = GenerationService(
            model_manager=self._model_manager,
            repository=repository,
        )
        self._logger.info("Model manager initialized with OpenRouter provider")

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------
    def shutdown(self) -> None:
        """Gracefully shut down all initialized components.

        This method should be called on application exit to ensure
        proper cleanup of resources (database connections, etc.).
        """
        if not self._initialized:
            return

        self.logger.info("Shutting down application...")

        # Close database connection
        if self._database_manager:
            try:
                self._database_manager.close()
                self.logger.debug("Database connection closed")
            except Exception as exc:
                self.logger.exception("Error closing database: %s", exc)

        # Close project manager (which closes its database)
        if self._project_manager:
            try:
                self._project_manager._db.close()
                self.logger.debug("Project manager database closed")
            except Exception as exc:
                self.logger.exception("Error closing project manager: %s", exc)

        # Shutdown AI engines
        if self._model_manager:
            for engine in self._model_manager._engines.values():
                try:
                    asyncio.get_running_loop()
                    self.logger.debug(
                        "Skipping async engine shutdown inside running event loop"
                    )
                    continue
                except RuntimeError:
                    pass
                try:
                    asyncio.run(engine.shutdown())
                except Exception as exc:
                    self.logger.debug("Engine shutdown skipped: %s", exc)

        self._initialized = False
        self.logger.info("Application shutdown complete")


# ----------------------------------------------------------------------
# Module-level convenience function
# ----------------------------------------------------------------------
_bootstrap_instance: Optional[ApplicationBootstrap] = None


def bootstrap(config_path: Optional[str | Path] = None) -> ApplicationBootstrap:
    """Get or create the global bootstrap instance.

    This is a convenience function for getting a singleton bootstrap
    instance. For more control, instantiate ApplicationBootstrap directly.

    Args:
        config_path: Optional path to configuration file.

    Returns:
        The initialized ApplicationBootstrap instance.

    Raises:
        BootstrapError: If initialization fails.
    """
    global _bootstrap_instance

    if _bootstrap_instance is None:
        _bootstrap_instance = ApplicationBootstrap(config_path)
        _bootstrap_instance.initialize()

    return _bootstrap_instance


def shutdown() -> None:
    """Shutdown the global bootstrap instance if it exists."""
    global _bootstrap_instance

    if _bootstrap_instance is not None:
        _bootstrap_instance.shutdown()
        _bootstrap_instance = None