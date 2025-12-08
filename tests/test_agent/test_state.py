"""Tests for state persistence."""
import pytest
from pathlib import Path
import tempfile
import shutil
from polyhedra.agent.state import StateManager, WorkflowState
from datetime import datetime


@pytest.fixture
def temp_state_dir():
    """Create temporary state directory."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.mark.asyncio
async def test_save_and_load_state(temp_state_dir):
    """Test saving and loading workflow state."""
    manager = StateManager(temp_state_dir)
    
    state = WorkflowState(
        workflow_id="test-123",
        intent={"type": "research_survey"},
        workflow={"name": "test"},
        completed_steps=["step1"],
        step_results={"step1": {"success": True}},
        current_step="step2",
        status="running",
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    
    await manager.save_state(state)
    loaded = await manager.load_state("test-123")
    
    assert loaded is not None
    assert loaded.workflow_id == "test-123"
    assert loaded.status == "running"
    assert len(loaded.completed_steps) == 1


@pytest.mark.asyncio
async def test_delete_state(temp_state_dir):
    """Test deleting workflow state."""
    manager = StateManager(temp_state_dir)
    
    state = WorkflowState(
        workflow_id="test-456",
        intent={},
        workflow={},
        completed_steps=[],
        step_results={},
        current_step=None,
        status="completed",
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    
    await manager.save_state(state)
    deleted = await manager.delete_state("test-456")
    assert deleted
    
    loaded = await manager.load_state("test-456")
    assert loaded is None


@pytest.mark.asyncio
async def test_list_workflows(temp_state_dir):
    """Test listing all workflows."""
    manager = StateManager(temp_state_dir)
    
    for i in range(3):
        state = WorkflowState(
            workflow_id=f"wf-{i}",
            intent={},
            workflow={},
            completed_steps=[],
            step_results={},
            current_step=None,
            status="running",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        await manager.save_state(state)
    
    workflows = await manager.list_workflows()
    assert len(workflows) == 3
    assert "wf-0" in workflows
