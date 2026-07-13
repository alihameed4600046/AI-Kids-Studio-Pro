# Architecture Overview

AI Kids Studio Pro follows a **layered MVC architecture** with clear separation between UI, business logic, AI services, and data persistence.

## Layer Diagram

```
++---------------------------+
|          UI Layer         |
|  (CustomTkinter Views)   |
++------------+--------------+
             |
++------------v--------------+
|      Controller Layer     |
|  (Tkinter event handlers) |
++------------+--------------+
             |
++------------v--------------+
|      Business Layer       |
|  (Use‑case / service)     |
++------------+--------------+
             |
++------------v--------------+
|        AI Layer           |
|  (Model adapters, prompts) |
++------------+--------------+
             |
++------------v--------------+
|     Database Layer        |
|  (SQLite via SQLModel)    |
++------------+--------------+
             |
++------------v--------------+
|        Utilities          |
|  (Logging, config, etc.)  |
++---------------------------+
```

### UI Layer

* **Views** – CustomTkinter widgets organized into reusable components (e.g., `Sidebar`, `TopBar`, `Dashboard`).
* **Theme System** – Centralised theme manager providing colors, fonts, and icons.

### Controller Layer

* Controllers bind UI events to business use‑cases.
* Each view has a corresponding controller class (e.g., `DashboardController`).

### Business Layer

* Implements application use‑cases such as `CreateProject`, `ExportMedia`, `RunAIEngine`.
* Orchestrates calls to the AI Layer and Database Layer.

### AI Layer

* **Prompt Engine**, **Script Engine**, **Image Engine**, **Voice Engine**, **Video Engine**.
* Each engine implements a common `AIEngine` interface allowing interchangeable providers.

### Database Layer

* SQLite database accessed via **SQLModel** (or similar ORM).
* Stores projects, settings, and cached AI results.

### Utilities & Managers

* **SettingsManager** – loads/saves user preferences.
* **ProjectManager** – handles project creation, loading, and autosave.
* **PluginSystem** – discovers and loads plugins at runtime.
* **LoggingSystem**, **ErrorSystem**, **RecoverySystem** – cross‑cutting concerns.

## Component Responsibilities

| Component | Responsibility |
|-----------|------------------|
| `MainWindow` | Initialise UI, bootstrap controllers |
| `Sidebar` | Navigation between major sections |
| `DashboardController` | Coordinate dashboard widgets and data refresh |
| `ProjectManager` | Create, open, save, autosave projects |
| `AIEngine` (abstract) | Define `run(prompt, **kwargs)` contract |
| `PromptEngine` | Build prompts for other engines |
| `ExportEngine` | Convert generated media into user‑selected formats |
| `PluginSystem` | Load external modules that extend functionality |

## Extensibility

* New AI providers can be added by implementing the `AIEngine` interface and registering with the `AIEngineFactory`.
* UI components follow a plug‑in pattern – new panels can be added without modifying core code.
