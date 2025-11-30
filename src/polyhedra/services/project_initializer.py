"""Project initialization service for research projects."""

from pathlib import Path
from typing import Any


class ProjectInitializer:
    """Handles initialization of new research projects."""

    STANDARD_DIRS = [
        "literature",
        "ideas",
        "method",
        "paper",
        ".poly/embeddings",
    ]

    CONFIG_TEMPLATE = """# Polyhedra Project Configuration
project:
  name: {name}
  created: {created}
  version: "2.0.0"

paths:
  papers: literature/papers.json
  citations: references.bib
  embeddings: .poly/embeddings/papers.pkl
"""

    def __init__(self, project_root: Path):
        """Initialize the project initializer.

        Args:
            project_root: Root directory for the project
        """
        self.root = project_root

    def initialize(self, project_name: str | None = None) -> dict[str, Any]:
        """Initialize a new research project.

        Creates standard directory structure and configuration files.
        Safe to run multiple times (idempotent).

        Args:
            project_name: Optional project name (defaults to directory name)

        Returns:
            Dict with initialization report:
            - root: Project root path
            - created_dirs: List of newly created directories
            - created_files: List of newly created files
            - existing_dirs: List of directories that already existed
            - existing_files: List of files that already existed
        """
        from datetime import datetime

        if project_name is None:
            project_name = self.root.name

        created_dirs = []
        existing_dirs = []
        created_files = []
        existing_files = []

        # Create standard directories
        for dir_path in self.STANDARD_DIRS:
            full_path = self.root / dir_path
            if full_path.exists():
                existing_dirs.append(dir_path)
            else:
                full_path.mkdir(parents=True, exist_ok=True)
                created_dirs.append(dir_path)

        # Create references.bib
        bib_file = self.root / "references.bib"
        if bib_file.exists():
            existing_files.append("references.bib")
        else:
            bib_file.write_text("", encoding="utf-8")
            created_files.append("references.bib")

        # Create .poly/config.yaml
        config_file = self.root / ".poly" / "config.yaml"
        if config_file.exists():
            existing_files.append(".poly/config.yaml")
        else:
            config_content = self.CONFIG_TEMPLATE.format(
                name=project_name,
                created=datetime.now().strftime("%Y-%m-%d"),
            )
            config_file.write_text(config_content, encoding="utf-8")
            created_files.append(".poly/config.yaml")

        return {
            "root": str(self.root),
            "created_dirs": created_dirs,
            "created_files": created_files,
            "existing_dirs": existing_dirs,
            "existing_files": existing_files,
        }
