# Migration Guide: v2.0 → v2.1

## Overview

Polyhedra v2.1 adds AI-powered literature review generation while maintaining **100% backward compatibility** with v2.0.

## Summary of Changes

### What's New ✨
- 📄 **Literature Review Generation**: Synthesize papers into structured academic reviews
- 💰 **Cost Estimation**: Pre-generation cost estimates for budget planning
- 🎯 **Multiple Review Styles**: Brief, standard, or comprehensive depth
- 🔍 **Research Gap Identification**: Automatically identify underexplored areas

### What's Unchanged ✅
- All 10 existing v2.0 tools work exactly the same
- No changes to existing tool APIs
- No changes to project structure
- No changes to IDE configuration
- No breaking changes whatsoever

## Breaking Changes

**None!** v2.1 is fully backward compatible.

## Upgrade Steps

### Step 1: Update Polyhedra

```bash
cd polyhedra
git pull origin main
pip install -e .
```

Or if using pip:
```bash
pip install --upgrade polyhedra
```

### Step 2: Restart Your IDE

Close and reopen your IDE to reload the MCP server with the new version.

### Step 3: Verify Upgrade

In your IDE chat:
```
"List all available Polyhedra tools"
```

Should show **12 tools** (was 10 in v2.0):
- 10 existing tools from v2.0
- 2 new tools: `generate_literature_review`, `estimate_review_cost`

### Step 4: Optional - Configure LLM (for new features)

**If you want to use literature review generation**:

1. Get API key from [Anthropic](https://console.anthropic.com/) or [OpenAI](https://platform.openai.com/)
2. Set environment variable:
   ```bash
   export ANTHROPIC_API_KEY=sk-ant-your-key
   # OR
   export OPENAI_API_KEY=sk-your-key
   ```
3. Restart IDE

**If you don't configure LLM**: All v2.0 tools continue working normally.

## Feature Comparison

| Feature | v2.0 | v2.1 |
|---------|------|------|
| Paper search | ✅ | ✅ |
| Citation management | ✅ | ✅ |
| Semantic search (RAG) | ✅ | ✅ |
| File operations | ✅ | ✅ |
| Project initialization | ✅ | ✅ |
| **Literature review generation** | ❌ | ✅ |
| **Cost estimation** | ❌ | ✅ |
| **Research gap identification** | ❌ | ✅ |

## Configuration Changes

### v2.0 Configuration (Still Works)

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

### v2.1 Configuration (Optional Additions)

```json
{
  "mcpServers": {
    "polyhedra": {
      "command": "python",
      "args": ["-m", "polyhedra.server"],
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-your-key",
        "POLYHEDRA_MAX_COST": "1.00"
      }
    }
  }
}
```

**New environment variables** (all optional):
- `ANTHROPIC_API_KEY`: For Claude models (recommended)
- `OPENAI_API_KEY`: For GPT models (alternative)
- `POLYHEDRA_LLM_PROVIDER`: Choose provider (default: anthropic)
- `POLYHEDRA_LLM_MODEL`: Override default model
- `POLYHEDRA_MAX_COST`: Maximum cost per operation (default: $1.00)

## Dependencies

### v2.0 Dependencies

```toml
[dependencies]
mcp = "^1.0.0"
httpx = "^0.27.0"
sentence-transformers = "^2.2.0"
faiss-cpu = "^1.7.4"
bibtexparser = "^2.0.0"
```

### v2.1 New Dependencies

```toml
# Added for LLM integration:
anthropic = "^0.40.0"  # Optional: only if using Claude
openai = "^1.54.0"     # Optional: only if using GPT
tiktoken = "^0.8.0"    # For token counting
```

**Installation**:
```bash
pip install -e ".[llm]"  # Install with LLM support
# OR
pip install -e .         # Basic installation (v2.0 features only)
```

## API Changes

### No Breaking Changes

All v2.0 tool signatures remain identical.

### New Tools (v2.1)

#### generate_literature_review

```python
# New in v2.1
{
  "name": "generate_literature_review",
  "parameters": {
    "papers_file": "literature/papers.json",  # Optional
    "focus": "mobile deployment",              # Optional
    "structure": "thematic",                   # Optional: thematic/chronological/methodological
    "depth": "standard",                       # Optional: brief/standard/comprehensive
    "include_gaps": true,                      # Optional
    "output_path": "literature/review.md",    # Optional
    "llm_model": "claude-3-5-sonnet-20241022" # Optional
  }
}
```

#### estimate_review_cost

```python
# New in v2.1
{
  "name": "estimate_review_cost",
  "parameters": {
    "paper_count": 50,                         # Required
    "depth": "standard",                       # Optional
    "llm_model": "claude-3-5-sonnet-20241022" # Optional
  }
}
```

## Workflow Changes

### v2.0 Workflow (Still Works)

```
1. Search papers
2. Index papers
3. Query similar papers
4. Add citations
5. Manually write literature review
```

### v2.1 Enhanced Workflow (Optional)

```
1. Search papers
2. Estimate review cost  ← New
3. Generate literature review  ← New
4. Refine and customize review
5. Citations auto-added
```

## Common Migration Scenarios

### Scenario 1: Continue Using v2.0 Features Only

**No action required!** Everything works exactly as before.

```
# Your existing workflows continue unchanged:
"Search for papers on transformers"
"Add citation for this paper"
"Index my papers"
"Find papers similar to attention mechanisms"
```

### Scenario 2: Add Literature Review Generation

1. Configure LLM API key (see Step 4 above)
2. Use existing search workflows to collect papers
3. Generate reviews:

```
"Generate a literature review from my papers"
```

### Scenario 3: Cost-Conscious Usage

1. Configure `POLYHEDRA_MAX_COST` environment variable
2. Always estimate before generating:

```
"Estimate cost for reviewing 50 papers"
"If under $0.20, generate the review"
```

### Scenario 4: Team Migration

**Gradual rollout recommended**:

1. **Week 1**: Upgrade to v2.1, continue using v2.0 features
2. **Week 2**: One team member configures LLM, tests review generation
3. **Week 3**: Share results, others configure LLM if desired
4. **Week 4**: Establish team cost budgets and review workflows

## Troubleshooting

### "No new tools appearing"

1. Verify upgrade: `pip show polyhedra` (should show v2.1.x)
2. Restart IDE completely (not just reload)
3. Check MCP logs in IDE for errors

### "generate_literature_review fails"

**Error**: "LLM service not configured"

**Solution**: Configure `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`

### "Costs higher than expected"

1. Check actual token usage in response
2. Use `estimate_review_cost` before generating
3. Try brief depth or reduce paper count
4. Consider using Claude Sonnet (cheaper than GPT-4)

### "Want to rollback to v2.0"

```bash
pip install polyhedra==2.0.0
# Restart IDE
```

All v2.0 features will work. v2.1 features will be unavailable.

## FAQ

### Q: Do I need to reconfigure my IDE?

**A**: No, existing MCP configuration works unchanged.

### Q: Do I need API keys for v2.0 features?

**A**: No, all v2.0 features work WITHOUT API keys.

### Q: Will my existing projects break?

**A**: No, v2.1 is 100% backward compatible.

### Q: Can I use both Anthropic and OpenAI?

**A**: Yes, set both keys. Polyhedra uses Anthropic by default, or set `POLYHEDRA_LLM_PROVIDER=openai`.

### Q: How much do literature reviews cost?

**A**: Typical costs with Claude Sonnet:
- Brief (50 papers): $0.08-0.12
- Standard (50 papers): $0.12-0.20
- Comprehensive (50 papers): $0.20-0.35

### Q: Can I opt out of v2.1 features?

**A**: Yes, simply don't configure LLM API keys. v2.0 features continue working.

### Q: How do I track my LLM spending?

**A**: Each review generation returns actual cost in the response. Also check your provider dashboard (Anthropic/OpenAI).

### Q: What if I hit rate limits?

**A**: Polyhedra automatically retries with backoff. For persistent issues:
- Wait 60 seconds and retry
- Check your API dashboard for limits
- Consider upgrading your account tier

## Getting Help

- **Documentation**: [docs/API.md](API.md), [docs/SETUP.md](SETUP.md), [docs/USER_GUIDE.md](USER_GUIDE.md)
- **GitHub Issues**: https://github.com/polyhedra/polyhedra/issues
- **Migration Issues**: Tag with `migration-v2.1`

## Changelog

### v2.1.0 (2024-12-07)

**Added**:
- Literature review generation tool (`generate_literature_review`)
- Cost estimation tool (`estimate_review_cost`)
- LLM service foundation (Anthropic Claude, OpenAI GPT)
- Support for three review depths (brief/standard/comprehensive)
- Support for three review structures (thematic/chronological/methodological)
- Research gap identification
- Cost management with configurable limits
- Comprehensive documentation updates

**Changed**:
- Tool count increased from 10 to 12
- Added optional LLM dependencies
- Enhanced error messages for new features

**Fixed**:
- No bug fixes (new feature release)

**Deprecated**:
- Nothing deprecated

**Removed**:
- Nothing removed

**Security**:
- API keys stored in environment variables (never in code)
- Cost limits prevent accidental overspending

---

**Welcome to Polyhedra v2.1!** 🎉
