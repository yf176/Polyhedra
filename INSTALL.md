# Polyhedra Installation Guide

Complete installation guide for Polyhedra MCP Server.

## Prerequisites

- **Python 3.11 or higher** (3.12 recommended)
- **pip** or **uv** package manager
- **Git** (for GitHub installation)
- One of the supported IDEs:
  - Cursor
  - VS Code with GitHub Copilot
  - Windsurf
  - VS Code with MCP extension

## Installation Methods

### Method 1: From GitHub (Only Method)

**Polyhedra is distributed via GitHub only**

```bash
# Clone the repository
git clone https://github.com/yourusername/polyhedra.git
cd polyhedra

# Install dependencies and package in editable mode
pip install -e .
```

**What this does**:
- Clones the full source code
- Installs all dependencies automatically
- Installs Polyhedra in "editable" mode (changes take effect immediately)
- Creates the `polyhedra` command

**Verify installation**:
```bash
python -m polyhedra.server
```

---

### Method 2: From PyPI (Future)

**Production installation (not yet available)**

```bash
pip install polyhedra
```

> **Note**: Package will be published to PyPI soon. Use Method 1 (GitHub) for now.

---

### Method 3: With uv (Faster)

**Recommended for development**

```bash
# Install uv if needed
pip install uv

# Clone and install
git clone https://github.com/yourusername/polyhedra.git
cd polyhedra
uv pip install -e .
```

---

## Post-Installation Setup

### 1. Verify Installation

```bash
# Check module
python -c "import polyhedra; print(' Polyhedra installed')"

# Check server
python -m polyhedra.server
```

### 2. Virtual Environment (Recommended)

```bash
# Create venv
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

# Install
pip install -e .
```

---

## IDE Configuration

### Cursor

**Config file**: `~/.cursor/mcp.json`

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

**Restart Cursor**, then test: *"What Polyhedra tools are available?"*

---

### VS Code with GitHub Copilot

**Workspace settings**: `.vscode/settings.json`

```json
{
  "mcp.servers": {
    "polyhedra": {
      "command": "python",
      "args": ["-m", "polyhedra.server"]
    }
  }
}
```

**Copilot instructions**: `.github/copilot-instructions.md`

```markdown
# Polyhedra Research Assistant

Use Polyhedra MCP tools for academic research.
Available: search_papers, add_citation, index_papers, etc.
```

**Reload window**: Ctrl+Shift+P  "Developer: Reload Window"

---

### Windsurf

Same as Cursor, use `~/.windsurf/mcp.json`

---

## Troubleshooting

### "Module not found"

**Fix**: Reinstall in correct environment
```bash
pip uninstall polyhedra
pip install -e .
```

### "MCP server not starting"

**Check**:
1. Valid JSON in config file
2. Python path correct
3. IDE console for errors
4. Restart IDE

### "Command 'uvx' not found"

**Fix**: Use `python -m polyhedra.server` instead

### Dependencies fail

**Fix**:
```bash
pip install --upgrade pip
uv pip install -e .
```

---

## Updating

```bash
cd polyhedra
git pull origin main
pip install -e . --upgrade
```

---

## Uninstalling

```bash
pip uninstall polyhedra
```

Remove config from IDE.

---

## Next Steps

1. Read **User Guide**: `docs/USER_GUIDE.md`
2. Try **Quick Start**: Initialize first project
3. Explore **API**: `docs/API.md` for all 10 tools
4. **Contribute**: Report issues, share workflows

**Happy researching! **
