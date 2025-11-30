# Contributing to Polyhedra

## Development Setup

### Prerequisites

- Python 3.11 or higher
- pip or uv package manager

### Initial Setup

```bash
# Clone the repository
cd poly

# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# source venv/bin/activate   # Linux/Mac

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Development Workflow

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=polyhedra --cov-report=html

# Format code
black src tests

# Lint code
ruff check src tests

# Type check
mypy src

# Run all checks before committing
black src tests ; ruff check src tests ; mypy src ; pytest
```

## Project Structure

```
poly/
 src/polyhedra/          # Main package
    services/           # Service implementations
    schemas/            # Pydantic models
    server.py           # MCP server entry point
    __init__.py
 tests/                  # Test suite
    test_services/      # Service tests
    test_schemas/       # Schema tests
    conftest.py         # Pytest fixtures
 docs/                   # Documentation
 pyproject.toml          # Project configuration
 README.md
```

## Testing Guidelines

- Write tests for all new features
- Maintain >80% code coverage
- Use pytest fixtures from conftest.py
- Mark integration tests with @pytest.mark.integration

## Code Style

- Follow PEP 8
- Use type hints for all functions
- Line length: 100 characters
- Use Black for formatting
- Use Ruff for linting

## Story Development Process

1. Check story status in docs/stories/
2. Implement features according to acceptance criteria
3. Write unit and integration tests
4. Update story checklist as you complete tasks
5. Run full test suite before marking story complete
