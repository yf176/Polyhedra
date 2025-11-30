"""Unit tests for Semantic Scholar service."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from polyhedra.services.semantic_scholar import SemanticScholarService


@pytest.fixture
def service():
    """Create service instance."""
    return SemanticScholarService()


@pytest.fixture
def mock_paper_data():
    """Mock paper data from API."""
    return {
        "paperId": "test123",
        "title": "Attention Is All You Need",
        "authors": [{"name": "Ashish Vaswani"}, {"name": "Noam Shazeer"}],
        "year": 2017,
        "venue": "NeurIPS",
        "abstract": (
            "The dominant sequence transduction models are based on "
            "complex recurrent or convolutional neural networks."
        ),
        "citationCount": 50000,
        "fieldsOfStudy": ["Computer Science"],
        "url": "https://semanticscholar.org/paper/test123",
        "openAccessPdf": {"url": "https://arxiv.org/pdf/1706.03762.pdf"},
    }


@pytest.fixture
def mock_search_response(mock_paper_data):
    """Mock search API response."""
    return {"total": 1000, "offset": 0, "next": 20, "data": [mock_paper_data]}


class TestGenerateBibtex:
    """Tests for BibTeX generation."""

    def test_generate_bibtex_basic(self, service):
        """Test basic BibTeX generation."""
        paper = {
            "title": "Attention Is All You Need",
            "authors": [{"name": "Ashish Vaswani"}],
            "year": 2017,
            "venue": "NeurIPS",
            "abstract": "Test abstract",
        }
        key, entry = service.generate_bibtex(paper)

        assert key == "vaswani2017"
        assert "@article{vaswani2017" in entry
        assert "Attention Is All You Need" in entry
        assert "Ashish Vaswani" in entry
        assert "2017" in entry
        assert "NeurIPS" in entry

    def test_generate_bibtex_multiple_authors(self, service):
        """Test BibTeX with multiple authors."""
        paper = {
            "title": "Test Paper",
            "authors": [{"name": "John Doe"}, {"name": "Jane Smith"}],
            "year": 2023,
            "venue": "ICML",
        }
        key, entry = service.generate_bibtex(paper)

        assert key == "doe2023"
        assert "John Doe and Jane Smith" in entry

    def test_generate_bibtex_no_authors(self, service):
        """Test BibTeX generation with no authors."""
        paper = {"title": "Test Paper", "authors": [], "year": 2023, "venue": "ICML"}
        key, entry = service.generate_bibtex(paper)

        assert key == "unknown2023"
        assert "@article{unknown2023" in entry

    def test_generate_bibtex_special_characters(self, service):
        """Test BibTeX with special characters."""
        paper = {
            "title": "Test {Paper}",
            "authors": [{"name": "O'Brien"}],
            "year": 2023,
            "venue": "Test",
            "abstract": "Abstract with % and {braces}",
        }
        key, entry = service.generate_bibtex(paper)

        # Special chars should be escaped
        assert "\\%" in entry
        assert "\\{" in entry or "\\}" in entry

    def test_generate_bibtex_string_authors(self, service):
        """Test BibTeX with author names as strings."""
        paper = {
            "title": "Test Paper",
            "authors": ["John Doe", "Jane Smith"],
            "year": 2023,
            "venue": "ICML",
        }
        key, entry = service.generate_bibtex(paper)

        assert "John Doe and Jane Smith" in entry


class TestSearch:
    """Tests for paper search."""

    @pytest.mark.asyncio
    async def test_search_basic(self, service, mock_search_response):
        """Test basic search functionality."""
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_search_response
        mock_client.get.return_value = mock_response

        service._client = mock_client

        results = await service.search("transformers", limit=5)

        assert len(results) == 1
        assert results[0]["title"] == "Attention Is All You Need"
        assert "bibtex_key" in results[0]
        assert results[0]["bibtex_key"] == "vaswani2017"
        assert isinstance(results[0]["authors"], list)
        assert results[0]["authors"][0] == "Ashish Vaswani"

    @pytest.mark.asyncio
    async def test_search_with_year_filter(self, service, mock_search_response):
        """Test search with year filtering."""
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_search_response
        mock_client.get.return_value = mock_response

        service._client = mock_client

        await service.search("vision", limit=5, year_start=2020, year_end=2023)

        # Verify year parameter was passed
        call_args = mock_client.get.call_args
        assert "year" in call_args.kwargs["params"]
        assert call_args.kwargs["params"]["year"] == "2020-2023"

    @pytest.mark.asyncio
    async def test_search_year_start_only(self, service, mock_search_response):
        """Test search with only year_start."""
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_search_response
        mock_client.get.return_value = mock_response

        service._client = mock_client

        await service.search("test", year_start=2020)

        call_args = mock_client.get.call_args
        assert call_args.kwargs["params"]["year"] == "2020"

    @pytest.mark.asyncio
    async def test_search_empty_query(self, service):
        """Test search with empty query raises error."""
        with pytest.raises(ValueError, match="Query cannot be empty"):
            await service.search("")

    @pytest.mark.asyncio
    async def test_search_invalid_limit(self, service):
        """Test search with invalid limit raises error."""
        with pytest.raises(ValueError, match="Limit must be between 1 and 100"):
            await service.search("test", limit=0)

        with pytest.raises(ValueError, match="Limit must be between 1 and 100"):
            await service.search("test", limit=101)

    @pytest.mark.asyncio
    async def test_search_rate_limit_retry(self, service, mock_search_response):
        """Test retry logic on rate limit."""
        mock_client = AsyncMock()

        # First call returns 429, second succeeds
        rate_limit_response = MagicMock()
        rate_limit_response.status_code = 429

        success_response = MagicMock()
        success_response.status_code = 200
        success_response.json.return_value = mock_search_response

        mock_client.get.side_effect = [rate_limit_response, success_response]
        service._client = mock_client

        with patch("asyncio.sleep"):
            results = await service.search("test")

        assert len(results) == 1
        assert mock_client.get.call_count == 2

    @pytest.mark.asyncio
    async def test_search_http_error(self, service):
        """Test handling of HTTP errors."""
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server error", request=MagicMock(), response=mock_response
        )
        mock_client.get.return_value = mock_response

        service._client = mock_client

        with pytest.raises(Exception, match="Semantic Scholar API error"):
            await service.search("test")


class TestGetPaper:
    """Tests for getting individual papers."""

    @pytest.mark.asyncio
    async def test_get_paper_by_id(self, service, mock_paper_data):
        """Test getting paper by ID."""
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_paper_data
        mock_client.get.return_value = mock_response

        service._client = mock_client

        paper = await service.get_paper("test123")

        assert paper["title"] == "Attention Is All You Need"
        assert "bibtex_key" in paper
        assert paper["bibtex_key"] == "vaswani2017"

    @pytest.mark.asyncio
    async def test_get_paper_empty_id(self, service):
        """Test getting paper with empty ID raises error."""
        with pytest.raises(ValueError, match="Paper ID cannot be empty"):
            await service.get_paper("")

    @pytest.mark.asyncio
    async def test_get_paper_not_found(self, service):
        """Test handling of paper not found."""
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not found", request=MagicMock(), response=mock_response
        )
        mock_client.get.return_value = mock_response

        service._client = mock_client

        with pytest.raises(httpx.HTTPStatusError):
            await service.get_paper("nonexistent")


class TestClientManagement:
    """Tests for HTTP client management."""

    @pytest.mark.asyncio
    async def test_client_creation(self, service):
        """Test client is created on first use."""
        assert service._client is None
        client = await service._get_client()
        assert client is not None
        assert isinstance(client, httpx.AsyncClient)

    @pytest.mark.asyncio
    async def test_client_reuse(self, service):
        """Test client is reused."""
        client1 = await service._get_client()
        client2 = await service._get_client()
        assert client1 is client2

    @pytest.mark.asyncio
    async def test_close(self, service):
        """Test client cleanup."""
        await service._get_client()
        assert service._client is not None

        await service.close()
        assert service._client is None
