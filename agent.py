"""
Lab 3: Goal-Oriented Agent
==========================
This module transforms the reactive chatbot into a goal-driven agent.

Key Concepts:
- Reactive vs goal-driven systems
- Task decomposition into steps
- Agent loop: plan → execute → reflect
- Agent behavior emerges from context and goals
"""

import os
from dataclasses import dataclass, field
from typing import Optional, Callable
from enum import Enum
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class StepStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Step:
    """A single step in a task plan."""
    description: str
    status: StepStatus = StepStatus.PENDING
    result: Optional[str] = None

    def mark_complete(self, result: str = None):
        self.status = StepStatus.COMPLETED
        self.result = result

    def mark_failed(self, reason: str = None):
        self.status = StepStatus.FAILED
        self.result = reason


@dataclass
class Goal:
    """
    A goal with a plan of steps.

    Goals transform the assistant from reactive (answer questions)
    to proactive (work towards objectives).
    """
    description: str
    steps: list[Step] = field(default_factory=list)
    current_step_index: int = 0
    is_complete: bool = False

    def add_step(self, description: str) -> Step:
        step = Step(description=description)
        self.steps.append(step)
        return step

    def get_current_step(self) -> Optional[Step]:
        if self.current_step_index < len(self.steps):
            return self.steps[self.current_step_index]
        return None

    def advance(self):
        """Move to the next step."""
        if self.current_step_index < len(self.steps):
            self.current_step_index += 1
        if self.current_step_index >= len(self.steps):
            self.is_complete = True

    def get_progress(self) -> str:
        completed = sum(1 for s in self.steps if s.status == StepStatus.COMPLETED)
        return f"{completed}/{len(self.steps)} steps completed"


class Agent:
    """
    A goal-oriented agent that works step-by-step.

    Key difference from chatbot:
    - Chatbot: responds to each message independently
    - Agent: works towards goals through planned steps
    """

    def __init__(self, context):
        self.context = context
        self.current_goal: Optional[Goal] = None
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def set_goal(self, goal_description: str) -> Goal:
        """Set a new goal and generate a plan."""
        self.current_goal = Goal(description=goal_description)
        self._generate_plan()
        return self.current_goal

    def _generate_plan(self):
        """Use LLM to decompose goal into steps."""
        if not self.current_goal:
            return

        prompt = f"""Break down this goal into 3-5 concrete, actionable steps:

Goal: {self.current_goal.description}

Context:
{self.context.to_prompt_context()}

Return ONLY a numbered list of steps, nothing else.
Example:
1. First step
2. Second step
3. Third step"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )

            plan_text = response.choices[0].message.content
            # Parse numbered steps
            for line in plan_text.strip().split('\n'):
                line = line.strip()
                if line and line[0].isdigit():
                    # Remove numbering (1. 2. etc.)
                    step_desc = line.split('.', 1)[-1].strip()
                    if step_desc:
                        self.current_goal.add_step(step_desc)

        except Exception as e:
            # Fallback: single step
            self.current_goal.add_step(f"Complete: {self.current_goal.description}")

    def execute_current_step(self) -> str:
        """Execute the current step and return the result."""
        if not self.current_goal:
            return "No goal set. Use 'goal: <description>' to set one."

        step = self.current_goal.get_current_step()
        if not step:
            return f"Goal complete! {self.current_goal.get_progress()}"

        step.status = StepStatus.IN_PROGRESS

        # Use LLM to execute the step
        prompt = f"""You are executing step {self.current_goal.current_step_index + 1} of a plan.

Goal: {self.current_goal.description}
Current Step: {step.description}

Context:
{self.context.to_prompt_context()}

Execute this step and provide the result. Be specific and actionable.
If this is a coding step, provide code.
If this requires user input, ask for it clearly."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )

            result = response.choices[0].message.content
            step.mark_complete(result)
            self.current_goal.advance()

            # Update context
            self.context.add_note(f"Completed step: {step.description}")

            return result

        except Exception as e:
            step.mark_failed(str(e))
            return f"Step failed: {str(e)}"

    def get_status(self) -> str:
        """Get the current goal and progress status."""
        if not self.current_goal:
            return "No active goal. Set one with 'goal: <description>'"

        lines = [
            f"Goal: {self.current_goal.description}",
            f"Progress: {self.current_goal.get_progress()}",
            "",
            "Steps:"
        ]

        for i, step in enumerate(self.current_goal.steps):
            marker = "→" if i == self.current_goal.current_step_index else " "
            status_icon = {
                StepStatus.PENDING: "○",
                StepStatus.IN_PROGRESS: "◐",
                StepStatus.COMPLETED: "●",
                StepStatus.FAILED: "✗",
                StepStatus.SKIPPED: "○"
            }.get(step.status, "?")

            lines.append(f"  {marker} {status_icon} {i + 1}. {step.description}")

        return "\n".join(lines)

    def run_all(self) -> list[str]:
        """Run all remaining steps automatically."""
        results = []
        while self.current_goal and not self.current_goal.is_complete:
            result = self.execute_current_step()
            results.append(result)
        return results
