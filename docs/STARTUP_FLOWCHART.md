# Polyhedra Startup Flowchart

```
┌─────────────────────────────────────────────────────────────┐
│                    Polyhedra MCP Server                      │
│                      Startup Flow                            │
└─────────────────────────────────────────────────────────────┘

                            Start
                             │
                             ▼
                ┌────────────────────────┐
                │  Dependencies installed?│
                │  pip install -e .      │
                └───────┬────────────────┘
                        │
                   Yes  │   No
            ┌───────────┴────────────┐
            │                        │
            ▼                        ▼
    ┌──────────────┐         ┌──────────────────┐
    │ Run diagnostic│         │ Install deps     │
    │ test_quick    │         │ pip install -e . │
    └──────┬───────┘         └────────┬─────────┘
           │                          │
           │ Pass                     │
           │                          │
           └──────────┬───────────────┘
                      │
                      ▼
            ┌─────────────────────┐
            │ Config updated?      │
            │ .vscode/settings.json│
            └─────────┬───────────┘
                      │
                 Yes  │   No
          ┌───────────┴─────────────┐
          │                         │
          ▼                         ▼
   ┌─────────────┐         ┌────────────────────┐
   │ Reload        │         │ See FIX_GUIDE.md  │
   │ VS Code       │         │ Update config     │
   │ Ctrl+Shift+P  │         └────────────────────┘
   └──────┬──────┘
          │
          ▼
   ┌─────────────────────┐
   │ MCP server auto-starts│
   │ (runs in background) │
   └──────┬──────────────┘
          │
          ▼
   ┌─────────────────────┐
   │ Check output panel   │
   │ Ctrl+Shift+U -> MCP  │
   └──────┬──────────────┘
          │
          ▼
   ┌─────────────────────────┐
   │ See "Server ready"?      │
   └────┬───────────┬─────────┘
        │           │
     Yes│           │ No
        │           │
        ▼           ▼
   ┌────────┐  ┌──────────────┐
   │ Success!│  │ Check errors  │
   └───┬────┘  │ See           │
       │       │ FIX_GUIDE.md  │
       │       └──────────────┘
       ▼
   ┌──────────────────────────┐
   │ Test in Copilot          │
   │ "Search transformer papers"│
   └──────────────────────────┘
       │
       ▼
   ┌──────────────────────────┐
   │ ✨ Start using Polyhedra!│
   └──────────────────────────┘
```

---

## Quick Command Reference

### Windows PowerShell

```powershell
# 📋 Diagnostic and testing
.\test_quick.ps1              # Quick diagnostic
.\run_demo.ps1                # Run demo
python test_fix.py            # Detailed test

# 🔧 Development commands
.\.venv\Scripts\Activate.ps1  # Activate virtual environment
python -m pytest              # Run tests
python demo_search.py         # Run search demo

# 🐛 Debug
python -m polyhedra.server    # Manually start server (Ctrl+C to stop)
```

### Batch Files

```cmd
test_quick.bat    # Quick diagnostic
run_demo.bat      # Run demo
```

---

## Three Usage Methods

### 1️⃣ Via IDE (Recommended)

```
VS Code starts
    ↓
Auto-start MCP server
    ↓
Use in Copilot chat
    ↓
Polyhedra tools auto-called
```

**Advantages**: 
- ✅ Auto-start
- ✅ No manual management
- ✅ Integrated in chat

### 2️⃣ Python Scripts

```python
from polyhedra.services.semantic_scholar import SemanticScholarService
import asyncio

async def main():
    service = SemanticScholarService()
    papers = await service.search("AI", limit=5)
    print(papers)

asyncio.run(main())
```

**Advantages**:
- ✅ Programmatic control
- ✅ Batch processing
- ✅ Custom workflows

### 3️⃣ Command Line Demo

```powershell
.\run_demo.ps1
```

**Advantages**:
- ✅ Quick testing
- ✅ Learn features
- ✅ No IDE needed

---

## Status Indicators

### ✅ Running Normally
```
MCP output: [polyhedra] Server ready
Copilot: Can call Polyhedra tools
Test: test_quick.ps1 all pass
```

### ⚠️ Needs Check
```
MCP output: No logs
Copilot: Can't see Polyhedra tools
Test: Some failures
```
**Fix**: Reload VS Code

### ❌ Has Problems
```
MCP output: Error messages
Copilot: Tool call failures
Test: Failed
```
**Fix**: See `FIX_GUIDE.md`

---

## Next Steps

1. ✅ Ensure diagnostic passes: `.\test_quick.ps1`
2. 🔄 Reload VS Code
3. 📝 Test in Copilot
4. 📚 See `docs/USER_GUIDE.md` to learn more
