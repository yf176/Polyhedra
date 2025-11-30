"""Integration tests for Semantic Scholar service with live API."""

import pytest

from polyhedra.services.semantic_scholar import SemanticScholarService


@pytest.fixture
def service():
    """Create service instance."""
    return SemanticScholarService()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_live_semantic_scholar_search(service):
    """Test live search with Semantic Scholar API."""
    try:
        results = await service.search("machine learning", limit=3)

        assert len(results) > 0
        assert len(results) <= 3

        # Check first result has required fields
        paper = results[0]
        assert "paperId" in paper or "id" in paper
        assert "title" in paper
        assert "authors" in paper
        assert isinstance(paper["authors"], list)

        # Check BibTeX was generated
        if paper.get("year") and paper.get("authors"):
            assert "bibtex_key" in paper
            assert "bibtex_entry" in paper
            assert paper["bibtex_key"]  # Not empty
            assert "@article" in paper["bibtex_entry"]

    finally:
        await service.close()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_live_search_with_year_filter(service):
    """Test live search with year filtering."""
    try:
        results = await service.search("deep learning", limit=5, year_start=2020, year_end=2023)

        assert len(results) > 0

        # Verify years are within range (if year is present)
        for paper in results:
            if paper.get("year"):
                assert 2020 <= paper["year"] <= 2023, f"Year {paper['year']} out of range"

    finally:
        await service.close()


@pytest.mark.integration
@pytest.mark.skip(reason="Semantic Scholar API has rate limits (429 errors) - use for manual testing only")
@pytest.mark.asyncio
async def test_get_paper_by_id(service):
    """Test getting a specific paper by ID."""
    try:
        # Use a well-known paper ID (Attention Is All You Need)
        paper_id = "204e3073870fae3d05bcbc2f6a8e263d9b72e776"
        paper = await service.get_paper(paper_id)

        assert paper is not None
        assert paper.get("title") is not None
        assert len(paper.get("title", "")) > 0

        # Check BibTeX was generated
        if paper.get("year") and paper.get("authors"):
            assert "bibtex_key" in paper
            assert "bibtex_entry" in paper

    finally:
        await service.close()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_returns_valid_bibtex(service):
    """Test that search results include valid BibTeX."""
    try:
        results = await service.search("neural networks", limit=2)

        assert len(results) > 0

        for paper in results:
            # Papers with authors and year should have BibTeX
            if paper.get("authors") and paper.get("year"):
                bibtex_key = paper.get("bibtex_key")
                bibtex_entry = paper.get("bibtex_entry")

                assert bibtex_key, "BibTeX key should not be empty"
                assert bibtex_entry, "BibTeX entry should not be empty"

                # Check BibTeX format
                assert f"@article{{{bibtex_key}" in bibtex_entry
                assert "title = {" in bibtex_entry
                assert "author = {" in bibtex_entry
                assert "year = {" in bibtex_entry

    finally:
        await service.close()
