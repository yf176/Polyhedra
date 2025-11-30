# Development Environment Setup

##  Virtual Environment Created

A Python 3.12 virtual environment has been set up at .venv/ to isolate project dependencies.

## Quick Test Commands

### Run all tests for reviewed stories:
```
.\test.bat tests/test_services/test_semantic_scholar.py tests/test_services/test_citation_manager.py -v
```

### Run with coverage:
```
.\test.bat tests/test_services/test_semantic_scholar.py tests/test_services/test_citation_manager.py --cov=polyhedra --cov-report=term-missing
```

### Run specific test class:
```
.\test.bat tests/test_services/test_citation_manager.py::TestAddCitation -v
```

## Installed Dependencies

- httpx (async HTTP client)
- pydantic (data validation)
- bibtexparser (BibTeX parsing)
- pytest (testing framework)
- pytest-asyncio (async test support)
- pytest-cov (coverage reporting)

## Test Results Summary

 **STORY-001** (Semantic Scholar): 18/18 tests passing, 91% coverage  
 **STORY-002** (Citation Management): 7/7 tests passing, 94% coverage  
 **Combined**: 25/25 tests passing

## Note on Python Versions

- **Project requires**: Python 3.11+ (see pyproject.toml)
- **Current venv**: Python 3.12.0
- **System Python 3.9**: Incompatible (too old)

The virtual environment isolates dependencies and ensures consistent behavior across development and testing.
