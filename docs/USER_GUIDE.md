# Polyhedra User Guide

Complete guide to using Polyhedra MCP Server for academic research.

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [IDE Setup](#ide-setup)
- [Core Concepts](#core-concepts)
- [Using the Tools](#using-the-tools)
- [Research Workflows](#research-workflows)
- [Tips & Best Practices](#tips--best-practices)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

**Get started in 3 steps:**

1. **Install Polyhedra**
   ```bash
   git clone https://github.com/yourusername/polyhedra.git
   cd polyhedra
   pip install -e .
   ```

2. **Configure Your IDE** (example for Cursor)
   
   Add to ~/.cursor/mcp.json:
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

3. **Start Using**
   
   Open your IDE and ask:
   `
   "Initialize a new research project called 'deep-learning-review'"
   `

---

## Installation

### Requirements

- Python 3.11 or higher
- Git
- One of the supported IDEs:
  - Cursor
  - VS Code with GitHub Copilot
  - Windsurf
  - VS Code with MCP extension

### Method 1: Standard Installation

```bash
git clone https://github.com/yourusername/polyhedra.git
cd polyhedra
pip install -e .
```

### Method 2: Using uv (faster)

```bash
git clone https://github.com/yourusername/polyhedra.git
cd polyhedra
pip install uv
uv pip install -e .
```

### Verify Installation

```bash
python -m polyhedra.server --version
```

---

## IDE Setup

### Cursor

1. **Open MCP Settings**: ~/.cursor/mcp.json

2. **Add Polyhedra**:
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

3. **Restart Cursor**

4. **Test**: Ask Copilot "What Polyhedra tools are available?"

### VS Code with GitHub Copilot

1. **Create workspace settings**: .vscode/settings.json

2. **Add configuration**:
   `json
   {
     "github.copilot.chat.codeGeneration.instructions": [
       {
         "file": ".github/copilot-instructions.md"
       }
     ]
   }
   `

3. **Create instructions file**: .github/copilot-instructions.md
   `markdown
   Use the Polyhedra MCP tools for academic research tasks.
   Available tools: search_papers, add_citation, index_papers, etc.
   `

4. **Reload window**: Ctrl+Shift+P  "Developer: Reload Window"

### Windsurf

Same as Cursor, but use ~/.windsurf/mcp.json

### VS Code with MCP Extension

1. Install MCP extension from marketplace
2. Configure in workspace settings
3. Point to uvx --from polyhedra polyhedra

For detailed setup instructions, see docs/SETUP.md

---

## Core Concepts

### Project Structure

Polyhedra expects this directory structure:

`
my-research-project/
 literature/          # Research papers (JSON, PDF)
 references.bib       # BibTeX citations
 writing/            # Your papers and drafts
 ideas/              # Notes and brainstorming
 data/               # Research data
 .poly/              # Polyhedra metadata (auto-created)
     embeddings/     # Semantic search index
`

### Semantic Search (RAG)

Polyhedra uses **RAG (Retrieval Augmented Generation)** to find relevant papers:

1. **Index papers**  Creates embeddings from titles and abstracts
2. **Query with natural language**  Finds semantically similar papers
3. **Get ranked results**  Papers sorted by relevance score

### Citation Management

- **BibTeX format** for all citations
- **Automatic deduplication** by citation key
- **Auto-generated keys** from author/year/title
- **Stored in** 
eferences.bib

---

## Using the Tools

### 1. Initialize Project

**What it does**: Creates standard research project structure

**When to use**: Starting a new research project

**Example**:
`
"Initialize a new research project called 'transformer-survey'"
`

**Creates**:
- 5 directories (literature, writing, ideas, data, notes)
- 2 files (README.md, references.bib)

---

### 2. Search Papers

**What it does**: Searches Semantic Scholar for academic papers

**When to use**: Literature review, finding related work

**Example**:
`
"Search for recent papers on 'attention mechanisms in transformers' 
 published between 2020-2023, limit to 10 results"
`

**Parameters**:
- query: Search terms (required)
- limit: Max results (default: 10, max: 100)
- year_start: Filter by year (optional)
- year_end: Filter by year (optional)

**Returns**: Paper details with titles, authors, abstracts, citations, BibTeX

---

### 3. Get Paper Details

**What it does**: Gets detailed info for a specific paper by ID

**When to use**: Following up on a specific paper

**Example**:
`
"Get details for paper ID 204e3073870fae3d05bcbc2f6a8e263d9b72e776"
`

**Returns**: Full paper metadata, BibTeX entry, citation count

---

### 4. Add Citation

**What it does**: Adds a BibTeX entry to references.bib

**When to use**: Building your bibliography

**Example**:
`
"Add this citation to my bibliography:
@article{vaswani2017attention,
  title={Attention is all you need},
  author={Vaswani, Ashish and Shazeer, Noam},
  year={2017}
}"
`

**Features**:
- Automatic deduplication
- Validates BibTeX format
- Returns citation key for use in writing

---

### 5. Get Citations

**What it does**: Lists all citations in your bibliography

**When to use**: Reviewing your references, checking what's already added

**Example**:
`
"Show me all my citations"
`

**Returns**: Array of all BibTeX entries with keys

---

### 6. Index Papers

**What it does**: Creates semantic search index from saved papers

**When to use**: After collecting papers, before querying

**Example**:
`
"Index the papers in literature/recent-papers.json"
`

**Requirements**: Papers file must exist with title and abstract fields

**Performance**: ~2 seconds for 50 papers

---

### 7. Query Similar Papers

**What it does**: Semantic search over indexed papers

**When to use**: Finding relevant papers in your collection

**Example**:
`
"Find papers similar to 'self-attention mechanisms for NLP' 
 from my indexed papers, show top 5"
`

**Parameters**:
- query: Natural language search (required)
- k: Number of results (default: 5)

**Returns**: Papers ranked by relevance score (0.0-1.0)

**Requires**: Papers must be indexed first

---

### 8. Save File

**What it does**: Writes content to a file in your project

**When to use**: Saving generated content, creating drafts

**Example**:
`
"Save this abstract to writing/draft-abstract.md:
[your abstract text]"
`

**Features**:
- Creates parent directories automatically
- Supports append mode
- UTF-8 encoding

---

### 9. Get Context

**What it does**: Reads files from your project

**When to use**: Reviewing content, including context in prompts

**Example**:
`
"Read the contents of writing/introduction.md and ideas/key-points.md"
`

**Features**:
- Batch reading (multiple files at once)
- Reports missing files without failing
- UTF-8 decoding

**Returns**: Dictionary of file contents + list of missing files

---

### 10. Get Project Status

**What it does**: Overview of your research project

**When to use**: Checking progress, understanding project state

**Example**:
`
"Give me the status of my research project"
`

**Returns**:
- Paper count in literature/
- Citation count in references.bib
- RAG index status
- List of standard files
- Total file count

---

## Research Workflows

### Workflow 1: Literature Review

**Goal**: Find and organize relevant papers

`
1. "Initialize a project called 'literature-review-transformers'"

2. "Search for papers on 'transformer architecture' from 2017-2023, 
    limit 20"

3. "Save those papers to literature/transformer-papers.json"

4. "Add citations for the top 5 papers to my bibliography"

5. "Index the papers in literature/transformer-papers.json"

6. "Find papers similar to 'positional encoding in transformers'"

7. "Get project status"
`

**Result**: Organized collection of papers with citations ready for writing

---

### Workflow 2: Writing with Citations

**Goal**: Draft a paper section with proper citations

`
1. "Search for papers on 'BERT pretraining' and add the top 3 
    to my citations"

2. "Show me all my citations"

3. "Save this introduction to writing/intro.md:
    [AI generates introduction with citation keys]"

4. "Read writing/intro.md to verify"
`

**Result**: Draft with citation keys that match references.bib

---

### Workflow 3: Finding Research Gaps

**Goal**: Identify under-explored areas

`
1. "Search for 'multimodal transformers' papers from 2020-2023"

2. "Save to literature/multimodal.json and index them"

3. "Query for papers about 'video understanding transformers'"

4. "Query for papers about 'audio-visual fusion'"

5. "Compare the results to find gaps"
`

**Result**: Understand coverage of different topics in your collection

---

### Workflow 4: Related Work Section

**Goal**: Build comprehensive related work

`
1. "Search for papers on [my topic] and save to literature/related.json"

2. "Index literature/related.json"

3. "For each subsection topic, query similar papers"

4. "Add relevant citations to references.bib"

5. "Save organized related work to writing/related-work.md"
`

**Result**: Well-organized related work section with citations

---

## Tips & Best Practices

### Search Strategies

 **DO**:
- Use specific technical terms: "attention mechanisms" vs "AI"
- Combine concepts: "BERT pretraining methodology"
- Filter by year for recent work: year_start=2020
- Start with small limits (5-10) and expand

 **DON'T**:
- Use overly broad terms: "machine learning"
- Request too many results at once (API rate limits)
- Search without year filters when recency matters

### Citation Management

 **DO**:
- Let Polyhedra generate citation keys automatically
- Review citations before adding to bibliography
- Use consistent citation styles
- Check for duplicates with "Show me all my citations"

 **DON'T**:
- Manually create citation keys (error-prone)
- Add same paper twice (auto-dedup handles this)
- Mix citation formats (stick to BibTeX)

### Semantic Search

 **DO**:
- Index papers before querying
- Re-index when adding new papers to collection
- Use natural language queries: "papers about X"
- Check relevance scores (>0.7 is high relevance)

 **DON'T**:
- Query before indexing (returns empty results)
- Use too many keywords (semantic search handles concepts)
- Ignore low relevance scores (<0.3)

### File Organization

 **DO**:
- Keep papers in literature/ directory
- Name files descriptively: 	ransformer-papers-2023.json
- Use subdirectories: literature/attention/, literature/pretraining/
- Back up your 
eferences.bib file

 **DON'T**:
- Store papers in random locations
- Use generic names: papers.json, data.json
- Forget to commit .poly/ to git (contains index)

### Performance

 **DO**:
- Index once, query many times
- Batch operations when possible
- Use local operations (file read/write) for speed
- Save search results to avoid re-querying

 **DON'T**:
- Re-index on every query
- Make many small API calls (use limits)
- Query API when local search works

---

## Troubleshooting

### "No tools available"

**Cause**: IDE hasn't loaded Polyhedra MCP server

**Fix**:
1. Check MCP config file location and syntax
2. Restart IDE completely
3. Verify installation: pip show polyhedra
4. Check IDE console for error messages

---

### "Papers not indexed. Run index_papers first"

**Cause**: Trying to query before indexing

**Fix**:
`
"Index the papers in literature/my-papers.json first"
`

Then query again.

---

### "Papers file not found"

**Cause**: File path doesn't exist or incorrect

**Fix**:
1. Check file exists: "Get project status"
2. Use relative path from project root
3. Verify spelling: literature/papers.json not literature/paper.json

---

### "Invalid BibTeX format"

**Cause**: Malformed BibTeX entry

**Fix**:
- Ensure @article{key, format
- Include required fields: 	itle, uthor, year
- Close all braces: }
- Check for special characters in values

**Example valid entry**:
`ibtex
@article{smith2023,
  title={My Paper Title},
  author={Smith, John and Doe, Jane},
  year={2023},
  journal={Conference Name}
}
`

---

### "Rate limit exceeded"

**Cause**: Too many API requests to Semantic Scholar

**Fix**:
- Wait 60 seconds before next request
- Reduce search limits
- Use indexed/cached papers when possible
- Polyhedra automatically retries with exponential backoff

---

### Search returns no results

**Possible causes**:
1. **Query too specific**: Try broader terms
2. **Year filter too narrow**: Remove or expand year range
3. **Spelling error**: Check technical term spelling
4. **API issue**: Try again in a few minutes

**Fix**: Start broad, then narrow down

---

### Slow performance

**Indexing takes long**:
- Normal for large collections (>100 papers)
- First run downloads ML model (~50MB)
- Subsequent runs are faster

**Searches take long**:
- Normal for first API call (cold start)
- API rate limiting may cause delays
- Use indexed papers for faster local search

---

## Advanced Usage

### Batch Operations

**Add multiple citations**:
`
"Search for papers on [topic], then add all of them to my bibliography"
`

**Read multiple files**:
`
"Read all markdown files in the writing/ directory"
`

### Complex Queries

**Semantic Scholar supports**:
- Boolean operators: "attention AND transformers"
- Author filtering: "author:Vaswani"
- Venue filtering: "venue:NeurIPS"

**Example**:
`
"Search for 'author:Vaswani transformers' from 2017-2020"
`

### Chaining Workflows

**Automated pipeline**:
`
"Search for [topic], save to literature/, index them, 
 query for [specific aspect], add top 5 to citations,
 and give me a project status"
`

---

## Need More Help?

- **Documentation**: docs/API.md - Full API reference
- **Setup Guide**: docs/SETUP.md - Detailed IDE setup
- **Workflows**: docs/WORKFLOWS.md - More examples
- **Architecture**: docs/ARCHITECTURE.md - Technical details
- **Error Handling**: docs/ERROR_HANDLING.md - All error scenarios

---

## Quick Reference Card

| Task | Example Prompt |
|------|---------------|
| **Initialize** | "Initialize project 'my-research'" |
| **Search** | "Search for 'topic' papers from 2020-2023" |
| **Save Results** | "Save those papers to literature/papers.json" |
| **Add Citation** | "Add citation for the first paper" |
| **Index Papers** | "Index literature/papers.json" |
| **Find Similar** | "Find papers similar to 'concept'" |
| **Check Status** | "Get project status" |
| **Read File** | "Read writing/draft.md" |
| **Save File** | "Save [content] to writing/notes.md" |
| **List Citations** | "Show all my citations" |

---

**Happy Researching with Polyhedra! **
