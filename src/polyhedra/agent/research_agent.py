"""Research agent for autonomous workflow execution."""

import logging
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from polyhedra.agent.intent_parser import IntentParser
from polyhedra.agent.workflow_generator import WorkflowGenerator
from polyhedra.agent.tool_adapter import ToolAdapter
from polyhedra.agent.models import Workflow, WorkflowStep, WorkflowResult
from polyhedra.agent.retry import RetryConfig, CircuitBreaker, retry_with_backoff
from polyhedra.agent.checkpoint import CheckpointConfig, CheckpointManager, Checkpoint
from polyhedra.agent.state import StateManager, WorkflowState
from polyhedra.agent.config import AgentConfig


class ResearchAgent:
    """
    Autonomous research agent that executes multi-step workflows.
    
    Responsibilities:
    - Parse natural language commands
    - Generate appropriate workflows
    - Execute workflows step-by-step with error recovery
    - Request user approval for expensive operations
    - Persist state for resume capability
    - Report progress
    - Handle errors gracefully
    """
    
    def __init__(
        self,
        tool_adapter: ToolAdapter,
        intent_parser: Optional[IntentParser] = None,
        workflow_generator: Optional[WorkflowGenerator] = None,
        config: Optional[AgentConfig] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize research agent.
        
        Args:
            tool_adapter: Adapter for MCP tools
            intent_parser: Parser for commands (creates new if None)
            workflow_generator: Generator for workflows (creates new if None)
            config: Agent configuration (creates default if None)
            logger: Logger instance
        """
        self.tool_adapter = tool_adapter
        self.intent_parser = intent_parser or IntentParser()
        self.workflow_generator = workflow_generator or WorkflowGenerator()
        self.config = config or AgentConfig()
        self.logger = logger or logging.getLogger(__name__)
        
        # Initialize error recovery components
        self.retry_config = RetryConfig(
            max_attempts=self.config.max_retry_attempts,
            initial_delay=self.config.initial_retry_delay,
            max_delay=self.config.max_retry_delay,
            exponential_base=self.config.exponential_base,
            jitter=self.config.retry_jitter
        )
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=self.config.circuit_breaker_threshold,
            timeout=self.config.circuit_breaker_timeout
        )
        
        # Initialize checkpoint system
        checkpoint_config = CheckpointConfig(
            cost_threshold=self.config.checkpoint_cost_threshold,
            auto_approve_below=self.config.checkpoint_auto_approve_below,
            timeout=self.config.checkpoint_timeout,
            require_approval=self.config.checkpoint_enabled
        )
        cost_estimator = tool_adapter.get_tool("estimate_review_cost") \
            if tool_adapter.has_tool("estimate_review_cost") else None
        self.checkpoint_manager = CheckpointManager(checkpoint_config, cost_estimator)
        
        # Initialize state persistence
        self.state_manager = StateManager(Path(self.config.state_dir))
    
    async def execute_command(self, command: str) -> WorkflowResult:
        """
        Execute a natural language research command.
        
        Args:
            command: Natural language command
            
        Returns:
            WorkflowResult with execution results
        """
        self.logger.info(f"Executing command: {command}")
        start_time = time.time()
        
        try:
            # Parse intent
            intent = await self.intent_parser.parse(command)
            self.logger.info(f"Parsed intent: {intent.type.value}, topic: {intent.topic}")
            
            # Generate workflow
            workflow = self.workflow_generator.generate(intent)
            self.logger.info(f"Generated workflow: {workflow.name} with {len(workflow.steps)} steps")
            
            # Execute workflow
            result = await self.execute_workflow(workflow)
            
            # Add elapsed time
            result.elapsed_seconds = time.time() - start_time
            
            return result
            
        except Exception as e:
            self.logger.error(f"Command execution failed: {e}")
            elapsed = time.time() - start_time
            return WorkflowResult(
                success=False,
                results={},
                errors=[str(e)],
                message=f"Command failed: {e}",
                elapsed_seconds=elapsed
            )
    
    async def execute_workflow(self, workflow: Workflow) -> WorkflowResult:
        """
        Execute a workflow.
        
        Args:
            workflow: Workflow to execute
            
        Returns:
            WorkflowResult
        """
        self.logger.info(f"Executing workflow: {workflow.name}")
        
        results = {}
        errors = []
        
        for i, step in enumerate(workflow.steps):
            self.logger.info(f"Step {i+1}/{len(workflow.steps)}: {step.name}")
            
            try:
                step_result = await self._execute_step(step, results)
                results[step.name] = step_result
                
                if not step_result.get(''success'', False):
                    error_msg = f"Step ''{step.name}'' failed: {step_result.get(''error'', ''Unknown error'')}"
                    errors.append(error_msg)
                    
                    if step.critical:
                        self.logger.error(f"Critical step failed: {step.name}")
                        return WorkflowResult(
                            success=False,
                            results=results,
                            errors=errors,
                            message=f"Workflow failed at critical step: {step.name}"
                        )
                
            except Exception as e:
                error_msg = f"Step ''{step.name}'' raised exception: {e}"
                self.logger.error(error_msg)
                errors.append(error_msg)
                results[step.name] = {''success'': False, ''error'': str(e)}
                
                if step.critical:
                    return WorkflowResult(
                        success=False,
                        results=results,
                        errors=errors,
                        message=f"Workflow failed at step: {step.name}"
                    )
        
        # All steps completed
        return WorkflowResult(
            success=True,
            results=results,
            errors=errors,
            message=f"Workflow ''{workflow.name}'' completed successfully"
        )
    
    async def _execute_step(
        self,
        step: WorkflowStep,
        previous_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a single workflow step.
        
        Args:
            step: Step to execute
            previous_results: Results from previous steps
            
        Returns:
            Step result dictionary
        """
        # Get tool
        try:
            tool = self.tool_adapter.get_tool(step.tool)
        except KeyError:
            return {''success'': False, ''error'': f"Tool ''{step.tool}'' not found"}
        
        # Resolve arguments
        args = self._resolve_arguments(step.arguments, previous_results)
        
        # Execute tool
        try:
            result = await tool(**args)
            return result
        except Exception as e:
            self.logger.error(f"Tool ''{step.tool}'' execution failed: {e}")
            return {''success'': False, ''error'': str(e)}
    
    def _resolve_arguments(
        self,
        arguments: Dict[str, Any],
        previous_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Resolve step arguments, replacing references with actual values.
        
        Args:
            arguments: Step arguments (may contain ${references})
            previous_results: Results from previous steps
            
        Returns:
            Resolved arguments
        """
        resolved = {}
        
        for key, value in arguments.items():
            if isinstance(value, str) and value.startswith(''${'') and value.endswith(''}''):
                # Extract reference: ${step_name.result_key}
                ref = value[2:-1]
                
                if ''.'' in ref:
                    step_name, result_key = ref.split(''.'', 1)
                    step_result = previous_results.get(step_name, {})
                    resolved[key] = step_result.get(result_key)
                else:
                    resolved[key] = previous_results.get(ref)
            else:
                resolved[key] = value
        
        return resolved
