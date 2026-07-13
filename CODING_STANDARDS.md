# Coding Standards

## General

* **Python 3.12+** – use modern language features where appropriate.
* Follow **PEP 8** style; enforce with **Black** (`line-length = 88`).
* Type hints for all public functions, methods, and class attributes.
* Run **flake8**, **mypy**, and **isort** in CI.

## Naming Conventions

| Element | Style |
|---------|-------|
| Packages / Modules | `snake_case` |
| Classes | `PascalCase` |
| Functions / Methods | `snake_case` |
| Constants | `UPPER_SNAKE_CASE` |
| Variables | `snake_case` |

## Imports

```python
import os
import sys

import requests
from customtkinter import CTkButton

from src.utils.file_utils import read_json
```

* Group imports: standard library, third‑party, local.
* Use absolute imports within the `src` package.

## Documentation

* Docstrings in **Google style** for all public callables.
* Module docstring at top of each file describing purpose.
* Keep documentation up‑to‑date with code changes.

## Formatting

* Run `black .` before committing.
* Use `isort` for import ordering.

## Testing

* Tests live in `src/tests/` and use **pytest**.
* Name test files `test_*.py` and test functions `test_*`.
* Aim for ≥ 80 % coverage.

## Commit Messages

Follow **Conventional Commits**:

```
feat(scope): description
fix(scope): description
docs(scope): description
```
