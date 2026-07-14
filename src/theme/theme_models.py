"""Data models for theme settings.

The :class:`ThemeSettings` dataclass holds all configurable values for
the application theme.  It is intentionally simple so that it can be
serialised to JSON by the :class:`~src.settings.manager.SettingsManager`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


ThemeMode = Literal["light", "dark", "system"]


@dataclass
class ThemeSettings:
    """Container for theme configuration.

    Attributes
    ----------
    mode:
        One of ``"light"``, ``"dark"`` or ``"system"``.
    accent_color:
        Hex colour string (e.g. ``"#ff0000"``).
    scale:
        UI scaling percentage (80–150).
    font_family:
        Name of the font family.
    font_size:
        Base font size in points.
    widget_radius:
        Corner radius for widgets in pixels.
    padding:
        Default padding in pixels.
    """

    mode: ThemeMode = "system"
    accent_color: str = "#0066ff"
    scale: int = 100
    font_family: str = "Arial"
    font_size: int = 12
    widget_radius: int = 4
    padding: int = 8

    def to_dict(self) -> dict:
        """Return a serialisable dictionary representation."""
        return {
            "mode": self.mode,
            "accent_color": self.accent_color,
            "scale": self.scale,
            "font_family": self.font_family,
            "font_size": self.font_size,
            "widget_radius": self.widget_radius,
            "padding": self.padding,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ThemeSettings":
        """Create an instance from a dictionary.

        Missing keys are filled with the default values.
        """
        return cls(
            mode=data.get("mode", "system"),
            accent_color=data.get("accent_color", "#0066ff"),
            scale=data.get("scale", 100),
            font_family=data.get("font_family", "Arial"),
            font_size=data.get("font_size", 12),
            widget_radius=data.get("widget_radius", 4),
            padding=data.get("padding", 8),
        )