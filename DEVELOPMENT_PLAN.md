# Development Plan

The project will be built in **phases**. Each phase delivers a functional slice of the system and includes design, implementation, testing, and documentation.

## Phase 0 – Architecture & Planning (Current)
* Produce all design documents (this set).
* Define folder structure and coding standards.

## Phase 1 – Project Scaffold
* Initialise repository, CI pipeline, and basic package layout.
* Implement `main.py` that launches an empty window.
* Add logging and configuration systems.

## Phase 2 – Theme & UI Foundations
* Implement ThemeManager, global style definitions.
* Build core UI skeleton: MainWindow, Sidebar, TopBar, StatusBar.

## Phase 3 – Project Management
* Implement ProjectManager, autosave, and project wizard UI.
* Persist projects in SQLite.

## Phase 4 – AI Engine Framework
* Define `AIEngine` abstract base class.
* Implement PromptEngine and a mock ScriptEngine.

## Phase 5 – Media Generation Engines
* ImageEngine, VoiceEngine, VideoEngine (stub implementations).
* Background worker infrastructure.

## Phase 6 – Export System
* ExportEngine supporting PDF, MP4, and ZIP packages.

## Phase 7 – Plugin System
* Discover and load plugins from `plugins/` directory.

## Phase 8 – Testing & QA
* Unit tests for all layers, integration tests for AI adapters.
* Performance profiling and UI responsiveness tests.

## Phase 9 – Release Preparation
* Build installers (NSIS/pyinstaller).
* Documentation finalisation and version bump.

Each phase ends with a **review checkpoint** where code, docs, and tests are evaluated before moving on.
