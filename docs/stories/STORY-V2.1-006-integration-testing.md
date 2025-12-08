# STORY-V2.1-006: Comprehensive Integration Testing

## Story Metadata

| Field | Value |
|-------|-------|
| **Story ID** | STORY-V2.1-006 |
| **Epic** | EPIC-V2.1-001: Core LLM Integration & Literature Review |
| **Title** | Comprehensive Integration Testing |
| **Priority** | P0 (Critical) |
| **Points** | 8 |
| **Status** | Not Started |
| **Agent Model Used** | Claude Sonnet 4.5 |
| **Estimated Effort** | 3-4 days |
| **Actual Effort** | TBD |
| **Dependencies** | STORY-V2.1-001, V2.1-002, V2.1-003, V2.1-004, V2.1-005 |

---

## User Story

**As a** Polyhedra user  
**I want** confidence that all features (v2.0 and v2.1) work correctly together  
**So that** I can reliably use the tool for my research without unexpected failures

---

## Acceptance Criteria

### AC-001: Regression Testing (v2.0 Features)
- [ ] All 55 existing v2.0 unit tests pass without modification
- [ ] All 10 v2.0 integration tests pass
- [ ] All 10 v2.0 tools work correctly (search, citations, RAG, files, project)
- [ ] No performance degradation (same latency benchmarks)
- [ ] No breaking changes to existing APIs

### AC-002: v2.1 Unit Test Coverage
- [ ] LLM Service tests: >90% coverage
- [ ] Literature Review Service tests: >85% coverage
- [ ] Server integration tests for new tools
- [ ] All tests pass consistently

### AC-003: End-to-End Integration Tests
- [ ] Test complete workflow: search → estimate → generate → citations
- [ ] Test with different paper counts (5, 25, 50, 75, 100)
- [ ] Test all depth levels (brief, standard, comprehensive)
- [ ] Test all structures (thematic, chronological, methodological)
- [ ] Test cost estimation accuracy (within ±20%)
- [ ] Test error handling for missing API keys
- [ ] Test error handling for API failures

### AC-004: Provider Integration Tests
- [ ] Anthropic Claude integration works end-to-end
- [ ] OpenAI GPT integration works end-to-end
- [ ] Provider switching works correctly
- [ ] Model override parameter works
- [ ] Token counting is accurate
- [ ] Cost calculation is accurate

### AC-005: Performance Benchmarks
- [ ] Brief review (50 papers): <2 minutes
- [ ] Standard review (50 papers): <3 minutes
- [ ] Comprehensive review (50 papers): <5 minutes
- [ ] Cost per review matches estimates (±20%)
- [ ] No memory leaks in long-running processes

### AC-006: IDE Integration Tests
- [ ] Manual testing in Cursor (all 12 tools work)
- [ ] Manual testing in VS Code Copilot (all 12 tools work)
- [ ] Manual testing in Windsurf (all 12 tools work)
- [ ] Tool discovery works in all IDEs
- [ ] Error messages display correctly
- [ ] Cost warnings display correctly

### AC-007: Edge Case Testing
- [ ] Empty papers file handled gracefully
- [ ] Single paper review works
- [ ] Very large collections (100+ papers) handled
- [ ] Papers without abstracts handled
- [ ] API rate limits handled with retry
- [ ] Network errors handled gracefully
- [ ] Invalid API keys show clear errors

---

## Integration Verification

- **IV1**: All v2.0 features continue working without LLM configuration
- **IV2**: v2.1 features fail gracefully without API keys
- **IV3**: Mixed workflows (v2.0 + v2.1 tools) work seamlessly
- **IV4**: Cost estimation matches actual costs within ±20%
- **IV5**: Performance meets benchmarks under realistic conditions

---

## Definition of Done

- [ ] All acceptance criteria met
- [ ] 100% v2.0 regression tests passing
- [ ] >85% coverage on new v2.1 code
- [ ] All integration tests passing
- [ ] Manual IDE testing complete for all supported IDEs
- [ ] Performance benchmarks documented
- [ ] Known issues documented with workarounds
- [ ] Ready for production release

---

## Dev Agent Record

### Tasks
- [ ] Create story file
- [ ] Run full v2.0 regression test suite
- [ ] Create v2.1 integration test suite
- [ ] Test end-to-end workflows
- [ ] Test Anthropic integration
- [ ] Test OpenAI integration
- [ ] Run performance benchmarks
- [ ] Manual testing in Cursor
- [ ] Manual testing in VS Code Copilot
- [ ] Manual testing in Windsurf
- [ ] Test edge cases and error scenarios
- [ ] Document test results
- [ ] Create QA gate document

### Debug Log
<!-- Record issues and resolutions -->

### Completion Notes
<!-- Summary of delivery -->

### File List
**Files to Create:**
- `tests/test_integration_v2_1.py` - NEW - v2.1 integration tests
- `tests/test_end_to_end_review.py` - NEW - End-to-end review generation tests
- `tests/test_provider_integration.py` - NEW - LLM provider integration tests
- `docs/qa/gates/EPIC-V2.1-001.STORY-V2.1-006-integration-testing.yml` - NEW - QA gate

**Files to Update:**
- `tests/conftest.py` - Add v2.1 fixtures if needed

### Change Log
| Change | Description |
|--------|-------------|
| TBD | TBD |

---

## Technical Notes

### Test Structure

#### 1. Regression Tests (v2.0)
Run existing test suite to ensure no breaking changes:
```bash
pytest tests/test_services/ -v
pytest tests/test_server.py -v
pytest tests/test_integration_workflows.py -v
```

Expected:
- All 55 unit tests pass
- All 10 integration tests pass
- No new warnings or errors

#### 2. Unit Tests (v2.1 Services)
Already created in previous stories:
- `tests/test_services/test_llm_service.py` (30 tests, 91% coverage)
- `tests/test_services/test_literature_review_service.py` (28 tests, 99% coverage)
- `tests/test_server.py` (updated for 12 tools)

#### 3. Integration Tests (v2.1 Features)

**Test File**: `tests/test_integration_v2_1.py`

```python
"""Integration tests for v2.1 literature review features."""

import pytest
import asyncio
from pathlib import Path

@pytest.mark.integration
@pytest.mark.asyncio
async def test_complete_review_workflow_anthropic(monkeypatch, temp_dir):
    """Test complete workflow with Anthropic."""
    # Setup
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.chdir(temp_dir)
    
    # 1. Search papers
    papers = await search_papers("transformer efficiency", limit=10)
    assert len(papers) >= 5
    
    # 2. Save papers
    papers_file = Path("literature/papers.json")
    papers_file.parent.mkdir(parents=True, exist_ok=True)
    papers_file.write_text(json.dumps(papers))
    
    # 3. Estimate cost
    estimate = await estimate_review_cost(paper_count=len(papers), depth="brief")
    assert estimate["estimated_usd"] > 0
    assert estimate["estimated_usd"] < 0.50  # Sanity check
    
    # 4. Generate review
    result = await generate_literature_review(
        papers_file=str(papers_file),
        depth="brief",
        structure="thematic"
    )
    
    # Verify
    assert result["success"]
    assert "review" in result
    assert result["metadata"]["paper_count"] == len(papers)
    assert result["cost"]["total_usd"] > 0
    
    # Verify actual cost vs estimate within 30%
    actual = result["cost"]["total_usd"]
    estimated = estimate["estimated_usd"]
    assert abs(actual - estimated) / estimated < 0.30

@pytest.mark.integration
def test_depth_levels_comparison():
    """Compare output sizes for different depth levels."""
    papers = load_sample_papers(50)
    
    brief = generate_review(papers, depth="brief")
    standard = generate_review(papers, depth="standard")
    comprehensive = generate_review(papers, depth="comprehensive")
    
    # Verify word count progression
    assert brief["metadata"]["word_count"] < standard["metadata"]["word_count"]
    assert standard["metadata"]["word_count"] < comprehensive["metadata"]["word_count"]
    
    # Verify approximate targets
    assert 500 < brief["metadata"]["word_count"] < 800
    assert 1500 < standard["metadata"]["word_count"] < 2500
    assert 2000 < comprehensive["metadata"]["word_count"] < 3000

@pytest.mark.integration
def test_structure_types_all_work():
    """Test all three structure types generate valid output."""
    papers = load_sample_papers(30)
    
    for structure in ["thematic", "chronological", "methodological"]:
        result = generate_review(papers, structure=structure, depth="brief")
        
        assert result["success"]
        assert len(result["metadata"]["sections"]) >= 3
        assert result["metadata"]["citations_found"] > 0

@pytest.mark.integration
def test_large_collection_handling():
    """Test system handles 100+ papers."""
    papers = load_sample_papers(100)
    
    # Should succeed or provide clear error
    result = generate_review(papers, depth="brief")
    
    if result.get("error"):
        # Error should be clear and actionable
        assert "too many papers" in result["error"].lower() or \
               "token limit" in result["error"].lower()
    else:
        # Or should succeed with all papers
        assert result["success"]
        assert result["metadata"]["paper_count"] == 100
```

#### 4. Provider Integration Tests

**Test File**: `tests/test_provider_integration.py`

```python
"""Test LLM provider integrations."""

@pytest.mark.integration
@pytest.mark.anthropic
@pytest.mark.asyncio
async def test_anthropic_end_to_end(monkeypatch):
    """Test Anthropic integration end-to-end."""
    # Requires real API key in environment
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        pytest.skip("ANTHROPIC_API_KEY not set")
    
    service = LLMService(provider="anthropic", api_key=api_key)
    
    # Test token counting
    tokens = service.estimate_tokens("This is a test.")
    assert tokens > 0
    assert tokens < 10
    
    # Test cost calculation
    cost = service.calculate_cost(1000, 500, "claude-3-5-sonnet-20241022")
    assert 0.01 < cost < 0.10
    
    # Test completion
    response, input_tokens, output_tokens = await service.complete(
        "Write a one-sentence summary of transformer models.",
        model="claude-3-5-sonnet-20241022"
    )
    
    assert len(response) > 10
    assert input_tokens > 0
    assert output_tokens > 0
    
    await service.close()

@pytest.mark.integration
@pytest.mark.openai
@pytest.mark.asyncio
async def test_openai_end_to_end(monkeypatch):
    """Test OpenAI integration end-to-end."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set")
    
    service = LLMService(provider="openai", api_key=api_key)
    
    # Same tests as Anthropic
    tokens = service.estimate_tokens("This is a test.")
    assert tokens > 0
    
    cost = service.calculate_cost(1000, 500, "gpt-4o")
    assert 0.01 < cost < 0.10
    
    response, input_tokens, output_tokens = await service.complete(
        "Write a one-sentence summary of transformer models.",
        model="gpt-4o"
    )
    
    assert len(response) > 10
    assert input_tokens > 0
    assert output_tokens > 0
    
    await service.close()

@pytest.mark.integration
def test_provider_switching():
    """Test switching between providers."""
    # Start with Anthropic
    service1 = LLMService(provider="anthropic", api_key="test-key-1")
    assert service1.provider == "anthropic"
    
    # Switch to OpenAI
    service2 = LLMService(provider="openai", api_key="test-key-2")
    assert service2.provider == "openai"
    
    # Both should calculate costs correctly
    cost1 = service1.calculate_cost(1000, 500, "claude-3-5-sonnet-20241022")
    cost2 = service2.calculate_cost(1000, 500, "gpt-4o")
    
    # GPT-4o should be slightly cheaper than Claude Sonnet
    assert cost2 < cost1 * 1.5  # Within reasonable range
```

#### 5. Performance Benchmarks

**Test File**: `tests/test_performance_v2_1.py`

```python
"""Performance benchmarks for v2.1 features."""

import time

@pytest.mark.performance
@pytest.mark.asyncio
async def test_brief_review_performance():
    """Brief review of 50 papers completes in <2 minutes."""
    papers = load_sample_papers(50)
    
    start = time.time()
    result = await generate_review(papers, depth="brief")
    elapsed = time.time() - start
    
    assert result["success"]
    assert elapsed < 120  # 2 minutes

@pytest.mark.performance
@pytest.mark.asyncio
async def test_standard_review_performance():
    """Standard review of 50 papers completes in <3 minutes."""
    papers = load_sample_papers(50)
    
    start = time.time()
    result = await generate_review(papers, depth="standard")
    elapsed = time.time() - start
    
    assert result["success"]
    assert elapsed < 180  # 3 minutes

@pytest.mark.performance
def test_cost_estimation_accuracy():
    """Cost estimates are within ±20% of actual."""
    papers = load_sample_papers(50)
    
    estimate = estimate_review_cost(paper_count=50, depth="standard")
    result = generate_review(papers, depth="standard")
    
    estimated = estimate["estimated_usd"]
    actual = result["cost"]["total_usd"]
    
    error = abs(actual - estimated) / estimated
    assert error < 0.20  # Within 20%
```

#### 6. Edge Case Tests

**Test File**: `tests/test_edge_cases_v2_1.py`

```python
"""Edge case testing for v2.1 features."""

def test_empty_papers_file():
    """Empty papers file returns clear error."""
    result = generate_literature_review(papers_file="literature/papers.json")
    
    assert "error" in result
    assert "empty" in result["error"].lower()

def test_single_paper_review():
    """Single paper generates minimal review."""
    papers = load_sample_papers(1)
    result = generate_review(papers, depth="brief")
    
    assert result["success"]
    assert result["metadata"]["paper_count"] == 1
    assert result["metadata"]["word_count"] > 100

def test_papers_without_abstracts():
    """Papers without abstracts handled gracefully."""
    papers = [{"title": "Paper 1", "authors": [{"name": "Author"}], "year": 2024}]
    result = generate_review(papers, depth="brief")
    
    # Should succeed or provide clear warning
    assert result["success"] or "abstract" in result.get("warning", "").lower()

def test_missing_api_key_error():
    """Missing API key returns clear error."""
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    
    result = generate_literature_review()
    
    assert "error" in result
    assert "api key" in result["error"].lower() or \
           "not configured" in result["error"].lower()
```

### Manual Testing Checklist

#### Cursor Testing
- [ ] Install/update Polyhedra in Cursor
- [ ] Verify 12 tools show in tool list
- [ ] Test: "Search for papers on transformers"
- [ ] Test: "Estimate cost for reviewing 50 papers"
- [ ] Test: "Generate a brief literature review"
- [ ] Verify review saved to file
- [ ] Verify citations added to references.bib
- [ ] Test error: Generate without API key
- [ ] Test error: Generate with empty papers file

#### VS Code Copilot Testing
- [ ] Same tests as Cursor
- [ ] Verify tool discovery works
- [ ] Verify error messages display correctly

#### Windsurf Testing
- [ ] Same tests as Cursor
- [ ] Verify MCP integration works

### QA Gate Format

**File**: `docs/qa/gates/EPIC-V2.1-001.STORY-V2.1-006-integration-testing.yml`

```yaml
schema: 1
story: 'EPIC-V2.1-001.STORY-V2.1-006'
title: 'Comprehensive Integration Testing'
date: '2024-12-07'
reviewer: 'TBD'
decision: 'PENDING'
score: TBD

acceptance_criteria:
  - id: AC-001
    title: 'Regression Testing (v2.0 Features)'
    status: TBD
    evidence: 'TBD'
  - id: AC-002
    title: 'v2.1 Unit Test Coverage'
    status: TBD
    evidence: 'TBD'
  - id: AC-003
    title: 'End-to-End Integration Tests'
    status: TBD
    evidence: 'TBD'
  - id: AC-004
    title: 'Provider Integration Tests'
    status: TBD
    evidence: 'TBD'
  - id: AC-005
    title: 'Performance Benchmarks'
    status: TBD
    evidence: 'TBD'
  - id: AC-006
    title: 'IDE Integration Tests'
    status: TBD
    evidence: 'TBD'
  - id: AC-007
    title: 'Edge Case Testing'
    status: TBD
    evidence: 'TBD'

test_results:
  total_tests: TBD
  unit_tests: TBD
  integration_tests: TBD
  performance_tests: TBD
  status: PENDING

quality_metrics:
  test_coverage: TBD
  code_quality: TBD
  documentation: TBD
  performance: TBD

critical_findings: []
minor_findings: []
recommendations: []

reviewer_notes: |
  TBD

sign_off:
  reviewer: TBD
  date: TBD
```

### Test Execution Plan

**Week 1: Automated Tests**
- Day 1: Run v2.0 regression suite, document results
- Day 2: Run v2.1 unit tests, verify coverage
- Day 3: Create and run integration tests
- Day 4: Run provider integration tests (requires API keys)
- Day 5: Run performance benchmarks

**Week 2: Manual & Edge Cases**
- Day 1: Manual testing in Cursor
- Day 2: Manual testing in VS Code Copilot
- Day 3: Manual testing in Windsurf
- Day 4: Edge case testing, error scenarios
- Day 5: Document results, create QA gate

### Success Criteria Summary

✅ **Pass**: All criteria met
- 100% v2.0 tests pass
- >85% v2.1 coverage
- All integration tests pass
- Performance benchmarks met
- Manual testing complete

⚠️ **Conditional Pass**: Minor issues with workarounds
- 95%+ v2.0 tests pass (with documented exceptions)
- 80%+ v2.1 coverage
- Most integration tests pass
- Performance within 10% of benchmarks
- Known issues documented

❌ **Fail**: Critical issues
- <90% v2.0 tests pass
- <75% v2.1 coverage
- Integration tests failing
- Performance >20% slower than benchmarks
- Undocumented critical bugs
