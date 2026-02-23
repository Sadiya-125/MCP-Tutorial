"""
Git Tools
=========
Lab 12: Git operations for MCP integration.
"""

import subprocess
from dataclasses import dataclass
from typing import Optional


@dataclass
class GitStatus:
    """Git repository status."""
    branch: str
    clean: bool
    staged: list[str]
    modified: list[str]
    untracked: list[str]

    def to_context_string(self) -> str:
        """Convert to context string."""
        lines = [
            "[GIT STATUS]",
            f"Branch: {self.branch}",
            f"Clean: {self.clean}"
        ]
        if self.staged:
            lines.append(f"Staged: {', '.join(self.staged[:5])}")
        if self.modified:
            lines.append(f"Modified: {', '.join(self.modified[:5])}")
        if self.untracked:
            lines.append(f"Untracked: {', '.join(self.untracked[:5])}")
        return "\n".join(lines)


@dataclass
class GitCommit:
    """A git commit."""
    hash: str
    message: str
    author: str
    date: str


class GitTools:
    """
    Git operations for MCP.

    Provides read-only git information.
    """

    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def get_status(self) -> Optional[GitStatus]:
        """Get repository status."""
        try:
            # Get branch
            branch_result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True, text=True, cwd=self.repo_path, timeout=5
            )
            branch = branch_result.stdout.strip() or "unknown"

            # Get status
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, cwd=self.repo_path, timeout=5
            )

            staged = []
            modified = []
            untracked = []

            for line in status_result.stdout.splitlines():
                if not line:
                    continue
                status = line[:2]
                filename = line[3:]

                if status[0] in ['A', 'M', 'D', 'R']:
                    staged.append(filename)
                if status[1] == 'M':
                    modified.append(filename)
                if status == '??':
                    untracked.append(filename)

            return GitStatus(
                branch=branch,
                clean=not (staged or modified or untracked),
                staged=staged,
                modified=modified,
                untracked=untracked
            )

        except Exception:
            return None

    def get_recent_commits(self, count: int = 10) -> list[GitCommit]:
        """Get recent commits."""
        try:
            result = subprocess.run(
                ["git", "log", f"-{count}", "--format=%H|%s|%an|%ad", "--date=short"],
                capture_output=True, text=True, cwd=self.repo_path, timeout=5
            )

            commits = []
            for line in result.stdout.splitlines():
                if not line:
                    continue
                parts = line.split("|", 3)
                if len(parts) >= 4:
                    commits.append(GitCommit(
                        hash=parts[0][:8],
                        message=parts[1][:50],
                        author=parts[2],
                        date=parts[3]
                    ))

            return commits

        except Exception:
            return []

    def get_diff(self, staged: bool = False) -> str:
        """Get diff."""
        try:
            cmd = ["git", "diff"]
            if staged:
                cmd.append("--staged")

            result = subprocess.run(
                cmd, capture_output=True, text=True,
                cwd=self.repo_path, timeout=10
            )
            return result.stdout[:2000]

        except Exception:
            return ""
