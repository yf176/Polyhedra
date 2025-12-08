# EPIC-V2.1-002: Custom Agent Mode & Autonomous Research Workflows

## Epic Metadata

| Field | Value |
|-------|-------|
| **Epic ID** | EPIC-V2.1-002 |
| **Epic Name** | Custom Agent Mode & Autonomous Research Workflows |
| **Project** | Polyhedra |
| **Type** | Brownfield Enhancement - Optional Feature |
| **Priority** | P1 (High - Nice to Have for v2.1) |
| **Status** | Not Started |
| **Created** | November 30, 2025 |
| **Target Completion** | 2-3 weeks (10-15 days) |
| **Owner** | Engineering Team |
| **Dependencies** | EPIC-V2.1-001 (Core LLM Integration) must be complete |

---

## Executive Summary

Transform Polyhedra into an autonomous research assistant that can execute complex multi-step workflows with a single command (e.g., "@research efficient transformers"). This epic builds on Epic 1's LLM foundation to provide BMAD-style autonomous agent capabilities.

### Business Value

- **For Researchers**: Delegate entire workflows instead of orchestrating individual tool calls
- **For Productivity**: Reduced cognitive loadagent handles workflow planning and error recovery
- **For Efficiency**: Faster research iteration with pre-built workflows for common tasks
- **For Differentiation**: Competitive differentiatorautonomous agent mode like BMAD but for research

### Success Metrics

- Custom agent workflow success rate >95% without user intervention (except checkpoints)
- Average workflow completion time <10 minutes for standard tasks
- User satisfaction: "Would recommend agent mode" >80%
- Error recovery success rate >90%

---

## Epic Goal

Enable researchers to delegate complex multi-step research tasks to an autonomous agent that understands natural language commands, executes workflows with minimal supervision, and recovers gracefully from errors.

---

## Scope

### In Scope

**Agent Framework (Week 1)**
- Core agent orchestration system
- Workflow execution engine
- Checkpoint and approval system
- State persistence

**Intent Understanding (Week 1-2)**
- Natural language command parsing
- Intent extraction and classification
- Parameter recognition
- Command validation

**Research Workflows (Week 2)**
- Literature survey workflow (search  index  review  gaps)
- Paper comparison workflow
- Gap analysis workflow
- Citation finding workflow

**Error Recovery (Week 2)**
- Retry logic with exponential backoff
- Graceful degradation
- Partial result preservation
- Clear error reporting

**IDE Integration (Week 2-3)**
- Cursor Custom Agent packaging
- GitHub Copilot Agent packaging
- Configuration templates
- Setup documentation

**Testing (Week 3)**
- Workflow integration tests
- Error recovery tests
- Intent parsing tests
- End-to-end agent tests

### Out of Scope

- Additional LLM providers beyond Epic 1 (OpenAI, Anthropic)
- Real-time collaboration features
- Multi-project workspace support
- Advanced workflow customization UI

---

## Integration Requirements

### Optional Feature Design

- Agent mode is **completely optional**system works without it
- Agent reuses all Epic 1 tools (no code duplication)
- Agent module is isolated in src/polyhedra/agent/
- Can be excluded from builds for users who don't need it
- IDE-specific packaging (Cursor, Copilot Agents)

### Technical Integration

**File Structure**:
`
src/polyhedra/
  agent/
    research_agent.py        # NEW: Main agent orchestrator
    intent_parser.py         # NEW: Command understanding
    workflows/               # NEW: Pre-built workflows
      literature_survey.py
      paper_comparison.py
      gap_analysis.py
      citation_finding.py
    checkpoint.py           # NEW: User approval system
    state_manager.py        # NEW: State persistence
  services/                 # FROM EPIC 1: Reused
    llm_service.py
    literature_review_service.py
  server.py                 # UNCHANGED: Agent mode separate
`

---

## Story Sequencing Rationale

Stories build autonomous capabilities progressively:

1. **Story 2.1**: Core agent orchestration framework
2. **Story 2.2**: Intent understanding and command parsing
3. **Story 2.3**: Pre-built workflow implementations
4. **Story 2.4**: Error recovery and checkpoint system
5. **Story 2.5**: IDE integration and packaging
6. **Story 2.6**: Agent-specific testing

Each story adds a layer of autonomy while maintaining the option to use Epic 1's tools directly.

---

## Stories

| Story ID | Title | Priority | Est. Days | Dependencies | Status |
|----------|-------|----------|-----------|--------------|--------|
| [STORY-V2.1-007](../stories/STORY-V2.1-007-agent-orchestration.md) | Agent Orchestration Framework | P1 | 3-4 | Epic 1 | Not Started |
| [STORY-V2.1-008](../stories/STORY-V2.1-008-intent-understanding.md) | Intent Understanding & Command Parsing | P1 | 2-3 | 007 | Not Started |
| [STORY-V2.1-009](../stories/STORY-V2.1-009-research-workflows.md) | Pre-built Research Workflows | P2 | 3-4 | 008 | Not Started |
| [STORY-V2.1-010](../stories/STORY-V2.1-010-error-recovery.md) | Error Recovery & Checkpoint System | P1 | 2-3 | 009 | Not Started |
| [STORY-V2.1-011](../stories/STORY-V2.1-011-ide-integration.md) | IDE Integration & Packaging | P1 | 2-3 | 007-010 | Not Started |
| [STORY-V2.1-012](../stories/STORY-V2.1-012-agent-testing.md) | Agent-Specific Testing | P1 | 2-3 | 007-011 | Not Started |

**Total Estimated Effort**: 14-20 days (~2-4 weeks)

---

## Risks and Mitigation

### Technical Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Complex workflow failures | High | Comprehensive checkpoint system, state persistence |
| Intent misunderstanding | Medium | Clear command patterns, fallback to tool mode |
| Infinite loops in error recovery | Medium | Max retry limits, timeout mechanisms |
| Resource exhaustion | Low | Memory limits, operation timeouts |

### User Experience Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Agent too autonomous | Medium | Configurable checkpoints, user control |
| Unclear agent actions | Low | Progress reporting, transparent logging |
| Workflow interruptions | Low | State persistence, resume capability |

### Integration Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| IDE compatibility issues | Medium | Thorough testing across IDEs |
| Agent conflicts with IDE features | Low | Clear separation, optional deployment |
| Performance overhead | Low | Async operations, efficient state management |

---

## Definition of Done

- [ ] All 6 stories completed and tested
- [ ] Agent mode works in Cursor and GitHub Copilot
- [ ] Workflow success rate >95%
- [ ] Error recovery success rate >90%
- [ ] Agent tests pass with >85% coverage
- [ ] Documentation complete (agent guide, workflow docs)
- [ ] User testing validates autonomous capabilities
- [ ] Code reviewed and merged to main branch
- [ ] Release notes prepared

---

## Dependencies

**Internal Dependencies**:
- **EPIC-V2.1-001 MUST be complete**: Agent reuses LLM service and literature review tool

**External Dependencies**:
- LLM APIs (from Epic 1: OpenAI/Anthropic)
- IDE support for custom agents (Cursor, GitHub Copilot)

**Blocking For**:
- None (optional feature, doesn't block other work)

---

## Delivery Options

### Option 1: Include in v2.1.0
- Deliver both Epic 1 and Epic 2 together
- **Timeline**: 5-7 weeks total (Epic 1: 3-4 weeks + Epic 2: 2-3 weeks)
- **Value**: Complete v2.1 experience with both tools and agent

### Option 2: Defer to v2.1.1 (Recommended)
- Deliver Epic 1 as v2.1.0 (tools + literature review)
- Deliver Epic 2 as v2.1.1 (agent mode)
- **Timeline**: v2.1.0 in 3-4 weeks, v2.1.1 in 2-3 weeks after
- **Value**: Faster time-to-market, reduced initial complexity, user feedback before agent

### Option 3: Make Fully Optional
- Package agent mode as separate install/plugin
- Users opt-in to agent capabilities
- **Timeline**: Can be developed in parallel with or after v2.1.0
- **Value**: Maximum flexibility, no impact on base system
