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

## Literature Review Generation (v2.1) 🆕

Generate AI-powered literature reviews from your paper collection.

### Prerequisites

1. **Papers collected** via `search_papers` or manual JSON file
2. **LLM API key configured** (see [Setup Guide](SETUP.md))
   - Anthropic (recommended): `export ANTHROPIC_API_KEY=sk-ant-...`
   - OpenAI (alternative): `export OPENAI_API_KEY=sk-...`

### Basic Workflow

#### Step 1: Search and Collect Papers

```
"Search for 50 papers on transformer efficiency techniques"
```

Papers automatically saved to `literature/papers.json`

#### Step 2: Estimate Cost (Recommended)

```
"Estimate cost for reviewing these 50 papers with standard depth"
```

Returns: `{"estimated_usd": 0.15, "paper_count": 50, "depth": "standard"}`

#### Step 3: Generate Review

```
"Generate a literature review from my papers focused on mobile deployment"
```

Generates:
- `literature/review.md` - Structured academic review
- Auto-adds all citations to `references.bib`
- Returns metadata and actual cost

#### Step 4: Review and Refine

Open `literature/review.md` to see:
- ✅ **Overview**: Field introduction and scope
- ✅ **Taxonomy**: Hierarchical organization of approaches
- ✅ **Critical Analysis**: Strengths, weaknesses, comparisons
- ✅ **Research Gaps**: Underexplored areas and opportunities
- ✅ **Conclusion**: Summary and future directions
- ✅ **Proper Citations**: All papers cited as `[Author et al., Year]`

### Review Depth Levels

Choose the right depth for your use case:

#### Brief (~650 words, 2-3 pages)
**Best for**: Quick overviews, presentation prep, initial exploration

```
"Generate a brief literature review"
```

**Output**:
- High-level overview
- Major themes only
- 5-10 minute read
- **Cost**: $0.05-0.12 (50 papers)

#### Standard (~2000 words, 5-8 pages)
**Best for**: Paper background sections, grant proposals, comprehensive understanding

```
"Generate a standard literature review"
```

**Output**:
- Comprehensive coverage
- Detailed taxonomy
- Critical analysis
- Research gaps section
- 20-30 minute read
- **Cost**: $0.12-0.25 (50 papers)

#### Comprehensive (~2500 words, 10-15 pages)
**Best for**: Dissertation chapters, major survey papers, formal publications

```
"Generate a comprehensive literature review"
```

**Output**:
- Exhaustive review
- Deep analysis of each approach
- Extensive gaps section
- Methodology comparison
- 45-60 minute read
- **Cost**: $0.20-0.40 (50 papers)

### Review Structure Types

Choose how to organize your review:

#### Thematic (Default)
Groups papers by research themes and approaches.

```
"Generate a thematic literature review"
```

**Best for**: Understanding the landscape, identifying main directions

**Example sections**:
- Attention Mechanisms
- Efficiency Techniques
- Mobile Architectures
- Quantization Methods

#### Chronological
Orders papers by publication timeline.

```
"Generate a chronological literature review"
```

**Best for**: Tracking field evolution, understanding historical context

**Example sections**:
- Early Work (2017-2019)
- Breakthrough Period (2020-2021)
- Recent Advances (2022-2024)

#### Methodological
Organizes by research methods used.

```
"Generate a methodological literature review"
```

**Best for**: Comparing approaches, identifying methodology gaps

**Example sections**:
- Neural Architecture Search
- Knowledge Distillation
- Pruning and Quantization
- Hardware-Aware Design

### Advanced Usage

#### Focused Review
Narrow the scope to specific aspects:

```
"Generate a comprehensive review focused on quantization techniques for edge devices"
```

The `focus` parameter helps the LLM:
- Prioritize relevant papers
- Emphasize specific aspects
- Filter out tangential content
- Provide deeper analysis of focus area

#### Custom Output Location

```
"Generate a review and save to method/related-work.md"
```

#### Specific Model Selection

```
"Generate review using GPT-4 Turbo"
```

Available models:
- `claude-3-5-sonnet-20241022` (default, recommended)
- `claude-3-opus-20240229` (higher quality, higher cost)
- `gpt-4o` (OpenAI default)
- `gpt-4-turbo` (OpenAI alternative)

#### Skip Research Gaps

```
"Generate a brief review without research gaps section"
```

Useful when you only need synthesis, not gap analysis.

### Cost Management

#### Always Estimate First

For large collections or expensive depths:

```
"Estimate cost before generating a comprehensive review of 100 papers"
```

Returns detailed cost breakdown before spending credits.

#### Understanding Cost Warnings

If estimated cost > $0.10, Polyhedra will warn you:

```
⚠️ Estimated cost: $0.25 for comprehensive review of 75 papers
Add confirm_cost=true to proceed
```

To proceed:
```
"Generate the review with confirm_cost=true"
```

#### Budget Limits

Default maximum cost: **$1.00 per operation**

To change:
```bash
export POLYHEDRA_MAX_COST=0.50  # Set lower limit
```

Polyhedra will block operations exceeding the limit.

To override (not recommended):
```
"Generate the review with force=true"
```

#### Tracking Costs

Each generation returns actual cost:

```json
{
  "cost": {
    "input_tokens": 18234,
    "output_tokens": 5890,
    "total_tokens": 24124,
    "total_usd": 0.14
  }
}
```

### Tips & Best Practices

#### 1. Start Small
Begin with brief reviews to understand output quality:
```
"Generate a brief review to see the format first"
```

#### 2. Curate Papers
**Better input = Better output**

Ideal paper count: **20-50 papers**
- Too few (<10): Shallow analysis
- Just right (20-50): Comprehensive but manageable
- Too many (>100): May hit token limits or high costs

#### 3. Use Focus Parameter
Narrow scope improves relevance:
```
"Generate review focused on real-time inference optimization"
```

#### 4. Check Cost for Large Collections
Always estimate for >50 papers:
```
"Estimate cost first for 80 papers"
```

#### 5. Iterate Depth Levels
Progressive refinement:
1. Start with `brief` for quick overview
2. Expand to `standard` for more detail
3. Use `comprehensive` only for formal publications

#### 6. Manual Refinement
Generated reviews are **starting points**:
- Review for accuracy
- Add domain-specific insights
- Verify citations against source papers
- Refine structure to match your needs

#### 7. Combine with Search
Iterative workflow:
```
1. "Search for initial papers on topic X"
2. "Generate brief review"
3. "Based on gaps, search for papers on Y"
4. "Add new papers to literature/papers.json"
5. "Generate updated standard review"
```

### Common Issues

#### "LLM service not configured"

**Cause**: Missing API key

**Solution**:
```bash
# Choose one:
export ANTHROPIC_API_KEY=sk-ant-your-key
export OPENAI_API_KEY=sk-your-key

# Restart IDE
```

Verify:
```
"Check if my LLM configuration is working"
```

#### "Papers file not found"

**Cause**: No papers.json exists

**Solution**:
```
"Search for papers first, then generate review"
```

Or manually create `literature/papers.json`:
```json
[
  {
    "title": "Paper Title",
    "authors": [{"name": "Author Name"}],
    "year": 2024,
    "abstract": "Paper abstract...",
    "venue": "Conference Name"
  }
]
```

#### "Papers file is empty"

**Cause**: Empty JSON array `[]`

**Solution**:
```
"Search for papers to populate the file"
```

#### "Cost exceeds configured limit"

**Cause**: Estimated cost > `POLYHEDRA_MAX_COST`

**Solutions**:
1. Increase limit: `export POLYHEDRA_MAX_COST=1.50`
2. Reduce paper count (filter to most relevant)
3. Use brief depth instead of comprehensive
4. Force execution: Add `force=true` (not recommended)

#### "Review quality insufficient"

**Causes & Solutions**:

**Too generic**:
- Add specific focus parameter
- Curate papers more carefully
- Try different structure type

**Missing key papers**:
- Verify papers.json includes them
- Check citation coverage in metadata

**Poor organization**:
- Try different structure (thematic vs chronological)
- Add focus to narrow scope

**Shallow analysis**:
- Upgrade from brief to standard/comprehensive
- Reduce paper count for deeper analysis

#### "Token limit exceeded"

**Cause**: Too many papers for context window

**Solutions**:
1. Reduce paper count (aim for <75)
2. Use brief depth (less output tokens)
3. Split into multiple focused reviews

### Cost Examples (Real Scenarios)

| Scenario | Papers | Depth | Cost | Time |
|----------|--------|-------|------|------|
| Conference presentation prep | 20 | brief | $0.06 | 1-2 min |
| Paper background section | 40 | standard | $0.14 | 2-3 min |
| PhD qualifying exam | 60 | comprehensive | $0.28 | 3-4 min |
| Grant proposal literature review | 50 | standard | $0.18 | 2-3 min |
| Dissertation chapter | 80 | comprehensive | $0.42 | 4-5 min |
| Survey paper | 100 | comprehensive | $0.55 | 5-6 min |

*Costs are estimates for Anthropic Claude Sonnet. GPT-4 Turbo costs ~2.5x more.*

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
