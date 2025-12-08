"""Tests for ToolAdapter."""

import pytest
from unittest.mock import AsyncMock

from polyhedra.agent.tool_adapter import ToolAdapter


class TestToolAdapter:
    """Test suite for ToolAdapter."""
    
    def test_initialization(self):
        """Test adapter initialization."""
        tools = {''tool1'': AsyncMock(), ''tool2'': AsyncMock()}
        adapter = ToolAdapter(tools)
        assert adapter.tools == tools
    
    def test_get_tool_exists(self):
        """Test getting existing tool."""
        tool = AsyncMock()
        adapter = ToolAdapter({''test_tool'': tool})
        result = adapter.get_tool(''test_tool'')
        assert result is tool
    
    def test_get_tool_not_found(self):
        """Test getting non-existent tool raises KeyError."""
        adapter = ToolAdapter({})
        with pytest.raises(KeyError, match="not found"):
            adapter.get_tool(''nonexistent'')
    
    def test_list_tools(self):
        """Test listing all tools."""
        tools = {''tool1'': AsyncMock(), ''tool2'': AsyncMock(), ''tool3'': AsyncMock()}
        adapter = ToolAdapter(tools)
        tool_list = adapter.list_tools()
        assert set(tool_list) == {''tool1'', ''tool2'', ''tool3''}
    
    def test_has_tool_exists(self):
        """Test has_tool returns True for existing tool."""
        adapter = ToolAdapter({''test_tool'': AsyncMock()})
        assert adapter.has_tool(''test_tool'') is True
    
    def test_has_tool_not_exists(self):
        """Test has_tool returns False for non-existent tool."""
        adapter = ToolAdapter({''test_tool'': AsyncMock()})
        assert adapter.has_tool(''other_tool'') is False
    
    def test_list_tools_empty(self):
        """Test listing tools when none exist."""
        adapter = ToolAdapter({})
        assert adapter.list_tools() == []
