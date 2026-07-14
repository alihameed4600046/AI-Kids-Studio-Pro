"""Theme Manager implementation.

The :class:`ThemeManager` is a thin wrapper around the existing
``SettingsManager``.  It provides a convenient API for getting and
setting theme related values while keeping the persistence logic
encapsulated.  The manager also logs changes via the project's
``logging`` module.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from ..settings.manager import SettingsManager
from ..logging.logger import get_logger
from .theme_models import ThemeSettings

__all__ = ["ThemeManager"]


class ThemeManager:
    """Singleton‑style manager for application theme settings.

    Parameters
    ----------
    config_path:
        Path to the JSON file that stores theme settings.  If omitted the
        default path ``~/.config/ai_kids_studio/theme.json`` is used.
    """

    _instance: "ThemeManager | None" = None

    def __new__(cls, config_path: str | Path | None = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init(config_path)
        return cls._instance

    def _init(self, config_path: str | Path | None):
        default_path = Path.home() / ".config" / "ai_kids_studio" / "theme.json"
        self._settings = SettingsManager(config_path or default_path, {})
        self._logger = get_logger("theme")
        self._logger.debug("ThemeManager initialised with %s", self._settings.config_path)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def get_settings(self) -> ThemeSettings:
        """Return the current :class:`ThemeSettings` instance.

        The settings are stored under the ``theme`` key in the JSON file.
        If the key is missing a default :class:`ThemeSettings` instance is
        returned.
        """
        data = self._settings.get("theme", {})
        return ThemeSettings.from_dict(data)

    def set_settings(self, settings: ThemeSettings) -> None:
        """Persist *settings* and log the change."""
        self._settings.set("theme", settings.to_dict())
        self._logger.info("Theme updated: %s", settings)

    def update(self, **kwargs: Any) -> None:
        """Update individual theme attributes.

        Parameters are passed as keyword arguments matching the
        :class:`ThemeSettings` fields.
        """
        current = self.get_settings()
        updated_dict: Dict[str, Any] = current.to_dict()
        updated_dict.update(kwargs)
        self.set_settings(ThemeSettings.from_dict(updated_dict))

    # Convenience getters
    def __getattr__(self, name: str) -> Any:
        if name in ThemeSettings.__annotations__:
            return getattr(self.get_settings(), name)
        raise AttributeError(name)
