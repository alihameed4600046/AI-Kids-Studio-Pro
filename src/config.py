"""Configuration module for the application.

This file will eventually load configuration from files or environment
variables. For now it provides a simple placeholder that can be
expanded later.
"""

from __future__ import annotations

class Config:
    """Placeholder configuration holder."""

    def __init__(self) -> None:
        self.settings: dict[str, str] = {}

    def load(self) -> None:
        """Load configuration – currently a no‑op."""
        pass
