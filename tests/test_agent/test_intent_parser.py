"""Tests for IntentParser."""

import pytest
from unittest.mock import AsyncMock, Mock

from polyhedra.agent.intent_parser import IntentParser
from polyhedra.agent.models import Intent, IntentType
from polyhedra.services.llm_service import LLMService


class TestIntentParser:
    """Test suite for IntentParser."""
    
    def test_initialization_without_llm(self):
        """Test parser initialization without LLM service."""
        parser = IntentParser()
        assert parser.llm_service is None
        assert parser.patterns is not None
    
    def test_initialization_with_llm(self):
        """Test parser initialization with LLM service."""
        llm = Mock(spec=LLMService)
        parser = IntentParser(llm_service=llm)
        assert parser.llm_service is llm
    
    @pytest.mark.asyncio
    async def test_parse_research_survey_simple(self):
        """Test parsing simple research survey command."""
        parser = IntentParser()
        intent = await parser.parse("research transformers")
        
        assert intent.type == IntentType.RESEARCH_SURVEY
        assert intent.topic == "transformers"
        assert intent.confidence == 0.9
        assert intent.raw_command == "research transformers"
    
    @pytest.mark.asyncio
    async def test_parse_research_survey_with_papers_on(self):
        """Test parsing research command with 'papers on'."""
        parser = IntentParser()
        intent = await parser.parse("research papers on attention mechanisms")
        
        assert intent.type == IntentType.RESEARCH_SURVEY
        assert intent.topic == "attention mechanisms"
    
    @pytest.mark.asyncio
    async def test_parse_find_papers(self):
        """Test parsing 'find papers' command."""
        parser = IntentParser()
        intent = await parser.parse("find papers on vision transformers")
        
        assert intent.type == IntentType.RESEARCH_SURVEY
        assert intent.topic == "vision transformers"
    
    @pytest.mark.asyncio
    async def test_parse_paper_comparison(self):
        """Test parsing paper comparison command."""
        parser = IntentParser()
        intent = await parser.parse("compare BERT vs GPT")
        
        assert intent.type == IntentType.PAPER_COMPARISON
        assert "bert" in intent.topic or "gpt" in intent.topic
    
    @pytest.mark.asyncio
    async def test_parse_gap_analysis(self):
        """Test parsing gap analysis command."""
        parser = IntentParser()
        intent = await parser.parse("find research gaps in multimodal learning")
        
        assert intent.type == IntentType.GAP_ANALYSIS
        assert intent.topic == "multimodal learning"
    
    @pytest.mark.asyncio
    async def test_parse_citation_finding(self):
        """Test parsing citation finding command."""
        parser = IntentParser()
        intent = await parser.parse("find citations for attention is all you need")
        
        assert intent.type == IntentType.CITATION_FINDING
        assert "attention" in intent.topic
    
    @pytest.mark.asyncio
    async def test_parse_extracts_paper_limit(self):
        """Test extracting paper limit from command."""
        parser = IntentParser()
        intent = await parser.parse("find 50 papers on transformers")
        
        assert intent.parameters.get('limit') == 50
    
    @pytest.mark.asyncio
    async def test_parse_extracts_depth_brief(self):
        """Test extracting brief depth parameter."""
        parser = IntentParser()
        intent = await parser.parse("research transformers brief review")
        
        assert intent.parameters.get('depth') == 'brief'
    
    @pytest.mark.asyncio
    async def test_parse_extracts_depth_comprehensive(self):
        """Test extracting comprehensive depth parameter."""
        parser = IntentParser()
        intent = await parser.parse("detailed research on transformers")
        
        assert intent.parameters.get('depth') == 'comprehensive'
    
    @pytest.mark.asyncio
    async def test_parse_extracts_structure_chronological(self):
        """Test extracting chronological structure parameter."""
        parser = IntentParser()
        intent = await parser.parse("research transformers chronological timeline")
        
        assert intent.parameters.get('structure') == 'chronological'
    
    @pytest.mark.asyncio
    async def test_parse_extracts_year_range(self):
        """Test extracting year range parameters."""
        parser = IntentParser()
        intent = await parser.parse("research transformers from 2020 to 2023")
        
        assert intent.parameters.get('year_from') == 2020
        assert intent.parameters.get('year_to') == 2023
    
    @pytest.mark.asyncio
    async def test_parse_unknown_command(self):
        """Test parsing unknown command without LLM."""
        parser = IntentParser()
        intent = await parser.parse("xyz abc def nonsense")
        
        assert intent.type == IntentType.UNKNOWN
        assert intent.confidence == 0.0
    
    @pytest.mark.asyncio
    async def test_parse_with_llm_fallback(self):
        """Test LLM fallback for unknown commands."""
        llm = Mock(spec=LLMService)
        llm.complete = AsyncMock(return_value=(
            '{"type": "research_survey", "topic": "efficient transformers", "parameters": {"depth": "standard"}}',
            100,
            50
        ))
        
        parser = IntentParser(llm_service=llm)
        intent = await parser.parse("some complex command about efficient transformers")
        
        assert intent.type == IntentType.RESEARCH_SURVEY
        assert intent.topic == "efficient transformers"
        assert intent.parameters.get('depth') == 'standard'
        assert intent.confidence == 0.8
    
    @pytest.mark.asyncio
    async def test_parse_llm_failure_returns_unknown(self):
        """Test LLM parsing failure returns unknown intent."""
        llm = Mock(spec=LLMService)
        llm.complete = AsyncMock(side_effect=Exception("API Error"))
        
        parser = IntentParser(llm_service=llm)
        intent = await parser.parse("unknown complex command")
        
        assert intent.type == IntentType.UNKNOWN
    
    @pytest.mark.asyncio
    async def test_parse_llm_invalid_json_returns_unknown(self):
        """Test LLM returning invalid JSON returns unknown."""
        llm = Mock(spec=LLMService)
        llm.complete = AsyncMock(return_value=("invalid json response", 100, 50))
        
        parser = IntentParser(llm_service=llm)
        intent = await parser.parse("unknown command")
        
        assert intent.type == IntentType.UNKNOWN
    
    def test_extract_parameters_default_values(self):
        """Test default parameter extraction."""
        parser = IntentParser()
        params = parser._extract_parameters("research transformers")
        
        assert params.get('depth') == 'standard'
        assert params.get('structure') == 'thematic'
