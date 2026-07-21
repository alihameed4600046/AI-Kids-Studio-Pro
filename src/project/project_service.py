"""Project service for coordinating Project creation and persistence."""

import uuid
from datetime import datetime, timezone
from pathlib import Path

from src.models.project import Project
from src.project.project_repository import ProjectRepository


class ProjectService:
    """Lightweight service layer for Project creation and persistence."""

    def __init__(self, repository: ProjectRepository | None = None) -> None:
        """Initialize the service.

        Args:
            repository: Optional ProjectRepository instance. Creates default if None.
        """
        self._repository = repository or ProjectRepository()

    def create_project(
        self,
        name: str,
        description: str,
        category: str,
        project_path: str,
    ) -> Project:
        """Create a new Project instance with generated metadata.

        Args:
            name: Human-readable project name.
            description: Brief description of the project.
            category: Project category/type.
            project_path: Filesystem path to the project directory.

        Returns:
            New Project instance with generated id and timestamps.
        """
        now = datetime.now(timezone.utc).isoformat()
        return Project(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            category=category,
            created_at=now,
            updated_at=now,
            project_path=project_path,
        )

    def save_project(self, project: Project, file_path: Path) -> None:
        """Save a Project to a JSON file.

        Args:
            project: Project instance to save.
            file_path: Destination file path.
        """
        self._repository.save(project, file_path)

    def load_project(self, file_path: Path) -> Project:
        """Load a Project from a JSON file.

        Args:
            file_path: Source file path.

        Returns:
            Project instance reconstructed from JSON.
        """
        return self._repository.load(file_path)

    def save_new_project(self, project: Project) -> Path:
        """Save a new Project as project.json in its project directory.

        Args:
            project: Project instance to serialize.

        Returns:
            Full Path of the saved project.json file.

        Raises:
            FileExistsError: If a project.json file already exists at the target location.
        """
        project_dir = Path(project.project_path)
        project_dir.mkdir(parents=True, exist_ok=True)

        file_path = project_dir / "project.json"

        if self._repository.exists(file_path):
            raise FileExistsError(f"Project file already exists at {file_path}")

        self._repository.save(project, file_path)
        return file_path

    def open_project(self, project_directory: str | Path) -> Project:
        """Open an existing project from a project.json file.

        Args:
            project_directory: Path to the project directory containing project.json.

        Returns:
            Loaded Project instance.

        Raises:
            FileNotFoundError: If project.json does not exist in the given directory.
        """
        project_dir = Path(project_directory)
        file_path = project_dir / "project.json"

        if not self._repository.exists(file_path):
            raise FileNotFoundError(f"Project file not found at {file_path}")

        return self._repository.load(file_path)


__all__ = ["ProjectService"]
