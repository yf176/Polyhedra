# Installation & Running Guide

## Prerequisites

- **Python 3.11 or 3.12** (3.9 is too old)
- **Windows PowerShell** or **Command Prompt**
- **pip** (comes with Python)

## Quick Start (5 minutes)

### 1. Check Python Version

```powershell
py -0
```

Look for -V:3.12 or -V:3.11 in the output. If not present, install Python 3.12 from [python.org](https://www.python.org/downloads/).

### 2. Clone/Navigate to Project

```powershell
cd c:\Users\OMEN\Desktop\poly
```

### 3. Create Virtual Environment

**Option A: Using py launcher (Recommended)**
```powershell
py -3.12 -m venv .venv
```

**Option B: Using python directly**
```powershell
python -m venv .venv
```

### 4. Install Dependencies

**Basic dependencies (for testing reviewed stories):**
```powershell
.\.venv\Scripts\pip.exe install httpx pydantic bibtexparser pytest pytest-asyncio pytest-cov
```

**All dependencies (if you have compatible PyTorch):**
```powershell
.\.venv\Scripts\pip.exe install httpx pydantic bibtexparser pytest pytest-asyncio pytest-cov numpy sentence-transformers
```

> **Note**: sentence-transformers requires PyTorch, which may fail on 32-bit Python or older systems. For QA testing of STORY-001 and STORY-002, only the basic dependencies are needed.

### 5. Run Tests

**Quick test:**
```powershell
.\test.bat tests/test_services/test_semantic_scholar.py tests/test_services/test_citation_manager.py -v
```

**With coverage:**
```powershell
.\test.bat tests/test_services/test_semantic_scholar.py tests/test_services/test_citation_manager.py --cov=polyhedra --cov-report=term-missing
```

## Detailed Installation

### Step-by-Step for Windows

#### 1. Verify Python Installation

```powershell
# Check all installed Python versions
py -0

# Should show something like:
#  -V:3.12 *        Python 3.12 (64-bit)
#  -V:3.11          Python 3.11 (64-bit)
```

If Python 3.11+ is not installed:
1. Download from https://www.python.org/downloads/
2. Run installer
3.  Check "Add Python to PATH"
4. Choose "Customize installation"
5.  Enable "py launcher"
6. Complete installation

#### 2. Create Isolated Environment

```powershell
# Navigate to project root
cd c:\Users\OMEN\Desktop\poly

# Create virtual environment with Python 3.12
py -3.12 -m venv .venv

# Verify creation
Test-Path .\.venv\Scripts\python.exe
# Should return: True
```

#### 3. Activate Virtual Environment

**PowerShell (if execution policy allows):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**If you get execution policy error:**
```powershell
# You don't need to activate - just use the full path to python.exe
.\.venv\Scripts\python.exe --version
```

**Command Prompt:**
```cmd
.venv\Scripts\activate.bat
```

#### 4. Install Dependencies

**Core dependencies only (for STORY-001 & STORY-002):**
```powershell
.\.venv\Scripts\pip.exe install -U pip
.\.venv\Scripts\pip.exe install httpx pydantic bibtexparser pytest pytest-asyncio pytest-cov
```

**Verify installation:**
```powershell
.\.venv\Scripts\python.exe -c "import httpx, pydantic, bibtexparser; print(' All imports successful')"
```

## Running Tests

### Using the Test Runner Script

The project includes 	est.bat for convenient test execution:

**Run all service tests:**
```powershell
.\test.bat tests/test_services/ -v
```

**Run specific story tests:**
```powershell
# STORY-001: Semantic Scholar
.\test.bat tests/test_services/test_semantic_scholar.py -v

# STORY-002: Citation Management
.\test.bat tests/test_services/test_citation_manager.py -v
```

**Run with coverage report:**
```powershell
.\test.bat tests/test_services/test_semantic_scholar.py --cov=polyhedra.services.semantic_scholar --cov-report=term-missing
```

**Run specific test class:**
```powershell
.\test.bat tests/test_services/test_citation_manager.py::TestAddCitation -v
```

**Run single test:**
```powershell
.\test.bat tests/test_services/test_semantic_scholar.py::TestGenerateBibtex::test_generate_bibtex_basic -v
```

### Manual Test Execution (without test.bat)

```powershell
# Set Python path
$env:PYTHONPATH = "c:\Users\OMEN\Desktop\poly\src"

# Run tests
.\.venv\Scripts\python.exe -m pytest tests/test_services/test_semantic_scholar.py -v
```

## Running the Services (Manual Testing)

### Test Semantic Scholar Service

```powershell
# Create a test script
@"
import asyncio
from pathlib import Path
import sys
sys.path.insert(0, 'src')

from polyhedra.services.semantic_scholar import SemanticScholarService

async def main():
    service = SemanticScholarService()
    try:
        # Search for papers
        papers = await service.search('attention mechanism', limit=3)
        print(f'Found {len(papers)} papers:')
        for paper in papers:
            print(f'  - {paper.get("title")}')
            print(f'    Authors: {", ".join(paper.get("authors", [])[:3])}')
            print(f'    Year: {paper.get("year")}')
            print(f'    BibTeX: {paper.get("bibtex_key")}')
            print()
    finally:
        await service.close()

asyncio.run(main())
