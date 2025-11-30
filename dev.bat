@echo off
REM Polyhedra Development Helper
REM Usage: dev.bat [command]

if "%1"=="" goto help
if "%1"=="test" goto test
if "%1"=="test-cov" goto test-cov
if "%1"=="format" goto format
if "%1"=="lint" goto lint
if "%1"=="type-check" goto type-check
if "%1"=="check-all" goto check-all
if "%1"=="run" goto run
goto help

:test
echo Running tests...
.\venv\Scripts\pytest.exe
goto end

:test-cov
echo Running tests with coverage...
.\venv\Scripts\pytest.exe --cov=polyhedra --cov-report=html --cov-report=term
echo Coverage report: htmlcov/index.html
goto end

:format
echo Formatting code...
.\venv\Scripts\black.exe src tests
goto end

:lint
echo Linting code...
.\venv\Scripts\ruff.exe check src tests
goto end

:type-check
echo Type checking...
.\venv\Scripts\mypy.exe src
goto end

:check-all
echo Running all checks...
call .\venv\Scripts\black.exe src tests
call .\venv\Scripts\ruff.exe check src tests
call .\venv\Scripts\mypy.exe src
call .\venv\Scripts\pytest.exe
echo All checks complete!
goto end

:run
echo Starting Polyhedra MCP Server...
.\venv\Scripts\python.exe -m polyhedra.server
goto end

:help
echo.
echo Polyhedra Development Commands:
echo.
echo   dev test        - Run tests
echo   dev test-cov    - Run tests with coverage
echo   dev format      - Format code with Black
echo   dev lint        - Lint code with Ruff
echo   dev type-check  - Type check with mypy
echo   dev check-all   - Run all checks
echo   dev run         - Start MCP server
echo.
.\venv\Scripts\python.exe -c "import polyhedra; print('v' + polyhedra.__version__ + ' ready')"

:end
