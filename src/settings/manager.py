"""Production‑ready settings manager.

Features
--------
* JSON configuration file with UTF‑8 support.
* Automatic creation of a default configuration if none exists.
* Read/write helpers with validation.
* Backup of the existing file before overwriting.
* Type‑hinted API and comprehensive docstrings.
"""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any, Dict, Optional

__all__ = ["SettingsManager"]


class SettingsManager:
    """Singleton‑style JSON settings manager.

    Parameters
    ----------
    config_path:
        Path to the JSON configuration file. If the file does not exist a
        default configuration is written.
    default_config:
        Dictionary representing the default configuration.
    """

    _instance: Optional["SettingsManager"] = None

    def __new__(cls, config_path: str | Path, default_config: Dict[str, Any] | None = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init(config_path, default_config or {})
        return cls._instance

    def _init(self, config_path: str | Path, default_config: Dict[str, Any]):
        self.config_path = Path(config_path).expanduser().resolve()
        self.default_config = default_config
        self._ensure_config_exists()
        self._load()

    def _ensure_config_exists(self) -> None:
        if not self.config_path.exists():
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            self._write(self.default_config)

    def _load(self) -> None:
        try:
            with self.config_path.open("r", encoding="utf-8") as f:
                self._data: Dict[str, Any] = json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in {self.config_path}: {exc}") from exc

    def _write(self, data: Dict[str, Any]) -> None:
        # Backup existing file
        if self.config_path.exists():
            backup = self.config_path.with_suffix(".bak")
            shutil.copy2(self.config_path, backup)
        with self.config_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, sort_keys=True)
        self._data = data

    # Public API -----------------------------------------------------
    def get(self, key: str, default: Any | None = None) -> Any:
        """Return the value for *key* or *default* if missing."""
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set *key* to *value* and persist the configuration."""
        self._data[key] = value
        self._write(self._data)

    def delete(self, key: str) -> None:
        """Delete *key* from the configuration if it exists."""
        if key in self._data:
            del self._data[key]
            self._write(self._data)

    def validate(self, schema: Dict[str, type]) -> bool:
        """Validate the current configuration against *schema*.

        The *schema* maps keys to expected types. Returns ``True`` if all
        keys present in the schema match their expected type, otherwise
        ``False``.
        """
        for k, expected_type in schema.items():
            if k in self._data and not isinstance(self._data[k], expected_type):
                return False
        return True
