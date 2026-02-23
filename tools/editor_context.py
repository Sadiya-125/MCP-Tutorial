"""
Editor Context Tool
===================
Lab 10: Capture editor state (active file, selection, cursor).
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class EditorState:
    """Current state of the editor."""
    active_file: Optional[str] = None
    selection: Optional[str] = None
    cursor_line: int = 0
    cursor_column: int = 0
    language: Optional[str] = None


class EditorContext:
    """
    Captures and manages editor context.

    This enables the assistant to know:
    - What file is currently open
    - What text is selected
    - Where the cursor is
    - What language/mode
    """

    def __init__(self):
        self._state = EditorState()
        self._history: list[EditorState] = []

    def set_active_file(self, file_path: str, language: str = None) -> None:
        """Set the currently active file."""
        self._state.active_file = file_path
        if language:
            self._state.language = language
        elif file_path:
            ext = file_path.rsplit('.', 1)[-1] if '.' in file_path else ''
            lang_map = {'py': 'python', 'js': 'javascript', 'ts': 'typescript'}
            self._state.language = lang_map.get(ext, ext)

    def set_selection(self, text: str) -> None:
        """Set the current selection."""
        self._state.selection = text

    def set_cursor(self, line: int, column: int = 0) -> None:
        """Set cursor position."""
        self._state.cursor_line = line
        self._state.cursor_column = column

    def get_state(self) -> EditorState:
        """Get current editor state."""
        return self._state

    def to_context_string(self) -> str:
        """Convert to context string for prompts."""
        if not self._state.active_file:
            return "[EDITOR] No file open"

        lines = [
            "[EDITOR CONTEXT]",
            f"File: {self._state.active_file}",
            f"Language: {self._state.language or 'unknown'}",
            f"Cursor: Line {self._state.cursor_line}"
        ]

        if self._state.selection:
            lines.append(f"Selection: {self._state.selection[:100]}...")

        return "\n".join(lines)

    def snapshot(self) -> None:
        """Save current state to history."""
        import copy
        self._history.append(copy.deepcopy(self._state))
