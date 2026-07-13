# UI Guidelines

## Design Principles

* **Kid‑friendly** – large touch targets, bright colors, simple language.
* **Consistency** – all panels share spacing, typography, and iconography defined by the Theme system.
* **Accessibility** – high contrast, keyboard navigation, screen‑reader friendly labels.

## Core Components

| Component | Description |
|-----------|-------------|
| MainWindow | Root `CTk` window, holds the navigation and content area. |
| Sidebar | Vertical navigation with icons for Dashboard, Projects, Media, Settings. |
| TopBar | Holds global actions, search, and user profile. |
| Dashboard | Overview of recent projects and quick actions. |
| ProjectWizard | Step‑by‑step dialog for creating a new project. |
| NotificationBar | Transient messages (info, warning, error). |
| ProgressOverlay | Modal overlay showing long‑running AI tasks. |

## Layout & Spacing

* Base spacing unit: **8 px**. Use multiples (8, 16, 24…) for padding/margin.
* Minimum touch target: **48 px** height.

## Typography

* Primary font: **Inter**, 14 pt for body, 18 pt for headings.
* Use bold for headings, regular for body text.

## Colors

Defined in `theme_manager.py`. Example palette:

```json
{
  "primary": "#4A90E2",
  "secondary": "#50E3C2",
  "background": "#F5F5F5",
  "text": "#212121",
  "error": "#D0021B"
}
```

## Icons

All icons are SVGs stored in `assets/icons/` and loaded via the Theme system to allow colour overrides.
