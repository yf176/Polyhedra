# STORY-V2.1-004: Cost Estimation & User Confirmation

## Story Metadata

| Field | Value |
|-------|-------|
| **Story ID** | STORY-V2.1-004 |
| **Epic** | EPIC-V2.1-001: Core LLM Integration & Literature Review |
| **Title** | Cost Estimation & User Confirmation |
| **Priority** | P1 (Important) |
| **Points** | 3 |
| **Status** | In Progress |
| **Agent Model Used** | Claude Sonnet 4.5 |
| **Estimated Effort** | 1-2 days |
| **Actual Effort** | TBD |
| **Dependencies** | STORY-V2.1-003 (MCP Tool Integration) |

---

## User Story

**As a** researcher using Polyhedra  
**I want** to see cost estimates before generating expensive reviews  
**So that** I can control LLM spending and avoid surprise charges

---

## Context

**What exists currently**:
- ✅ LLMService has `calculate_cost()` method
- ✅ LiteratureReviewService has `estimate_cost()` method
- ✅ `generate_review()` logs estimated cost before generation
- ✅ Cost included in return value after generation

**What's missing**:
- ❌ User confirmation step before expensive operations (>$0.10 threshold)
- ❌ MCP tool doesn't expose cost estimation before execution
- ❌ No way to get cost estimate without running the full generation
- ❌ No cost threshold configuration

**Why this matters**:
- Users may accidentally generate expensive comprehensive reviews of 100+ papers
- No way to estimate cost from IDE before calling the tool
- Current implementation generates first, bills after

---

## Acceptance Criteria

### AC-001: New Tool for Cost Estimation
- [ ] Add new MCP tool `estimate_review_cost`
- [ ] Tool accepts parameters:
  - `paper_count`: Number of papers
  - `depth`: Review depth (brief/standard/comprehensive)
  - `llm_model`: Optional model override
- [ ] Tool returns cost estimate without generating review

### AC-002: Cost Warning in Review Generation
- [ ] `generate_literature_review` tool checks estimated cost
- [ ] If cost > $0.10, return warning message with estimate
- [ ] User must pass `confirm_cost=true` parameter to proceed
- [ ] Log cost estimates for all generations

### AC-003: Cost Configuration
- [ ] Add `POLYHEDRA_MAX_COST` environment variable (default: $1.00)
- [ ] Reject operations exceeding max cost with clear error
- [ ] Allow override with `force=true` parameter (with warning)

### AC-004: Documentation
- [ ] Update USER_GUIDE.md with cost estimation workflow
- [ ] Document cost thresholds and configuration
- [ ] Add examples of checking cost before generation
- [ ] Include typical costs for different scenarios

---

## Integration Verification

- **IV1**: Cost estimation doesn't slow down normal operations
- **IV2**: Existing users without cost limits continue working unchanged
- **IV3**: Cost checks only apply to LLM operations, not data tools
- **IV4**: All v2.0 tests still pass

---

## Definition of Done

- [ ] Code reviewed and approved
- [ ] Unit tests for cost estimation tool
- [ ] Unit tests for cost confirmation logic
- [ ] Integration tests for threshold enforcement
- [ ] Documentation updated
- [ ] Manual testing in IDE
- [ ] Ready for merge to main branch

---

## Dev Agent Record

### Tasks
- [x] Create story file
- [ ] Add `estimate_review_cost` tool to server
- [ ] Implement cost confirmation logic
- [ ] Add `confirm_cost` parameter to `generate_literature_review`
- [ ] Add cost threshold configuration
- [ ] Create unit tests for new tool
- [ ] Create unit tests for confirmation logic
- [ ] Update documentation
- [ ] Manual IDE testing

### Debug Log
<!-- Record issues and resolutions -->

### Completion Notes
<!-- Summary of delivery -->

### File List
**Files to Modify:**
- `src/polyhedra/server.py` - Add new tool, cost confirmation logic
- `tests/test_server.py` - Add tests for cost estimation and confirmation
- `docs/USER_GUIDE.md` - Document cost management
- `docs/API.md` - Document new tool

### Change Log
| Change | Description |
|--------|-------------|
| TBD | TBD |

---

## Technical Notes

### Design Options

**Option A: Pre-Check Tool (Recommended)**
```python
# User workflow:
# 1. Estimate cost first
result = await tools.estimate_review_cost(paper_count=50, depth="standard")
# → {"estimated_cost": 0.15}

# 2. If acceptable, generate
review = await tools.generate_literature_review(..., confirm_cost=True)
```

**Option B: Automatic Warning**
```python
# First call without confirmation
review = await tools.generate_literature_review(papers=50_papers, depth="standard")
# → {"warning": "Estimated cost: $0.15. Add confirm_cost=true to proceed."}

# Second call with confirmation
review = await tools.generate_literature_review(..., confirm_cost=True)
# → {Generated review}
```

**Option C: Threshold Only**
```python
# Only blocks if > threshold
review = await tools.generate_literature_review(papers=150_papers, depth="comprehensive")
# → {"error": "Estimated cost $0.75 exceeds limit $1.00. Set force=true to override."}
```

**Recommended**: Implement both Option A (new tool) AND Option B (confirmation parameter). This gives users flexibility:
- Check cost explicitly before generation (Option A)
- Get automatic warning on first attempt (Option B)
- Respect max cost threshold (Option C safety net)

### Implementation Checklist

1. **Add `estimate_review_cost` tool** (~30 min)
   - Register in `list_tools()`
   - Implement handler in `call_tool()`
   - Call `LiteratureReviewService.estimate_cost()`
   - Return formatted estimate

2. **Add cost confirmation to `generate_literature_review`** (~45 min)
   - Add `confirm_cost` boolean parameter (default: False)
   - Estimate cost before generation
   - If cost > $0.10 and not confirmed, return warning instead
   - Log all cost estimates

3. **Add cost threshold configuration** (~30 min)
   - Read `POLYHEDRA_MAX_COST` from environment
   - Add `force` boolean parameter for override
   - Check threshold before confirmation
   - Clear error messages for violations

4. **Tests** (~1 hour)
   - Test `estimate_review_cost` tool
   - Test confirmation requirement
   - Test threshold enforcement
   - Test force override
   - Test typical user workflows

5. **Documentation** (~45 min)
   - Update USER_GUIDE.md with cost management section
   - Update API.md with new tool
   - Add cost examples to README
   - Document environment variables

### Example Tool Schema

```python
{
    "name": "estimate_review_cost",
    "description": "Estimate cost before generating literature review",
    "inputSchema": {
        "type": "object",
        "properties": {
            "paper_count": {
                "type": "number",
                "description": "Number of papers to review"
            },
            "depth": {
                "type": "string",
                "enum": ["brief", "standard", "comprehensive"],
                "description": "Review depth level",
                "default": "standard"
            },
            "llm_model": {
                "type": "string",
                "description": "Optional LLM model override"
            }
        },
        "required": ["paper_count"]
    }
}
```

### Example Updated Schema for generate_literature_review

```python
# Add new parameters:
"confirm_cost": {
    "type": "boolean",
    "description": "Confirm proceeding with estimated cost",
    "default": False
},
"force": {
    "type": "boolean",
    "description": "Force execution even if cost exceeds configured limit",
    "default": False
}
```
