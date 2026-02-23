"""
Task Context
============
Current task-specific context.
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class TaskContext:
    """
    Task context - specific to the current task being worked on.

    Contains:
    - Task definition
    - Progress tracking
    - Related files and code
    """

    # Task definition
    title: str = ""
    description: str = ""
    goal: str = ""
    status: TaskStatus = TaskStatus.PENDING

    # Progress
    steps: list = field(default_factory=list)
    current_step: int = 0
    completed_steps: list = field(default_factory=list)

    # Related context
    related_files: list = field(default_factory=list)
    code_snippets: dict = field(default_factory=dict)
    notes: list = field(default_factory=list)

    # Constraints
    constraints: list = field(default_factory=list)
    requirements: list = field(default_factory=list)

    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

    def start(self) -> None:
        """Start working on the task."""
        self.status = TaskStatus.IN_PROGRESS
        self.started_at = datetime.now().isoformat()

    def complete(self) -> None:
        """Mark the task as completed."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now().isoformat()

    def add_step(self, step: str) -> None:
        """Add a step to the task."""
        self.steps.append(step)

    def complete_step(self) -> Optional[str]:
        """Complete the current step and return it."""
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            self.completed_steps.append(step)
            self.current_step += 1
            return step
        return None

    def add_note(self, note: str) -> None:
        """Add a note to the task."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.notes.append(f"[{timestamp}] {note}")

    def get_progress(self) -> str:
        """Get progress string."""
        if not self.steps:
            return "No steps defined"
        return f"{self.current_step}/{len(self.steps)} steps"

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "title": self.title,
            "description": self.description,
            "goal": self.goal,
            "status": self.status.value,
            "steps": self.steps,
            "current_step": self.current_step,
            "related_files": self.related_files,
            "notes": self.notes
        }

    def to_prompt_string(self) -> str:
        """Convert to string for prompt injection."""
        if not self.title:
            return "[TASK CONTEXT]\nNo active task."

        lines = [
            "[TASK CONTEXT]",
            f"Task: {self.title}",
            f"Status: {self.status.value}",
        ]

        if self.goal:
            lines.append(f"Goal: {self.goal}")

        if self.steps:
            lines.append(f"Progress: {self.get_progress()}")
            if self.current_step < len(self.steps):
                lines.append(f"Current Step: {self.steps[self.current_step]}")

        if self.related_files:
            lines.append(f"Files: {', '.join(self.related_files[:5])}")

        if self.notes:
            lines.append("Recent Notes:")
            for note in self.notes[-3:]:
                lines.append(f"  - {note}")

        return "\n".join(lines)
