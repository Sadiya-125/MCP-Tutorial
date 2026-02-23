"""
MCP Tool Handler
================
Executes actions and manages tool invocations.

Responsibilities:
- Registering available tools
- Validating tool calls
- Executing tools safely
- Returning results

This separation ensures actions are controlled and auditable.
"""

from typing import Callable, Any, Optional
from dataclasses import dataclass, field


@dataclass
class Tool:
    """Definition of a tool that can be invoked."""
    name: str
    description: str
    handler: Callable
    parameters: dict = field(default_factory=dict)
    requires_confirmation: bool = False


@dataclass
class ToolResult:
    """Result of a tool invocation."""
    success: bool
    output: Any
    error: Optional[str] = None


class ToolHandler:
    """
    Manages and executes tools.

    Tools are the "hands" of the AI system - they perform
    actual actions in the world (read files, execute code, etc.)
    """

    def __init__(self):
        self._tools: dict[str, Tool] = {}
        self._execution_log: list[dict] = []

    def register_tool(
        self,
        name: str,
        handler: Callable,
        description: str = "",
        parameters: dict = None,
        requires_confirmation: bool = False
    ) -> None:
        """Register a new tool."""
        self._tools[name] = Tool(
            name=name,
            description=description,
            handler=handler,
            parameters=parameters or {},
            requires_confirmation=requires_confirmation
        )

    def list_tools(self) -> list[dict]:
        """List all available tools."""
        return [
            {
                "name": t.name,
                "description": t.description,
                "parameters": t.parameters,
                "requires_confirmation": t.requires_confirmation
            }
            for t in self._tools.values()
        ]

    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        return self._tools.get(name)

    def invoke(self, tool_name: str, **kwargs) -> ToolResult:
        """
        Invoke a tool by name with given arguments.

        This is the central point for all tool executions,
        enabling logging, validation, and control.
        """
        tool = self._tools.get(tool_name)

        if not tool:
            return ToolResult(
                success=False,
                output=None,
                error=f"Unknown tool: {tool_name}"
            )

        # Log the invocation
        log_entry = {
            "tool": tool_name,
            "args": kwargs,
            "status": "pending"
        }
        self._execution_log.append(log_entry)

        try:
            result = tool.handler(**kwargs)
            log_entry["status"] = "success"
            log_entry["result"] = str(result)[:100]  # Truncate for log

            return ToolResult(success=True, output=result)

        except Exception as e:
            log_entry["status"] = "error"
            log_entry["error"] = str(e)

            return ToolResult(
                success=False,
                output=None,
                error=str(e)
            )

    def get_execution_log(self) -> list[dict]:
        """Get the history of tool executions."""
        return self._execution_log.copy()

    def clear_log(self) -> None:
        """Clear the execution log."""
        self._execution_log.clear()


# Default tools that come with the system
def create_default_tools() -> ToolHandler:
    """Create a ToolHandler with default tools."""
    handler = ToolHandler()

    # Echo tool (for testing)
    handler.register_tool(
        name="echo",
        handler=lambda message: f"Echo: {message}",
        description="Echoes back the input message",
        parameters={"message": "string"}
    )

    # Help tool
    def show_help(tool_handler: ToolHandler = handler):
        tools = tool_handler.list_tools()
        lines = ["Available tools:"]
        for t in tools:
            lines.append(f"  - {t['name']}: {t['description']}")
        return "\n".join(lines)

    handler.register_tool(
        name="help",
        handler=show_help,
        description="Shows available tools"
    )

    return handler
