# Polyhedra User Stories - Complete Set

## Overview

This directory contains all 12 user stories for **EPIC-001: Polyhedra MCP Server MVP**.

---

## Story Index

### Phase 1: Core Services (Week 1) - Stories 1-5

| Story | Title | Points | Status | Sprint |
|-------|-------|--------|--------|--------|
| [STORY-001](STORY-001-semantic-scholar-integration.md) | Semantic Scholar Integration | 5 | Not Started | Week 1, Days 1-2 |
| [STORY-002](STORY-002-citation-management.md) | Citation Management | 3 | Not Started | Week 1, Day 3 |
| [STORY-003](STORY-003-rag-retrieval.md) | RAG Retrieval System | 5 | Not Started | Week 1, Day 4 |
| [STORY-004](STORY-004-file-context-management.md) | File & Context Management | 3 | Not Started | Week 1, Day 5 |
| [STORY-005](STORY-005-project-initialization.md) | Project Initialization | 2 | Not Started | Week 1, Day 5 |

**Phase 1 Total: 18 story points**

---

### Phase 2: MCP Server (Week 2) - Stories 6-9

| Story | Title | Points | Status | Sprint |
|-------|-------|--------|--------|--------|
| [STORY-006](STORY-006-mcp-server-core.md) | MCP Server Core | 5 | Not Started | Week 2, Days 6-7 |
| [STORY-007](STORY-007-tool-implementations.md) | Tool Implementations | 5 | Not Started | Week 2, Day 8 |
| [STORY-008](STORY-008-ide-integration.md) | IDE Integration Configs | 3 | Not Started | Week 2, Day 9 |
| [STORY-009](STORY-009-integration-testing.md) | Integration Testing | 3 | Not Started | Week 2, Day 9 |

**Phase 2 Total: 16 story points**

---

### Phase 3: Polish & Launch (Week 3) - Stories 10-12

| Story | Title | Points | Status | Sprint |
|-------|-------|--------|--------|--------|
| [STORY-010](STORY-010-error-handling.md) | Error Handling & Resilience | 3 | Not Started | Week 3, Day 11 |
| [STORY-011](STORY-011-documentation.md) | Documentation & Examples | 3 | Not Started | Week 3, Days 12-13 |
| [STORY-012](STORY-012-package-publish.md) | Package & Publish | 2 | Not Started | Week 3, Day 14 |

**Phase 3 Total: 8 story points**

---

## Total Epic Summary

- **Total Stories**: 12
- **Total Story Points**: 42
- **Timeline**: 3 weeks (15 working days)
- **Average Velocity**: 14 points/week

---

## Story Dependencies

```
Phase 1 (Foundation)
├── STORY-001: Semantic Scholar Integration
├── STORY-002: Citation Management (depends on STORY-001)
├── STORY-003: RAG Retrieval (depends on STORY-001)
├── STORY-004: File & Context Management
└── STORY-005: Project Initialization (depends on STORY-004)

Phase 2 (MCP Implementation)
├── STORY-006: MCP Server Core (depends on Phase 1)
├── STORY-007: Tool Implementations (depends on STORY-006)
├── STORY-008: IDE Integration Configs (depends on STORY-006)
└── STORY-009: Integration Testing (depends on STORY-007, STORY-008)

Phase 3 (Launch)
├── STORY-010: Error Handling (depends on Phase 2)
├── STORY-011: Documentation (depends on Phase 2)
└── STORY-012: Package & Publish (depends on STORY-011)
```

---

## Quick Reference

### By Priority

**P0 (Critical) - 10 stories:**
- STORY-001, 002, 003, 004, 006, 007, 008, 009, 010, 011

**P1 (High) - 2 stories:**
- STORY-005, 012

### By Sprint Week

**Week 1:** STORY-001 → STORY-005 (18 points)  
**Week 2:** STORY-006 → STORY-009 (16 points)  
**Week 3:** STORY-010 → STORY-012 (8 points)

---

## Development Workflow

### Starting Development

1. **Read Epic**: [`docs/epics/EPIC-001-polyhedra-mvp.md`](../epics/EPIC-001-polyhedra-mvp.md)
2. **Read PRD**: [`docs/prd.md`](../prd.md)
3. **Start with STORY-001**: Semantic Scholar Integration
4. **Follow dependency order** as shown above

### For Each Story

1. Read story document thoroughly
2. Review acceptance criteria
3. Set up development environment
4. Implement following task breakdown
5. Write tests (unit + integration)
6. Run manual testing checklist
7. Submit for code review
8. Complete definition of done
9. Move to next story

### Story Completion Criteria

Each story is complete when:
- [ ] All acceptance criteria met
- [ ] Unit tests written and passing (>80% coverage)
- [ ] Integration tests passing
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Manual testing checklist completed
- [ ] No new P0/P1 bugs introduced

---

## Testing Strategy

### Unit Tests
- **Location**: `tests/test_services/`
- **Coverage Target**: >80%
- **Run**: `pytest tests/test_services/`

### Integration Tests
- **Location**: `tests/test_integration/`
- **Coverage**: End-to-end workflows
- **Run**: `pytest tests/test_integration/`

### Manual Testing
- Each story has a manual testing checklist
- Test in at least 2 IDEs (Cursor + VS Code recommended)
- Verify performance targets met

---

## Success Metrics

### Development Metrics
- All 12 stories completed
- Code coverage >80%
- Zero P0 bugs in production

### Performance Metrics
- Paper search: < 2s (95th percentile)
- Local operations: < 100ms
- RAG query: < 500ms

### User Metrics (Post-Launch)
- Setup time: < 5 minutes
- 50+ installations in first 30 days
- Positive user feedback

---

## Getting Help

- **Epic Questions**: Review EPIC-001 document
- **Technical Questions**: Check PRD Section 2 (Architecture)
- **Story Clarifications**: Comment in story document
- **Blockers**: Escalate to Product Owner

---

## Document History

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-29 | 1.0 | Initial story set created |

---

**Epic**: [EPIC-001: Polyhedra MCP Server MVP](../epics/EPIC-001-polyhedra-mvp.md)  
**PRD**: [Polyhedra Product Requirements](../prd.md)  
**Status**: Ready for Development
