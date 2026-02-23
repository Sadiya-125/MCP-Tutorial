"""
Codebase Analyzer
=================
Lab 11: Multi-file understanding and project-wide reasoning.
"""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class FileInfo:
    """Information about a single file."""
    path: str
    extension: str
    lines: int
    size: int
    imports: list[str] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)
    functions: list[str] = field(default_factory=list)


@dataclass
class CodebaseInfo:
    """Information about the entire codebase."""
    root_path: str
    total_files: int
    total_lines: int
    languages: dict[str, int]
    files: list[FileInfo]
    structure: dict


class CodebaseAnalyzer:
    """
    Analyzes a codebase for multi-file understanding.

    Enables:
    - Project-wide reasoning
    - Understanding file relationships
    - Finding relevant code
    """

    LANG_MAP = {
        '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
        '.json': 'JSON', '.md': 'Markdown', '.yaml': 'YAML', '.yml': 'YAML'
    }

    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self._cache: Optional[CodebaseInfo] = None

    def analyze(self, force_refresh: bool = False) -> CodebaseInfo:
        """Analyze the codebase and return info."""
        if self._cache and not force_refresh:
            return self._cache

        files = []
        languages = {}
        structure = {}
        total_lines = 0

        for ext in self.LANG_MAP.keys():
            for file_path in self.root_path.rglob(f"*{ext}"):
                if '.git' in str(file_path) or '__pycache__' in str(file_path):
                    continue

                try:
                    content = file_path.read_text(encoding='utf-8')
                    lines = len(content.splitlines())
                    total_lines += lines

                    # Track language
                    lang = self.LANG_MAP.get(ext, 'Unknown')
                    languages[lang] = languages.get(lang, 0) + 1

                    # Basic analysis for Python files
                    imports, classes, functions = [], [], []
                    if ext == '.py':
                        for line in content.splitlines():
                            line = line.strip()
                            if line.startswith('import ') or line.startswith('from '):
                                imports.append(line)
                            elif line.startswith('class '):
                                classes.append(line.split('(')[0].replace('class ', ''))
                            elif line.startswith('def '):
                                functions.append(line.split('(')[0].replace('def ', ''))

                    files.append(FileInfo(
                        path=str(file_path.relative_to(self.root_path)),
                        extension=ext,
                        lines=lines,
                        size=len(content),
                        imports=imports[:10],
                        classes=classes,
                        functions=functions[:20]
                    ))

                    # Build structure
                    parts = str(file_path.relative_to(self.root_path)).split(os.sep)
                    current = structure
                    for part in parts[:-1]:
                        if part not in current:
                            current[part] = {}
                        current = current[part]

                except:
                    continue

        self._cache = CodebaseInfo(
            root_path=str(self.root_path),
            total_files=len(files),
            total_lines=total_lines,
            languages=languages,
            files=files,
            structure=structure
        )
        return self._cache

    def find_file(self, name: str) -> list[FileInfo]:
        """Find files by name."""
        info = self.analyze()
        return [f for f in info.files if name.lower() in f.path.lower()]

    def find_function(self, name: str) -> list[tuple[str, str]]:
        """Find functions by name. Returns (file, function)."""
        info = self.analyze()
        results = []
        for f in info.files:
            for func in f.functions:
                if name.lower() in func.lower():
                    results.append((f.path, func))
        return results

    def find_class(self, name: str) -> list[tuple[str, str]]:
        """Find classes by name. Returns (file, class)."""
        info = self.analyze()
        results = []
        for f in info.files:
            for cls in f.classes:
                if name.lower() in cls.lower():
                    results.append((f.path, cls))
        return results

    def to_context_string(self) -> str:
        """Convert to context string for prompts."""
        info = self.analyze()

        lines = [
            "[CODEBASE CONTEXT]",
            f"Root: {info.root_path}",
            f"Files: {info.total_files}",
            f"Lines: {info.total_lines}",
            f"Languages: {', '.join(f'{k}({v})' for k, v in info.languages.items())}",
            "",
            "Key Files:"
        ]

        for f in info.files[:10]:
            lines.append(f"  - {f.path} ({f.lines} lines)")
            if f.classes:
                lines.append(f"      Classes: {', '.join(f.classes[:3])}")
            if f.functions:
                lines.append(f"      Functions: {', '.join(f.functions[:5])}")

        return "\n".join(lines)
