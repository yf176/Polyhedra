# Architecture Documentation

System design and implementation details for Polyhedra MCP Server.

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Component Design](#component-design)
4. [Data Flow](#data-flow)
5. [Technology Stack](#technology-stack)
6. [Integration Points](#integration-points)
7. [Performance Considerations](#performance-considerations)
8. [Security & Privacy](#security--privacy)

---

## Overview

Polyhedra is an MCP (Model Context Protocol) server that extends IDE AI assistants with academic research capabilities. It follows a service-oriented architecture with clean separation of concerns.

### Design Principles

1. **Simplicity**: Pure tool server, no UI components
2. **Composability**: Services can be used independently or combined
3. **Reliability**: Comprehensive error handling and graceful degradation
4. **Performance**: Caching, batching, and async operations
5. **Testability**: 100% test coverage, dependency injection

### Architecture Patterns

- **Service Layer Pattern**: Business logic in dedicated services
- **Repository Pattern**: Data access abstracted behind interfaces
- **Strategy Pattern**: Pluggable search/retrieval strategies
- **Facade Pattern**: MCP server provides unified interface

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        IDE (Cursor, VS Code, etc.)           │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            AI Assistant (Claude, GPT-4, etc.)         │  │
│  └────────────────────┬─────────────────────────────────┘  │
└────────────────────────┼─────────────────────────────────────┘
                         │
                         │ MCP Protocol (JSON-RPC over stdio)
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                  Polyhedra MCP Server                         │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                 Server (server.py)                     │  │
│  │  • Tool registration                                   │  │
│  │  • Request routing                                     │  │
│  │  • Error handling                                      │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                       │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │              Service Layer                            │  │
│  │                                                       │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │  │
│  │  │   Semantic   │  │   Citation   │  │   File     │ │  │
│  │  │   Scholar    │  │  Management  │  │  Context   │ │  │
│  │  │   Service    │  │   Service    │  │  Service   │ │  │
│  │  └──────────────┘  └──────────────┘  └────────────┘ │  │
│  │                                                       │  │
│  │  ┌──────────────┐  ┌──────────────┐                 │  │
│  │  │    RAG       │  │   Project    │                 │  │
│  │  │  Retrieval   │  │ Initializer  │                 │  │
│  │  │   Service    │  │   Service    │                 │  │
│  │  └──────────────┘  └──────────────┘                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              External Dependencies                     │  │
│  │                                                       │  │
│  │  • Semantic Scholar API                               │  │
│  │  • sentence-transformers (RAG)                        │  │
│  │  • FAISS (vector indexing)                            │  │
│  │  • bibtexparser (citations)                           │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
                         │
                         │ File System
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                   Research Project                            │
│                                                              │
│  .polyhedra/               papers/                           │
│  ├── embeddings.index     ├── paper1.pdf                     │
│  ├── metadata.json        └── paper2.pdf                     │
│  └── cache/                                                  │
│                           notes/                             │
│  references.bib           ├── summary.md                     │
│                           └── ideas.md                       │
│  README.md                                                   │
│                           literature-review/                 │
│                           └── draft.md                       │
└───────────────────────────────────────────────────────────────┘
```

---

## Component Design

### MCP Server (`server.py`)

**Responsibility**: Bridge between IDE and services.

```python
class PolyhedraMCPServer:
    """Main MCP server implementing tool interface."""
    
    def __init__(self):
        self.semantic_scholar = SemanticScholarService()
        self.citation_manager = CitationManager()
        self.file_context = FileContextService()
        self.rag_retrieval = RAGRetrievalService()
        self.project_init = ProjectInitializer()
    
    async def list_tools(self) -> list[Tool]:
        """Register all 10 tools with MCP."""
        
    async def call_tool(self, name: str, arguments: dict) -> list[TextContent]:
        """Route tool calls to appropriate service."""
```

**Key Features**:
- **Tool Registration**: Defines schemas for 10 tools
- **Request Routing**: Maps tool names to service methods
- **Error Wrapping**: Catches exceptions, returns formatted errors
- **Async Support**: Uses asyncio for concurrent operations

**Design Decisions**:
- Single server instance per IDE process
- Stateless tool calls (no session management)
- Services instantiated once and reused

---

### Semantic Scholar Service

**Responsibility**: Paper search and retrieval via Semantic Scholar API.

```python
class SemanticScholarService:
    """Academic paper search via Semantic Scholar API."""
    
    BASE_URL = "https://api.semanticscholar.org/graph/v1"
    
    def __init__(self):
        self.session = requests.Session()
        self.cache = RequestCache()
    
    async def search_papers(
        self, 
        query: str,
        year_range: Optional[str] = None,
        limit: int = 10
    ) -> dict:
        """Search for papers by query."""
    
    async def get_paper(
        self,
        paper_id: str,
        fields: Optional[list[str]] = None
    ) -> dict:
        """Get detailed paper information."""
```

**Features**:
- **Rate Limiting**: Respects 100 req/5min limit
- **Retry Logic**: Exponential backoff on failures
- **Caching**: LRU cache for repeated queries
- **Error Recovery**: Returns cached data on network errors

**API Integration**:
```python
# Search endpoint
GET /paper/search?query={query}&year={year}&limit={limit}

# Details endpoint  
GET /paper/{paper_id}?fields={fields}
```

**Cache Strategy**:
- Search results: 1 hour TTL
- Paper details: 24 hour TTL
- Cache location: `.polyhedra/cache/`

---

### Citation Manager

**Responsibility**: BibTeX bibliography management.

```python
class CitationManager:
    """Manage BibTeX citations in references.bib."""
    
    def __init__(self, bib_file: str = "references.bib"):
        self.bib_file = Path(bib_file)
        self.parser = bibtexparser.bparser.BibTexParser()
    
    def add_citation(self, citation_key: str, bibtex: str) -> dict:
        """Add citation to bibliography."""
    
    def get_citations(self) -> list[dict]:
        """Get all citations from bibliography."""
```

**Features**:
- **Validation**: Checks BibTeX syntax
- **Duplicate Detection**: Prevents duplicate keys
- **Atomic Writes**: Tmp file + rename for safety
- **Parsing**: Converts BibTeX to structured JSON

**File Format**:
```bibtex
@article{vaswani2017attention,
  title={Attention is all you need},
  author={Vaswani, Ashish and ...},
  journal={NeurIPS},
  year={2017}
}
```

**Lock Strategy**:
- File lock for concurrent writes
- 5 second timeout
- Retry with exponential backoff

---

### RAG Retrieval Service

**Responsibility**: Semantic search over collected papers using embeddings.

```python
class RAGRetrievalService:
    """Semantic paper search using sentence transformers."""
    
    MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    def __init__(self):
        self.model = SentenceTransformer(self.MODEL)
        self.index = None
        self.papers = []
    
    async def index_papers(
        self,
        papers: list[dict],
        force_rebuild: bool = False
    ) -> dict:
        """Build FAISS index from papers."""
    
    async def query_similar_papers(
        self,
        query: str,
        limit: int = 10,
        min_similarity: float = 0.7
    ) -> list[dict]:
        """Find similar papers to query."""
```

**Architecture**:

```
Papers → Sentence Transformer → Embeddings (384-dim) → FAISS Index
                                                             ↓
Query → Sentence Transformer → Query Embedding → FAISS Search → Similar Papers
```

**Embedding Model**:
- **Model**: all-MiniLM-L6-v2
- **Dimensions**: 384
- **Size**: ~80MB
- **Speed**: ~1000 sentences/sec on CPU

**Index Structure**:
```python
{
    "embeddings": np.ndarray,  # (N, 384) float32
    "papers": list[dict],       # Paper metadata
    "version": str,             # Index version
    "created_at": datetime      # Build timestamp
}
```

**Similarity Metric**:
- Cosine similarity (dot product of normalized vectors)
- Range: [-1, 1], typical useful range: [0.5, 1.0]

---

### File Context Service

**Responsibility**: Read/write project files safely.

```python
class FileContextService:
    """Manage project file operations."""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()
    
    def save_file(
        self,
        path: str,
        content: str,
        create_dirs: bool = True
    ) -> dict:
        """Write content to file."""
    
    def get_context(
        self,
        paths: list[str]
    ) -> list[dict]:
        """Read content from files."""
```

**Safety Features**:
- **Path Validation**: Prevents directory traversal
- **Atomic Writes**: Tmp file + rename
- **Encoding**: UTF-8 with fallbacks
- **Directory Creation**: Automatic parent dir creation

**Path Resolution**:
```python
# Relative to project root
path = "notes/summary.md"
full_path = project_root / path  # /home/user/project/notes/summary.md

# Absolute paths rejected
path = "/etc/passwd"  # Error: must be relative

# Traversal rejected
path = "../../../etc/passwd"  # Error: outside project
```

---

### Project Initializer

**Responsibility**: Create standardized research project structure.

```python
class ProjectInitializer:
    """Initialize research project structure."""
    
    DIRECTORIES = [
        ".polyhedra",
        "papers",
        "notes",
        "literature-review",
        "data"
    ]
    
    def initialize(
        self,
        project_name: str,
        base_path: Optional[Path] = None
    ) -> dict:
        """Create project structure."""
```

**Created Structure**:
```
project_name/
├── .polyhedra/          # Tool data (index, cache)
├── papers/              # Paper PDFs and metadata
├── notes/               # Research notes
├── literature-review/   # Literature review drafts
├── data/                # Datasets
├── references.bib       # BibTeX bibliography (empty)
└── README.md            # Project overview (template)
```

**Idempotency**:
- Safe to run multiple times
- Only creates missing dirs/files
- Returns report of created vs. existing

---

## Data Flow

### Search Papers Flow

```
User → IDE AI → MCP Request
                    ↓
              [Server: call_tool]
                    ↓
         [SemanticScholarService]
                    ↓
              Check Cache? ──Yes→ Return cached
                    ↓ No
              API Request
                    ↓
         [Semantic Scholar API]
                    ↓
           Parse Response
                    ↓
            Cache Result
                    ↓
         Return to Server
                    ↓
      Format as TextContent
                    ↓
      Return via MCP
                    ↓
           IDE AI → User
```

**Timing**:
- Cache hit: <10ms
- API request: 200-500ms
- With retry: up to 2 seconds

---

### RAG Query Flow

```
User Query → IDE AI → MCP Request
                          ↓
                   [Server: call_tool]
                          ↓
                [RAGRetrievalService]
                          ↓
                  Check Index Exists?
                          ↓ Yes
                 Load Index from Disk
                          ↓
            [Sentence Transformer Model]
                          ↓
              Generate Query Embedding (384-dim)
                          ↓
                   [FAISS Index]
                          ↓
            Search for Similar Embeddings
                          ↓
              Return Top K Papers with Scores
                          ↓
         Filter by min_similarity Threshold
                          ↓
              Format Results with Metadata
                          ↓
                Return via MCP
                          ↓
                   IDE AI → User
```

**Timing**:
- Model load (first time): 2-3 seconds
- Embedding generation: 10-50ms
- FAISS search: 1-5ms
- **Total**: 50-100ms (after first query)

---

### Citation Management Flow

```
User + BibTeX → IDE AI → MCP Request
                              ↓
                       [Server: call_tool]
                              ↓
                     [CitationManager]
                              ↓
                      Acquire File Lock
                              ↓
                    Load references.bib
                              ↓
                      Parse BibTeX
                              ↓
               Check Duplicate Key? ──Yes→ Error
                              ↓ No
                    Validate BibTeX Syntax
                              ↓
                   Append to Bibliography
                              ↓
                Write to Temp File (references.bib.tmp)
                              ↓
            Rename Temp → references.bib (atomic)
                              ↓
                      Release Lock
                              ↓
                   Return Success
                              ↓
                  Return via MCP
                              ↓
                      IDE AI → User
```

**Concurrency**:
- File lock prevents concurrent writes
- Timeout: 5 seconds
- Retry: 3 attempts with backoff

---

## Technology Stack

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `mcp` | 1.0+ | Model Context Protocol SDK |
| `requests` | 2.31+ | HTTP client for API calls |
| `sentence-transformers` | 2.2+ | Embedding model for RAG |
| `faiss-cpu` | 1.7+ | Vector similarity search |
| `bibtexparser` | 1.4+ | BibTeX parsing |
| `aiofiles` | 23.0+ | Async file operations |

### Development Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `pytest` | 8.0+ | Testing framework |
| `pytest-asyncio` | 0.21+ | Async test support |
| `pytest-cov` | 4.1+ | Coverage reporting |
| `ruff` | 0.1+ | Linting and formatting |

### Python Version

- **Minimum**: Python 3.11
- **Recommended**: Python 3.12
- **Reason**: Type hints, asyncio improvements, performance

### External APIs

- **Semantic Scholar API**: v1
  - No authentication required
  - Rate limit: 100 req/5min
  - Documentation: https://api.semanticscholar.org/

---

## Integration Points

### MCP Protocol

**Communication**: JSON-RPC over stdio

**Request Format**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search_papers",
    "arguments": {
      "query": "transformers",
      "limit": 10
    }
  }
}
```

**Response Format**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"papers\": [...]}"
      }
    ]
  }
}
```

**Error Format**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32603,
    "message": "Internal error",
    "data": {
      "details": "Network connection failed"
    }
  }
}
```

---

### IDE Integration

**Supported IDEs**:

1. **Cursor**
   - Config: `~/.cursor/mcp.json`
   - Launch: `uvx --from polyhedra polyhedra`

2. **VS Code + GitHub Copilot**
   - Config: `.vscode/settings.json`
   - Extension: GitHub Copilot Chat
   - MCP support: Via Copilot

3. **Windsurf**
   - Config: `~/.windsurf/mcp.json`
   - Launch: `uvx --from polyhedra polyhedra`

4. **VS Code + MCP Extension**
   - Config: `.vscode/settings.json`
   - Extension: MCP Tools
   - Launch: Direct MCP integration

**Configuration Schema**:
```json
{
  "mcpServers": {
    "polyhedra": {
      "command": "uvx",
      "args": ["--from", "polyhedra", "polyhedra"],
      "env": {
        "POLYHEDRA_PROJECT_ROOT": "/path/to/project"
      }
    }
  }
}
```

---

### File System

**Project Structure Convention**:
```
project-root/
├── .polyhedra/              # Hidden tool directory
│   ├── embeddings.index     # FAISS index (binary)
│   ├── metadata.json        # Index metadata
│   └── cache/               # API response cache
│       ├── search/          # Search results cache
│       └── papers/          # Paper details cache
│
├── papers/                  # Paper storage
│   ├── *.pdf                # Paper PDFs
│   └── *.json               # Paper metadata
│
├── notes/                   # Research notes
│   └── *.md                 # Markdown notes
│
├── literature-review/       # Review drafts
│   └── *.md                 # Markdown sections
│
├── data/                    # Research data
│   └── *.csv, *.json        # Datasets
│
├── references.bib           # BibTeX bibliography
└── README.md                # Project overview
```

**File Permissions**:
- Read: All files in project
- Write: Files in project only (no traversal)
- Create: Directories and files in project

---

## Performance Considerations

### Caching Strategy

**API Response Cache**:
- **Location**: `.polyhedra/cache/`
- **Structure**: `{endpoint}/{hash}.json`
- **TTL**: 1 hour (search), 24 hours (papers)
- **Eviction**: LRU, max 1000 entries

**Embedding Cache**:
- **Location**: `.polyhedra/embeddings.index`
- **Format**: FAISS IndexFlatIP + metadata JSON
- **Update**: Incremental (append new papers)
- **Rebuild**: Manual with `force_rebuild=true`

### Async Operations

**Concurrent API Calls**:
```python
# Batch paper retrieval
papers = await asyncio.gather(*[
    get_paper(paper_id) for paper_id in paper_ids
])
```

**File I/O**:
```python
# Async file reading
async with aiofiles.open(path) as f:
    content = await f.read()
```

### Memory Management

**Embedding Model**:
- Loaded once, kept in memory
- ~150MB RAM
- Lazy loading on first RAG query

**FAISS Index**:
- Loaded on demand
- Memory: ~1.5MB per 1000 papers
- Unloaded after idle timeout (5 minutes)

**Paper Metadata**:
- Stored with index
- ~2KB per paper
- Total: ~2MB for 1000 papers

### Rate Limiting

**Semantic Scholar API**:
```python
class RateLimiter:
    def __init__(self):
        self.requests = deque()
        self.max_requests = 100
        self.window = 300  # 5 minutes
    
    async def acquire(self):
        now = time.time()
        # Remove requests outside window
        while self.requests and self.requests[0] < now - self.window:
            self.requests.popleft()
        
        # Wait if at limit
        if len(self.requests) >= self.max_requests:
            wait = self.requests[0] + self.window - now
            await asyncio.sleep(wait)
        
        self.requests.append(now)
```

### Optimization Tips

1. **Batch Operations**: Use `asyncio.gather()` for concurrent requests
2. **Cache Aggressively**: API responses, embeddings, parsed BibTeX
3. **Lazy Load**: Don't load embedding model until needed
4. **Index Incrementally**: Append to index instead of rebuilding
5. **Limit Results**: Default to 10 results, max 100

---

## Security & Privacy

### Data Privacy

**No Data Transmission**:
- All processing happens locally
- No telemetry or analytics
- No user tracking

**API Calls**:
- Only to Semantic Scholar (public API)
- No authentication tokens stored
- Query data not retained by API

**File Access**:
- Restricted to project directory
- No system file access
- Path traversal prevented

### Input Validation

**Path Validation**:
```python
def validate_path(path: str, project_root: Path) -> Path:
    """Ensure path is within project."""
    full_path = (project_root / path).resolve()
    
    # Check still within project
    if not full_path.is_relative_to(project_root):
        raise ValueError("Path outside project")
    
    return full_path
```

**BibTeX Validation**:
```python
def validate_bibtex(bibtex: str) -> bool:
    """Check BibTeX syntax."""
    try:
        parser.parse_string(bibtex)
        return True
    except Exception:
        return False
```

**Query Sanitization**:
```python
def sanitize_query(query: str) -> str:
    """Remove special characters from search query."""
    # Remove control characters
    # Limit length to 500 chars
    # URL encode for API
```

### Error Information Disclosure

**Safe Errors**:
```python
# Good: Generic error
return {"error": "File not found"}

# Bad: Exposes system info
return {"error": f"Cannot read /home/user/.ssh/id_rsa"}
```

**Error Messages**:
- No system paths in errors
- No internal implementation details
- No stack traces to user (logged only)

### Dependency Security

**Pinned Versions**:
- All dependencies pinned in `pyproject.toml`
- Regular security updates
- Automated vulnerability scanning (Dependabot)

**Trusted Sources**:
- PyPI packages only
- Verified publishers
- Popular, maintained projects

---

## Deployment

### Installation

**Via pip**:
```bash
pip install polyhedra
```

**Via uv** (recommended):
```bash
uv pip install polyhedra
uvx --from polyhedra polyhedra  # Run directly
```

### Configuration

**Environment Variables**:
- `POLYHEDRA_PROJECT_ROOT`: Override project root
- `POLYHEDRA_CACHE_DIR`: Custom cache location
- `POLYHEDRA_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

**Example**:
```bash
export POLYHEDRA_PROJECT_ROOT=/path/to/research
export POLYHEDRA_LOG_LEVEL=INFO
```

### Logging

**Log Locations**:
- **Console**: stderr (captured by IDE)
- **File**: `.polyhedra/polyhedra.log` (optional)

**Log Format**:
```
2024-01-15 10:30:45 INFO [server] Tool call: search_papers
2024-01-15 10:30:45 DEBUG [semantic_scholar] Query: transformers
2024-01-15 10:30:46 INFO [semantic_scholar] Found 25 papers
2024-01-15 10:30:46 INFO [server] Tool call completed: 1.2s
```

---

## Testing Architecture

### Test Structure

```
tests/
├── test_server.py              # MCP server integration tests
├── test_services/
│   ├── test_semantic_scholar.py
│   ├── test_citation_manager.py
│   ├── test_file_context.py
│   ├── test_rag_retrieval.py
│   └── test_project_initializer.py
├── test_integration_workflows.py  # End-to-end workflows
└── test_error_handling.py      # Error scenarios
```

### Test Coverage

- **Unit Tests**: 88-100% coverage per service
- **Integration Tests**: Full workflows tested
- **Error Tests**: All error paths covered

### Test Strategy

1. **Unit Tests**: Mock external dependencies (API, file system)
2. **Integration Tests**: Real dependencies, test data
3. **E2E Tests**: Full workflows with actual API calls (limited)

---

## Future Extensibility

### Planned Extensions

1. **Additional APIs**:
   - arXiv direct integration
   - Google Scholar (via SerpAPI)
   - PubMed for biomedical papers

2. **Enhanced RAG**:
   - Multiple embedding models
   - Hybrid search (keyword + semantic)
   - Re-ranking with cross-encoders

3. **Collaboration**:
   - Shared indexes
   - Team bibliographies
   - Comment/annotation system

4. **Export Formats**:
   - LaTeX integration
   - Markdown citations
   - Zotero/Mendeley import/export

### Extension Points

**Custom Services**:
```python
class CustomPaperService:
    """Implement your own paper source."""
    
    async def search(self, query: str) -> list[dict]:
        """Custom search implementation."""
```

**Custom Embeddings**:
```python
class CustomEmbeddingModel:
    """Use your own embedding model."""
    
    def encode(self, texts: list[str]) -> np.ndarray:
        """Generate custom embeddings."""
```

---

## Troubleshooting

For detailed troubleshooting, see:
- [Error Handling Guide](ERROR_HANDLING.md)
- [Setup Guide](SETUP.md)
- [Manual Testing](MANUAL_TESTING.md)

---

## References

- **MCP Protocol**: https://modelcontextprotocol.io
- **Semantic Scholar API**: https://api.semanticscholar.org
- **Sentence Transformers**: https://www.sbert.net
- **FAISS**: https://github.com/facebookresearch/faiss

---

*Architecture documentation maintained by Polyhedra team. Last updated: January 2024.*
