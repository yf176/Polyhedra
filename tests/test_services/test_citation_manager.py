"""Unit tests for CitationManager service."""

import tempfile
from pathlib import Path

import pytest

from polyhedra.services.citation_manager import CitationManager


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def citation_manager(temp_dir):
    return CitationManager(temp_dir)


@pytest.fixture
def sample_bibtex():
    return '''@article{vaswani2017attention,
  title={Attention is All You Need},
  author={Vaswani, Ashish and Shazeer, Noam and Parmar, Niki},
  year={2017},
  venue={NeurIPS}
}'''


@pytest.fixture
def sample_bibtex2():
    return '''@article{devlin2019bert,
  title={BERT: Pre-training of Deep Bidirectional Transformers},
  author={Devlin, Jacob and Chang, Ming-Wei and Lee, Kenton},
  year={2019},
  journal={NAACL}
}'''


class TestAddCitation:

    def test_add_citation_new(self, citation_manager, sample_bibtex, temp_dir):
        key, added = citation_manager.add_entry(sample_bibtex)
        assert key == "vaswani2017attention"
        assert added is True
        assert (temp_dir / "references.bib").exists()

    def test_add_citation_duplicate(self, citation_manager, sample_bibtex):
        key1, added1 = citation_manager.add_entry(sample_bibtex)
        key2, added2 = citation_manager.add_entry(sample_bibtex)
        assert key1 == key2 == "vaswani2017attention"
        assert added1 is True
        assert added2 is False
        assert len(citation_manager.get_all_keys()) == 1

    def test_invalid_bibtex(self, citation_manager):
        with pytest.raises(ValueError, match="No valid BibTeX entries"):
            citation_manager.add_entry("not valid bibtex")


class TestGetAllKeys:

    def test_get_all_keys_empty(self, citation_manager):
        assert citation_manager.get_all_keys() == []

    def test_get_all_keys_multiple(self, citation_manager, sample_bibtex, sample_bibtex2):
        citation_manager.add_entry(sample_bibtex)
        citation_manager.add_entry(sample_bibtex2)
        keys = citation_manager.get_all_keys()
        assert len(keys) == 2
        assert "devlin2019bert" in keys
        assert "vaswani2017attention" in keys


class TestGetAllEntries:

    def test_get_all_entries_empty(self, citation_manager):
        assert citation_manager.get_all_entries() == []

    def test_get_all_entries_single(self, citation_manager, sample_bibtex):
        citation_manager.add_entry(sample_bibtex)
        entries = citation_manager.get_all_entries()
        assert len(entries) == 1
        entry = entries[0]
        assert entry["key"] == "vaswani2017attention"
        assert entry["title"] == "Attention is All You Need"
        assert "Vaswani" in entry["author"]
        assert entry["year"] == "2017"
