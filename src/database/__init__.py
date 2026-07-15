"""Database package initialization.

This package contains the production-ready SQLite database layer used by
the application. The public API is exposed via
``src.database.database_manager.DatabaseManager``.
"""

from .database_manager import DatabaseManager

__all__ = ["DatabaseManager"]