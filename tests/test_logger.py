"""Simple tests for the :mod:`src.logging.logger` module."""

import logging
import os
import shutil
import sys
from pathlib import Path

import pytest

from src.logging.logger import Logger, log_exception


def test_logger_creates_handlers(tmp_path: Path) -> None:
    log_dir = tmp_path / "logs"
    logger = Logger(name="test", log_dir=log_dir, level="DEBUG")
    log = logger.get()
    assert log.handlers, "Logger should have at least one handler"
    # Ensure file handler exists
    file_handler = next((h for h in log.handlers if isinstance(h, logging.handlers.TimedRotatingFileHandler)), None)
    assert file_handler is not None
    assert log_dir.exists()


def test_log_exception(tmp_path: Path) -> None:
    log_dir = tmp_path / "logs"
    logger = Logger(name="exc_test", log_dir=log_dir, level="ERROR")
    log = logger.get()
    try:
        raise ValueError("test error")
    except Exception as e:
        log_exception(e, logger=log, msg="Caught error")
    # Check that the log file contains the message
    log_file = log_dir / "exc_test.log"
    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "Caught error" in content
    assert "ValueError" in content
