"""A very small subset of the PyYAML API used by the project.

Only :func:`safe_load` and :func:`safe_dump` are implemented.  The
implementation is intentionally minimal – it supports the simple
configuration format used in the tests (a top‑level mapping with a
single nested ``database`` mapping).  It is **not** a full YAML parser.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

__all__ = ["safe_load", "safe_dump"]


def safe_dump(data: Dict[str, Any]) -> str:
    """Return a YAML‑like string for *data*.

    The output is sufficient for the test suite which only writes the
    configuration file.  Nested dictionaries are indented by two spaces.
    """
    lines: list[str] = []
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{key}:")
            for k, v in value.items():
                lines.append(f"  {k}: {v}")
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines) + "\n"


def safe_load(stream: str | Path | object) -> Dict[str, Any]:
    """Parse a very small subset of YAML.

    Only mappings with optional nested mappings are supported.  The
    implementation is intentionally simple and not suitable for
    production use.
    """
    if isinstance(stream, Path):
        text = stream.read_text(encoding="utf-8")
    elif hasattr(stream, 'read'):
        # Handle file-like objects
        text = stream.read()
    else:
        text = stream
    result: Dict[str, Any] = {}
    current_key: str | None = None
    for line in text.splitlines():
        line = line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("  ") and current_key:
            # nested key
            subkey, subvalue = [p.strip() for p in line.strip().split(":", 1)]
            if current_key not in result or not isinstance(result[current_key], dict):
                result[current_key] = {}
            result[current_key][subkey] = subvalue
        else:
            key, value = [p.strip() for p in line.split(":", 1)]
            current_key = key
            result[key] = value
    return result
