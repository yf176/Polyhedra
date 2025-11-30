# EPIC-001: Polyhedra MCP Server MVP

## Epic Metadata

| Field | Value |
|-------|-------|
| **Epic ID** | EPIC-001 |
| **Epic Name** | Polyhedra MCP Server MVP |
| **Project** | Polyhedra |
| **Type** | Greenfield - Initial Implementation |
| **Priority** | P0 (Critical) |
| **Status** | Not Started |
| **Created** | November 29, 2025 |
| **Target Completion** | 3 weeks |
| **Owner** | Engineering Team |

---

## Executive Summary

Build a production-ready Model Context Protocol (MCP) tool server that extends IDE AI assistants with academic research capabilities. This epic covers the complete MVP implementation including paper search, citation management, RAG retrieval, and file operations.

### Business Value

- **For Researchers**: Streamlines academic research workflow within their IDE
- **For PhD Students**: Reduces research overhead from hours to minutes
- **For Engineering**: Establishes reusable MCP server architecture
- **Market Position**: First pure MCP tool for academic research

### Success Metrics

- Sub-2-second paper search response time
- 100% valid BibTeX generation
- 4+ IDE integrations working (Cursor, Copilot, Windsurf, VS Code)
- Setup time < 5 minutes

---

## Epic Goal

Deliver a fully functional MCP tool server that enables researchers to search academic papers, manage citations, and write research documents entirely within their IDE, with all content generation handled by the IDE's native AI assistant.

---

## Scope

### In Scope

**Phase 1: Core Services (Week 1)**
- Semantic Scholar API integration
- Citation management with BibTeX
- RAG service with semantic search
- Context and file management
- Project initialization

**Phase 2: MCP Server (Week 2)**
- MCP protocol implementation
- 10 tool endpoints
- IDE configuration templates
- Integration testing

**Phase 3: Polish & Launch (Week 3)**
- Error handling and resilience
- Documentation and examples
- PyPI packaging
- IDE-specific setup guides

### Out of Scope

- Built-in LLM calls (delegated to IDE)
- Agent orchestration layer
- Custom UI components
- PDF parsing/download
- Citation style conversion beyond BibTeX
- Multi-user collaboration features
- Cloud deployment options

---

## Architecture Overview

`

                  IDE (Cursor / Copilot)                 
    
                IDE's LLM (Claude/GPT)                 
     Intent understanding                             
     Literature review generation                     
     Paper writing                                    
    
                         MCP Protocol                    
    
              Polyhedra MCP Server                     
                                                       
    Tool Layer:                                        
     search_papers     get_paper                     
     query_similar     index_papers                  
     add_citation      get_citations                 
     save_file         get_context                   
     get_project_status  init_project                
                                                       
    Service Layer:                                     
     SemanticScholarService                           
     CitationManager                                  
     RAGService                                       
     ContextManager                                   
    

`

---

## User Stories

### Phase 1: Core Services

**STORY-001: Semantic Scholar Integration**
- As a researcher, I want to search academic papers by keywords so that I can find relevant literature
- Acceptance: Search returns structured results with metadata and auto-generated BibTeX

**STORY-002: Citation Management**
- As a researcher, I want to manage citations in a BibTeX file so that I can reference papers correctly
- Acceptance: Add/list citations with automatic deduplication

**STORY-003: RAG Retrieval System**
- As a researcher, I want semantic search over my papers so that I can find relevant citations while writing
- Acceptance: Index papers and return top-k similar results with relevance scores

**STORY-004: File & Context Management**
- As a researcher, I want to read/write project files so that the IDE can access my research context
- Acceptance: Multi-file read, safe write with directory creation, project status reporting

**STORY-005: Project Initialization**
- As a researcher, I want to initialize a research project structure so that I can start organized
- Acceptance: Create standard directories and config files

### Phase 2: MCP Server Implementation

**STORY-006: MCP Server Core**
- As a developer, I want MCP protocol implementation so that IDEs can discover and call tools
- Acceptance: Server runs via stdio, all 10 tools registered with proper schemas

**STORY-007: Tool Implementations**
- As a developer, I want all tools fully implemented so that IDEs can execute research workflows
- Acceptance: All tools call services correctly and return structured responses

**STORY-008: IDE Integration Configs**
- As a researcher, I want IDE configuration templates so that I can set up Polyhedra quickly
- Acceptance: Working configs for Cursor, Copilot, Windsurf, VS Code

**STORY-009: Integration Testing**
- As a developer, I want end-to-end tests so that I can verify IDE integration works
- Acceptance: Test workflows execute successfully in at least 2 IDEs

### Phase 3: Polish & Launch

**STORY-010: Error Handling & Resilience**
- As a researcher, I want graceful error handling so that failures don't crash my workflow
- Acceptance: API errors, network issues, file problems all handled with clear messages

**STORY-011: Documentation & Examples**
- As a researcher, I want comprehensive docs so that I can set up and use Polyhedra effectively
- Acceptance: README, setup guide, API docs, example workflows published

**STORY-012: Package & Publish**
- As a researcher, I want easy installation so that I can start using Polyhedra in minutes
- Acceptance: Published to PyPI, installable via pip/uv, setup time < 5 minutes

---

## Technical Requirements

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-001 | Paper Search via Semantic Scholar | P0 |
| FR-002 | RAG Semantic Retrieval | P0 |
| FR-003 | BibTeX Citation Management | P0 |
| FR-004 | File & Context Operations | P0 |
| FR-005 | Project Initialization | P1 |

### Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-001 | Paper Search Performance | < 2s |
| NFR-002 | Local Operations Performance | < 100ms |
| NFR-003 | RAG Query Performance | < 500ms |
| NFR-004 | BibTeX Validity | 100% |
| NFR-005 | IDE Compatibility | 4+ IDEs |
| NFR-006 | Setup Time | < 5 minutes |

---

## Technology Stack

`yaml
language: Python 3.11+
mcp_framework: mcp (official SDK)
http_client: httpx
data_validation: Pydantic
bibtex_parser: bibtexparser
embeddings: sentence-transformers (all-MiniLM-L6-v2)
vector_store: numpy (cosine similarity)
package_manager: uv

dependencies:
  - mcp>=1.0.0
  - httpx>=0.25.0
  - pydantic>=2.0.0
  - bibtexparser>=2.0.0
  - sentence-transformers>=2.2.0
  - numpy>=1.24.0
`

---

## Dependencies & Integration Points

### External Dependencies
- **Semantic Scholar API**: Paper search and metadata (no API key required, rate limited)
- **MCP Protocol**: Standard protocol for IDE communication
- **IDE MCP Support**: Cursor, Copilot, Windsurf, VS Code

### Internal Dependencies
- Services layer must be complete before MCP server implementation
- RAG service requires sentence-transformers model download (~80MB)
- Project structure must support standard research workflows

### Integration Points
- **IDE <-> MCP Server**: stdio communication, JSON-RPC protocol
- **MCP Server <-> Services**: Internal Python imports
- **Services <-> External APIs**: HTTP REST calls
- **Services <-> Filesystem**: Read/write project files

---

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Semantic Scholar API rate limiting | High | Medium | Implement retry logic, caching, rate limit handling |
| MCP protocol changes | High | Low | Pin to stable MCP SDK version, monitor updates |
| IDE compatibility issues | Medium | Medium | Test early with all 4 target IDEs |
| Embedding model size concerns | Low | Low | Use lightweight model (all-MiniLM-L6-v2, 80MB) |
| BibTeX format edge cases | Medium | Medium | Comprehensive testing with diverse papers |
| Setup complexity | Medium | Medium | Clear docs, automated config generation |

---

## Testing Strategy

### Unit Tests
- Service layer: All services with mocked dependencies
- BibTeX parsing: Valid/invalid entries, deduplication
- RAG: Indexing, querying, similarity scoring
- File operations: Read/write, missing files, encoding

### Integration Tests
- End-to-end workflows: Search  Index  Query  Cite
- API integration: Live Semantic Scholar calls (rate-limited test suite)
- File system integration: Project init, multi-file operations

### Manual Testing
- IDE integration: Each target IDE with sample workflows
- Performance: Measure response times against targets
- Error scenarios: Network failures, invalid inputs

---

## Acceptance Criteria

### Epic-Level Acceptance

- [ ] All 12 user stories completed
- [ ] All functional requirements (FR-001 to FR-005) implemented
- [ ] All non-functional requirements met (performance, compatibility)
- [ ] Published to PyPI and installable via pip/uv
- [ ] Documentation complete (README, setup, API, examples)
- [ ] Tested and working in 4+ IDEs
- [ ] No P0/P1 bugs in backlog
- [ ] Setup time verified < 5 minutes with 3+ users

### Story Completion Criteria

Each story must meet:
- [ ] Acceptance criteria fulfilled
- [ ] Unit tests written and passing
- [ ] Integration tests passing
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] No new P0/P1 issues introduced

---

## Timeline & Milestones

### Week 1: Core Services (40% Complete)
- **Day 1-2**: Project setup, Semantic Scholar service
- **Day 3**: Citation manager service
- **Day 4**: RAG service
- **Day 5**: Context manager, review/testing

**Milestone**: All services functional with unit tests

### Week 2: MCP Server (75% Complete)
- **Day 6-7**: MCP server implementation, tool registration
- **Day 8**: Tool implementations
- **Day 9**: IDE configs and integration testing
- **Day 10**: Bug fixes and optimization

**Milestone**: Working MCP server integrated with at least 2 IDEs

### Week 3: Polish & Launch (100% Complete)
- **Day 11**: Error handling and edge cases
- **Day 12-13**: Documentation and examples
- **Day 14**: PyPI packaging and publishing
- **Day 15**: Final testing and launch

**Milestone**: Published, documented, ready for users

---

## Definition of Done

The epic is complete when:

1. **Code Complete**
   - All 10 MCP tools implemented and tested
   - All 5 services functional with test coverage
   - Error handling comprehensive

2. **Quality Gates Passed**
   - All unit tests passing (>80% coverage)
   - Integration tests passing
   - Manual IDE testing successful in 4+ IDEs
   - Performance targets met

3. **Documentation Complete**
   - README with quick start
   - Setup guide for each IDE
   - API documentation for all tools
   - Example workflows documented
   - Architecture documented

4. **Published & Accessible**
   - Published to PyPI
   - Installable via \pip install polyhedra\
   - GitHub repo public with MIT license
   - Setup verified < 5 minutes

5. **User Validation**
   - 3+ researchers successfully set up and use
   - Key workflows (search, index, cite, write) verified
   - Positive feedback on usability

---

## Success Metrics (Post-Launch)

### Usage Metrics (30 days)
- 50+ installations
- 20+ active projects initialized
- 500+ paper searches performed

### Quality Metrics
- < 5 critical bugs reported
- 100% valid BibTeX generation (no validation failures)
- Average setup time < 5 minutes (user surveys)

### Performance Metrics
- 95th percentile paper search < 2s
- 95th percentile local operations < 100ms
- 95th percentile RAG query < 500ms

---

## Notes & Assumptions

### Assumptions
- Researchers have Python 3.11+ installed
- Researchers use one of the 4 target IDEs
- Internet connectivity for Semantic Scholar API
- Local storage for embeddings cache (~100MB per 1000 papers)

### Constraints
- Must use MCP protocol (no custom protocols)
- Must delegate all LLM generation to IDE
- Must not require Semantic Scholar API key
- Must be free and open source (MIT license)

### Open Questions
- Should we support additional paper sources (arXiv API, PubMed)?
- Should we provide pre-built embeddings for popular paper sets?
- Should we support team collaboration features in future?

---

## Related Documents

- **PRD**: \docs/prd.md\ - Full product requirements
- **Architecture**: (To be created in implementation)
- **API Docs**: (To be created with implementation)
- **User Guide**: (To be created with implementation)

---

## Stakeholders

| Role | Name | Responsibility |
|------|------|----------------|
| Product Manager | Product Team | Requirements, prioritization |
| Tech Lead | Engineering | Architecture, implementation |
| Developer(s) | Engineering | Implementation, testing |
| QA | Engineering | Testing, quality gates |
| Users | Research Community | Feedback, validation |

