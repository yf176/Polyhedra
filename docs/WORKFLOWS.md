# Research Workflows

Complete workflow examples for common research tasks using Polyhedra.

## Table of Contents

1. [Literature Review Workflow](#literature-review-workflow)
2. [Paper Discovery & Analysis](#paper-discovery--analysis)
3. [Citation Management Workflow](#citation-management-workflow)
4. [RAG-Powered Research Exploration](#rag-powered-research-exploration)
5. [Project Organization Workflow](#project-organization-workflow)
6. [Multi-Topic Research](#multi-topic-research)
7. [Collaborative Research Setup](#collaborative-research-setup)

---

## Literature Review Workflow

**Goal**: Write a comprehensive literature review on a specific topic.

### Step-by-Step Process

#### 1. Initialize Project

```
Initialize a new research project called "transformer-survey-2024"
```

**Result**: Creates project structure with papers/, notes/, literature-review/ directories.

#### 2. Broad Topic Search

```
Search for papers on "transformer architectures" from 2020-2024, limit 50
```

**What to look for**:
- Highly cited foundational papers
- Recent survey papers
- Papers with high influential citation counts

#### 3. Refine and Organize

Save search results:
```
Save the search results to "papers/metadata.json"
```

Take notes on key papers:
```
Save these notes to "notes/transformer-basics.md":

# Transformer Basics

## Key Papers
- Vaswani et al. 2017: Original transformer architecture
- Devlin et al. 2018: BERT - bidirectional encoders
- Brown et al. 2020: GPT-3 - scaling laws

## Research Themes
1. Architecture improvements
2. Training efficiency
3. Application domains
```

#### 4. Build Semantic Index

```
Index the papers from my search to enable semantic queries
```

**Result**: Creates embeddings for semantic search.

#### 5. Deep Dive with Semantic Search

Ask research questions:
```
Find papers similar to "What are the limitations of self-attention in long sequences?"
```

```
Query similar papers about "efficient alternatives to standard attention mechanisms"
```

#### 6. Collect Citations

Add key papers to bibliography:
```
Add this citation with key "vaswani2017attention":
@article{vaswani2017attention,
  title={Attention is all you need},
  author={Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N and Kaiser, {\L}ukasz and Polosukhin, Illia},
  journal={Advances in neural information processing systems},
  volume={30},
  year={2017}
}
```

Repeat for 20-30 key papers.

#### 7. Draft Literature Review

```
Save this literature review draft to "literature-review/section-1-intro.md":

# Transformer Architectures: A Survey

## Introduction

The transformer architecture \cite{vaswani2017attention} revolutionized...

## Evolution of Transformers

Following the original work, several improvements emerged...

[Continue with organized sections citing papers from bibliography]
```

#### 8. Verify Citations

```
Show me all citations in my bibliography
```

Check that all cited papers are in references.bib.

#### 9. Get Project Overview

```
Show me my project status
```

**Expected output**:
- 50 papers in papers/ directory
- 5-10 notes files
- 3-5 literature review sections
- 30+ citations in bibliography

### Time Estimate

- **Setup**: 5 minutes
- **Paper discovery**: 30-60 minutes
- **Semantic exploration**: 30 minutes
- **Note-taking**: 2-3 hours
- **Draft writing**: 4-8 hours
- **Total**: 1-2 days

### Tips

- Start broad, narrow with semantic search
- Take notes immediately after reading papers
- Use semantic queries to find gaps in coverage
- Save work frequently to notes/
- Review project status to track progress

---

## Paper Discovery & Analysis

**Goal**: Find the most important papers on a new topic you're unfamiliar with.

### Step-by-Step Process

#### 1. Initial Search

```
Search for recent survey papers on "federated learning" from 2023-2024
```

**Look for**: Papers with "survey", "review", "systematic" in title.

#### 2. Get Survey Paper Details

```
Get detailed information for paper ID abc123
```

**Analyze**:
- Reference count (comprehensive surveys cite 50-200+ papers)
- Citation count (quality indicator)
- Open access PDF availability

#### 3. Find Foundational Papers

From survey paper references:
```
Get detailed information for paper xyz789 [cited as foundational]
```

Identify 5-10 most-cited papers as foundation.

#### 4. Track Citation Relationships

```
Get paper abc123 with fields: ["citations", "references"]
```

**Create citation map**:
```
Save citation network to "notes/citation-map.md":

# Federated Learning Citation Network

## Foundational Papers (2016-2018)
- McMahan 2017: Communication-efficient learning (5000+ citations)
- ...

## Key Follow-ups (2019-2021)
- Li 2020: Federated optimization (cited by 50+ papers in dataset)
- ...

## Recent Work (2022-2024)
- New directions identified...
```

#### 5. Identify Research Clusters

Build semantic index and query:
```
Index the 50 papers I've found
```

```
Query similar papers about "privacy-preserving techniques in federated learning"
```

```
Query similar papers about "communication efficiency in distributed training"
```

**Result**: Identifies sub-topics and research clusters.

#### 6. Find Gaps

Compare clusters:
```
Save research gaps analysis to "notes/research-gaps.md":

# Research Gaps Analysis

## Well-covered Areas
- Privacy mechanisms (20+ papers)
- Communication protocols (15+ papers)

## Underexplored Areas
- Federated learning for time-series (2 papers found)
- Cross-silo vs cross-device comparison (3 papers)

## Potential Contributions
Based on gap analysis, potential research directions...
```

#### 7. Create Paper Database

```
Save structured paper database to "papers/database.json":
{
  "foundational": [
    {
      "key": "mcmahan2017",
      "title": "...",
      "reason": "Introduced federated averaging",
      "citations": 5000
    }
  ],
  "clusters": {
    "privacy": ["paper1", "paper2"],
    "efficiency": ["paper3", "paper4"]
  }
}
```

### Time Estimate

- **Initial search**: 15 minutes
- **Survey analysis**: 1 hour
- **Deep dive**: 2-3 hours
- **Gap analysis**: 1-2 hours
- **Total**: 4-6 hours

### Tips

- Start with surveys/reviews to get landscape
- Follow citation chains bidirectionally
- Use semantic search to cluster related papers
- Document gaps as you notice them
- Create visual citation maps if possible

---

## Citation Management Workflow

**Goal**: Maintain organized, accurate bibliography for your research.

### Step-by-Step Process

#### 1. Set Up Bibliography

```
Initialize project "my-research"
```

Creates empty references.bib file.

#### 2. Add Citations During Research

As you find important papers:

```
Add citation with key "smith2024novel":
@article{smith2024novel,
  title={A Novel Approach to X},
  author={Smith, John and Doe, Jane},
  journal={Journal of Research},
  year={2024},
  volume={10},
  pages={123-145}
}
```

#### 3. Batch Citation Import

If you have multiple papers:

```
Get detailed information for papers: abc123, def456, ghi789
```

For each result, generate BibTeX and add:

```
Add citation with key "author2024title": [generated bibtex]
```

#### 4. Organize by Topic

```
Save citation organization to "notes/citations-by-topic.md":

# Citations Organized by Topic

## Deep Learning Fundamentals
- goodfellow2016deep
- lecun2015deep

## Transformers
- vaswani2017attention
- devlin2018bert
- brown2020language

## Applications
- ...
```

#### 5. Verify Bibliography

```
Show me all citations in my bibliography
```

**Check for**:
- Duplicate keys
- Consistent naming convention
- Complete metadata (title, author, year, venue)

#### 6. Export for Writing

Copy references.bib to your paper directory:

```
Read references.bib
```

Then use in LaTeX:
```latex
\bibliographystyle{plain}
\bibliography{references}

In text: \cite{vaswani2017attention}
```

#### 7. Update as You Write

When citing new papers:

1. Search for the paper
2. Get BibTeX from paper details
3. Add to references.bib immediately
4. Document in notes/

### Best Practices

#### Citation Key Convention

Choose one convention and stick to it:

- **author_year_keyword**: `vaswani2017attention`
- **firstauthor_etal_year**: `vaswani_etal_2017`
- **shorttitle_year**: `attention_2017`

#### Required Fields

Always include:
- title
- author (all authors or use "and others")
- year
- venue (journal/conference)

Optional but recommended:
- volume, number, pages
- doi or url
- abstract (for your reference)

#### Organization

Create topic-based citation lists in notes/:
```
notes/
├── citations-by-topic.md
├── foundational-papers.md
├── recent-work-2024.md
└── to-read.md
```

### Time Estimate

- **Per citation**: 2-3 minutes
- **Batch import (10 papers)**: 20-30 minutes
- **Organization**: 30 minutes
- **Maintenance**: 5-10 minutes per writing session

---

## RAG-Powered Research Exploration

**Goal**: Use semantic search to explore research questions and discover connections.

### Step-by-Step Process

#### 1. Collect Diverse Papers

```
Search for papers on "natural language processing" from 2022-2024, limit 100
```

Cast a wide net initially.

#### 2. Build Knowledge Base

```
Index all 100 papers I found
```

**Wait time**: 30-60 seconds for embedding generation.

#### 3. Ask Research Questions

Use natural language queries:

```
Query similar papers about "How do language models understand context?"
```

```
Query similar papers about "What makes a good evaluation metric for text generation?"
```

```
Query similar papers about "Can transformers learn to reason?"
```

#### 4. Follow Connections

For each query result, dive deeper:

```
Get detailed information for paper abc123 [from query results]
```

```
Query similar papers about "reasoning capabilities in transformer models" [refined query]
```

#### 5. Map Research Landscape

```
Save research landscape to "notes/research-map.md":

# NLP Research Landscape 2022-2024

## Core Questions

### Question 1: Contextual Understanding
- Query revealed 8 papers
- Key approaches: attention visualization, probing tasks
- Gap: Limited work on cross-lingual context

### Question 2: Evaluation Metrics
- Query revealed 12 papers
- Consensus: Human evaluation still gold standard
- Controversy: Disagreement on automatic metrics

### Question 3: Reasoning Capabilities
- Query revealed 15 papers
- Split: Emergent reasoning vs. pattern matching debate
- Active area: Chain-of-thought prompting
```

#### 6. Identify Clusters

Use minimum similarity threshold:

```
Query similar papers about "reasoning" with minimum similarity 0.8
```

High similarity = tight cluster (specific sub-topic)

```
Query similar papers about "reasoning" with minimum similarity 0.5
```

Lower similarity = broader connections (related topics)

#### 7. Find Surprising Connections

```
Query similar papers about "visual reasoning in multimodal models"
```

**Unexpected result**: Papers on embodied AI, not just vision-language models.

Document:
```
Save surprising connections to "notes/unexpected-findings.md":

# Unexpected Research Connections

## Visual Reasoning → Embodied AI
Query about multimodal reasoning returned papers on:
- Robot learning
- Physical world understanding
- Simulation environments

**Insight**: Reasoning isn't just language - requires grounding
```

#### 8. Iterative Refinement

Based on findings, search for more papers:

```
Search for papers on "embodied AI reasoning" from 2023-2024
```

Index new papers:
```
Index the 20 new papers on embodied AI
```

Continue exploration cycle.

### Advanced Techniques

#### Comparative Queries

```
Query similar papers about "BERT vs GPT architectures - what are the tradeoffs?"
```

Returns papers comparing approaches.

#### Gap Finding

```
Query similar papers about "combining symbolic reasoning with neural networks"
```

Low similarity scores = underexplored area.

#### Trend Detection

Query same topic across different year ranges:
```
# 2020-2021
Query similar papers about "few-shot learning"

# 2022-2024  
Query similar papers about "few-shot learning"
```

Compare results to see trend evolution.

### Time Estimate

- **Initial collection**: 30 minutes
- **Index building**: 2-5 minutes
- **Exploration queries**: 1-2 hours
- **Documentation**: 1 hour
- **Iterative refinement**: Ongoing
- **Total initial pass**: 3-4 hours

### Tips

- Start with 50-100 papers minimum for good coverage
- Use natural language questions, not keywords
- Vary similarity thresholds to explore broadly vs. specifically
- Document surprising findings immediately
- Re-index when adding significant new papers
- Use queries to validate your understanding

---

## Project Organization Workflow

**Goal**: Maintain organized research project as it grows.

### Initial Setup

```
Initialize project "long-term-research"
```

### Weekly Maintenance

#### Monday: New Papers

```
Search for recent papers on [your topic] from last week
```

```
Save new papers metadata to "papers/weekly-2024-01-15.json"
```

#### Wednesday: Update Index

```
Index papers from papers/weekly-2024-01-15.json
```

Keeps semantic search current.

#### Friday: Status Review

```
Show me my project status
```

**Review**:
- Papers collected this week
- Notes created
- Citations added

### Monthly Cleanup

#### Organize Notes

```
Read all files in notes/
```

Consolidate related notes:
```
Save consolidated summary to "notes/monthly-summary-2024-01.md"
```

#### Citation Audit

```
Show me all citations
```

Check for:
- Uncited papers (in papers/ but not in references.bib)
- Cited but not filed (in references.bib but no PDF/metadata)

#### Archive Old Work

```
Save project snapshot to "archive/2024-01-snapshot.md":

# Project Snapshot - January 2024

## Stats
- Papers: 150
- Notes: 45
- Citations: 78

## Key Findings
[Summary of month's work]

## Next Steps
[Plans for next month]
```

### File Organization Patterns

#### By Topic
```
papers/
├── topic-1-fundamentals/
├── topic-2-applications/
└── topic-3-theory/
```

#### By Date
```
papers/
├── 2024-01/
├── 2024-02/
└── 2024-03/
```

#### By Status
```
papers/
├── to-read/
├── reading/
├── read/
└── cited/
```

### Automation Ideas

Create scripts for common tasks:

```python
# weekly_update.py
# 1. Search for new papers
# 2. Save to weekly file
# 3. Update index
# 4. Generate summary
```

### Time Estimate

- **Weekly maintenance**: 30 minutes
- **Monthly cleanup**: 1-2 hours
- **Organization setup**: 1 hour initially

---

## Multi-Topic Research

**Goal**: Research multiple related topics simultaneously.

### Setup

```
Initialize project "multi-topic-survey"
```

Create topic-specific subdirectories:
```
Save topic structure to "notes/topics.md":

# Research Topics

## Topic 1: Transformers
- papers/transformers/
- notes/transformers/

## Topic 2: Vision Models  
- papers/vision/
- notes/vision/

## Topic 3: Multimodal
- papers/multimodal/
- notes/multimodal/
```

### Per-Topic Workflow

#### Topic 1: Transformers

```
Search for papers on "transformer architectures" from 2023-2024
```

```
Save results to "papers/transformers/search-results.json"
```

```
Index papers from transformers search
```

#### Topic 2: Vision Models

```
Search for papers on "vision transformers" from 2023-2024
```

```
Save results to "papers/vision/search-results.json"
```

```
Index papers from vision search
```

### Cross-Topic Analysis

```
Query similar papers about "how are transformers adapted for vision tasks?"
```

**Result**: Returns papers from both topics showing connections.

```
Save cross-topic analysis to "notes/cross-cutting/transformers-vision.md":

# Transformers in Vision: Cross-Topic Analysis

## Papers from Transformers Topic
- [List with relevance to vision]

## Papers from Vision Topic  
- [List with transformer connections]

## Key Insights
- Attention mechanisms transfer directly
- Positional encoding differs (2D vs 1D)
- ...
```

### Unified Bibliography

Keep single references.bib with prefixed keys:

```
Add citation "trans_vaswani2017": [original transformer]
Add citation "vision_dosovitskiy2020": [vision transformer]
Add citation "multi_radford2021": [CLIP multimodal]
```

### Topic Status Tracking

```
Save research progress to "notes/progress.md":

# Research Progress

## Transformers (70% complete)
- Papers: 45
- Notes: 12
- Status: Literature review drafted

## Vision (40% complete)
- Papers: 30
- Notes: 6
- Status: Still collecting papers

## Multimodal (20% complete)
- Papers: 15
- Notes: 3
- Status: Initial exploration
```

### Time Estimate

- **Per topic setup**: 1 hour
- **Per topic research**: 4-8 hours
- **Cross-topic analysis**: 2-3 hours
- **Total**: Varies by topic count

---

## Collaborative Research Setup

**Goal**: Set up Polyhedra for team research project.

### Project Structure for Teams

```
Initialize project "team-research-2024"
```

Add collaboration guidelines:
```
Save collaboration guide to "README.md":

# Team Research Project 2024

## Team Members
- Alice: Literature review
- Bob: Methodology papers
- Carol: Applications

## Directory Structure
- papers/literature/ - Alice's papers
- papers/methodology/ - Bob's papers  
- papers/applications/ - Carol's papers
- notes/ - Individual notes (prefix with name)
- literature-review/ - Shared drafts

## Workflow
1. Each member searches their area
2. Add citations immediately
3. Index papers weekly
4. Cross-reference using semantic queries

## Citation Key Convention
[area]_[author]_[year]_[keyword]
Example: lit_smith2024survey
```

### Role-Based Workflows

#### Alice (Literature Review)

```
Search for survey papers on [topic] from 2020-2024
```

```
Save papers to "papers/literature/surveys.json"
```

```
Save literature review notes to "notes/alice-lit-review.md"
```

#### Bob (Methodology)

```
Search for papers on [methods] from 2022-2024
```

```
Save papers to "papers/methodology/methods.json"
```

```
Save methodology analysis to "notes/bob-methods.md"
```

#### Carol (Applications)

```
Search for papers on [applications] from 2023-2024
```

```
Save papers to "papers/applications/apps.json"
```

```
Save application examples to "notes/carol-applications.md"
```

### Weekly Team Sync

#### Monday: Share Findings

Each member:
```
Show project status
```

Share in team meeting what was added this week.

#### Wednesday: Cross-Reference

Build unified index:
```
Index all papers from papers/literature/, papers/methodology/, and papers/applications/
```

Team semantic search session:
```
Query similar papers about "how are these methods applied in practice?"
```

Reveals connections between Bob's and Carol's work.

#### Friday: Bibliography Update

```
Show all citations
```

Check for:
- No duplicate keys
- Consistent naming
- All team members' papers included

### Shared Deliverables

#### Unified Literature Review

```
Save team literature review to "literature-review/full-draft.md":

# Team Literature Review

## Background (Alice)
[Alice's section]

## Methodology (Bob)  
[Bob's section]

## Applications (Carol)
[Carol's section]

## Integration
[Team discussion of connections]
```

#### Master Bibliography

Single references.bib with all citations:
- Prefixed by area (lit_, meth_, app_)
- Maintained by all team members
- Updated as papers are added

### Conflict Resolution

If multiple people add same paper with different keys:

```
Show all citations
```

Find duplicates, standardize on one key:
```
# Update references.bib manually to use consistent key
# Update team notes to use consistent key
```

### Time Estimate

- **Initial setup**: 2 hours (team meeting)
- **Per member weekly**: 3-5 hours
- **Team sync**: 1 hour per week
- **Integration work**: 2-3 hours per week

---

## Summary

These workflows demonstrate:

1. **Systematic approach**: Initialize → Search → Index → Query → Document
2. **Iterative refinement**: Start broad, narrow with semantic search
3. **Organization**: Maintain structure as project grows
4. **Collaboration**: Share index and bibliography across team
5. **Documentation**: Save findings immediately to notes/

### Workflow Selection Guide

- **New topic**: Literature Review Workflow
- **Unfamiliar area**: Paper Discovery & Analysis
- **Writing paper**: Citation Management Workflow
- **Exploring connections**: RAG-Powered Research Exploration
- **Long-term project**: Project Organization Workflow
- **Multiple topics**: Multi-Topic Research
- **Team project**: Collaborative Research Setup

### Key Principles

1. **Search first**: Gather papers before deep analysis
2. **Index early**: Build semantic search capability quickly
3. **Document continuously**: Save notes as you learn
4. **Use semantic queries**: Let RAG find connections
5. **Maintain bibliography**: Add citations immediately
6. **Check status regularly**: Use project status to track progress

---

For detailed API documentation, see [API.md](API.md).
For troubleshooting, see [ERROR_HANDLING.md](ERROR_HANDLING.md).
