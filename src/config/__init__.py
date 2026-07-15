"""Compatibility shim for the legacy ``src.config`` import path.

The original project placed the configuration module at the project root
(``config/config.py``).  Some modules and tests import it via
``src.config.config``.  To keep backward compatibility without moving
files, this package re-exports :class:`~config.config.Config`.
"""

import sys
from pathlib import Path

# Add the project root to sys.path to import config.config
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from config.config import Config  # noqa: F401

__all__ = ["Config"]
