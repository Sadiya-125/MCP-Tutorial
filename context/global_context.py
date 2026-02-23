"""
Global Context
==============
System-wide configuration and defaults that apply to all operations.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GlobalContext:
    """
    Global context - applies to all operations system-wide.

    Contains:
    - System configuration
    - Default behaviors
    - Global constraints
    """

    # System settings
    model_name: str = "gpt-4o-mini"
    max_tokens: int = 1000
    temperature: float = 0.7

    # Default behaviors
    auto_save: bool = True
    verbose_mode: bool = False
    safe_mode: bool = True

    # Global constraints
    max_memory_entries: int = 1000
    max_value_length: int = 10000
    allowed_file_extensions: list = field(default_factory=lambda: [
        '.py', '.js', '.ts', '.json', '.md', '.txt', '.yaml', '.yml'
    ])

    # System identity
    system_name: str = "MCP Assistant"
    version: str = "0.6.0"

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "model_name": self.model_name,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "auto_save": self.auto_save,
            "verbose_mode": self.verbose_mode,
            "safe_mode": self.safe_mode,
            "system_name": self.system_name,
            "version": self.version
        }

    def to_prompt_string(self) -> str:
        """Convert to string for prompt injection."""
        return f"""[GLOBAL CONTEXT]
System: {self.system_name} v{self.version}
Model: {self.model_name}
Safe Mode: {'Enabled' if self.safe_mode else 'Disabled'}
Verbose: {'On' if self.verbose_mode else 'Off'}"""
