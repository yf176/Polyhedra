# PowerShell Execution Policy Fix

## Problem Description

Windows PowerShell blocks script execution by default as a security policy.

## 🚀 Solutions (3 Methods)

### Method 1: Use Batch Files (Easiest)

**No settings changes needed, just double-click to run:**

```cmd
test_quick.bat    # Quick diagnostic
run_demo.bat      # Run demo
```

Or in command line:
```cmd
test_quick.bat
```

---

### Method 2: Temporarily Allow Current Session (Recommended)

**Run each time you open a new PowerShell window:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

Then you can run `.ps1` scripts:
```powershell
.\test_quick.ps1
```

---

### Method 3: Permanent Change (Requires Admin)

**Open PowerShell as Administrator, then run:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Select `Y` to confirm.

After this, you can run scripts normally.

---

### Method 4: Use Python Directly (No Scripts Needed)

**No dependency on PowerShell or batch files:**

```cmd
# Quick diagnostic
.venv\Scripts\python.exe test_fix.py

# Run demo
.venv\Scripts\python.exe demo_search.py

# Run tests
.venv\Scripts\python.exe -m pytest
```

---

## ⚡ Start Immediately (No Policy Changes Needed)

### Option A: Use Batch Files
```cmd
test_quick.bat
```

### Option B: Use Python Directly
```cmd
.venv\Scripts\python.exe test_fix.py
```

### Option C: Temporary Bypass (Single Command)
```powershell
powershell -ExecutionPolicy Bypass -File .\test_quick.ps1
```

---

## Recommended Workflow

```cmd
REM 1. Quick diagnostic
.venv\Scripts\python.exe test_fix.py

REM 2. Run demo
.venv\Scripts\python.exe demo_search.py

REM 3. VS Code will auto-start MCP server
REM    Just reload the window
```

---

## Security Notes

- **Bypass**: Only affects current PowerShell session, reverts after closing
- **RemoteSigned**: Only allows local scripts and signed remote scripts (recommended)
- **Unrestricted**: Allows all scripts (not recommended)

More info: https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_execution_policies
