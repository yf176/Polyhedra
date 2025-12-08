# EPIC-V2.1-001: Core LLM Integration & Literature Review Generation

## Epic Metadata

| Field | Value |
|-------|-------|
| **Epic ID** | EPIC-V2.1-001 |
| **Epic Name** | Core LLM Integration & Literature Review Generation |
| **Project** | Polyhedra |
| **Type** | Brownfield Enhancement - New Feature Addition |
| **Priority** | P0 (Critical - Must Have for v2.1) |
| **Status** | Not Started |
| **Created** | November 30, 2025 |
| **Target Completion** | 3-4 weeks (15-22 days) |
| **Owner** | Engineering Team |
| **Dependencies** | None (foundational epic) |

---

## Executive Summary

Add LLM-powered literature review generation capability to Polyhedra while maintaining 100% backward compatibility with existing v2.0 functionality. This epic delivers the foundational LLM integration and first concrete agent capability that provides immediate value to researchers.

### Business Value

- **For Researchers**: Synthesize 20-100 papers into structured reviews in minutes instead of days
- **For Cost Management**: Cost-transparent LLM usage with user confirmation before expensive operations
- **For Existing Users**: Zero disruptionLLM features are opt-in
- **For Future**: Establishes foundation for future agent capabilities

### Success Metrics

- Literature review generation completes in <3 minutes for 50 papers
- 100% of existing v2.0 tests pass without modification
- Setup time remains <15 minutes including LLM configuration
- Cost per review stays <$0.50 for standard depth

---

## Epic Goal

Transform Polyhedra from a pure MCP tool server into a hybrid system that supports both passive tools (v2.0 functionality) and active agent capabilities (v2.1 features), with literature review generation as the flagship feature.

---

## Scope

### In Scope

**Core LLM Infrastructure (Week 1)**
- LLM service layer with multi-provider support (OpenAI, Anthropic)
- Configuration via environment variables
- Token counting and cost calculation
- Error handling for API failures

**Literature Review Generation (Weeks 1-2)**
- Literature review service accepting paper collections
- Structured output with sections: Overview, Taxonomy, Critical Analysis, Gaps, Conclusion
- Three depth levels: brief (2-3 pages), standard (5-8 pages), comprehensive (10-15 pages)
- Proper academic citations

**MCP Integration (Week 2)**
- New `generate_literature_review` tool
- Integration with existing paper search tools
- Automatic citation management
- Cost estimation and user confirmation

**Testing & Documentation (Weeks 2-3)**
- Comprehensive integration testing
- Documentation updates for new features
- Example usage scenarios
- Troubleshooting guides

### Out of Scope

- Custom agent mode (Epic 2)
- Pre-built research workflows (Epic 2)
- Autonomous multi-step execution (Epic 2)
- Intent understanding system (Epic 2)

---

## Integration Requirements

### Backward Compatibility

- All existing v2.0 MCP tools continue to function identically without LLM configuration
- New LLM service is isolatedno changes to existing services
- MCP server tool registration extended but existing tools unchanged
- All existing IDE integrations remain functional
- Clear separation: existing features work WITHOUT API keys, new features require API keys

### Technical Integration

**File Structure**:
`
src/polyhedra/
  services/
    llm_service.py              # NEW: LLM provider abstraction
    literature_review_service.py # NEW: Review generation logic
    semantic_scholar.py          # UNCHANGED
    citation_manager.py          # UNCHANGED
    rag_service.py              # UNCHANGED
  server.py                     # MODIFIED: Register new tool
`

**Zero Breaking Changes**:
- No modifications to existing service interfaces
- No changes to existing tool signatures
- No database schema changes (file-based storage)
- No configuration changes required for v2.0 features

---

## Story Sequencing Rationale

Stories are sequenced to minimize risk to the existing system:

1. **Story 1.1**: Build isolated LLM service (no impact on v2.0)
2. **Story 1.2**: Add literature review service on top of LLM service (isolated module)
3. **Story 1.3**: Integrate with MCP server (minimal, additive changes)
4. **Story 1.4**: Add cost safety features (user protection)
5. **Story 1.5**: Documentation updates (enable users)
6. **Story 1.6**: Comprehensive testing (ensure v2.0 + v2.1 both work)

Each story is independently testable and delivers incremental value while maintaining system integrity.

---

## Stories

| Story ID | Title | Priority | Est. Days | Dependencies | Status |
|----------|-------|----------|-----------|--------------|--------|
| [STORY-V2.1-001](../stories/STORY-V2.1-001-llm-service-foundation.md) | LLM Service Foundation | P0 | 2-3 | None | Not Started |
| [STORY-V2.1-002](../stories/STORY-V2.1-002-literature-review-service.md) | Literature Review Service | P0 | 3-4 | 001 | Not Started |
| [STORY-V2.1-003](../stories/STORY-V2.1-003-mcp-tool-integration.md) | MCP Tool Integration | P0 | 2-3 | 002 | Not Started |
| [STORY-V2.1-004](../stories/STORY-V2.1-004-cost-estimation.md) | Cost Estimation & Confirmation | P1 | 1-2 | 003 | Not Started |
| [STORY-V2.1-005](../stories/STORY-V2.1-005-documentation-updates.md) | Documentation Updates | P1 | 2-3 | 001-004 | Not Started |
| [STORY-V2.1-006](../stories/STORY-V2.1-006-integration-testing.md) | Comprehensive Integration Testing | P0 | 3-4 | 001-005 | Not Started |

**Total Estimated Effort**: 15-22 days (~3-4 weeks)

---

## Risks and Mitigation

### Technical Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| LLM API rate limits | Medium | Exponential backoff, user notification, cost estimation |
| Token limit exceeded | High | Paper content chunking and batching |
| LLM response quality | Medium | Prompt engineering, user feedback mechanism |
| Breaking existing tools | High | Comprehensive regression testing, isolated LLM service |

### Integration Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Configuration complexity | Medium | Clear documentation, optional LLM features |
| Performance degradation | Medium | Async operations, caching, benchmarking |
| API key security | Low | Environment variable best practices documentation |

### Deployment Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Upgrade failures | Low | Version pinning, rollback plan, backward compatibility |
| Cost surprises | Medium | Cost estimation, user confirmation, budget tracking |
| User confusion | Low | Clear v2.0 vs v2.1 feature distinction in docs |

---

## Definition of Done

- [ ] All 6 stories completed and tested
- [ ] 100% of existing v2.0 tests pass without modification
- [ ] New integration tests pass with >85% coverage
- [ ] Literature review generation works in all supported IDEs
- [ ] Documentation complete and reviewed
- [ ] Cost estimation accurate within 20%
- [ ] Performance benchmarks met (<3 min for 50 papers)
- [ ] Code reviewed and merged to main branch
- [ ] Release notes prepared

---

## Dependencies

**External Dependencies**:
- OpenAI API access (user provides API key)
- Anthropic API access (user provides API key, optional)
- Existing Semantic Scholar API (already integrated in v2.0)

**Internal Dependencies**:
- None (foundational epic, no dependencies on other epics)

**Blocking For**:
- EPIC-V2.1-002 (Custom Agent Mode) depends on completion of this epic

---

## Delivery Options

### Option 1: Minimum Viable v2.1 (Recommended)
- Deliver Epic 1 only for v2.1.0
- Epic 2 can follow in v2.1.1 if needed
- **Timeline**: 3-4 weeks
- **Value**: Immediate literature review capability

### Option 2: Full v2.1 Release
- Deliver both Epic 1 and Epic 2 for v2.1.0
- **Timeline**: 6-8 weeks
- **Value**: Complete autonomous agent experience

### Option 3: Phased Delivery (Recommended for Low Risk)
- v2.1.0: Epic 1 only (3-4 weeks)
- v2.1.1: Epic 2 (2-3 weeks after v2.1.0)
- **Timeline**: Total 6-8 weeks, but phased
- **Value**: Earlier time-to-market, reduced deployment risk
