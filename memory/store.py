"""
Persistent Memory Store
=======================
Lab 5: Adding persistent memory that survives across sessions.

Key Concepts:
- Persistent vs ephemeral state
- Memory that survives restarts
- JSON-based storage for simplicity
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Any, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class MemoryRecord:
    """A single memory record with metadata."""
    key: str
    value: Any
    category: str = "general"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    access_count: int = 0


class PersistentMemory:
    """
    Persistent memory storage using JSON files.

    This enables the assistant to remember information
    across sessions - a key requirement for continuity.
    """

    def __init__(self, storage_path: str = "memory/data"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._memory_file = self.storage_path / "memory.json"
        self._memory: dict[str, MemoryRecord] = {}
        self._load()

    def _load(self) -> None:
        """Load memory from disk."""
        if self._memory_file.exists():
            try:
                with open(self._memory_file, 'r') as f:
                    data = json.load(f)
                    for key, record_data in data.items():
                        self._memory[key] = MemoryRecord(**record_data)
            except (json.JSONDecodeError, TypeError):
                self._memory = {}

    def _save(self) -> None:
        """Save memory to disk."""
        data = {key: asdict(record) for key, record in self._memory.items()}
        with open(self._memory_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def store(self, key: str, value: Any, category: str = "general") -> None:
        """
        Store a value persistently.

        Args:
            key: Unique identifier
            value: The data to store (must be JSON-serializable)
            category: Category for organization
        """
        now = datetime.now().isoformat()

        if key in self._memory:
            # Update existing
            record = self._memory[key]
            record.value = value
            record.category = category
            record.updated_at = now
        else:
            # Create new
            record = MemoryRecord(
                key=key,
                value=value,
                category=category,
                created_at=now,
                updated_at=now
            )
            self._memory[key] = record

        self._save()

    def retrieve(self, key: str, default: Any = None) -> Any:
        """Retrieve a value from persistent memory."""
        record = self._memory.get(key)
        if record:
            record.access_count += 1
            record.updated_at = datetime.now().isoformat()
            self._save()
            return record.value
        return default

    def delete(self, key: str) -> bool:
        """Delete a value from persistent memory."""
        if key in self._memory:
            del self._memory[key]
            self._save()
            return True
        return False

    def list_keys(self, category: Optional[str] = None) -> list[str]:
        """List all keys, optionally filtered by category."""
        if category:
            return [k for k, v in self._memory.items() if v.category == category]
        return list(self._memory.keys())

    def get_categories(self) -> list[str]:
        """Get all unique categories."""
        return list(set(r.category for r in self._memory.values()))

    def search(self, query: str) -> list[tuple[str, Any]]:
        """Search memory by key or value content."""
        results = []
        query_lower = query.lower()

        for key, record in self._memory.items():
            if query_lower in key.lower():
                results.append((key, record.value))
            elif isinstance(record.value, str) and query_lower in record.value.lower():
                results.append((key, record.value))

        return results

    def get_stats(self) -> dict:
        """Get memory statistics."""
        return {
            "total_entries": len(self._memory),
            "categories": self.get_categories(),
            "storage_file": str(self._memory_file),
            "most_accessed": sorted(
                [(k, r.access_count) for k, r in self._memory.items()],
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }

    def to_context_string(self) -> str:
        """Convert memory to a context string for prompts."""
        if not self._memory:
            return "Persistent memory is empty."

        lines = ["Persistent Memory:"]

        # Group by category
        by_category: dict[str, list] = {}
        for key, record in self._memory.items():
            if record.category not in by_category:
                by_category[record.category] = []
            by_category[record.category].append((key, record.value))

        for category, items in by_category.items():
            lines.append(f"\n[{category.upper()}]")
            for key, value in items:
                value_str = str(value)[:80]
                if len(str(value)) > 80:
                    value_str += "..."
                lines.append(f"  {key}: {value_str}")

        return "\n".join(lines)

    def clear(self, category: Optional[str] = None) -> int:
        """Clear memory entries."""
        if category:
            keys_to_delete = [k for k, v in self._memory.items() if v.category == category]
            for key in keys_to_delete:
                del self._memory[key]
            count = len(keys_to_delete)
        else:
            count = len(self._memory)
            self._memory.clear()

        self._save()
        return count

    def export(self, filepath: str) -> None:
        """Export memory to a file."""
        data = {key: asdict(record) for key, record in self._memory.items()}
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def import_from(self, filepath: str) -> int:
        """Import memory from a file."""
        with open(filepath, 'r') as f:
            data = json.load(f)

        count = 0
        for key, record_data in data.items():
            self._memory[key] = MemoryRecord(**record_data)
            count += 1

        self._save()
        return count
