"""Polyhedra MCP Server - Academic research tool server."""

__version__ = "2.0.0"

# Lazy import to avoid MCP dependency during testing
def main():
    from polyhedra.server import main as _main
    return _main()

__all__ = ["main", "__version__"]
