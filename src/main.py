"""Entry point for the AI Kids Studio Pro application.

This module is intentionally lightweight – it simply imports the
``run`` function from :mod:`src.app` (which will be added later) and
executes it. The goal is to keep the top‑level package free of side
effects so that importing :mod:`src` does not start the UI or perform
network calls.
"""

from __future__ import annotations

def main() -> None:  # pragma: no cover - trivial wrapper
    """Run the application.

    The actual application logic lives in :mod:`src.app`. Importing it
    lazily keeps the import graph shallow and avoids circular
    dependencies.
    """

    from .app import run  # local import to avoid heavy imports at module load

    run()


if __name__ == "__main__":  # pragma: no cover - standard guard
    main()
