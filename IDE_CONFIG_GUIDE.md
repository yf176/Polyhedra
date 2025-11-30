# Polyhedra IDE Configuration Guide

## What is MCP?

**MCP (Model Context Protocol)** is a protocol that allows AI assistants to call external tools.

```
You → VS Code Copilot → Polyhedra MCP Server → Semantic Scholar API
      (chat)           (call tools)          (search papers)
```

## Configuration File Location

The configuration file is in your project's `.vscode/settings.json`:

```json
{
  "mcp.servers": {
    "polyhedra": {
      "command": "py",                    // ← Python launcher
      "args": ["-3.12", "-m", "polyhedra.server"],  // ← Run Polyhedra
      "env": {}
    }
  }
}
```

### What does this configuration do?

1. **Tells VS Code**: "There's an MCP server called polyhedra"
2. **Launch command**: Run `py -3.12 -m polyhedra.server`
3. **VS Code auto-starts**: When you open Copilot, it starts Polyhedra in the background

## How to Verify Configuration?

### Method 1: Reload VS Code Window

1. Press `Ctrl + Shift + P`
2. Type "Reload Window"
3. Press Enter

### Method 2: Check MCP Connection (if supported)

Some IDEs show MCP server status in settings.

## Usage Examples

After successful configuration, you can say in Copilot Chat:

### 📝 Example Conversation:

**You**: "Search for papers about transformers"

**Copilot** (internally):
1. Recognizes you want to search papers
2. Calls Polyhedra's `search_papers` tool
3. Passes parameters: query="transformer"
4. Gets results and shows them to you

**What you see**:
```
Found 10 papers:

1. Attention is All You Need
   Authors: Vaswani et al.
   Year: 2017
   Citations: 95,432
   ...
```

### 📚 More Examples:

```
"Initialize a new research project called ai-research"
→ Calls init_project tool

"Add this paper to my bibliography"
→ Calls add_citation tool

"Find similar papers about attention mechanisms"
→ Calls query_similar_papers tool
```

## Other IDE Configurations

### Cursor / Windsurf

Configuration file: `~/.cursor/mcp.json` or `~/.windsurf/mcp.json`

```json
{
  "mcpServers": {
    "polyhedra": {
      "command": "py",
      "args": ["-3.12", "-m", "polyhedra.server"]
    }
  }
}
```

## Common Issues

### Q: I configured it but it's not working?

**A**: Check:
1. Did you reload the VS Code window?
2. Is polyhedra installed in Python 3.12? (`py -3.12 -m pip show polyhedra`)
3. Does your GitHub Copilot version support MCP?

### Q: How to test if the MCP server can run?

**A**: Run in terminal:
```powershell
py -3.12 -m polyhedra.server
```
If there's no error, the server can start.

### Q: Does GitHub Copilot support MCP?

**A**: GitHub Copilot's MCP support may still be experimental.
**Alternative**: Use Cursor or Windsurf (native MCP support)

## Manual Testing (without IDE)

If MCP integration doesn't work, you can run scripts directly:

```powershell
py -3.12 demo_search.py
```

This directly calls Polyhedra's functionality to search papers.

## Summary

```
Configuration file (.vscode/settings.json)
    ↓
VS Code reads config on startup
    ↓
Starts Polyhedra MCP Server in background (py -3.12 -m polyhedra.server)
    ↓
Copilot can call Polyhedra's 10 tools
    ↓
You use these tools through natural language conversation
```

**Key Point**: The configuration file just tells the IDE how to start Polyhedra. The actual functionality is accessed through conversation.
