import unittest
import shutil
from src.file_manager.file_manager import FileManager
from pathlib import Path
import os

class TestFileManager(unittest.TestCase):
    def setUp(self):
        """Set up a temporary directory for testing."""
        self.test_dir = Path("test_file_manager")
        self.file_manager = FileManager(base_path=self.test_dir)

    def tearDown(self):
        """Clean up the temporary directory after tests."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_create_directory(self):
        """Test creating a directory."""
        dir_name = "test_dir"
        created_dir = self.file_manager.create_directory(dir_name)
        self.assertTrue(created_dir.exists())
        self.assertTrue(created_dir.is_dir())

    def test_create_file(self):
        """Test creating a file."""
        file_name = "test_file.txt"
        created_file = self.file_manager.create_file(file_name, "Hello, World!")
        self.assertTrue(created_file.exists())
        self.assertTrue(created_file.is_file())
        self.assertEqual(created_file.read_text(), "Hello, World!")

    def test_delete_file(self):
        """Test deleting a file."""
        file_name = "test_file.txt"
        self.file_manager.create_file(file_name, "Hello, World!")
        self.assertTrue(self.file_manager.delete_file(file_name))
        self.assertFalse(Path(self.file_manager.get_absolute_path(file_name)).exists())

    def test_delete_directory(self):
        """Test deleting a directory."""
        dir_name = "test_dir"
        self.file_manager.create_directory(dir_name)
        self.assertTrue(self.file_manager.delete_directory(dir_name))
        self.assertFalse(Path(self.file_manager.get_absolute_path(dir_name)).exists())

    def test_create_project_structure(self):
        """Test creating a project structure."""
        project_name = "my_project"

        project_root = self.file_manager.create_project_structure(project_name)

        self.assertTrue(project_root.exists())
        self.assertTrue(project_root.is_dir())

        expected_dirs = [
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

        for dir_name in expected_dirs:
            self.assertTrue((project_root / dir_name).exists())
            self.assertTrue((project_root / dir_name).is_dir())

if __name__ == "__main__":
    unittest.main()