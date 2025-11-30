# Quick Start - No PowerShell Scripts Needed

Due to PowerShell execution policy restrictions, use these methods:

## 🎯 Easiest Methods

### 1. Use Batch Files (Double-Click to Run)

**Quick Diagnostic:**
- Double-click `test_quick.bat`
- Or run in command line: `test_quick.bat`

**Run Demo:**
- Double-click `run_demo.bat`
- Or run in command line: `run_demo.bat`

### 2. Use Python Directly

Open Command Prompt (cmd) or PowerShell:

```cmd
REM Quick diagnostic
.venv\Scripts\python.exe test_fix.py

REM Run demo
.venv\Scripts\python.exe demo_search.py

REM Run tests
.venv\Scripts\python.exe -m pytest tests/
```

### 3. Temporarily Bypass PowerShell Restrictions

Each time you open PowerShell, run first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

Then you can run `.ps1` scripts:
```powershell
.\test_quick.ps1
```

---

## ⚡ Test Immediately (Copy & Paste)

### Command Prompt (CMD)
```cmd
cd C:\Users\OMEN\Desktop\poly
.venv\Scripts\python.exe test_fix.py
```

### PowerShell (Temporary Bypass)
```powershell
cd C:\Users\OMEN\Desktop\poly
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\test_quick.ps1
```

---

## 🔧 Start MCP Server

**Good news**: MCP server is not affected by this issue!

1. Reload VS Code: `Ctrl+Shift+P` → "Reload Window"
2. VS Code will auto-start MCP server
3. Test in Copilot chat: "Search for transformer papers"

---

## 📋 Complete Workflow

```cmd
REM 1. Test installation
.venv\Scripts\python.exe test_fix.py

REM 2. View demo
.venv\Scripts\python.exe demo_search.py

REM 3. Reload VS Code
REM    Ctrl+Shift+P -> "Reload Window"

REM 4. Use in Copilot
REM    "Search for papers"
```

---

## Need Help?

- PowerShell execution policy issues: See `POWERSHELL_FIX.md`
- MCP configuration issues: See `FIX_GUIDE.md`
- Complete startup guide: See `START_GUIDE.md`
