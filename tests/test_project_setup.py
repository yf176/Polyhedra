"""Basic smoke tests to verify project setup."""

import sys
from pathlib import Path


def test_imports():
    """Test that basic imports work."""
    import polyhedra

    assert polyhedra.__version__ == "2.0.0"


def test_project_structure():
    """Verify expected directories exist."""
    root = Path(__file__).parent.parent

    assert (root / "src" / "polyhedra").exists()
    assert (root / "src" / "polyhedra" / "services").exists()
    assert (root / "src" / "polyhedra" / "schemas").exists()
    assert (root / "tests").exists()
    assert (root / "pyproject.toml").exists()


def test_python_version():
    """Ensure Python version meets requirements."""
    assert sys.version_info >= (3, 11), "Python 3.11+ required"
