# Run Polyhedra Demo - PowerShell version

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "[Error] Virtual environment not found" -ForegroundColor Red
    Write-Host "Please run test_quick.ps1 first for diagnostic"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Starting Polyhedra demo..." -ForegroundColor Cyan
Write-Host ""
& .\.venv\Scripts\python.exe demo_search.py
Write-Host ""
Read-Host "Press Enter to exit"
