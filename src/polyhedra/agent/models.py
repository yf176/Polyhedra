"""Data models for agent orchestration framework."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class StepStatus(Enum):
    """Status of a workflow step."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class IntentType(Enum):
    """Type of research intent."""
    RESEARCH_SURVEY = "research_survey"
    PAPER_COMPARISON = "paper_comparison"
    GAP_ANALYSIS = "gap_analysis"
    CITATION_FINDING = "citation_finding"
    UNKNOWN = "unknown"


@dataclass
class Intent:
    """
    Parsed user intent.
    
    Attributes:
        type: Intent type
        topic: Main research topic
        parameters: Additional parameters
        confidence: Parsing confidence (0-1)
        raw_command: Original command text
    """
    type: IntentType
    topic: str
    parameters: Dict[str, Any]
    confidence: float
    raw_command: str


@dataclass
class WorkflowStep:
    """
    A single step in a workflow.
    
    Attributes:
        name: Step identifier
        tool: Tool to invoke
        arguments: Tool arguments (may reference previous step results)
        critical: If True, failure halts workflow
        timeout: Max execution time in seconds
        retry_count: Number of retries on failure
        description: Human-readable step description
    """
    name: str
    tool: str
    arguments: Dict[str, Any]
    critical: bool = True
    timeout: float = 60.0
    retry_count: int = 0
    description: Optional[str] = None


@dataclass
class Workflow:
    """
    A multi-step research workflow.
    
    Attributes:
        name: Workflow identifier
        description: Human-readable description
        steps: Ordered list of steps
        metadata: Additional workflow metadata
    """
    name: str
    description: str
    steps: List[WorkflowStep]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def validate(self) -> None:
        """
        Validate workflow definition.
        
        Raises:
            ValueError: If workflow is invalid
        """
        if not self.name:
            raise ValueError("Workflow name is required")
        
        if not self.steps:
            raise ValueError("Workflow must have at least one step")
        
        # Check for duplicate step names
        step_names = [step.name for step in self.steps]
        if len(step_names) != len(set(step_names)):
            raise ValueError("Workflow has duplicate step names")


@dataclass
class WorkflowState:
    """
    Current state of an executing workflow.
    
    Attributes:
        session_id: Unique session identifier
        workflow: Workflow being executed
        status: Current status (pending, running, completed, failed)
        current_step: Index of current/next step
        completed_steps: List of completed step names
        step_results: Results from each step
        errors: List of errors encountered
        started_at: Workflow start time
    """
    session_id: str
    workflow: Optional[Workflow]
    status: str = "pending"
    current_step: int = 0
    completed_steps: List[str] = field(default_factory=list)
    step_results: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)


@dataclass
class WorkflowResult:
    """
    Result of workflow execution.
    
    Attributes:
        success: Whether workflow completed successfully
        results: Results from all steps
        errors: List of errors
        message: Summary message
        elapsed_seconds: Total execution time
    """
    success: bool
    results: Dict[str, Any]
    errors: List[str]
    message: str
    elapsed_seconds: Optional[float] = None
