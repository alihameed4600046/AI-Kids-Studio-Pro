"""Project package initialization.

This package contains the project management functionality for the application.
The public API is exposed via ``src.project.project_manager.ProjectManager``.
"""

from .project_manager import ProjectManager

__all__ = ["ProjectManager"]