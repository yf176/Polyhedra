# IDE Setup Guide

This guide will help you configure Polyhedra in your IDE in less than 5 minutes.

## Prerequisites

- Python 3.11 or higher
- One of the supported IDEs:
  - Cursor
  - VS Code with GitHub Copilot
  - Windsurf
  - VS Code with MCP extension

## Installation

### Step 1: Install Polyhedra

Using pip:
```bash
pip install polyhedra
```

Using uv (recommended):
```bash
uv pip install polyhedra
```

### Step 2: Verify Installation

```bash
polyhedra --version
```

## IDE Configuration

Choose your IDE and follow the specific setup instructions:

### Cursor Setup

1. **Create MCP config directory** (if it doesn't exist):
   ```bash
   mkdir -p ~/.cursor
   ```

2. **Create or edit `~/.cursor/mcp.json`**:
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

3. **Add `.cursorrules` to your project** (optional but recommended):
   Copy `.cursorrules` from the Polyhedra repository to your research project root.

4. **Restart Cursor**

5. **Verify**: Open Cursor chat and type "List available Polyhedra tools"

### VS Code + GitHub Copilot Setup

1. **Install GitHub Copilot Chat extension** (if not already installed)

2. **Add to your workspace `.vscode/settings.json`**:
   ```json
   {
     "github.copilot.chat.codeGeneration.instructions": [
       {
         "text": "When working on research projects, use the Polyhedra MCP tools to search papers, manage citations, and organize literature."
       }
     ],
     "mcp.servers": {
       "polyhedra": {
         "command": "uvx",
         "args": ["--from", "polyhedra", "polyhedra"],
         "env": {}
       }
     }
   }
   ```

3. **Add `.github/copilot-instructions.md`** to your project (optional):
   Copy `copilot-instructions.md` from the Polyhedra repository.

4. **Restart VS Code**

5. **Verify**: Open Copilot Chat and ask "What Polyhedra tools are available?"

### Windsurf Setup

1. **Create MCP config directory** (if it doesn't exist):
   ```bash
   mkdir -p ~/.windsurf
   ```

2. **Create or edit `~/.windsurf/mcp.json`**:
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

3. **Add `.cursorrules` to your project** (Windsurf uses same format):
   Copy `.cursorrules` from the Polyhedra repository to your research project root.

4. **Restart Windsurf**

5. **Verify**: Open chat and ask about available tools

### VS Code + MCP Extension Setup

1. **Install the MCP extension** from VS Code marketplace

2. **Add to your workspace `.vscode/settings.json`**:
   ```json
   {
     "mcp.servers": {
       "polyhedra": {
         "command": "uvx",
         "args": ["--from", "polyhedra", "polyhedra"],
         "env": {}
       }
     }
   }
   ```

3. **Restart VS Code**

4. **Verify**: Check the MCP extension panel for Polyhedra tools

## Initialize Your First Project

Once configured, initialize a new research project:

1. **Create project directory**:
   ```bash
   mkdir my-research-project
   cd my-research-project
   ```

2. **In your IDE chat, run**:
   ```
   Use init_project to set up this research project
   ```

3. **Verify the structure was created**:
   ```
   literature/
   ideas/
   method/
   paper/
   references.bib
   .poly/
   ```

## Quick Start Example

Try this workflow in your IDE chat:

1. **Search for papers**:
   ```
   Search for recent papers on "large language models" from 2023-2024
   ```

2. **Add a citation**:
   ```
   Add this paper to my bibliography: [paste BibTeX]
   ```

3. **Get project status**:
   ```
   Show me my current project status
   ```

## Troubleshooting

### "Command not found: uvx"

Install `uv`:
```bash
pip install uv
```

Or use `python -m polyhedra` instead:
```json
{
  "command": "python",
  "args": ["-m", "polyhedra"]
}
```

### "No tools available"

1. Check that Polyhedra is installed: `pip list | grep polyhedra`
2. Verify the MCP config file is in the correct location
3. Restart your IDE completely
4. Check IDE logs for MCP connection errors

### "Tool execution failed"

1. Verify you're in a project directory
2. Check that required files exist (e.g., `literature/papers.json` for indexing)
3. Ensure you have internet connectivity for paper searches

## Next Steps

- Read the [API Documentation](API.md) for detailed tool information
- Follow [Example Workflows](WORKFLOWS.md) for common research tasks
- Check the [Architecture Guide](ARCHITECTURE.md) to understand how Polyhedra works

## Getting Help

- GitHub Issues: https://github.com/polyhedra/polyhedra/issues
- Documentation: https://github.com/polyhedra/polyhedra#readme
