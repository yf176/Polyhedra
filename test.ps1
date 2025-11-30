# Test runner script for Polyhedra project
# Uses Python 3.12 virtual environment

$env:PYTHONPATH = "$PSScriptRoot\src"
& "$PSScriptRoot\.venv\Scripts\python.exe" -m pytest @args
