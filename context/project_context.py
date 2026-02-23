"""
Project Context
===============
Project-specific context that persists across sessions.
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class ProjectContext:
    """
    Project context - specific to the current project/codebase.

    Contains:
    - Project metadata
    - Code structure info
    - Project-specific conventions
    """

    # Project identity
    name: str = ""
    description: str = ""
    root_path: Optional[str] = None

    # Technical info
    language: str = ""
    framework: str = ""
    package_manager: str = ""

    # Code structure
    main_directories: list = field(default_factory=list)
    entry_points: list = field(default_factory=list)
    config_files: list = field(default_factory=list)

    # Project conventions
    naming_convention: str = ""  # snake_case, camelCase, etc.
    test_framework: str = ""
    style_guide: str = ""

    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def update(self, **kwargs) -> None:
        """Update project context fields."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "root_path": self.root_path,
            "language": self.language,
            "framework": self.framework,
            "package_manager": self.package_manager,
            "main_directories": self.main_directories,
            "entry_points": self.entry_points,
            "naming_convention": self.naming_convention,
            "test_framework": self.test_framework
        }

    def to_prompt_string(self) -> str:
        """Convert to string for prompt injection."""
        if not self.name:
            return "[PROJECT CONTEXT]\nNo project configured."

        lines = [
            "[PROJECT CONTEXT]",
            f"Project: {self.name}",
        ]

        if self.description:
            lines.append(f"Description: {self.description}")
        if self.language:
            lines.append(f"Language: {self.language}")
        if self.framework:
            lines.append(f"Framework: {self.framework}")
        if self.main_directories:
            lines.append(f"Main Dirs: {', '.join(self.main_directories)}")
        if self.naming_convention:
            lines.append(f"Naming: {self.naming_convention}")

        return "\n".join(lines)
