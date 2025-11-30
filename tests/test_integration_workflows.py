"""End-to-end workflow integration tests."""

import json
import shutil
import time
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from polyhedra.server import call_tool, get_services
from polyhedra.services.project_initializer import ProjectInitializer


@pytest.fixture
def test_project():
    """Create a temporary test project."""
    with TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        
        # Initialize project structure
        initializer = ProjectInitializer(root)
        initializer.initialize("test-project")
        
        yield root
        
        # Force cleanup on Windows
        try:
            shutil.rmtree(root, ignore_errors=True)
        except Exception:
            pass


class TestEndToEndWorkflows:
    """Test complete end-to-end workflows."""

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_workflow_search_save_index_query(self, test_project, monkeypatch):
        """Test: Search → Save → Index → Query workflow."""
        monkeypatch.chdir(test_project)
        
        # Clear service cache
        services = get_services()
        services.clear()

        # Step 1: Search for papers
        search_result = await call_tool(
            "search_papers",
            {"query": "machine learning", "limit": 3}
        )
        papers = json.loads(search_result[0].text)
        assert len(papers) > 0
        print(f"✓ Found {len(papers)} papers")

        # Step 2: Save papers to file
        save_result = await call_tool(
            "save_file",
            {
                "path": "literature/papers.json",
                "content": json.dumps(papers, indent=2)
            }
        )
        save_data = json.loads(save_result[0].text)
        assert save_data["success"] is True
        print(f"✓ Saved {save_data['bytes_written']} bytes")

        # Step 3: Index papers for semantic search
        index_result = await call_tool(
            "index_papers",
            {"papers_path": "literature/papers.json"}
        )
        index_data = json.loads(index_result[0].text)
        assert index_data.get("success") is True
        assert index_data["indexed_count"] == len(papers)
        print(f"✓ Indexed {index_data['indexed_count']} papers")

        # Step 4: Query similar papers
        query_result = await call_tool(
            "query_similar_papers",
            {"query": "deep learning", "k": 2}
        )
        similar = json.loads(query_result[0].text)
        assert isinstance(similar, list)
        assert len(similar) > 0
        assert "relevance_score" in similar[0]
        print(f"✓ Found {len(similar)} similar papers")

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_workflow_search_add_citations(self, test_project, monkeypatch):
        """Test: Search → Add Citations workflow."""
        monkeypatch.chdir(test_project)
        
        # Clear service cache
        services = get_services()
        services.clear()

        # Step 1: Search for papers
        search_result = await call_tool(
            "search_papers",
            {"query": "transformer architecture", "limit": 2}
        )
        papers = json.loads(search_result[0].text)
        assert len(papers) > 0
        print(f"✓ Found {len(papers)} papers")

        # Step 2: Add citations from papers
        citations_added = 0
        for paper in papers:
            if paper.get("bibtex_entry"):
                cite_result = await call_tool(
                    "add_citation",
                    {"bibtex": paper["bibtex_entry"]}
                )
                cite_data = json.loads(cite_result[0].text)
                if cite_data.get("added"):
                    citations_added += 1

        print(f"✓ Added {citations_added} citations")

        # Step 3: Verify citations were added
        get_citations_result = await call_tool("get_citations", {})
        citations = json.loads(get_citations_result[0].text)
        assert len(citations) >= citations_added
        print(f"✓ Total citations: {len(citations)}")

    @pytest.mark.asyncio
    async def test_workflow_init_get_status(self, monkeypatch):
        """Test: Init Project → Get Status workflow."""
        tmpdir = TemporaryDirectory(delete=False)
        project_root = Path(tmpdir.name)
        try:
            monkeypatch.chdir(project_root)
            
            # Clear service cache
            services = get_services()
            services.clear()

            # Step 1: Initialize project
            init_result = await call_tool(
                "init_project",
                {"project_name": "test-research"}
            )
            init_data = json.loads(init_result[0].text)
            assert len(init_data["created_dirs"]) > 0
            assert len(init_data["created_files"]) > 0
            print(f"✓ Created {len(init_data['created_dirs'])} dirs, {len(init_data['created_files'])} files")

            # Step 2: Get project status
            status_result = await call_tool("get_project_status", {})
            status = json.loads(status_result[0].text)
            assert status["papers_count"] == 0
            assert status["citations_count"] == 0
            assert status["rag_indexed"] is False
            assert len(status["standard_files"]) > 0
            print(f"✓ Project status retrieved: {len(status['standard_files'])} standard files tracked")
        finally:
            # Manual cleanup to avoid Windows recursion issues
            import gc
            gc.collect()  # Force garbage collection first
            try:
                shutil.rmtree(project_root, ignore_errors=True)
            except Exception:
                pass

    @pytest.mark.asyncio
    async def test_workflow_write_read_file(self, test_project, monkeypatch):
        """Test: Write File → Read File workflow."""
        monkeypatch.chdir(test_project)
        
        # Clear service cache
        services = get_services()
        services.clear()

        # Step 1: Write file
        content = "# Research Notes\n\nThese are my notes on ML papers."
        write_result = await call_tool(
            "save_file",
            {"path": "ideas/notes.md", "content": content}
        )
        write_data = json.loads(write_result[0].text)
        assert write_data["success"] is True
        print(f"✓ Wrote {write_data['bytes_written']} bytes")

        # Step 2: Read file back
        read_result = await call_tool(
            "get_context",
            {"paths": ["ideas/notes.md"]}
        )
        read_data = json.loads(read_result[0].text)
        assert "ideas/notes.md" in read_data["contents"]
        assert read_data["contents"]["ideas/notes.md"] == content
        print(f"✓ Read file successfully, content matches")

        # Step 3: Append to file
        append_content = "\n\n## More Notes\n\nAdditional thoughts."
        append_result = await call_tool(
            "save_file",
            {
                "path": "ideas/notes.md",
                "content": append_content,
                "append": True
            }
        )
        append_data = json.loads(append_result[0].text)
        assert append_data["success"] is True
        print(f"✓ Appended {append_data['bytes_written']} bytes")

        # Step 4: Verify appended content
        verify_result = await call_tool(
            "get_context",
            {"paths": ["ideas/notes.md"]}
        )
        verify_data = json.loads(verify_result[0].text)
        full_content = verify_data["contents"]["ideas/notes.md"]
        assert content in full_content
        assert append_content.strip() in full_content
        print(f"✓ Verified appended content")


class TestPerformance:
    """Test performance targets."""

    @pytest.mark.integration
    @pytest.mark.skip(reason="External API timing is unreliable, depends on network and rate limits")
    @pytest.mark.asyncio
    async def test_search_performance(self):
        """Search should complete in < 2s."""
        from polyhedra.services.semantic_scholar import SemanticScholarService
        
        service = SemanticScholarService()
        try:
            start = time.time()
            results = await service.search("machine learning", limit=5)
            duration = time.time() - start

            assert duration < 2.0, f"Search took {duration:.2f}s, expected < 2s"
            assert len(results) > 0
            print(f"✓ Search completed in {duration:.3f}s (< 2s target)")
        finally:
            await service.close()

    @pytest.mark.asyncio
    async def test_local_operations_performance(self, test_project, monkeypatch):
        """Local operations should complete in < 100ms."""
        monkeypatch.chdir(test_project)
        
        # Clear service cache
        services = get_services()
        services.clear()

        # Test write file
        start = time.time()
        await call_tool(
            "save_file",
            {"path": "test.txt", "content": "test content"}
        )
        write_duration = time.time() - start
        assert write_duration < 0.1, f"Write took {write_duration*1000:.1f}ms, expected < 100ms"
        print(f"✓ Write file: {write_duration*1000:.1f}ms")

        # Test read file
        start = time.time()
        await call_tool("get_context", {"paths": ["test.txt"]})
        read_duration = time.time() - start
        assert read_duration < 0.1, f"Read took {read_duration*1000:.1f}ms, expected < 100ms"
        print(f"✓ Read file: {read_duration*1000:.1f}ms")

        # Test get status
        start = time.time()
        await call_tool("get_project_status", {})
        status_duration = time.time() - start
        assert status_duration < 0.1, f"Status took {status_duration*1000:.1f}ms, expected < 100ms"
        print(f"✓ Get status: {status_duration*1000:.1f}ms")

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_rag_query_performance(self, test_project, monkeypatch):
        """RAG query should complete in < 500ms."""
        monkeypatch.chdir(test_project)
        
        # Clear service cache
        services = get_services()
        services.clear()

        # Create sample papers
        papers = [
            {
                "paperId": "1",
                "title": "Deep Learning for Computer Vision",
                "abstract": "This paper explores deep learning techniques for image recognition.",
                "authors": ["Smith, J."],
                "year": 2020
            },
            {
                "paperId": "2",
                "title": "Transformer Models in NLP",
                "abstract": "We present transformer architectures for natural language processing.",
                "authors": ["Jones, A."],
                "year": 2021
            }
        ]

        # Save and index
        await call_tool(
            "save_file",
            {"path": "literature/papers.json", "content": json.dumps(papers)}
        )
        await call_tool("index_papers", {})

        # Test query performance
        start = time.time()
        result = await call_tool(
            "query_similar_papers",
            {"query": "deep learning", "k": 2}
        )
        duration = time.time() - start

        assert duration < 0.5, f"RAG query took {duration*1000:.1f}ms, expected < 500ms"
        
        similar = json.loads(result[0].text)
        assert len(similar) > 0
        print(f"✓ RAG query: {duration*1000:.1f}ms")


class TestErrorHandling:
    """Test error handling in workflows."""

    @pytest.mark.asyncio
    async def test_query_before_indexing(self, test_project, monkeypatch):
        """Should handle query before indexing gracefully."""
        monkeypatch.chdir(test_project)
        
        # Clear service cache
        services = get_services()
        services.clear()

        result = await call_tool(
            "query_similar_papers",
            {"query": "test"}
        )
        data = json.loads(result[0].text)
        assert "error" in data
        assert "not indexed" in data["error"].lower()
        print("✓ Handles query before indexing")

    @pytest.mark.asyncio
    async def test_missing_file_read(self, test_project, monkeypatch):
        """Should handle missing files gracefully."""
        monkeypatch.chdir(test_project)
        
        # Clear service cache
        services = get_services()
        services.clear()

        result = await call_tool(
            "get_context",
            {"paths": ["nonexistent.md"]}
        )
        data = json.loads(result[0].text)
        assert "missing" in data
        assert "nonexistent.md" in data["missing"]
        print("✓ Handles missing files")

    @pytest.mark.asyncio
    async def test_invalid_citation(self, test_project, monkeypatch):
        """Should handle invalid BibTeX gracefully."""
        monkeypatch.chdir(test_project)
        
        # Clear service cache
        services = get_services()
        services.clear()

        result = await call_tool(
            "add_citation",
            {"bibtex": "invalid bibtex"}
        )
        data = json.loads(result[0].text)
        assert "error" in data
        print("✓ Handles invalid BibTeX")
