"""Minimal application entry point.

This module provides a :func:`run` function that can be called from
``src/main.py``. It currently just prints a message so that the
application can be executed without errors.
"""

from __future__ import annotations

def run() -> None:  # pragma: no cover - trivial
    """Run the application.

    In a full implementation this would start the UI and load
    configuration. For now it simply indicates that the application
    has started.
    """

    print("AI Kids Studio Pro application started.")
