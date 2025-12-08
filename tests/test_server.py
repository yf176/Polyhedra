"""Integration tests for MCP server."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from polyhedra.server import app, call_tool, get_services, list_tools


@pytest.fixture
def temp_project():
    """Create temporary project directory."""
    with TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        # Create basic structure
        (project_root / "literature").mkdir()
        (project_root / "literature" / "papers.json").write_text("[]", encoding="utf-8")
        (project_root / "references.bib").write_text("", encoding="utf-8")
        yield project_root


class TestServerInitialization:
    """Test server initialization."""

    def test_server_name(self):
        """Server should have correct name."""
        assert app.name == "polyhedra"

    @pytest.mark.asyncio
    async def test_list_tools_count(self):
        """Should list all 11 tools (10 existing + generate_literature_review)."""
        tools = await list_tools()
        assert len(tools) == 11

    @pytest.mark.asyncio
    async def test_list_tools_names(self):
        """Should include all expected tool names."""
        tools = await list_tools()
        tool_names = {tool.name for tool in tools}

        expected_names = {
            "search_papers",
            "get_paper",
            "get_context",
            "query_similar_papers",
            "index_papers",
            "save_file",
            "add_citation",
            "get_citations",
            "get_project_status",
            "init_project",
            "generate_literature_review",
        }

        assert tool_names == expected_names

    @pytest.mark.asyncio
    async def test_tool_schemas_valid(self):
        """All tools should have valid schemas."""
        tools = await list_tools()

        for tool in tools:
            assert tool.name
            assert tool.description
            assert tool.inputSchema
            assert "type" in tool.inputSchema
            assert tool.inputSchema["type"] == "object"
            assert "properties" in tool.inputSchema


class TestToolExecution:
    """Test tool execution."""

    @pytest.mark.asyncio
    async def test_get_project_status(self, temp_project, monkeypatch):
        """Should execute get_project_status tool."""
        monkeypatch.chdir(temp_project)

        # Clear service cache
        services = get_services()
        services.clear()

        result = await call_tool("get_project_status", {})
        assert len(result) == 1
        assert result[0].type == "text"

        data = json.loads(result[0].text)
        assert "root" in data
        assert "papers_count" in data
        assert "citations_count" in data

    @pytest.mark.asyncio
    async def test_get_citations(self, temp_project, monkeypatch):
        """Should execute get_citations tool."""
        monkeypatch.chdir(temp_project)

        # Clear service cache
        services = get_services()
        services.clear()

        result = await call_tool("get_citations", {})
        assert len(result) == 1

        data = json.loads(result[0].text)
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_save_file(self, temp_project, monkeypatch):
        """Should execute save_file tool."""
        monkeypatch.chdir(temp_project)

        # Clear service cache
        services = get_services()
        services.clear()

        result = await call_tool(
            "save_file",
            {"path": "test.txt", "content": "Hello, World!"},
        )
        assert len(result) == 1

        data = json.loads(result[0].text)
        assert data["success"] is True
        assert data["path"] == "test.txt"
        assert data["bytes_written"] > 0

        # Verify file was created
        assert (temp_project / "test.txt").exists()

    @pytest.mark.asyncio
    async def test_add_citation(self, temp_project, monkeypatch):
        """Should execute add_citation tool."""
        monkeypatch.chdir(temp_project)

        # Clear service cache
        services = get_services()
        services.clear()

        bibtex = """@article{test2021,
    author = {Test, A.},
    title = {Test Paper},
    year = {2021}
}"""

        result = await call_tool("add_citation", {"bibtex": bibtex})
        assert len(result) == 1

        data = json.loads(result[0].text)
        assert data["key"] == "test2021"
        assert data["added"] is True

    @pytest.mark.asyncio
    async def test_init_project(self, temp_project, monkeypatch):
        """Should execute init_project tool."""
        new_project = temp_project / "new_proj"
        new_project.mkdir()
        monkeypatch.chdir(new_project)

        # Clear service cache
        services = get_services()
        services.clear()

        result = await call_tool("init_project", {"project_name": "test-project"})
        assert len(result) == 1

        data = json.loads(result[0].text)
        assert "created_dirs" in data
        assert "created_files" in data
        assert len(data["created_dirs"]) > 0

    @pytest.mark.asyncio
    async def test_unknown_tool(self):
        """Should handle unknown tool gracefully."""
        result = await call_tool("unknown_tool", {})
        assert len(result) == 1

        data = json.loads(result[0].text)
        assert "error" in data
        assert "Unknown tool" in data["error"]

    @pytest.mark.asyncio
    async def test_tool_error_handling(self, temp_project, monkeypatch):
        """Should handle tool execution errors."""
        monkeypatch.chdir(temp_project)

        # Clear service cache
        services = get_services()
        services.clear()

        # Try to add invalid BibTeX
        result = await call_tool("add_citation", {"bibtex": "invalid"})
        assert len(result) == 1

        data = json.loads(result[0].text)
        assert "error" in data


class TestServiceIntegration:
    """Test service integration."""

    @pytest.mark.asyncio
    async def test_get_context(self, temp_project, monkeypatch):
        """Should read project files."""
        monkeypatch.chdir(temp_project)

        # Clear service cache
        services = get_services()
        services.clear()

        # Create test file
        (temp_project / "test.md").write_text("# Test", encoding="utf-8")

        result = await call_tool("get_context", {"paths": ["test.md", "missing.md"]})
        assert len(result) == 1

        data = json.loads(result[0].text)
        assert "contents" in data
        assert "missing" in data
        assert "test.md" in data["contents"]
        assert "missing.md" in data["missing"]

    @pytest.mark.asyncio
    async def test_query_similar_papers_not_indexed(self, temp_project, monkeypatch):
        """Should handle query before indexing."""
        monkeypatch.chdir(temp_project)

        # Clear service cache
        services = get_services()
        services.clear()

        result = await call_tool("query_similar_papers", {"query": "test"})
        assert len(result) == 1

        data = json.loads(result[0].text)
        assert "error" in data
        assert "not indexed" in data["error"].lower()

    @pytest.mark.asyncio
    async def test_generate_literature_review_missing_papers(
        self, temp_project, monkeypatch
    ):
        """Should handle missing papers file gracefully."""
        monkeypatch.chdir(temp_project)

        # Clear service cache
        services = get_services()
        services.clear()

        result = await call_tool("generate_literature_review", {})
        assert len(result) == 1

        data = json.loads(result[0].text)
        assert "error" in data
        # Should handle either missing file or empty file
        assert "not found" in data["error"].lower() or "empty" in data["error"].lower()
