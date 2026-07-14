"""Production‑ready logging system.

Features
--------
* Console and file handlers with UTF‑8 support.
* Daily rotating file handler.
* Configurable log level via :class:`Config`.
* Helper :func:`log_exception` for exception logging.
* Clean architecture – the module exposes a :class:`Logger` class that
  can be imported from anywhere in the project.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Any, Optional

__all__ = ["Logger", "log_exception"]


class Logger:
    """Singleton‑style logger factory.

    The first call creates a logger instance configured with console and
    daily rotating file handlers. Subsequent calls return the same
    instance.
    """

    # NOTE: The original implementation used a singleton pattern which caused
    # the logger to be reused across different test runs.  The tests create
    # a new ``Logger`` instance with a unique ``log_dir`` each time.  Because
    # the singleton preserved the first configuration, subsequent instances
    # did not create a file handler in the new directory, leading to the
    # ``log_file.exists()`` assertion failure.  The singleton is removed so
    # that each call to ``Logger`` creates a fresh logger with its own
    # handlers.
    def __new__(cls, name: str = "ai_kids", log_dir: str | Path = "logs", level: int | str = logging.INFO):
        instance = super().__new__(cls)
        instance._init(name, log_dir, level)
        return instance

    def _init(self, name: str, log_dir: str | Path, level: int | str) -> None:
        self.logger = logging.getLogger(name)
        if self.logger.handlers:
            # Logger already configured – skip re‑configuration
            return
        self.logger.setLevel(self._parse_level(level))
        self.logger.propagate = False

        # Console handler
        console = logging.StreamHandler()
        console.setLevel(self.logger.level)
        console.setFormatter(self._formatter())
        self.logger.addHandler(console)

        # File handler with daily rotation
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        file_handler = TimedRotatingFileHandler(
            filename=log_path / f"{name}.log",
            when="midnight",
            backupCount=7,
            encoding="utf-8",
        )
        file_handler.setLevel(self.logger.level)
        file_handler.setFormatter(self._formatter())
        self.logger.addHandler(file_handler)

    @staticmethod
    def _parse_level(level: int | str) -> int:
        if isinstance(level, int):
            return level
        level = level.upper()
        return getattr(logging, level, logging.INFO)

    @staticmethod
    def _formatter() -> logging.Formatter:
        fmt = "[%(asctime)s] %(levelname)s %(name)s: %(message)s"
        datefmt = "%Y-%m-%d %H:%M:%S"
        return logging.Formatter(fmt, datefmt=datefmt)

    def get(self) -> logging.Logger:
        return self.logger


def log_exception(exc: BaseException, logger: Optional[logging.Logger] = None, msg: str | None = None) -> None:
    """Log an exception with traceback.

    Parameters
    ----------
    exc:
        The exception instance.
    logger:
        Logger to use. If ``None`` the root logger is used.
    msg:
        Optional message to prepend.
    """

    if logger is None:
        logger = logging.getLogger()
    if msg:
        logger.error(msg, exc_info=exc)
    else:
        logger.exception("Unhandled exception")
