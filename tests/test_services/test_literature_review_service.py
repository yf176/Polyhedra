"""Tests for literature review service."""

import pytest
from unittest.mock import AsyncMock, Mock

from polyhedra.services.literature_review_service import LiteratureReviewService
from polyhedra.services.llm_service import LLMService


# Sample papers for testing
SAMPLE_PAPERS = [
    {
        "title": "Attention Is All You Need",
        "authors": [{"name": "Vaswani et al."}],
        "year": 2017,
        "venue": "NeurIPS",
        "abstract": "We propose a new architecture based solely on attention mechanisms.",
        "citationCount": 50000,
        "fieldsOfStudy": ["Computer Science"]
    },
    {
        "title": "BERT: Pre-training of Deep Bidirectional Transformers",
        "authors": [{"name": "Devlin, J."}, {"name": "Chang, M."}],
        "year": 2019,
        "venue": "NAACL",
        "abstract": "We introduce BERT, which stands for Bidirectional Encoder Representations from Transformers.",
        "citationCount": 40000,
        "fieldsOfStudy": ["Computer Science", "NLP"]
    },
    {
        "title": "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale",
        "authors": [{"name": "Dosovitskiy"}, {"name": "Beyer"}, {"name": "Kolesnikov"}],
        "year": 2021,
        "venue": "ICLR",
        "abstract": "Vision Transformers (ViT) apply transformers directly to image patches.",
        "citationCount": 20000,
        "fieldsOfStudy": ["Computer Science", "Computer Vision"]
    },
]


@pytest.fixture
def mock_llm_service():
    """Create a mock LLM service."""
    service = Mock(spec=LLMService)
    service.is_configured = True
    service.estimate_tokens = Mock(return_value=5000)
    service.calculate_cost = Mock(return_value=0.15)
    service.close = AsyncMock()
    return service


@pytest.fixture
def review_service(mock_llm_service):
    """Create literature review service with mocked LLM."""
    return LiteratureReviewService(llm_service=mock_llm_service)


@pytest.fixture
def sample_review_text():
    """Sample review text for metadata extraction."""
    return """## Overview

Transformers have revolutionized natural language processing and computer vision.

## Taxonomy of Approaches

### Attention Mechanisms
The Transformer architecture [Vaswani et al., 2017] introduced self-attention.

### Language Models
BERT [Devlin and Chang, 2019] pre-trains bidirectional transformers.

### Vision Transformers
Vision Transformers [Dosovitskiy et al., 2021] apply transformers to images.

## Critical Analysis

Different approaches show various trade-offs between performance and efficiency.

## Research Gaps

- **Efficiency at Scale**: Current transformers struggle with long sequences.
- **Interpretability**: Understanding attention patterns remains challenging.
- **Transfer Learning**: Better methods for domain adaptation are needed.

## Conclusion

Transformers continue to drive progress across multiple domains.
"""


class TestLiteratureReviewService:
    """Test suite for LiteratureReviewService."""
    
    def test_initialization_with_llm_service(self, mock_llm_service):
        """Test initialization with existing LLM service."""
        service = LiteratureReviewService(llm_service=mock_llm_service)
        assert service.llm == mock_llm_service
    
    def test_initialization_creates_llm_service(self, monkeypatch):
        """Test initialization creates new LLM service if not provided."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
        service = LiteratureReviewService(provider="anthropic", api_key="test-key")
        assert service.llm is not None
    
    def test_format_authors_single(self, review_service):
        """Test author formatting with single author."""
        authors = [{"name": "John Doe"}]
        result = review_service._format_authors(authors)
        assert result == "John Doe"
    
    def test_format_authors_two(self, review_service):
        """Test author formatting with two authors."""
        authors = [{"name": "John Doe"}, {"name": "Jane Smith"}]
        result = review_service._format_authors(authors)
        assert result == "John Doe and Jane Smith"
    
    def test_format_authors_multiple(self, review_service):
        """Test author formatting with multiple authors."""
        authors = [{"name": "John Doe"}, {"name": "Jane Smith"}, {"name": "Bob Johnson"}]
        result = review_service._format_authors(authors)
        assert "et al." in result
    
    def test_format_authors_empty(self, review_service):
        """Test author formatting with empty list."""
        result = review_service._format_authors([])
        assert result == "Unknown"
    
    def test_prepare_papers_summary(self, review_service):
        """Test paper summary preparation."""
        result = review_service._prepare_papers_summary(SAMPLE_PAPERS[:2])
        assert '"title": "Attention Is All You Need"' in result
        assert '"year": 2017' in result
        assert "Vaswani et al." in result
    
    def test_build_prompt_brief(self, review_service):
        """Test prompt building for brief depth."""
        prompt = review_service._build_prompt(
            papers=SAMPLE_PAPERS,
            focus="transformers",
            structure="thematic",
            depth="brief",
            include_gaps=True
        )
        assert "transformers" in prompt
        assert str(len(SAMPLE_PAPERS)) in prompt
        assert "650 words" in prompt or "approximately 650" in prompt
        assert "Research Gaps" in prompt
        assert "thematic" in prompt.lower()
    
    def test_build_prompt_standard(self, review_service):
        """Test prompt building for standard depth."""
        prompt = review_service._build_prompt(
            papers=SAMPLE_PAPERS,
            focus=None,
            structure="chronological",
            depth="standard",
            include_gaps=False
        )
        assert "2000 words" in prompt or "approximately 2000" in prompt
        assert "Research Gaps" not in prompt
        assert "chronological" in prompt.lower()
    
    def test_build_prompt_comprehensive(self, review_service):
        """Test prompt building for comprehensive depth."""
        prompt = review_service._build_prompt(
            papers=SAMPLE_PAPERS,
            focus="vision transformers",
            structure="methodological",
            depth="comprehensive",
            include_gaps=True
        )
        assert "vision transformers" in prompt
        assert "2500 words" in prompt or "approximately 2500" in prompt
        assert "methodological" in prompt.lower()
    
    def test_extract_metadata_basic(self, review_service, sample_review_text):
        """Test metadata extraction from review."""
        metadata = review_service._extract_metadata(
            review_text=sample_review_text,
            papers=SAMPLE_PAPERS,
            include_gaps=True
        )
        
        assert metadata["word_count"] > 50
        assert len(metadata["sections"]) >= 5
        assert "Overview" in metadata["sections"]
        assert metadata["paper_count"] == len(SAMPLE_PAPERS)
        assert metadata["citations_found"] >= 3
        assert metadata["citation_coverage"] > 0
    
    def test_extract_metadata_research_gaps(self, review_service, sample_review_text):
        """Test research gaps extraction."""
        metadata = review_service._extract_metadata(
            review_text=sample_review_text,
            papers=SAMPLE_PAPERS,
            include_gaps=True
        )
        
        assert len(metadata["research_gaps"]) >= 2
        assert any("Efficiency" in gap["title"] for gap in metadata["research_gaps"])
    
    def test_extract_metadata_no_gaps(self, review_service):
        """Test metadata extraction without gaps section."""
        simple_review = """## Overview
        
This is a simple review.

## Conclusion

Summary here.
"""
        metadata = review_service._extract_metadata(
            review_text=simple_review,
            papers=SAMPLE_PAPERS[:1],
            include_gaps=False
        )
        
        assert metadata["research_gaps"] == []
        assert metadata["paper_count"] == 1
    
    @pytest.mark.asyncio
    async def test_generate_review_success(self, review_service, mock_llm_service):
        """Test successful review generation."""
        # Mock LLM response
        mock_review = """## Overview

Transformers have become dominant [Vaswani et al., 2017].

## Taxonomy of Approaches

BERT improved language understanding [Devlin and Chang, 2019].

## Conclusion

The field continues to evolve.
"""
        mock_llm_service.complete = AsyncMock(return_value=(mock_review, 5000, 2000))
        
        result = await review_service.generate_review(
            papers=SAMPLE_PAPERS,
            focus="transformers",
            structure="thematic",
            depth="brief",
            include_gaps=False
        )
        
        assert "review" in result
        assert "metadata" in result
        assert "cost" in result
        
        assert result["review"] == mock_review
        assert result["metadata"]["paper_count"] == len(SAMPLE_PAPERS)
        assert result["metadata"]["word_count"] > 0
        assert result["cost"]["input_tokens"] == 5000
        assert result["cost"]["output_tokens"] == 2000
        assert abs(result["cost"]["total_usd"] - 0.15) < 0.0001
        
        # Verify LLM was called correctly
        mock_llm_service.complete.assert_called_once()
        call_args = mock_llm_service.complete.call_args
        assert "transformers" in call_args[0][0]  # prompt contains focus
    
    @pytest.mark.asyncio
    async def test_generate_review_with_gaps(self, review_service, mock_llm_service, sample_review_text):
        """Test review generation with research gaps."""
        mock_llm_service.complete = AsyncMock(return_value=(sample_review_text, 6000, 2500))
        
        result = await review_service.generate_review(
            papers=SAMPLE_PAPERS,
            structure="thematic",
            depth="standard",
            include_gaps=True
        )
        
        assert len(result["metadata"]["research_gaps"]) > 0
        assert result["cost"]["total_tokens"] == 8500
    
    @pytest.mark.asyncio
    async def test_generate_review_empty_papers(self, review_service):
        """Test review generation with empty papers list."""
        with pytest.raises(ValueError, match="cannot be empty"):
            await review_service.generate_review(papers=[])
    
    @pytest.mark.asyncio
    async def test_generate_review_invalid_depth(self, review_service):
        """Test review generation with invalid depth."""
        with pytest.raises(ValueError, match="Depth must be one of"):
            await review_service.generate_review(
                papers=SAMPLE_PAPERS,
                depth="invalid"
            )
    
    @pytest.mark.asyncio
    async def test_generate_review_invalid_structure(self, review_service):
        """Test review generation with invalid structure."""
        with pytest.raises(ValueError, match="Structure must be"):
            await review_service.generate_review(
                papers=SAMPLE_PAPERS,
                structure="invalid"
            )
    
    @pytest.mark.asyncio
    async def test_generate_review_not_configured(self, review_service, mock_llm_service):
        """Test review generation with unconfigured LLM."""
        mock_llm_service.is_configured = False
        
        with pytest.raises(RuntimeError, match="not configured"):
            await review_service.generate_review(papers=SAMPLE_PAPERS)
    
    @pytest.mark.asyncio
    async def test_generate_review_llm_returns_none(self, review_service, mock_llm_service):
        """Test handling when LLM returns None."""
        mock_llm_service.complete = AsyncMock(return_value=None)
        
        with pytest.raises(RuntimeError, match="returned no result"):
            await review_service.generate_review(papers=SAMPLE_PAPERS)
    
    @pytest.mark.asyncio
    async def test_generate_review_different_structures(self, review_service, mock_llm_service):
        """Test all structure types."""
        mock_llm_service.complete = AsyncMock(return_value=("Review text", 5000, 2000))
        
        for structure in ["thematic", "chronological", "methodological"]:
            result = await review_service.generate_review(
                papers=SAMPLE_PAPERS,
                structure=structure,
                depth="brief"
            )
            assert result["review"] == "Review text"
    
    @pytest.mark.asyncio
    async def test_generate_review_all_depths(self, review_service, mock_llm_service):
        """Test all depth levels."""
        mock_llm_service.complete = AsyncMock(return_value=("Review text", 5000, 2000))
        
        for depth in ["brief", "standard", "comprehensive"]:
            result = await review_service.generate_review(
                papers=SAMPLE_PAPERS,
                depth=depth
            )
            assert result["metadata"]["word_count"] > 0
    
    def test_estimate_cost_brief(self, review_service):
        """Test cost estimation for brief review."""
        estimate = review_service.estimate_cost(
            paper_count=10,
            depth="brief"
        )
        
        assert estimate["paper_count"] == 10
        assert estimate["depth"] == "brief"
        assert estimate["estimated_input_tokens"] > 0
        assert estimate["estimated_output_tokens"] == 650
        assert abs(estimate["estimated_usd"] - 0.15) < 0.0001
    
    def test_estimate_cost_standard(self, review_service):
        """Test cost estimation for standard review."""
        estimate = review_service.estimate_cost(
            paper_count=50,
            depth="standard"
        )
        
        assert estimate["paper_count"] == 50
        assert estimate["estimated_output_tokens"] == 2000
        assert estimate["estimated_total_tokens"] > 2000
    
    def test_estimate_cost_comprehensive(self, review_service):
        """Test cost estimation for comprehensive review."""
        estimate = review_service.estimate_cost(
            paper_count=100,
            depth="comprehensive"
        )
        
        assert estimate["paper_count"] == 100
        assert estimate["estimated_output_tokens"] == 2500
    
    @pytest.mark.asyncio
    async def test_close(self, review_service, mock_llm_service):
        """Test service cleanup."""
        await review_service.close()
        mock_llm_service.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_review_logs_info(self, review_service, mock_llm_service, caplog):
        """Test that review generation logs appropriately."""
        mock_llm_service.complete = AsyncMock(return_value=("Review", 5000, 2000))
        
        with caplog.at_level("INFO"):
            await review_service.generate_review(papers=SAMPLE_PAPERS)
        
        assert any("Generating" in record.message for record in caplog.records)
        assert any("Generated review" in record.message for record in caplog.records)
    
    def test_depth_config(self):
        """Test depth configuration values."""
        assert "brief" in LiteratureReviewService.DEPTH_CONFIG
        assert "standard" in LiteratureReviewService.DEPTH_CONFIG
        assert "comprehensive" in LiteratureReviewService.DEPTH_CONFIG
        
        brief = LiteratureReviewService.DEPTH_CONFIG["brief"]
        assert brief["min"] < brief["target"] < brief["max"]
