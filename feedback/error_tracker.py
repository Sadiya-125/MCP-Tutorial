"""
Error Tracker
=============
Lab 8: Track errors and add them to context for learning.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class ErrorEntry:
    """A tracked error."""
    error_type: str
    message: str
    context: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    resolved: bool = False
    resolution: Optional[str] = None


class ErrorTracker:
    """
    Tracks errors and adds them to context for self-improvement.

    By tracking errors, the assistant can:
    1. Avoid repeating mistakes
    2. Learn from failures
    3. Improve over time
    """

    def __init__(self, max_entries: int = 50):
        self._errors: list[ErrorEntry] = []
        self._max_entries = max_entries

    def track(self, error_type: str, message: str, context: str = "") -> ErrorEntry:
        """Track a new error."""
        entry = ErrorEntry(
            error_type=error_type,
            message=message,
            context=context
        )
        self._errors.append(entry)

        # Keep size limited
        if len(self._errors) > self._max_entries:
            self._errors = self._errors[-self._max_entries:]

        return entry

    def resolve(self, index: int, resolution: str) -> bool:
        """Mark an error as resolved."""
        if 0 <= index < len(self._errors):
            self._errors[index].resolved = True
            self._errors[index].resolution = resolution
            return True
        return False

    def get_unresolved(self) -> list[ErrorEntry]:
        """Get unresolved errors."""
        return [e for e in self._errors if not e.resolved]

    def get_by_type(self, error_type: str) -> list[ErrorEntry]:
        """Get errors of a specific type."""
        return [e for e in self._errors if e.error_type == error_type]

    def to_context_string(self) -> str:
        """Convert errors to context string for prompts."""
        unresolved = self.get_unresolved()
        if not unresolved:
            return "No tracked errors."

        lines = ["Recent Errors to Avoid:"]
        for e in unresolved[-5:]:
            lines.append(f"  - [{e.error_type}] {e.message}")

        return "\n".join(lines)

    def get_stats(self) -> dict:
        """Get error statistics."""
        return {
            "total": len(self._errors),
            "unresolved": len(self.get_unresolved()),
            "resolved": len([e for e in self._errors if e.resolved]),
            "types": list(set(e.error_type for e in self._errors))
        }
