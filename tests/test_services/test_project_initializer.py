"""Tests for project initialization service."""

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from polyhedra.services.project_initializer import ProjectInitializer


@pytest.fixture
def temp_dir():
    """Create temporary directory for testing."""
    with TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def initializer(temp_dir):
    """Create project initializer instance."""
    return ProjectInitializer(temp_dir)


class TestInitialize:
    """Test project initialization."""

    def test_create_all_directories(self, initializer, temp_dir):
        """Should create all standard directories."""
        result = initializer.initialize()

        expected_dirs = [
            "literature",
            "ideas",
            "method",
            "paper",
            ".poly/embeddings",
        ]

        for dir_path in expected_dirs:
            full_path = temp_dir / dir_path
            assert full_path.exists(), f"Directory {dir_path} should exist"
            assert full_path.is_dir(), f"{dir_path} should be a directory"

        assert set(result["created_dirs"]) == set(expected_dirs)

    def test_create_references_bib(self, initializer, temp_dir):
        """Should create empty references.bib file."""
        result = initializer.initialize()

        bib_file = temp_dir / "references.bib"
        assert bib_file.exists()
        assert bib_file.read_text(encoding="utf-8") == ""
        assert "references.bib" in result["created_files"]

    def test_create_config_yaml(self, initializer, temp_dir):
        """Should create config.yaml with project metadata."""
        result = initializer.initialize(project_name="test-project")

        config_file = temp_dir / ".poly" / "config.yaml"
        assert config_file.exists()

        content = config_file.read_text(encoding="utf-8")
        assert "test-project" in content
        assert "version: \"2.0.0\"" in content
        assert "literature/papers.json" in content
        assert "references.bib" in content

        assert ".poly/config.yaml" in result["created_files"]

    def test_default_project_name(self, temp_dir):
        """Should use directory name as default project name."""
        initializer = ProjectInitializer(temp_dir)
        initializer.initialize()

        config_file = temp_dir / ".poly" / "config.yaml"
        content = config_file.read_text(encoding="utf-8")
        assert temp_dir.name in content

    def test_idempotent_initialization(self, initializer, temp_dir):
        """Should be safe to run multiple times."""
        # First initialization
        result1 = initializer.initialize()
        assert len(result1["created_dirs"]) == 5
        assert len(result1["created_files"]) == 2

        # Second initialization
        result2 = initializer.initialize()
        assert len(result2["created_dirs"]) == 0
        assert len(result2["created_files"]) == 0
        assert len(result2["existing_dirs"]) == 5
        assert len(result2["existing_files"]) == 2

        # Verify no files were overwritten
        config_file = temp_dir / ".poly" / "config.yaml"
        content = config_file.read_text(encoding="utf-8")
        assert content.count("version:") == 1  # Only one occurrence

    def test_preserve_existing_files(self, initializer, temp_dir):
        """Should not overwrite existing files."""
        # Pre-create references.bib with content
        bib_file = temp_dir / "references.bib"
        original_content = "@article{test2021}"
        bib_file.write_text(original_content, encoding="utf-8")

        result = initializer.initialize()

        # File should be preserved
        assert bib_file.read_text(encoding="utf-8") == original_content
        assert "references.bib" in result["existing_files"]
        assert "references.bib" not in result["created_files"]

    def test_partial_initialization(self, initializer, temp_dir):
        """Should handle partially initialized projects."""
        # Pre-create some directories
        (temp_dir / "literature").mkdir()
        (temp_dir / "ideas").mkdir()

        result = initializer.initialize()

        # Should report existing and newly created separately
        assert "literature" in result["existing_dirs"]
        assert "ideas" in result["existing_dirs"]
        assert "method" in result["created_dirs"]
        assert "paper" in result["created_dirs"]

    def test_return_structure(self, initializer):
        """Should return complete initialization report."""
        result = initializer.initialize()

        assert "root" in result
        assert "created_dirs" in result
        assert "created_files" in result
        assert "existing_dirs" in result
        assert "existing_files" in result

        assert isinstance(result["root"], str)
        assert isinstance(result["created_dirs"], list)
        assert isinstance(result["created_files"], list)
        assert isinstance(result["existing_dirs"], list)
        assert isinstance(result["existing_files"], list)
