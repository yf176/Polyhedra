"""Tests for context manager service."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from polyhedra.services.context_manager import ContextManager


@pytest.fixture
def temp_dir():
    """Create temporary directory for testing."""
    with TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def context_manager(temp_dir):
    """Create context manager instance."""
    return ContextManager(temp_dir)


class TestReadFiles:
    """Test reading files."""

    def test_read_existing_file(self, context_manager, temp_dir):
        """Should read existing file content."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Hello, World!", encoding="utf-8")

        contents, missing = context_manager.read_files(["test.txt"])

        assert contents == {"test.txt": "Hello, World!"}
        assert missing == []

    def test_read_multiple_files(self, context_manager, temp_dir):
        """Should read multiple files."""
        (temp_dir / "file1.txt").write_text("Content 1", encoding="utf-8")
        (temp_dir / "subdir").mkdir()
        (temp_dir / "subdir" / "file2.txt").write_text("Content 2", encoding="utf-8")

        contents, missing = context_manager.read_files([
            "file1.txt",
            "subdir/file2.txt",
        ])

        assert len(contents) == 2
        assert contents["file1.txt"] == "Content 1"
        assert contents["subdir/file2.txt"] == "Content 2"
        assert missing == []

    def test_read_missing_file(self, context_manager):
        """Should report missing files."""
        contents, missing = context_manager.read_files([
            "missing.txt",
            "also_missing.txt",
        ])

        assert contents == {}
        assert missing == ["missing.txt", "also_missing.txt"]

    def test_read_mixed_files(self, context_manager, temp_dir):
        """Should handle mix of existing and missing files."""
        (temp_dir / "exists.txt").write_text("I exist", encoding="utf-8")

        contents, missing = context_manager.read_files([
            "exists.txt",
            "missing.txt",
        ])

        assert contents == {"exists.txt": "I exist"}
        assert missing == ["missing.txt"]


class TestWriteFile:
    """Test writing files."""

    def test_write_new_file(self, context_manager, temp_dir):
        """Should create and write new file."""
        bytes_written = context_manager.write_file("output.txt", "Test content")

        assert bytes_written > 0
        output_file = temp_dir / "output.txt"
        assert output_file.exists()
        assert output_file.read_text(encoding="utf-8") == "Test content"

    def test_write_with_directory_creation(self, context_manager, temp_dir):
        """Should create directories as needed."""
        context_manager.write_file("deep/nested/file.txt", "Content")

        output_file = temp_dir / "deep" / "nested" / "file.txt"
        assert output_file.exists()
        assert output_file.read_text(encoding="utf-8") == "Content"

    def test_write_file_overwrite(self, context_manager, temp_dir):
        """Should overwrite existing file by default."""
        test_file = temp_dir / "file.txt"
        test_file.write_text("Original", encoding="utf-8")

        context_manager.write_file("file.txt", "New content")

        assert test_file.read_text(encoding="utf-8") == "New content"

    def test_write_file_append(self, context_manager, temp_dir):
        """Should append to file when requested."""
        test_file = temp_dir / "file.txt"
        test_file.write_text("Line 1\n", encoding="utf-8")

        context_manager.write_file("file.txt", "Line 2\n", append=True)

        assert test_file.read_text(encoding="utf-8") == "Line 1\nLine 2\n"


class TestGetStatus:
    """Test project status retrieval."""

    def test_empty_project(self, context_manager):
        """Should return zero counts for empty project."""
        status = context_manager.get_status()

        assert status["papers_count"] == 0
        assert status["citations_count"] == 0
        assert status["rag_indexed"] is False
        assert isinstance(status["standard_files"], dict)

    def test_with_papers(self, context_manager, temp_dir):
        """Should count papers from papers.json."""
        papers_dir = temp_dir / "literature"
        papers_dir.mkdir()
        papers_file = papers_dir / "papers.json"

        papers = [
            {"paperId": "123", "title": "Paper 1"},
            {"paperId": "456", "title": "Paper 2"},
        ]
        papers_file.write_text(json.dumps(papers), encoding="utf-8")

        status = context_manager.get_status()

        assert status["papers_count"] == 2

    def test_with_citations(self, context_manager, temp_dir):
        """Should count citations from references.bib."""
        bib_file = temp_dir / "references.bib"
        bib_content = """
@article{smith2021,
    author = {Smith, J.},
    title = {Example Paper},
    year = {2021}
}

@inproceedings{jones2022,
    author = {Jones, A.},
    title = {Another Paper},
    year = {2022}
}
"""
        bib_file.write_text(bib_content, encoding="utf-8")

        status = context_manager.get_status()

        assert status["citations_count"] == 2

    def test_with_rag_index(self, context_manager, temp_dir):
        """Should detect RAG index file."""
        rag_dir = temp_dir / ".poly" / "embeddings"
        rag_dir.mkdir(parents=True)
        (rag_dir / "papers.pkl").write_bytes(b"dummy")

        status = context_manager.get_status()

        assert status["rag_indexed"] is True

    def test_standard_files_detection(self, context_manager, temp_dir):
        """Should detect standard project files."""
        # Create some standard files
        (temp_dir / "references.bib").write_text("", encoding="utf-8")
        lit_dir = temp_dir / "literature"
        lit_dir.mkdir()
        (lit_dir / "papers.json").write_text("[]", encoding="utf-8")

        status = context_manager.get_status()

        standard_files = status["standard_files"]
        assert standard_files["references.bib"] is True
        assert standard_files["literature/papers.json"] is True
        assert standard_files["paper/abstract.md"] is False
