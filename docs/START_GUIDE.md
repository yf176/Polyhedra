# Polyhedra Startup Guide

## 🚀 Quick Start (Recommended)

Polyhedra as an **MCP server** is automatically launched by your IDE. No manual startup needed!

### Step 1: Reload VS Code

**Must do this first!**

1. Press `Ctrl+Shift+P` (or `F1`)
2. Type and select: **"Developer: Reload Window"**
3. Or simply close and reopen VS Code

### Step 2: Verify MCP Server Started

Open VS Code's Output panel:
1. Press `Ctrl+Shift+U` to open Output panel
2. Select **"MCP"** from dropdown menu
3. Should see logs like:
   ```
   [polyhedra] Starting MCP server...
   [polyhedra] Server ready
   ```

### Step 3: Test Functionality

Test in **GitHub Copilot Chat**:

```
Search for papers about transformer architecture
```

Copilot should automatically call Polyhedra's MCP tools!

---

## 🧪 Testing and Verification

### Quick Diagnostic Test

**Windows PowerShell:**
```powershell
.\test_quick.ps1
```

**Or use batch file:**
```cmd
test_quick.bat
```

This verifies:
- ✅ Python environment is correct
- ✅ All dependencies installed
- ✅ Services can be imported normally

### Run Demo (No IDE Needed)

**PowerShell:**
```powershell
.\run_demo.ps1
```

**Batch:**
```cmd
run_demo.bat
```

**Or directly with Python:**
```powershell
.\.venv\Scripts\python.exe demo_search.py
```

---

## 🛠️ Manual Startup Methods

### Method 1: Via VS Code (Recommended)

MCP server automatically starts when VS Code launches. Configuration is in:
- `mcp.servers` section of `.vscode/settings.json`

### Method 2: Command Line Testing (Development/Debug)

**Only for testing if server can start, press Ctrl+C to stop:**

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Start MCP server
python -m polyhedra.server
```

**Note**: Server will wait for JSON-RPC input, this is normal. Press `Ctrl+C` to stop.

### Method 3: Using Python API (In Scripts)

```python
# demo_search.py is an example
import asyncio
from polyhedra.services.semantic_scholar import SemanticScholarService

async def main():
    service = SemanticScholarService()
    papers = await service.search("transformer", limit=5)
    print(f"Found {len(papers)} papers")

asyncio.run(main())
```

---

## 🔍 Check if MCP Tools Are Available

### In VS Code Copilot

1. Open Copilot Chat (sidebar icon or `Ctrl+Alt+I`)
2. Type `@workspace` then press space
3. Should see command prompts like `/`
4. Or directly ask: "Search for papers"

### View Available Tools

Ask in Copilot chat:
```
What tools are available in Polyhedra?
```

Or check documentation:
```powershell
cat docs\API.md
```

---

## ❓ Common Issues

### Q: How to know if MCP server is running?

**A:** Check VS Code Output panel (MCP channel):
- Has logs = Running ✅
- Errors = Configuration problem ❌
- No output = Not started or not configured ⚠️

### Q: Need to restart after code changes?

**A:** Yes. After modifying code:
1. Press `Ctrl+Shift+P`
2. Select "Developer: Reload Window"

### Q: MCP tools not available?

**A:** Check in order:
1. ✅ Run `.\test_quick.ps1` to ensure basic functionality works
2. ✅ Check MCP output panel for error messages
3. ✅ Confirm `.vscode/settings.json` configuration is correct
4. ✅ Reload VS Code
5. ✅ See `FIX_GUIDE.md` for detailed troubleshooting

### Q: Want to test specific functionality?

**A:** Use test scripts:
```powershell
# Run all tests
.\.venv\Scripts\python.exe -m pytest tests/

# Test specific functionality
.\.venv\Scripts\python.exe -m pytest tests/test_services/test_semantic_scholar.py

# Run demo
.\.venv\Scripts\python.exe demo_search.py
```

### Q: How to debug MCP server?

**A:** 
1. Check MCP output panel logs
2. Add logging to code:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```
3. Manually run server to see full output:
   ```powershell
   .\.venv\Scripts\python.exe -m polyhedra.server
   ```

---

## 📋 Startup Checklist

After completing all steps, verify:

- [ ] Virtual environment created: `.venv` folder exists
- [ ] Dependencies installed: `pip list` shows polyhedra
- [ ] Configuration updated: `.vscode/settings.json` uses local Python
- [ ] VS Code reloaded
- [ ] MCP output panel shows server startup
- [ ] Diagnostic test passes: `.\test_quick.ps1`
- [ ] Copilot can call Polyhedra tools

---

## 🎯 Recommended Workflow

### First Time Use
```powershell
# 1. Verify installation
.\test_quick.ps1

# 2. Run demo to understand features
.\run_demo.ps1

# 3. Reload VS Code
# Ctrl+Shift+P -> "Reload Window"

# 4. Test in Copilot
# "Search for transformer papers"
```

### Daily Development
```powershell
# After modifying code
# Ctrl+Shift+P -> "Reload Window"

# Run tests
.\.venv\Scripts\python.exe -m pytest

# Use Copilot to interact with Polyhedra
```

---

## 📚 Related Documentation

- **API Documentation**: `docs/API.md` - Detailed description of all 10 tools
- **Fix Guide**: `FIX_GUIDE.md` - Troubleshooting
- **User Guide**: `docs/USER_GUIDE.md` - Usage examples
- **IDE Configuration**: `ide-integration/SETUP_GUIDE.md` - Detailed configuration instructions

---

**Tip**: Polyhedra is an MCP tool server that extends AI assistant capabilities. You don't need to "run" it directly, but use its features through AI chat in your IDE!
