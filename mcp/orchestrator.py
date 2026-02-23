"""
MCP Orchestrator
================
The central coordinator that ties all MCP components together.

Lab 5 Updates:
- Integrated persistent memory
- Added guardrails for safety
"""

from typing import Optional
from .reasoner import Reasoner
from .tool_handler import ToolHandler, create_default_tools
from .memory_manager import MemoryManager

# Import new v5 modules
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from memory.store import PersistentMemory
from guardrails.rules import GuardRails, RuleResult


class Orchestrator:
    """
    The central coordinator of the MCP system.

    Lab 5 additions:
    - Persistent memory that survives across sessions
    - Guardrails for safety and control
    """

    def __init__(self, use_persistent_memory: bool = True):
        self.reasoner = Reasoner()
        self.tools = create_default_tools()
        self.session_memory = MemoryManager()  # Ephemeral session memory
        self.guardrails = GuardRails()

        # Use persistent memory if enabled
        if use_persistent_memory:
            self.persistent_memory = PersistentMemory()
        else:
            self.persistent_memory = None

        self._setup_tools()

    def _setup_tools(self):
        """Register memory and guarded tools."""

        # Persistent remember
        self.tools.register_tool(
            name="remember",
            handler=lambda key, value: self._guarded_remember(key, value),
            description="Store information persistently",
            parameters={"key": "string", "value": "any"}
        )

        # Persistent recall
        self.tools.register_tool(
            name="recall",
            handler=lambda key: self._recall(key),
            description="Retrieve information from persistent memory",
            parameters={"key": "string"}
        )

        # Forget
        self.tools.register_tool(
            name="forget",
            handler=lambda key: self._forget(key),
            description="Remove information from memory",
            parameters={"key": "string"}
        )

        # Search memory
        self.tools.register_tool(
            name="search_memory",
            handler=lambda query: self._search_memory(query),
            description="Search through persistent memory",
            parameters={"query": "string"}
        )

    def _guarded_remember(self, key: str, value: str) -> str:
        """Store with guardrail check."""
        # Check guardrails
        context = self.guardrails.create_action_context(
            action="store",
            value=value
        )
        result, messages = self.guardrails.check(context)

        if result == RuleResult.DENY:
            return f"Blocked: {'; '.join(messages)}"

        if self.persistent_memory:
            self.persistent_memory.store(key, value, category="user")
            msg = f"Remembered (persistent): {key}"
        else:
            self.session_memory.store(key, value, category="user")
            msg = f"Remembered (session only): {key}"

        if result == RuleResult.WARN:
            msg += f"\nWarnings: {'; '.join(messages)}"

        return msg

    def _recall(self, key: str) -> str:
        """Retrieve from memory (persistent first, then session)."""
        if self.persistent_memory:
            value = self.persistent_memory.retrieve(key)
            if value is not None:
                return f"{key} = {value} (from persistent memory)"

        value = self.session_memory.retrieve(key)
        if value is not None:
            return f"{key} = {value} (from session memory)"

        return f"No memory found for: {key}"

    def _forget(self, key: str) -> str:
        """Remove from memory."""
        forgotten = False

        if self.persistent_memory and self.persistent_memory.delete(key):
            forgotten = True

        if self.session_memory.delete(key):
            forgotten = True

        return f"Forgot: {key}" if forgotten else f"Nothing to forget for: {key}"

    def _search_memory(self, query: str) -> str:
        """Search through persistent memory."""
        if not self.persistent_memory:
            return "Persistent memory not enabled."

        results = self.persistent_memory.search(query)
        if not results:
            return f"No results found for: {query}"

        lines = [f"Search results for '{query}':"]
        for key, value in results:
            lines.append(f"  - {key}: {str(value)[:50]}...")
        return "\n".join(lines)

    def process(self, user_input: str) -> str:
        """
        Main entry point - process user input and return a response.

        Now with guardrails checking!
        """
        # Store the input
        self.session_memory.store("last_input", user_input, category="session")

        # Get combined context
        context = self._get_full_context()

        # Interpret intent
        intent = self.reasoner.interpret_intent(user_input, context)
        intent_type = intent.get("type", "question")

        if intent_type == "command":
            return self._handle_command(intent, context)
        elif intent_type == "goal":
            return self._handle_goal(intent, context)
        else:
            return self._handle_question(user_input, context)

    def _get_full_context(self) -> str:
        """Get combined context from all memory sources."""
        parts = []

        if self.persistent_memory:
            parts.append(self.persistent_memory.to_context_string())

        parts.append(self.session_memory.to_context_string())

        return "\n\n".join(parts)

    def _handle_command(self, intent: dict, context: str) -> str:
        """Handle command-type intents with guardrails."""
        action = intent.get("action", "")

        # Check guardrails for the action
        ctx = self.guardrails.create_action_context(action=action)
        result, messages = self.guardrails.check(ctx)

        if result == RuleResult.DENY:
            return f"Action blocked by guardrails:\n" + "\n".join(messages)

        # Check if it matches a tool
        for tool in self.tools.list_tools():
            if tool["name"].lower() in action.lower():
                tool_result = self.tools.invoke(tool["name"])
                response = tool_result.output if tool_result.success else tool_result.error

                if result == RuleResult.WARN:
                    response = f"Warnings: {'; '.join(messages)}\n\n{response}"

                return response

        return self.reasoner.generate_response(f"Execute: {action}", context)

    def _handle_goal(self, intent: dict, context: str) -> str:
        """Handle goal-type intents."""
        goal = intent.get("action", "")
        steps = self.reasoner.generate_plan(goal, context)

        # Store goal in persistent memory if available
        if self.persistent_memory:
            self.persistent_memory.store("current_goal", goal, category="task")
            self.persistent_memory.store("current_plan", steps, category="task")
            self.persistent_memory.store("current_step", 0, category="task")
        else:
            self.session_memory.store("current_goal", goal, category="task")
            self.session_memory.store("current_plan", steps, category="task")
            self.session_memory.store("current_step", 0, category="task")

        lines = [f"Goal: {goal}", "", "Plan:"]
        for i, step in enumerate(steps, 1):
            lines.append(f"  {i}. {step}")

        return "\n".join(lines)

    def _handle_question(self, question: str, context: str) -> str:
        """Handle question-type intents."""
        return self.reasoner.generate_response(question, context)

    def execute_step(self) -> str:
        """Execute the next step in the current plan."""
        # Try persistent first, then session
        memory = self.persistent_memory or self.session_memory

        goal = memory.retrieve("current_goal")
        plan = memory.retrieve("current_plan")
        step_index = memory.retrieve("current_step", 0)

        if not goal or not plan:
            return "No active goal. Set one first."

        if step_index >= len(plan):
            return f"Goal '{goal}' is complete!"

        current_step = plan[step_index]
        context = self._get_full_context()

        result = self.reasoner.generate_response(
            f"Execute this step for goal '{goal}': {current_step}",
            context
        )

        # Advance step
        if self.persistent_memory:
            self.persistent_memory.store("current_step", step_index + 1, category="task")
        else:
            self.session_memory.store("current_step", step_index + 1, category="task")

        return f"Step {step_index + 1}: {current_step}\n\n{result}"

    def get_status(self) -> str:
        """Get the current system status including guardrails."""
        lines = ["=== MCP Status ===", ""]

        # Memory stats
        if self.persistent_memory:
            stats = self.persistent_memory.get_stats()
            lines.append(f"Persistent memory: {stats['total_entries']} entries")
            lines.append(f"Categories: {', '.join(stats['categories']) if stats['categories'] else 'none'}")

        # Session memory
        snapshot = self.session_memory.get_snapshot()
        lines.append(f"Session memory: {snapshot['entry_count']} entries")

        # Current goal
        memory = self.persistent_memory or self.session_memory
        goal = memory.retrieve("current_goal")
        if goal:
            plan = memory.retrieve("current_plan", [])
            step = memory.retrieve("current_step", 0)
            lines.append("")
            lines.append(f"Current goal: {goal}")
            lines.append(f"Progress: {step}/{len(plan)} steps")

        # Guardrails
        lines.append("")
        lines.append(f"Active guardrails: {len(self.guardrails.list_rules())}")
        violations = self.guardrails.get_violations()
        if violations:
            lines.append(f"Recent violations: {len(violations)}")

        # Tools
        lines.append("")
        lines.append(f"Available tools: {len(self.tools.list_tools())}")

        return "\n".join(lines)

    def get_guardrail_status(self) -> str:
        """Get detailed guardrail status."""
        lines = ["=== Guardrails ===", ""]

        for rule in self.guardrails.list_rules():
            lines.append(f"[{rule['severity'].upper()}] {rule['name']}")
            lines.append(f"    {rule['description']}")
            lines.append(f"    Category: {rule['category']}")
            lines.append("")

        violations = self.guardrails.get_violations()
        if violations:
            lines.append("Recent Violations:")
            for v in violations[-5:]:
                lines.append(f"  - {v['timestamp']}: {v['rule']} ({v['action']})")

        return "\n".join(lines)
