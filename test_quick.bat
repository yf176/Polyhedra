@echo off
REM Quick diagnostic script - Windows batch version

echo ========================================
echo Polyhedra Quick Diagnostic
echo ========================================
echo.

REM Check virtual environment
if not exist ".venv\Scripts\python.exe" (
    echo [Error] Virtual environment not found
    echo Please run: python -m venv .venv
    echo Then: .venv\Scripts\pip install -e .
    pause
    exit /b 1
)

echo [1/3] Checking Python environment...
.venv\Scripts\python.exe --version
echo.

echo [2/3] Running diagnostic tests...
.venv\Scripts\python.exe test_fix.py
echo.

if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo ✅ Diagnostic complete - All OK
    echo ========================================
    echo.
    echo Next steps:
    echo   1. Close and reopen VS Code
    echo   2. Test MCP tools in AI chat
    echo   3. Or run demo: run_demo.bat
) else (
    echo ========================================
    echo ❌ Issues found
    echo ========================================
    echo.
    echo See docs\FIX_GUIDE.md for detailed solutions
)

echo.
pause
