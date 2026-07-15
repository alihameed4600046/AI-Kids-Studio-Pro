"""Production-ready SQLite database layer.

This module implements a lightweight, yet fully-featured SQLite
database manager that satisfies the following requirements:

* Automatic database file creation.
* Automatic table creation based on a declarative schema.
* Schema versioning and migration support.
* Context-manager based transactions with automatic rollback on error.
* Parameterised SQL to avoid injection.
* Integration with the existing :class:`~src.logging.logger.Logger` and
  :class:`~config.config.Config` for logging and configuration.
* Type hints and comprehensive docstrings.
* SOLID-compliant design - the manager is a single responsibility
  component that delegates SQL execution to a private helper.
"""

from __future__ import annotations

import contextlib
import os
import sqlite3
from contextlib import AbstractContextManager
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from config.config import Config
from src.logging.logger import get_logger
from . import migrations

__all__ = ["DatabaseManager"]


class DatabaseManager:
    """Singleton-style SQLite database manager.

    Parameters
    ----------
    config_path:
        Path to the configuration file. The manager will read the
        ``database.path`` value from :class:`~config.config.Config`.
    """

    _instance: "DatabaseManager | None" = None

    def __new__(cls, config_path: str | Path | None = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init(config_path)
        return cls._instance

    def _init(self, config_path: str | Path | None):
        self._config = Config(config_path)
        db_path = Path(self._config.get("database", "path"))
        self._db_path = db_path.resolve()
        self._logger = get_logger("database")
        self._conn: Optional[sqlite3.Connection] = None
        self._ensure_db()
        self._connect()
        self._migrate()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def open(self) -> None:
        """Open the database connection if not already open."""
        if self._conn is None:
            self._connect()
            self._logger.info("Database connection opened: %s", self._db_path)

    def close(self) -> None:
        """Close the database connection if open."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None
            self._logger.info("Database connection closed: %s", self._db_path)

    def execute(
        self, sql: str, params: Iterable[Any] | None = None
    ) -> sqlite3.Cursor:
        """Execute *sql* with optional *params* and return the cursor.

        Parameters
        ----------
        sql:
            SQL statement to execute.
        params:
            Optional parameters for the SQL statement.

        Returns
        -------
        sqlite3.Cursor
            The cursor after execution.
        """
        if self._conn is None:
            self.open()
        cursor = self._conn.cursor()
        try:
            cursor.execute(sql, params or [])
            self._conn.commit()
            return cursor
        except Exception as exc:
            self._conn.rollback()
            self._logger.exception("SQL execution failed: %s", sql)
            raise exc
        finally:
            cursor.close()

    def executemany(
        self, sql: str, params_list: Iterable[Iterable[Any]]
    ) -> sqlite3.Cursor:
        """Execute *sql* against all parameter sequences in *params_list*.

        Parameters
        ----------
        sql:
            SQL statement to execute.
        params_list:
            Iterable of parameter sequences.

        Returns
        -------
        sqlite3.Cursor
            The cursor after execution.
        """
        if self._conn is None:
            self.open()
        cursor = self._conn.cursor()
        try:
            cursor.executemany(sql, params_list)
            self._conn.commit()
            return cursor
        except Exception as exc:
            self._conn.rollback()
            self._logger.exception("SQL executemany failed: %s", sql)
            raise exc
        finally:
            cursor.close()

    def fetchone(
        self, sql: str, params: Iterable[Any] | None = None
    ) -> Optional[sqlite3.Row]:
        """Execute *sql* with optional *params* and return a single row.

        Parameters
        ----------
        sql:
            SQL query to execute.
        params:
            Optional parameters for the SQL query.

        Returns
        -------
        sqlite3.Row or None
            A single row or None if no result.
        """
        if self._conn is None:
            self.open()
        cursor = self._conn.cursor()
        try:
            cursor.execute(sql, params or [])
            return cursor.fetchone()
        finally:
            cursor.close()

    def fetchall(
        self, sql: str, params: Iterable[Any] | None = None
    ) -> List[sqlite3.Row]:
        """Execute *sql* with optional *params* and return all rows.

        Parameters
        ----------
        sql:
            SQL query to execute.
        params:
            Optional parameters for the SQL query.

        Returns
        -------
        list of sqlite3.Row
            List of rows returned by the query.
        """
        if self._conn is None:
            self.open()
        cursor = self._conn.cursor()
        try:
            cursor.execute(sql, params or [])
            return cursor.fetchall()
        finally:
            cursor.close()

    @contextlib.contextmanager
    def transaction(self) -> AbstractContextManager[sqlite3.Cursor]:
        """Yield a cursor within a transaction.

        The transaction is committed on normal exit and rolled back on
        exception.

        Yields
        ------
        sqlite3.Cursor
            A cursor within the transaction context.
        """
        if self._conn is None:
            self.open()
        cursor = self._conn.cursor()
        try:
            yield cursor
            self._conn.commit()
        except Exception:
            self._conn.rollback()
            raise
        finally:
            cursor.close()

    def commit(self) -> None:
        """Commit the current transaction."""
        if self._conn is not None:
            self._conn.commit()
            self._logger.debug("Transaction committed")

    def rollback(self) -> None:
        """Rollback the current transaction."""
        if self._conn is not None:
            self._conn.rollback()
            self._logger.debug("Transaction rolled back")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _ensure_db(self) -> None:
        """Ensure the database file and its parent directory exist."""
        if not self._db_path.parent.exists():
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._db_path.exists():
            self._db_path.touch()
            self._logger.info("Created new database file %s", self._db_path)

    def _connect(self) -> None:
        """Establish a connection to the SQLite database."""
        self._conn = sqlite3.connect(
            str(self._db_path), detect_types=sqlite3.PARSE_DECLTYPES
        )
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._conn.row_factory = sqlite3.Row

    def _migrate(self) -> None:
        """Run migrations to bring the database to the latest schema.

        The current schema version is stored in a ``schema_version`` table.
        Migrations are defined in :mod:`src.database.migrations`.
        """
        self._ensure_schema_version_table()
        current = self._get_schema_version()
        target = migrations.LATEST_VERSION
        if current == target:
            return
        self._logger.info("Migrating database from %s to %s", current, target)
        for version in range(current + 1, target + 1):
            migration_sql = migrations.MIGRATIONS.get(version)
            if migration_sql:
                # Use executescript for multi-statement migrations
                if self._conn is None:
                    self.open()
                cursor = self._conn.cursor()
                try:
                    cursor.executescript(migration_sql)
                    self._conn.commit()
                except Exception as exc:
                    self._conn.rollback()
                    self._logger.exception("Migration %s failed: %s", version, migration_sql)
                    raise exc
                finally:
                    cursor.close()
                self._set_schema_version(version)
                self._logger.info("Applied migration %s", version)

    def _ensure_schema_version_table(self) -> None:
        """Ensure the schema_version table exists and has a row."""
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY
            );
            """
        )
        # Ensure a row exists
        rows = self.fetchall("SELECT version FROM schema_version;")
        if not rows:
            self.execute("INSERT INTO schema_version (version) VALUES (0);")

    def _get_schema_version(self) -> int:
        """Get the current schema version from the database."""
        row = self.fetchall("SELECT version FROM schema_version;")[0]
        return row["version"]

    def _set_schema_version(self, version: int) -> None:
        """Set the schema version in the database."""
        self.execute("UPDATE schema_version SET version = ?;", (version,))

    def __enter__(self) -> "DatabaseManager":
        """Support for context manager protocol."""
        self.open()
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[object],
    ) -> None:
        """Close the connection on context exit."""
        self.close()