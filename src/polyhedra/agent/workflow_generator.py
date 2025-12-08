"""Generate workflows from parsed intents."""

import logging
from typing import Dict, Any, List
from polyhedra.agent.models import (
    Intent, IntentType, Workflow, WorkflowStep
)


class WorkflowGenerator:
    """Generate executable workflows from parsed intents."""
    
    def __init__(self):
        """Initialize workflow generator."""
        self.logger = logging.getLogger(__name__)
    
    def generate(self, intent: Intent) -> Workflow:
        """
        Generate workflow from intent.
        
        Args:
            intent: Parsed intent
            
        Returns:
            Executable workflow
            
        Raises:
            ValueError: If intent type is unknown
        """
        if intent.type == IntentType.RESEARCH_SURVEY:
            return self._generate_research_survey(intent)
        elif intent.type == IntentType.PAPER_COMPARISON:
            return self._generate_paper_comparison(intent)
        elif intent.type == IntentType.GAP_ANALYSIS:
            return self._generate_gap_analysis(intent)
        elif intent.type == IntentType.CITATION_FINDING:
            return self._generate_citation_finding(intent)
        else:
            raise ValueError(f"Cannot generate workflow for intent type: {intent.type}")
    
    def _generate_research_survey(self, intent: Intent) -> Workflow:
        """Generate research survey workflow."""
        limit = intent.parameters.get('limit', 50)
        depth = intent.parameters.get('depth', 'standard')
        structure = intent.parameters.get('structure', 'thematic')
        year_from = intent.parameters.get('year_from')
        year_to = intent.parameters.get('year_to')
        
        # Build year range parameter
        year_range = None
        if year_from and year_to:
            year_range = f"{year_from}-{year_to}"
        elif year_from:
            year_range = f"{year_from}-"
        elif year_to:
            year_range = f"-{year_to}"
        
        steps = []
        
        # Step 1: Search papers
        search_args = {
            'query': intent.topic,
            'limit': limit
        }
        if year_range:
            search_args['year_range'] = year_range
        
        steps.append(WorkflowStep(
            name='search_papers',
            tool='search_papers',
            arguments=search_args,
            critical=True,
            timeout=60.0,
            description=f"Search for {limit} papers on {intent.topic}"
        ))
        
        # Step 2: Save papers to file
        steps.append(WorkflowStep(
            name='save_papers',
            tool='save_file',
            arguments={
                'path': 'literature/papers.json',
                'content': '${search_papers.papers}'
            },
            critical=True,
            timeout=10.0,
            description='Save papers to literature/papers.json'
        ))
        
        # Step 3: Estimate review cost
        steps.append(WorkflowStep(
            name='estimate_cost',
            tool='estimate_review_cost',
            arguments={
                'paper_count': '${search_papers.count}',
                'depth': depth
            },
            critical=False,
            timeout=5.0,
            description='Estimate literature review cost'
        ))
        
        # Step 4: Generate literature review
        steps.append(WorkflowStep(
            name='generate_review',
            tool='generate_literature_review',
            arguments={
                'papers_file': 'literature/papers.json',
                'depth': depth,
                'structure': structure,
                'focus': intent.topic,
                'include_gaps': True
            },
            critical=True,
            timeout=300.0,
            retry_count=1,
            description=f"Generate {depth} literature review"
        ))
        
        # Step 5: Save review
        steps.append(WorkflowStep(
            name='save_review',
            tool='save_file',
            arguments={
                'path': f'literature-review/{intent.topic.replace(" ", "-")}.md',
                'content': '${generate_review.review}'
            },
            critical=True,
            timeout=10.0,
            description='Save literature review to file'
        ))
        
        return Workflow(
            name=f"research_survey_{intent.topic}",
            description=f"Research survey workflow for: {intent.topic}",
            steps=steps,
            metadata={
                'intent_type': intent.type.value,
                'topic': intent.topic,
                'parameters': intent.parameters
            }
        )
    
    def _generate_paper_comparison(self, intent: Intent) -> Workflow:
        """Generate paper comparison workflow."""
        topic = intent.topic
        
        steps = []
        
        # Search for papers on topic
        steps.append(WorkflowStep(
            name='search_papers',
            tool='search_papers',
            arguments={
                'query': topic,
                'limit': 20
            },
            critical=True,
            timeout=60.0,
            description=f"Search papers for comparison: {topic}"
        ))
        
        # Generate comparison review
        steps.append(WorkflowStep(
            name='generate_comparison',
            tool='generate_literature_review',
            arguments={
                'papers_file': 'literature/papers.json',
                'depth': 'standard',
                'structure': 'methodological',
                'focus': topic,
                'include_gaps': False
            },
            critical=True,
            timeout=300.0,
            description='Generate comparison analysis'
        ))
        
        return Workflow(
            name=f"paper_comparison_{topic}",
            description=f"Paper comparison workflow for: {topic}",
            steps=steps,
            metadata={
                'intent_type': intent.type.value,
                'topic': topic
            }
        )
    
    def _generate_gap_analysis(self, intent: Intent) -> Workflow:
        """Generate gap analysis workflow."""
        topic = intent.topic
        limit = intent.parameters.get('limit', 50)
        
        steps = []
        
        # Search papers
        steps.append(WorkflowStep(
            name='search_papers',
            tool='search_papers',
            arguments={
                'query': topic,
                'limit': limit
            },
            critical=True,
            timeout=60.0,
            description=f"Search {limit} papers on {topic}"
        ))
        
        # Generate review with emphasis on gaps
        steps.append(WorkflowStep(
            name='analyze_gaps',
            tool='generate_literature_review',
            arguments={
                'papers_file': 'literature/papers.json',
                'depth': 'comprehensive',
                'structure': 'thematic',
                'focus': topic,
                'include_gaps': True
            },
            critical=True,
            timeout=300.0,
            description='Analyze research gaps'
        ))
        
        return Workflow(
            name=f"gap_analysis_{topic}",
            description=f"Gap analysis workflow for: {topic}",
            steps=steps,
            metadata={
                'intent_type': intent.type.value,
                'topic': topic,
                'parameters': intent.parameters
            }
        )
    
    def _generate_citation_finding(self, intent: Intent) -> Workflow:
        """Generate citation finding workflow."""
        topic = intent.topic
        
        steps = []
        
        # Search for papers
        steps.append(WorkflowStep(
            name='search_papers',
            tool='search_papers',
            arguments={
                'query': topic,
                'limit': 10
            },
            critical=True,
            timeout=60.0,
            description=f"Find papers matching: {topic}"
        ))
        
        # Add citations to bibliography
        steps.append(WorkflowStep(
            name='add_citations',
            tool='add_citation',
            arguments={
                'papers': '${search_papers.papers}'
            },
            critical=True,
            timeout=30.0,
            description='Add citations to references.bib'
        ))
        
        return Workflow(
            name=f"citation_finding_{topic}",
            description=f"Citation finding workflow for: {topic}",
            steps=steps,
            metadata={
                'intent_type': intent.type.value,
                'topic': topic
            }
        )
