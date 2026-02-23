"""
Lab 2: Structured Context
=========================
This module introduces the first MCP-style separation: context as a
structured object, separate from prompts.

Key Concepts:
- Context is state, not text
- Prompts become minimal when context is externalized
- Structured context enables predictability
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class TaskInfo:
    """Information about the current task."""
    description: str = ""
    goal: str = ""
    status: str = "pending"  # pending, in_progress, completed, blocked
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class FileInfo:
    """Information about files being worked on."""
    current_file: Optional[str] = None
    language: Optional[str] = None
    framework: Optional[str] = None
    related_files: list = field(default_factory=list)


@dataclass
class Context:
    """
    Structured context object - the first MCP-style separation.

    Instead of embedding everything in prompts, we externalize:
    - Task information
    - File information
    - Session notes

    This allows prompts to be minimal while maintaining state.
    """
    task: TaskInfo = field(default_factory=TaskInfo)
    file_info: FileInfo = field(default_factory=FileInfo)
    notes: list = field(default_factory=list)
    user_name: Optional[str] = None
    session_id: str = field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S"))

    def add_note(self, note: str) -> None:
        """Add a note to the context."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.notes.append(f"[{timestamp}] {note}")

    def set_task(self, description: str, goal: str = "") -> None:
        """Set the current task."""
        self.task = TaskInfo(description=description, goal=goal, status="in_progress")

    def complete_task(self) -> None:
        """Mark the current task as completed."""
        self.task.status = "completed"

    def set_file_context(self, filename: str, language: str = None, framework: str = None) -> None:
        """Set the current file context."""
        self.file_info.current_file = filename
        if language:
            self.file_info.language = language
        if framework:
            self.file_info.framework = framework

    def to_prompt_context(self) -> str:
        """
        Convert structured context to a string for inclusion in prompts.
        This is how we inject context without bloating the prompt itself.
        """
        parts = []

        if self.user_name:
            parts.append(f"User: {self.user_name}")

        if self.task.description:
            parts.append(f"Current Task: {self.task.description}")
            if self.task.goal:
                parts.append(f"Goal: {self.task.goal}")
            parts.append(f"Status: {self.task.status}")

        if self.file_info.current_file:
            parts.append(f"Working on: {self.file_info.current_file}")
            if self.file_info.language:
                parts.append(f"Language: {self.file_info.language}")
            if self.file_info.framework:
                parts.append(f"Framework: {self.file_info.framework}")

        if self.notes:
            parts.append("Recent notes:")
            for note in self.notes[-5:]:  # Last 5 notes
                parts.append(f"  - {note}")

        return "\n".join(parts) if parts else "No context set."

    def __str__(self) -> str:
        return self.to_prompt_context()


def create_context() -> Context:
    """Factory function to create a new context."""
    return Context()
