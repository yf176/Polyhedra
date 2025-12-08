"""Adapter for integrating MCP tools with agent workflows."""

import logging
from typing import Dict, Any, Callable


class ToolAdapter:
    """
    Adapts MCP server tools for use in agent workflows.
    
    Responsibilities:
    - Wrap tools as async callables
    - Handle tool errors gracefully
    - Format tool results consistently
    - Provide tool discovery
    """
    
    def __init__(self, tools: Dict[str, Callable]):
        """
        Initialize tool adapter.
        
        Args:
            tools: Dictionary of tool name -> async callable
        """
        self.tools = tools
        self.logger = logging.getLogger(__name__)
    
    def get_tool(self, name: str) -> Callable:
        """
        Get tool by name.
        
        Args:
            name: Tool name
            
        Returns:
            Async callable for tool
            
        Raises:
            KeyError: If tool not found
        """
        if name not in self.tools:
            raise KeyError(f"Tool ''{name}'' not found")
        return self.tools[name]
    
    def list_tools(self) -> list:
        """List all available tool names."""
        return list(self.tools.keys())
    
    def has_tool(self, name: str) -> bool:
        """
        Check if tool exists.
        
        Args:
            name: Tool name
            
        Returns:
            True if tool exists
        """
        return name in self.tools
