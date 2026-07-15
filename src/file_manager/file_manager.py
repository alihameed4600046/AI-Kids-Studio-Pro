"""File Manager implementation.

The :class:`FileManager` provides a high-level API for file and directory
operations within the application. It uses :mod:`pathlib` for cross-platform
path handling and integrates with the project's logging system.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from src.logging.logger import get_logger

__all__ = ["FileManager"]


class FileManager:
    """Manager for file and directory operations.

    Parameters
    ----------
    base_path:
        Base directory for all operations. If None, uses the current working directory.
    logger_name:
        Name for the logger instance.
    """

    def __init__(
        self,
        base_path: Union[str, Path, None] = None,
        logger_name: str = "file_manager",
    ):
        self._base_path = Path(base_path).resolve() if base_path else Path.cwd()
        self._logger = get_logger(logger_name)
        self._logger.debug("FileManager initialised with base path: %s", self._base_path)

    # ------------------------------------------------------------------
    # Project structure creation
    # ------------------------------------------------------------------
    def create_project_structure(self, project_name: str) -> Path:
        """Create the standard directory structure for a new project.

        Parameters
        ----------
        project_name:
            Name of the project (used as the root directory name).

        Returns
        -------
        Path
            Path to the created project root directory.

        Raises
        ------
        ValueError
            If project_name is empty or contains invalid characters.
        FileExistsError
            If the project directory already exists.
        """
        if not project_name or not project_name.strip():
            raise ValueError("Project name cannot be empty")

        sanitized_name = self.sanitize_filename(project_name)
        project_root = self._base_path / sanitized_name

        if project_root.exists():
            raise FileExistsError(f"Project directory already exists: {project_root}")

        # Standard project directories
        directories = [
            "images",
            "videos",
            "audio",
            "scripts",
            "prompts",
            "exports",
            "temp",
            "logs",
            "assets",
        ]

        for dir_name in directories:
            dir_path = project_root / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            self._logger.debug("Created directory: %s", dir_path)

        self._logger.info("Created project structure for '%s' at %s", project_name, project_root)
        return project_root

    # ------------------------------------------------------------------
    # Directory operations
    # ------------------------------------------------------------------
    def create_directory(self, path: Union[str, Path], parents: bool = True, exist_ok: bool = False) -> Path:
        """Create a directory.

        Parameters
        ----------
        path:
            Directory path (relative to base_path or absolute).
        parents:
            Create parent directories if needed.
        exist_ok:
            Do not raise error if directory already exists.

        Returns
        -------
        Path
            Path to the created directory.

        Raises
        ------
        FileExistsError
            If directory exists and exist_ok is False.
        ValueError
            If path is invalid or attempts directory traversal.
        """
        resolved_path = self._resolve_path(path)
        self._validate_path(resolved_path)

        if resolved_path.exists() and not exist_ok:
            raise FileExistsError(f"Directory already exists: {resolved_path}")

        resolved_path.mkdir(parents=parents, exist_ok=exist_ok)
        self._logger.info("Created directory: %s", resolved_path)
        return resolved_path

    def delete_directory(self, path: Union[str, Path], recursive: bool = False) -> bool:
        """Delete a directory.

        Parameters
        ----------
        path:
            Directory path (relative to base_path or absolute).
        recursive:
            If True, delete non-empty directories.

        Returns
        -------
        bool
            True if directory was deleted, False if it didn't exist.

        Raises
        ------
        ValueError
            If path is invalid or attempts directory traversal.
        OSError
            If directory is not empty and recursive is False.
        """
        resolved_path = self._resolve_path(path)
        self._validate_path(resolved_path)

        if not resolved_path.exists():
            self._logger.warning("Directory not found for deletion: %s", resolved_path)
            return False

        if not resolved_path.is_dir():
            raise ValueError(f"Path is not a directory: {resolved_path}")

        if recursive:
            shutil.rmtree(resolved_path)
        else:
            resolved_path.rmdir()  # Only works on empty directories

        self._logger.info("Deleted directory: %s", resolved_path)
        return True

    def directory_exists(self, path: Union[str, Path]) -> bool:
        """Check if a directory exists.

        Parameters
        ----------
        path:
            Directory path (relative to base_path or absolute).

        Returns
        -------
        bool
            True if directory exists, False otherwise.
        """
        resolved_path = self._resolve_path(path)
        return resolved_path.exists() and resolved_path.is_dir()

    def list_directories(self, path: Union[str, Path] = ".", pattern: str = "*") -> List[Path]:
        """List directories in a given path.

        Parameters
        ----------
        path:
            Directory to list (relative to base_path or absolute).
        pattern:
            Glob pattern to filter directories.

        Returns
        -------
        list of Path
            List of directory paths.
        """
        resolved_path = self._resolve_path(path)
        self._validate_path(resolved_path)

        if not resolved_path.exists():
            return []

        dirs = [p for p in resolved_path.glob(pattern) if p.is_dir()]
        self._logger.debug("Listed %d directories in %s", len(dirs), resolved_path)
        return dirs

    def ensure_directory(self, path: Union[str, Path]) -> Path:
        """Ensure a directory exists, creating it if necessary.

        Parameters
        ----------
        path:
            Directory path (relative to base_path or absolute).

        Returns
        -------
        Path
            Path to the directory.
        """
        resolved_path = self._resolve_path(path)
        self._validate_path(resolved_path)

        if not resolved_path.exists():
            resolved_path.mkdir(parents=True, exist_ok=True)
            self._logger.info("Ensured directory exists: %s", resolved_path)
        elif not resolved_path.is_dir():
            raise ValueError(f"Path exists but is not a directory: {resolved_path}")

        return resolved_path

    # ------------------------------------------------------------------
    # File operations
    # ------------------------------------------------------------------
    def create_file(self, path: Union[str, Path], content: str = "", overwrite: bool = False) -> Path:
        """Create a file with optional content.

        Parameters
        ----------
        path:
            File path (relative to base_path or absolute).
        content:
            Initial content to write.
        overwrite:
            If True, overwrite existing file.

        Returns
        -------
        Path
            Path to the created file.

        Raises
        ------
        FileExistsError
            If file exists and overwrite is False.
        ValueError
            If path is invalid or attempts directory traversal.
        """
        resolved_path = self._resolve_path(path)
        self._validate_path(resolved_path)

        if resolved_path.exists() and not overwrite:
            raise FileExistsError(f"File already exists: {resolved_path}")

        # Ensure parent directory exists
        resolved_path.parent.mkdir(parents=True, exist_ok=True)

        resolved_path.write_text(content, encoding="utf-8")
        self._logger.info("Created file: %s", resolved_path)
        return resolved_path

    def delete_file(self, path: Union[str, Path]) -> bool:
        """Delete a file.

        Parameters
        ----------
        path:
            File path (relative to base_path or absolute).

        Returns
        -------
        bool
            True if file was deleted, False if it didn't exist.

        Raises
        ------
        ValueError
            If path is invalid or attempts directory traversal.
        """
        resolved_path = self._resolve_path(path)
        self._validate_path(resolved_path)

        if not resolved_path.exists():
            self._logger.warning("File not found for deletion: %s", resolved_path)
            return False

        if not resolved_path.is_file():
            raise ValueError(f"Path is not a file: {resolved_path}")

        resolved_path.unlink()
        self._logger.info("Deleted file: %s", resolved_path)
        return True

    def copy_file(
        self,
        src: Union[str, Path],
        dst: Union[str, Path],
        overwrite: bool = False,
    ) -> Path:
        """Copy a file.

        Parameters
        ----------
        src:
            Source file path.
        dst:
            Destination file path.
        overwrite:
            If True, overwrite existing destination file.

        Returns
        -------
        Path
            Path to the copied file.

        Raises
        ------
        FileNotFoundError
            If source file doesn't exist.
        FileExistsError
            If destination exists and overwrite is False.
        ValueError
            If paths are invalid or attempt directory traversal.
        """
        src_path = self._resolve_path(src)
        dst_path = self._resolve_path(dst)
        self._validate_path(src_path)
        self._validate_path(dst_path)

        if not src_path.exists():
            raise FileNotFoundError(f"Source file not found: {src_path}")

        if not src_path.is_file():
            raise ValueError(f"Source is not a file: {src_path}")

        if dst_path.exists() and not overwrite:
            raise FileExistsError(f"Destination file already exists: {dst_path}")

        # Ensure parent directory exists
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(src_path, dst_path)
        self._logger.info("Copied file from %s to %s", src_path, dst_path)
        return dst_path

    def move_file(
        self,
        src: Union[str, Path],
        dst: Union[str, Path],
        overwrite: bool = False,
    ) -> Path:
        """Move (or rename) a file.

        Parameters
        ----------
        src:
            Source file path.
        dst:
            Destination file path.
        overwrite:
            If True, overwrite existing destination file.

        Returns
        -------
        Path
            Path to the moved file.

        Raises
        ------
        FileNotFoundError
            If source file doesn't exist.
        FileExistsError
            If destination exists and overwrite is False.
        ValueError
            If paths are invalid or attempt directory traversal.
        """
        src_path = self._resolve_path(src)
        dst_path = self._resolve_path(dst)
        self._validate_path(src_path)
        self._validate_path(dst_path)

        if not src_path.exists():
            raise FileNotFoundError(f"Source file not found: {src_path}")

        if not src_path.is_file():
            raise ValueError(f"Source is not a file: {src_path}")

        if dst_path.exists() and not overwrite:
            raise FileExistsError(f"Destination file already exists: {dst_path}")

        # Ensure parent directory exists
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.move(str(src_path), str(dst_path))
        self._logger.info("Moved file from %s to %s", src_path, dst_path)
        return dst_path

    def rename_file(self, path: Union[str, Path], new_name: str) -> Path:
        """Rename a file.

        Parameters
        ----------
        path:
            Current file path.
        new_name:
            New filename (not a full path).

        Returns
        -------
        Path
            Path to the renamed file.

        Raises
        ------
        FileNotFoundError
            If file doesn't exist.
        ValueError
            If new_name is invalid or attempts directory traversal.
        """
        resolved_path = self._resolve_path(path)
        self._validate_path(resolved_path)

        if not resolved_path.exists():
            raise FileNotFoundError(f"File not found: {resolved_path}")

        if not resolved_path.is_file():
            raise ValueError(f"Path is not a file: {resolved_path}")

        # Sanitize new name
        sanitized_name = self.sanitize_filename(new_name)
        new_path = resolved_path.parent / sanitized_name

        if new_path.exists():
            raise FileExistsError(f"File with name already exists: {new_path}")

        resolved_path.rename(new_path)
        self._logger.info("Renamed file from %s to %s", resolved_path, new_path)
        return new_path

    def read_text(self, path: Union[str, Path], encoding: str = "utf-8") -> str:
        """Read text content from a file.

        Parameters
        ----------
        path:
            File path (relative to base_path or absolute).
        encoding:
            Text encoding to use.

        Returns
        -------
        str
            File content.

        Raises
        ------
        FileNotFoundError
            If file doesn't exist.
        ValueError
            If path is invalid or attempts directory traversal.
        """
        resolved_path = self._resolve_path(path)
        self._validate_path(resolved_path)

        if not resolved_path.exists():
            raise FileNotFoundError(f"File not found: {resolved_path}")

        if not resolved_path.is_file():
            raise ValueError(f"Path is not a file: {resolved_path}")

        content = resolved_path.read_text(encoding=encoding)
        self._logger.debug("Read text from file: %s (%d chars)", resolved_path, len(content))
        return content

    def write_text(self, path: Union[str, Path], content: str, encoding: str = "utf-8") -> Path:
        """Write text content to a file (overwrites existing).

        Parameters
        ----------
        path:
            File path (relative to base_path or absolute).
        content:
            Content to write.
        encoding:
            Text encoding to use.

        Returns
        -------
        Path
            Path to the written file.

        Raises
        ------
        ValueError
            If path is invalid or attempts directory traversal.
        """
        resolved_path = self._resolve_path(path)
        self._validate_path(resolved_path)

        # Ensure parent directory exists
        resolved_path.parent.mkdir(parents=True, exist_ok=True)

        resolved_path.write_text(content, encoding=encoding)
        self._logger.info("Wrote text to file: %s (%d chars)", resolved_path, len(content))
        return resolved_path

    def append_text(self, path: Union[str, Path], content: str, encoding: str = "utf-8") -> Path:
        """Append text content to a file.

        Parameters
        ----------
        path:
            File path (relative to base_path or absolute).
        content:
            Content to append.
        encoding:
            Text encoding to use.

        Returns
        -------
        Path
            Path to the file.

        Raises
        ------
        ValueError
            If path is invalid or attempts directory traversal.
        """
        resolved_path = self._resolve_path(path)
        self._validate_path(resolved_path)

        # Ensure parent directory exists
        resolved_path.parent.mkdir(parents=True, exist_ok=True)

        with resolved_path.open("a", encoding=encoding) as f:
            f.write(content)

        self._logger.info("Appended text to file: %s (%d chars)", resolved_path, len(content))
        return resolved_path

    def file_exists(self, path: Union[str, Path]) -> bool:
        """Check if a file exists.

        Parameters
        ----------
        path:
            File path (relative to base_path or absolute).

        Returns
        -------
        bool
            True if file exists, False otherwise.
        """
        resolved_path = self._resolve_path(path)
        return resolved_path.exists() and resolved_path.is_file()

    def list_files(self, path: Union[str, Path] = ".", pattern: str = "*") -> List[Path]:
        """List files in a given path.

        Parameters
        ----------
        path:
            Directory to list (relative to base_path or absolute).
        pattern:
            Glob pattern to filter files.

        Returns
        -------
        list of Path
            List of file paths.
        """
        resolved_path = self._resolve_path(path)
        self._validate_path(resolved_path)

        if not resolved_path.exists():
            return []

        files = [p for p in resolved_path.glob(pattern) if p.is_file()]
        self._logger.debug("Listed %d files in %s", len(files), resolved_path)
        return files

    def get_file_size(self, path: Union[str, Path]) -> int:
        """Get file size in bytes.

        Parameters
        ----------
        path:
            File path (relative to base_path or absolute).

        Returns
        -------
        int
            File size in bytes.

        Raises
        ------
        FileNotFoundError
            If file doesn't exist.
        ValueError
            If path is not a file.
        """
        resolved_path = self._resolve_path(path)
        self._validate_path(resolved_path)

        if not resolved_path.exists():
            raise FileNotFoundError(f"File not found: {resolved_path}")

        if not resolved_path.is_file():
            raise ValueError(f"Path is not a file: {resolved_path}")

        size = resolved_path.stat().st_size
        self._logger.debug("File size for %s: %d bytes", resolved_path, size)
        return size

    # ------------------------------------------------------------------
    # Path utilities
    # ------------------------------------------------------------------
    def get_extension(self, path: Union[str, Path]) -> str:
        """Get file extension (including the dot).

        Parameters
        ----------
        path:
            File path.

        Returns
        -------
        str
            File extension (e.g., '.txt') or empty string if none.
        """
        resolved_path = self._resolve_path(path)
        return resolved_path.suffix

    def get_filename(self, path: Union[str, Path]) -> str:
        """Get filename without extension.

        Parameters
        ----------
        path:
            File path.

        Returns
        -------
        str
            Filename without extension.
        """
        resolved_path = self._resolve_path(path)
        return resolved_path.stem

    def get_absolute_path(self, path: Union[str, Path]) -> Path:
        """Get absolute path for a given path.

        Parameters
        ----------
        path:
            Path (relative to base_path or absolute).

        Returns
        -------
        Path
            Absolute path.
        """
        return self._resolve_path(path)

    def sanitize_filename(self, filename: str) -> str:
        """Sanitize a filename to be safe for the filesystem.

        Parameters
        ----------
        filename:
            Original filename.

        Returns
        -------
        str
            Sanitized filename.

        Raises
        ------
        ValueError
            If filename is empty or becomes empty after sanitization.
        """
        if not filename or not filename.strip():
            raise ValueError("Filename cannot be empty")

        # Remove directory traversal attempts
        filename = filename.replace("..", "").replace("/", "").replace("\\", "")

        # Remove control characters
        filename = "".join(c for c in filename if ord(c) >= 32)

        # Remove reserved characters on Windows
        reserved_chars = '<>:"/\\|?*'
        for char in reserved_chars:
            filename = filename.replace(char, "_")

        # Remove trailing dots and spaces (Windows)
        filename = filename.rstrip(". ")

        # Limit length
        if len(filename) > 255:
            name, ext = os.path.splitext(filename)
            filename = name[: 255 - len(ext)] + ext

        if not filename:
            raise ValueError("Filename becomes empty after sanitization")

        return filename

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _resolve_path(self, path: Union[str, Path]) -> Path:
        """Resolve a path relative to base_path."""
        path_obj = Path(path)
        if path_obj.is_absolute():
            return path_obj.resolve()
        return (self._base_path / path_obj).resolve()

    def _validate_path(self, path: Path) -> None:
        """Validate that a path is within the allowed base directory."""
        try:
            path.resolve().relative_to(self._base_path.resolve())
        except ValueError:
            raise ValueError(f"Path traversal attempt detected: {path} is outside base path {self._base_path}")

    def __enter__(self) -> "FileManager":
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[object],
    ) -> None:
        pass