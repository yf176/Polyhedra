"""MCP Server implementation for Polyhedra."""

import asyncio
import json
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from polyhedra.services.citation_manager import CitationManager
from polyhedra.services.context_manager import ContextManager
from polyhedra.services.project_initializer import ProjectInitializer
from polyhedra.services.rag_service import RAGService
from polyhedra.services.semantic_scholar import SemanticScholarService

# Initialize MCP server
app = Server("polyhedra")

# Service instances (initialized lazily)
_services: dict[str, Any] = {}


def get_project_root() -> Path:
    """Get project root directory from current working directory."""
    return Path.cwd()


def get_services() -> dict[str, Any]:
    """Get or initialize service instances."""
    if not _services:
        project_root = get_project_root()
        _services["semantic_scholar"] = SemanticScholarService()
        _services["citation_manager"] = CitationManager(project_root)
        _services["context_manager"] = ContextManager(project_root)
        _services["rag_service"] = RAGService(project_root)
        _services["project_initializer"] = ProjectInitializer(project_root)
    return _services


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available MCP tools."""
    return [
        Tool(
            name="search_papers",
            description="Search academic papers using Semantic Scholar API",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query string"},
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (1-100)",
                        "default": 20,
                        "minimum": 1,
                        "maximum": 100,
                    },
                    "year_start": {
                        "type": "integer",
                        "description": "Start year for filtering (optional)",
                    },
                    "year_end": {
                        "type": "integer",
                        "description": "End year for filtering (optional)",
                    },
                    "fields_of_study": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Fields of study to filter by (optional)",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_paper",
            description="Get detailed information about a specific paper by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "paper_id": {
                        "type": "string",
                        "description": "Semantic Scholar paper ID",
                    },
                },
                "required": ["paper_id"],
            },
        ),
        Tool(
            name="get_context",
            description="Read multiple files from the research project",
            inputSchema={
                "type": "object",
                "properties": {
                    "paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of relative file paths to read",
                    },
                },
                "required": ["paths"],
            },
        ),
        Tool(
            name="query_similar_papers",
            description="Find similar papers using semantic search over indexed papers",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Query text to search for similar papers",
                    },
                    "k": {
                        "type": "integer",
                        "description": "Number of similar papers to return",
                        "default": 5,
                        "minimum": 1,
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="index_papers",
            description="Build semantic search index from papers.json",
            inputSchema={
                "type": "object",
                "properties": {
                    "papers_path": {
                        "type": "string",
                        "description": (
                            "Path to papers.json file "
                            "(optional, defaults to literature/papers.json)"
                        ),
                    },
                },
            },
        ),
        Tool(
            name="save_file",
            description="Write content to a file in the research project",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative file path from project root",
                    },
                    "content": {"type": "string", "description": "Content to write"},
                    "append": {
                        "type": "boolean",
                        "description": "Append to file instead of overwriting",
                        "default": False,
                    },
                },
                "required": ["path", "content"],
            },
        ),
        Tool(
            name="add_citation",
            description="Add a BibTeX citation to references.bib",
            inputSchema={
                "type": "object",
                "properties": {
                    "bibtex": {
                        "type": "string",
                        "description": "BibTeX entry to add",
                    },
                },
                "required": ["bibtex"],
            },
        ),
        Tool(
            name="get_citations",
            description="Get all citations from references.bib",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_project_status",
            description="Get comprehensive project status and statistics",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="init_project",
            description="Initialize a new research project with standard structure",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "Name of the project (optional, defaults to directory name)",
                    },
                },
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Execute a tool by name with given arguments."""
    services = get_services()

    try:
        if name == "search_papers":
            service = services["semantic_scholar"]
            results = await service.search(
                query=arguments["query"],
                limit=arguments.get("limit", 20),
                year_start=arguments.get("year_start"),
                year_end=arguments.get("year_end"),
                fields_of_study=arguments.get("fields_of_study"),
            )
            return [TextContent(type="text", text=json.dumps(results, indent=2))]

        elif name == "get_paper":
            service = services["semantic_scholar"]
            paper = await service.get_paper(arguments["paper_id"])
            return [TextContent(type="text", text=json.dumps(paper, indent=2))]

        elif name == "get_context":
            service = services["context_manager"]
            contents, missing = service.read_files(arguments["paths"])
            result = {"contents": contents, "missing": missing}
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "query_similar_papers":
            service = services["rag_service"]
            if not service.is_indexed():
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(
                            {
                                "error": "Papers not indexed. Run index_papers first.",
                            }
                        ),
                    )
                ]
            results = service.query(
                arguments["query"],
                k=arguments.get("k", 5),
            )
            return [TextContent(type="text", text=json.dumps(results, indent=2))]

        elif name == "index_papers":
            service = services["rag_service"]
            papers_path = arguments.get("papers_path", "literature/papers.json")
            papers_file = get_project_root() / papers_path

            if not papers_file.exists():
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(
                            {"error": f"Papers file not found: {papers_path}"}
                        ),
                    )
                ]

            with open(papers_file, encoding="utf-8") as f:
                papers = json.load(f)

            service.index_papers(papers)
            return [
                TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "success": True,
                            "indexed_count": len(papers),
                        }
                    ),
                )
            ]

        elif name == "save_file":
            service = services["context_manager"]
            bytes_written = service.write_file(
                arguments["path"],
                arguments["content"],
                append=arguments.get("append", False),
            )
            return [
                TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "success": True,
                            "path": arguments["path"],
                            "bytes_written": bytes_written,
                        }
                    ),
                )
            ]

        elif name == "add_citation":
            service = services["citation_manager"]
            key, was_added = service.add_entry(arguments["bibtex"])
            return [
                TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "key": key,
                            "added": was_added,
                            "message": (
                                f"Citation '{key}' added"
                                if was_added
                                else f"Citation '{key}' already exists"
                            ),
                        }
                    ),
                )
            ]

        elif name == "get_citations":
            service = services["citation_manager"]
            citations = service.get_all_entries()
            return [TextContent(type="text", text=json.dumps(citations, indent=2))]

        elif name == "get_project_status":
            service = services["context_manager"]
            status = service.get_status()
            return [TextContent(type="text", text=json.dumps(status, indent=2))]

        elif name == "init_project":
            service = services["project_initializer"]
            result = service.initialize(arguments.get("project_name"))
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        else:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({"error": f"Unknown tool: {name}"}),
                )
            ]

    except Exception as e:
        return [
            TextContent(
                type="text",
                text=json.dumps(
                    {
                        "error": f"Tool execution failed: {str(e)}",
                        "tool": name,
                    }
                ),
            )
        ]


async def serve() -> None:
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


def main() -> None:
    """Entry point for the MCP server."""
    asyncio.run(serve())


if __name__ == "__main__":
    main()
