# Manual IDE Integration Testing Checklist

This checklist guides manual testing of Polyhedra in real IDE environments.

## Test Environment Setup

**IDEs to Test** (minimum 2 required):
- [ ] Cursor
- [ ] VS Code with GitHub Copilot
- [ ] Windsurf
- [ ] VS Code with MCP extension

**Prerequisites:**
- [ ] Polyhedra installed (`pip install polyhedra` or `uv pip install polyhedra`)
- [ ] IDE configured per `docs/SETUP.md`
- [ ] IDE restarted after configuration

## Test Suite

### Test 1: Tool Discovery

**Objective:** Verify all tools are available in the IDE

**Steps:**
1. Open IDE chat/copilot
2. Ask: "What Polyhedra tools are available?"
3. Verify response lists all 10 tools

**Expected Result:**
- [ ] search_papers
- [ ] get_paper
- [ ] query_similar_papers
- [ ] index_papers
- [ ] add_citation
- [ ] get_citations
- [ ] save_file
- [ ] get_context
- [ ] get_project_status
- [ ] init_project

**Status:** ☐ Pass ☐ Fail

---

### Test 2: Project Initialization

**Objective:** Initialize a new research project

**Steps:**
1. Create new empty directory
2. Open directory in IDE
3. In IDE chat: "Initialize a new research project named 'test-research'"
4. Verify directory structure created

**Expected Result:**
```
literature/
ideas/
method/
paper/
references.bib
.poly/
  config.yaml
  embeddings/
```

**Status:** ☐ Pass ☐ Fail

---

### Test 3: Paper Search

**Objective:** Search for academic papers

**Steps:**
1. In IDE chat: "Search for 5 recent papers on 'transformer models' from 2023-2024"
2. Wait for results
3. Verify papers returned with metadata

**Expected Result:**
- [ ] Returns 5 or fewer papers
- [ ] Papers have titles, authors, years
- [ ] Years are within 2023-2024
- [ ] Response time < 3 seconds

**Status:** ☐ Pass ☐ Fail

---

### Test 4: Citation Management

**Objective:** Add and retrieve citations

**Steps:**
1. In IDE chat: "Add this BibTeX entry to my bibliography:"
```bibtex
@article{vaswani2017attention,
  title={Attention is all you need},
  author={Vaswani, Ashish and Shazeer, Noam},
  journal={Advances in neural information processing systems},
  year={2017}
}
```
2. In IDE chat: "Show me all my citations"
3. Verify citation appears

**Expected Result:**
- [ ] Citation added successfully
- [ ] Citation appears in list
- [ ] references.bib file updated

**Status:** ☐ Pass ☐ Fail

---

### Test 5: File Operations

**Objective:** Write and read project files

**Steps:**
1. In IDE chat: "Create a file ideas/hypothesis.md with content: '# Research Hypothesis\n\nWe hypothesize that...'"
2. Verify file created
3. In IDE chat: "Read the contents of ideas/hypothesis.md"
4. Verify content matches

**Expected Result:**
- [ ] File created in correct location
- [ ] Content is correct
- [ ] Read operation returns same content

**Status:** ☐ Pass ☐ Fail

---

### Test 6: Project Status

**Objective:** Get comprehensive project status

**Steps:**
1. In IDE chat: "Show me my project status"
2. Verify status information returned

**Expected Result:**
- [ ] Shows papers_count
- [ ] Shows citations_count
- [ ] Shows rag_indexed status
- [ ] Lists standard_files existence
- [ ] Response time < 100ms

**Status:** ☐ Pass ☐ Fail

---

### Test 7: Complete Workflow

**Objective:** Execute a complete research workflow

**Steps:**
1. "Initialize a new project called 'ml-survey'"
2. "Search for 3 papers on 'deep learning'"
3. "Save these papers to literature/papers.json"
4. "Add citations from these papers to my bibliography"
5. "Get my project status"
6. "Create a file literature/review.md with notes about these papers"

**Expected Result:**
- [ ] All steps complete without errors
- [ ] Files created correctly
- [ ] Citations added successfully
- [ ] Status shows correct counts

**Status:** ☐ Pass ☐ Fail

---

### Test 8: Error Handling

**Objective:** Verify graceful error handling

**Steps:**
1. In IDE chat: "Read the file nonexistent.md"
2. Verify error message is clear
3. In IDE chat: "Query similar papers about 'test'" (before indexing)
4. Verify error message is helpful

**Expected Result:**
- [ ] Missing file error clearly explains issue
- [ ] Not indexed error suggests running index_papers
- [ ] No crashes or unclear errors

**Status:** ☐ Pass ☐ Fail

---

### Test 9: Semantic Search (RAG)

**Objective:** Index and query papers semantically

**Steps:**
1. Create literature/papers.json with 3+ papers
2. In IDE chat: "Index the papers in literature/papers.json"
3. Wait for indexing (may take 30-60s first time)
4. In IDE chat: "Find papers similar to 'attention mechanisms'"
5. Verify results with similarity scores

**Expected Result:**
- [ ] Indexing completes successfully
- [ ] Returns similar papers
- [ ] Each result has similarity score
- [ ] Query time < 1 second (after initial model download)

**Status:** ☐ Pass ☐ Fail

---

### Test 10: Performance Validation

**Objective:** Verify performance targets

**Measurements:**
- [ ] Paper search: < 2 seconds
- [ ] Local file ops: < 100ms
- [ ] RAG query: < 500ms (after indexing)
- [ ] Project status: < 100ms

**Status:** ☐ Pass ☐ Fail

---

## Test Results Summary

**IDE:** _____________
**Date:** _____________
**Tester:** _____________

**Results:**
- Tests Passed: _____ / 10
- Tests Failed: _____ / 10
- Critical Issues: _____________

**Notes:**
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

## Critical Issues Found

| Test | Issue | Severity | Notes |
|------|-------|----------|-------|
|      |       |          |       |

## Performance Benchmarks

| Operation | Target | Actual | Status |
|-----------|--------|--------|--------|
| Paper search | < 2s | ___s | ☐ Pass ☐ Fail |
| File write | < 100ms | ___ms | ☐ Pass ☐ Fail |
| File read | < 100ms | ___ms | ☐ Pass ☐ Fail |
| Project status | < 100ms | ___ms | ☐ Pass ☐ Fail |
| RAG query | < 500ms | ___ms | ☐ Pass ☐ Fail |

## Sign-off

**Tested By:** _____________
**Date:** _____________
**Approved:** ☐ Yes ☐ No (explain below)

**Comments:**
_________________________________________________________________
_________________________________________________________________
