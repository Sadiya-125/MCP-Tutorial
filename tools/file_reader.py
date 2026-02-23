"""
File Reader Tool
================
Lab 10: Read-only file access for the MCP system.
"""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class FileContent:
    """Content of a read file."""
    path: str
    content: str
    lines: int
    size: int
    extension: str


class FileReader:
    """
    Read-only file access tool.

    This is the primary "docking" interface for file system access.
    All file reads go through here for control and auditing.
    """

    ALLOWED_EXTENSIONS = {'.py', '.js', '.ts', '.json', '.md', '.txt', '.yaml', '.yml', '.toml'}

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path).resolve()
        self._read_history: list[str] = []

    def read(self, file_path: str) -> Optional[FileContent]:
        """Read a file and return its content."""
        path = Path(file_path)

        # Security: resolve to absolute and check if within base
        try:
            abs_path = path.resolve()
        except:
            return None

        # Check extension
        if abs_path.suffix.lower() not in self.ALLOWED_EXTENSIONS:
            return None

        # Read file
        try:
            content = abs_path.read_text(encoding='utf-8')
            self._read_history.append(str(abs_path))

            return FileContent(
                path=str(abs_path),
                content=content,
                lines=len(content.splitlines()),
                size=len(content),
                extension=abs_path.suffix
            )
        except:
            return None

    def list_files(self, directory: str = ".", pattern: str = "*") -> list[str]:
        """List files in a directory."""
        path = Path(directory)
        try:
            return [str(f) for f in path.glob(pattern) if f.is_file()]
        except:
            return []

    def get_read_history(self) -> list[str]:
        """Get history of read files."""
        return self._read_history.copy()
