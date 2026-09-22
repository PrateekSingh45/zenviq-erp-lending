from typing import Dict, List
from .base import Tool

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Tool:
        if name not in self._tools:
            raise ValueError(f"Tool {name} not found in registry")
        return self._tools[name]
        
    def get_all_tools(self) -> List[Tool]:
        return list(self._tools.values())
        
    def get_tools_by_risk(self, risk_level: str) -> List[Tool]:
        return [t for t in self._tools.values() if t.risk_classification == risk_level]

# Global registry instance
registry = ToolRegistry()
