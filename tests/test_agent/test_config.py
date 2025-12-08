"""Tests for agent configuration."""
import pytest
from polyhedra.agent.config import AgentConfig


def test_default_config():
    """Test default configuration."""
    config = AgentConfig()
    
    assert config.max_retry_attempts == 3
    assert config.checkpoint_cost_threshold == 0.50
    assert config.state_dir == ".polyhedra/state"


def test_config_to_dict():
    """Test configuration serialization."""
    config = AgentConfig(max_retry_attempts=5)
    data = config.to_dict()
    
    assert data["max_retry_attempts"] == 5
    assert "checkpoint_cost_threshold" in data
