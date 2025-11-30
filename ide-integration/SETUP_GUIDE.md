# Polyhedra IDE Integration - Setup Guide

Complete instructions for setting up Polyhedra MCP Server with your IDE.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Cursor Setup](#cursor-setup)
3. [VS Code + GitHub Copilot Setup](#vs-code--github-copilot-setup)
4. [Windsurf Setup](#windsurf-setup)
5. [VS Code + MCP Extension Setup](#vs-code--mcp-extension-setup)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Configuration](#advanced-configuration)

---

## Prerequisites

Before setting up any IDE, ensure you have:

### 1. Install Polyhedra

```bash
# Using pip
pip install polyhedra

# Or using uv (recommended)
uv pip install polyhedra
```

Verify installation:
```bash
python -c "import polyhedra; print('Polyhedra installed successfully')"
```

### 2. Install uvx (Recommended)

```bash
# Install uv (includes uvx)
pip install uv

# Verify uvx is available
uvx --version
```

**Why uvx?** It automatically manages isolated environments for packages, making it ideal for MCP servers.

### 3. Test Server Manually

```bash
# Test the server starts correctly
uvx --from polyhedra polyhedra
```

You should see:
```
Polyhedra MCP server running on stdio
```

Press `Ctrl+C` to stop. If this works, you're ready to configure your IDE.

---

## Cursor Setup

**Time**: 3 minutes

### Step 1: Copy Configuration

```bash
# Windows (PowerShell)
Copy-Item ide-integration\cursor\mcp.json $HOME\.cursor\mcp.json

# macOS/Linux
cp ide-integration/cursor/mcp.json ~/.cursor/mcp.json
```

If `~/.cursor/` doesn't exist:
```bash
# Windows
New-Item -ItemType Directory -Path $HOME\.cursor

# macOS/Linux
mkdir -p ~/.cursor
```

### Step 2: Copy AI Instructions (Optional)

Copy `.cursorrules` to your project root:

```bash
# Windows
Copy-Item ide-integration\cursor\.cursorrules .cursorrules

# macOS/Linux
cp ide-integration/cursor/.cursorrules .cursorrules
```

This tells Cursor's AI how to use Polyhedra tools effectively.

### Step 3: Restart Cursor

1. Quit Cursor completely
2. Reopen Cursor
3. Open any project

### Step 4: Verify

In Cursor's chat (Cmd/Ctrl+L), type:
```
What Polyhedra tools are available?
```

Expected response should list 10 tools: search_papers, get_paper, etc.

### Cursor Configuration Details

**File Location**: `~/.cursor/mcp.json`

**Configuration**:
```json
{
  "mcpServers": {
    "polyhedra": {
      "command": "uvx",
      "args": ["--from", "polyhedra", "polyhedra"],
      "env": {},
      "disabled": false
    }
  }
}
```

**Custom Project Root** (optional):
```json
{
  "mcpServers": {
    "polyhedra": {
      "command": "uvx",
      "args": ["--from", "polyhedra", "polyhedra"],
      "env": {
        "POLYHEDRA_PROJECT_ROOT": "/path/to/my/research"
      },
      "disabled": false
    }
  }
}
```

---

## VS Code + GitHub Copilot Setup

**Time**: 4 minutes  
**Requirements**: GitHub Copilot subscription

### Step 1: Ensure GitHub Copilot is Installed

1. Open VS Code Extensions (Ctrl+Shift+X)
2. Search for "GitHub Copilot"
3. Install if not already installed
4. Sign in with your GitHub account

### Step 2: Copy Configuration

Create `.vscode` directory in your project if it doesn't exist:

```bash
# Windows
New-Item -ItemType Directory -Path .vscode -Force

# macOS/Linux
mkdir -p .vscode
```

Copy settings:
```bash
# Windows
Copy-Item ide-integration\vscode-copilot\settings.json .vscode\settings.json

# macOS/Linux
cp ide-integration/vscode-copilot/settings.json .vscode/settings.json
```

### Step 3: Copy Copilot Instructions

Create `.github` directory:

```bash
# Windows
New-Item -ItemType Directory -Path .github -Force

# macOS/Linux
mkdir -p .github
```

Copy instructions:
```bash
# Windows
Copy-Item ide-integration\vscode-copilot\copilot-instructions.md .github\copilot-instructions.md

# macOS/Linux
cp ide-integration/vscode-copilot/copilot-instructions.md .github/copilot-instructions.md
```

### Step 4: Restart VS Code

1. Close VS Code
2. Reopen your project
3. Copilot should auto-detect the configuration

### Step 5: Verify

Open Copilot Chat (Ctrl+Shift+I), type:
```
@workspace Search for papers on transformer models
```

Copilot should invoke the Polyhedra `search_papers` tool.

### VS Code + Copilot Configuration Details

**File Locations**:
- `.vscode/settings.json` - VS Code settings
- `.github/copilot-instructions.md` - Copilot AI instructions

**Settings**:
```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    {
      "text": "When working on research projects, use the Polyhedra MCP tools..."
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

---

## Windsurf Setup

**Time**: 3 minutes

### Step 1: Copy Configuration

```bash
# Windows (PowerShell)
Copy-Item ide-integration\windsurf\mcp.json $HOME\.windsurf\mcp.json

# macOS/Linux
cp ide-integration/windsurf/mcp.json ~/.windsurf/mcp.json
```

If `~/.windsurf/` doesn't exist:
```bash
# Windows
New-Item -ItemType Directory -Path $HOME\.windsurf

# macOS/Linux
mkdir -p ~/.windsurf
```

### Step 2: Restart Windsurf

1. Quit Windsurf completely
2. Reopen Windsurf
3. Open any project

### Step 3: Verify

In Windsurf's AI chat, type:
```
List available MCP tools
```

Should show 10 Polyhedra tools.

### Windsurf Configuration Details

**File Location**: `~/.windsurf/mcp.json`

**Configuration**:
```json
{
  "mcpServers": {
    "polyhedra": {
      "command": "uvx",
      "args": ["--from", "polyhedra", "polyhedra"],
      "env": {},
      "disabled": false
    }
  }
}
```

---

## VS Code + MCP Extension Setup

**Time**: 5 minutes  
**Requirements**: MCP Tools extension

### Step 1: Install MCP Extension

1. Open VS Code Extensions (Ctrl+Shift+X)
2. Search for "MCP Tools"
3. Install the extension
4. Reload VS Code if prompted

### Step 2: Copy Configuration

Create `.vscode` directory:
```bash
# Windows
New-Item -ItemType Directory -Path .vscode -Force

# macOS/Linux
mkdir -p .vscode
```

Copy settings:
```bash
# Windows
Copy-Item ide-integration\vscode-mcp\settings.json .vscode\settings.json

# macOS/Linux
cp ide-integration/vscode-mcp/settings.json .vscode/settings.json
```

### Step 3: Restart VS Code

1. Close VS Code
2. Reopen your project

### Step 4: Verify

1. Open MCP panel (should appear in sidebar)
2. Check "Polyhedra" server is listed
3. Expand to see 10 available tools

### VS Code + MCP Configuration Details

**File Location**: `.vscode/settings.json`

**Configuration**:
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

---

## Verification

After setup, verify your installation with these tests:

### Test 1: Tool Discovery

Ask your IDE's AI:
```
What Polyhedra tools are available?
```

**Expected**: List of 10 tools (search_papers, get_paper, query_similar_papers, index_papers, add_citation, get_citations, save_file, get_context, init_project, get_project_status)

### Test 2: Paper Search

```
Search for papers on "neural networks" from 2024
```

**Expected**: JSON response with paper results from Semantic Scholar

### Test 3: Project Initialization

```
Initialize a research project called "test-project"
```

**Expected**: Creates directory structure with papers/, notes/, literature-review/, etc.

### Test 4: File Operations

```
Save "Hello from Polyhedra" to notes/test.md
```

**Expected**: Creates notes/test.md with content

### Test 5: Project Status

```
Show my project status
```

**Expected**: Overview of project structure and files

### All Tests Passing?

✅ **You're ready to use Polyhedra!**

See [docs/WORKFLOWS.md](../../docs/WORKFLOWS.md) for research workflow examples.

---

## Troubleshooting

### Issue: Tools Not Appearing

**Symptoms**: IDE doesn't show Polyhedra tools

**Solutions**:

1. **Verify config location**:
   ```bash
   # Cursor/Windsurf: User home
   ls ~/.cursor/mcp.json
   ls ~/.windsurf/mcp.json
   
   # VS Code: Project root
   ls .vscode/settings.json
   ```

2. **Check uvx is in PATH**:
   ```bash
   uvx --version
   ```
   If not found, add to PATH or use full path in config

3. **Restart IDE completely**:
   - Quit application (don't just close window)
   - Reopen

4. **Check logs**:
   - Cursor: Output panel → MCP
   - VS Code: Output panel → MCP Server
   - Windsurf: Developer tools → Console

### Issue: Permission Errors

**Symptoms**: "Permission denied" or "Access denied"

**Solutions**:

1. **Check file permissions**:
   ```bash
   # Make config readable
   chmod 644 ~/.cursor/mcp.json
   ```

2. **Verify Polyhedra installation**:
   ```bash
   pip show polyhedra
   ```

3. **Try with full path**:
   ```json
   {
     "command": "/path/to/uvx",
     "args": ["--from", "polyhedra", "polyhedra"]
   }
   ```

### Issue: Server Won't Start

**Symptoms**: Error messages about server startup

**Solutions**:

1. **Test server manually**:
   ```bash
   uvx --from polyhedra polyhedra
   ```
   If this fails, the issue is with Polyhedra installation

2. **Check Python version**:
   ```bash
   python --version  # Should be 3.11+
   ```

3. **Reinstall Polyhedra**:
   ```bash
   pip uninstall polyhedra
   pip install polyhedra
   ```

4. **Check for conflicts**:
   ```bash
   # Ensure no other MCP servers conflict
   # Check IDE settings for duplicate server names
   ```

### Issue: Tools Execute But Fail

**Symptoms**: Tools are visible but return errors

**Solutions**:

1. **Check project structure**:
   ```bash
   # Ensure you're in a project directory
   pwd
   ```

2. **Initialize project**:
   ```
   Initialize a research project called "my-research"
   ```

3. **Check network for API calls**:
   ```bash
   # Test Semantic Scholar API
   curl https://api.semanticscholar.org/graph/v1/paper/search?query=test
   ```

4. **Review error messages**:
   - Look for specific error types
   - Check [docs/ERROR_HANDLING.md](../../docs/ERROR_HANDLING.md)

### Issue: Slow Performance

**Symptoms**: Tools take long time to respond

**Solutions**:

1. **First RAG query downloads model** (~400MB):
   - This is one-time
   - Subsequent queries are fast

2. **Check network speed**:
   - Semantic Scholar API calls require internet
   - Use caching for repeated queries

3. **Optimize queries**:
   - Limit search results (default: 10)
   - Use specific year ranges
   - Index papers once, query many times

### Issue: RAG/Semantic Search Not Working

**Symptoms**: query_similar_papers fails or returns no results

**Solutions**:

1. **Must index papers first**:
   ```
   Search for papers on "topic"
   Index the papers from my search
   Query similar papers about "research question"
   ```

2. **Model download on first use**:
   - Downloads sentence-transformers model
   - Takes 30-60 seconds first time
   - Check `.polyhedra/` directory created

3. **Check disk space**:
   - Model: ~400MB
   - Index: ~1-2MB per 1000 papers

### Still Having Issues?

1. **Check documentation**:
   - [API Reference](../../docs/API.md)
   - [Error Handling](../../docs/ERROR_HANDLING.md)
   - [Workflows](../../docs/WORKFLOWS.md)

2. **Enable debug logging**:
   ```json
   {
     "env": {
       "POLYHEDRA_LOG_LEVEL": "DEBUG"
     }
   }
   ```

3. **Run tests**:
   ```bash
   cd /path/to/polyhedra
   pytest tests/ -v
   ```

4. **File an issue**:
   - GitHub: Include error messages, config, and steps to reproduce

---

## Advanced Configuration

### Custom Project Root

Override default project directory:

```json
{
  "mcpServers": {
    "polyhedra": {
      "command": "uvx",
      "args": ["--from", "polyhedra", "polyhedra"],
      "env": {
        "POLYHEDRA_PROJECT_ROOT": "/home/user/my-research"
      }
    }
  }
}
```

All file operations will be relative to this path.

### Custom Cache Location

Change where embeddings and cache are stored:

```json
{
  "env": {
    "POLYHEDRA_CACHE_DIR": "/path/to/custom/cache"
  }
}
```

Useful for:
- Network drives
- Synced folders (Dropbox, etc.)
- Limited disk space on default location

### Debug Logging

Enable detailed logs for troubleshooting:

```json
{
  "env": {
    "POLYHEDRA_LOG_LEVEL": "DEBUG"
  }
}
```

Logs will appear in IDE's output panel.

### Multiple Polyhedra Instances

Run multiple instances for different projects:

```json
{
  "mcpServers": {
    "polyhedra-project-a": {
      "command": "uvx",
      "args": ["--from", "polyhedra", "polyhedra"],
      "env": {
        "POLYHEDRA_PROJECT_ROOT": "/path/to/project-a"
      }
    },
    "polyhedra-project-b": {
      "command": "uvx",
      "args": ["--from", "polyhedra", "polyhedra"],
      "env": {
        "POLYHEDRA_PROJECT_ROOT": "/path/to/project-b"
      }
    }
  }
}
```

Tools will be prefixed with instance name.

### Development Version

Use local development version instead of PyPI:

```json
{
  "command": "python",
  "args": ["-m", "polyhedra.server"],
  "env": {
    "PYTHONPATH": "/path/to/polyhedra/src"
  }
}
```

Restart IDE after code changes.

---

## Quick Reference

### Command Locations

| IDE | Config File | Location Type |
|-----|-------------|---------------|
| Cursor | `~/.cursor/mcp.json` | User home |
| Windsurf | `~/.windsurf/mcp.json` | User home |
| VS Code | `.vscode/settings.json` | Project root |

### Installation Commands

```bash
# Install Polyhedra
pip install polyhedra

# Install uv (includes uvx)
pip install uv

# Test server
uvx --from polyhedra polyhedra

# Verify installation
python -c "import polyhedra; print('OK')"
```

### Quick Test Commands

```
# After setup, test with:
What Polyhedra tools are available?
Search for papers on "neural networks" from 2024
Initialize a research project called "test"
Show my project status
```

---

## Need More Help?

- **API Documentation**: [docs/API.md](../../docs/API.md)
- **Workflow Examples**: [docs/WORKFLOWS.md](../../docs/WORKFLOWS.md)
- **Error Handling**: [docs/ERROR_HANDLING.md](../../docs/ERROR_HANDLING.md)
- **Architecture**: [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md)
- **Main README**: [README.md](../../README.md)

Happy researching! 🚀
