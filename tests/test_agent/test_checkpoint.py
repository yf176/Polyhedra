"""Tests for checkpoint system."""
import pytest
from polyhedra.agent.checkpoint import CheckpointConfig, CheckpointManager, Checkpoint


@pytest.mark.asyncio
async def test_checkpoint_auto_approve_small_cost():
    """Test auto-approval for small costs."""
    config = CheckpointConfig(auto_approve_below=0.10)
    manager = CheckpointManager(config)
    
    checkpoint = Checkpoint(
        step_name="test",
        operation="test_op",
        estimated_cost=0.05,
        rationale="Small cost"
    )
    
    approved = await manager.request_approval(checkpoint)
    assert approved
    assert checkpoint.auto_approved


@pytest.mark.asyncio
async def test_checkpoint_requires_approval_large_cost():
    """Test approval required for large costs."""
    config = CheckpointConfig(cost_threshold=0.50)
    manager = CheckpointManager(config)
    
    # In development mode, auto-approves
    checkpoint = Checkpoint(
        step_name="test",
        operation="test_op",
        estimated_cost=1.00,
        rationale="Large cost"
    )
    
    approved = await manager.request_approval(checkpoint)
    assert approved  # Auto-approved in dev mode


@pytest.mark.asyncio
async def test_checkpoint_history():
    """Test checkpoint history tracking."""
    config = CheckpointConfig()
    manager = CheckpointManager(config)
    
    checkpoint1 = Checkpoint("step1", "op1", 0.05, "test")
    checkpoint2 = Checkpoint("step2", "op2", 0.15, "test")
    
    await manager.request_approval(checkpoint1)
    await manager.request_approval(checkpoint2)
    
    history = manager.get_checkpoint_history()
    assert len(history) == 2
    assert history[0].step_name == "step1"
    assert history[1].step_name == "step2"
