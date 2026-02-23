"""
Execution Pipeline
==================
Lab 7: Implementing deterministic execution pipelines.

Key Concepts:
- Deterministic execution flow
- Pipeline stages: initialize, interpret, decide, invoke, update
- Why execution flow matters more than prompts
"""

from dataclasses import dataclass, field
from typing import Callable, Any, Optional
from datetime import datetime
from enum import Enum


class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class ExecutionResult:
    """Result of a pipeline execution."""
    success: bool
    output: Any
    error: Optional[str] = None
    duration_ms: float = 0
    steps_completed: int = 0


@dataclass
class PipelineStep:
    """A single step in the execution pipeline."""
    name: str
    handler: Callable
    description: str = ""
    required: bool = True
    status: StepStatus = StepStatus.PENDING
    result: Any = None
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

    def execute(self, context: dict) -> Any:
        """Execute this step."""
        self.status = StepStatus.RUNNING
        self.started_at = datetime.now().isoformat()

        try:
            self.result = self.handler(context)
            self.status = StepStatus.COMPLETED
            return self.result
        except Exception as e:
            self.status = StepStatus.FAILED
            self.error = str(e)
            raise
        finally:
            self.completed_at = datetime.now().isoformat()


class ExecutionPipeline:
    """
    Deterministic execution pipeline for MCP.

    The pipeline ensures:
    1. Predictable execution order
    2. Clear state transitions
    3. Traceable execution history
    4. Error handling at each stage

    Standard MCP Pipeline:
    1. Initialize Context - Load and prepare context
    2. Interpret Instruction - Understand user intent
    3. Decide Action - Choose what to do
    4. Invoke Tool - Execute the action
    5. Update State - Save results and update context
    """

    def __init__(self):
        self._steps: list[PipelineStep] = []
        self._execution_history: list[dict] = []
        self._context: dict = {}

    def add_step(
        self,
        name: str,
        handler: Callable,
        description: str = "",
        required: bool = True
    ) -> 'ExecutionPipeline':
        """Add a step to the pipeline. Returns self for chaining."""
        step = PipelineStep(
            name=name,
            handler=handler,
            description=description,
            required=required
        )
        self._steps.append(step)
        return self

    def execute(self, initial_context: dict = None) -> ExecutionResult:
        """
        Execute the entire pipeline.

        Args:
            initial_context: Starting context for the pipeline

        Returns:
            ExecutionResult with output and metadata
        """
        start_time = datetime.now()
        self._context = initial_context or {}
        steps_completed = 0
        final_output = None

        # Reset all steps
        for step in self._steps:
            step.status = StepStatus.PENDING
            step.result = None
            step.error = None

        try:
            for step in self._steps:
                # Execute the step
                result = step.execute(self._context)

                # Update context with result
                self._context[f"{step.name}_result"] = result
                self._context["last_result"] = result
                final_output = result
                steps_completed += 1

            # Record execution
            end_time = datetime.now()
            duration_ms = (end_time - start_time).total_seconds() * 1000

            self._execution_history.append({
                "timestamp": start_time.isoformat(),
                "duration_ms": duration_ms,
                "steps_completed": steps_completed,
                "success": True
            })

            return ExecutionResult(
                success=True,
                output=final_output,
                duration_ms=duration_ms,
                steps_completed=steps_completed
            )

        except Exception as e:
            end_time = datetime.now()
            duration_ms = (end_time - start_time).total_seconds() * 1000

            self._execution_history.append({
                "timestamp": start_time.isoformat(),
                "duration_ms": duration_ms,
                "steps_completed": steps_completed,
                "success": False,
                "error": str(e)
            })

            return ExecutionResult(
                success=False,
                output=None,
                error=str(e),
                duration_ms=duration_ms,
                steps_completed=steps_completed
            )

    def get_status(self) -> str:
        """Get the current pipeline status."""
        lines = ["Pipeline Status:", ""]

        for i, step in enumerate(self._steps, 1):
            status_icon = {
                StepStatus.PENDING: "○",
                StepStatus.RUNNING: "◐",
                StepStatus.COMPLETED: "●",
                StepStatus.FAILED: "✗",
                StepStatus.SKIPPED: "○"
            }.get(step.status, "?")

            lines.append(f"  {status_icon} {i}. {step.name}")
            if step.description:
                lines.append(f"      {step.description}")

        return "\n".join(lines)

    def get_history(self) -> list[dict]:
        """Get execution history."""
        return self._execution_history.copy()

    def get_context(self) -> dict:
        """Get current context."""
        return self._context.copy()

    def reset(self) -> None:
        """Reset the pipeline state."""
        for step in self._steps:
            step.status = StepStatus.PENDING
            step.result = None
            step.error = None
        self._context = {}


def create_mcp_pipeline(orchestrator) -> ExecutionPipeline:
    """
    Create the standard MCP execution pipeline.

    This is the core MCP runtime flow.
    """
    pipeline = ExecutionPipeline()

    # Step 1: Initialize Context
    def initialize_context(ctx: dict) -> dict:
        """Load and prepare all context."""
        ctx["context_string"] = orchestrator._get_full_context()
        ctx["session_id"] = orchestrator.context_hierarchy.session_ctx.session_id
        return ctx

    pipeline.add_step(
        "initialize_context",
        initialize_context,
        "Load context from all sources"
    )

    # Step 2: Interpret Instruction
    def interpret_instruction(ctx: dict) -> dict:
        """Understand user intent."""
        user_input = ctx.get("user_input", "")
        intent = orchestrator.reasoner.interpret_intent(
            user_input,
            ctx.get("context_string", "")
        )
        return intent

    pipeline.add_step(
        "interpret_instruction",
        interpret_instruction,
        "Parse and understand user intent"
    )

    # Step 3: Decide Action
    def decide_action(ctx: dict) -> str:
        """Choose what action to take."""
        intent = ctx.get("interpret_instruction_result", {})
        intent_type = intent.get("type", "question")

        if intent_type == "command":
            return "execute_command"
        elif intent_type == "goal":
            return "create_plan"
        else:
            return "generate_response"

    pipeline.add_step(
        "decide_action",
        decide_action,
        "Determine the appropriate action"
    )

    # Step 4: Invoke Tool/Generate Response
    def invoke_action(ctx: dict) -> str:
        """Execute the decided action."""
        action = ctx.get("decide_action_result", "generate_response")
        intent = ctx.get("interpret_instruction_result", {})
        context_str = ctx.get("context_string", "")
        user_input = ctx.get("user_input", "")

        if action == "create_plan":
            goal = intent.get("action", user_input)
            steps = orchestrator.reasoner.generate_plan(goal, context_str)
            return f"Goal: {goal}\n\nPlan:\n" + "\n".join(
                f"  {i}. {s}" for i, s in enumerate(steps, 1)
            )
        else:
            return orchestrator.reasoner.generate_response(user_input, context_str)

    pipeline.add_step(
        "invoke_action",
        invoke_action,
        "Execute the action or generate response"
    )

    # Step 5: Update State
    def update_state(ctx: dict) -> dict:
        """Save results and update context."""
        orchestrator.context_hierarchy.session_ctx.increment_messages()
        return {
            "output": ctx.get("invoke_action_result"),
            "intent": ctx.get("interpret_instruction_result"),
            "action": ctx.get("decide_action_result")
        }

    pipeline.add_step(
        "update_state",
        update_state,
        "Update memory and context"
    )

    return pipeline
