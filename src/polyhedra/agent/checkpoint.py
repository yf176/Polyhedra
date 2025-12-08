"""Checkpoint system for user approval before expensive operations."""
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


@dataclass
class CheckpointConfig:
    """Configuration for checkpoint behavior."""
    cost_threshold: float = 0.50  # USD
    require_approval: bool = True
    auto_approve_below: float = 0.10  # Auto-approve if < $0.10
    timeout: float = 300.0  # 5 minutes to respond


@dataclass
class Checkpoint:
    """Represents a checkpoint in workflow execution."""
    step_name: str
    operation: str
    estimated_cost: float
    rationale: str
    auto_approved: bool = False
    user_approved: Optional[bool] = None
    
    def __str__(self) -> str:
        """Format checkpoint for display."""
        return (
            f"Checkpoint: {self.step_name}\n"
            f"  Operation: {self.operation}\n"
            f"  Estimated Cost: ${self.estimated_cost:.2f}\n"
            f"  Rationale: {self.rationale}"
        )


class CheckpointManager:
    """Manages workflow checkpoints for user approval."""
    
    def __init__(
        self,
        config: CheckpointConfig,
        cost_estimator: Optional[Any] = None
    ):
        self.config = config
        self.cost_estimator = cost_estimator
        self.checkpoints: List[Checkpoint] = []
        
    async def should_checkpoint(
        self,
        operation: str,
        context: Dict[str, Any]
    ) -> bool:
        """Determine if operation requires checkpoint.
        
        Args:
            operation: Name of the operation
            context: Context for cost estimation
            
        Returns:
            True if checkpoint is needed
        """
        if not self.config.require_approval:
            return False
            
        # If no cost estimator, checkpoint all expensive-looking operations
        if not self.cost_estimator:
            expensive_ops = {
                "generate_literature_review",
                "index_papers",
                "query_similar_papers"
            }
            return operation in expensive_ops
            
        # Use cost estimator
        try:
            cost = await self._estimate_cost(operation, context)
            return cost >= self.config.cost_threshold
        except Exception as e:
            logger.warning(f"Cost estimation failed: {e}. Checkpointing by default.")
            return True
            
    async def _estimate_cost(
        self,
        operation: str,
        context: Dict[str, Any]
    ) -> float:
        """Estimate cost of operation.
        
        Args:
            operation: Name of the operation
            context: Context for estimation
            
        Returns:
            Estimated cost in USD
        """
        if not self.cost_estimator:
            return 0.0
            
        # Map operation to cost estimation
        if operation == "generate_literature_review":
            return await self.cost_estimator(
                context.get("paper_count", 10),
                context.get("depth", "standard")
            )
        elif operation == "index_papers":
            # Embedding costs (rough estimate)
            paper_count = context.get("paper_count", 0)
            return paper_count * 0.0001  # ~$0.0001 per paper
        else:
            return 0.0
            
    async def request_approval(self, checkpoint: Checkpoint) -> bool:
        """Request user approval for checkpoint.
        
        Args:
            checkpoint: Checkpoint to request approval for
            
        Returns:
            True if approved, False if denied
        """
        self.checkpoints.append(checkpoint)
        
        # Auto-approve small costs
        if checkpoint.estimated_cost < self.config.auto_approve_below:
            checkpoint.auto_approved = True
            logger.info(
                f"Auto-approved checkpoint '{checkpoint.step_name}' "
                f"(cost ${checkpoint.estimated_cost:.2f})"
            )
            return True
            
        # Format approval prompt
        prompt = self._format_approval_prompt(checkpoint)
        logger.info(f"Checkpoint approval required:\n{prompt}")
        
        # Get user approval (stub for IDE integration)
        approved = await self._get_user_approval(prompt, self.config.timeout)
        checkpoint.user_approved = approved
        
        if approved:
            logger.info(f"Checkpoint '{checkpoint.step_name}' approved")
        else:
            logger.warning(f"Checkpoint '{checkpoint.step_name}' denied")
            
        return approved
        
    def _format_approval_prompt(self, checkpoint: Checkpoint) -> str:
        """Format checkpoint for user approval.
        
        Args:
            checkpoint: Checkpoint to format
            
        Returns:
            Formatted prompt string
        """
        return (
            f"\n{'='*60}\n"
            f"CHECKPOINT APPROVAL REQUIRED\n"
            f"{'='*60}\n"
            f"{checkpoint}\n"
            f"{'='*60}\n"
            f"Approve this operation? (y/n): "
        )
        
    async def _get_user_approval(
        self,
        prompt: str,
        timeout: float
    ) -> bool:
        """Get user approval (stub for IDE integration).
        
        In production, this will integrate with IDE approval mechanisms.
        For now, auto-approve in testing/development.
        
        Args:
            prompt: Approval prompt to display
            timeout: Timeout in seconds
            
        Returns:
            True if approved
        """
        # TODO: Integrate with IDE approval mechanism in Story V2.1-011
        # For now, log the prompt and auto-approve
        logger.info(
            "User approval requested (auto-approving in development mode)"
        )
        return True
        
    def get_checkpoint_history(self) -> List[Checkpoint]:
        """Get history of all checkpoints.
        
        Returns:
            List of checkpoints in chronological order
        """
        return self.checkpoints.copy()
        
    def clear_history(self) -> None:
        """Clear checkpoint history."""
        self.checkpoints.clear()
