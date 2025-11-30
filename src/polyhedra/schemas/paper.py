"""Pydantic schemas for academic papers."""

from typing import Any

from pydantic import BaseModel, Field


class Author(BaseModel):
    """Author information."""

    name: str
    author_id: str | None = Field(None, alias="authorId")


class Paper(BaseModel):
    """Academic paper model."""

    model_config = {"populate_by_name": True}

    id: str = Field(..., alias="paperId")
    title: str
    authors: list[str]
    year: int | None = None
    venue: str | None = None
    abstract: str | None = None
    citation_count: int = Field(0, alias="citationCount")
    bibtex_key: str = ""
    bibtex_entry: str = ""
    url: str | None = None
    pdf_url: str | None = Field(None, alias="openAccessPdf")
    fields_of_study: list[str] = Field(default_factory=list, alias="fieldsOfStudy")


class SemanticScholarResponse(BaseModel):
    """Response from Semantic Scholar API."""

    total: int | None = None
    offset: int = 0
    next_offset: int | None = Field(None, alias="next")
    data: list[dict[str, Any]]
