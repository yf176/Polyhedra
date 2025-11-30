# Polyhedra - Product Requirements Document

## Document Control

| Field | Value |
|-------|-------|
| **Project Name** | Polyhedra |
| **Version** | 2.0.0 |
| **Type** | MCP Tool Server |
| **Status** | Ready for Development |
| **Created** | November 26, 2024 |
| **Last Updated** | November 29, 2025 |
| **Author** | Product Team |
| **Stakeholders** | Engineering, Research Community |

### Revision History

| Version | Date | Author | Changes |
|---------|------|--------|----------|
| 2.0.0 | 2024-11-26 | Product Team | BREAKING: Removed internal LLM calls, simplified to pure MCP tool server |
| 1.x | - | Product Team | Legacy versions with built-in LLM agents |

---

## Executive Summary

### Purpose

Polyhedra is a pure Model Context Protocol (MCP) tool server designed to augment IDE-based AI assistants (Cursor, GitHub Copilot, Windsurf, VS Code) with academic research capabilities. Unlike traditional research tools, Polyhedra does not call LLMs directly—all content generation is handled by the IDE's native AI, while Polyhedra provides specialized research tools and data access.

### Key Capabilities

- **Paper Discovery**: Search and retrieve academic papers via Semantic Scholar API
- **Citation Management**: Automated BibTeX generation and reference management
- **RAG Retrieval**: Semantic search across indexed papers for relevant citations
- **Context Management**: Read/write project files for research workflow
- **Project Scaffolding**: Initialize standardized research project structures

### Target Audience

- ML/AI researchers using modern IDEs with AI assistants
- PhD students requiring streamlined research workflows
- Academic professionals seeking IDE-integrated paper management

### Success Criteria

- Sub-2-second paper search response time
- 100% valid BibTeX generation
- Support for 4+ major IDEs (Cursor, Copilot, Windsurf, VS Code)
- Setup time under 5 minutes

---

## 1. Product Overview

### 1.1 Vision

Polyhedra is a **pure MCP tool server** that extends IDE AI assistants (Cursor, GitHub Copilot, Windsurf, VS Code) with academic research capabilities.

**Polyhedra does NOT call LLMs** — all generation capabilities come from the IDE's AI.

### 1.2 Architecture Philosophy

```
┌─────────────────────────────────────────────────────────┐
│                  IDE (Cursor / Copilot)                 │
│  ┌───────────────────────────────────────────────────┐  │
│  │              IDE's LLM (Claude/GPT)               │  │
│  │  • Intent understanding                           │  │
│  │  • Literature review generation                   │  │
│  │  • Paper writing                                  │  │
│  │  • Hypothesis generation                          │  │
│  └─────────────────────┬─────────────────────────────┘  │
│                        │ MCP Protocol                    │
│  ┌─────────────────────▼─────────────────────────────┐  │
│  │            Polyhedra MCP Server                   │  │
│  │  • Paper search (Semantic Scholar API)            │  │
│  │  • Context management (project files)             │  │
│  │  • RAG retrieval (relevant papers)                │  │
│  │  • Citation management (BibTeX)                   │  │
│  │  • File read/write                                │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 1.3 What Polyhedra Does vs What IDE Does

| Capability | Polyhedra (MCP) | IDE (LLM) |
|------------|-----------------|-----------|
| Search academic papers | ✓ | |
| Fetch paper metadata & BibTeX | ✓ | |
| Read project files | ✓ | |
| Write/save files | ✓ | |
| RAG retrieval | ✓ | |
| Manage citations | ✓ | |
| Understand user intent | | ✓ |
| Generate literature review | | ✓ |
| Generate hypotheses | | ✓ |
| Write paper sections | | ✓ |
| Decide workflow | | ✓ |

### 1.4 Target Users

- ML/AI researchers using Cursor, Copilot, or Windsurf
- PhD students who want AI-assisted research workflow
- Anyone who wants academic paper tools in their IDE

### 1.5 Tech Stack

```yaml
language: Python 3.11+
mcp_framework: mcp (official SDK)
http_client: httpx
data_validation: Pydantic
bibtex_parser: bibtexparser
embeddings: sentence-transformers
vector_store: numpy (simple cosine similarity)
package_manager: uv

supported_ides:
  - Cursor
  - GitHub Copilot
  - Windsurf
  - VS Code (with MCP extension)
```

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     MCP Server                          │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │                 Tool Layer                       │   │
│  │  search_papers | get_paper | get_context        │   │
│  │  query_similar | save_file | manage_citations   │   │
│  └─────────────────────┬───────────────────────────┘   │
│                        │                                │
│  ┌─────────────────────▼───────────────────────────┐   │
│  │               Service Layer                      │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │   │
│  │  │  Papers  │ │ Context  │ │ Citations│        │   │
│  │  │ Service  │ │ Service  │ │ Service  │        │   │
│  │  └──────────┘ └──────────┘ └──────────┘        │   │
│  │  ┌──────────┐ ┌──────────┐                     │   │
│  │  │   RAG    │ │   File   │                     │   │
│  │  │ Service  │ │ Service  │                     │   │
│  │  └──────────┘ └──────────┘                     │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Directory Structure

```
polyhedra/
├── pyproject.toml
├── README.md
├── src/
│   └── polyhedra/
│       ├── __init__.py
│       ├── server.py              # MCP server entry point
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── papers.py          # search_papers, get_paper
│       │   ├── context.py         # get_context, get_project_status
│       │   ├── retrieval.py       # query_similar_papers
│       │   ├── citations.py       # add_citation, get_citations
│       │   └── files.py           # save_file, read_file
│       ├── services/
│       │   ├── __init__.py
│       │   ├── semantic_scholar.py
│       │   ├── context_manager.py
│       │   ├── citation_manager.py
│       │   ├── rag_service.py
│       │   └── file_service.py
│       └── schemas/
│           ├── __init__.py
│           ├── paper.py
│           └── project.py
└── tests/
    ├── test_tools/
    └── test_services/
```

### 2.3 Project Output Structure

When used in a research project:

```
my-research/
├── .poly/
│   ├── config.yaml          # Project configuration
│   └── embeddings/          # Cached paper embeddings
│       └── papers.pkl
├── literature/
│   ├── papers.json          # Paper metadata (structured)
│   ├── review.md            # Generated by IDE's LLM
│   └── gaps.md              # Generated by IDE's LLM
├── ideas/
│   └── hypotheses.md        # Generated by IDE's LLM
├── method/
│   └── design.md            # Generated by IDE's LLM
├── paper/
│   ├── abstract.md
│   ├── introduction.md
│   └── ...                  # All generated by IDE's LLM
├── references.bib           # Managed by Polyhedra
└── .cursorrules             # IDE prompts for research workflow
```

---

## 3. MCP Tools Specification

### 3.1 Tool: `search_papers`

Search academic papers via Semantic Scholar.

```yaml
name: search_papers
description: |
  Search for academic papers on Semantic Scholar. 
  Returns paper metadata including title, authors, abstract, 
  citations, and BibTeX entry.

input_schema:
  type: object
  properties:
    query:
      type: string
      description: Search query (topic, keywords, or paper title)
    limit:
      type: integer
      default: 20
      description: Maximum number of papers to return (max 100)
    year_start:
      type: integer
      description: Filter papers from this year onwards
    year_end:
      type: integer
      description: Filter papers until this year
    fields_of_study:
      type: array
      items:
        type: string
      description: Filter by fields (e.g., "Computer Science", "Medicine")
  required: [query]

output_schema:
  type: object
  properties:
    papers:
      type: array
      items:
        $ref: "#/schemas/Paper"
    total_results:
      type: integer
    query_used:
      type: string
```

### 3.2 Tool: `get_paper`

Get detailed information for a specific paper.

```yaml
name: get_paper
description: |
  Get detailed information about a specific paper by its ID.
  Returns full metadata, abstract, BibTeX, and citation context.

input_schema:
  type: object
  properties:
    paper_id:
      type: string
      description: Semantic Scholar paper ID or DOI or ArXiv ID
  required: [paper_id]

output_schema:
  type: object
  properties:
    paper:
      $ref: "#/schemas/Paper"
    references:
      type: array
      description: Papers this paper cites
    citations:
      type: array
      description: Papers that cite this paper
```

### 3.3 Tool: `get_context`

Read project files for context.

```yaml
name: get_context
description: |
  Read one or more project files to provide context for generation.
  Use this before writing paper sections to get relevant background.

input_schema:
  type: object
  properties:
    files:
      type: array
      items:
        type: string
      description: |
        File paths relative to project root.
        Common paths: literature/papers.json, literature/review.md,
        ideas/hypotheses.md, method/design.md
    include_papers:
      type: boolean
      default: false
      description: If true, include full paper metadata from papers.json
  required: [files]

output_schema:
  type: object
  properties:
    contents:
      type: object
      description: Map of filename to file content
    missing_files:
      type: array
      description: Files that were requested but don't exist
```

### 3.4 Tool: `query_similar_papers`

RAG retrieval for relevant papers.

```yaml
name: query_similar_papers
description: |
  Find papers most relevant to a query using semantic similarity.
  Useful when writing sections that need specific citations.
  Papers must first be indexed via index_papers.

input_schema:
  type: object
  properties:
    query:
      type: string
      description: Natural language query describing what you need
    k:
      type: integer
      default: 5
      description: Number of papers to return
  required: [query]

output_schema:
  type: object
  properties:
    papers:
      type: array
      items:
        type: object
        properties:
          paper_id:
            type: string
          title:
            type: string
          abstract:
            type: string
          relevance_score:
            type: number
          bibtex_key:
            type: string
```

### 3.5 Tool: `index_papers`

Index papers for RAG retrieval.

```yaml
name: index_papers
description: |
  Index papers from papers.json for semantic search.
  Call this after search_papers to enable query_similar_papers.

input_schema:
  type: object
  properties:
    papers_file:
      type: string
      default: "literature/papers.json"
      description: Path to papers JSON file
  required: []

output_schema:
  type: object
  properties:
    indexed_count:
      type: integer
    status:
      type: string
```

### 3.6 Tool: `save_file`

Save generated content to project.

```yaml
name: save_file
description: |
  Save content to a file in the project.
  Creates parent directories if they don't exist.

input_schema:
  type: object
  properties:
    path:
      type: string
      description: File path relative to project root
    content:
      type: string
      description: Content to write
    append:
      type: boolean
      default: false
      description: If true, append instead of overwrite
  required: [path, content]

output_schema:
  type: object
  properties:
    success:
      type: boolean
    path:
      type: string
    bytes_written:
      type: integer
```

### 3.7 Tool: `add_citation`

Add a citation to references.bib.

```yaml
name: add_citation
description: |
  Add a BibTeX entry to the project's references.bib file.
  Handles duplicates automatically (skips if key exists).

input_schema:
  type: object
  properties:
    bibtex:
      type: string
      description: BibTeX entry string
    paper_id:
      type: string
      description: |
        Alternative: Semantic Scholar paper ID. 
        Will fetch BibTeX automatically.
  required: []  # One of bibtex or paper_id required

output_schema:
  type: object
  properties:
    key:
      type: string
      description: The BibTeX citation key
    added:
      type: boolean
      description: True if newly added, false if already existed
```

### 3.8 Tool: `get_citations`

List all citations in references.bib.

```yaml
name: get_citations
description: |
  Get all citation keys and entries from references.bib.
  Useful for checking what papers are already cited.

input_schema:
  type: object
  properties:
    keys_only:
      type: boolean
      default: true
      description: If true, return only keys. If false, return full entries.
  required: []

output_schema:
  type: object
  properties:
    citations:
      type: array
      items:
        type: object
        properties:
          key:
            type: string
          title:
            type: string
          authors:
            type: string
          year:
            type: integer
    count:
      type: integer
```

### 3.9 Tool: `get_project_status`

Get current project state.

```yaml
name: get_project_status
description: |
  Get overview of current research project state.
  Shows which files exist and project progress.

input_schema:
  type: object
  properties: {}
  required: []

output_schema:
  type: object
  properties:
    project_root:
      type: string
    existing_files:
      type: array
      items:
        type: string
    paper_count:
      type: integer
    citation_count:
      type: integer
    indexed_for_rag:
      type: boolean
```

### 3.10 Tool: `init_project`

Initialize a new research project.

```yaml
name: init_project
description: |
  Initialize a new research project with standard directory structure.

input_schema:
  type: object
  properties:
    path:
      type: string
      default: "."
      description: Project root path
    name:
      type: string
      description: Project name (used in config)
  required: []

output_schema:
  type: object
  properties:
    created_dirs:
      type: array
    created_files:
      type: array
    project_root:
      type: string
```

---

## 4. Data Schemas

### 4.1 Paper Schema

```python
# schemas/paper.py
from pydantic import BaseModel
from typing import Optional

class Paper(BaseModel):
    id: str                      # Semantic Scholar ID
    title: str
    authors: list[str]
    year: int
    venue: Optional[str]
    abstract: str
    citation_count: int
    bibtex_key: str              # e.g., "vaswani2017attention"
    bibtex_entry: str            # Full BibTeX string
    url: Optional[str]
    pdf_url: Optional[str]
    fields_of_study: list[str]
```

### 4.2 Project Config Schema

```python
# schemas/project.py
from pydantic import BaseModel
from typing import Optional

class ProjectConfig(BaseModel):
    name: str
    created_at: str
    paper_count: int = 0
    indexed: bool = False
```

---

## 5. Service Implementations

### 5.1 Semantic Scholar Service

```python
# services/semantic_scholar.py
import httpx
from typing import Optional

class SemanticScholarService:
    BASE_URL = "https://api.semanticscholar.org/graph/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.client = httpx.AsyncClient(
            headers={"x-api-key": api_key} if api_key else {}
        )
    
    async def search(
        self,
        query: str,
        limit: int = 20,
        year_start: Optional[int] = None,
        year_end: Optional[int] = None,
        fields_of_study: Optional[list[str]] = None
    ) -> list[dict]:
        """Search papers by query"""
        params = {
            "query": query,
            "limit": min(limit, 100),
            "fields": "paperId,title,authors,year,venue,abstract,"
                     "citationCount,fieldsOfStudy,url,openAccessPdf"
        }
        
        if year_start or year_end:
            year_filter = f"{year_start or ''}-{year_end or ''}"
            params["year"] = year_filter
        
        if fields_of_study:
            params["fieldsOfStudy"] = ",".join(fields_of_study)
        
        resp = await self.client.get(
            f"{self.BASE_URL}/paper/search",
            params=params
        )
        resp.raise_for_status()
        return resp.json().get("data", [])
    
    async def get_paper(self, paper_id: str) -> dict:
        """Get paper by ID"""
        resp = await self.client.get(
            f"{self.BASE_URL}/paper/{paper_id}",
            params={
                "fields": "paperId,title,authors,year,venue,abstract,"
                         "citationCount,citations,references,fieldsOfStudy,"
                         "url,openAccessPdf"
            }
        )
        resp.raise_for_status()
        return resp.json()
    
    def generate_bibtex(self, paper: dict) -> tuple[str, str]:
        """Generate BibTeX key and entry for a paper"""
        # Generate key: firstauthorYear
        first_author = paper["authors"][0]["name"].split()[-1].lower()
        year = paper.get("year", "unknown")
        key = f"{first_author}{year}"
        
        # Generate entry
        authors = " and ".join(a["name"] for a in paper["authors"])
        entry = f"""@article{{{key},
  title={{{paper['title']}}},
  author={{{authors}}},
  year={{{year}}},
  venue={{{paper.get('venue', '')}}},
}}"""
        return key, entry
```

### 5.2 Citation Manager Service

```python
# services/citation_manager.py
import bibtexparser
from pathlib import Path
from typing import Optional

class CitationManager:
    def __init__(self, project_root: Path):
        self.bib_path = project_root / "references.bib"
    
    def load(self) -> bibtexparser.Library:
        if self.bib_path.exists():
            return bibtexparser.parse_file(str(self.bib_path))
        return bibtexparser.Library()
    
    def save(self, library: bibtexparser.Library):
        bibtexparser.write_file(str(self.bib_path), library)
    
    def add_entry(self, bibtex_str: str) -> tuple[str, bool]:
        """Add entry, returns (key, was_added)"""
        library = self.load()
        new_entry = bibtexparser.parse_string(bibtex_str).entries[0]
        key = new_entry.key
        
        existing_keys = {e.key for e in library.entries}
        if key in existing_keys:
            return key, False
        
        library.add(new_entry)
        self.save(library)
        return key, True
    
    def get_all_keys(self) -> list[str]:
        library = self.load()
        return [e.key for e in library.entries]
    
    def get_all_entries(self) -> list[dict]:
        library = self.load()
        return [
            {
                "key": e.key,
                "title": e.get("title", ""),
                "authors": e.get("author", ""),
                "year": int(e.get("year", 0)) if e.get("year") else None
            }
            for e in library.entries
        ]
```

### 5.3 RAG Service

```python
# services/rag_service.py
import json
import pickle
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

class RAGService:
    def __init__(
        self, 
        project_root: Path,
        model_name: str = "all-MiniLM-L6-v2"
    ):
        self.project_root = project_root
        self.embeddings_path = project_root / ".poly" / "embeddings" / "papers.pkl"
        self.model = None  # Lazy load
        self.model_name = model_name
        self._index = None
    
    def _load_model(self):
        if self.model is None:
            self.model = SentenceTransformer(self.model_name)
    
    def index_papers(self, papers_file: Path) -> int:
        """Index papers for retrieval"""
        self._load_model()
        
        papers = json.loads(papers_file.read_text())
        
        texts = []
        metadata = []
        
        for paper in papers:
            text = f"{paper['title']}. {paper['abstract']}"
            texts.append(text)
            metadata.append({
                "id": paper["id"],
                "title": paper["title"],
                "abstract": paper["abstract"],
                "bibtex_key": paper.get("bibtex_key", "")
            })
        
        embeddings = self.model.encode(texts, show_progress_bar=False)
        
        self._index = {
            "embeddings": embeddings,
            "metadata": metadata
        }
        
        self.embeddings_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.embeddings_path, "wb") as f:
            pickle.dump(self._index, f)
        
        return len(papers)
    
    def query(self, query: str, k: int = 5) -> list[dict]:
        """Find top-k similar papers"""
        if self._index is None:
            self._load_index()
        
        if self._index is None:
            return []
        
        self._load_model()
        query_emb = self.model.encode([query])[0]
        
        embeddings = self._index["embeddings"]
        similarities = np.dot(embeddings, query_emb) / (
            np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_emb)
        )
        
        top_indices = np.argsort(similarities)[-k:][::-1]
        
        results = []
        for idx in top_indices:
            meta = self._index["metadata"][idx]
            results.append({
                "paper_id": meta["id"],
                "title": meta["title"],
                "abstract": meta["abstract"],
                "bibtex_key": meta["bibtex_key"],
                "relevance_score": float(similarities[idx])
            })
        
        return results
    
    def _load_index(self):
        if self.embeddings_path.exists():
            with open(self.embeddings_path, "rb") as f:
                self._index = pickle.load(f)
    
    def is_indexed(self) -> bool:
        return self.embeddings_path.exists()
```

### 5.4 Context Manager Service

```python
# services/context_manager.py
import json
from pathlib import Path
from typing import Optional

class ContextManager:
    def __init__(self, project_root: Path):
        self.root = project_root
    
    def read_files(self, paths: list[str]) -> tuple[dict, list[str]]:
        """Read multiple files, return contents and missing files"""
        contents = {}
        missing = []
        
        for path in paths:
            full_path = self.root / path
            if full_path.exists():
                contents[path] = full_path.read_text()
            else:
                missing.append(path)
        
        return contents, missing
    
    def write_file(self, path: str, content: str, append: bool = False) -> int:
        """Write content to file, return bytes written"""
        full_path = self.root / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        mode = "a" if append else "w"
        with open(full_path, mode) as f:
            return f.write(content)
    
    def get_status(self) -> dict:
        """Get project status"""
        existing = []
        
        check_paths = [
            "literature/papers.json",
            "literature/review.md",
            "literature/gaps.md",
            "ideas/hypotheses.md",
            "method/design.md",
            "paper/abstract.md",
            "paper/introduction.md",
            "paper/related_work.md",
            "paper/method.md",
            "paper/experiments.md",
            "paper/conclusion.md",
            "references.bib"
        ]
        
        for path in check_paths:
            if (self.root / path).exists():
                existing.append(path)
        
        paper_count = 0
        papers_file = self.root / "literature" / "papers.json"
        if papers_file.exists():
            papers = json.loads(papers_file.read_text())
            paper_count = len(papers)
        
        citation_count = 0
        bib_file = self.root / "references.bib"
        if bib_file.exists():
            import bibtexparser
            lib = bibtexparser.parse_file(str(bib_file))
            citation_count = len(lib.entries)
        
        indexed = (self.root / ".poly" / "embeddings" / "papers.pkl").exists()
        
        return {
            "project_root": str(self.root),
            "existing_files": existing,
            "paper_count": paper_count,
            "citation_count": citation_count,
            "indexed_for_rag": indexed
        }
    
    def init_project(self, name: Optional[str] = None) -> dict:
        """Initialize project structure"""
        dirs = [
            "literature",
            "ideas", 
            "method",
            "paper",
            ".poly/embeddings"
        ]
        
        created_dirs = []
        for d in dirs:
            path = self.root / d
            if not path.exists():
                path.mkdir(parents=True)
                created_dirs.append(d)
        
        created_files = []
        
        # Create empty references.bib
        bib_path = self.root / "references.bib"
        if not bib_path.exists():
            bib_path.write_text("")
            created_files.append("references.bib")
        
        # Create config
        config_path = self.root / ".poly" / "config.yaml"
        if not config_path.exists():
            import yaml
            from datetime import datetime
            config = {
                "name": name or self.root.name,
                "created_at": datetime.now().isoformat(),
                "paper_count": 0,
                "indexed": False
            }
            config_path.write_text(yaml.dump(config))
            created_files.append(".poly/config.yaml")
        
        return {
            "created_dirs": created_dirs,
            "created_files": created_files,
            "project_root": str(self.root)
        }
```

---

## 6. MCP Server Implementation

### 6.1 Server Entry Point

```python
# server.py
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pathlib import Path
import json

from polyhedra.services.semantic_scholar import SemanticScholarService
from polyhedra.services.citation_manager import CitationManager
from polyhedra.services.rag_service import RAGService
from polyhedra.services.context_manager import ContextManager

# Initialize server
server = Server("polyhedra")

# Services (initialized per project root)
_project_root: Path = Path.cwd()
_papers_service = SemanticScholarService()
_citation_manager: CitationManager = None
_rag_service: RAGService = None
_context_manager: ContextManager = None

def _init_services(project_root: Path = None):
    global _project_root, _citation_manager, _rag_service, _context_manager
    _project_root = project_root or Path.cwd()
    _citation_manager = CitationManager(_project_root)
    _rag_service = RAGService(_project_root)
    _context_manager = ContextManager(_project_root)

_init_services()

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_papers",
            description="Search academic papers on Semantic Scholar",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "limit": {"type": "integer", "default": 20},
                    "year_start": {"type": "integer"},
                    "year_end": {"type": "integer"}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_paper",
            description="Get detailed paper information by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "paper_id": {"type": "string"}
                },
                "required": ["paper_id"]
            }
        ),
        Tool(
            name="get_context",
            description="Read project files for context",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["files"]
            }
        ),
        Tool(
            name="query_similar_papers",
            description="Find similar papers using semantic search",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "k": {"type": "integer", "default": 5}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="index_papers",
            description="Index papers for semantic search",
            inputSchema={
                "type": "object",
                "properties": {
                    "papers_file": {"type": "string", "default": "literature/papers.json"}
                }
            }
        ),
        Tool(
            name="save_file",
            description="Save content to project file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                    "append": {"type": "boolean", "default": False}
                },
                "required": ["path", "content"]
            }
        ),
        Tool(
            name="add_citation",
            description="Add BibTeX citation to references.bib",
            inputSchema={
                "type": "object",
                "properties": {
                    "bibtex": {"type": "string"},
                    "paper_id": {"type": "string"}
                }
            }
        ),
        Tool(
            name="get_citations",
            description="List all citations in references.bib",
            inputSchema={
                "type": "object",
                "properties": {
                    "keys_only": {"type": "boolean", "default": True}
                }
            }
        ),
        Tool(
            name="get_project_status",
            description="Get current project status",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="init_project",
            description="Initialize research project structure",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    
    if name == "search_papers":
        papers = await _papers_service.search(
            query=arguments["query"],
            limit=arguments.get("limit", 20),
            year_start=arguments.get("year_start"),
            year_end=arguments.get("year_end")
        )
        
        # Add BibTeX to each paper
        results = []
        for p in papers:
            key, entry = _papers_service.generate_bibtex(p)
            results.append({
                "id": p["paperId"],
                "title": p["title"],
                "authors": [a["name"] for a in p.get("authors", [])],
                "year": p.get("year"),
                "venue": p.get("venue"),
                "abstract": p.get("abstract", ""),
                "citation_count": p.get("citationCount", 0),
                "bibtex_key": key,
                "bibtex_entry": entry
            })
        
        # Auto-save to papers.json
        papers_path = _project_root / "literature" / "papers.json"
        papers_path.parent.mkdir(parents=True, exist_ok=True)
        papers_path.write_text(json.dumps(results, indent=2))
        
        return [TextContent(
            type="text",
            text=json.dumps({
                "papers": results,
                "total_results": len(results),
                "saved_to": "literature/papers.json"
            }, indent=2)
        )]
    
    elif name == "get_paper":
        paper = await _papers_service.get_paper(arguments["paper_id"])
        key, entry = _papers_service.generate_bibtex(paper)
        
        result = {
            "paper": {
                "id": paper["paperId"],
                "title": paper["title"],
                "authors": [a["name"] for a in paper.get("authors", [])],
                "year": paper.get("year"),
                "abstract": paper.get("abstract", ""),
                "bibtex_key": key,
                "bibtex_entry": entry
            },
            "references": len(paper.get("references", [])),
            "citations": len(paper.get("citations", []))
        }
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "get_context":
        contents, missing = _context_manager.read_files(arguments["files"])
        return [TextContent(
            type="text",
            text=json.dumps({
                "contents": contents,
                "missing_files": missing
            }, indent=2)
        )]
    
    elif name == "query_similar_papers":
        results = _rag_service.query(
            arguments["query"],
            k=arguments.get("k", 5)
        )
        return [TextContent(type="text", text=json.dumps({"papers": results}, indent=2))]
    
    elif name == "index_papers":
        papers_file = _project_root / arguments.get("papers_file", "literature/papers.json")
        count = _rag_service.index_papers(papers_file)
        return [TextContent(
            type="text",
            text=json.dumps({"indexed_count": count, "status": "success"})
        )]
    
    elif name == "save_file":
        bytes_written = _context_manager.write_file(
            arguments["path"],
            arguments["content"],
            append=arguments.get("append", False)
        )
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": True,
                "path": arguments["path"],
                "bytes_written": bytes_written
            })
        )]
    
    elif name == "add_citation":
        if arguments.get("bibtex"):
            key, added = _citation_manager.add_entry(arguments["bibtex"])
        elif arguments.get("paper_id"):
            paper = await _papers_service.get_paper(arguments["paper_id"])
            _, entry = _papers_service.generate_bibtex(paper)
            key, added = _citation_manager.add_entry(entry)
        else:
            return [TextContent(type="text", text='{"error": "Provide bibtex or paper_id"}')]
        
        return [TextContent(
            type="text",
            text=json.dumps({"key": key, "added": added})
        )]
    
    elif name == "get_citations":
        if arguments.get("keys_only", True):
            keys = _citation_manager.get_all_keys()
            return [TextContent(
                type="text",
                text=json.dumps({"citations": keys, "count": len(keys)})
            )]
        else:
            entries = _citation_manager.get_all_entries()
            return [TextContent(
                type="text",
                text=json.dumps({"citations": entries, "count": len(entries)})
            )]
    
    elif name == "get_project_status":
        status = _context_manager.get_status()
        return [TextContent(type="text", text=json.dumps(status, indent=2))]
    
    elif name == "init_project":
        result = _context_manager.init_project(arguments.get("name"))
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

---

## 7. IDE Integration

### 7.1 Configuration Files

**Cursor** (`.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "polyhedra": {
      "command": "python",
      "args": ["-m", "polyhedra.server"],
      "env": {}
    }
  }
}
```

**VS Code / GitHub Copilot** (`settings.json`):
```json
{
  "mcp": {
    "servers": {
      "polyhedra": {
        "command": "python",
        "args": ["-m", "polyhedra.server"]
      }
    }
  }
}
```

**Windsurf** (`.windsurf/mcp.json`):
```json
{
  "mcpServers": {
    "polyhedra": {
      "command": "python",
      "args": ["-m", "polyhedra.server"]
    }
  }
}
```

### 7.2 IDE Prompt Instructions

Create `.cursorrules` or `.github/copilot-instructions.md`:

```markdown
# Research Project Instructions

This is an academic research project. Use Polyhedra MCP tools for research tasks.

## Workflow

### 1. Literature Search
When asked to find papers or do a literature review:
1. Use `search_papers` to find relevant papers
2. Use `index_papers` to enable semantic search
3. Use `get_context` to read papers.json
4. Generate a literature review and save with `save_file` to literature/review.md
5. For each cited paper, use `add_citation` to update references.bib

### 2. Writing Paper Sections
When writing paper sections:
1. Use `get_context` to load relevant files (review.md, hypotheses.md, etc.)
2. Use `query_similar_papers` to find papers to cite
3. Generate content with proper citations (\cite{key} format)
4. Use `save_file` to save the section
5. Use `add_citation` for any new citations

### 3. Citation Format
- Always use \cite{bibtex_key} or [@bibtex_key] format
- Check existing citations with `get_citations` before adding
- Only cite papers from papers.json

### 4. Project Status
Use `get_project_status` to see what files exist and progress.

## File Locations
- Literature review: literature/review.md
- Paper metadata: literature/papers.json
- Research gaps: literature/gaps.md
- Hypotheses: ideas/hypotheses.md
- Method design: method/design.md
- Paper sections: paper/{section}.md
- Citations: references.bib
```

---

## 8. Functional Requirements

### Requirements Summary Table

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-001 | Paper Search | P0 | Not Started |
| FR-002 | RAG Retrieval | P0 | Not Started |
| FR-003 | Citation Management | P0 | Not Started |
| FR-004 | Context Management | P0 | Not Started |
| FR-005 | Project Initialization | P1 | Not Started |
| NFR-001 | Performance | P0 | Not Started |
| NFR-002 | Reliability | P0 | Not Started |
| NFR-003 | Compatibility | P0 | Not Started |

### FR-001: Paper Search

**Priority**: P0 (Critical)  
**Status**: Not Started

**Description**  
Search Semantic Scholar API and return structured paper data with automatically generated BibTeX entries.

**Acceptance Criteria**
- Returns papers with all required fields (title, authors, abstract, year, venue, citation count)
- Auto-generates BibTeX key using format: `firstauthor+year`
- Auto-generates valid BibTeX entry
- Saves results to `literature/papers.json`
- Handles API rate limiting gracefully with retry logic
- Returns up to 100 results per query

**Dependencies**: Semantic Scholar API access

---

### FR-002: RAG Retrieval

**Priority**: P0 (Critical)  
**Status**: Not Started

**Description**  
Index papers locally and enable semantic similarity search for finding relevant citations during writing.

**Acceptance Criteria**
- Indexes paper titles and abstracts using sentence transformers
- Returns top-k most similar papers to a natural language query
- Includes relevance scores (cosine similarity)
- Cached embeddings persist across sessions in `.poly/embeddings/`
- Supports re-indexing when papers.json is updated

**Dependencies**: sentence-transformers, numpy

---

### FR-003: Citation Management

**Priority**: P0 (Critical)  
**Status**: Not Started

**Description**  
Manage project's `references.bib` file with automatic deduplication and BibTeX validation.

**Acceptance Criteria**
- Add new citations without duplicates (check by key)
- Fetch BibTeX by Semantic Scholar paper ID
- List all citation keys
- List all citation entries with metadata
- Generate 100% valid BibTeX format
- Support manual BibTeX entry addition

**Dependencies**: bibtexparser

---

### FR-004: Context Management

**Priority**: P0 (Critical)  
**Status**: Not Started

**Description**  
Read and write project files to provide context to IDE's LLM for content generation.

**Acceptance Criteria**
- Read multiple files in one call
- Report missing files (don't fail silently)
- Create parent directories automatically on write
- Support append mode for incremental updates
- Return file contents as structured JSON
- Handle encoding issues gracefully

**Dependencies**: None (standard library)

---

### FR-005: Project Initialization

**Priority**: P1 (High)  
**Status**: Not Started

**Description**  
Initialize a new research project with standardized directory structure and configuration files.

**Acceptance Criteria**
- Creates standard directories: `literature/`, `ideas/`, `method/`, `paper/`, `.poly/embeddings/`
- Creates empty `references.bib`
- Creates `.poly/config.yaml` with project metadata
- Idempotent (safe to run multiple times)
- Returns list of created directories and files

**Dependencies**: None (standard library)

---

### NFR-001: Performance

**Priority**: P0 (Critical)  
**Status**: Not Started

**Description**  
Ensure responsive tool execution to maintain IDE assistant responsiveness.

**Acceptance Criteria**
- Paper search: < 2 seconds (including API call)
- Local file operations: < 100ms
- RAG indexing: < 5 seconds for 100 papers
- RAG query: < 500ms
- Citation operations: < 50ms

---

### NFR-002: Reliability

**Priority**: P0 (Critical)  
**Status**: Not Started

**Description**  
Handle errors gracefully without crashing or losing data.

**Acceptance Criteria**
- API failures return informative error messages
- Network timeouts handled with retry logic
- File I/O errors reported clearly
- Invalid BibTeX rejected with validation errors
- No data corruption on concurrent access

---

### NFR-003: IDE Compatibility

**Priority**: P0 (Critical)  
**Status**: Not Started

**Description**  
Support major IDEs with MCP protocol compatibility.

**Acceptance Criteria**
- Works with Cursor IDE
- Works with GitHub Copilot (VS Code)
- Works with Windsurf
- Works with VS Code + MCP extension
- Provides configuration templates for each IDE

---

## 9. Development Tasks

### Phase 1: Core Services (Week 1)

```yaml
tasks:
  - id: T-001
    name: Project setup
    description: |
      - pyproject.toml with dependencies
      - src layout
      - Basic tests structure
    estimate: 2h
    
  - id: T-002
    name: Semantic Scholar service
    description: |
      - Search endpoint
      - Get paper endpoint
      - BibTeX generation
      - Rate limiting
    estimate: 4h
    depends_on: [T-001]
    
  - id: T-003
    name: Citation manager service
    description: |
      - BibTeX parsing with bibtexparser
      - Add/get/list operations
      - Deduplication
    estimate: 3h
    depends_on: [T-001]
    
  - id: T-004
    name: RAG service
    description: |
      - Paper indexing
      - Embedding with sentence-transformers
      - Similarity search
      - Caching
    estimate: 4h
    depends_on: [T-001]
    
  - id: T-005
    name: Context manager service
    description: |
      - File read/write
      - Project status
      - Project init
    estimate: 3h
    depends_on: [T-001]
```

### Phase 2: MCP Server (Week 2)

```yaml
tasks:
  - id: T-006
    name: MCP server implementation
    description: |
      - Server setup with mcp SDK
      - All 10 tools implemented
      - Tool schemas
    estimate: 6h
    depends_on: [T-002, T-003, T-004, T-005]
    
  - id: T-007
    name: IDE configuration files
    description: |
      - .cursor/mcp.json template
      - .vscode settings template
      - .cursorrules template
    estimate: 2h
    depends_on: [T-006]
    
  - id: T-008
    name: Integration testing
    description: |
      - Test with Cursor
      - Test with Copilot
      - End-to-end workflow
    estimate: 4h
    depends_on: [T-006, T-007]
```

### Phase 3: Polish (Week 3)

```yaml
tasks:
  - id: T-009
    name: Error handling
    description: |
      - API errors
      - File not found
      - Invalid inputs
    estimate: 3h
    depends_on: [T-006]
    
  - id: T-010
    name: Documentation
    description: |
      - README with setup instructions
      - Tool documentation
      - Example workflows
    estimate: 3h
    depends_on: [T-008]
    
  - id: T-011
    name: Package and publish
    description: |
      - PyPI setup
      - Installation instructions
    estimate: 2h
    depends_on: [T-010]
```

**Total: ~3 weeks** (down from 8 weeks in v1.x)

---

## 10. Testing Strategy

### Unit Tests

```python
# tests/test_services/test_citation_manager.py

def test_add_citation():
    mgr = CitationManager(tmp_path)
    bibtex = "@article{test2023, title={Test Paper}}"
    
    key, added = mgr.add_entry(bibtex)
    
    assert key == "test2023"
    assert added == True

def test_no_duplicate_citations():
    mgr = CitationManager(tmp_path)
    bibtex = "@article{test2023, title={Test}}"
    
    mgr.add_entry(bibtex)
    key, added = mgr.add_entry(bibtex)
    
    assert added == False
    assert len(mgr.get_all_keys()) == 1
```

### Integration Tests

```python
# tests/test_integration.py

async def test_search_and_index_workflow():
    # 1. Search papers
    result = await call_tool("search_papers", {"query": "transformers", "limit": 5})
    papers = json.loads(result[0].text)["papers"]
    assert len(papers) == 5
    
    # 2. Index papers
    result = await call_tool("index_papers", {})
    assert json.loads(result[0].text)["status"] == "success"
    
    # 3. Query similar
    result = await call_tool("query_similar_papers", {"query": "attention mechanism", "k": 3})
    similar = json.loads(result[0].text)["papers"]
    assert len(similar) == 3
```

---

## 11. Success Metrics

### Performance Metrics

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| Paper Search Response Time | < 2 seconds | Average response time over 100 queries |
| Local Operations | < 100ms | File read/write, citation operations |
| RAG Indexing | < 5 seconds per 100 papers | Benchmark with standard paper set |
| RAG Query | < 500ms | Average query time |

### Quality Metrics

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| Search Result Relevance | Relevant papers in top 10 | Manual evaluation by researchers |
| Citation Accuracy | 100% valid BibTeX | Automated validation with LaTeX |
| BibTeX Deduplication | 0 duplicate keys | Automated testing |

### Compatibility Metrics

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| IDE Support | 4+ IDEs supported | Integration testing |
| Setup Time | < 5 minutes | Timed user testing from install to first search |
| Documentation Completeness | 100% API coverage | Documentation review |

### Adoption Metrics (Post-Launch)

| Metric | Target (3 months) | Measurement Method |
|--------|-------------------|--------------------|
| Active Users | 100+ | Telemetry (opt-in) |
| Papers Searched | 10,000+ | Usage statistics |
| Projects Initialized | 50+ | Project creation count |

---

## Appendix A: Example IDE Conversation

```
User: Search for papers about efficient vision transformers

Copilot: I'll search for papers on efficient vision transformers.

[Calls search_papers with query="efficient vision transformers"]

Found 20 papers. Here are the top results:

1. **EfficientViT: Memory Efficient Vision Transformer** (liu2023)
   - Citations: 245
   - Year: 2023

2. **MobileViT: Light-weight Vision Transformer** (mehta2022)
   - Citations: 890
   - Year: 2022

...

Papers saved to literature/papers.json. Would you like me to:
1. Generate a literature review
2. Index papers for semantic search
3. Look at a specific paper

User: Generate a literature review and save it

Copilot: I'll read the papers and generate a review.

[Calls get_context with files=["literature/papers.json"]]
[Calls index_papers]

# Literature Review: Efficient Vision Transformers

## Overview
Vision Transformers (ViTs) have achieved remarkable success...

## Taxonomy of Approaches
### 1. Architecture Modifications
...

[Calls save_file with path="literature/review.md"]
[Calls add_citation for each cited paper]

✓ Saved literature review to literature/review.md
✓ Added 12 citations to references.bib
```

---

## Appendix B: Comparison with v1.x

| Aspect | v1.x (Agent-based) | v2.0 (Pure MCP) |
|--------|-------------------|-----------------|
| LLM calls | Internal | IDE handles |
| Complexity | High | Low |
| Dependencies | Many (LLM SDKs) | Few |
| Development time | 8 weeks | 3 weeks |
| Cost | User pays API | IDE subscription |
| Flexibility | Fixed prompts | IDE customizable |
| Maintenance | Prompt updates | Minimal |
