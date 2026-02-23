"""
Context Hierarchy
=================
Lab 6: Organizing context into a hierarchical structure.

The hierarchy enables:
- Scoped context (global vs local)
- Context inheritance
- Modular and scalable context management
"""

from typing import Optional
from .global_context import GlobalContext
from .project_context import ProjectContext
from .task_context import TaskContext
from .session_context import SessionContext


class ContextHierarchy:
    """
    Hierarchical context manager.

    Layers (from most general to most specific):
    1. Global - System-wide settings
    2. Project - Project-specific context
    3. Task - Current task context
    4. Session - Current session state

    More specific contexts can override or extend more general ones.
    """

    def __init__(self):
        self.global_ctx = GlobalContext()
        self.project_ctx = ProjectContext()
        self.task_ctx = TaskContext()
        self.session_ctx = SessionContext()

    def set_project(self, name: str, **kwargs) -> None:
        """Configure the project context."""
        self.project_ctx.name = name
        self.project_ctx.update(**kwargs)

    def set_task(self, title: str, description: str = "", goal: str = "") -> None:
        """Set the current task."""
        self.task_ctx = TaskContext(
            title=title,
            description=description,
            goal=goal
        )
        self.task_ctx.start()

    def complete_task(self) -> None:
        """Complete the current task."""
        self.task_ctx.complete()

    def new_session(self) -> None:
        """Start a new session."""
        self.session_ctx = SessionContext()

    def get_full_context(self) -> str:
        """
        Get the full context string from all layers.

        This is what gets injected into prompts.
        """
        parts = [
            self.global_ctx.to_prompt_string(),
            self.project_ctx.to_prompt_string(),
            self.task_ctx.to_prompt_string(),
            self.session_ctx.to_prompt_string()
        ]
        return "\n\n".join(parts)

    def get_context_for_scope(self, scope: str) -> str:
        """
        Get context for a specific scope.

        Scopes:
        - 'global': Only global context
        - 'project': Global + project
        - 'task': Global + project + task
        - 'session': All contexts (default)
        """
        parts = [self.global_ctx.to_prompt_string()]

        if scope in ['project', 'task', 'session']:
            parts.append(self.project_ctx.to_prompt_string())

        if scope in ['task', 'session']:
            parts.append(self.task_ctx.to_prompt_string())

        if scope == 'session':
            parts.append(self.session_ctx.to_prompt_string())

        return "\n\n".join(parts)

    def get_summary(self) -> dict:
        """Get a summary of all context layers."""
        return {
            "global": {
                "system": self.global_ctx.system_name,
                "version": self.global_ctx.version,
                "safe_mode": self.global_ctx.safe_mode
            },
            "project": {
                "name": self.project_ctx.name or "Not configured",
                "language": self.project_ctx.language or "Unknown",
                "framework": self.project_ctx.framework or "Unknown"
            },
            "task": {
                "title": self.task_ctx.title or "No active task",
                "status": self.task_ctx.status.value,
                "progress": self.task_ctx.get_progress()
            },
            "session": {
                "id": self.session_ctx.session_id,
                "duration": self.session_ctx.get_duration(),
                "messages": self.session_ctx.message_count
            }
        }

    def to_dict(self) -> dict:
        """Convert all contexts to dictionary."""
        return {
            "global": self.global_ctx.to_dict(),
            "project": self.project_ctx.to_dict(),
            "task": self.task_ctx.to_dict(),
            "session": self.session_ctx.to_dict()
        }

    def __str__(self) -> str:
        return self.get_full_context()
