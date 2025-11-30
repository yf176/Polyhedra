"""RAG (Retrieval Augmented Generation) service for semantic paper search."""

import pickle
from pathlib import Path
from typing import Any

import numpy as np
from sentence_transformers import SentenceTransformer


class RAGService:
    """Semantic search service for academic papers using embeddings."""

    def __init__(self, project_root: Path, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize RAG service.

        Args:
            project_root: Root directory of the project
            model_name: Name of the sentence-transformers model to use
        """
        self.project_root = project_root
        self.model_name = model_name
        self.embeddings_path = project_root / ".poly" / "embeddings" / "papers.pkl"
        self._model: SentenceTransformer | None = None
        self._index: dict[str, Any] | None = None

    def _load_model(self) -> SentenceTransformer:
        """Lazy load the embedding model."""
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def _load_index(self) -> dict[str, Any]:
        """Load index from disk if not in memory."""
        if self._index is None:
            if not self.embeddings_path.exists():
                return {"embeddings": np.array([]), "metadata": []}
            with open(self.embeddings_path, "rb") as f:
                self._index = pickle.load(f)
        return self._index

    def is_indexed(self) -> bool:
        """Check if papers are indexed.

        Returns:
            True if embeddings file exists, False otherwise
        """
        return self.embeddings_path.exists()

    def index_papers(self, papers: list[dict[str, Any]]) -> int:
        """Index papers for semantic search.

        Args:
            papers: List of paper dicts with 'title' and 'abstract' fields

        Returns:
            Number of papers indexed

        Raises:
            ValueError: If papers list is empty or missing required fields
        """
        if not papers:
            raise ValueError("Cannot index empty papers list")

        model = self._load_model()

        # Prepare text for embedding (title + abstract)
        texts = []
        metadata = []
        for paper in papers:
            if "title" not in paper:
                raise ValueError("Paper missing required 'title' field")
            
            title = paper.get("title", "")
            abstract = paper.get("abstract", "")
            text = f"{title}. {abstract}".strip()
            texts.append(text)
            
            # Store metadata for retrieval
            metadata.append({
                "id": paper.get("id", ""),
                "title": title,
                "abstract": abstract,
                "authors": paper.get("authors", []),
                "year": paper.get("year", ""),
                "bibtex_key": paper.get("bibtex_key", ""),
            })

        # Generate embeddings
        embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)

        # Save to disk
        self.embeddings_path.parent.mkdir(parents=True, exist_ok=True)
        index_data = {"embeddings": embeddings, "metadata": metadata}
        
        with open(self.embeddings_path, "wb") as f:
            pickle.dump(index_data, f)

        # Update in-memory cache
        self._index = index_data

        return len(papers)

    def query(self, query_text: str, k: int = 5) -> list[dict[str, Any]]:
        """Query indexed papers with semantic search.

        Args:
            query_text: Natural language search query
            k: Number of top results to return

        Returns:
            List of dicts with paper metadata and relevance scores,
            sorted by score descending

        Raises:
            ValueError: If no papers are indexed
        """
        index = self._load_index()
        
        if len(index["embeddings"]) == 0:
            return []

        model = self._load_model()
        
        # Generate query embedding
        query_embedding = model.encode([query_text], convert_to_numpy=True)[0]

        # Calculate cosine similarities
        embeddings = index["embeddings"]
        similarities = np.dot(embeddings, query_embedding) / (
            np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding)
        )

        # Get top-k indices
        top_k = min(k, len(similarities))
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        # Build results
        results = []
        for idx in top_indices:
            result = index["metadata"][idx].copy()
            result["relevance_score"] = float(similarities[idx])
            results.append(result)

        return results
