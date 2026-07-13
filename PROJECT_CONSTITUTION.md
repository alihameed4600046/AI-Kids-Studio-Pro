# Project Constitution

## Project Vision

Create a professional, AI‑powered content studio for children that runs as a native Windows desktop application. The tool should empower kids to generate scripts, images, voices, and videos safely and intuitively, fostering creativity and learning.

## Long‑term Goals

* Provide a stable, extensible platform for AI‑driven media creation.
* Support multiple AI providers and models without code changes.
* Enable community‑driven plugins and content packs.
* Maintain high standards of security, privacy, and performance.

## Architecture Rules

* Strict separation of concerns via MVC layers.
* Each module must have a single responsibility.
* No circular dependencies.
* All external interactions (AI services, file I/O) go through well‑defined interfaces.

## Coding Standards

* Follow **PEP 8** with Black formatting.
* Type hints for all public functions and methods.
* Use `flake8` and `mypy` in CI.

## Naming Rules

* Modules: `snake_case.py`
* Classes: `PascalCase`
* Functions/Methods: `snake_case`
* Constants: `UPPER_SNAKE_CASE`

## Folder Rules

```
src/
│   main.py
│   config.py
│
├─controllers/
├─models/
├─views/
├─services/
├─ai/
├─utils/
└─plugins/
```

## Module Rules

* One public class or a cohesive set of functions per module.
* Keep module size < 500 lines.

## Import Rules

* Absolute imports within the `src` package.
* Group imports: standard library, third‑party, local.

## Error Handling Rules

* Use custom exception hierarchy defined in `src/errors.py`.
* Log errors with stack trace; surface user‑friendly messages via UI.

## Logging Rules

* Central logger configured in `src/logging_config.py`.
* Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL.

## Git Rules

* Feature branches per task.
* Pull requests require review and pass CI.
* Commit messages follow **Conventional Commits**.

## Versioning Rules

* Semantic Versioning 2.0.0.

## Testing Rules

* Unit tests with `pytest` covering ≥ 80 % of code.
* Integration tests for AI service adapters.

## Documentation Rules

* Docstrings in Google style.
* Project‑level docs in Markdown.

## UI Rules

* Consistent spacing, fonts, and colors defined in the theme system.
* Accessibility: high contrast, keyboard navigation.

## Theme Rules

* Light and dark themes, switchable at runtime.
* All colors referenced via the theme manager.

## Performance Rules

* UI must remain responsive; long AI calls run in background threads.
* Cache AI results where appropriate.

## Security Rules

* No hard‑coded API keys; use encrypted config store.
* Validate all user inputs.

## AI Integration Rules

* Abstract AI providers behind interfaces.
* Allow swapping models without code changes.

## Future Expansion Rules

* Plugin system for third‑party extensions.
* Modular export pipelines.

## Recovery Rules

* Auto‑save project state every few seconds.
* Graceful recovery from crashes using persisted state.

## Backup Rules

* Optional cloud backup via encrypted zip files.

## Refactoring Rules

* Refactor when cyclomatic complexity > 10 or duplicate code detected.

## No Duplicate Code Rules

* Use shared utilities; run static analysis to detect duplicates.

## File Size Limits

* ≤ 500 lines per Python file.

## Module Size Limits

* ≤ 5 classes or 10 functions per module.

## Maximum Function Length

* ≤ 30 lines of code.

## Maximum Class Length

* ≤ 300 lines.

## Comment Standards

* Inline comments only when the code is not self‑explanatory.

## Docstring Standards

* Google style docstrings for all public callables.

## Formatting Standards

* Black with line length 88.

## Commit Standards

* Conventional Commits format.
