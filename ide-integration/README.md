# IDE Integration for Polyhedra

This folder contains configuration files and instructions for integrating Polyhedra MCP Server with various IDEs.

## Supported IDEs

1. **Cursor** - AI-first code editor
2. **VS Code + GitHub Copilot** - VS Code with Copilot extension
3. **Windsurf** - Codeium's AI-native IDE
4. **VS Code + MCP Extension** - VS Code with MCP Tools extension

## Quick Setup

Choose your IDE and follow the corresponding guide:

### Cursor

1. Copy `cursor/mcp.json` to `~/.cursor/mcp.json`
2. Copy `cursor/.cursorrules` to your project root
3. Restart Cursor
4. Test: Ask "Search for papers on transformer models"

### VS Code + GitHub Copilot

1. Copy `vscode-copilot/settings.json` to `.vscode/settings.json` in your project
2. Copy `vscode-copilot/copilot-instructions.md` to `.github/copilot-instructions.md`
3. Restart VS Code
4. Test: Ask Copilot "Initialize a research project"

### Windsurf

1. Copy `windsurf/mcp.json` to `~/.windsurf/mcp.json`
2. Restart Windsurf
3. Test: Ask "Show me my project status"

### VS Code + MCP Extension

1. Install "MCP Tools" extension from marketplace
2. Copy `vscode-mcp/settings.json` to `.vscode/settings.json`
3. Restart VS Code
4. Test: Check MCP panel shows 10 Polyhedra tools

## Directory Structure

```
ide-integration/
├── README.md                      # This file
├── cursor/
│   ├── mcp.json                   # MCP server configuration
│   └── .cursorrules               # AI assistant instructions
├── vscode-copilot/
│   ├── settings.json              # VS Code settings with Copilot
│   └── copilot-instructions.md    # GitHub Copilot instructions
├── windsurf/
│   └── mcp.json                   # Windsurf MCP configuration
├── vscode-mcp/
│   └── settings.json              # VS Code with MCP extension
└── SETUP_GUIDE.md                 # Detailed setup instructions
```

## Configuration Options

All configurations support these environment variables:

- `POLYHEDRA_PROJECT_ROOT`: Override default project root
- `POLYHEDRA_CACHE_DIR`: Custom cache location
- `POLYHEDRA_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

### Example with custom project root

**Cursor (`~/.cursor/mcp.json`):**
```json
{
  "mcpServers": {
    "polyhedra": {
      "command": "uvx",
      "args": ["--from", "polyhedra", "polyhedra"],
      "env": {
        "POLYHEDRA_PROJECT_ROOT": "/path/to/my/research"
      }
    }
  }
}
```

## Troubleshooting

### Tools not appearing

1. Check IDE has restarted after config changes
2. Verify `uvx` is in PATH: `uvx --version`
3. Check logs in IDE's output panel
4. Try running directly: `uvx --from polyhedra polyhedra`

### Permission errors

Make sure config files have correct location:
- Cursor: `~/.cursor/mcp.json` (user home)
- Windsurf: `~/.windsurf/mcp.json` (user home)
- VS Code: `.vscode/settings.json` (project root)

### Connection issues

1. Check polyhedra is installed: `pip show polyhedra`
2. Verify server starts: `python -m polyhedra.server`
3. Check for port conflicts
4. Review IDE extension logs

## Testing Your Setup

After configuration, test with these commands:

1. **Tool Discovery**: "What Polyhedra tools are available?"
2. **Search**: "Search for papers on neural networks from 2024"
3. **Project Init**: "Initialize a research project called test"
4. **File Ops**: "Save 'Hello Research' to notes/test.md"
5. **Status**: "Show my project status"

All commands should work without errors.

## Need Help?

- **Full Guide**: See `SETUP_GUIDE.md` for detailed instructions
- **API Docs**: See `../docs/API.md` for tool documentation
- **Workflows**: See `../docs/WORKFLOWS.md` for usage examples
- **Issues**: Check `../docs/ERROR_HANDLING.md` for common problems

## Development

To modify configurations:

1. Edit files in this folder
2. Test with your IDE
3. Update `SETUP_GUIDE.md` if behavior changes
4. Keep all IDE configs in sync (same tool names, args)

## Version Compatibility

- **Polyhedra**: 0.1.0+
- **Cursor**: 0.40+
- **VS Code**: 1.85+
- **Windsurf**: 1.0+
- **MCP Extension**: Latest from marketplace
