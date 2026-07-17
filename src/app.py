"""Application entry point.

This module provides a :func:`run` function that initializes the application
bootstrap, creates the main window, and starts the main event loop.
"""

from __future__ import annotations

from src.bootstrap import ApplicationBootstrap, bootstrap
from src.views.main_window import MainWindow
from src.logging.logger import get_logger


__all__ = ["run"]


def run(config_path: str | None = None) -> None:
    """Run the application.

    This function initializes the bootstrap, creates the main window,
    and starts the CustomTkinter main event loop.

    Args:
        config_path: Optional path to configuration file.
    """
    logger = get_logger("app")

    try:
        # Initialize bootstrap
        logger.info("Initializing application bootstrap...")
        app_bootstrap = bootstrap(config_path)

        # Create main window
        logger.info("Creating main window...")
        main_window = MainWindow(app_bootstrap)

        # Start main event loop
        logger.info("Starting main event loop...")
        main_window.mainloop()

    except Exception as exc:
        logger.exception("Application failed to start: %s", exc)
        raise
    finally:
        logger.info("Application shutdown complete")