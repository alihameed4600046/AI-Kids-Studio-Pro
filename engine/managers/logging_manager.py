"""Logging manager – creates a singleton logger.
"""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from config.config import Config


class LoggingManager:
    _logger: Optional[logging.Logger] = None

    def __init__(self, config: Config) -> None:
        if LoggingManager._logger is None:
            self._configure(config)

    @staticmethod
    def _configure(config: Config) -> None:
        cfg = config.get("log", default={})
        level = getattr(logging, cfg.get("level", "INFO").upper(), logging.INFO)
        log_file = Path(cfg.get("file", "logs/app.log"))
        log_file.parent.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger("ai_kids_studio")
        logger.setLevel(level)
        fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(fmt)
        logger.addHandler(ch)

        fh = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
        fh.setFormatter(fmt)
        logger.addHandler(fh)

        LoggingManager._logger = logger

    def get_logger(self) -> logging.Logger:
        if LoggingManager._logger is None:
            raise RuntimeError("LoggingManager not initialised")
        return LoggingManager._logger
