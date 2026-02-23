"""
MCP Memory Manager
==================
Manages state, context, and persistence.

Responsibilities:
- Storing and retrieving context
- Managing session state
- Handling persistence (future: to files/database)
- Context versioning and history

This separation ensures state is centralized and controllable.
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from datetime import datetime


@dataclass
class MemoryEntry:
    """A single memory entry with metadata."""
    key: str
    value: Any
    category: str = "general"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    ttl: Optional[int] = None  # Time to live in seconds, None = permanent


class MemoryManager:
    """
    Centralized memory and state management.

    All context and state flows through here, making it easy to:
    - Track what the system "knows"
    - Persist important information
    - Clear/reset state
    - Implement memory limits
    """

    def __init__(self):
        self._memory: dict[str, MemoryEntry] = {}
        self._history: list[dict] = []
        self._session_start = datetime.now().isoformat()

    def store(
        self,
        key: str,
        value: Any,
        category: str = "general",
        ttl: Optional[int] = None
    ) -> None:
        """
        Store a value in memory.

        Args:
            key: Unique identifier
            value: The data to store
            category: Category for organization (e.g., "user", "task", "file")
            ttl: Optional time-to-live in seconds
        """
        entry = MemoryEntry(key=key, value=value, category=category, ttl=ttl)
        self._memory[key] = entry

        # Log the change
        self._history.append({
            "action": "store",
            "key": key,
            "category": category,
            "timestamp": entry.timestamp
        })

    def retrieve(self, key: str, default: Any = None) -> Any:
        """Retrieve a value from memory."""
        entry = self._memory.get(key)
        if entry:
            return entry.value
        return default

    def delete(self, key: str) -> bool:
        """Delete a value from memory."""
        if key in self._memory:
            del self._memory[key]
            self._history.append({
                "action": "delete",
                "key": key,
                "timestamp": datetime.now().isoformat()
            })
            return True
        return False

    def list_by_category(self, category: str) -> dict[str, Any]:
        """Get all memories in a category."""
        return {
            key: entry.value
            for key, entry in self._memory.items()
            if entry.category == category
        }

    def get_all_keys(self) -> list[str]:
        """Get all memory keys."""
        return list(self._memory.keys())

    def get_snapshot(self) -> dict:
        """
        Get a snapshot of current memory state.

        Useful for including in prompts or debugging.
        """
        snapshot = {
            "session_start": self._session_start,
            "entry_count": len(self._memory),
            "categories": {},
            "entries": {}
        }

        for key, entry in self._memory.items():
            if entry.category not in snapshot["categories"]:
                snapshot["categories"][entry.category] = 0
            snapshot["categories"][entry.category] += 1
            snapshot["entries"][key] = {
                "value": entry.value,
                "category": entry.category,
                "timestamp": entry.timestamp
            }

        return snapshot

    def to_context_string(self) -> str:
        """
        Convert memory to a string suitable for prompt context.
        """
        if not self._memory:
            return "Memory is empty."

        lines = ["Current Memory:"]

        # Group by category
        categories = {}
        for key, entry in self._memory.items():
            if entry.category not in categories:
                categories[entry.category] = []
            categories[entry.category].append((key, entry.value))

        for category, items in categories.items():
            lines.append(f"\n[{category.upper()}]")
            for key, value in items:
                # Truncate long values
                value_str = str(value)
                if len(value_str) > 100:
                    value_str = value_str[:100] + "..."
                lines.append(f"  {key}: {value_str}")

        return "\n".join(lines)

    def clear(self, category: Optional[str] = None) -> int:
        """
        Clear memory entries.

        Args:
            category: If provided, only clear entries in this category.
                     If None, clear all entries.

        Returns:
            Number of entries cleared.
        """
        if category is None:
            count = len(self._memory)
            self._memory.clear()
        else:
            keys_to_delete = [
                key for key, entry in self._memory.items()
                if entry.category == category
            ]
            for key in keys_to_delete:
                del self._memory[key]
            count = len(keys_to_delete)

        self._history.append({
            "action": "clear",
            "category": category,
            "count": count,
            "timestamp": datetime.now().isoformat()
        })

        return count

    def get_history(self) -> list[dict]:
        """Get memory operation history."""
        return self._history.copy()
