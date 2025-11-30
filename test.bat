@echo off
REM Test runner for Polyhedra project using Python 3.12 venv
set PYTHONPATH=%~dp0src
"%~dp0.venv\Scripts\python.exe" -m pytest %*
