"""Application configuration handling.

Loads defaults and optional ``config.yaml`` from the project root.
"""

from __future__ import annotations

import yaml
from pathlib import Path
from typing import Any, Dict


class Config:
    DEFAULTS: Dict[str, Any] = {
        "log": {"level": "INFO", "file": "logs/app.log"},
        "paths": {
            "root": str(Path.cwd()),
            "assets": "assets",
            "fonts": "assets/fonts",
            "icons": "assets/icons",
        },
    }

    def __init__(self, path: str | Path | None = None) -> None:
        self._path = Path(path) if path else Path.cwd() / "config.yaml"
        self.data: Dict[str, Any] = self.DEFAULTS.copy()
        self._load()

    def _load(self) -> None:
        if self._path.is_file():
            with self._path.open("r", encoding="utf-8") as f:
                loaded = yaml.safe_load(f) or {}
                self._deep_update(self.data, loaded)

    @staticmethod
    def _deep_update(target: Dict[str, Any], src: Dict[str, Any]) -> None:
        for k, v in src.items():
            if isinstance(v, dict) and isinstance(target.get(k), dict):
                Config._deep_update(target[k], v)
            else:
                target[k] = v

    def get(self, *keys: str, default: Any = None) -> Any:
        node: Any = self.data
        for key in keys:
            if not isinstance(node, dict) or key not in node:
                return default
            node = node[key]
        return node
