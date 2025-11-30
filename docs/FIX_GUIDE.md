# Polyhedra Fix Guide

## Problem Diagnosis

Your project encountered MCP server configuration issues. Main reasons:

1. **Incorrect command configuration**: Used `uvx --from polyhedra` attempting to install from PyPI, but the package is not yet published
2. **VS Code MCP interception**: MCP server is intercepting terminal output preventing normal command execution

## Fix Steps

### 1. Reload VS Code

**Important**: First reload VS Code to stop the current MCP server.

- Press `Ctrl+Shift+P` or `Cmd+Shift+P`
- Type "Reload Window" and execute
- Or simply close and reopen VS Code

### 2. Update IDE Configuration (Development Mode)

Update configuration based on your IDE:

#### VS Code (Already Updated)
`.vscode/settings.json` has been updated to use local Python environment.

#### Cursor
Update `~/.cursor/mcp.json` or project's `ide-integration/cursor/mcp.json`:

```json
{
  "mcpServers": {
    "polyhedra": {
      "command": "C:\\Users\\OMEN\\Desktop\\poly\\.venv\\Scripts\\python.exe",
      "args": ["-m", "polyhedra.server"],
      "env": {}
    }
  }
}
```

#### Windsurf
Update `~/.windsurf/mcp.json` or project's `ide-integration/windsurf/mcp.json`:

```json
{
  "mcpServers": {
    "polyhedra": {
      "command": "C:\\Users\\OMEN\\Desktop\\poly\\.venv\\Scripts\\python.exe",
      "args": ["-m", "polyhedra.server"],
      "env": {}
    }
  }
}
```

### 3. Test Basic Functionality

After reloading, test in a new PowerShell terminal:

```powershell
# Activate virtual environment
cd C:\Users\OMEN\Desktop\poly
.\.venv\Scripts\Activate.ps1

# Test import
python -c "from polyhedra.services.semantic_scholar import SemanticScholarService; print('✅ Import successful')"

# Run demo
python demo_search.py
```

### 4. Test MCP Tools

Test in VS Code Copilot chat:

```
Search for papers about transformer architecture
```

If configured correctly, Copilot should be able to call Polyhedra's MCP tools.

## Production Environment Configuration

After publishing the package to PyPI, you can use:

```json
{
  "mcpServers": {
    "polyhedra": {
      "command": "uvx",
      "args": ["--from", "polyhedra", "polyhedra"],
      "env": {}
    }
  }
}
```

## Common Issues

### Q: Terminal commands still being intercepted?
A: Completely quit VS Code (not reload), then reopen.

### Q: MCP tools not callable?
A: 
1. Check VS Code Output panel's "MCP" channel for error logs
2. Ensure Python path is correct
3. Try saying "reload MCP server" in chat

### Q: Wrong Python path?
A: 
1. Get correct path: `(Get-Command python).Source` (after activating virtual environment)
2. Update configuration file with that path

### Q: How to check MCP server status?
A:
```powershell
# Test server startup
.\.venv\Scripts\python.exe -m polyhedra.server
# Then press Ctrl+C to stop (if it starts normally, configuration is correct)
```

## Project Status

✅ **Fixed**:
- VS Code configuration file updated to use local Python
- Removed deprecated Copilot instructions configuration

⚠️ **Manual Action Required**:
- Reload VS Code
- Update Cursor/Windsurf configuration (if using)

## Next Steps

After completing fixes, you can:

1. **Run demo**: `python demo_search.py`
2. **Run tests**: `python -m pytest tests/`
3. **Use MCP tools**: Use Polyhedra features in IDE's AI chat

## Need Help?

Check documentation:
- Complete setup guide: `docs/SETUP.md`
- API documentation: `docs/API.md`
- User guide: `docs/USER_GUIDE.md`
