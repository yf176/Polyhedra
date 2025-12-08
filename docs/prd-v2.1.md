# Polyhedra - Product Requirements Document v2.1

## Document Control

| Field | Value |
|-------|-------|
| **Project Name** | Polyhedra |
| **Version** | 2.1.0 |
| **Type** | Hybrid MCP Server (Tools + Limited Agent) |
| **Status** | Draft |
| **Created** | November 30, 2025 |
| **Last Updated** | November 30, 2025 |
| **Author** | Product Team |
| **Stakeholders** | Engineering, Research Community |

### Revision History

| Version | Date | Author | Changes |
|---------|------|--------|----------|
| 2.1.0 | 2025-11-30 | Product Team | Added literature review generation capability |
| 2.0.0 | 2024-11-26 | Product Team | BREAKING: Removed internal LLM calls, simplified to pure MCP tool server |
| 1.x | - | Product Team | Legacy versions with built-in LLM agents |

---

## Executive Summary

### Purpose

Polyhedra is a **hybrid MCP server** that augments IDE-based AI assistants with academic research capabilities. Version 2.1 introduces **literature review generation** as the first built-in agent capability, while maintaining the pure tool server approach for other features.

### Key Capabilities

- **Paper Discovery**: Search and retrieve academic papers via Semantic Scholar API
- **Citation Management**: Automated BibTeX generation and reference management
- **RAG Retrieval**: Semantic search across indexed papers for relevant citations
- **Context Management**: Read/write project files for research workflow
- **Project Scaffolding**: Initialize standardized research project structures
- **🆕 Literature Review Generation**: AI-powered synthesis of research papers into structured reviews

### Target Audience

- ML/AI researchers using modern IDEs with AI assistants
- PhD students requiring streamlined research workflows
- Academic professionals seeking IDE-integrated paper management

### Success Criteria

- Sub-2-second paper search response time
- 100% valid BibTeX generation
- Literature review quality: Coherent, well-structured, properly cited
- Support for 4+ major IDEs (Cursor, Copilot, Windsurf, VS Code)
- Setup time under 10 minutes (increased due to LLM config)

---

## 1. Product Overview

### 1.1 Vision

Polyhedra is a **hybrid MCP server** that provides both:
1. **Pure tools** for data access (search, citations, files)
2. **Limited agent capabilities** for complex synthesis tasks (literature review)

This design balances simplicity with capability—keeping most features as passive tools while adding AI where synthesis is truly needed.

### 1.2 Architecture Philosophy (v2.1)

**Two Deployment Modes**:

#### Mode 1: Pure MCP Server (Default)
Traditional tool server that IDE's AI can call directly.

```
┌─────────────────────────────────────────────────────────────────┐
│                    IDE (Cursor / Copilot)                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                IDE's LLM (Claude/GPT)                     │  │
│  │  • Intent understanding                                   │  │
│  │  • Paper writing                                          │  │
│  │  • Hypothesis generation                                  │  │
│  │  • Method design                                          │  │
│  └─────────────────────┬─────────────────────────────────────┘  │
│                        │ MCP Protocol                            │
│  ┌─────────────────────▼─────────────────────────────────────┐  │
│  │              Polyhedra MCP Server v2.1                    │  │
│  │                                                           │  │
│  │  Pure Tools (no LLM):                                    │  │
│  │  • Paper search (Semantic Scholar API)                   │  │
│  │  • Context management (project files)                    │  │
│  │  • RAG retrieval (relevant papers)                       │  │
│  │  • Citation management (BibTeX)                          │  │
│  │  • File read/write                                       │  │
│  │                                                           │  │
│  │  🆕 Agent Capabilities (with LLM):                       │  │
│  │  • Literature review generation                          │  │
│  │    └─> Calls LLM for synthesis                          │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

#### Mode 2: Custom Agent (BMAD-style) 🆕
Packaged as an autonomous agent within the IDE.

```
┌─────────────────────────────────────────────────────────────────┐
│                         IDE (Cursor)                            │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │         Polyhedra Research Agent (Custom Agent)        │    │
│  │                                                        │    │
│  │  ┌──────────────────────────────────────────────┐     │    │
│  │  │         Agent Orchestration Layer            │     │    │
│  │  │  • User intent understanding                 │     │    │
│  │  │  • Task planning & execution                 │     │    │
│  │  │  • Multi-step workflow coordination          │     │    │
│  │  │  • Error handling & recovery                 │     │    │
│  │  └──────────────┬───────────────────────────────┘     │    │
│  │                 │                                      │    │
│  │  ┌──────────────▼───────────────────────────────┐     │    │
│  │  │              Agent's LLM                      │     │    │
│  │  │         (Claude/GPT via IDE)                  │     │    │
│  │  └──────────────┬───────────────────────────────┘     │    │
│  │                 │ Internal Tool Calls                  │    │
│  │  ┌──────────────▼───────────────────────────────┐     │    │
│  │  │           Polyhedra Tools                     │     │    │
│  │  │  • search_papers                              │     │    │
│  │  │  • generate_literature_review                 │     │    │
│  │  │  • query_similar_papers                       │     │    │
│  │  │  • add_citation                               │     │    │
│  │  │  • save_file                                  │     │    │
│  │  └───────────────────────────────────────────────┘     │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  User: "@research efficient transformers"                      │
│  Agent: [Autonomously executes: search → index → review]       │
└─────────────────────────────────────────────────────────────────┘
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
| **🆕 Generate literature review** | **✓ (built-in)** | |
| Understand user intent | | ✓ |
| Generate hypotheses | | ✓ |
| Write paper sections | | ✓ |
| Decide workflow | | ✓ |

### 1.4 Design Rationale: Why Add Literature Review?

**Why literature review needs built-in LLM**:
1. **Synthesis complexity**: Requires reading 20-100 papers and synthesizing themes
2. **Structured output**: Needs taxonomy, gaps analysis, citation weaving
3. **Context window limits**: IDE's LLM may hit token limits with 50+ papers
4. **Specialized prompts**: Literature review has domain-specific patterns

**Why other features stay as tools**:
- Search: Data retrieval only
- Citations: Deterministic operations
- Files: Simple I/O
- RAG: Vector similarity computation

**Hybrid approach benefits**:
- Keep simplicity where possible
- Add intelligence where necessary
- Users can still override (regenerate with IDE's LLM if preferred)

### 1.4.1 Custom Agent Mode (BMAD-style) 🆕

**What is Custom Agent Mode?**

Polyhedra can be deployed as a **self-contained research agent** within IDEs (like Cursor's Custom Agents or GitHub Copilot Agents), similar to how BMAD (Build-Measure-Analyze-Debug) works.

**Key Differences from Pure MCP**:

| Aspect | Pure MCP Mode | Custom Agent Mode |
|--------|---------------|-------------------|
| **User Interaction** | User explicitly calls tools | User gives high-level command |
| **Orchestration** | IDE's LLM decides | Agent decides internally |
| **Workflow** | Step-by-step manual | Autonomous multi-step |
| **Example** | "search papers X" → "generate review" | "@research X" → [auto: search+index+review] |
| **Control** | Full user control | Agent autonomy with checkpoints |

**Custom Agent Capabilities**:

1. **Natural Language Commands**:
   ```
   User: "@research efficient vision transformers"
   Agent: [Understands intent]
          ├─ Step 1: Search papers (50 results)
          ├─ Step 2: Index for RAG
          ├─ Step 3: Generate literature review
          └─ Step 4: Save to literature/review.md
          
          ✓ Complete! Review saved with 47 citations.
   ```

2. **Multi-step Workflows**:
   - Literature survey workflow
   - Paper comparison workflow
   - Citation finding workflow
   - Research gap analysis workflow

3. **Proactive Suggestions**:
   ```
   Agent: "I found 47 papers. Would you like me to:
           1. Generate a full review
           2. Show top 10 most cited papers first
           3. Focus on a specific sub-topic"
   ```

4. **Error Recovery**:
   ```
   Agent: "Failed to fetch 3 papers due to API timeout.
           Continuing with 44 papers. Retry failed papers? [Y/n]"
   ```

**Architecture: Custom Agent Implementation**:

```python
# polyhedra/agent/research_agent.py

class PolyhedraResearchAgent:
    """
    Custom Agent for autonomous research workflows.
    Inspired by BMAD's autonomous task execution.
    """
    
    def __init__(self, llm_client, tools):
        self.llm = llm_client
        self.tools = tools
        self.workflows = self._load_workflows()
    
    async def handle_command(self, command: str) -> str:
        """
        Main entry point for custom agent.
        
        Supported commands:
        - @research <topic>
        - @compare <paper1> <paper2>
        - @find-gaps <topic>
        - @cite <query>
        """
        
        # Parse intent
        intent = await self._understand_intent(command)
        
        # Select workflow
        workflow = self.workflows.get(intent["type"])
        if not workflow:
            return "Unknown command. Try: @research <topic>"
        
        # Execute workflow
        result = await workflow.execute(intent["params"])
        
        return result.summary
    
    async def _understand_intent(self, command: str) -> dict:
        """Use LLM to understand user intent"""
        
        prompt = f"""
        Analyze this research command and extract intent:
        
        Command: {command}
        
        Available workflows:
        - research: Comprehensive literature survey
        - compare: Side-by-side paper comparison
        - find_gaps: Research gap identification
        - cite: Find relevant citations for writing
        
        Return JSON:
        {{
            "type": "workflow_name",
            "params": {{
                "topic": "...",
                "focus": "...",
                "depth": "standard"
            }}
        }}
        """
        
        response = await self.llm.complete(prompt)
        return json.loads(response)
    
    def _load_workflows(self):
        """Load pre-defined multi-step workflows"""
        return {
            "research": LiteratureSurveyWorkflow(self.tools),
            "compare": PaperComparisonWorkflow(self.tools),
            "find_gaps": GapAnalysisWorkflow(self.tools),
            "cite": CitationFindingWorkflow(self.tools)
        }


class LiteratureSurveyWorkflow:
    """
    Multi-step workflow for literature survey.
    Similar to BMAD's build-measure-analyze cycle.
    """
    
    def __init__(self, tools):
        self.tools = tools
        self.steps = [
            SearchPapersStep(),
            IndexPapersStep(),
            GenerateReviewStep(),
            IdentifyGapsStep(),
            SaveOutputsStep()
        ]
    
    async def execute(self, params: dict) -> WorkflowResult:
        """Execute all steps with error handling"""
        
        context = {"params": params, "artifacts": {}}
        
        for step in self.steps:
            try:
                # Execute step
                result = await step.run(context, self.tools)
                
                # Update context
                context["artifacts"][step.name] = result
                
                # User checkpoint (optional)
                if step.requires_approval:
                    approved = await self._request_approval(step, result)
                    if not approved:
                        return WorkflowResult.cancelled(step.name)
                
            except Exception as e:
                # Error recovery
                recovered = await self._handle_error(step, e, context)
                if not recovered:
                    return WorkflowResult.failed(step.name, str(e))
        
        return WorkflowResult.success(context["artifacts"])
    
    async def _request_approval(self, step, result):
        """Request user approval at checkpoint"""
        # Implementation depends on IDE's interaction model
        pass
    
    async def _handle_error(self, step, error, context):
        """Attempt to recover from error"""
        # Retry logic, fallbacks, etc.
        pass


class SearchPapersStep:
    """Step 1: Search papers"""
    
    name = "search_papers"
    requires_approval = False
    
    async def run(self, context, tools):
        topic = context["params"]["topic"]
        limit = context["params"].get("limit", 50)
        
        papers = await tools.search_papers(
            query=topic,
            limit=limit
        )
        
        return {
            "papers": papers,
            "count": len(papers),
            "message": f"Found {len(papers)} papers on '{topic}'"
        }


class GenerateReviewStep:
    """Step 3: Generate literature review"""
    
    name = "generate_review"
    requires_approval = True  # User can preview papers before review
    
    async def run(self, context, tools):
        papers = context["artifacts"]["search_papers"]["papers"]
        
        review = await tools.generate_literature_review(
            papers=papers,
            focus=context["params"].get("focus"),
            depth=context["params"].get("depth", "standard")
        )
        
        return {
            "review_text": review["review"],
            "word_count": review["metadata"]["word_count"],
            "gaps": review["metadata"]["research_gaps"],
            "cost": review["cost"]["total_usd"],
            "message": f"Generated {review['metadata']['word_count']}-word review"
        }
```

**IDE Integration (Cursor Example)**:

```json
// .cursor/agents/polyhedra.json
{
  "name": "Polyhedra Research Agent",
  "description": "Autonomous research assistant for academic literature",
  "trigger": "@research",
  "capabilities": [
    "literature_survey",
    "paper_comparison",
    "gap_analysis",
    "citation_finding"
  ],
  "tools": [
    "search_papers",
    "get_paper",
    "generate_literature_review",
    "query_similar_papers",
    "add_citation",
    "save_file"
  ],
  "system_prompt": "You are an expert research assistant...",
  "autonomy_level": "supervised",  // Request approval at checkpoints
  "error_handling": "recover"      // Attempt recovery before failing
}
```

**Usage Examples**:

```
# Example 1: Simple research survey
User: @research efficient vision transformers

Agent: Starting literature survey on "efficient vision transformers"...

       [Step 1/5] Searching papers...
       ✓ Found 47 papers from Semantic Scholar
       
       [Step 2/5] Indexing papers for RAG...
       ✓ Indexed 47 papers (embeddings cached)
       
       [Step 3/5] Generating literature review...
       ⚠️ This will cost ~$0.15. Continue? [Y/n]
       
User: Y

Agent: ✓ Generated 4,523-word review
       ✓ Identified 5 research gaps
       ✓ Added 47 citations to references.bib
       ✓ Saved to literature/review.md
       
       📄 Preview:
       # Literature Review: Efficient Vision Transformers
       
       ## Overview
       Vision Transformers have demonstrated remarkable...
       
       [Read full review] [Regenerate with focus] [Export]


# Example 2: Focused research with constraints
User: @research sparse attention mechanisms 
      --years 2023-2024 
      --focus "scaling beyond 1B parameters"
      --depth brief

Agent: Customizing search:
       • Time range: 2023-2024
       • Focus: scaling beyond 1B parameters
       • Depth: brief (2-3 pages)
       
       [Executing workflow...]
       
       ✓ Found 23 papers (filtered by year)
       ✓ Generated brief review (2,100 words)
       ✓ Cost: $0.08
       
       Key finding: Only 3 papers address scaling >1B
       → This could be a good research gap to explore!


# Example 3: Compare two papers
User: @compare arxiv:2304.12345 arxiv:2305.67890

Agent: Comparing two papers:
       1. "EfficientViT" (Liu et al., 2023)
       2. "MobileViT v2" (Mehta et al., 2023)
       
       [Fetching papers...]
       
       ✓ Generated comparison table:
       
       | Aspect | EfficientViT | MobileViT v2 |
       |--------|--------------|--------------|
       | Method | Sparse attention | Hybrid CNN-ViT |
       | Params | 32M | 18M |
       | FLOPs | 2.1G | 1.8G |
       | Accuracy | 82.3% | 81.7% |
       
       [Full comparison] [Add to review] [Export]


# Example 4: Find citations while writing
User: @cite "methods for reducing transformer memory footprint"

Agent: Finding relevant papers for:
       "methods for reducing transformer memory footprint"
       
       [Querying indexed papers...]
       
       Top 5 relevant citations:
       1. [@vaswani2017attention] - Original transformer (baseline)
       2. [@kitaev2020reformer] - Reversible layers
       3. [@dao2022flashattention] - Memory-efficient attention
       4. [@liu2023efficientvit] - Architecture optimization
       5. [@child2019generating] - Sparse transformers
       
       [Insert citations] [See abstracts] [Add to bib]
```

**Benefits of Custom Agent Mode**:

1. **Reduced cognitive load**: User gives intent, agent handles details
2. **Consistent workflows**: Pre-defined best practices
3. **Error resilience**: Automatic retry and recovery
4. **Cost awareness**: Warns before expensive operations
5. **Contextual help**: Suggests next steps based on current state

**Comparison with BMAD**:

| Feature | BMAD | Polyhedra Agent |
|---------|------|-----------------|
| **Domain** | Software debugging | Research literature |
| **Workflow** | Build → Measure → Analyze → Debug | Search → Index → Review → Analyze |
| **Autonomy** | Fully autonomous | Supervised (checkpoints) |
| **Tools** | Compiler, debugger, profiler | Search, RAG, LLM synthesis |
| **Output** | Bug fixes | Literature reviews, gaps |
| **Iteration** | Until bug fixed | Until research question answered |

### 1.5 Target Users

- ML/AI researchers using Cursor, Copilot, or Windsurf
- PhD students who want AI-assisted literature synthesis
- Anyone who wants academic paper tools in their IDE

### 1.6 Tech Stack

```yaml
language: Python 3.11+
mcp_framework: mcp (official SDK)
http_client: httpx
data_validation: Pydantic
bibtex_parser: bibtexparser
embeddings: sentence-transformers
vector_store: numpy (simple cosine similarity)
package_manager: uv

# 🆕 New in v2.1
llm_providers:
  - anthropic (Claude)
  - openai (GPT-4)
  - configurable via environment

# 🆕 Custom Agent Mode
agent_framework:
  - workflow_engine: custom (inspired by BMAD)
  - state_management: in-memory with persistence
  - error_recovery: retry with exponential backoff
  - checkpoints: user approval at key steps

supported_ides:
  - Cursor (with Custom Agents support)
  - GitHub Copilot (with Agents support)
  - Windsurf
  - VS Code (with MCP extension)

deployment_modes:
  - mode_1: Pure MCP Server (tool calls)
  - mode_2: Custom Agent (autonomous workflows)
```

### 1.7 Deployment Modes Comparison

| Aspect | Mode 1: Pure MCP | Mode 2: Custom Agent |
|--------|------------------|----------------------|
| **Best For** | Power users, flexible integration | Beginners, streamlined workflows |
| **User Control** | Full (every step) | Partial (checkpoints) |
| **Setup Complexity** | Low (just install server) | Medium (agent config + server) |
| **Learning Curve** | Steep (must know all tools) | Gentle (natural language commands) |
| **Flexibility** | High (any combination) | Medium (pre-defined workflows) |
| **Error Handling** | Manual | Automatic retry |
| **Example Use** | "search_papers X" → "index" → "generate_review" | "@research X" |
| **Cost Predictability** | User-controlled | Agent-estimated (with warnings) |

**Recommendation**: 
- Start with **Mode 2** (Custom Agent) for ease of use
- Switch to **Mode 1** (Pure MCP) for advanced customization

---

## 2. Multi-Agent Research System 🆕

### 2.1 Overview

Polyhedra v2.1 introduces a **multi-agent research system** that covers the complete academic research lifecycle. Inspired by BMAD's autonomous approach, each specialized agent handles a distinct phase of research, from literature review to paper publication.

### 2.2 Research Lifecycle Coverage

```
Complete Research Pipeline:
┌────────────────────────────────────────────────────────────────┐
│                    Research Lifecycle                          │
├────────────────────────────────────────────────────────────────┤
│  1. Literature Review    →  LiteratureAgent                    │
│  2. Hypothesis Generation →  HypothesisAgent                   │
│  3. Method Design        →  MethodAgent                        │
│  4. Experiment Planning  →  ExperimentAgent                    │
│  5. Result Analysis      →  AnalysisAgent                      │
│  6. Paper Writing        →  WritingAgent                       │
│  7. Review & Revision    →  ReviewAgent                        │
└────────────────────────────────────────────────────────────────┘
```

### 2.3 Multi-Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│              PolyhedraAgentOrchestrator                         │
│         (Coordinator / Research Project Manager)                │
│                                                                 │
│  • Understands user's research goal                            │
│  • Plans which agents to invoke                                │
│  • Manages state across research stages                        │
│  • Coordinates agent handoffs                                  │
└────────────┬────────────────────────────────────────────────────┘
             │
             ├──────────────────────────────────────────────────┐
             │                                                  │
   ┌─────────▼─────────┐  ┌──────────────┐  ┌──────────────┐  │
   │ LiteratureAgent   │  │ HypothesisAgent│ │ MethodAgent  │  │
   │                   │  │                │  │              │  │
   │ • Search papers   │  │ • Identify gaps│  │ • Design     │  │
   │ • Generate review │  │ • Generate     │  │   experiments│  │
   │ • Identify gaps   │  │   hypotheses   │  │ • Plan       │  │
   │ • Save artifacts  │  │ • Evaluate     │  │   methodology│  │
   └───────────────────┘  │   novelty      │  │ • Resource   │  │
                          └────────────────┘  │   estimation │  │
                                              └──────────────┘  │
             │                                                  │
   ┌─────────▼─────────┐  ┌──────────────┐  ┌──────────────┐  │
   │ ExperimentAgent   │  │ AnalysisAgent│  │ WritingAgent │  │
   │                   │  │              │  │              │  │
   │ • Setup code      │  │ • Parse      │  │ • Draft      │  │
   │ • Run experiments │  │   results    │  │   sections   │  │
   │ • Monitor progress│  │ • Generate   │  │ • Cite papers│  │
   │ • Handle failures │  │   plots      │  │ • Format     │  │
   └───────────────────┘  │ • Statistical│  │   references │  │
                          │   tests      │  └──────────────┘  │
                          └──────────────┘                     │
             │                                                  │
   ┌─────────▼─────────┐                                       │
   │ ReviewAgent       │                                       │
   │                   │                                       │
   │ • Self-review     │                                       │
   │ • Quality checks  │                                       │
   │ • Suggest edits   │                                       │
   │ • Check citations │                                       │
   └───────────────────┘                                       │
```

### 2.4 Key Concepts

**Agent**: Specialized autonomous component for one research phase
- Has specific domain expertise (literature, experiments, writing)
- Can invoke tools and make decisions
- Produces structured artifacts

**Orchestrator**: Meta-agent that coordinates specialized agents
- Understands overall research goals
- Plans agent execution sequence
- Manages handoffs and dependencies

**Checkpoint**: User approval point before critical/expensive operations

**Artifact**: Structured output from each agent (review.md, hypotheses.json, paper.tex)

**State Management**: Track progress across the entire research lifecycle

### 2.5 Specialized Agents

#### Agent 1: LiteratureAgent
```yaml
name: LiteratureAgent
trigger: "@literature <topic>" or "@research <topic>"
phase: Literature Review (Phase 1)
description: Search, analyze, and synthesize academic papers

capabilities:
  - Search academic databases (Semantic Scholar)
  - Index papers for semantic search
  - Generate structured literature reviews
  - Identify research gaps
  - Compare papers
  - Find citations for claims

workflows:
  - literature_survey: Comprehensive review generation
  - paper_comparison: Side-by-side analysis
  - gap_analysis: Identify underexplored areas
  - citation_finding: Find relevant citations

outputs:
  - literature/review.md (structured review)
  - literature/gaps.md (research opportunities)
  - literature/papers.json (paper metadata)
  - references.bib (all citations)

typical_duration: 3-5 minutes for 50 papers
typical_cost: $0.15-0.30
```

#### Agent 2: HypothesisAgent
```yaml
name: HypothesisAgent
trigger: "@hypothesize" or "@generate-ideas"
phase: Hypothesis Generation (Phase 2)
description: Generate and evaluate research hypotheses

capabilities:
  - Generate hypotheses from research gaps
  - Evaluate novelty (check against existing work)
  - Assess feasibility (resources, timeline)
  - Rank hypotheses by potential impact
  - Suggest experimental validation approaches

inputs:
  - literature/gaps.md
  - literature/papers.json
  - User constraints (budget, timeline, resources)

workflows:
  - hypothesis_generation: Create 5-10 candidate hypotheses
  - novelty_check: Verify each hypothesis is novel
  - feasibility_analysis: Estimate resources needed
  - ranking: Sort by impact × feasibility

outputs:
  - ideas/hypotheses.md (ranked list)
  - ideas/novelty-analysis.md (why each is novel)
  - ideas/feasibility.json (resource estimates)

typical_duration: 5-10 minutes
typical_cost: $0.20-0.50
```

#### Agent 3: MethodAgent
```yaml
name: MethodAgent
trigger: "@design-method" or "@plan-experiments"
phase: Method Design (Phase 3)
description: Design experimental methodology

capabilities:
  - Design experimental setup
  - Select appropriate baselines
  - Choose datasets and metrics
  - Plan ablation studies
  - Estimate computational requirements
  - Generate code scaffolding

inputs:
  - ideas/hypotheses.md (selected hypothesis)
  - User constraints (available hardware, time)

workflows:
  - method_design: Create detailed methodology
  - baseline_selection: Choose comparison methods
  - dataset_selection: Pick appropriate datasets
  - metric_selection: Define evaluation metrics
  - resource_planning: Estimate GPU hours, cost

outputs:
  - method/design.md (detailed methodology)
  - method/baselines.md (comparison methods)
  - method/experiments.yaml (experiment configs)
  - method/code_scaffold/ (initial code structure)

typical_duration: 10-15 minutes
typical_cost: $0.30-0.60
```

#### Agent 4: ExperimentAgent
```yaml
name: ExperimentAgent
trigger: "@run-experiments" or "@execute"
phase: Experiment Execution (Phase 4)
description: Setup, run, and monitor experiments

capabilities:
  - Generate experiment code from methodology
  - Setup training pipelines
  - Monitor experiment progress
  - Handle failures (auto-restart, checkpointing)
  - Log metrics to Wandb/TensorBoard
  - Alert on anomalies (NaN loss, divergence)

inputs:
  - method/experiments.yaml
  - method/code_scaffold/

workflows:
  - code_generation: Generate full training code
  - environment_setup: Install dependencies, prepare data
  - experiment_execution: Run experiments with monitoring
  - checkpoint_management: Save/restore experiment state

outputs:
  - experiments/runs/ (logs, checkpoints, configs)
  - experiments/results.json (final metrics)
  - experiments/logs.txt (execution logs)

typical_duration: Hours to days (actual experiment runtime)
typical_cost: Varies (depends on compute requirements)
agent_role: Setup and monitoring, not compute itself
```

#### Agent 5: AnalysisAgent
```yaml
name: AnalysisAgent
trigger: "@analyze-results"
phase: Result Analysis (Phase 5)
description: Analyze experimental results and generate insights

capabilities:
  - Parse experiment logs and metrics
  - Generate plots and visualizations
  - Perform statistical significance tests
  - Compare against baselines
  - Identify interesting patterns
  - Suggest follow-up experiments

inputs:
  - experiments/results.json
  - method/baselines.md

workflows:
  - metric_parsing: Extract results from logs
  - visualization: Generate plots (loss curves, accuracy tables)
  - statistical_analysis: T-tests, confidence intervals
  - comparison: Compare against baselines
  - insight_generation: Identify key findings

outputs:
  - results/analysis.md (narrative analysis)
  - results/figures/ (all plots)
  - results/tables.tex (LaTeX tables)
  - results/statistics.json (significance tests)

typical_duration: 5-10 minutes
typical_cost: $0.15-0.30
```

#### Agent 6: WritingAgent
```yaml
name: WritingAgent
trigger: "@write-paper" or "@draft <section>"
phase: Paper Writing (Phase 6)
description: Draft paper sections with proper citations

capabilities:
  - Draft paper sections (intro, related work, method, etc.)
  - Cite papers from literature review
  - Generate figure captions
  - Format references (BibTeX)
  - Check for citation completeness
  - Suggest paper structure

inputs:
  - literature/review.md
  - ideas/hypotheses.md
  - method/design.md
  - results/analysis.md
  - references.bib

workflows:
  - abstract_writing: Concise summary (250 words)
  - introduction_writing: Motivation and contributions
  - related_work_writing: Compare with existing work
  - method_writing: Describe methodology
  - results_writing: Present findings
  - conclusion_writing: Summary and future work

outputs:
  - paper/abstract.tex
  - paper/introduction.tex
  - paper/related_work.tex
  - paper/method.tex
  - paper/experiments.tex
  - paper/conclusion.tex

typical_duration: 3-5 minutes per section
typical_cost: $0.10-0.20 per section
```

#### Agent 7: ReviewAgent
```yaml
name: ReviewAgent
trigger: "@review-paper" or "@check-quality"
phase: Review & Revision (Phase 7)
description: Self-review and quality checking

capabilities:
  - Check citation completeness (all claims cited)
  - Verify figure/table references
  - Check grammar and clarity
  - Assess novelty claims
  - Suggest improvements
  - Check against venue guidelines

inputs:
  - paper/*.tex (all paper sections)
  - references.bib

workflows:
  - citation_check: Ensure all claims are cited
  - reference_check: Verify figure/table numbers
  - clarity_check: Identify unclear sentences
  - novelty_check: Verify contribution claims
  - guideline_check: Match venue requirements (page limit, format)

outputs:
  - review/checklist.md (quality checklist)
  - review/suggestions.md (improvement suggestions)
  - review/missing_citations.md (uncited claims)

typical_duration: 5-8 minutes
typical_cost: $0.20-0.40
```

### 2.6 Agent Orchestration

#### Orchestrator Design

```python
# polyhedra/orchestrator/research_orchestrator.py

class PolyhedraResearchOrchestrator:
    """
    Meta-agent that coordinates specialized agents across research lifecycle.
    Manages state, handoffs, and dependencies between agents.
    """
    
    RESEARCH_PHASES = [
        "literature_review",
        "hypothesis_generation",
        "method_design",
        "experiment_execution",
        "result_analysis",
        "paper_writing",
        "review_revision"
    ]
    
    def __init__(self, project_root: Path):
        self.project = project_root
        self.state = ResearchState.load(project_root)
        
        # Initialize all specialized agents
        self.agents = {
            "literature": LiteratureAgent(project_root),
            "hypothesis": HypothesisAgent(project_root),
            "method": MethodAgent(project_root),
            "experiment": ExperimentAgent(project_root),
            "analysis": AnalysisAgent(project_root),
            "writing": WritingAgent(project_root),
            "review": ReviewAgent(project_root)
        }
    
    async def handle_command(self, command: str) -> str:
        """
        Main entry point for research commands.
        
        Examples:
        - "@research transformers" → LiteratureAgent
        - "@hypothesize" → HypothesisAgent
        - "@write-paper" → WritingAgent
        - "@full-pipeline" → All agents in sequence
        """
        
        # Parse intent
        intent = await self._parse_intent(command)
        
        # Route to appropriate agent or pipeline
        if intent["type"] == "single_agent":
            agent = self.agents[intent["agent"]]
            result = await agent.execute(intent["params"])
            return self._format_result(result)
        
        elif intent["type"] == "pipeline":
            # Execute multiple agents in sequence
            result = await self._execute_pipeline(intent["phases"])
            return self._format_pipeline_result(result)
    
    async def _execute_pipeline(self, phases: list[str]) -> dict:
        """
        Execute multiple research phases in sequence.
        Each agent produces artifacts consumed by next agent.
        """
        
        results = {}
        
        for phase in phases:
            # Get agent for this phase
            agent = self._get_agent_for_phase(phase)
            
            # Check prerequisites
            if not self._check_prerequisites(phase):
                return {
                    "success": False,
                    "phase_failed": phase,
                    "error": f"Prerequisites not met for {phase}"
                }
            
            # Execute agent
            try:
                result = await agent.execute_for_pipeline(self.state)
                results[phase] = result
                
                # Update state with artifacts
                self.state.update(phase, result.artifacts)
                self.state.save()
                
            except Exception as e:
                return {
                    "success": False,
                    "phase_failed": phase,
                    "error": str(e),
                    "completed_phases": list(results.keys())
                }
        
        return {
            "success": True,
            "results": results
        }
    
    def _check_prerequisites(self, phase: str) -> bool:
        """Check if prerequisites for a phase are met"""
        
        prereqs = {
            "hypothesis_generation": ["literature_review"],
            "method_design": ["hypothesis_generation"],
            "experiment_execution": ["method_design"],
            "result_analysis": ["experiment_execution"],
            "paper_writing": ["literature_review", "result_analysis"],
            "review_revision": ["paper_writing"]
        }
        
        if phase not in prereqs:
            return True
        
        for prereq_phase in prereqs[phase]:
            if not self.state.is_completed(prereq_phase):
                return False
        
        return True


class ResearchState:
    """
    Tracks progress across research lifecycle.
    Persists to .polyhedra/state.json
    """
    
    def __init__(self, project_root: Path):
        self.root = project_root
        self.phases = {
            "literature_review": {"status": "not_started"},
            "hypothesis_generation": {"status": "not_started"},
            "method_design": {"status": "not_started"},
            "experiment_execution": {"status": "not_started"},
            "result_analysis": {"status": "not_started"},
            "paper_writing": {"status": "not_started"},
            "review_revision": {"status": "not_started"}
        }
        self.artifacts = {}
        self.metadata = {
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
    
    def update(self, phase: str, artifacts: dict):
        """Update state after phase completion"""
        self.phases[phase]["status"] = "completed"
        self.phases[phase]["completed_at"] = datetime.now().isoformat()
        self.artifacts[phase] = artifacts
        self.metadata["last_updated"] = datetime.now().isoformat()
    
    def is_completed(self, phase: str) -> bool:
        """Check if a phase is completed"""
        return self.phases[phase]["status"] == "completed"
    
    def save(self):
        """Persist state to disk"""
        state_file = self.root / ".polyhedra" / "state.json"
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(json.dumps({
            "phases": self.phases,
            "artifacts": self.artifacts,
            "metadata": self.metadata
        }, indent=2))
    
    @classmethod
    def load(cls, project_root: Path):
        """Load state from disk"""
        state_file = project_root / ".polyhedra" / "state.json"
        if not state_file.exists():
            return cls(project_root)
        
        data = json.loads(state_file.read_text())
        state = cls(project_root)
        state.phases = data["phases"]
        state.artifacts = data["artifacts"]
        state.metadata = data["metadata"]
        return state
```

### 2.7 Complete Research Pipeline

**End-to-End Command**:
```
User: @full-research "efficient vision transformers"

Orchestrator: Planning complete research pipeline...
             
             Phases to execute:
             1. Literature Review (3-5 min, ~$0.20)
             2. Hypothesis Generation (5-10 min, ~$0.40)
             3. Method Design (10-15 min, ~$0.50)
             4. Paper Writing (20-30 min, ~$1.00)
             5. Review & Polish (5-8 min, ~$0.30)
             
             Total estimated time: 45-70 minutes
             Total estimated cost: $2.40
             
             (Experiment execution excluded - requires compute)
             
             Proceed? [Y/n]

User: Y

Orchestrator: [Phase 1/5] Literature Review
             ├─ Searching papers... ✓ (47 papers found)
             ├─ Indexing for RAG... ✓
             ├─ Generating review... ✓ (4,200 words)
             └─ Identifying gaps... ✓ (6 gaps found)
             
             Phase 1 complete. Artifacts:
             • literature/review.md
             • literature/gaps.md
             • references.bib (47 citations)
             
             [Phase 2/5] Hypothesis Generation
             ├─ Analyzing gaps... ✓
             ├─ Generating hypotheses... ✓ (8 candidates)
             ├─ Novelty checking... ✓
             └─ Feasibility analysis... ✓
             
             Top hypothesis (ranked by impact × feasibility):
             "Structured sparse attention patterns can scale to
              10B parameters with <5% accuracy degradation"
             
             ⚠️ Checkpoint: Select hypothesis to proceed?
             1. Use top-ranked hypothesis (recommended)
             2. Review all 8 hypotheses first
             3. Generate more hypotheses

User: 1

Orchestrator: [Phase 3/5] Method Design
             ├─ Designing experiments... ✓
             ├─ Selecting baselines... ✓ (Dense ViT, EfficientViT)
             ├─ Choosing datasets... ✓ (ImageNet-1K)
             ├─ Planning metrics... ✓ (Acc, FLOPs, Latency)
             └─ Generating code scaffold... ✓
             
             Method design complete. Artifacts:
             • method/design.md
             • method/experiments.yaml
             • method/code_scaffold/
             
             ⚠️ Phase 4 (Experiments) requires manual execution
                or external compute. Run experiments, then:
                $ @analyze-results
             
             Skip to Phase 5 (Paper Writing)? [Y/n]

User: Y

Orchestrator: [Phase 5/5] Paper Writing
             ├─ Drafting abstract... ✓
             ├─ Writing introduction... ✓
             ├─ Writing related work... ✓ (cited 23 papers)
             ├─ Writing method... ✓
             ├─ Writing experiments... ✓ (placeholder results)
             └─ Writing conclusion... ✓
             
             Paper draft complete. Artifacts:
             • paper/main.tex (full paper)
             • paper/figures/ (placeholders)
             
             ✓ Research pipeline complete!
             
             Next steps:
             1. Run experiments (method/experiments.yaml)
             2. Update results in paper/experiments.tex
             3. Run quality check: @review-paper
```

### 2.8 Agent Architecture

```python
# polyhedra/agent/__init__.py

from .research_agent import PolyhedraResearchAgent
from .workflows import (
    LiteratureSurveyWorkflow,
    PaperComparisonWorkflow,
    GapAnalysisWorkflow,
    CitationFindingWorkflow
)

__all__ = [
    "PolyhedraResearchAgent",
    "LiteratureSurveyWorkflow",
    "PaperComparisonWorkflow", 
    "GapAnalysisWorkflow",
    "CitationFindingWorkflow"
]
```

```python
# polyhedra/agent/research_agent.py

from typing import Dict, Any, Optional
import asyncio
from dataclasses import dataclass

@dataclass
class WorkflowResult:
    """Result of workflow execution"""
    success: bool
    artifacts: Dict[str, Any]
    error: Optional[str] = None
    step_failed: Optional[str] = None
    
    @classmethod
    def success(cls, artifacts: Dict[str, Any]):
        return cls(success=True, artifacts=artifacts)
    
    @classmethod
    def failed(cls, step: str, error: str):
        return cls(success=False, artifacts={}, step_failed=step, error=error)
    
    @classmethod
    def cancelled(cls, step: str):
        return cls(success=False, artifacts={}, step_failed=step, error="User cancelled")


class PolyhedraResearchAgent:
    """
    Autonomous research agent with multi-step workflow execution.
    
    Inspired by BMAD's autonomous debugging approach:
    - Understands high-level user intent
    - Decomposes into actionable steps
    - Executes with error recovery
    - Provides progress feedback
    """
    
    SUPPORTED_COMMANDS = {
        "research": "Comprehensive literature survey",
        "compare": "Side-by-side paper comparison",
        "find-gaps": "Research gap identification",
        "cite": "Find relevant citations"
    }
    
    def __init__(self, llm_client, polyhedra_tools, config: Optional[Dict] = None):
        """
        Args:
            llm_client: IDE's LLM client (Claude/GPT)
            polyhedra_tools: All Polyhedra MCP tools
            config: Agent configuration (checkpoints, retries, etc.)
        """
        self.llm = llm_client
        self.tools = polyhedra_tools
        self.config = config or self._default_config()
        
        # Load workflows
        self.workflows = {
            "research": LiteratureSurveyWorkflow(self.tools, self.llm),
            "compare": PaperComparisonWorkflow(self.tools, self.llm),
            "find_gaps": GapAnalysisWorkflow(self.tools, self.llm),
            "cite": CitationFindingWorkflow(self.tools, self.llm)
        }
    
    async def handle_command(self, command: str) -> str:
        """
        Main entry point for agent commands.
        
        Example commands:
        - "@research efficient transformers"
        - "@compare arxiv:2304.12345 arxiv:2305.67890"
        - "@find-gaps sparse attention"
        - "@cite methods for reducing memory in transformers"
        
        Returns:
            Human-readable summary of execution
        """
        
        # Parse command
        try:
            intent = await self._parse_intent(command)
        except ValueError as e:
            return self._format_error(str(e))
        
        # Get workflow
        workflow = self.workflows.get(intent["command"])
        if not workflow:
            return self._format_unknown_command(intent["command"])
        
        # Execute workflow
        try:
            result = await workflow.execute(intent["params"])
            
            if result.success:
                return self._format_success(workflow, result)
            else:
                return self._format_failure(workflow, result)
                
        except Exception as e:
            return self._format_error(f"Workflow failed: {str(e)}")
    
    async def _parse_intent(self, command: str) -> Dict[str, Any]:
        """
        Parse natural language command into structured intent.
        
        Uses LLM to extract:
        - Command type (research, compare, etc.)
        - Parameters (topic, papers, options)
        - Preferences (depth, focus, etc.)
        """
        
        prompt = f"""
Parse this research command:

Command: {command}

Available commands:
{self._format_available_commands()}

Extract:
1. Command type (one of: {', '.join(self.SUPPORTED_COMMANDS.keys())})
2. Primary parameter (topic, paper IDs, query)
3. Options (year range, depth, focus, etc.)

Return JSON:
{{
    "command": "research",
    "params": {{
        "topic": "extracted topic",
        "year_start": 2020,
        "year_end": 2024,
        "depth": "standard",
        "focus": null
    }}
}}

If command is unclear or unsupported, return:
{{
    "error": "explanation of what's wrong"
}}
"""
        
        response = await self.llm.complete(prompt)
        intent = json.loads(response)
        
        if "error" in intent:
            raise ValueError(intent["error"])
        
        return intent
    
    def _format_available_commands(self) -> str:
        """Format supported commands for display"""
        lines = []
        for cmd, desc in self.SUPPORTED_COMMANDS.items():
            lines.append(f"  @{cmd}: {desc}")
        return "\n".join(lines)
    
    def _format_success(self, workflow, result: WorkflowResult) -> str:
        """Format successful execution message"""
        artifacts = result.artifacts
        
        # Workflow-specific formatting
        if isinstance(workflow, LiteratureSurveyWorkflow):
            return f"""
✓ Literature survey complete!

📄 Review: {artifacts['review_path']}
   • {artifacts['word_count']} words
   • {artifacts['paper_count']} papers cited
   • {len(artifacts['gaps'])} research gaps identified

💰 Cost: ${artifacts['cost']:.2f}

📋 Next steps:
   • Review the gaps in literature/gaps.md
   • Refine specific sections if needed
   • Start hypothesis generation with @hypothesize
"""
        
        elif isinstance(workflow, PaperComparisonWorkflow):
            return f"""
✓ Paper comparison complete!

📊 Comparison saved to: {artifacts['comparison_path']}

Key differences:
{self._format_comparison_summary(artifacts['comparison'])}

[View full comparison] [Add to review] [Compare more papers]
"""
        
        # Generic success message
        return f"✓ Workflow '{workflow.name}' completed successfully"
    
    def _format_failure(self, workflow, result: WorkflowResult) -> str:
        """Format failure message with recovery suggestions"""
        return f"""
✗ Workflow failed at step: {result.step_failed}

Error: {result.error}

What you can try:
{self._suggest_recovery(workflow, result)}

[Retry] [Skip this step] [Start over]
"""
    
    def _format_error(self, error: str) -> str:
        """Format generic error message"""
        return f"""
❌ Error: {error}

Available commands:
{self._format_available_commands()}

Example: @research efficient vision transformers
"""
    
    def _default_config(self) -> Dict:
        """Default agent configuration"""
        return {
            "max_retries": 3,
            "retry_delay": 2.0,
            "enable_checkpoints": True,
            "auto_save": True,
            "verbose": True
        }


class BaseWorkflow:
    """Base class for all workflows"""
    
    def __init__(self, tools, llm):
        self.tools = tools
        self.llm = llm
        self.steps = []
        self.checkpoints = []
    
    async def execute(self, params: Dict[str, Any]) -> WorkflowResult:
        """Execute workflow with error handling and checkpoints"""
        
        context = {
            "params": params,
            "artifacts": {},
            "state": "running"
        }
        
        for step in self.steps:
            # Check if this is a checkpoint
            if step.name in self.checkpoints:
                approved = await self._checkpoint(step, context)
                if not approved:
                    return WorkflowResult.cancelled(step.name)
            
            # Execute step
            try:
                result = await self._execute_step_with_retry(step, context)
                context["artifacts"][step.name] = result
                
            except Exception as e:
                # Attempt recovery
                recovered = await self._recover_from_error(step, e, context)
                if not recovered:
                    return WorkflowResult.failed(step.name, str(e))
        
        return WorkflowResult.success(context["artifacts"])
    
    async def _execute_step_with_retry(self, step, context, max_retries=3):
        """Execute step with automatic retry on transient failures"""
        
        for attempt in range(max_retries):
            try:
                return await step.run(context, self.tools)
            except (TimeoutError, ConnectionError) as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise
    
    async def _checkpoint(self, step, context) -> bool:
        """
        Pause for user approval.
        Implementation depends on IDE's interaction model.
        """
        # In practice, this would show a UI dialog or inline message
        # For now, return True (auto-approve)
        return True
    
    async def _recover_from_error(self, step, error, context) -> bool:
        """Attempt to recover from error"""
        
        # Example recovery strategies:
        if "rate limit" in str(error).lower():
            await asyncio.sleep(60)  # Wait for rate limit reset
            return True
        
        if "not found" in str(error).lower():
            # Try alternative source
            return await self._try_alternative(step, context)
        
        return False
```

### 2.5 IDE Integration

**Cursor Configuration**:
```json
// .cursor/agents/polyhedra.json
{
  "name": "Polyhedra Research",
  "version": "2.1.0",
  "description": "Autonomous research assistant for academic literature",
  
  "activation": {
    "triggers": ["@research", "@compare", "@find-gaps", "@cite"],
    "file_patterns": ["*.md", "*.tex", "*.bib"]
  },
  
  "capabilities": {
    "autonomous_execution": true,
    "multi_step_workflows": true,
    "error_recovery": true,
    "cost_estimation": true
  },
  
  "configuration": {
    "llm_provider": "anthropic",
    "enable_checkpoints": true,
    "max_cost_per_workflow": 1.00,
    "auto_save_artifacts": true
  },
  
  "workflows": [
    {
      "name": "literature_survey",
      "description": "Comprehensive literature review",
      "estimated_time": "2-5 minutes",
      "estimated_cost": "$0.10-0.30"
    },
    {
      "name": "paper_comparison", 
      "description": "Compare two papers side-by-side",
      "estimated_time": "30-60 seconds",
      "estimated_cost": "$0.05-0.10"
    }
  ]
}
```

**System Prompt for Agent**:
```
You are Polyhedra, an expert research assistant specializing in academic literature.

Your capabilities:
• Search and retrieve papers from Semantic Scholar
• Generate comprehensive literature reviews
• Identify research gaps and opportunities
• Find relevant citations for specific claims
• Compare papers side-by-side

Your interaction style:
• Proactive: Suggest next steps and alternatives
• Transparent: Explain what you're doing and why
• Cost-conscious: Warn before expensive operations
• Helpful: Recover gracefully from errors

When given a command like "@research X":
1. Understand the research topic X
2. Plan the workflow (search → index → review)
3. Estimate cost and time
4. Request approval for expensive steps
5. Execute with progress updates
6. Summarize results with actionable next steps

Always prioritize the researcher's time and budget.
```

### 2.6 Example Session

```
[User opens research project in Cursor]

User: @research efficient vision transformers for mobile devices

Agent: 🔍 Starting literature survey...
       
       Topic: Efficient vision transformers for mobile devices
       
       Planning workflow:
       1. Search papers (Semantic Scholar)
       2. Filter for mobile/edge deployment focus
       3. Index papers for RAG
       4. Generate literature review
       5. Identify research gaps
       
       Estimated time: 3-4 minutes
       Estimated cost: $0.15-0.20
       
       Proceed? [Y/n]

User: y

Agent: [1/5] Searching papers...
       ✓ Found 52 papers on "efficient vision transformers"
       ✓ Filtered to 31 papers mentioning mobile/edge deployment
       
       [2/5] Analyzing paper relevance...
       ✓ Top papers by citations:
         • MobileViT (Mehta et al., 2022) - 890 citations
         • EfficientViT (Liu et al., 2023) - 245 citations
         • EdgeViT (Pan et al., 2022) - 156 citations
       
       [3/5] Indexing papers...
       ✓ Generated embeddings for 31 papers
       ✓ Cached in .poly/embeddings/
       
       [4/5] Generating literature review...
       📊 Review will include:
          • 3 main categories (architecture, training, deployment)
          • Critical analysis of trade-offs
          • 5-7 research gaps
       
       This step will cost ~$0.14. Continue? [Y/n]

User: y

Agent: ✓ Generated literature review (4,234 words)
       
       [5/5] Finalizing outputs...
       ✓ Saved to literature/review.md
       ✓ Added 31 citations to references.bib
       ✓ Identified 6 research gaps → literature/gaps.md
       
       Total cost: $0.16 | Time: 3m 42s
       
       📄 Review Preview:
       # Literature Review: Efficient Vision Transformers for Mobile
       
       ## Overview
       This review synthesizes 31 recent papers (2022-2024) on efficient
       vision transformers targeting mobile and edge deployment...
       
       [Read full review]
       
       🔬 Top Research Gaps:
       1. **Real-time performance on mobile GPUs**
          Only 3 papers benchmark on actual mobile hardware.
          Most use FLOPs as proxy metric.
          
       2. **Energy consumption analysis**
          Critical for battery-powered devices, but rarely measured.
       
       [View all gaps]
       
       💡 Suggested next steps:
       • Generate hypotheses based on gaps (@hypothesize)
       • Compare top 3 approaches (@compare)
       • Find related work on energy efficiency (@cite "energy efficient transformers")

User: @compare EfficientViT MobileViT

Agent: 🔬 Comparing papers...
       
       Paper 1: EfficientViT (Liu et al., 2023)
       Paper 2: MobileViT (Mehta et al., 2022)
       
       [Fetching full metadata...]
       
       ✓ Generated comparison:
       
       | Metric | EfficientViT | MobileViT |
       |--------|--------------|-----------|
       | Parameters | 32M | 18M |
       | FLOPs | 2.1G | 1.8G |
       | ImageNet Acc | 82.3% | 81.7% |
       | Mobile latency | 12ms (A100) | 8ms (iPhone 13) |
       | Method | Sparse attention | Hybrid CNN-ViT |
       | Memory | 180MB | 95MB |
       
       Key insights:
       • MobileViT is more memory-efficient (2x smaller)
       • EfficientViT has slightly better accuracy (+0.6%)
       • MobileViT benchmarked on real mobile device ✓
       • EfficientViT only on server GPU ✗
       
       [Save comparison] [Add to review] [Export table]

User: save comparison

Agent: ✓ Saved to literature/comparisons/efficientvit-vs-mobilevit.md
       ✓ Added to references.bib
       
       You can now cite this comparison in your paper:
       ```latex
       \cite{liu2023efficient,mehta2022mobile}
       ```
```

---

## 3. New Feature: Literature Review Generation

### 2.1 Overview

**Tool Name**: `generate_literature_review`

**Purpose**: Automatically synthesize multiple papers into a structured literature review with:
- Thematic organization
- Gap identification
- Proper citations
- Critical analysis

### 2.2 User Workflow

```
User: "Generate a literature review on efficient transformers"

Step 1: Polyhedra searches papers
├─ Calls search_papers("efficient transformers", limit=50)
├─ Auto-indexes papers
└─ Returns 47 papers found

Step 2: User confirms or refines
├─ Option A: Proceed with all 47 papers
├─ Option B: Filter by year/venue
└─ Option C: Add specific papers

Step 3: Polyhedra generates review
├─ Sends papers to LLM with specialized prompt
├─ Generates structured review:
│   ├─ Abstract/Overview
│   ├─ Taxonomy of approaches
│   ├─ Key papers per category
│   ├─ Research gaps
│   └─ Future directions
├─ Auto-adds citations to references.bib
└─ Saves to literature/review.md

Step 4: User can refine
├─ Regenerate specific sections
├─ Add focus on specific topics
└─ Adjust structure
```

### 2.3 Tool Specification

```yaml
name: generate_literature_review
description: |
  Generate a structured literature review from a collection of papers.
  This tool calls an LLM to synthesize papers into a coherent review
  with thematic organization, gap analysis, and proper citations.

input_schema:
  type: object
  properties:
    papers_file:
      type: string
      default: "literature/papers.json"
      description: Path to papers JSON (from search_papers)
    
    focus:
      type: string
      description: Optional focus area (e.g., "sparse attention mechanisms")
    
    structure:
      type: string
      enum: ["thematic", "chronological", "methodological"]
      default: "thematic"
      description: Organization structure for the review
    
    depth:
      type: string
      enum: ["brief", "standard", "comprehensive"]
      default: "standard"
      description: |
        - brief: 2-3 pages, high-level overview
        - standard: 5-8 pages, detailed analysis
        - comprehensive: 10-15 pages, deep dive
    
    include_gaps:
      type: boolean
      default: true
      description: Whether to identify research gaps
    
    output_path:
      type: string
      default: "literature/review.md"
      description: Where to save the generated review
    
    llm_model:
      type: string
      default: "claude-3-5-sonnet-20241022"
      description: LLM model to use for generation
  
  required: []

output_schema:
  type: object
  properties:
    review:
      type: string
      description: The generated literature review (markdown)
    
    metadata:
      type: object
      properties:
        paper_count:
          type: integer
        word_count:
          type: integer
        sections:
          type: array
          items:
            type: string
        research_gaps:
          type: array
          items:
            type: object
            properties:
              gap:
                type: string
              description:
                type: string
        citations_added:
          type: integer
    
    cost:
      type: object
      properties:
        input_tokens:
          type: integer
        output_tokens:
          type: integer
        total_usd:
          type: number
    
    saved_to:
      type: string
      description: File path where review was saved
```

### 2.4 LLM Prompt Design

```python
# Core prompt for literature review generation
LITERATURE_REVIEW_PROMPT = """
You are an expert academic researcher tasked with writing a literature review.

INPUT:
{paper_count} academic papers on the topic: "{topic}"

PAPERS DATA:
{papers_json}

TASK:
Write a comprehensive literature review with the following structure:

1. **Overview** (1 paragraph)
   - Summarize the research area
   - State the scope of this review
   - Preview main findings

2. **Taxonomy of Approaches** (main section)
   - Organize papers into 3-5 thematic categories
   - For each category:
     * Define the approach
     * List 3-5 key papers with citations
     * Compare methods
     * Note trends and developments

3. **Critical Analysis** (1-2 paragraphs per category)
   - Strengths and limitations of each approach
   - Comparative insights
   - Identify what works and what doesn't

4. **Research Gaps** (bullet list)
   - Identify 3-7 gaps in current literature
   - For each gap:
     * What is missing?
     * Why does it matter?
     * Potential research directions

5. **Conclusion** (1 paragraph)
   - Synthesize main insights
   - Highlight most promising directions

REQUIREMENTS:
- Use markdown format
- Cite papers as [Author et al., Year] or [@bibtex_key]
- Be critical and analytical, not just descriptive
- Focus on {focus_area} if specified
- Target length: {target_length} words
- Structure: {structure_type}

OUTPUT FORMAT:
Return ONLY the markdown content, no preamble.
"""

# Prompt for gap identification
GAP_IDENTIFICATION_PROMPT = """
Based on the literature review you just generated, identify research gaps.

For each gap, provide:
1. Gap title (concise)
2. Description (2-3 sentences)
3. Why it matters
4. Potential approaches to address it

Return as JSON array:
[
  {
    "title": "Gap title",
    "description": "...",
    "significance": "...",
    "potential_approaches": ["approach1", "approach2"]
  }
]
"""
```

### 2.5 Implementation Architecture

```python
# services/literature_review_service.py
from anthropic import Anthropic
from openai import OpenAI
import json
from pathlib import Path
from typing import Literal

class LiteratureReviewService:
    def __init__(
        self,
        llm_provider: Literal["anthropic", "openai"] = "anthropic",
        api_key: str = None
    ):
        self.provider = llm_provider
        if llm_provider == "anthropic":
            self.client = Anthropic(api_key=api_key)
            self.default_model = "claude-3-5-sonnet-20241022"
        else:
            self.client = OpenAI(api_key=api_key)
            self.default_model = "gpt-4-turbo-preview"
    
    async def generate_review(
        self,
        papers: list[dict],
        focus: str = None,
        structure: str = "thematic",
        depth: str = "standard",
        include_gaps: bool = True,
        model: str = None
    ) -> dict:
        """
        Generate literature review from papers
        
        Returns:
            {
                "review": "markdown content",
                "metadata": {...},
                "cost": {...}
            }
        """
        model = model or self.default_model
        
        # Prepare papers data
        papers_summary = self._prepare_papers_summary(papers)
        
        # Determine target length
        length_map = {
            "brief": "1500-2000",
            "standard": "3000-5000", 
            "comprehensive": "6000-10000"
        }
        target_length = length_map[depth]
        
        # Build prompt
        prompt = LITERATURE_REVIEW_PROMPT.format(
            paper_count=len(papers),
            topic=focus or "the research area",
            papers_json=papers_summary,
            focus_area=focus or "general research trends",
            target_length=target_length,
            structure_type=structure
        )
        
        # Call LLM
        if self.provider == "anthropic":
            response = self.client.messages.create(
                model=model,
                max_tokens=8192,
                messages=[{"role": "user", "content": prompt}]
            )
            review_text = response.content[0].text
            usage = {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "total_usd": self._calculate_cost_anthropic(
                    response.usage.input_tokens,
                    response.usage.output_tokens,
                    model
                )
            }
        else:  # OpenAI
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=8192
            )
            review_text = response.choices[0].message.content
            usage = {
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
                "total_usd": self._calculate_cost_openai(
                    response.usage.prompt_tokens,
                    response.usage.completion_tokens,
                    model
                )
            }
        
        # Extract metadata
        word_count = len(review_text.split())
        sections = self._extract_sections(review_text)
        
        # Identify gaps if requested
        gaps = []
        if include_gaps:
            gaps = await self._identify_gaps(review_text, model)
        
        return {
            "review": review_text,
            "metadata": {
                "paper_count": len(papers),
                "word_count": word_count,
                "sections": sections,
                "research_gaps": gaps,
                "citations_added": self._count_citations(review_text)
            },
            "cost": usage
        }
    
    def _prepare_papers_summary(self, papers: list[dict]) -> str:
        """Convert papers to structured summary for LLM"""
        summaries = []
        for p in papers:
            summaries.append(f"""
Title: {p['title']}
Authors: {', '.join(p['authors'])}
Year: {p['year']}
Venue: {p.get('venue', 'N/A')}
Citations: {p['citation_count']}
BibTeX Key: {p['bibtex_key']}

Abstract:
{p['abstract']}

---
""")
        return "\n".join(summaries)
    
    async def _identify_gaps(self, review: str, model: str) -> list[dict]:
        """Extract research gaps from review"""
        prompt = GAP_IDENTIFICATION_PROMPT
        
        if self.provider == "anthropic":
            response = self.client.messages.create(
                model=model,
                max_tokens=2048,
                messages=[
                    {"role": "user", "content": review},
                    {"role": "assistant", "content": "I've written the review."},
                    {"role": "user", "content": prompt}
                ]
            )
            gaps_json = response.content[0].text
        else:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": review},
                    {"role": "assistant", "content": "I've written the review."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2048
            )
            gaps_json = response.choices[0].message.content
        
        # Parse JSON response
        try:
            gaps = json.loads(gaps_json)
            return gaps
        except:
            return []
    
    def _extract_sections(self, review: str) -> list[str]:
        """Extract section headings from markdown"""
        import re
        headings = re.findall(r'^#{1,3}\s+(.+)$', review, re.MULTILINE)
        return headings
    
    def _count_citations(self, review: str) -> int:
        """Count citation references in text"""
        import re
        citations = re.findall(r'\[@\w+\d+\]|\[.+?\s+et al\.,\s+\d{4}\]', review)
        return len(citations)
    
    def _calculate_cost_anthropic(self, input_tokens: int, output_tokens: int, model: str) -> float:
        """Calculate cost for Anthropic models"""
        prices = {
            "claude-3-5-sonnet-20241022": {"input": 3.0, "output": 15.0},  # per 1M tokens
            "claude-3-opus-20240229": {"input": 15.0, "output": 75.0}
        }
        price = prices.get(model, prices["claude-3-5-sonnet-20241022"])
        cost = (input_tokens * price["input"] + output_tokens * price["output"]) / 1_000_000
        return round(cost, 4)
    
    def _calculate_cost_openai(self, input_tokens: int, output_tokens: int, model: str) -> float:
        """Calculate cost for OpenAI models"""
        prices = {
            "gpt-4-turbo-preview": {"input": 10.0, "output": 30.0},
            "gpt-4": {"input": 30.0, "output": 60.0}
        }
        price = prices.get(model, prices["gpt-4-turbo-preview"])
        cost = (input_tokens * price["input"] + output_tokens * price["output"]) / 1_000_000
        return round(cost, 4)
```

### 2.6 MCP Tool Implementation

```python
# In server.py

from polyhedra.services.literature_review_service import LiteratureReviewService

# Initialize service
_review_service: LiteratureReviewService = None

def _init_review_service():
    global _review_service
    import os
    
    provider = os.getenv("POLYHEDRA_LLM_PROVIDER", "anthropic")
    api_key = os.getenv("ANTHROPIC_API_KEY") if provider == "anthropic" else os.getenv("OPENAI_API_KEY")
    
    _review_service = LiteratureReviewService(
        llm_provider=provider,
        api_key=api_key
    )

_init_review_service()

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        # ... existing tools ...
        
        Tool(
            name="generate_literature_review",
            description="Generate a structured literature review from papers using AI synthesis",
            inputSchema={
                "type": "object",
                "properties": {
                    "papers_file": {
                        "type": "string",
                        "default": "literature/papers.json",
                        "description": "Path to papers JSON file"
                    },
                    "focus": {
                        "type": "string",
                        "description": "Optional focus area for the review"
                    },
                    "structure": {
                        "type": "string",
                        "enum": ["thematic", "chronological", "methodological"],
                        "default": "thematic"
                    },
                    "depth": {
                        "type": "string",
                        "enum": ["brief", "standard", "comprehensive"],
                        "default": "standard"
                    },
                    "include_gaps": {
                        "type": "boolean",
                        "default": True
                    },
                    "output_path": {
                        "type": "string",
                        "default": "literature/review.md"
                    },
                    "llm_model": {
                        "type": "string",
                        "description": "LLM model to use"
                    }
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    # ... existing tools ...
    
    elif name == "generate_literature_review":
        # Load papers
        papers_file = _project_root / arguments.get("papers_file", "literature/papers.json")
        if not papers_file.exists():
            return [TextContent(
                type="text",
                text=json.dumps({
                    "error": "Papers file not found. Run search_papers first."
                })
            )]
        
        papers = json.loads(papers_file.read_text())
        
        # Generate review
        result = await _review_service.generate_review(
            papers=papers,
            focus=arguments.get("focus"),
            structure=arguments.get("structure", "thematic"),
            depth=arguments.get("depth", "standard"),
            include_gaps=arguments.get("include_gaps", True),
            model=arguments.get("llm_model")
        )
        
        # Save to file
        output_path = _project_root / arguments.get("output_path", "literature/review.md")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result["review"])
        
        # Add citations to references.bib
        citations_added = 0
        for paper in papers:
            key, added = _citation_manager.add_entry(paper["bibtex_entry"])
            if added:
                citations_added += 1
        
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": True,
                "saved_to": str(output_path),
                "metadata": result["metadata"],
                "cost": result["cost"],
                "citations_added": citations_added
            }, indent=2)
        )]
```

### 2.7 Configuration

**Environment Variables**:
```bash
# .env file
POLYHEDRA_LLM_PROVIDER=anthropic  # or "openai"
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```

**IDE Configuration**:
```json
// .cursor/mcp.json or .vscode/settings.json
{
  "mcpServers": {
    "polyhedra": {
      "command": "python",
      "args": ["-m", "polyhedra.server"],
      "env": {
        "POLYHEDRA_LLM_PROVIDER": "anthropic",
        "ANTHROPIC_API_KEY": "sk-ant-..."
      }
    }
  }
}
```

---

## 3. Updated System Architecture

### 3.1 Layered Architecture (v2.1)

```
┌──────────────────────────────────────────────────┐
│          MCP Tool Layer                          │
│  Pure Tools + Agent Tool                         │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────┐
│         Service Layer                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │  Papers  │ │ Context  │ │ Citations│        │
│  │ Service  │ │ Service  │ │ Service  │        │
│  └──────────┘ └──────────┘ └──────────┘        │
│  ┌──────────┐ ┌──────────────────────┐         │
│  │   RAG    │ │  🆕 Literature       │         │
│  │ Service  │ │  Review Service      │         │
│  └──────────┘ └──────────────────────┘         │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────┐
│      External Services                           │
│  • Semantic Scholar API                          │
│  • 🆕 Anthropic/OpenAI API                       │
└──────────────────────────────────────────────────┘
```

### 3.2 Updated Directory Structure

```
polyhedra/
├── pyproject.toml
├── README.md
├── .env.example                # 🆕 LLM API keys
├── src/
│   └── polyhedra/
│       ├── __init__.py
│       ├── server.py
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── papers.py
│       │   ├── context.py
│       │   ├── retrieval.py
│       │   ├── citations.py
│       │   ├── files.py
│       │   └── review.py      # 🆕 Literature review tool
│       ├── services/
│       │   ├── __init__.py
│       │   ├── semantic_scholar.py
│       │   ├── context_manager.py
│       │   ├── citation_manager.py
│       │   ├── rag_service.py
│       │   └── literature_review_service.py  # 🆕
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── paper.py
│       │   └── project.py
│       └── prompts/           # 🆕 Prompt templates
│           ├── __init__.py
│           ├── literature_review.py
│           └── gap_analysis.py
└── tests/
    ├── test_tools/
    │   └── test_review.py     # 🆕
    └── test_services/
        └── test_literature_review_service.py  # 🆕
```

---

## 4. Updated Functional Requirements

### FR-006: LiteratureAgent - Autonomous Literature Review (NEW) 🆕

**Priority**: P1 (High - Week 4)  
**Status**: Not Started  
**Agent**: Phase 1 of Research Pipeline

**Description**  
Autonomous agent that searches academic literature, synthesizes findings, and identifies research gaps. First agent in the multi-agent research pipeline.

**User Story**  
"As a researcher starting a new project, I want an AI agent to read my research direction, search relevant papers, organize them by themes, and generate a well-structured literature review with proper citations, so I can quickly understand the state of the art."

**Capabilities**
1. **Intent understanding**: Parse natural language research topics
2. **Multi-query search**: Generate and execute 3-5 complementary search queries
3. **Paper selection**: Rank papers by relevance, select top 10-20
4. **Theme clustering**: Group papers into coherent themes (Methods, Applications, Gaps)
5. **Synthesis generation**: Write 500-1500 word literature review
6. **Citation integration**: Properly cite all referenced papers in BibTeX format
7. **Gap identification**: Highlight under-explored areas and suggest research directions

**Triggers**
- Direct command: `@literature-review "multimodal transformers for vision-language"`
- Pipeline mode: First phase in `@full-research`

**Input Parameters**
```python
{
  "research_topic": str,  # Natural language description
  "max_papers": int = 20,  # Papers to include
  "depth": str = "standard"  # "brief" (500w), "standard" (1000w), "comprehensive" (2000w)
}
```

**Output Artifacts** (consumed by HypothesisAgent)
```json
{
  "review_text": "markdown content with citations",
  "papers": [
    {"paper_id": "arxiv:2203.12345", "relevance_score": 0.95, "theme": "Architecture"}
  ],
  "themes": ["Architectures", "Pre-training Methods", "Benchmarks"],
  "identified_gaps": [
    "Few studies on low-resource languages",
    "Limited benchmarks for video understanding"
  ],
  "suggested_directions": [
    "Investigate synthetic data for low-resource VL",
    "Extend temporal modeling for video tasks"
  ],
  "metadata": {
    "paper_count": 18,
    "citation_count": 18,
    "generation_time_sec": 125,
    "cost_usd": 0.25
  }
}
```

**Checkpoint System**
```
User: @literature-review "multimodal transformers for vision-language"

Agent: 
[Step 1/4] Searching papers...
  ✓ Generated 4 search queries
  ✓ Found 45 papers on Semantic Scholar
  → Top 20 selected by relevance
  
[Checkpoint] Do you want to:
  1. Continue with these 20 papers ✓
  2. Add more search queries
  3. Manually select specific papers
  
User: 1

[Step 2/4] Clustering papers into themes...
  ✓ Identified 4 themes: Architectures (8), Pre-training (5), Benchmarks (4), Applications (3)
  
[Step 3/4] Generating literature review (est. 2-3 min)...
  ✓ Generated 1200-word review
  ✓ Added 18 citations to references.bib
  
[Step 4/4] Identifying research gaps...
  ✓ Found 3 under-explored areas
  
[Output] Saved to: literature/multimodal_transformers_review.md

Next: Run @hypothesize to generate research hypotheses from these gaps
```

**Cost & Performance**
- LLM calls: 3-5 (synthesis, clustering, gap analysis)
- Total tokens: ~15K input + 5K output
- Cost: $0.15-0.30 per review
- Time: 3-5 minutes

**Dependencies**
- Semantic Scholar API (FR-001)
- Citation manager (FR-002)
- LLM client (Anthropic/OpenAI)

**Edge Cases**
- Handle papers without abstracts (use title + introduction text)
- Handle duplicate papers (deduplicate by DOI/arxiv ID)
- Handle API rate limits (exponential backoff)
- Handle < 5 papers found (adjust depth, warn user)

---

### FR-007: HypothesisAgent - Research Hypothesis Generation (NEW) 🆕

**Priority**: P1 (High - Week 5)  
**Status**: Not Started  
**Agent**: Phase 2 of Research Pipeline

**Description**  
Generates testable research hypotheses based on literature gaps. Performs novelty checking and feasibility analysis.

**User Story**  
"Given the gaps I've identified in existing work, I want an AI agent to propose 3-5 testable hypotheses with novelty scores and feasibility assessments, so I can select the most promising research direction."

**Capabilities**
1. **Gap analysis**: Process identified gaps from LiteratureAgent
2. **Hypothesis generation**: Propose 3-5 testable hypotheses per gap
3. **Novelty checking**: Search for similar existing work, compute novelty score
4. **Feasibility assessment**: Evaluate required resources (data, compute, time)
5. **Impact prediction**: Estimate potential contribution to the field
6. **Interactive selection**: Help user choose best hypothesis

**Triggers**
- Direct command: `@hypothesize`
- Pipeline mode: Second phase in `@full-research` (after LiteratureAgent)

**Input** (from LiteratureAgent)
```json
{
  "literature_review": {...},
  "identified_gaps": ["Gap 1", "Gap 2", "Gap 3"],
  "papers": [...]
}
```

**Output Artifacts** (consumed by MethodAgent)
```json
{
  "hypotheses": [
    {
      "id": "H1",
      "statement": "Fine-tuning with synthetic data improves low-resource VL tasks",
      "novelty_score": 0.85,
      "novelty_rationale": "Only 2 papers explore synthetic data for VL, none for low-resource",
      "feasibility": "High",
      "required_resources": {
        "data": "Public datasets + Stable Diffusion API",
        "compute": "2x A100 GPUs",
        "time_weeks": 3
      },
      "expected_impact": "Address major gap in low-resource languages",
      "risks": ["Synthetic data distribution mismatch"]
    }
  ],
  "selected_hypothesis": {...},
  "selection_rationale": "Selected H1 because highest novelty (0.85) + feasible timeline (3 weeks)"
}
```

**Checkpoint System**
```
Agent: 
[Step 1/3] Analyzing 3 identified gaps...
  ✓ Gap 1: Low-resource languages (8 relevant papers)
  ✓ Gap 2: Video understanding (12 relevant papers)
  ✓ Gap 3: Efficiency (15 relevant papers)

[Step 2/3] Generating hypotheses (est. 5 min)...
  ✓ Generated 5 hypotheses
  ✓ Novelty scores computed (range: 0.65-0.92)
  
[Checkpoint] Top 3 hypotheses:
  1. [Novelty: 0.92, Feasibility: High] Synthetic data for low-resource VL
  2. [Novelty: 0.85, Feasibility: Medium] Temporal attention for video
  3. [Novelty: 0.78, Feasibility: High] Efficient cross-modal fusion
  
Which hypothesis should we develop? (1-3, or 'all' to compare):

User: 1

[Step 3/3] Assessing feasibility...
  ✓ Feasibility: High
  ✓ Resources: 2 GPUs, 3 weeks, $500 compute
  ✓ Expected impact: High (addresses major gap in low-resource languages)
  ✓ Risks identified: 1 (synthetic data distribution mismatch)

Next: Run @design-method to create experimental setup
```

**Cost & Performance**
- LLM calls: 5-8 (generation, novelty checking, feasibility analysis)
- Total tokens: ~20K input + 8K output
- Cost: $0.20-0.50 per run
- Time: 5-10 minutes

**Dependencies**
- LiteratureAgent output (FR-006)
- Semantic Scholar API (for novelty checking)
- LLM client

**Edge Cases**
- Handle no clear gaps (ask user for manual direction)
- Handle all hypotheses low novelty (< 0.5) - warn and suggest broader search
- Handle infeasible resources (> user's compute budget) - suggest scaled-down version

---

### FR-008: MethodAgent - Experimental Method Design (NEW) 🆕

**Priority**: P1 (High - Week 5-6)  
**Status**: Not Started  
**Agent**: Phase 3 of Research Pipeline

**Description**  
Designs detailed experimental methods to test hypotheses. Selects baselines, metrics, datasets, and creates implementation plan.

**User Story**  
"Given a research hypothesis, I want an AI agent to design a complete experimental setup with baselines, metrics, datasets, and implementation plan, so I can start experiments quickly."

**Capabilities**
1. **Method design**: Propose experimental approach
2. **Baseline selection**: Identify 3-5 relevant baselines from literature
3. **Metric definition**: Choose appropriate evaluation metrics
4. **Dataset recommendation**: Suggest suitable datasets (public/synthetic)
5. **Resource estimation**: Compute hours, time, budget
6. **Risk assessment**: Identify potential failure points and mitigations

**Triggers**
- Direct command: `@design-method`
- Pipeline mode: Third phase in `@full-research` (after HypothesisAgent)

**Input** (from HypothesisAgent)
```json
{
  "selected_hypothesis": {...},
  "feasibility_assessment": {...},
  "required_resources": {...}
}
```

**Output Artifacts** (consumed by ExperimentAgent)
```json
{
  "method_description": "markdown text (500-1000 words)",
  "baselines": [
    {"name": "CLIP", "paper_id": "...", "reason": "Standard baseline", "code_url": "..."},
    {"name": "ALIGN", "paper_id": "...", "reason": "SOTA comparison", "code_url": "..."}
  ],
  "metrics": [
    {"name": "Accuracy", "justification": "Standard for classification"},
    {"name": "F1", "justification": "Handle class imbalance"}
  ],
  "datasets": [
    {"name": "COCO", "split": "val", "size": "5K images"},
    {"name": "Flickr30K", "split": "test", "size": "1K images"}
  ],
  "implementation_plan": {
    "steps": [
      "1. Prepare data (Week 1)",
      "2. Implement model (Week 1-2)",
      "3. Train baselines + ours (Week 2-3)",
      "4. Evaluate (Week 3)"
    ],
    "estimated_time_weeks": 3,
    "compute_resources": "2x A100 GPUs",
    "estimated_cost_usd": 500
  },
  "risks": [
    {
      "risk": "Data leakage risk",
      "mitigation": "Use strict train/test split, no test set touching during dev"
    }
  ]
}
```

**Checkpoint System**
```
Agent: 
[Step 1/4] Analyzing hypothesis...
  ✓ Hypothesis: Synthetic data for low-resource VL
  ✓ Task type: Vision-Language Classification
  
[Step 2/4] Searching for baselines (est. 3 min)...
  ✓ Found 12 relevant papers with code
  ✓ Selected 4 baselines: CLIP, ALIGN, LiT, FLAVA
  
[Checkpoint] Proposed method:
  1. Generate synthetic image-text pairs using Stable Diffusion + LLM
  2. Fine-tune CLIP on synthetic + real data (mix ratio 50:50)
  3. Evaluate on 3 low-resource language benchmarks
  
Baselines:
  - CLIP (zero-shot) - lower bound
  - CLIP fine-tuned on real data only - ablation
  - ALIGN - larger model comparison
  
Datasets:
  - XM3600 (35 languages) - main benchmark
  - COCO-CN (Chinese) - language-specific
  - Multi30K-Hindi (Hindi) - language-specific
  
Metrics:
  - Accuracy (primary)
  - F1 (handle class imbalance)
  - Inference time (efficiency)
  
Does this setup make sense? (y/n/modify):

User: y

[Step 3/4] Estimating resources...
  ✓ Compute: 2x A100 GPUs (24GB VRAM each)
  ✓ Time: 3 weeks (1 week data gen, 2 weeks training)
  ✓ Budget: ~$500 compute cost (Lambda Labs)
  
[Step 4/4] Identifying risks...
  ⚠ Risk 1: Synthetic data quality may not match real data
     → Mitigation: Use diverse prompts, human verification sampling
  ⚠ Risk 2: Overfitting to synthetic distribution
     → Mitigation: Mix 50:50 with real data, monitor val loss

Next: Run @setup-experiment to generate code scaffolding
```

**Cost & Performance**
- LLM calls: 6-10 (method design, baseline search, risk analysis)
- Total tokens: ~25K input + 10K output
- Cost: $0.30-0.60 per run
- Time: 10-15 minutes

**Dependencies**
- HypothesisAgent output (FR-007)
- Semantic Scholar API (for baseline paper search)
- LLM client

**Edge Cases**
- Handle no public datasets available (suggest synthetic data generation)
- Handle baselines without code (suggest reimplementation)
- Handle resource exceeds budget (suggest scaled-down method)

---

### FR-009: ExperimentAgent - Experiment Setup & Monitoring (NEW) 🆕

**Priority**: P2 (Medium - Week 7)  
**Status**: Not Started  
**Agent**: Phase 4 of Research Pipeline

**Description**  
Generates experiment code scaffolding, config files, and monitoring scripts. Does NOT run experiments (user's compute).

**User Story**  
"Given an experimental design, I want an AI agent to generate training scripts, config files, and monitoring dashboards so I can start experiments immediately."

**Capabilities**
1. **Code generation**: PyTorch/TensorFlow training scripts
2. **Config creation**: YAML configs for hyperparameters
3. **Data pipeline**: Dataset loaders and preprocessing code
4. **Monitoring setup**: Wandb/TensorBoard integration
5. **Baseline implementation**: Generate baseline comparison code
6. **Checkpointing**: Auto-save best models, resume training

**Triggers**
- Direct command: `@setup-experiment`
- Pipeline mode: Fourth phase in `@full-research` (after MethodAgent)

**Input** (from MethodAgent)
```json
{
  "method_description": "...",
  "baselines": [...],
  "datasets": [...],
  "implementation_plan": {...}
}
```

**Output Artifacts** (used by researcher + AnalysisAgent later)
```json
{
  "code_files": {
    "train.py": "# PyTorch training script (250 lines)",
    "model.py": "# Model architecture (180 lines)",
    "data.py": "# Dataset loaders (120 lines)",
    "config.yaml": "# Hyperparameters",
    "README.md": "# Setup and run instructions"
  },
  "setup_instructions": "markdown text",
  "monitoring": {
    "wandb_project": "synthetic-vlm",
    "dashboard_url": "https://wandb.ai/user/synthetic-vlm",
    "tracked_metrics": ["train_loss", "val_acc", "val_f1"]
  },
  "expected_outputs": {
    "checkpoints": "checkpoints/*.pth",
    "logs": "logs/*.json",
    "results": "results.csv"
  }
}
```

**Checkpoint System**
```
Agent: 
[Step 1/3] Generating code scaffolding...
  ✓ Created train.py (250 lines) - main training loop
  ✓ Created model.py (180 lines) - CLIP + custom head
  ✓ Created data.py (120 lines) - XM3600, COCO-CN, Multi30K loaders
  ✓ Created config.yaml - hyperparameters (LR, batch size, epochs)
  
[Step 2/3] Setting up monitoring...
  ✓ Wandb integration added
  ✓ Metrics: train_loss, val_acc, val_f1, inference_time
  ✓ Checkpointing: save top-3 models by val_acc
  
[Checkpoint] Generated files:
  - experiments/synthetic_vlm/train.py
  - experiments/synthetic_vlm/model.py
  - experiments/synthetic_vlm/data.py
  - experiments/synthetic_vlm/config.yaml
  - experiments/synthetic_vlm/README.md
  
Ready to review code? (y/n):

User: y

[Agent shows code preview in IDE]

[Step 3/3] Creating monitoring dashboard...
  ✓ Wandb project created: synthetic-vlm
  ✓ Dashboard URL: https://wandb.ai/user/synthetic-vlm
  
[Instructions]
To start training:
  cd experiments/synthetic_vlm
  pip install -r requirements.txt
  python train.py --config config.yaml
  
Expected runtime: 2 weeks
Expected outputs: results.csv, checkpoints/, logs/

Next: After training completes, run @analyze-results experiments/synthetic_vlm/results.csv
```

**Cost & Performance**
- LLM calls: 4-6 (code generation, config creation)
- Total tokens: ~15K input + 12K output (code is verbose)
- Cost: $0.20-0.40 per run
- Time: 5-8 minutes (setup only, NOT training time)

**Dependencies**
- MethodAgent output (FR-008)
- LLM client (for code generation)

**Edge Cases**
- Handle unsupported frameworks (only PyTorch/TensorFlow)
- Handle custom architectures (generate template, ask user to fill)
- Handle missing dependencies (auto-generate requirements.txt)

**Note**: This agent does NOT run experiments. User runs experiments on their own compute. Agent only prepares code and monitoring infrastructure.

---

### FR-010: AnalysisAgent - Result Analysis & Visualization (NEW) 🆕

**Priority**: P2 (Medium - Week 7-8)  
**Status**: Not Started  
**Agent**: Phase 5 of Research Pipeline

**Description**  
Analyzes experimental results, generates publication-quality plots, performs statistical tests, and summarizes findings.

**User Story**  
"After my experiments finish, I want an AI agent to parse result logs, generate publication-quality plots, run significance tests, and summarize findings in plain language."

**Capabilities**
1. **Result parsing**: Read CSV/JSON/TensorBoard logs
2. **Plot generation**: Training curves, comparison bar charts, ablation studies
3. **Statistical tests**: T-tests, confidence intervals, significance testing
4. **Table generation**: LaTeX tables for paper
5. **Finding summarization**: Interpret results in plain language
6. **Failure diagnosis**: Identify why experiments failed (if applicable)

**Triggers**
- Direct command: `@analyze-results <path/to/results.csv>`
- Pipeline mode: Fifth phase in `@full-research` (after user completes experiments)

**Input** (from ExperimentAgent + user's training runs)
```json
{
  "log_files": ["results.csv", "logs/train.json"],
  "checkpoint_dir": "checkpoints/",
  "baseline_results": {...}
}
```

**Output Artifacts** (consumed by WritingAgent)
```json
{
  "summary": "Proposed method achieved 78.5% accuracy (+5.2% vs CLIP baseline, p<0.01)",
  "plots": [
    "figures/training_curve.pdf",
    "figures/baseline_comparison.pdf",
    "figures/ablation_study.pdf"
  ],
  "tables": {
    "results_table.tex": "\\begin{table}...",
    "ablation_table.tex": "\\begin{table}..."
  },
  "statistical_tests": {
    "ours_vs_clip": {"t_statistic": 3.45, "p_value": 0.008, "significant": true},
    "ours_vs_align": {"t_statistic": 1.52, "p_value": 0.12, "significant": false}
  },
  "insights": [
    "Synthetic data most effective for low-resource languages (+7.2% on Hindi)",
    "Performance drops for fine-grained tasks (only +2.1% on COCO)",
    "Inference time comparable to CLIP baseline (45ms vs 43ms)"
  ],
  "recommendations": [
    "Investigate why fine-grained tasks benefit less",
    "Try higher synthetic:real ratios for low-resource languages"
  ]
}
```

**Checkpoint System**
```
User: @analyze-results experiments/synthetic_vlm/results.csv

Agent: 
[Step 1/4] Parsing results...
  ✓ Found 3 runs: Ours, CLIP, ALIGN
  ✓ Metrics: Accuracy, F1, Inference Time
  ✓ Datasets: XM3600 (35 languages), COCO-CN, Multi30K-Hindi
  
[Step 2/4] Generating plots (est. 2 min)...
  ✓ Training curve: figures/training_curve.pdf
  ✓ Baseline comparison: figures/comparison.pdf
  ✓ Per-language breakdown: figures/per_language.pdf
  
[Step 3/4] Running statistical tests...
  ✓ Ours vs CLIP: +5.2% (t=3.45, p=0.008, **significant**)
  ✓ Ours vs ALIGN: +1.8% (t=1.52, p=0.12, not significant)
  
[Checkpoint] Summary:
  - Proposed method: 78.5% ± 1.2%
  - CLIP baseline: 73.3% ± 1.5%
  - ALIGN baseline: 76.7% ± 1.8%
  - Statistical significance: Yes (vs CLIP), No (vs ALIGN)
  
Generate LaTeX tables? (y/n):

User: y

[Step 4/4] Generating LaTeX tables...
  ✓ Main results table: tables/results.tex
  ✓ Ablation study table: tables/ablation.tex
  
Key insights:
  1. Synthetic data provides +5.2% improvement over CLIP
  2. Most effective for low-resource languages (+7.2% on Hindi)
  3. Performance comparable to larger model ALIGN (76.7% vs 78.5%)
  4. Inference time unchanged (45ms vs 43ms)

Recommendations:
  - Investigate why fine-grained tasks benefit less
  - Try higher synthetic:real ratios for low-resource languages

Next: Run @write-paper method to draft the methodology section
```

**Cost & Performance**
- LLM calls: 3-5 (interpretation, insight generation)
- Total tokens: ~10K input + 5K output
- Cost: $0.15-0.30 per run
- Time: 5-10 minutes

**Dependencies**
- ExperimentAgent output (FR-009)
- Matplotlib/Seaborn (for plotting)
- SciPy (for statistical tests)
- LLM client (for insight generation)

**Edge Cases**
- Handle missing baselines (skip comparison, warn user)
- Handle failed experiments (diagnose failure, suggest fixes)
- Handle incomplete logs (work with partial data)

---

### FR-011: WritingAgent - Academic Paper Drafting (NEW) 🆕

**Priority**: P1 (High - Week 6)  
**Status**: Not Started  
**Agent**: Phase 6 of Research Pipeline

**Description**  
Drafts paper sections with proper academic style, citations, and LaTeX formatting.

**User Story**  
"Given my experimental results and literature review, I want an AI agent to draft paper sections (introduction, related work, method, results) in academic style with proper citations."

**Capabilities**
1. **Section drafting**: Introduction, Related Work, Method, Results, Discussion, Conclusion
2. **Citation integration**: Automatically cite papers from references.bib
3. **Academic style**: Formal language, appropriate hedging, clear argumentation
4. **Figure references**: Cross-reference generated plots and tables
5. **Logical flow**: Ensure coherent narrative across sections
6. **LaTeX formatting**: Output ready for Overleaf/LaTeX compilation

**Triggers**
- Direct command: `@write-paper <section>` (e.g., `@write-paper introduction`)
- Pipeline mode: Sixth phase in `@full-research` (after AnalysisAgent)

**Input** (from previous agents)
```json
{
  "literature_review": {...},  # From LiteratureAgent
  "hypothesis": {...},  # From HypothesisAgent
  "method": {...},  # From MethodAgent
  "results": {...},  # From AnalysisAgent
  "references_bib": "path/to/references.bib"
}
```

**Output Artifacts** (consumed by ReviewAgent)
```json
{
  "sections": {
    "introduction.tex": "\\section{Introduction}...",
    "related_work.tex": "\\section{Related Work}...",
    "method.tex": "\\section{Method}...",
    "results.tex": "\\section{Results}...",
    "discussion.tex": "\\section{Discussion}...",
    "conclusion.tex": "\\section{Conclusion}..."
  },
  "word_counts": {
    "introduction": 650,
    "related_work": 1200,
    "method": 1800,
    "results": 900,
    "discussion": 600,
    "conclusion": 300
  },
  "citation_count": 24,
  "figure_references": ["fig:training_curve", "fig:comparison", "tab:results"]
}
```

**Checkpoint System**
```
User: @write-paper introduction

Agent: 
[Step 1/3] Analyzing context...
  ✓ Literature review: 18 papers
  ✓ Research gap: Low-resource VL
  ✓ Hypothesis: Synthetic data improves performance
  ✓ Key result: +5.2% improvement (p<0.01)
  
[Step 2/3] Drafting introduction (est. 3 min)...
  ✓ Generated 650 words
  ✓ Added 8 citations
  ✓ Structure: Context → Gap → Contribution → Outline
  
[Checkpoint] Preview:
  
  \section{Introduction}
  
  Vision-language models have achieved remarkable success on
  high-resource languages \cite{radford2021learning}, but
  performance degrades significantly for low-resource languages
  due to limited training data \cite{aggarwal2023multilingual}...
  
  [... 650 words total ...]
  
  The main contributions of this work are:
  \begin{itemize}
    \item A method to generate high-quality synthetic training data
          for low-resource vision-language tasks
    \item Empirical validation showing 5.2\% accuracy improvement
          over CLIP baseline (p<0.01)
    \item Analysis of effectiveness across 35 languages, with
          strongest gains on low-resource languages
  \end{itemize}
  
Accept this draft? (y/n/revise):

User: y

[Step 3/3] Saving...
  ✓ Saved to: paper/introduction.tex
  ✓ Word count: 650
  ✓ Citations: 8 (all in references.bib)
  
Next sections to draft:
  - @write-paper related-work (est. 5 min, 1200 words)
  - @write-paper method (est. 4 min, 1800 words)
  - @write-paper results (est. 3 min, 900 words)
  
Or: @write-paper all (draft all sections, est. 15 min)
```

**Cost & Performance per Section**
- Introduction: $0.10-0.15 (650 words, 3-5 min)
- Related Work: $0.15-0.25 (1200 words, 5-7 min)
- Method: $0.20-0.30 (1800 words, 4-6 min)
- Results: $0.10-0.15 (900 words, 3-5 min)
- Discussion: $0.10-0.15 (600 words, 3-4 min)
- Conclusion: $0.05-0.10 (300 words, 2-3 min)
- **Total for full paper**: $0.70-1.10, 20-30 minutes

**Dependencies**
- LiteratureAgent output (FR-006)
- HypothesisAgent output (FR-007)
- MethodAgent output (FR-008)
- AnalysisAgent output (FR-010)
- references.bib (FR-002)
- LLM client

**Edge Cases**
- Handle missing citations (add placeholder, warn user)
- Handle overly long sections (exceed word limit) - auto-trim or warn
- Handle inconsistent results (method says X, results show Y) - flag for review

---

### FR-012: ReviewAgent - Quality Check & Compliance (NEW) 🆕

**Priority**: P2 (Medium - Week 6)  
**Status**: Not Started  
**Agent**: Phase 7 of Research Pipeline (Final)

**Description**  
Reviews drafted paper for quality, citation completeness, and conference guideline compliance.

**User Story**  
"Before submitting my paper, I want an AI agent to check for missing citations, style issues, guideline compliance, and suggest improvements."

**Capabilities**
1. **Citation check**: Ensure all claims have proper citations
2. **Style review**: Check academic writing quality (clarity, conciseness)
3. **Guideline compliance**: Verify page limit, formatting, required sections
4. **Consistency check**: Cross-reference method description and results
5. **Improvement suggestions**: Highlight weak arguments or unclear statements
6. **Final checklist**: Submission readiness score (0-10)

**Triggers**
- Direct command: `@review-paper`
- Pipeline mode: Seventh phase in `@full-research` (after WritingAgent)

**Input** (from WritingAgent)
```json
{
  "paper_sections": {...},
  "figures": ["figures/..."],
  "tables": ["tables/..."],
  "references_bib": "path/to/references.bib",
  "venue": "NeurIPS"  # Optional: check venue-specific guidelines
}
```

**Output** (final artifacts)
```json
{
  "review_report": {
    "overall_score": 8.5,
    "readiness": "90%",
    "sections_reviewed": 6,
    "issues_found": 5,
    "issues_fixed": 2
  },
  "issues": [
    {
      "severity": "high",
      "location": "introduction.tex:45",
      "issue": "Claim without citation: 'multimodal models are widely used'",
      "suggestion": "Add citation to support this claim (e.g., \\cite{radford2021learning})"
    },
    {
      "severity": "medium",
      "location": "method.tex:120",
      "issue": "Passive voice overuse (65% of sentences)",
      "suggestion": "Rewrite some sentences in active voice for clarity"
    },
    {
      "severity": "low",
      "location": "results.tex:80",
      "issue": "Repetition: 'propose' used 8 times",
      "suggestion": "Use synonyms: suggest, introduce, present"
    }
  ],
  "guideline_compliance": {
    "page_limit": {"status": "pass", "actual": 8, "limit": 8},
    "sections": {"status": "pass", "missing": []},
    "citations": {"status": "pass", "count": 24, "formatted": true},
    "figures": {"status": "pass", "format": "PDF", "resolution": "300dpi"}
  },
  "suggested_revisions": "markdown text with actionable items"
}
```

**Checkpoint System**
```
User: @review-paper

Agent: 
[Step 1/5] Checking citations (est. 3 min)...
  ✓ Scanned 6 sections (4500 words)
  ✓ Found 24 citations
  ⚠ Found 3 claims without citations:
     1. introduction.tex:45 - "multimodal models are widely used"
     2. method.tex:230 - "synthetic data is effective"
     3. results.tex:180 - "our approach is efficient"
  
[Step 2/5] Checking style...
  ✓ Academic tone: Good
  ✓ Clarity: Good (Flesch reading ease: 45)
  ⚠ Passive voice: 65% (acceptable for methods, but high overall)
  ⚠ Repetition: "propose" used 8 times (suggest synonyms)
  
[Step 3/5] Checking guideline compliance (NeurIPS)...
  ✓ Page limit: 8/8 pages (perfect)
  ✓ Sections: All required sections present
  ✓ Figure format: All PDFs, 300dpi
  ✓ References: BibTeX formatted correctly
  ✓ Anonymization: No author names in text
  
[Step 4/5] Checking consistency...
  ✓ Method matches results (all baselines evaluated)
  ✓ Figures referenced in text (3/3)
  ⚠ Table 2 mentioned in results.tex but not found in tables/
  
[Step 5/5] Generating improvement suggestions...
  
[Checkpoint] Review Summary:
  
  Overall Score: 8.5/10 (Ready with minor revisions)
  Submission Readiness: 90%
  
  High Priority Issues (3):
   1. Add citation for claim in introduction.tex:45
   2. Add citation for claim in method.tex:230
   3. Add citation for claim in results.tex:180
  
  Medium Priority Issues (2):
   1. Reduce repetition of "propose" (8 occurrences)
   2. Add missing Table 2 or remove reference
  
  Low Priority Issues:
   - Consider rewriting some passive voice sentences
  
  Guideline Compliance: ✓ All checks passed (NeurIPS 2024)
  
Apply automatic fixes? (y/n/manual):

User: y

[Applying fixes...]
  ✓ Added citation placeholders for 3 uncited claims
  ✓ Replaced "propose" with synonyms where appropriate
  ✓ Removed Table 2 reference (table doesn't exist)
  
Updated score: 9.2/10
Submission readiness: 98%

Remaining manual tasks:
  - Fill in citation placeholders with specific papers
  - Final proofread for typos
  - Upload to conference submission system

Paper ready for submission! 🎉
```

**Cost & Performance**
- LLM calls: 5-8 (citation check, style review, suggestions)
- Total tokens: ~20K input + 8K output
- Cost: $0.20-0.40 per review
- Time: 5-8 minutes

**Dependencies**
- WritingAgent output (FR-011)
- references.bib (FR-002)
- LaTeX parsing library (for citation extraction)
- LLM client (for style and improvement suggestions)

**Edge Cases**
- Handle non-LaTeX formats (warn: only LaTeX supported)
- Handle unknown venue (skip venue-specific checks)
- Handle very long papers (> 20 pages) - may timeout, suggest section-by-section review

---

## 5. Updated Development Tasks

### Phase 1: Core Services (Week 1)
```yaml
# Same as v2.0
tasks:
  - T-001 to T-005 (unchanged)
```

### Phase 2: MCP Server + Basic Tools (Week 2)
```yaml
# Same as v2.0
tasks:
  - T-006 to T-008 (unchanged)
```

### Phase 3: Literature Review Feature (Week 3)

```yaml
tasks:
  - id: T-012
    name: Literature review service
    description: |
      - LLM client initialization (Anthropic/OpenAI)
      - Prompt templates
      - Review generation logic
      - Gap identification
      - Cost calculation
    estimate: 6h
    depends_on: [T-002, T-003]
    
  - id: T-013
    name: MCP tool integration
    description: |
      - Add generate_literature_review tool
      - Environment variable handling
      - Error handling for API failures
      - Token limit management
    estimate: 3h
    depends_on: [T-012, T-006]
    
  - id: T-014
    name: Prompt engineering
    description: |
      - Test prompts with sample papers
      - Optimize for quality and coherence
      - Handle edge cases (few papers, missing abstracts)
      - Validate citation format
    estimate: 4h
    depends_on: [T-012]
    
  - id: T-015
    name: Integration testing
    description: |
      - End-to-end test: search → review
      - Test with different paper counts (5, 20, 50, 100)
      - Test different structures (thematic, chronological)
      - Validate output quality manually
    estimate: 3h
    depends_on: [T-013, T-014]
```

### Phase 4: Multi-Agent System - Foundation (Week 4) 🆕

```yaml
tasks:
  - id: T-019
    name: Agent orchestration framework
    description: |
      - PolyhedraResearchOrchestrator (meta-agent)
      - ResearchState (lifecycle tracking)
      - Intent parsing with LLM
      - Agent registry and routing
      - Checkpoint system
      - Pipeline execution engine
    estimate: 12h
    depends_on: [T-006]
    
  - id: T-020
    name: BaseAgent class
    description: |
      - Abstract base class for all agents
      - Common capabilities (LLM access, tools, state)
      - Workflow execution framework
      - Error recovery patterns
      - Artifact management
    estimate: 6h
    depends_on: [T-019]
    
  - id: T-021
    name: LiteratureAgent (Phase 1)
    description: |
      - Search and index papers
      - Generate literature reviews
      - Identify research gaps
      - Paper comparison
      - Citation finding
    estimate: 8h
    depends_on: [T-020, T-012]
    
  - id: T-022
    name: IDE integration
    description: |
      - Cursor custom agent configuration
      - Command triggers (@research, @hypothesize, etc.)
      - Progress display in IDE
      - Checkpoint UI interactions
    estimate: 4h
    depends_on: [T-021]
```

### Phase 5: Multi-Agent System - Core Agents (Weeks 5-6) 🆕

```yaml
tasks:
  - id: T-024
    name: HypothesisAgent (Phase 2)
    description: |
      - Generate hypotheses from gaps
      - Novelty checking against literature
      - Feasibility analysis
      - Ranking by impact × feasibility
      - Interactive hypothesis selection
    estimate: 10h
    depends_on: [T-020]
    
  - id: T-025
    name: MethodAgent (Phase 3)
    description: |
      - Experimental design generation
      - Baseline selection
      - Dataset recommendation
      - Metrics definition
      - Resource estimation (GPU hours, cost)
      - Code scaffolding generation
    estimate: 12h
    depends_on: [T-020]
    
  - id: T-026
    name: WritingAgent (Phase 6)
    description: |
      - Paper section drafting (abstract, intro, method, etc.)
      - Citation integration from references.bib
      - Figure/table caption generation
      - LaTeX formatting
      - Section coherence checking
    estimate: 10h
    depends_on: [T-020, T-021]
    
  - id: T-027
    name: ReviewAgent (Phase 7)
    description: |
      - Citation completeness check
      - Figure/table reference validation
      - Grammar and clarity check
      - Novelty claim verification
      - Venue guideline compliance
    estimate: 8h
    depends_on: [T-026]
```

### Phase 6: Advanced Agents (Weeks 7-8) 🆕

```yaml
tasks:
  - id: T-028
    name: ExperimentAgent (Phase 4)
    description: |
      - Training code generation from methodology
      - Experiment setup automation
      - Progress monitoring integration (Wandb)
      - Checkpoint management
      - Failure detection and recovery
      - NOTE: Does not run compute, only setup/monitor
    estimate: 12h
    depends_on: [T-025]
    
  - id: T-029
    name: AnalysisAgent (Phase 5)
    description: |
      - Parse experiment logs and results
      - Generate plots (matplotlib/seaborn)
      - Statistical significance testing
      - Baseline comparison
      - Insight generation
      - LaTeX table generation
    estimate: 10h
    depends_on: [T-028]
    
  - id: T-030
    name: Full pipeline integration
    description: |
      - End-to-end pipeline testing
      - Agent handoff validation
      - State persistence across phases
      - Pipeline resume after interruption
      - @full-research command
    estimate: 8h
    depends_on: [T-024, T-025, T-026, T-027, T-028, T-029]
```

### Phase 7: Polish & Documentation (Week 9)

```yaml
tasks:
  - id: T-016
    name: Documentation
    description: |
      - Update README with literature review feature
      - API key setup instructions
      - Example workflows
      - Cost estimation guide
    estimate: 2h
    depends_on: [T-015]
    
  - id: T-017
    name: Configuration templates
    description: |
      - .env.example file
      - IDE config with LLM keys
      - Troubleshooting guide
    estimate: 2h
    depends_on: [T-016]
    
  - id: T-018
    name: Quality assurance
    description: |
      - Manual review of 5 generated reviews
      - Check citation accuracy
      - Verify gap identification quality
      - Cost benchmarking
    estimate: 3h
    depends_on: [T-015]
```

**Total Development Timeline**:
- Mode 1 only (Pure MCP): 3 weeks
- Mode 1 + LiteratureAgent: 4 weeks  
- **Full Multi-Agent System: 9 weeks** 🆕

**Incremental Delivery**:
- Week 4: LiteratureAgent (usable for literature review)
- Week 6: + HypothesisAgent + MethodAgent + WritingAgent (70% functionality)
- Week 8: + ExperimentAgent + AnalysisAgent + ReviewAgent (100% functionality)
- Week 9: Polish & documentation

---

## 6. Cost Analysis

### Literature Review Generation Costs

**Assumptions**:
- Average paper: 300 words (title + abstract)
- 50 papers = 15,000 words ≈ 20,000 tokens
- Review output: 3,000-5,000 words ≈ 6,000 tokens

**Cost per Review** (Claude 3.5 Sonnet):
- Input: 20,000 tokens × $3/1M = $0.06
- Output: 6,000 tokens × $15/1M = $0.09
- **Total: ~$0.15 per review**

**Cost per Review** (GPT-4 Turbo):
- Input: 20,000 tokens × $10/1M = $0.20
- Output: 6,000 tokens × $30/1M = $0.18
- **Total: ~$0.38 per review**

**Recommendation**: Default to Claude 3.5 Sonnet for cost-effectiveness.

---

## 7. Success Metrics (Updated)

### Performance Metrics

| Metric | Target | v2.0 | v2.1 |
|--------|--------|------|------|
| Paper Search | < 2 seconds | ✓ | ✓ |
| Local Operations | < 100ms | ✓ | ✓ |
| RAG Indexing | < 5 sec / 100 papers | ✓ | ✓ |
| RAG Query | < 500ms | ✓ | ✓ |
| **🆕 Literature Review** | **< 60 seconds** | - | **✓** |

### Quality Metrics (NEW)

| Metric | Target | Measurement |
|--------|--------|-------------|
| Review Coherence | 4/5 avg rating | Manual evaluation by researchers |
| Citation Accuracy | 100% valid format | Automated validation |
| Gap Relevance | 80% useful | Survey of users |
| Cost per Review | < $0.20 | Actual API usage |

### Adoption Metrics

| Metric | v2.0 Target | v2.1 Target |
|--------|-------------|-------------|
| Active Users (3 months) | 100+ | 150+ |
| Papers Searched | 10,000+ | 15,000+ |
| Projects Initialized | 50+ | 75+ |
| **🆕 Reviews Generated** | - | **500+** |

---

## 8. Migration from v2.0

### For Existing Users

**What's New**:
1. One new tool: `generate_literature_review`
2. Requires LLM API key (Anthropic or OpenAI)
3. All existing tools work exactly the same

**Migration Steps**:
1. Update Polyhedra: `pip install --upgrade polyhedra`
2. Add API key to environment: `export ANTHROPIC_API_KEY=...`
3. Update IDE config with env vars
4. (Optional) Try new tool: `generate_literature_review`

**Backward Compatibility**: 
- ✅ All v2.0 tools unchanged
- ✅ No breaking changes
- ✅ New tool is optional (skipped if no API key)

---

## 9. Roadmap & Evolution Path

### v2.1 (Current) - Multi-Agent Research System
**Timeline**: 9 weeks  
**Status**: In planning

**Agents**:
- ✅ LiteratureAgent (Phase 1: Literature Review)
- ✅ HypothesisAgent (Phase 2: Hypothesis Generation)
- ✅ MethodAgent (Phase 3: Method Design)
- ✅ ExperimentAgent (Phase 4: Experiment Setup)
- ✅ AnalysisAgent (Phase 5: Result Analysis)
- ✅ WritingAgent (Phase 6: Paper Writing)
- ✅ ReviewAgent (Phase 7: Review & Polish)

**Capabilities**:
- Complete research lifecycle coverage
- Agent orchestration and handoffs
- State management across phases
- Checkpoint-based user control
- End-to-end pipeline (@full-research)

### v2.2 (Q1 2026) - Enhanced Intelligence
**Timeline**: +4 weeks  

**New Features**:
- **Adaptive Agents**: Learn from user preferences
  - Remember which papers user finds relevant
  - Adapt writing style to match user's papers
  - Adjust checkpoint frequency based on user trust
  
- **Multi-modal Support**:
  - Generate figures from data
  - OCR for reading paper figures
  - Code-to-diagram conversion
  
- **Advanced Analysis**:
  - Citation network visualization
  - Research trend prediction
  - Conference acceptance probability estimation
  
- **Collaboration**:
  - Team mode (shared state)
  - Multi-author paper writing
  - Reviewer feedback integration

### v2.3 (Q2 2026) - Production Ready
**Timeline**: +3 weeks  

**Enhancements**:
- **Robustness**:
  - 99% uptime for critical agents
  - Comprehensive error recovery
  - Data backup and versioning
  
- **Performance**:
  - 2x faster literature review (parallel processing)
  - 50% cost reduction (prompt optimization)
  - Caching and incremental updates
  
- **Integration**:
  - Overleaf sync
  - Zotero import/export
  - Wandb/TensorBoard integration
  - arXiv submission automation

### v3.0 (Q3 2026) - Full Research Assistant
**Timeline**: +8 weeks  

**Major Upgrades**:
- **Confidence-Driven Autonomy** (ResearchKit approach):
  - Self-assess output quality
  - Request review only when uncertain
  - Explain reasoning for all decisions
  
- **User Profile Learning**:
  - Research interests and expertise
  - Writing style and preferences
  - Resource constraints (budget, timeline)
  - Publication strategy
  
- **Proactive Assistance**:
  - Suggest research directions
  - Alert on relevant new papers
  - Recommend collaborators
  - Track paper deadlines
  
- **Advanced Workflows**:
  - Multi-paper comparative studies
  - Meta-analysis generation
  - Literature survey papers
  - Replication studies

### Evolution Comparison

| Version | Agents | Autonomy | Lifecycle Coverage | Development |
|---------|--------|----------|-------------------|-------------|
| v2.0 | 0 (Pure tools) | Manual | 20% (literature only) | 3 weeks |
| v2.1 | 7 specialized | Supervised | 100% (full pipeline) | 9 weeks |
| v2.2 | 7 + enhancements | Adaptive | 100% + collaboration | +4 weeks |
| v2.3 | 7 + production | Reliable | 100% + integrations | +3 weeks |
| v3.0 | 10+ (specialized) | Confident | 100% + proactive | +8 weeks |

### Research Lifecycle Coverage Evolution

```
v2.0: [████░░░░░░░░░░░░░░░░] 20%
      Literature review only

v2.1: [████████████████████] 100%
      Complete research pipeline:
      Literature → Hypothesis → Method → Experiments
      → Analysis → Writing → Review

v2.2: [████████████████████] 100% + Collaboration
      + Team features, multi-modal support

v2.3: [████████████████████] 100% + Integrations
      + External tools (Overleaf, Zotero, arXiv)

v3.0: [████████████████████] 100% + Proactive
      + Confidence-driven, learning, suggestions
```

### Comparison with ResearchKit v2.0

| Feature | ResearchKit v2.0 | Polyhedra v2.1 | Polyhedra v3.0 |
|---------|------------------|----------------|----------------|
| **Agents** | 6 agents | 7 agents | 10+ agents |
| **Philosophy** | Collaborative | Supervised | Confident |
| **Interaction** | Progressive clarification | Checkpoint-based | Adaptive |
| **Learning** | User profiles | None yet | Full learning |
| **Branching** | Built-in | Not yet | Planned v3.0 |
| **Transparency** | Explainable decisions | Basic | Full reasoning |
| **Timeline** | 8 months (complex) | 9 weeks (focused) | +6 months |

**Strategic Positioning**:
- **v2.1**: Faster to market, covers full lifecycle
- **v3.0**: Matches ResearchKit's sophistication
- **Approach**: Incremental delivery vs big-bang release

---

## 10. Open Questions

1. **Chunking Strategy**: How to handle >100 papers exceeding context window?
   - Option A: Summarize papers first, then synthesize summaries
   - Option B: Generate review in multiple passes (per category)
   - Decision: TBD based on testing

2. **Review Quality Validation**: How to ensure consistent quality?
   - Approach: Manual review of first 50 generated reviews
   - Collect user feedback via survey
   - Iterate on prompts based on feedback

3. **Cost Management**: Should we add a token budget limit?
   - Concern: Users accidentally generating expensive reviews
   - Proposal: Add `max_cost` parameter (default $1.00)
   - Warn user before generation if estimate exceeds budget

4. **Multi-language Support**: Should reviews support non-English papers?
   - Current: English only
   - Future: Detect paper language, generate review in same language

---

## Appendix A: Example Usage

### Scenario: Generate Literature Review

```bash
# Step 1: Search papers
$ # In IDE, call: search_papers("efficient vision transformers", limit=50)
# → Saves to literature/papers.json

# Step 2: Generate review
$ # In IDE, call: generate_literature_review()
# → Generates review
# → Saves to literature/review.md
# → Returns:
{
  "success": true,
  "saved_to": "literature/review.md",
  "metadata": {
    "paper_count": 47,
    "word_count": 4523,
    "sections": [
      "Overview",
      "Taxonomy of Approaches",
      "Architecture-based Methods",
      "Training-based Methods",
      "Deployment-focused Methods",
      "Critical Analysis",
      "Research Gaps",
      "Conclusion"
    ],
    "research_gaps": [
      {
        "title": "Scaling sparse attention beyond 1B parameters",
        "description": "Current work on sparse attention...",
        "significance": "..."
      },
      ...
    ],
    "citations_added": 47
  },
  "cost": {
    "input_tokens": 18234,
    "output_tokens": 5890,
    "total_usd": 0.14
  }
}

# Step 3: Review the output
$ # Open literature/review.md in editor
# → Edit if needed
# → All citations already in references.bib
```

### Generated Review Sample

```markdown
# Literature Review: Efficient Vision Transformers

## Overview

Vision Transformers (ViTs) have demonstrated remarkable performance across 
various computer vision tasks, but their computational demands remain a 
significant barrier to practical deployment. This review synthesizes 47 
recent papers (2022-2024) exploring efficiency improvements for ViTs, 
organizing approaches into three main categories: architecture modifications, 
training optimizations, and deployment techniques.

## Taxonomy of Approaches

### 1. Architecture-based Methods

Architecture-based approaches modify the ViT structure to reduce computational 
complexity while maintaining accuracy.

**Sparse Attention Mechanisms** focus on reducing the quadratic complexity 
of self-attention. Notable work includes EfficientViT [@liu2023efficient], 
which introduces a memory-efficient attention design achieving 3× speedup 
with <1% accuracy drop. Similarly, Sparse ViT [@chen2023sparse] demonstrates 
that structured sparsity patterns can scale to larger models effectively.

**Hierarchical Designs** adopt pyramid structures similar to CNNs. 
MobileViT [@mehta2022mobile] combines convolutions with transformers for 
mobile deployment, while Swin Transformer [@liu2021swin] uses shifted 
windows to limit attention scope, achieving linear complexity.

[... continues with detailed analysis ...]

## Research Gaps

Based on this review, we identify five critical gaps:

1. **Scaling Sparse Attention Beyond 1B Parameters**
   - Current work demonstrates sparse attention up to 1B parameters
   - Unclear if benefits persist at 10B+ scale
   - Potential approaches: Hybrid sparse-dense architectures

2. **Unified Efficiency Metrics**
   - Papers report FLOPs, latency, memory separately
   - Need standardized benchmarking framework
   - Potential: Community-wide efficiency benchmark suite

[... more gaps ...]

## Conclusion

The field of efficient Vision Transformers has made substantial progress, 
with sparse attention and hierarchical designs showing particular promise. 
However, significant gaps remain, especially in scaling efficiency techniques 
to larger models and establishing standardized evaluation protocols. Future 
work should prioritize real-world deployment scenarios and cross-technique 
combinations.
```

---

## Appendix B: Comparison Table

| Feature | v2.0 | v2.1 |
|---------|------|------|
| Paper Search | ✓ | ✓ |
| Citation Management | ✓ | ✓ |
| RAG Retrieval | ✓ | ✓ |
| File Management | ✓ | ✓ |
| **Literature Review** | **IDE's LLM** | **✓ Built-in** |
| Hypothesis Generation | IDE's LLM | IDE's LLM |
| Method Design | IDE's LLM | IDE's LLM |
| Paper Writing | IDE's LLM | IDE's LLM |
| **Requires API Key** | **No** | **Yes (Anthropic/OpenAI)** |
| **Setup Time** | **< 5 min** | **< 10 min** |
| **Development Time** | **3 weeks** | **4 weeks** |

---

## Appendix C: Feature Matrix

### Functional Requirements Summary

| ID | Requirement | Priority | Status | Mode 1 (MCP) | Mode 2 (Agent) |
|----|-------------|----------|--------|--------------|----------------|
| FR-001 | Paper Search | P0 | Not Started | ✓ Manual call | ✓ Auto in workflows |
| FR-002 | RAG Retrieval | P0 | Not Started | ✓ Manual call | ✓ Auto in workflows |
| FR-003 | Citation Management | P0 | Not Started | ✓ Manual call | ✓ Auto in workflows |
| FR-004 | Context Management | P0 | Not Started | ✓ Manual call | ✓ Auto in workflows |
| FR-005 | Project Initialization | P1 | Not Started | ✓ Manual call | ✓ Auto in workflows |
| FR-006 | Literature Review | P1 | Not Started | ✓ Manual call | ✓ Auto in workflows |
| FR-007 | Custom Agent | P1 | Not Started | ✗ Not available | ✓ Core feature |
| FR-008 | Workflow System | P1 | Not Started | ✗ Not available | ✓ Core feature |

### Development Effort Comparison

| Aspect | Mode 1 Only | Mode 1 + Mode 2 |
|--------|-------------|-----------------|
| **Development Time** | 4 weeks | 5 weeks |
| **Codebase Size** | ~3,000 LOC | ~5,000 LOC |
| **Test Coverage** | Tools + Services | + Agent + Workflows |
| **Complexity** | Low | Medium |
| **Maintenance** | Minimal | Moderate |

### User Experience Comparison

| Scenario | Mode 1: Pure MCP | Mode 2: Custom Agent |
|----------|------------------|----------------------|
| **Literature Survey** | 5 manual steps | 1 command: @research |
| **Paper Comparison** | 3 manual steps | 1 command: @compare |
| **Find Citations** | 2 manual steps | 1 command: @cite |
| **Error Handling** | Manual retry | Auto retry + recovery |
| **Cost Awareness** | Check manually | Auto warnings |
| **Learning Curve** | Steep | Gentle |

---

**Document Status**: Draft - Ready for Team Review  
**Next Steps**: 
1. Validate literature review prompt with sample papers
2. Prototype LiteratureReviewService
3. Prototype Custom Agent framework (PolyhedraResearchAgent)
4. Test workflows with real research tasks
5. Cost analysis with real API usage
6. User testing with PhD students (both modes)
