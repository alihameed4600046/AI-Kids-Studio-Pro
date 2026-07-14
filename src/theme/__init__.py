"""Theme package initialization.

This module exposes the :class:`ThemeManager` and the data models used
by the theme system.  The package is intentionally lightweight – the
implementation lives in :mod:`theme_manager` and the models in
``theme_models``.
"""

from .theme_manager import ThemeManager  # noqa: F401
from .theme_models import ThemeSettings  # noqa: F401

__all__ = ["ThemeManager", "ThemeSettings"]