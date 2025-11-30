"""Semantic Scholar API integration service."""

import asyncio
import re

import httpx

from polyhedra.schemas.paper import SemanticScholarResponse


class SemanticScholarService:
    """Service for interacting with Semantic Scholar API."""

    BASE_URL = "https://api.semanticscholar.org/graph/v1"
    MAX_RETRIES = 3
    RETRY_DELAY = 1.0  # seconds

    def __init__(self, timeout: float = 30.0):
        """Initialize the service.

        Args:
            timeout: HTTP request timeout in seconds
        """
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def search(
        self,
        query: str,
        limit: int = 20,
        year_start: int | None = None,
        year_end: int | None = None,
        fields_of_study: list[str] | None = None,
    ) -> list[dict]:
        """Search for academic papers.

        Args:
            query: Search query string
            limit: Maximum number of results (1-100, default 20)
            year_start: Start year for filtering (inclusive)
            year_end: End year for filtering (inclusive)
            fields_of_study: List of fields to filter by

        Returns:
            List of paper dictionaries with metadata

        Raises:
            httpx.HTTPError: If API request fails
            ValueError: If parameters are invalid
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        if limit < 1 or limit > 100:
            raise ValueError("Limit must be between 1 and 100")

        client = await self._get_client()

        # Build request parameters
        fields = (
            "paperId,title,authors,year,venue,abstract,citationCount,"
            "fieldsOfStudy,url,openAccessPdf"
        )
        params = {
            "query": query,
            "limit": limit,
            "fields": fields,
        }

        # Add year filter if provided
        if year_start is not None or year_end is not None:
            year_filter = ""
            if year_start:
                year_filter = str(year_start)
            if year_end:
                year_filter += f"-{year_end}" if year_filter else str(year_end)
            if year_filter:
                params["year"] = year_filter

        # Add fields of study filter
        if fields_of_study:
            params["fieldsOfStudy"] = ",".join(fields_of_study)

        # Make request with retry logic
        for attempt in range(self.MAX_RETRIES):
            try:
                response = await client.get(
                    f"{self.BASE_URL}/paper/search",
                    params=params,
                )

                if response.status_code == 429:
                    # Rate limit - wait and retry
                    delay = self.RETRY_DELAY * (2**attempt)
                    await asyncio.sleep(delay)
                    continue

                response.raise_for_status()
                data = response.json()

                # Parse and process results
                result = SemanticScholarResponse(**data)
                papers = result.data

                # Generate BibTeX for each paper
                for paper in papers:
                    if paper.get("authors") and paper.get("year"):
                        bibtex_key, bibtex_entry = self.generate_bibtex(paper)
                        paper["bibtex_key"] = bibtex_key
                        paper["bibtex_entry"] = bibtex_entry

                    # Flatten authors to list of names
                    if paper.get("authors"):
                        paper["authors"] = [
                            author["name"] if isinstance(author, dict) else author
                            for author in paper["authors"]
                        ]

                    # Handle openAccessPdf structure
                    if paper.get("openAccessPdf"):
                        pdf_data = paper["openAccessPdf"]
                        paper["pdf_url"] = (
                            pdf_data.get("url") if isinstance(pdf_data, dict) else None
                        )
                    else:
                        paper["pdf_url"] = None

                return papers

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429 and attempt < self.MAX_RETRIES - 1:
                    delay = self.RETRY_DELAY * (2**attempt)
                    await asyncio.sleep(delay)
                    continue
                raise Exception(
                    f"Semantic Scholar API error: {e.response.status_code} - {e.response.text}"
                )

            except httpx.HTTPError as e:
                if attempt < self.MAX_RETRIES - 1:
                    await asyncio.sleep(self.RETRY_DELAY)
                    continue
                raise Exception(f"HTTP error occurred: {str(e)}")

        raise Exception(f"Failed after {self.MAX_RETRIES} retries due to rate limiting")

    async def get_paper(self, paper_id: str) -> dict:
        """Get a specific paper by ID.

        Args:
            paper_id: Semantic Scholar paper ID

        Returns:
            Paper metadata dictionary

        Raises:
            httpx.HTTPError: If API request fails
            ValueError: If paper_id is invalid
        """
        if not paper_id or not paper_id.strip():
            raise ValueError("Paper ID cannot be empty")

        client = await self._get_client()

        fields = (
            "paperId,title,authors,year,venue,abstract,citationCount,"
            "fieldsOfStudy,url,openAccessPdf"
        )

        response = await client.get(
            f"{self.BASE_URL}/paper/{paper_id}",
            params={"fields": fields},
        )

        response.raise_for_status()
        paper = response.json()

        # Generate BibTeX
        if paper.get("authors") and paper.get("year"):
            bibtex_key, bibtex_entry = self.generate_bibtex(paper)
            paper["bibtex_key"] = bibtex_key
            paper["bibtex_entry"] = bibtex_entry

        # Flatten authors
        if paper.get("authors"):
            paper["authors"] = [
                author["name"] if isinstance(author, dict) else author
                for author in paper["authors"]
            ]

        # Handle PDF URL
        if paper.get("openAccessPdf"):
            pdf_data = paper["openAccessPdf"]
            paper["pdf_url"] = pdf_data.get("url") if isinstance(pdf_data, dict) else None

        return paper

    def generate_bibtex(self, paper: dict) -> tuple[str, str]:
        """Generate BibTeX key and entry from paper metadata.

        Args:
            paper: Paper metadata dictionary

        Returns:
            Tuple of (bibtex_key, bibtex_entry)
        """
        # Extract first author's last name
        authors = paper.get("authors", [])
        if not authors:
            first_author = "unknown"
        else:
            author = authors[0]
            if isinstance(author, dict):
                name = author.get("name", "unknown")
            else:
                name = author

            # Get last name (last word)
            name_parts = name.strip().split()
            first_author = name_parts[-1] if name_parts else "unknown"
            # Clean non-alphanumeric characters
            first_author = re.sub(r"[^a-zA-Z]", "", first_author).lower()

        year = paper.get("year", "")
        bibtex_key = f"{first_author}{year}"

        # Format all authors
        author_list = []
        for author in authors:
            if isinstance(author, dict):
                author_list.append(author.get("name", ""))
            else:
                author_list.append(str(author))
        authors_str = " and ".join(author_list)

        # Build BibTeX entry
        title = paper.get("title", "").replace("{", "").replace("}", "")
        venue = paper.get("venue", "")
        abstract = paper.get("abstract", "")

        # Escape special characters in abstract
        if abstract:
            abstract = abstract.replace("{", "\\{").replace("}", "\\}")
            abstract = abstract.replace("%", "\\%")

        bibtex_entry = f"""@article{{{bibtex_key},
  title = {{{title}}},
  author = {{{authors_str}}},
  year = {{{year}}},
  venue = {{{venue}}},
  abstract = {{{abstract}}}
}}"""

        return bibtex_key, bibtex_entry
