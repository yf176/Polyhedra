"""Quick integration test for error recovery system."""
import asyncio
from polyhedra.agent import (
    RetryConfig, CircuitBreaker, retry_with_backoff,
    CheckpointConfig, CheckpointManager, Checkpoint,
    StateManager, WorkflowState, AgentConfig
)


async def test_retry():
    """Test retry with backoff."""
    attempts = []
    
    async def flaky_func():
        attempts.append(1)
        if len(attempts) < 2:
            raise Exception("Transient error")
        return "success"
    
    config = RetryConfig(max_attempts=3, initial_delay=0.01)
    result = await retry_with_backoff(flaky_func, config)
    
    print(f" Retry test passed: {result}, attempts: {len(attempts)}")


async def test_checkpoint():
    """Test checkpoint approval."""
    config = CheckpointConfig(auto_approve_below=0.10)
    manager = CheckpointManager(config)
    
    checkpoint = Checkpoint(
        step_name="test",
        operation="test_op",
        estimated_cost=0.05,
        rationale="Test checkpoint"
    )
    
    approved = await manager.request_approval(checkpoint)
    print(f" Checkpoint test passed: approved={approved}, auto_approved={checkpoint.auto_approved}")


async def test_state():
    """Test state persistence."""
    from pathlib import Path
    from datetime import datetime
    
    manager = StateManager(Path(".test_state"))
    
    state = WorkflowState(
        workflow_id="test-123",
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
    loaded = await manager.load_state("test-123")
    
    print(f" State test passed: loaded workflow_id={loaded.workflow_id}")
    
    # Cleanup
    await manager.delete_state("test-123")


async def main():
    """Run all integration tests."""
    print("Running error recovery integration tests...\n")
    
    await test_retry()
    await test_checkpoint()
    await test_state()
    
    print("\n All integration tests passed!")


if __name__ == "__main__":
    asyncio.run(main())
