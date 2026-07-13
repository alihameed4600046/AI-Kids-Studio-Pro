# Recommended Folder Structure

```
AI Kids Studio Pro/
│   README.md
│   PROJECT_CONSTITUTION.md
│   ARCHITECTURE.md
│   DEVELOPMENT_PLAN.md
│   FOLDER_STRUCTURE.md
│   CODING_STANDARDS.md
│   UI_GUIDELINES.md
│   ROADMAP.md
│   CHANGELOG.md
│   TODO.md
│   requirements.txt
│   .gitignore
│
└─src/
    │   main.py               # Application entry point
    │   config.py             # Global configuration loader
    │   logging_config.py     # Central logging setup
    │
    ├─controllers/           # MVC Controllers
    │   │   __init__.py
    │   │   dashboard.py
    │   │   project.py
    │   │   ...
    │
    ├─models/                # Data models (SQLModel / Pydantic)
    │   │   __init__.py
    │   │   project.py
    │   │   media.py
    │   │   ...
    │
    ├─views/                 # CustomTkinter UI components
    │   │   __init__.py
    │   │   main_window.py
    │   │   sidebar.py
    │   │   dashboard.py
    │   │   ...
    │
    ├─services/              # Business use‑case services
    │   │   __init__.py
    │   │   project_service.py
    │   │   export_service.py
    │   │   ...
    │
    ├─ai/                    # AI engine implementations
    │   │   __init__.py
    │   │   base_engine.py
    │   │   prompt_engine.py
    │   │   script_engine.py
    │   │   image_engine.py
    │   │   ...
    │
    ├─utils/                 # Helper utilities
    │   │   __init__.py
    │   │   file_utils.py
    │   │   thread_pool.py
    │   │   ...
    │
    ├─plugins/               # Optional third‑party extensions
    │   │   __init__.py
    │   │   sample_plugin.py
    │
    └─tests/                 # Test suite
        │   __init__.py
        │   test_project.py
        │   test_ai_engines.py
        │   ...
```

The structure enforces the separation of concerns defined in the architecture and makes it easy to locate related code.
