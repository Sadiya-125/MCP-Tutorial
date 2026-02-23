"""
Context Hierarchy Module
========================
Lab 6: Organizing context into reusable, hierarchical layers.

Context Levels:
- Global: System-wide configuration and defaults
- Project: Project-specific settings and info
- Task: Current task context
- Session: Current session state
"""

from .global_context import GlobalContext
from .project_context import ProjectContext
from .task_context import TaskContext
from .session_context import SessionContext
from .hierarchy import ContextHierarchy

__all__ = [
    'GlobalContext',
    'ProjectContext',
    'TaskContext',
    'SessionContext',
    'ContextHierarchy'
]
