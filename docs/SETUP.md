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

## LLM Configuration (for v2.1 Literature Review Features)

Polyhedra v2.1 adds AI-powered literature review generation. This requires an API key from Anthropic or OpenAI.

### Option 1: Anthropic Claude (Recommended)

**Why Claude?** Better academic writing, lower cost ($3/M input, $15/M output)

1. **Get API Key**:
   - Visit https://console.anthropic.com/
   - Sign up or log in
   - Navigate to **API Keys** section
   - Click **Create Key** (name it "Polyhedra")
   - Copy the key (starts with `sk-ant-`)

2. **Configure Environment Variable**:
   
   **Windows**:
   ```powershell
   $env:ANTHROPIC_API_KEY = "sk-ant-api03-your-key-here"
   # Or add permanently:
   setx ANTHROPIC_API_KEY "sk-ant-api03-your-key-here"
   ```
   
   **Mac/Linux**:
   ```bash
   export ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
   # Add to ~/.bashrc or ~/.zshrc for persistence
   ```
   
   **Or create `.env` file** in your project:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
   ```

3. **Verify Configuration**:
   ```
   # In your IDE chat:
   "Estimate cost for reviewing 50 papers"
   ```
   Should return cost estimate without errors.

### Option 2: OpenAI GPT

**Why GPT?** You may already have an account, familiar models

1. **Get API Key**:
   - Visit https://platform.openai.com/api-keys
   - Sign up or log in
   - Click **Create new secret key**
   - Copy the key (starts with `sk-`)

2. **Configure**:
   ```bash
   export OPENAI_API_KEY=sk-your-key-here
   export POLYHEDRA_LLM_PROVIDER=openai  # Optional: specify provider
   ```

3. **Model Selection** (optional):
   ```bash
   export POLYHEDRA_LLM_MODEL=gpt-4-turbo  # Default: gpt-4o
   ```

### Cost Management

**Set maximum cost per operation** (recommended):
```bash
export POLYHEDRA_MAX_COST=1.00  # Default: $1.00
```

Polyhedra will:
- ✅ Estimate cost before each review generation
- ✅ Warn if estimated cost exceeds $0.10
- ✅ Block operations exceeding `POLYHEDRA_MAX_COST` (unless forced)
- ✅ Log all LLM API calls with token counts

**Example `.env` file**:
```bash
# LLM Provider (choose one)
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
# OPENAI_API_KEY=sk-your-key-here

# Optional: Provider selection (default: anthropic)
# POLYHEDRA_LLM_PROVIDER=anthropic

# Optional: Cost limit (default: $1.00)
POLYHEDRA_MAX_COST=0.50

# Optional: Model override
# POLYHEDRA_LLM_MODEL=claude-3-5-sonnet-20241022
```

### Verify LLM Setup

In your IDE chat:
```
"Check if my LLM configuration is working"
```

Should confirm:
- ✓ API key detected
- ✓ Provider configured (anthropic or openai)
- ✓ Connection successful
- ✓ Ready to generate reviews

### LLM Features

Once configured, you can:

1. **Generate Literature Reviews**:
   ```
   "Generate a literature review from my papers focused on efficiency"
   ```

2. **Estimate Costs**:
   ```
   "Estimate cost for reviewing 75 papers with comprehensive depth"
   ```

3. **Check Budget**:
   ```
   "What's my current cost limit?"
   ```

**Note**: All v2.0 features (search, citations, files) work WITHOUT LLM configuration. Only literature review generation requires API keys.

---

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

### "LLM service not configured"

This error appears when trying to use literature review generation without API keys:

1. Set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` environment variable
2. Restart your IDE to pick up the new environment variable
3. Verify with: `"Check if my LLM configuration is working"`

### "API rate limit exceeded"

**Anthropic**: 50 requests/minute limit
- Wait 60 seconds and retry
- Check your API usage dashboard

**OpenAI**: Varies by account tier
- Upgrade your account tier
- Wait for rate limit reset

### "Cost exceeds configured limit"

If you see: `"Estimated cost $0.75 exceeds limit $0.50"`

**Options**:
1. Increase limit: `export POLYHEDRA_MAX_COST=1.00`
2. Reduce paper count or use brief depth
3. Force execution: Add `force=true` to your request (not recommended)

## Next Steps

- Read the [API Documentation](API.md) for detailed tool information
- Follow [Example Workflows](WORKFLOWS.md) for common research tasks
- Check the [Architecture Guide](ARCHITECTURE.md) to understand how Polyhedra works

## Getting Help

- GitHub Issues: https://github.com/polyhedra/polyhedra/issues
- Documentation: https://github.com/polyhedra/polyhedra#readme
