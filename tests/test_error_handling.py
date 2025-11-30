"""Tests for error handling across all services."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from polyhedra.server import call_tool, get_services
from polyhedra.services.citation_manager import CitationManager
from polyhedra.services.context_manager import ContextManager
from polyhedra.services.rag_service import RAGService


class TestNetworkErrorHandling:
    """Test network error scenarios."""

    @pytest.mark.asyncio
    async def test_invalid_paper_id(self):
        """Should handle invalid paper ID gracefully."""
        result = await call_tool(
            "get_paper",
            {"paper_id": "invalid-nonexistent-id-12345"}
        )
        data = json.loads(result[0].text)
        # May return error or empty result depending on API
        assert isinstance(data, (dict, type(None)))


class TestFileSystemErrorHandling:
    """Test file system error scenarios."""

    @pytest.mark.asyncio
    async def test_read_missing_files(self, tmp_path, monkeypatch):
        """Should report missing files without failing."""
        monkeypatch.chdir(tmp_path)
        
        # Clear service cache
        services = get_services()
        services.clear()

        result = await call_tool(
            "get_context",
            {"paths": ["missing1.md", "missing2.md", "missing3.md"]}
        )
        data = json.loads(result[0].text)
        
        assert "missing" in data
        assert len(data["missing"]) == 3
        assert "missing1.md" in data["missing"]
        print("✓ Missing files reported correctly")

    @pytest.mark.asyncio
    async def test_read_mixed_existing_missing(self, tmp_path, monkeypatch):
        """Should read existing files and report missing ones."""
        monkeypatch.chdir(tmp_path)
        
        # Create one file
        (tmp_path / "exists.md").write_text("content", encoding="utf-8")
        
        # Clear service cache
        services = get_services()
        services.clear()

        result = await call_tool(
            "get_context",
            {"paths": ["exists.md", "missing.md"]}
        )
        data = json.loads(result[0].text)
        
        assert "exists.md" in data["contents"]
        assert "missing.md" in data["missing"]
        print("✓ Graceful degradation working")

    def test_write_to_nonexistent_directory(self, tmp_path):
        """Should create parent directories automatically."""
        manager = ContextManager(tmp_path)
        
        # Should succeed by creating directories
        bytes_written = manager.write_file(
            "deep/nested/path/file.txt",
            "content"
        )
        
        assert bytes_written > 0
        assert (tmp_path / "deep" / "nested" / "path" / "file.txt").exists()
        print("✓ Creates parent directories")


class TestValidationErrorHandling:
    """Test validation error scenarios."""

    def test_invalid_bibtex_format(self, tmp_path):
        """Should reject invalid BibTeX with clear error."""
        manager = CitationManager(tmp_path)
        
        with pytest.raises(ValueError) as exc_info:
            manager.add_entry("invalid bibtex")
        
        # Accepts either error message from different bibtexparser versions
        error_msg = str(exc_info.value)
        assert "Invalid BibTeX" in error_msg or "No valid BibTeX entries" in error_msg
        print("✓ Invalid BibTeX rejected with clear error")

    def test_bibtex_missing_required_fields(self, tmp_path):
        """Should reject BibTeX missing ID."""
        manager = CitationManager(tmp_path)
        
        # BibTeX without proper structure
        invalid_bibtex = "@article{}"
        
        with pytest.raises(ValueError) as exc_info:
            manager.add_entry(invalid_bibtex)
        
        error_msg = str(exc_info.value)
        assert "BibTeX" in error_msg or "ID" in error_msg
        print("✓ Missing fields detected")

    def test_empty_papers_list_indexing(self, tmp_path):
        """Should reject empty papers list."""
        service = RAGService(tmp_path)
        
        with pytest.raises(ValueError) as exc_info:
            service.index_papers([])
        
        assert "empty" in str(exc_info.value).lower()
        print("✓ Empty papers list rejected")

    def test_paper_missing_title(self, tmp_path):
        """Should reject paper without title."""
        service = RAGService(tmp_path)
        
        papers = [
            {"paperId": "123", "abstract": "Test"}
            # Missing title
        ]
        
        with pytest.raises(ValueError) as exc_info:
            service.index_papers(papers)
        
        assert "title" in str(exc_info.value).lower()
        print("✓ Missing title detected")

    @pytest.mark.asyncio
    async def test_empty_search_query(self):
        """Should reject empty search query."""
        from polyhedra.services.semantic_scholar import SemanticScholarService
        
        service = SemanticScholarService()
        try:
            with pytest.raises(ValueError) as exc_info:
                await service.search("")
            
            assert "empty" in str(exc_info.value).lower()
            print("✓ Empty query rejected")
        finally:
            await service.close()

    @pytest.mark.asyncio
    async def test_invalid_search_limit(self):
        """Should reject invalid limit values."""
        from polyhedra.services.semantic_scholar import SemanticScholarService
        
        service = SemanticScholarService()
        try:
            # Test limit too high
            with pytest.raises(ValueError) as exc_info:
                await service.search("test", limit=101)
            assert "between 1 and 100" in str(exc_info.value)
            
            # Test limit too low
            with pytest.raises(ValueError) as exc_info:
                await service.search("test", limit=0)
            assert "between 1 and 100" in str(exc_info.value)
            
            print("✓ Invalid limits rejected")
        finally:
            await service.close()


class TestStateErrorHandling:
    """Test state-related error scenarios."""

    @pytest.mark.asyncio
    async def test_query_before_indexing(self, tmp_path, monkeypatch):
        """Should error when querying before indexing."""
        monkeypatch.chdir(tmp_path)
        
        # Initialize project structure
        (tmp_path / "literature").mkdir()
        (tmp_path / "references.bib").write_text("", encoding="utf-8")
        
        # Clear service cache
        services = get_services()
        services.clear()

        result = await call_tool(
            "query_similar_papers",
            {"query": "test", "k": 5}
        )
        data = json.loads(result[0].text)
        
        assert "error" in data
        assert "not indexed" in data["error"].lower()
        print("✓ Query before indexing handled")

    @pytest.mark.asyncio
    async def test_index_missing_papers_file(self, tmp_path, monkeypatch):
        """Should error when papers file doesn't exist."""
        monkeypatch.chdir(tmp_path)
        
        # Clear service cache
        services = get_services()
        services.clear()

        result = await call_tool(
            "index_papers",
            {"papers_path": "literature/papers.json"}
        )
        data = json.loads(result[0].text)
        
        assert "error" in data
        assert "not found" in data["error"].lower()
        print("✓ Missing papers file handled")


class TestGracefulDegradation:
    """Test graceful degradation in partial failures."""

    @pytest.mark.asyncio
    async def test_multiple_file_read_partial_success(self, tmp_path, monkeypatch):
        """Should return available files and report missing ones."""
        monkeypatch.chdir(tmp_path)
        
        # Create some files
        (tmp_path / "file1.md").write_text("Content 1", encoding="utf-8")
        (tmp_path / "file2.md").write_text("Content 2", encoding="utf-8")
        (tmp_path / "file3.md").write_text("Content 3", encoding="utf-8")
        
        # Clear service cache
        services = get_services()
        services.clear()

        result = await call_tool(
            "get_context",
            {
                "paths": [
                    "file1.md",
                    "missing1.md",
                    "file2.md",
                    "missing2.md",
                    "file3.md"
                ]
            }
        )
        data = json.loads(result[0].text)
        
        # Should have 3 successful reads
        assert len(data["contents"]) == 3
        assert "file1.md" in data["contents"]
        assert "file2.md" in data["contents"]
        assert "file3.md" in data["contents"]
        
        # Should report 2 missing
        assert len(data["missing"]) == 2
        assert "missing1.md" in data["missing"]
        assert "missing2.md" in data["missing"]
        
        print("✓ Partial success handled correctly")

    def test_duplicate_citation_handling(self, tmp_path):
        """Should handle duplicate citations gracefully."""
        manager = CitationManager(tmp_path)
        
        bibtex = """@article{test2021,
    author = {Test, A.},
    title = {Test Paper},
    year = {2021}
}"""
        
        # Add first time
        key1, added1 = manager.add_entry(bibtex)
        assert added1 is True
        
        # Add duplicate
        key2, added2 = manager.add_entry(bibtex)
        assert added2 is False
        assert key1 == key2
        
        print("✓ Duplicate citations handled")


class TestErrorMessaging:
    """Test error message clarity and consistency."""

    @pytest.mark.asyncio
    async def test_error_message_format(self, tmp_path, monkeypatch):
        """Error messages should have consistent format."""
        monkeypatch.chdir(tmp_path)
        
        # Clear service cache
        services = get_services()
        services.clear()

        # Test unknown tool
        result = await call_tool("unknown_tool", {})
        data = json.loads(result[0].text)
        
        assert "error" in data
        assert isinstance(data["error"], str)
        assert len(data["error"]) > 0
        print("✓ Error message format consistent")

    @pytest.mark.asyncio
    async def test_error_includes_context(self, tmp_path, monkeypatch):
        """Error messages should include helpful context."""
        monkeypatch.chdir(tmp_path)
        
        # Clear service cache
        services = get_services()
        services.clear()

        result = await call_tool(
            "index_papers",
            {"papers_path": "nonexistent.json"}
        )
        data = json.loads(result[0].text)
        
        assert "error" in data
        # Should mention the file path
        assert "nonexistent.json" in data["error"]
        print("✓ Error includes context")


class TestErrorRecovery:
    """Test error recovery scenarios."""

    @pytest.mark.asyncio
    async def test_retry_after_error(self, tmp_path, monkeypatch):
        """Should be able to retry after error."""
        monkeypatch.chdir(tmp_path)
        
        # Clear service cache
        services = get_services()
        services.clear()

        # First attempt fails (missing file)
        result1 = await call_tool(
            "index_papers",
            {"papers_path": "papers.json"}
        )
        data1 = json.loads(result1[0].text)
        assert "error" in data1
        
        # Create file
        (tmp_path / "papers.json").write_text(
            json.dumps([
                {
                    "paperId": "1",
                    "title": "Test Paper",
                    "abstract": "Abstract",
                    "authors": ["Test"],
                    "year": 2021
                }
            ]),
            encoding="utf-8"
        )
        
        # Retry succeeds
        result2 = await call_tool(
            "index_papers",
            {"papers_path": "papers.json"}
        )
        data2 = json.loads(result2[0].text)
        assert data2.get("success") is True
        
        print("✓ Retry after error works")
