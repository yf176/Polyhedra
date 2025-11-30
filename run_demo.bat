@echo off
REM Run Polyhedra demo

if not exist ".venv\Scripts\python.exe" (
    echo [Error] Virtual environment not found
    echo Please run test_quick.bat first for diagnostic
    pause
    exit /b 1
)

echo Starting Polyhedra demo...
echo.
.venv\Scripts\python.exe demo_search.py
echo.
pause
