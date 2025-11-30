"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def mock_semantic_scholar_response():
    """Mock Semantic Scholar API response."""
    return {
        "data": [
            {
                "paperId": "test123",
                "title": "Test Paper",
                "authors": [{"name": "Test Author"}],
                "year": 2023,
                "venue": "Test Conference",
                "abstract": "Test abstract",
                "citationCount": 10,
            }
        ]
    }
