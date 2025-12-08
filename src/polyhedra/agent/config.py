"""Agent configuration management."""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import os
import json
import yaml
import logging

logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Complete agent configuration."""
    
    # Retry configuration
    max_retry_attempts: int = 3
    initial_retry_delay: float = 1.0
    max_retry_delay: float = 60.0
    exponential_base: float = 2.0
    retry_jitter: bool = True
    
    # Circuit breaker
    circuit_breaker_threshold: int = 5
    circuit_breaker_timeout: float = 60.0
    
    # Checkpoint configuration
    checkpoint_cost_threshold: float = 0.50
    checkpoint_auto_approve_below: float = 0.10
    checkpoint_timeout: float = 300.0
    checkpoint_enabled: bool = True
    
    # State persistence
    state_dir: str = ".polyhedra/state"
    state_cleanup_days: int = 7
    
    # Logging
    log_level: str = "INFO"
    
    @classmethod
    def from_env(cls) -> "AgentConfig":
        """Load configuration from environment variables.
        
        Environment variables should be prefixed with POLYHEDRA_AGENT_
        Example: POLYHEDRA_AGENT_MAX_RETRY_ATTEMPTS=5
        
        Returns:
            AgentConfig with values from environment
        """
        config = cls()
        
        # Map environment variables to config fields
        env_mappings = {
            "POLYHEDRA_AGENT_MAX_RETRY_ATTEMPTS": ("max_retry_attempts", int),
            "POLYHEDRA_AGENT_INITIAL_RETRY_DELAY": ("initial_retry_delay", float),
            "POLYHEDRA_AGENT_MAX_RETRY_DELAY": ("max_retry_delay", float),
            "POLYHEDRA_AGENT_CIRCUIT_BREAKER_THRESHOLD": ("circuit_breaker_threshold", int),
            "POLYHEDRA_AGENT_CIRCUIT_BREAKER_TIMEOUT": ("circuit_breaker_timeout", float),
            "POLYHEDRA_AGENT_CHECKPOINT_COST_THRESHOLD": ("checkpoint_cost_threshold", float),
            "POLYHEDRA_AGENT_CHECKPOINT_AUTO_APPROVE": ("checkpoint_auto_approve_below", float),
            "POLYHEDRA_AGENT_CHECKPOINT_TIMEOUT": ("checkpoint_timeout", float),
            "POLYHEDRA_AGENT_CHECKPOINT_ENABLED": ("checkpoint_enabled", lambda x: x.lower() == "true"),
            "POLYHEDRA_AGENT_STATE_DIR": ("state_dir", str),
            "POLYHEDRA_AGENT_STATE_CLEANUP_DAYS": ("state_cleanup_days", int),
            "POLYHEDRA_AGENT_LOG_LEVEL": ("log_level", str),
        }
        
        for env_var, (field_name, converter) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                try:
                    setattr(config, field_name, converter(value))
                except Exception as e:
                    logger.warning(
                        f"Failed to parse {env_var}={value}: {e}"
                    )
                    
        return config
        
    @classmethod
    def from_file(cls, path: str) -> "AgentConfig":
        """Load configuration from YAML or JSON file.
        
        Args:
            path: Path to configuration file (.yaml, .yml, or .json)
            
        Returns:
            AgentConfig with values from file
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is unsupported
        """
        path_obj = Path(path)
        
        if not path_obj.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
            
        # Read file
        content = path_obj.read_text()
        
        # Parse based on extension
        if path_obj.suffix in [".yaml", ".yml"]:
            try:
                data = yaml.safe_load(content)
            except ImportError:
                logger.error("PyYAML not installed. Install with: pip install pyyaml")
                raise
        elif path_obj.suffix == ".json":
            data = json.loads(content)
        else:
            raise ValueError(
                f"Unsupported config format: {path_obj.suffix}. "
                "Use .yaml, .yml, or .json"
            )
            
        # Create config from data
        return cls(**data)
        
    def to_dict(self) -> dict:
        """Convert configuration to dictionary.
        
        Returns:
            Dictionary representation of configuration
        """
        return {
            "max_retry_attempts": self.max_retry_attempts,
            "initial_retry_delay": self.initial_retry_delay,
            "max_retry_delay": self.max_retry_delay,
            "exponential_base": self.exponential_base,
            "retry_jitter": self.retry_jitter,
            "circuit_breaker_threshold": self.circuit_breaker_threshold,
            "circuit_breaker_timeout": self.circuit_breaker_timeout,
            "checkpoint_cost_threshold": self.checkpoint_cost_threshold,
            "checkpoint_auto_approve_below": self.checkpoint_auto_approve_below,
            "checkpoint_timeout": self.checkpoint_timeout,
            "checkpoint_enabled": self.checkpoint_enabled,
            "state_dir": self.state_dir,
            "state_cleanup_days": self.state_cleanup_days,
            "log_level": self.log_level,
        }
        
    def save(self, path: str) -> None:
        """Save configuration to file.
        
        Args:
            path: Path to save configuration to
        """
        path_obj = Path(path)
        data = self.to_dict()
        
        if path_obj.suffix in [".yaml", ".yml"]:
            try:
                content = yaml.dump(data, default_flow_style=False)
                path_obj.write_text(content)
            except ImportError:
                logger.error("PyYAML not installed. Install with: pip install pyyaml")
                raise
        elif path_obj.suffix == ".json":
            content = json.dumps(data, indent=2)
            path_obj.write_text(content)
        else:
            raise ValueError(
                f"Unsupported config format: {path_obj.suffix}. "
                "Use .yaml, .yml, or .json"
            )
            
        logger.info(f"Saved configuration to {path}")
