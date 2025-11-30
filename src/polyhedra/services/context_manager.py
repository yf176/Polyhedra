"""Context manager service for file operations and project status."""

from pathlib import Path
from typing import Any


class ContextManager:
    """Manages file operations and project context."""

    def __init__(self, project_root: Path):
        """Initialize context manager.

        Args:
            project_root: Root directory of the project
        """
        self.root = project_root

    def read_files(self, paths: list[str]) -> tuple[dict[str, str], list[str]]:
        """Read multiple files from project.

        Args:
            paths: List of relative paths from project root

        Returns:
            Tuple of (contents_dict, missing_files)
            - contents_dict: Map of path to file content
            - missing_files: List of paths that don't exist
        """
        contents = {}
        missing = []

        for path in paths:
            file_path = self.root / path
            if file_path.exists() and file_path.is_file():
                try:
                    contents[path] = file_path.read_text(encoding="utf-8")
                except Exception:
                    missing.append(path)
            else:
                missing.append(path)

        return contents, missing

    def write_file(self, path: str, content: str, append: bool = False) -> int:
        """Write content to file.

        Args:
            path: Relative path from project root
            content: Content to write
            append: If True, append to file; if False, overwrite

        Returns:
            Number of bytes written
        """
        file_path = self.root / path
        file_path.parent.mkdir(parents=True, exist_ok=True)

        mode = "a" if append else "w"
        with open(file_path, mode, encoding="utf-8") as f:
            bytes_written = f.write(content)

        return bytes_written

    def get_status(self) -> dict[str, Any]:
        """Get comprehensive project status.

        Returns:
            Dict with project information:
            - root: Project root path
            - papers_count: Number of papers in papers.json
            - citations_count: Number of citations in references.bib
            - rag_indexed: Whether RAG index exists
            - standard_files: Dict of standard files and their existence
        """
        status: dict[str, Any] = {
            "root": str(self.root),
            "papers_count": 0,
            "citations_count": 0,
            "rag_indexed": False,
            "standard_files": {},
        }

        # Check for papers
        papers_file = self.root / "literature" / "papers.json"
        if papers_file.exists():
            try:
                import json
                with open(papers_file, encoding="utf-8") as f:
                    papers = json.load(f)
                    status["papers_count"] = len(papers) if isinstance(papers, list) else 0
            except Exception:
                pass

        # Check for citations
        bib_file = self.root / "references.bib"
        if bib_file.exists():
            try:
                import bibtexparser
                with open(bib_file, encoding="utf-8") as f:
                    bib_db = bibtexparser.load(f)
                    status["citations_count"] = len(bib_db.entries)
            except Exception:
                pass

        # Check for RAG index
        rag_file = self.root / ".poly" / "embeddings" / "papers.pkl"
        status["rag_indexed"] = rag_file.exists()

        # Check standard files
        standard_files = [
            "literature/papers.json",
            "literature/review.md",
            "literature/gaps.md",
            "ideas/hypotheses.md",
            "method/design.md",
            "paper/abstract.md",
            "paper/introduction.md",
            "paper/related_work.md",
            "paper/method.md",
            "paper/experiments.md",
            "paper/conclusion.md",
            "references.bib",
        ]

        for file_path in standard_files:
            full_path = self.root / file_path
            status["standard_files"][file_path] = full_path.exists()

        return status
