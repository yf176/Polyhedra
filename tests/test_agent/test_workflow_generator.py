"""Tests for WorkflowGenerator."""

import pytest

from polyhedra.agent.workflow_generator import WorkflowGenerator
from polyhedra.agent.models import Intent, IntentType, Workflow, WorkflowStep


class TestWorkflowGenerator:
    """Test suite for WorkflowGenerator."""
    
    def test_initialization(self):
        """Test generator initialization."""
        generator = WorkflowGenerator()
        assert generator.logger is not None
    
    def test_generate_research_survey_workflow(self):
        """Test generating research survey workflow."""
        generator = WorkflowGenerator()
        
        intent = Intent(
            type=IntentType.RESEARCH_SURVEY,
            topic="transformers",
            parameters={'limit': 50, 'depth': 'standard', 'structure': 'thematic'},
            confidence=0.9,
            raw_command="research transformers"
        )
        
        workflow = generator.generate(intent)
        
        assert isinstance(workflow, Workflow)
        assert workflow.name == "research_survey_transformers"
        assert "transformers" in workflow.description
        assert len(workflow.steps) == 5  # search, save, estimate, generate, save
        
        # Verify steps
        assert workflow.steps[0].name == 'search_papers'
        assert workflow.steps[1].name == 'save_papers'
        assert workflow.steps[2].name == 'estimate_cost'
        assert workflow.steps[3].name == 'generate_review'
        assert workflow.steps[4].name == 'save_review'
    
    def test_generate_research_survey_with_year_range(self):
        """Test research survey workflow with year constraints."""
        generator = WorkflowGenerator()
        
        intent = Intent(
            type=IntentType.RESEARCH_SURVEY,
            topic="vision transformers",
            parameters={'limit': 30, 'year_from': 2020, 'year_to': 2023},
            confidence=0.9,
            raw_command="research vision transformers from 2020 to 2023"
        )
        
        workflow = generator.generate(intent)
        
        # Check search step has year_range
        search_step = workflow.steps[0]
        assert 'year_range' in search_step.arguments
        assert search_step.arguments['year_range'] == "2020-2023"
    
    def test_generate_paper_comparison_workflow(self):
        """Test generating paper comparison workflow."""
        generator = WorkflowGenerator()
        
        intent = Intent(
            type=IntentType.PAPER_COMPARISON,
            topic="bert vs gpt",
            parameters={},
            confidence=0.9,
            raw_command="compare BERT vs GPT"
        )
        
        workflow = generator.generate(intent)
        
        assert isinstance(workflow, Workflow)
        assert workflow.name == "paper_comparison_bert vs gpt"
        assert len(workflow.steps) == 2  # search, generate comparison
        
        # Verify methodological structure is used
        comparison_step = workflow.steps[1]
        assert comparison_step.arguments['structure'] == 'methodological'
        assert comparison_step.arguments['include_gaps'] == False
    
    def test_generate_gap_analysis_workflow(self):
        """Test generating gap analysis workflow."""
        generator = WorkflowGenerator()
        
        intent = Intent(
            type=IntentType.GAP_ANALYSIS,
            topic="multimodal learning",
            parameters={'limit': 50},
            confidence=0.9,
            raw_command="find gaps in multimodal learning"
        )
        
        workflow = generator.generate(intent)
        
        assert isinstance(workflow, Workflow)
        assert workflow.name == "gap_analysis_multimodal learning"
        assert len(workflow.steps) == 2  # search, analyze gaps
        
        # Verify comprehensive depth and gaps included
        analysis_step = workflow.steps[1]
        assert analysis_step.arguments['depth'] == 'comprehensive'
        assert analysis_step.arguments['include_gaps'] == True
    
    def test_generate_citation_finding_workflow(self):
        """Test generating citation finding workflow."""
        generator = WorkflowGenerator()
        
        intent = Intent(
            type=IntentType.CITATION_FINDING,
            topic="attention is all you need",
            parameters={},
            confidence=0.9,
            raw_command="find citations for attention is all you need"
        )
        
        workflow = generator.generate(intent)
        
        assert isinstance(workflow, Workflow)
        assert workflow.name == "citation_finding_attention is all you need"
        assert len(workflow.steps) == 2  # search, add citations
        
        # Verify steps
        assert workflow.steps[0].name == 'search_papers'
        assert workflow.steps[1].name == 'add_citations'
    
    def test_generate_unknown_intent_raises_error(self):
        """Test generating workflow for unknown intent raises error."""
        generator = WorkflowGenerator()
        
        intent = Intent(
            type=IntentType.UNKNOWN,
            topic="",
            parameters={},
            confidence=0.0,
            raw_command="unknown command"
        )
        
        with pytest.raises(ValueError, match="Cannot generate workflow"):
            generator.generate(intent)
    
    def test_workflow_metadata_includes_intent_info(self):
        """Test workflow metadata includes intent information."""
        generator = WorkflowGenerator()
        
        intent = Intent(
            type=IntentType.RESEARCH_SURVEY,
            topic="transformers",
            parameters={'depth': 'brief'},
            confidence=0.9,
            raw_command="research transformers"
        )
        
        workflow = generator.generate(intent)
        
        assert 'intent_type' in workflow.metadata
        assert workflow.metadata['intent_type'] == IntentType.RESEARCH_SURVEY.value
        assert workflow.metadata['topic'] == "transformers"
        assert workflow.metadata['parameters']['depth'] == 'brief'
    
    def test_research_survey_step_timeouts(self):
        """Test research survey steps have appropriate timeouts."""
        generator = WorkflowGenerator()
        
        intent = Intent(
            type=IntentType.RESEARCH_SURVEY,
            topic="test",
            parameters={},
            confidence=0.9,
            raw_command="research test"
        )
        
        workflow = generator.generate(intent)
        
        # Search should have 60s timeout
        assert workflow.steps[0].timeout == 60.0
        
        # Generate review should have longer timeout (300s)
        assert workflow.steps[3].timeout == 300.0
    
    def test_research_survey_critical_steps(self):
        """Test research survey marks critical steps correctly."""
        generator = WorkflowGenerator()
        
        intent = Intent(
            type=IntentType.RESEARCH_SURVEY,
            topic="test",
            parameters={},
            confidence=0.9,
            raw_command="research test"
        )
        
        workflow = generator.generate(intent)
        
        # Search, save, generate, save should be critical
        assert workflow.steps[0].critical == True
        assert workflow.steps[1].critical == True
        assert workflow.steps[3].critical == True
        assert workflow.steps[4].critical == True
        
        # Estimate cost is not critical
        assert workflow.steps[2].critical == False
    
    def test_research_survey_parameter_references(self):
        """Test research survey uses parameter references."""
        generator = WorkflowGenerator()
        
        intent = Intent(
            type=IntentType.RESEARCH_SURVEY,
            topic="test",
            parameters={},
            confidence=0.9,
            raw_command="research test"
        )
        
        workflow = generator.generate(intent)
        
        # Save papers step should reference search results
        save_step = workflow.steps[1]
        assert '${search_papers.papers}' in save_step.arguments['content']
        
        # Estimate step should reference search count
        estimate_step = workflow.steps[2]
        assert '${search_papers.count}' in estimate_step.arguments['paper_count']
