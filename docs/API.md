# API Reference

Complete reference for all Polyhedra MCP tools.

**Version 2.1** includes 12 tools total (10 from v2.0 + 2 new literature review tools).

## Table of Contents

1. [Literature Search](#literature-search)
   - [search_papers](#search_papers)
   - [get_paper](#get_paper)
   - [query_similar_papers](#query_similar_papers)
   - [index_papers](#index_papers)

2. [Citation Management](#citation-management)
   - [add_citation](#add_citation)
   - [get_citations](#get_citations)

3. [**🆕 Literature Review Generation (v2.1)**](#literature-review-generation-v21)
   - [generate_literature_review](#generate_literature_review)
   - [estimate_review_cost](#estimate_review_cost)

4. [File Operations](#file-operations)
   - [save_file](#save_file)
   - [get_context](#get_context)

5. [Project Management](#project-management)
   - [init_project](#init_project)
   - [get_project_status](#get_project_status)

---

## Literature Search

### search_papers

Search for academic papers using Semantic Scholar.

**Purpose**: Discover papers by keywords, authors, or topics across 200M+ publications.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Search query (keywords, author names, topics) |
| `year_range` | string | No | Filter by publication year (e.g., "2020-2024") |
| `limit` | integer | No | Maximum results (default: 10, max: 100) |
| `fields` | array[string] | No | Fields to include (default: title, authors, year, abstract, citationCount) |

**Returns**:

```json
{
  "papers": [
    {
      "paperId": "abc123",
      "title": "Attention Is All You Need",
      "authors": [{"name": "Ashish Vaswani"}],
      "year": 2017,
      "abstract": "The dominant sequence...",
      "citationCount": 75000,
      "url": "https://semanticscholar.org/paper/abc123"
    }
  ],
  "total": 1,
  "query": "transformers attention"
}
```

**Example Usage**:

```
Search for papers on "neural networks" published 2022-2024 with high citations
```

**Common Patterns**:

- **By topic**: `"transformers in nlp"`
- **By author**: `"author:Hinton neural networks"`
- **Recent papers**: Combine with `year_range: "2023-2024"`
- **Highly cited**: Sort results by `citationCount`

**Error Scenarios**:

- **Network error**: Returns cached results if available
- **Invalid year_range**: Falls back to all years
- **Empty results**: Suggests query refinements
- **Rate limit**: Automatically retries with backoff

**Related Tools**:
- Use `get_paper` for detailed information on specific results
- Use `index_papers` to enable semantic search on results

---

### get_paper

Get detailed information about a specific paper.

**Purpose**: Retrieve comprehensive metadata for a single paper by ID.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `paper_id` | string | Yes | Semantic Scholar paper ID (e.g., "abc123") |
| `fields` | array[string] | No | Fields to retrieve (default: all available) |

**Returns**:

```json
{
  "paperId": "abc123",
  "title": "Attention Is All You Need",
  "authors": [
    {"authorId": "456", "name": "Ashish Vaswani"}
  ],
  "year": 2017,
  "abstract": "The dominant sequence...",
  "citationCount": 75000,
  "referenceCount": 35,
  "influentialCitationCount": 12000,
  "venue": "NeurIPS",
  "url": "https://semanticscholar.org/paper/abc123",
  "openAccessPdf": {"url": "https://arxiv.org/pdf/1706.03762.pdf"},
  "fieldsOfStudy": ["Computer Science"],
  "citations": [...],
  "references": [...]
}
```

**Example Usage**:

```
Get detailed information for paper abc123
```

**Common Patterns**:

- **Get full metadata**: Use default fields
- **Get citations only**: `fields: ["citations"]`
- **Get references**: `fields: ["references"]`
- **Check PDF availability**: Look for `openAccessPdf`

**Error Scenarios**:

- **Invalid paper_id**: Returns error with suggested format
- **Paper not found**: Returns 404 with similar papers suggestion
- **Network error**: Returns cached data if available

**Related Tools**:
- Use after `search_papers` to get full details
- Use with `add_citation` to add to bibliography

---

### query_similar_papers

Find papers similar to a query using semantic search.

**Purpose**: Discover related papers through RAG-powered semantic similarity.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Natural language query or research question |
| `limit` | integer | No | Maximum results (default: 10) |
| `min_similarity` | float | No | Minimum similarity score 0-1 (default: 0.7) |

**Returns**:

```json
{
  "papers": [
    {
      "paperId": "abc123",
      "title": "Attention Is All You Need",
      "similarity": 0.92,
      "reason": "Discusses transformer architecture and attention mechanisms"
    }
  ],
  "query": "self-attention in neural networks"
}
```

**Example Usage**:

```
Find papers similar to "improving model interpretability with attention visualization"
```

**Common Patterns**:

- **Research questions**: `"How do transformers handle long sequences?"`
- **Topic exploration**: `"alternatives to BERT for document classification"`
- **Methodology search**: `"training strategies for large language models"`
- **Gap analysis**: Find what's missing in current literature

**Requirements**:

- Must call `index_papers` first to build search index
- Index must contain relevant papers for query

**Error Scenarios**:

- **Index not built**: Returns message to call `index_papers` first
- **No similar papers**: Returns empty list with suggestion to search more papers
- **Model not loaded**: Downloads embedding model (~400MB) automatically

**Related Tools**:
- Use `index_papers` before querying
- Use `search_papers` to collect papers to index

---

### index_papers

Build semantic search index from collected papers.

**Purpose**: Enable RAG-powered similarity search across your paper collection.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `papers` | array[object] | Yes | List of papers to index (from `search_papers`) |
| `force_rebuild` | boolean | No | Rebuild index even if exists (default: false) |

**Paper Object Schema**:

```json
{
  "paperId": "abc123",
  "title": "Paper Title",
  "abstract": "Paper abstract text...",
  "year": 2023,
  "authors": [{"name": "Author Name"}]
}
```

**Returns**:

```json
{
  "indexed_count": 25,
  "total_papers": 25,
  "index_path": "/path/to/.polyhedra/embeddings.index",
  "model": "sentence-transformers/all-MiniLM-L6-v2"
}
```

**Example Usage**:

```
Index the papers I just searched for to enable semantic search
```

**Common Patterns**:

1. **Search + Index workflow**:
   ```
   1. Search for papers on topic X
   2. Index the results
   3. Query similar papers with research questions
   ```

2. **Incremental indexing**:
   - Index papers as you discover them
   - `force_rebuild: false` appends to existing index

3. **Rebuild index**:
   - Use `force_rebuild: true` to start fresh
   - Useful when changing paper collection focus

**Performance Notes**:

- First run downloads embedding model (~400MB)
- Indexing 100 papers takes ~10-30 seconds
- Index is persisted in `.polyhedra/embeddings.index`

**Error Scenarios**:

- **Missing abstract**: Uses title only for indexing
- **Duplicate papers**: Automatically deduplicated by paperId
- **Disk full**: Returns error with space requirements

**Related Tools**:
- Use `search_papers` to collect papers to index
- Use `query_similar_papers` after indexing

---

## Citation Management

### add_citation

Add BibTeX entry to project bibliography.

**Purpose**: Maintain formatted citations for papers you reference.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `citation_key` | string | Yes | Unique BibTeX key (e.g., "vaswani2017attention") |
| `bibtex` | string | Yes | Complete BibTeX entry |

**BibTeX Format**:

```bibtex
@article{vaswani2017attention,
  title={Attention Is All You Need},
  author={Vaswani, Ashish and Shazeer, Noam and ...},
  journal={Advances in neural information processing systems},
  volume={30},
  year={2017}
}
```

**Returns**:

```json
{
  "success": true,
  "citation_key": "vaswani2017attention",
  "file": "references.bib",
  "total_citations": 42
}
```

**Example Usage**:

```
Add this BibTeX citation with key "hinton2012imagenet": @article{...}
```

**Common Patterns**:

1. **From paper details**:
   ```
   1. Get paper details with get_paper
   2. Generate BibTeX from metadata
   3. Add to bibliography
   ```

2. **Batch citations**:
   - Add multiple citations in sequence
   - Automatically creates `references.bib` if missing

3. **Key naming conventions**:
   - `author_year_keyword` (e.g., `vaswani2017attention`)
   - `firstauthor_etal_year` (e.g., `brown_etal_2020`)

**Validation**:

- Checks for valid BibTeX syntax
- Prevents duplicate citation keys
- Validates required fields (@article, @inproceedings, etc.)

**Error Scenarios**:

- **Invalid BibTeX**: Returns syntax error with line number
- **Duplicate key**: Suggests appending suffix (e.g., `_v2`)
- **File locked**: Retries with exponential backoff
- **Disk full**: Returns error with space needed

**Related Tools**:
- Use `get_citations` to view all citations
- Use `get_paper` to get BibTeX for a paper

---

### get_citations

List all citations in project bibliography.

**Purpose**: View and manage your collected citations.

**Parameters**: None

**Returns**:

```json
{
  "citations": [
    {
      "key": "vaswani2017attention",
      "type": "article",
      "title": "Attention Is All You Need",
      "authors": "Vaswani, Ashish and Shazeer, Noam and ...",
      "year": "2017",
      "venue": "Advances in neural information processing systems"
    }
  ],
  "total": 1,
  "file": "references.bib"
}
```

**Example Usage**:

```
Show me all the citations in my bibliography
```

**Common Patterns**:

1. **Review citations**:
   - Check what papers you've cited
   - Find citation keys for writing

2. **Export bibliography**:
   - Copy references.bib to document
   - Use with LaTeX `\bibliography{references}`

3. **Citation search**:
   - Find citation key by author/title
   - Check if paper already cited

**Output Format**:

- Parses BibTeX into structured JSON
- Sorted by citation key alphabetically
- Includes total count for overview

**Error Scenarios**:

- **No references.bib**: Returns empty list with suggestion to add citations
- **Corrupted file**: Returns error with validation details
- **Read permission**: Returns error with file path

**Related Tools**:
- Use `add_citation` to add new citations
- Use `save_file` to export formatted bibliography

---

## File Operations

### save_file

Write content to a project file.

**Purpose**: Create or update research documents, notes, and outputs.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | string | Yes | File path relative to project root |
| `content` | string | Yes | Content to write |
| `create_dirs` | boolean | No | Create parent directories (default: true) |

**Returns**:

```json
{
  "success": true,
  "path": "literature-review/transformers.md",
  "bytes_written": 1024,
  "created": true
}
```

**Example Usage**:

```
Save this literature review to "papers/summary.md": [content]
```

**Common Patterns**:

1. **Research notes**:
   ```
   Save paper summaries to notes/
   Track ideas in ideas.md
   ```

2. **Generated content**:
   ```
   Write literature review sections
   Generate paper outlines
   Create annotated bibliographies
   ```

3. **Data organization**:
   ```
   Save paper metadata as JSON
   Export search results
   Store processed data
   ```

**Safety Features**:

- Creates parent directories automatically
- UTF-8 encoding for international characters
- Atomic writes (tmp file + rename)
- Preserves original on write failure

**Path Resolution**:

- Relative to project root
- Supports nested paths: `papers/2024/summary.md`
- Normalizes path separators (cross-platform)

**Error Scenarios**:

- **Invalid path**: Returns error with valid path format
- **Permission denied**: Returns error with required permissions
- **Disk full**: Returns error with space needed
- **Invalid UTF-8**: Returns encoding error

**Related Tools**:
- Use `get_context` to read files
- Use `get_project_status` to see project structure

---

### get_context

Read content from project files.

**Purpose**: Access research documents, notes, and data files.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `paths` | array[string] | Yes | List of file paths to read (relative to project) |

**Returns**:

```json
{
  "files": [
    {
      "path": "notes/summary.md",
      "content": "# Literature Review\n\n...",
      "size": 1024,
      "encoding": "utf-8"
    }
  ],
  "total": 1
}
```

**Example Usage**:

```
Read the files: notes/summary.md, papers/metadata.json
```

**Common Patterns**:

1. **Review research**:
   ```
   Read literature review drafts
   Check project notes
   Review paper summaries
   ```

2. **Context for generation**:
   ```
   Read existing content before updating
   Get context for writing new sections
   Check what's already documented
   ```

3. **Batch reading**:
   ```
   Read all markdown files in notes/
   Get all paper summaries
   Load configuration files
   ```

**File Types Supported**:

- Text files: `.md`, `.txt`, `.json`, `.yaml`
- Code: `.py`, `.js`, `.tex`
- Config: `.bib`, `.toml`, `.ini`
- Any UTF-8 encoded file

**Performance**:

- Reads up to 10 files in parallel
- Max file size: 10MB per file
- Returns errors for individual files without failing entire operation

**Error Scenarios**:

- **File not found**: Returns empty content with error message
- **Permission denied**: Skips file with error in response
- **Binary file**: Returns error suggesting text files only
- **Encoding error**: Tries fallback encodings (latin-1, cp1252)

**Related Tools**:
- Use `save_file` to write files
- Use `get_project_status` to see available files

---

## Project Management

### init_project

Initialize a new research project structure.

**Purpose**: Create standardized directory structure and starter files.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_name` | string | Yes | Name of the project (used for directory naming) |
| `base_path` | string | No | Parent directory (default: current working directory) |

**Created Structure**:

```
project_name/
├── .polyhedra/           # Tool data (index, cache)
├── papers/               # Paper PDFs and metadata
├── notes/                # Research notes
├── literature-review/    # Literature review drafts
├── data/                 # Datasets and processed data
├── references.bib        # BibTeX bibliography
└── README.md             # Project overview
```

**Returns**:

```json
{
  "project_name": "my-research",
  "path": "/home/user/my-research",
  "created_dirs": [
    ".polyhedra",
    "papers",
    "notes",
    "literature-review",
    "data"
  ],
  "created_files": [
    "references.bib",
    "README.md"
  ]
}
```

**Example Usage**:

```
Initialize a new research project called "transformer-survey"
```

**Common Patterns**:

1. **Start new research**:
   ```
   1. Initialize project
   2. Set project as working directory
   3. Begin searching for papers
   ```

2. **Organize existing research**:
   ```
   1. Create project structure
   2. Move existing files into structure
   3. Start using tools
   ```

**Idempotent Operation**:

- Safe to run multiple times
- Won't overwrite existing files
- Only creates missing directories
- Reports what was created vs. already existed

**README Template**:

```markdown
# [Project Name]

## Research Question

TODO: Define your research question

## Papers

Papers are organized in the `papers/` directory.

## Notes

Research notes are in the `notes/` directory.

## Citations

Bibliography is in `references.bib`.
```

**Error Scenarios**:

- **Directory exists**: Reports existing, doesn't fail
- **Permission denied**: Returns error with required permissions
- **Invalid project name**: Suggests valid naming (alphanumeric, dashes, underscores)

**Related Tools**:
- Use `get_project_status` to see project structure
- Use `save_file` and `get_context` for file operations

---

### get_project_status

Get overview of project structure and contents.

**Purpose**: Understand project organization and find files.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | string | No | Project root path (default: current directory) |

**Returns**:

```json
{
  "project_path": "/home/user/my-research",
  "structure": {
    "papers": {
      "file_count": 5,
      "total_size": "25.3 MB",
      "files": ["paper1.pdf", "paper2.pdf"]
    },
    "notes": {
      "file_count": 3,
      "files": ["summary.md", "ideas.md"]
    },
    "literature-review": {
      "file_count": 1,
      "files": ["draft.md"]
    }
  },
  "citations": {
    "total": 42,
    "file": "references.bib"
  },
  "index": {
    "exists": true,
    "papers_indexed": 25,
    "last_updated": "2024-01-15T10:30:00Z"
  }
}
```

**Example Usage**:

```
Show me the status of my research project
```

**Common Patterns**:

1. **Project overview**:
   ```
   Check what files exist
   See how many papers collected
   Review citation count
   ```

2. **Before writing**:
   ```
   Check existing structure
   Find where to save new content
   See what's already documented
   ```

3. **Progress tracking**:
   ```
   Monitor paper collection growth
   Track documentation progress
   Check index status
   ```

**Status Indicators**:

- **Papers**: Count, total size, recent additions
- **Notes**: File count, last modified
- **Literature Review**: Section count, word count
- **Citations**: Total count in bibliography
- **Index**: Existence, paper count, freshness

**Error Scenarios**:

- **Not a project**: Suggests running `init_project`
- **Permission denied**: Returns error with path
- **Corrupted structure**: Reports issues found

**Related Tools**:
- Use `init_project` to create project
- Use `get_context` to read specific files
- Use `get_citations` for detailed citation info

---

## Literature Review Generation (v2.1)

### generate_literature_review

Generate structured academic literature review from paper collection.

**Purpose**: Synthesize 10-100 papers into coherent academic review with proper citations, taxonomy, critical analysis, and research gaps.

**Prerequisites**: 
- LLM API key configured (`ANTHROPIC_API_KEY` or `OPENAI_API_KEY`)
- Papers file from `search_papers` or manually created JSON

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `papers_file` | string | No | Path to papers JSON (default: "literature/papers.json") |
| `focus` | string | No | Specific focus area for review |
| `structure` | string | No | Organization: "thematic"/"chronological"/"methodological" (default: "thematic") |
| `depth` | string | No | Review depth: "brief"/"standard"/"comprehensive" (default: "standard") |
| `include_gaps` | boolean | No | Include research gaps section (default: true) |
| `output_path` | string | No | Where to save review (default: "literature/review.md") |
| `llm_model` | string | No | Model override (default: claude-3-5-sonnet-20241022) |

**Returns**:

```json
{
  "success": true,
  "saved_to": "literature/review.md",
  "metadata": {
    "paper_count": 47,
    "word_count": 3542,
    "sections": ["Overview", "Taxonomy", "Critical Analysis", "Research Gaps", "Conclusion"],
    "citations_found": 45,
    "citation_coverage": 0.96,
    "research_gaps": [
      {
        "title": "Efficiency at Scale",
        "description": "Current transformers struggle with sequences >10K tokens"
      }
    ]
  },
  "cost": {
    "input_tokens": 18234,
    "output_tokens": 5890,
    "total_tokens": 24124,
    "total_usd": 0.14
  },
  "citations_added": 47
}
```

**Review Depth Levels**:

| Depth | Words | Pages | Cost (50 papers) | Use Case |
|-------|-------|-------|------------------|----------|
| **brief** | ~650 | 2-3 | $0.08-0.12 | Quick overview, presentation prep |
| **standard** | ~2000 | 5-8 | $0.12-0.20 | Paper background section, grant proposals |
| **comprehensive** | ~2500 | 10-15 | $0.20-0.35 | Dissertation chapters, major surveys |

**Structure Types**:

- **thematic**: Groups papers by research themes and approaches (recommended for most cases)
- **chronological**: Orders papers by publication timeline (good for tracking field evolution)
- **methodological**: Organizes by research methods used (good for comparing techniques)

**Example Usage**:

```
"Generate a literature review from my papers focused on mobile deployment"
```

```
"Generate a comprehensive review with chronological structure"
```

```
"Generate brief review without research gaps, save to method/background.md"
```

**Common Patterns**:

1. **Quick Synopsis**: Use `depth="brief"` for rapid overview
2. **Focused Review**: Set `focus` parameter to narrow scope
3. **Cost-Conscious**: Use `estimate_review_cost` first
4. **Custom Location**: Set `output_path` to save anywhere in project
5. **Chronological Survey**: Use `structure="chronological"` for historical perspective

**Error Scenarios**:

| Error | Cause | Solution |
|-------|-------|----------|
| "LLM service not configured" | Missing API key | Set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` |
| "Papers file not found" | No papers.json | Run `search_papers` first or create file |
| "Papers file is empty" | Empty JSON array | Search for papers or add manually |
| "API rate limit exceeded" | Too many requests | Wait 60 seconds and retry |
| "Token limit exceeded" | Too many papers | Reduce paper count or use brief depth |

**Cost Guidance**:

- **25 papers, brief**: $0.05-0.08
- **50 papers, standard**: $0.12-0.20
- **75 papers, comprehensive**: $0.25-0.40
- **100 papers, comprehensive**: $0.35-0.60

Cost scales with:
- Number of papers (more input tokens)
- Review depth (more output tokens)
- Model choice (Claude Sonnet < GPT-4 Turbo)

**Output Format**:

Generated review includes:
- **Overview**: Field introduction and scope
- **Taxonomy**: Hierarchical organization of approaches
- **Critical Analysis**: Strengths, weaknesses, comparisons
- **Research Gaps** (if enabled): Underexplored areas and opportunities
- **Conclusion**: Summary and future directions
- **Proper Citations**: All papers cited as `[Author et al., Year]`

**Related Tools**:
- Use `search_papers` to find papers first
- Use `estimate_review_cost` to check cost before generation
- Use `add_citation` to add more citations manually
- Use `save_file` to modify and save the review

---

### estimate_review_cost

Estimate cost before generating literature review.

**Purpose**: Get accurate cost estimate without consuming API credits. Helps budget and plan expensive operations.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `paper_count` | number | Yes | Number of papers to review |
| `depth` | string | No | Review depth (default: "standard") |
| `llm_model` | string | No | Model to use (affects pricing) |

**Returns**:

```json
{
  "estimated_input_tokens": 18000,
  "estimated_output_tokens": 2000,
  "estimated_total_tokens": 20000,
  "estimated_usd": 0.15,
  "paper_count": 50,
  "depth": "standard"
}
```

**Example Usage**:

```
"Estimate cost for reviewing 75 papers with comprehensive depth"
```

```
"How much will it cost to generate a brief review of 30 papers?"
```

**Cost Examples**:

| Papers | Depth | Model | Estimated Cost |
|--------|-------|-------|----------------|
| 25 | brief | Claude Sonnet | $0.05-0.08 |
| 50 | standard | Claude Sonnet | $0.12-0.20 |
| 50 | standard | GPT-4 Turbo | $0.30-0.40 |
| 75 | comprehensive | Claude Sonnet | $0.25-0.40 |
| 100 | comprehensive | Claude Sonnet | $0.40-0.65 |

**When to Use**:

- Before generating reviews with >50 papers
- When using comprehensive depth
- When working with budget constraints
- Before batch processing multiple reviews

**Accuracy**: Estimates are typically within ±20% of actual cost. Actual cost depends on:
- Actual paper abstract lengths (estimated at 300 words avg)
- LLM's response length (may vary from target)
- Model pricing changes

**Related Tools**:
- Use before `generate_literature_review` for cost-conscious workflows
- Combine with `get_project_status` to track total costs

---

## Error Handling

All tools follow consistent error handling patterns:

### Error Response Format

```json
{
  "error": true,
  "message": "Human-readable error description",
  "error_type": "NetworkError",
  "details": {
    "path": "/path/to/file",
    "suggestion": "Try checking your internet connection"
  }
}
```

### Common Error Types

| Error Type | Description | Recovery |
|------------|-------------|----------|
| `NetworkError` | API or connection issues | Retries automatically, uses cache |
| `FileNotFoundError` | File doesn't exist | Returns suggestion for valid path |
| `ValidationError` | Invalid input parameters | Returns validation details |
| `RateLimitError` | API rate limit exceeded | Waits and retries automatically |
| `IndexNotBuiltError` | Semantic index missing | Suggests calling `index_papers` |

### Automatic Retries

- **Network errors**: 3 retries with exponential backoff
- **Rate limits**: Waits for reset time, then retries
- **Transient errors**: Retries with jitter

### Graceful Degradation

- **Offline mode**: Uses cached data when available
- **Partial results**: Returns successful operations even if some fail
- **Fallbacks**: Switches to alternative methods when primary fails

See [Error Handling Guide](ERROR_HANDLING.md) for detailed troubleshooting.

---

## Rate Limits & Performance

### Semantic Scholar API

- **Rate limit**: 100 requests/5 minutes
- **Burst**: 10 requests/second
- **Handling**: Automatic backoff and retry

### Local Operations

- **File reads**: No limit, cached in memory
- **File writes**: No limit, atomic operations
- **Indexing**: ~100 papers/minute (after model download)

### Best Practices

1. **Batch operations** when possible
2. **Reuse index** instead of rebuilding
3. **Cache search results** for repeated queries
4. **Use specific queries** to reduce API calls

---

## Version Compatibility

- **Python**: 3.11+
- **MCP SDK**: 1.0+
- **Semantic Scholar API**: v1
- **IDEs**: Cursor 0.40+, VS Code 1.85+, Windsurf 1.0+

For updates and changelog, see [GitHub Releases](https://github.com/yourusername/polyhedra/releases).
