# STORY-V2.1-007: Agent Orchestration Framework

## Story Metadata

| Field | Value |
|-------|-------|
| **Story ID** | STORY-V2.1-007 |
| **Epic** | EPIC-V2.1-002: Custom Agent Mode & Autonomous Research Workflows |
| **Title** | Agent Orchestration Framework |
| **Priority** | P1 (High) |
| **Points** | 8 |
| **Status** | Draft |
| **Agent Model Used** | Claude Sonnet 4.5 |
| **Estimated Effort** | 3-4 days |
| **Actual Effort** | TBD |
| **Dependencies** | EPIC-V2.1-001 (Stories 001-006 complete) |

---

## User Story

**As a** researcher using Polyhedra  
**I want** an autonomous agent that can orchestrate multi-step research workflows  
**So that** I can delegate complex tasks with a single command instead of manually calling individual tools

---

## Acceptance Criteria

### AC-001: Core Agent Framework
- [ ] `ResearchAgent` class implements agent orchestration
- [ ] Supports task decomposition (breaks commands into steps)
- [ ] Maintains execution state across steps
- [ ] Provides progress reporting
- [ ] Handles async execution of tool chains

### AC-002: Tool Integration
- [ ] Agent can invoke all existing MCP tools (12 tools from Epic 1)
- [ ] Tool results flow between steps
- [ ] Tool failures are captured and handled
- [ ] Tool execution is logged for debugging

### AC-003: State Management
- [ ] `StateManager` persists workflow state to disk
- [ ] State includes: current step, completed steps, results, errors
- [ ] Agent can resume from last checkpoint on interruption
- [ ] State is stored in `.polyhedra/agent/` directory
- [ ] State is cleaned up after successful completion

### AC-004: Workflow Execution
- [ ] `WorkflowExecutor` executes step sequences
- [ ] Steps execute in dependency order
- [ ] Parallel steps execute concurrently
- [ ] Step results are accessible to subsequent steps
- [ ] Execution stops on critical failures

### AC-005: Progress & Logging
- [ ] Agent reports progress after each step
- [ ] Progress includes: step name, status, elapsed time
- [ ] Detailed logs saved to `.polyhedra/agent/logs/`
- [ ] Logs include: timestamps, tool calls, results, errors

### AC-006: Error Handling
- [ ] Agent catches tool execution errors
- [ ] Non-critical errors allow workflow to continue
- [ ] Critical errors halt execution with clear message
- [ ] Partial results preserved on failure
- [ ] Agent provides recovery suggestions

### AC-007: Testing
- [ ] Unit tests for `ResearchAgent` (>85% coverage)
- [ ] Unit tests for `StateManager` (>90% coverage)
- [ ] Unit tests for `WorkflowExecutor` (>85% coverage)
- [ ] Integration test: multi-step workflow
- [ ] Integration test: state persistence and resume
- [ ] Integration test: error handling and recovery

---

## Technical Design

### Architecture

```
src/polyhedra/
  agent/
    __init__.py
    research_agent.py      # Main agent orchestrator
    state_manager.py       # State persistence
    workflow_executor.py   # Workflow execution engine
    models.py              # Data models (Step, Workflow, State)
    exceptions.py          # Agent-specific exceptions
```

### Component Details

#### 1. ResearchAgent (`research_agent.py`)

Main orchestrator that coordinates workflow execution:

```python
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import asyncio
import logging

@dataclass
class AgentConfig:
    """Configuration for research agent."""
    max_retries: int = 3
    timeout_seconds: float = 300.0
    enable_checkpoints: bool = True
    log_level: str = "INFO"
    state_dir: str = ".polyhedra/agent"


class ResearchAgent:
    """
    Autonomous research agent that orchestrates multi-step workflows.
    
    Responsibilities:
    - Execute multi-step research workflows
    - Coordinate tool invocations
    - Manage execution state
    - Report progress
    - Handle errors gracefully
    """
    
    def __init__(
        self,
        tools: Dict[str, callable],
        config: Optional[AgentConfig] = None,
        state_manager: Optional[StateManager] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize research agent.
        
        Args:
            tools: Dictionary of tool name -> callable
            config: Agent configuration
            state_manager: State persistence manager
            logger: Logger instance
        """
        self.tools = tools
        self.config = config or AgentConfig()
        self.state_manager = state_manager or StateManager(self.config.state_dir)
        self.logger = logger or logging.getLogger(__name__)
        self.executor = WorkflowExecutor(tools, self.state_manager, self.logger)
    
    async def execute_workflow(
        self,
        workflow: Workflow,
        session_id: Optional[str] = None
    ) -> WorkflowResult:
        """
        Execute a multi-step workflow.
        
        Args:
            workflow: Workflow definition with steps
            session_id: Optional session ID for resuming
            
        Returns:
            WorkflowResult with success status and results
            
        Raises:
            WorkflowExecutionError: If workflow fails critically
        """
        # Generate or use provided session ID
        session_id = session_id or self._generate_session_id()
        
        self.logger.info(f"Starting workflow '{workflow.name}' (session: {session_id})")
        
        try:
            # Check for existing state
            state = await self.state_manager.load_state(session_id)
            if state:
                self.logger.info(f"Resuming from step {state.current_step}")
            else:
                state = WorkflowState(
                    session_id=session_id,
                    workflow=workflow,
                    status="running"
                )
            
            # Execute workflow
            result = await self.executor.execute(workflow, state)
            
            # Save final state
            if result.success:
                state.status = "completed"
                await self.state_manager.cleanup_state(session_id)
            else:
                state.status = "failed"
                await self.state_manager.save_state(state)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Workflow failed: {e}")
            raise WorkflowExecutionError(f"Workflow execution failed: {e}") from e
    
    async def resume_workflow(self, session_id: str) -> WorkflowResult:
        """
        Resume a previously interrupted workflow.
        
        Args:
            session_id: Session ID to resume
            
        Returns:
            WorkflowResult
        """
        state = await self.state_manager.load_state(session_id)
        if not state:
            raise ValueError(f"No state found for session {session_id}")
        
        self.logger.info(f"Resuming workflow (session: {session_id})")
        return await self.execute_workflow(state.workflow, session_id)
    
    async def list_sessions(self) -> List[Dict[str, Any]]:
        """
        List all active/failed sessions.
        
        Returns:
            List of session info dictionaries
        """
        return await self.state_manager.list_sessions()
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID."""
        import uuid
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        return f"{timestamp}_{unique_id}"
```

#### 2. StateManager (`state_manager.py`)

Handles state persistence to disk:

```python
from pathlib import Path
import json
import asyncio
from typing import Optional, List, Dict, Any
from datetime import datetime

class StateManager:
    """
    Manages workflow state persistence.
    
    Responsibilities:
    - Save workflow state to disk
    - Load workflow state from disk
    - List active sessions
    - Clean up completed sessions
    """
    
    def __init__(self, state_dir: str = ".polyhedra/agent"):
        """
        Initialize state manager.
        
        Args:
            state_dir: Directory for state files
        """
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
    
    async def save_state(self, state: WorkflowState) -> None:
        """
        Save workflow state to disk.
        
        Args:
            state: WorkflowState to save
        """
        state_file = self.state_dir / f"{state.session_id}.json"
        
        state_dict = {
            "session_id": state.session_id,
            "workflow_name": state.workflow.name,
            "status": state.status,
            "current_step": state.current_step,
            "completed_steps": state.completed_steps,
            "step_results": state.step_results,
            "errors": state.errors,
            "started_at": state.started_at.isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Write atomically
        temp_file = state_file.with_suffix(".tmp")
        await asyncio.to_thread(temp_file.write_text, json.dumps(state_dict, indent=2))
        await asyncio.to_thread(temp_file.rename, state_file)
    
    async def load_state(self, session_id: str) -> Optional[WorkflowState]:
        """
        Load workflow state from disk.
        
        Args:
            session_id: Session ID to load
            
        Returns:
            WorkflowState or None if not found
        """
        state_file = self.state_dir / f"{session_id}.json"
        
        if not state_file.exists():
            return None
        
        state_dict = json.loads(await asyncio.to_thread(state_file.read_text))
        
        # Reconstruct WorkflowState (workflow reconstruction TBD in Story 008)
        return WorkflowState(
            session_id=state_dict["session_id"],
            workflow=None,  # Will be reconstructed from workflow_name
            status=state_dict["status"],
            current_step=state_dict["current_step"],
            completed_steps=state_dict["completed_steps"],
            step_results=state_dict["step_results"],
            errors=state_dict["errors"],
            started_at=datetime.fromisoformat(state_dict["started_at"])
        )
    
    async def cleanup_state(self, session_id: str) -> None:
        """
        Delete state file for completed session.
        
        Args:
            session_id: Session ID to clean up
        """
        state_file = self.state_dir / f"{session_id}.json"
        if state_file.exists():
            await asyncio.to_thread(state_file.unlink)
    
    async def list_sessions(self) -> List[Dict[str, Any]]:
        """
        List all sessions with their status.
        
        Returns:
            List of session info dictionaries
        """
        sessions = []
        
        for state_file in self.state_dir.glob("*.json"):
            state_dict = json.loads(await asyncio.to_thread(state_file.read_text))
            sessions.append({
                "session_id": state_dict["session_id"],
                "workflow_name": state_dict["workflow_name"],
                "status": state_dict["status"],
                "current_step": state_dict["current_step"],
                "started_at": state_dict["started_at"],
                "updated_at": state_dict["updated_at"]
            })
        
        return sorted(sessions, key=lambda s: s["updated_at"], reverse=True)
```

#### 3. WorkflowExecutor (`workflow_executor.py`)

Executes workflow steps:

```python
from typing import Dict, Any, List
import asyncio
import time

class WorkflowExecutor:
    """
    Executes workflow steps with dependency management.
    
    Responsibilities:
    - Execute steps in dependency order
    - Run parallel steps concurrently
    - Handle step failures
    - Report progress
    """
    
    def __init__(
        self,
        tools: Dict[str, callable],
        state_manager: StateManager,
        logger: logging.Logger
    ):
        """
        Initialize workflow executor.
        
        Args:
            tools: Available tools
            state_manager: State persistence
            logger: Logger instance
        """
        self.tools = tools
        self.state_manager = state_manager
        self.logger = logger
    
    async def execute(
        self,
        workflow: Workflow,
        state: WorkflowState
    ) -> WorkflowResult:
        """
        Execute workflow steps.
        
        Args:
            workflow: Workflow to execute
            state: Current workflow state
            
        Returns:
            WorkflowResult
        """
        results = state.step_results.copy()
        errors = state.errors.copy()
        
        # Start from current step or beginning
        start_index = state.current_step if state.current_step else 0
        
        for i in range(start_index, len(workflow.steps)):
            step = workflow.steps[i]
            state.current_step = i
            
            self.logger.info(f"Executing step {i+1}/{len(workflow.steps)}: {step.name}")
            
            try:
                # Execute step
                step_start = time.time()
                result = await self._execute_step(step, results)
                step_elapsed = time.time() - step_start
                
                # Store result
                results[step.name] = result
                state.completed_steps.append(step.name)
                
                # Save state checkpoint
                await self.state_manager.save_state(state)
                
                self.logger.info(
                    f"Step '{step.name}' completed in {step_elapsed:.2f}s"
                )
                
            except Exception as e:
                error_msg = f"Step '{step.name}' failed: {e}"
                self.logger.error(error_msg)
                errors.append(error_msg)
                
                # Check if step is critical
                if step.critical:
                    return WorkflowResult(
                        success=False,
                        results=results,
                        errors=errors,
                        message=f"Critical step failed: {step.name}"
                    )
                else:
                    # Continue with non-critical failure
                    results[step.name] = {"error": str(e)}
                    continue
        
        # All steps completed
        return WorkflowResult(
            success=True,
            results=results,
            errors=errors,
            message=f"Workflow '{workflow.name}' completed successfully"
        )
    
    async def _execute_step(
        self,
        step: WorkflowStep,
        previous_results: Dict[str, Any]
    ) -> Any:
        """
        Execute a single workflow step.
        
        Args:
            step: Step to execute
            previous_results: Results from previous steps
            
        Returns:
            Step result
        """
        # Get tool
        tool = self.tools.get(step.tool)
        if not tool:
            raise ValueError(f"Tool '{step.tool}' not found")
        
        # Prepare arguments (may reference previous step results)
        args = self._prepare_arguments(step.arguments, previous_results)
        
        # Execute tool
        result = await tool(**args)
        
        return result
    
    def _prepare_arguments(
        self,
        arguments: Dict[str, Any],
        previous_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Prepare step arguments, resolving references to previous results.
        
        Args:
            arguments: Step arguments (may contain references)
            previous_results: Results from previous steps
            
        Returns:
            Resolved arguments
        """
        resolved = {}
        
        for key, value in arguments.items():
            # Check for reference syntax: ${step_name.result_key}
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                ref = value[2:-1]  # Remove ${ and }
                
                # Parse reference
                if "." in ref:
                    step_name, result_key = ref.split(".", 1)
                    resolved[key] = previous_results.get(step_name, {}).get(result_key)
                else:
                    resolved[key] = previous_results.get(ref)
            else:
                resolved[key] = value
        
        return resolved
```

#### 4. Data Models (`models.py`)

Core data structures:

```python
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


@dataclass
class WorkflowState:
    """
    Current state of an executing workflow.
    
    Attributes:
        session_id: Unique session identifier
        workflow: Workflow being executed
        status: Current status (running, completed, failed)
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
    """
    success: bool
    results: Dict[str, Any]
    errors: List[str]
    message: str
```

#### 5. Exceptions (`exceptions.py`)

Agent-specific exceptions:

```python
class AgentError(Exception):
    """Base exception for agent errors."""
    pass


class WorkflowExecutionError(AgentError):
    """Raised when workflow execution fails."""
    pass


class WorkflowValidationError(AgentError):
    """Raised when workflow definition is invalid."""
    pass


class StateLoadError(AgentError):
    """Raised when state cannot be loaded."""
    pass


class ToolNotFoundError(AgentError):
    """Raised when required tool is not available."""
    pass
```

---

## Dev Notes

### Implementation Order

1. **Models first** (`models.py`) - Define data structures
2. **State manager** (`state_manager.py`) - Implement persistence
3. **Executor** (`workflow_executor.py`) - Implement execution logic
4. **Agent** (`research_agent.py`) - Tie it all together
5. **Tests** - Unit tests for each component

### Testing Strategy

**Unit Tests** (src: tests/test_agent/):
- `test_research_agent.py` - Agent orchestration logic
- `test_state_manager.py` - State persistence
- `test_workflow_executor.py` - Step execution
- `test_models.py` - Data model validation

**Integration Tests**:
- Execute simple 2-step workflow (search → save)
- Execute workflow with error recovery
- State persistence and resume
- Parallel step execution

### Dependencies

**From Epic V2.1-001**:
- All 12 existing MCP tools
- `LLMService` (for future intent parsing in Story 008)

**New Python Packages**:
- None (uses stdlib only: asyncio, json, pathlib, dataclasses)

---

## Definition of Done

- [ ] All source files created in `src/polyhedra/agent/`
- [ ] All 7 acceptance criteria met
- [ ] Unit tests pass with >85% coverage
- [ ] Integration tests pass
- [ ] Code follows project standards
- [ ] No regressions in existing functionality
- [ ] Story marked "Ready for Review"

---

## Dev Agent Record

### Tasks
- [ ] Create `src/polyhedra/agent/` directory structure
- [ ] Implement `models.py` with all data structures
- [ ] Implement `exceptions.py` with agent exceptions
- [ ] Implement `state_manager.py` with state persistence
- [ ] Implement `workflow_executor.py` with step execution
- [ ] Implement `research_agent.py` with main orchestrator
- [ ] Create `__init__.py` with public API exports
- [ ] Write unit tests for `models.py`
- [ ] Write unit tests for `state_manager.py`
- [ ] Write unit tests for `workflow_executor.py`
- [ ] Write unit tests for `research_agent.py`
- [ ] Write integration tests
- [ ] Run all tests and verify coverage
- [ ] Update File List
- [ ] Mark story as Ready for Review

### Debug Log
<!-- Record issues and resolutions -->

### Completion Notes
<!-- Summary of delivery -->

### File List
**Files to Create:**
- `src/polyhedra/agent/__init__.py` - NEW
- `src/polyhedra/agent/research_agent.py` - NEW
- `src/polyhedra/agent/state_manager.py` - NEW
- `src/polyhedra/agent/workflow_executor.py` - NEW
- `src/polyhedra/agent/models.py` - NEW
- `src/polyhedra/agent/exceptions.py` - NEW
- `tests/test_agent/__init__.py` - NEW
- `tests/test_agent/test_research_agent.py` - NEW
- `tests/test_agent/test_state_manager.py` - NEW
- `tests/test_agent/test_workflow_executor.py` - NEW
- `tests/test_agent/test_models.py` - NEW
- `tests/test_agent/test_integration.py` - NEW

### Change Log
| Change | Description |
|--------|-------------|
| TBD | TBD |
