"""Tests for the :mod:`src.settings.manager` module."""

import json
import os
from pathlib import Path

import pytest

from src.settings.manager import SettingsManager


def test_default_creation(tmp_path: Path) -> None:
    cfg_path = tmp_path / "config.json"
    default = {"foo": 1}
    sm = SettingsManager(cfg_path, default)
    assert cfg_path.exists()
    with cfg_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == default


def test_get_set_delete(tmp_path: Path) -> None:
    cfg_path = tmp_path / "config.json"
    sm = SettingsManager(cfg_path, {})
    sm.set("bar", "baz")
    assert sm.get("bar") == "baz"
    sm.delete("bar")
    assert sm.get("bar") is None


def test_validate(tmp_path: Path) -> None:
    cfg_path = tmp_path / "config.json"
    sm = SettingsManager(cfg_path, {"num": 5})
    assert sm.validate({"num": int})
    assert not sm.validate({"num": str})
