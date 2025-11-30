"""Unit tests for RAG service."""

import tempfile
from pathlib import Path

import numpy as np
import pytest

from polyhedra.services.rag_service import RAGService


@pytest.fixture
def temp_dir():
    """Create temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def rag_service(temp_dir):
    """Create RAG service instance."""
    return RAGService(temp_dir)


@pytest.fixture
def sample_papers():
    """Sample papers for testing."""
    return [
        {
            "id": "paper1",
            "title": "Attention Is All You Need",
            "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks.",
            "authors": ["Vaswani"],
            "year": "2017",
            "bibtex_key": "vaswani2017attention",
        },
        {
            "id": "paper2",
            "title": "BERT: Pre-training of Deep Bidirectional Transformers",
            "abstract": "We introduce a new language representation model called BERT.",
            "authors": ["Devlin"],
            "year": "2019",
            "bibtex_key": "devlin2019bert",
        },
        {
            "id": "paper3",
            "title": "ImageNet Classification with Deep Convolutional Neural Networks",
            "abstract": "We trained a large deep convolutional neural network to classify images.",
            "authors": ["Krizhevsky"],
            "year": "2012",
            "bibtex_key": "krizhevsky2012imagenet",
        },
    ]


class TestIndexing:
    """Tests for paper indexing."""

    def test_index_papers_success(self, rag_service, sample_papers, temp_dir):
        """Test successful paper indexing."""
        count = rag_service.index_papers(sample_papers)
        
        assert count == 3
        assert (temp_dir / ".poly" / "embeddings" / "papers.pkl").exists()
        assert rag_service.is_indexed()

    def test_index_creates_directory(self, rag_service, sample_papers, temp_dir):
        """Test that indexing creates directory if missing."""
        embeddings_dir = temp_dir / ".poly" / "embeddings"
        assert not embeddings_dir.exists()
        
        rag_service.index_papers(sample_papers)
        assert embeddings_dir.exists()

    def test_index_empty_papers(self, rag_service):
        """Test indexing empty list raises error."""
        with pytest.raises(ValueError, match="Cannot index empty"):
            rag_service.index_papers([])

    def test_index_missing_title(self, rag_service):
        """Test indexing paper without title raises error."""
        papers = [{"abstract": "Some abstract"}]
        with pytest.raises(ValueError, match="missing required 'title'"):
            rag_service.index_papers(papers)

    def test_is_indexed_before_indexing(self, rag_service):
        """Test is_indexed returns False before indexing."""
        assert not rag_service.is_indexed()

    def test_is_indexed_after_indexing(self, rag_service, sample_papers):
        """Test is_indexed returns True after indexing."""
        rag_service.index_papers(sample_papers)
        assert rag_service.is_indexed()


class TestQuerying:
    """Tests for semantic querying."""

    def test_query_returns_top_k(self, rag_service, sample_papers):
        """Test query returns exactly k results."""
        rag_service.index_papers(sample_papers)
        results = rag_service.query("transformers", k=2)
        assert len(results) == 2

    def test_query_relevance_order(self, rag_service, sample_papers):
        """Test results are ordered by relevance."""
        rag_service.index_papers(sample_papers)
        results = rag_service.query("attention mechanisms transformers", k=3)
        
        # Should find transformer papers first
        assert "attention" in results[0]["title"].lower() or "transformer" in results[0]["title"].lower()
        
        # Scores should be descending
        scores = [r["relevance_score"] for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_query_similarity_scores(self, rag_service, sample_papers):
        """Test similarity scores are in valid range."""
        rag_service.index_papers(sample_papers)
        results = rag_service.query("neural networks", k=3)
        
        for result in results:
            assert 0.0 <= result["relevance_score"] <= 1.0

    def test_query_before_indexing(self, rag_service):
        """Test query before indexing returns empty list."""
        results = rag_service.query("test query")
        assert results == []

    def test_query_with_large_k(self, rag_service, sample_papers):
        """Test query with k larger than number of papers."""
        rag_service.index_papers(sample_papers)
        results = rag_service.query("test", k=100)
        assert len(results) == 3

    def test_query_result_structure(self, rag_service, sample_papers):
        """Test query results have expected structure."""
        rag_service.index_papers(sample_papers)
        results = rag_service.query("transformers", k=1)
        
        result = results[0]
        assert "id" in result
        assert "title" in result
        assert "abstract" in result
        assert "authors" in result
        assert "year" in result
        assert "bibtex_key" in result
        assert "relevance_score" in result


class TestPersistence:
    """Tests for embedding persistence."""

    def test_load_existing_index(self, sample_papers, temp_dir):
        """Test loading index from disk."""
        # Create and index
        service1 = RAGService(temp_dir)
        service1.index_papers(sample_papers)
        
        # Create new instance and query without indexing
        service2 = RAGService(temp_dir)
        results = service2.query("transformers", k=2)
        
        assert len(results) == 2
        assert results[0]["title"]

    def test_reindex_replaces_old(self, rag_service, sample_papers):
        """Test re-indexing replaces old embeddings."""
        # Initial index
        rag_service.index_papers(sample_papers[:2])
        results1 = rag_service.query("test", k=10)
        assert len(results1) == 2
        
        # Re-index with all papers
        rag_service.index_papers(sample_papers)
        results2 = rag_service.query("test", k=10)
        assert len(results2) == 3
