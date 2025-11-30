# Polyhedra Quick Diagnostic Script - PowerShell version

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Polyhedra Quick Diagnostic" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check virtual environment
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "[Error] Virtual environment not found" -ForegroundColor Red
    Write-Host "Please run: python -m venv .venv"
    Write-Host "Then: .venv\Scripts\pip install -e ."
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[1/3] Checking Python environment..." -ForegroundColor Yellow
& .\.venv\Scripts\python.exe --version
Write-Host ""

Write-Host "[2/3] Running diagnostic tests..." -ForegroundColor Yellow
& .\.venv\Scripts\python.exe test_fix.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✅ Diagnostic complete - All OK" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "  1. Close and reopen VS Code"
    Write-Host "  2. Test MCP tools in AI chat"
    Write-Host "  3. Or run demo: .\run_demo.ps1"
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "❌ Issues found" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "See docs/FIX_GUIDE.md for detailed solutions"
}

Write-Host ""
Read-Host "Press Enter to exit"
