"""Tests for ResearchAgent."""

import pytest
from unittest.mock import AsyncMock, Mock

from polyhedra.agent.research_agent import ResearchAgent
from polyhedra.agent.tool_adapter import ToolAdapter
from polyhedra.agent.intent_parser import IntentParser
from polyhedra.agent.workflow_generator import WorkflowGenerator
from polyhedra.agent.models import (
    Intent, IntentType, Workflow, WorkflowStep, WorkflowResult
)


@pytest.fixture
def mock_tool_adapter():
    """Create mock tool adapter."""
    tools = {
        ''search_papers'': AsyncMock(return_value={''success'': True, ''papers'': [], ''count'': 0}),
        ''save_file'': AsyncMock(return_value={''success'': True}),
        ''estimate_review_cost'': AsyncMock(return_value={''success'': True}),
        ''generate_literature_review'': AsyncMock(return_value={''success'': True, ''review'': ''Test review''}),
    }
    return ToolAdapter(tools)


@pytest.fixture
def research_agent(mock_tool_adapter):
    """Create research agent with mocked dependencies."""
    return ResearchAgent(tool_adapter=mock_tool_adapter)


class TestResearchAgent:
    """Test suite for ResearchAgent."""
    
    def test_initialization(self, mock_tool_adapter):
        """Test agent initialization."""
        agent = ResearchAgent(tool_adapter=mock_tool_adapter)
        assert agent.tool_adapter is mock_tool_adapter
        assert isinstance(agent.intent_parser, IntentParser)
        assert isinstance(agent.workflow_generator, WorkflowGenerator)
    
    def test_initialization_with_custom_components(self, mock_tool_adapter):
        """Test initialization with custom parser and generator."""
        parser = Mock(spec=IntentParser)
        generator = Mock(spec=WorkflowGenerator)
        
        agent = ResearchAgent(
            tool_adapter=mock_tool_adapter,
            intent_parser=parser,
            workflow_generator=generator
        )
        
        assert agent.intent_parser is parser
        assert agent.workflow_generator is generator
    
    @pytest.mark.asyncio
    async def test_execute_command_success(self, research_agent):
        """Test successful command execution."""
        # Mock the parser and generator
        mock_intent = Intent(
            type=IntentType.RESEARCH_SURVEY,
            topic=''transformers'',
            parameters={},
            confidence=0.9,
            raw_command=''research transformers''
        )
        research_agent.intent_parser.parse = AsyncMock(return_value=mock_intent)
        
        result = await research_agent.execute_command(''research transformers'')
        
        assert isinstance(result, WorkflowResult)
        assert result.elapsed_seconds is not None
    
    @pytest.mark.asyncio
    async def test_execute_workflow_all_steps_succeed(self, mock_tool_adapter):
        """Test workflow execution when all steps succeed."""
        agent = ResearchAgent(tool_adapter=mock_tool_adapter)
        
        workflow = Workflow(
            name=''test_workflow'',
            description=''Test workflow'',
            steps=[
                WorkflowStep(
                    name=''step1'',
                    tool=''search_papers'',
                    arguments={''query'': ''test''},
                    critical=True
                ),
                WorkflowStep(
                    name=''step2'',
                    tool=''save_file'',
                    arguments={''path'': ''test.txt''},
                    critical=True
                ),
            ]
        )
        
        result = await agent.execute_workflow(workflow)
        
        assert result.success is True
        assert len(result.results) == 2
        assert ''step1'' in result.results
        assert ''step2'' in result.results
    
    @pytest.mark.asyncio
    async def test_execute_workflow_critical_step_fails(self, mock_tool_adapter):
        """Test workflow stops when critical step fails."""
        # Make search_papers fail
        mock_tool_adapter.tools[''search_papers''] = AsyncMock(
            return_value={''success'': False, ''error'': ''API error''}
        )
        
        agent = ResearchAgent(tool_adapter=mock_tool_adapter)
        
        workflow = Workflow(
            name=''test_workflow'',
            description=''Test'',
            steps=[
                WorkflowStep(
                    name=''step1'',
                    tool=''search_papers'',
                    arguments={},
                    critical=True
                ),
                WorkflowStep(
                    name=''step2'',
                    tool=''save_file'',
                    arguments={},
                    critical=True
                ),
            ]
        )
        
        result = await agent.execute_workflow(workflow)
        
        assert result.success is False
        assert len(result.errors) > 0
        assert ''step1'' in result.results
        assert ''step2'' not in result.results  # Should not execute
    
    @pytest.mark.asyncio
    async def test_execute_workflow_non_critical_step_fails(self, mock_tool_adapter):
        """Test workflow continues when non-critical step fails."""
        # Make estimate fail
        mock_tool_adapter.tools[''estimate_review_cost''] = AsyncMock(
            return_value={''success'': False, ''error'': ''Estimation failed''}
        )
        
        agent = ResearchAgent(tool_adapter=mock_tool_adapter)
        
        workflow = Workflow(
            name=''test_workflow'',
            description=''Test'',
            steps=[
                WorkflowStep(
                    name=''step1'',
                    tool=''search_papers'',
                    arguments={},
                    critical=True
                ),
                WorkflowStep(
                    name=''step2'',
                    tool=''estimate_review_cost'',
                    arguments={},
                    critical=False  # Non-critical
                ),
                WorkflowStep(
                    name=''step3'',
                    tool=''save_file'',
                    arguments={},
                    critical=True
                ),
            ]
        )
        
        result = await agent.execute_workflow(workflow)
        
        assert result.success is True
        assert len(result.results) == 3
        assert result.results[''step2''][''success''] is False
        assert result.results[''step3''][''success''] is True
    
    @pytest.mark.asyncio
    async def test_execute_step_tool_not_found(self, mock_tool_adapter):
        """Test step execution when tool doesn''t exist."""
        agent = ResearchAgent(tool_adapter=mock_tool_adapter)
        
        step = WorkflowStep(
            name=''test_step'',
            tool=''nonexistent_tool'',
            arguments={},
            critical=True
        )
        
        result = await agent._execute_step(step, {})
        
        assert result[''success''] is False
        assert ''not found'' in result[''error'']
    
    @pytest.mark.asyncio
    async def test_resolve_arguments_no_references(self, research_agent):
        """Test argument resolution with no references."""
        args = {
            ''query'': ''transformers'',
            ''limit'': 50,
            ''depth'': ''standard''
        }
        
        resolved = research_agent._resolve_arguments(args, {})
        
        assert resolved == args
    
    @pytest.mark.asyncio
    async def test_resolve_arguments_with_references(self, research_agent):
        """Test argument resolution with references."""
        args = {
            ''path'': ''papers.json'',
            ''content'': ''${step1.papers}'',
            ''count'': ''${step1.count}''
        }
        
        previous_results = {
            ''step1'': {
                ''papers'': [''paper1'', ''paper2''],
                ''count'': 2
            }
        }
        
        resolved = research_agent._resolve_arguments(args, previous_results)
        
        assert resolved[''path''] == ''papers.json''
        assert resolved[''content''] == [''paper1'', ''paper2'']
        assert resolved[''count''] == 2
    
    @pytest.mark.asyncio
    async def test_resolve_arguments_step_reference_only(self, research_agent):
        """Test resolving reference to entire step result."""
        args = {
            ''data'': ''${step1}''
        }
        
        previous_results = {
            ''step1'': {''papers'': [], ''count'': 0}
        }
        
        resolved = research_agent._resolve_arguments(args, previous_results)
        
        assert resolved[''data''] == {''papers'': [], ''count'': 0}
    
    @pytest.mark.asyncio
    async def test_execute_command_handles_exceptions(self, research_agent):
        """Test command execution handles exceptions gracefully."""
        # Make parser raise exception
        research_agent.intent_parser.parse = AsyncMock(side_effect=Exception(''Parse error''))
        
        result = await research_agent.execute_command(''invalid command'')
        
        assert result.success is False
        assert len(result.errors) > 0
        assert ''Parse error'' in result.errors[0]
    
    @pytest.mark.asyncio
    async def test_execute_workflow_logs_progress(self, research_agent, caplog):
        """Test workflow execution logs progress."""
        workflow = Workflow(
            name=''test_workflow'',
            description=''Test'',
            steps=[
                WorkflowStep(
                    name=''step1'',
                    tool=''search_papers'',
                    arguments={''query'': ''test''},
                    critical=True
                ),
            ]
        )
        
        with caplog.at_level(''INFO''):
            await research_agent.execute_workflow(workflow)
        
        assert any(''Executing workflow'' in record.message for record in caplog.records)
        assert any(''Step 1/1'' in record.message for record in caplog.records)
