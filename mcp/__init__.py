"""
MCP - Modular Context Protocol
==============================
This package implements the core MCP architecture with clear role separation.

Roles:
- Orchestrator: Coordinates the overall flow
- Reasoner: LLM-based reasoning and decision making
- ToolHandler: Executes actions and tools
- MemoryManager: Manages state and persistence
"""

from .orchestrator import Orchestrator
from .reasoner import Reasoner
from .tool_handler import ToolHandler
from .memory_manager import MemoryManager

__all__ = ['Orchestrator', 'Reasoner', 'ToolHandler', 'MemoryManager']
