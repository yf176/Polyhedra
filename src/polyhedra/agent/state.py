"""Workflow state persistence for resume capability."""
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Any, Optional, List
import json
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class WorkflowState:
    """Persisted workflow execution state."""
    workflow_id: str
    intent: Dict[str, Any]
    workflow: Dict[str, Any]
    completed_steps: List[str]
    step_results: Dict[str, Any]
    current_step: Optional[str]
    status: str  # running, paused, completed, failed
    created_at: str
    updated_at: str
    error_count: int = 0
    last_error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkflowState":
        """Create from dictionary."""
        return cls(**data)


class StateManager:
    """Manages workflow state persistence."""
    
    def __init__(self, state_dir: Optional[Path] = None):
        self.state_dir = state_dir or Path(".polyhedra/state")
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
    def _get_state_path(self, workflow_id: str) -> Path:
        """Get path to state file.
        
        Args:
            workflow_id: Workflow identifier
            
        Returns:
            Path to state file
        """
        return self.state_dir / f"{workflow_id}.json"
        
    async def save_state(self, state: WorkflowState) -> None:
        """Persist workflow state to disk.
        
        Args:
            state: Workflow state to save
        """
        try:
            path = self._get_state_path(state.workflow_id)
            
            # Update timestamp
            state.updated_at = datetime.now().isoformat()
            
            # Convert to JSON
            data = state.to_dict()
            json_str = json.dumps(data, indent=2)
            
            # Write atomically (write to temp, then rename)
            temp_path = path.with_suffix(".tmp")
            await asyncio.to_thread(temp_path.write_text, json_str)
            await asyncio.to_thread(temp_path.replace, path)
            
            logger.debug(f"Saved state for workflow {state.workflow_id}")
            
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
            raise
            
    async def load_state(self, workflow_id: str) -> Optional[WorkflowState]:
        """Load workflow state from disk.
        
        Args:
            workflow_id: Workflow identifier
            
        Returns:
            Workflow state or None if not found
        """
        try:
            path = self._get_state_path(workflow_id)
            
            if not path.exists():
                return None
                
            # Read and parse
            json_str = await asyncio.to_thread(path.read_text)
            data = json.loads(json_str)
            
            # Validate required fields
            required = {
                "workflow_id", "intent", "workflow", "completed_steps",
                "step_results", "current_step", "status", "created_at",
                "updated_at"
            }
            if not all(field in data for field in required):
                logger.error(f"Invalid state file: {path}")
                return None
                
            state = WorkflowState.from_dict(data)
            logger.debug(f"Loaded state for workflow {workflow_id}")
            return state
            
        except Exception as e:
            logger.error(f"Failed to load state: {e}")
            return None
            
    async def delete_state(self, workflow_id: str) -> bool:
        """Delete workflow state.
        
        Args:
            workflow_id: Workflow identifier
            
        Returns:
            True if deleted, False if not found
        """
        try:
            path = self._get_state_path(workflow_id)
            
            if not path.exists():
                return False
                
            await asyncio.to_thread(path.unlink)
            logger.debug(f"Deleted state for workflow {workflow_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete state: {e}")
            return False
            
    async def list_workflows(self) -> List[str]:
        """List all workflow IDs with saved state.
        
        Returns:
            List of workflow IDs
        """
        try:
            paths = await asyncio.to_thread(
                lambda: list(self.state_dir.glob("*.json"))
            )
            return [p.stem for p in paths]
        except Exception as e:
            logger.error(f"Failed to list workflows: {e}")
            return []
            
    async def cleanup_old_states(self, days: int = 7) -> int:
        """Clean up old workflow states.
        
        Args:
            days: Delete states older than this many days
            
        Returns:
            Number of states deleted
        """
        try:
            from datetime import timedelta
            
            cutoff = datetime.now() - timedelta(days=days)
            deleted = 0
            
            for workflow_id in await self.list_workflows():
                state = await self.load_state(workflow_id)
                if not state:
                    continue
                    
                # Parse timestamp
                updated = datetime.fromisoformat(state.updated_at)
                
                # Delete if old and completed/failed
                if updated < cutoff and state.status in ["completed", "failed"]:
                    if await self.delete_state(workflow_id):
                        deleted += 1
                        
            logger.info(f"Cleaned up {deleted} old workflow states")
            return deleted
            
        except Exception as e:
            logger.error(f"Failed to cleanup states: {e}")
            return 0
            
    async def can_resume(self, workflow_id: str) -> bool:
        """Check if workflow can be resumed.
        
        Args:
            workflow_id: Workflow identifier
            
        Returns:
            True if workflow exists and is paused
        """
        state = await self.load_state(workflow_id)
        return state is not None and state.status == "paused"
