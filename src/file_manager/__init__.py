"""File Manager package initialization.

This package contains the file management functionality for the application.
The public API is exposed via ``src.file_manager.file_manager.FileManager``.
"""

from .file_manager import FileManager

__all__ = ["FileManager"]