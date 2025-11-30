"""Citation management service for BibTeX references."""

from pathlib import Path
from typing import Any

import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter


class CitationManager:
    """Manages BibTeX citations in references.bib file."""

    def __init__(self, project_root: Path):
        """Initialize citation manager.

        Args:
            project_root: Root directory containing references.bib
        """
        self.bib_path = project_root / "references.bib"

    def load(self) -> BibDatabase:
        """Load BibTeX library from file.

        Returns:
            BibDatabase object with entries
        """
        if not self.bib_path.exists():
            return BibDatabase()

        with open(self.bib_path, encoding="utf-8") as bib_file:
            return bibtexparser.load(bib_file)

    def save(self, library: BibDatabase) -> None:
        """Save BibTeX library to file.

        Args:
            library: BibDatabase object to save
        """
        writer = BibTexWriter()
        writer.indent = "  "
        writer.order_entries_by = None

        with open(self.bib_path, "w", encoding="utf-8") as bib_file:
            bib_file.write(writer.write(library))

    def add_entry(self, bibtex_str: str) -> tuple[str, bool]:
        """Add a citation entry from BibTeX string.

        Args:
            bibtex_str: Valid BibTeX entry as string

        Returns:
            Tuple of (citation_key, was_added)

        Raises:
            ValueError: If BibTeX string is invalid
        """
        try:
            parsed_db = bibtexparser.loads(bibtex_str)
        except Exception as e:
            raise ValueError(f"Invalid BibTeX format: {e}") from e

        if not parsed_db.entries:
            raise ValueError("No valid BibTeX entries found in input")

        new_entry = parsed_db.entries[0]
        citation_key = new_entry.get("ID")

        if not citation_key:
            raise ValueError("BibTeX entry missing required ID field")

        library = self.load()
        existing_keys = {entry.get("ID") for entry in library.entries}

        if citation_key in existing_keys:
            return (citation_key, False)

        library.entries.append(new_entry)
        self.save(library)

        return (citation_key, True)

    def get_all_keys(self) -> list[str]:
        """Get all citation keys from references.bib.

        Returns:
            Sorted list of citation keys
        """
        library = self.load()
        keys = [entry.get("ID", "") for entry in library.entries if entry.get("ID")]
        return sorted(keys)

    def get_all_entries(self) -> list[dict[str, Any]]:
        """Get all citation entries with metadata.

        Returns:
            List of dicts with key, title, authors, year, etc.
        """
        library = self.load()
        entries = []

        for entry in library.entries:
            entry_dict: dict[str, Any] = {
                "key": entry.get("ID", ""),
                "type": entry.get("ENTRYTYPE", "misc"),
                "title": entry.get("title", ""),
                "author": entry.get("author", ""),
                "year": entry.get("year", ""),
            }

            optional = ["journal", "booktitle", "venue", "url", "doi", "pages"]
            for field in optional:
                if field in entry:
                    entry_dict[field] = entry[field]

            entries.append(entry_dict)

        return entries
