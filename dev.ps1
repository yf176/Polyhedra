# Polyhedra Development Helper Script
# Usage: .\dev.ps1 <command>

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

$venvPython = ".\venv\Scripts\python.exe"
$venvPytest = ".\venv\Scripts\pytest.exe"
$venvBlack = ".\venv\Scripts\black.exe"
$venvRuff = ".\venv\Scripts\ruff.exe"
$venvMypy = ".\venv\Scripts\mypy.exe"

switch ($Command) {
    "test" {
        Write-Host "Running tests..." -ForegroundColor Cyan
        & $venvPytest
    }
    "test-cov" {
        Write-Host "Running tests with coverage..." -ForegroundColor Cyan
        & $venvPytest --cov=polyhedra --cov-report=html --cov-report=term
        Write-Host "`nCoverage report generated in htmlcov/index.html" -ForegroundColor Green
    }
    "format" {
        Write-Host "Formatting code..." -ForegroundColor Cyan
        & $venvBlack src tests
    }
    "lint" {
        Write-Host "Linting code..." -ForegroundColor Cyan
        & $venvRuff check src tests
    }
    "type-check" {
        Write-Host "Type checking..." -ForegroundColor Cyan
        & $venvMypy src
    }
    "check-all" {
        Write-Host "Running all checks..." -ForegroundColor Cyan
        & $venvBlack src tests
        & $venvRuff check src tests
        & $venvMypy src
        & $venvPytest
        Write-Host "`nAll checks complete!" -ForegroundColor Green
    }
    "run" {
        Write-Host "Starting Polyhedra MCP Server..." -ForegroundColor Cyan
        & $venvPython -m polyhedra.server
    }
    "shell" {
        Write-Host "Starting Python shell with polyhedra loaded..." -ForegroundColor Cyan
        & $venvPython -i -c "import polyhedra; from polyhedra.server import app; print(f'Polyhedra v{polyhedra.__version__} loaded')"
    }
    default {
        Write-Host "Polyhedra Development Commands:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  .\dev.ps1 test        - Run tests" -ForegroundColor White
        Write-Host "  .\dev.ps1 test-cov    - Run tests with coverage report" -ForegroundColor White
        Write-Host "  .\dev.ps1 format      - Format code with Black" -ForegroundColor White
        Write-Host "  .\dev.ps1 lint        - Lint code with Ruff" -ForegroundColor White
        Write-Host "  .\dev.ps1 type-check  - Type check with mypy" -ForegroundColor White
        Write-Host "  .\dev.ps1 check-all   - Run all checks (format, lint, type, test)" -ForegroundColor White
        Write-Host "  .\dev.ps1 run         - Start MCP server" -ForegroundColor White
        Write-Host "  .\dev.ps1 shell       - Interactive Python shell" -ForegroundColor White
        Write-Host ""
        Write-Host "Quick test: " -NoNewline -ForegroundColor Cyan
        & $venvPython -c "import polyhedra; print(f'v{polyhedra.__version__} ready')"
    }
}
