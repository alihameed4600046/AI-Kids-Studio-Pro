"""Tests for the Theme Manager.

The tests exercise the public API and verify that settings are
persisted via the :class:`SettingsManager`.
"""

import json
import os
from pathlib import Path

from src.theme.theme_manager import ThemeManager
from src.theme.theme_models import ThemeSettings


def test_theme_manager_roundtrip(tmp_path):
    # Use a temporary config file
    config_file = tmp_path / "theme.json"
    manager = ThemeManager(config_file)

    # Default settings should be loaded
    default = manager.get_settings()
    assert isinstance(default, ThemeSettings)
    assert default.mode == "system"

    # Update a few values
    manager.update(mode="dark", accent_color="#ff0000", scale=120)
    updated = manager.get_settings()
    assert updated.mode == "dark"
    assert updated.accent_color == "#ff0000"
    assert updated.scale == 120

    # Verify persistence
    with config_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["theme"] == updated.to_dict()
