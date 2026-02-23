"""
MCP Orchestrator
================
The central coordinator that ties all MCP components together.

Responsibilities:
- Receiving user input
- Coordinating between Reasoner, ToolHandler, and MemoryManager
- Managing the overall execution flow
- Maintaining conversation state

This is the "brain" that decides what to do and delegates to specialists.
"""

from typing import Optional
from .reasoner import Reasoner
from .tool_handler import ToolHandler, create_default_tools
from .memory_manager import MemoryManager


class Orchestrator:
    """
    The central coordinator of the MCP system.

    Think of it as the conductor of an orchestra:
    - It doesn't play instruments (that's the tools)
    - It doesn't compose music (that's the reasoner)
    - It doesn't remember the score (that's memory)
    - But it coordinates everything to create a coherent performance
    """

    def __init__(self):
        self.reasoner = Reasoner()
        self.tools = create_default_tools()
        self.memory = MemoryManager()
        self._setup_memory_tools()

    def _setup_memory_tools(self):
        """Register memory-related tools."""
        # Remember tool
        self.tools.register_tool(
            name="remember",
            handler=lambda key, value: self._remember(key, value),
            description="Store information in memory",
            parameters={"key": "string", "value": "any"}
        )

        # Recall tool
        self.tools.register_tool(
            name="recall",
            handler=lambda key: self._recall(key),
            description="Retrieve information from memory",
            parameters={"key": "string"}
        )

        # Forget tool
        self.tools.register_tool(
            name="forget",
            handler=lambda key: self._forget(key),
            description="Remove information from memory",
            parameters={"key": "string"}
        )

    def _remember(self, key: str, value: str) -> str:
        self.memory.store(key, value, category="user")
        return f"Remembered: {key} = {value}"

    def _recall(self, key: str) -> str:
        value = self.memory.retrieve(key)
        if value:
            return f"{key} = {value}"
        return f"No memory found for: {key}"

    def _forget(self, key: str) -> str:
        if self.memory.delete(key):
            return f"Forgot: {key}"
        return f"Nothing to forget for: {key}"

    def process(self, user_input: str) -> str:
        """
        Main entry point - process user input and return a response.

        This method orchestrates the entire flow:
        1. Update context with input
        2. Interpret the intent
        3. Decide on action
        4. Execute (tool or response)
        5. Update memory
        6. Return result
        """
        # Store the input in memory
        self.memory.store("last_input", user_input, category="session")

        # Get current context
        context = self.memory.to_context_string()

        # Interpret intent
        intent = self.reasoner.interpret_intent(user_input, context)

        # Handle different intent types
        intent_type = intent.get("type", "question")

        if intent_type == "command":
            return self._handle_command(intent, context)
        elif intent_type == "goal":
            return self._handle_goal(intent, context)
        else:
            return self._handle_question(user_input, context)

    def _handle_command(self, intent: dict, context: str) -> str:
        """Handle command-type intents."""
        action = intent.get("action", "")

        # Check if it matches a tool
        for tool in self.tools.list_tools():
            if tool["name"].lower() in action.lower():
                result = self.tools.invoke(tool["name"])
                return result.output if result.success else result.error

        # Otherwise, let the reasoner decide
        return self.reasoner.generate_response(
            f"Execute this command: {action}",
            context
        )

    def _handle_goal(self, intent: dict, context: str) -> str:
        """Handle goal-type intents."""
        goal = intent.get("action", "")

        # Generate a plan
        steps = self.reasoner.generate_plan(goal, context)

        # Store the goal and plan
        self.memory.store("current_goal", goal, category="task")
        self.memory.store("current_plan", steps, category="task")
        self.memory.store("current_step", 0, category="task")

        # Format the plan
        lines = [f"Goal: {goal}", "", "Plan:"]
        for i, step in enumerate(steps, 1):
            lines.append(f"  {i}. {step}")

        return "\n".join(lines)

    def _handle_question(self, question: str, context: str) -> str:
        """Handle question-type intents."""
        return self.reasoner.generate_response(question, context)

    def execute_step(self) -> str:
        """Execute the next step in the current plan."""
        goal = self.memory.retrieve("current_goal")
        plan = self.memory.retrieve("current_plan")
        step_index = self.memory.retrieve("current_step", 0)

        if not goal or not plan:
            return "No active goal. Set one first."

        if step_index >= len(plan):
            return f"Goal '{goal}' is complete!"

        current_step = plan[step_index]
        context = self.memory.to_context_string()

        # Execute the step using reasoner
        result = self.reasoner.generate_response(
            f"Execute this step for the goal '{goal}': {current_step}",
            context
        )

        # Advance to next step
        self.memory.store("current_step", step_index + 1, category="task")

        return f"Step {step_index + 1}: {current_step}\n\n{result}"

    def get_status(self) -> str:
        """Get the current system status."""
        lines = ["=== MCP Status ===", ""]

        # Memory summary
        snapshot = self.memory.get_snapshot()
        lines.append(f"Memory entries: {snapshot['entry_count']}")
        lines.append(f"Categories: {', '.join(snapshot['categories'].keys())}")

        # Current goal
        goal = self.memory.retrieve("current_goal")
        if goal:
            plan = self.memory.retrieve("current_plan", [])
            step = self.memory.retrieve("current_step", 0)
            lines.append("")
            lines.append(f"Current goal: {goal}")
            lines.append(f"Progress: {step}/{len(plan)} steps")

        # Tools
        lines.append("")
        lines.append(f"Available tools: {len(self.tools.list_tools())}")

        return "\n".join(lines)
