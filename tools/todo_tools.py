"""
Todo Tools
==========
Lab 12: TODO.md management for MCP integration.
"""

from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class TodoItem:
    """A single todo item."""
    text: str
    completed: bool
    priority: str  # high, medium, low
    line_number: int

    def to_string(self) -> str:
        """Convert to markdown string."""
        checkbox = "[x]" if self.completed else "[ ]"
        markers = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        marker = markers.get(self.priority, "")
        return f"- {checkbox} {marker} {self.text}"


@dataclass
class TodoList:
    """Todo list from TODO.md."""
    items: list[TodoItem]
    file_path: str

    @property
    def total(self) -> int:
        return len(self.items)

    @property
    def completed(self) -> int:
        return sum(1 for i in self.items if i.completed)

    @property
    def pending(self) -> int:
        return self.total - self.completed

    def to_context_string(self) -> str:
        """Convert to context string."""
        lines = [
            "[TODO LIST]",
            f"Total: {self.total} ({self.completed} done, {self.pending} pending)",
            ""
        ]
        for item in self.items[:10]:
            status = "✓" if item.completed else "○"
            lines.append(f"  {status} {item.text[:50]}")
        return "\n".join(lines)


class TodoTools:
    """
    TODO.md management for MCP.

    Read and write todo items.
    """

    def __init__(self, todo_path: str = "TODO.md"):
        self.todo_path = Path(todo_path)

    def read(self) -> TodoList:
        """Read todo list from file."""
        items = []

        if not self.todo_path.exists():
            return TodoList(items=[], file_path=str(self.todo_path))

        try:
            content = self.todo_path.read_text(encoding='utf-8')

            for line_num, line in enumerate(content.splitlines(), 1):
                line = line.strip()

                # Match markdown checkbox: - [ ] or - [x]
                match = re.match(r'^-\s*\[([ xX])\]\s*(.*)$', line)
                if match:
                    completed = match.group(1).lower() == 'x'
                    text = match.group(2).strip()

                    # Detect priority
                    priority = "medium"
                    if "🔴" in text or "[high]" in text.lower():
                        priority = "high"
                        text = text.replace("🔴", "").replace("[high]", "").strip()
                    elif "🟢" in text or "[low]" in text.lower():
                        priority = "low"
                        text = text.replace("🟢", "").replace("[low]", "").strip()
                    elif "🟡" in text:
                        text = text.replace("🟡", "").strip()

                    items.append(TodoItem(
                        text=text,
                        completed=completed,
                        priority=priority,
                        line_number=line_num
                    ))

        except Exception:
            pass

        return TodoList(items=items, file_path=str(self.todo_path))

    def add(self, text: str, priority: str = "medium") -> bool:
        """Add a todo item."""
        try:
            content = ""
            if self.todo_path.exists():
                content = self.todo_path.read_text(encoding='utf-8')

            if not content.strip():
                content = "# TODO\n\n"

            markers = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            marker = markers.get(priority, "🟡")

            content += f"- [ ] {marker} {text}\n"
            self.todo_path.write_text(content, encoding='utf-8')
            return True

        except Exception:
            return False

    def complete(self, line_number: int) -> bool:
        """Mark a todo item as complete."""
        try:
            if not self.todo_path.exists():
                return False

            lines = self.todo_path.read_text(encoding='utf-8').splitlines()

            if 0 < line_number <= len(lines):
                line = lines[line_number - 1]
                if "- [ ]" in line:
                    lines[line_number - 1] = line.replace("- [ ]", "- [x]", 1)
                    self.todo_path.write_text("\n".join(lines) + "\n", encoding='utf-8')
                    return True

            return False

        except Exception:
            return False

    def remove(self, line_number: int) -> bool:
        """Remove a todo item."""
        try:
            if not self.todo_path.exists():
                return False

            lines = self.todo_path.read_text(encoding='utf-8').splitlines()

            if 0 < line_number <= len(lines):
                del lines[line_number - 1]
                self.todo_path.write_text("\n".join(lines) + "\n", encoding='utf-8')
                return True

            return False

        except Exception:
            return False
