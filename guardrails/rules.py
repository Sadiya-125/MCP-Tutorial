"""
Guardrails and Safety Rules
===========================
Lab 5: Implementing capability boundaries and safety constraints.

Key Concepts:
- Why AI needs rules
- Rule-based constraints on actions
- Capability boundaries
- Safe and controllable assistants
"""

from dataclasses import dataclass
from typing import Callable, Optional, Any
from enum import Enum


class RuleResult(Enum):
    """Result of a rule check."""
    ALLOW = "allow"
    DENY = "deny"
    WARN = "warn"


@dataclass
class Rule:
    """A single guardrail rule."""
    name: str
    description: str
    check: Callable[[dict], RuleResult]
    category: str = "general"
    severity: str = "medium"  # low, medium, high, critical


class GuardRails:
    """
    Safety guardrails for the MCP system.

    Guardrails ensure the assistant operates within
    defined boundaries and doesn't perform harmful actions.

    Categories of rules:
    - Content: What can be discussed/generated
    - Actions: What operations can be performed
    - Data: What data can be accessed/modified
    - System: What system operations are allowed
    """

    def __init__(self):
        self._rules: list[Rule] = []
        self._violations: list[dict] = []
        self._setup_default_rules()

    def _setup_default_rules(self):
        """Set up default safety rules."""

        # Rule: No file deletion without confirmation
        self.add_rule(Rule(
            name="no_silent_delete",
            description="Prevent file deletion without explicit confirmation",
            category="actions",
            severity="high",
            check=lambda ctx: (
                RuleResult.DENY
                if ctx.get("action") == "delete_file" and not ctx.get("confirmed")
                else RuleResult.ALLOW
            )
        ))

        # Rule: No execution of shell commands
        self.add_rule(Rule(
            name="no_shell_exec",
            description="Prevent direct shell command execution",
            category="system",
            severity="critical",
            check=lambda ctx: (
                RuleResult.DENY
                if ctx.get("action") == "shell_exec"
                else RuleResult.ALLOW
            )
        ))

        # Rule: Warn on accessing sensitive files
        self.add_rule(Rule(
            name="sensitive_file_warning",
            description="Warn when accessing potentially sensitive files",
            category="data",
            severity="medium",
            check=lambda ctx: (
                RuleResult.WARN
                if self._is_sensitive_file(ctx.get("file_path", ""))
                else RuleResult.ALLOW
            )
        ))

        # Rule: No modification of system files
        self.add_rule(Rule(
            name="no_system_modification",
            description="Prevent modification of system files",
            category="system",
            severity="critical",
            check=lambda ctx: (
                RuleResult.DENY
                if ctx.get("action") == "write_file" and self._is_system_path(ctx.get("file_path", ""))
                else RuleResult.ALLOW
            )
        ))

        # Rule: Memory size limits
        self.add_rule(Rule(
            name="memory_size_limit",
            description="Limit size of stored memory values",
            category="data",
            severity="low",
            check=lambda ctx: (
                RuleResult.DENY
                if ctx.get("action") == "store" and len(str(ctx.get("value", ""))) > 10000
                else RuleResult.ALLOW
            )
        ))

    def _is_sensitive_file(self, path: str) -> bool:
        """Check if a file path is potentially sensitive."""
        sensitive_patterns = [
            '.env', 'password', 'secret', 'key', 'token',
            'credential', 'private', '.pem', '.key'
        ]
        path_lower = path.lower()
        return any(pattern in path_lower for pattern in sensitive_patterns)

    def _is_system_path(self, path: str) -> bool:
        """Check if a path is a system path."""
        system_patterns = [
            '/etc/', '/usr/', '/bin/', '/sbin/',
            'C:\\Windows', 'C:\\Program Files',
            '/System/', '/Library/'
        ]
        return any(pattern in path for pattern in system_patterns)

    def add_rule(self, rule: Rule) -> None:
        """Add a new rule."""
        self._rules.append(rule)

    def remove_rule(self, name: str) -> bool:
        """Remove a rule by name."""
        original_count = len(self._rules)
        self._rules = [r for r in self._rules if r.name != name]
        return len(self._rules) < original_count

    def check(self, context: dict) -> tuple[RuleResult, list[str]]:
        """
        Check all rules against the given context.

        Returns:
            Tuple of (overall result, list of messages)
        """
        messages = []
        overall_result = RuleResult.ALLOW

        for rule in self._rules:
            try:
                result = rule.check(context)

                if result == RuleResult.DENY:
                    messages.append(f"BLOCKED by {rule.name}: {rule.description}")
                    overall_result = RuleResult.DENY
                    self._log_violation(rule, context, "denied")

                elif result == RuleResult.WARN:
                    messages.append(f"WARNING from {rule.name}: {rule.description}")
                    if overall_result != RuleResult.DENY:
                        overall_result = RuleResult.WARN
                    self._log_violation(rule, context, "warned")

            except Exception as e:
                messages.append(f"Rule {rule.name} error: {str(e)}")

        return overall_result, messages

    def _log_violation(self, rule: Rule, context: dict, action: str) -> None:
        """Log a rule violation."""
        from datetime import datetime
        self._violations.append({
            "timestamp": datetime.now().isoformat(),
            "rule": rule.name,
            "category": rule.category,
            "severity": rule.severity,
            "action": action,
            "context": str(context)[:200]
        })

    def get_violations(self) -> list[dict]:
        """Get the violation log."""
        return self._violations.copy()

    def clear_violations(self) -> None:
        """Clear the violation log."""
        self._violations.clear()

    def list_rules(self) -> list[dict]:
        """List all rules."""
        return [
            {
                "name": r.name,
                "description": r.description,
                "category": r.category,
                "severity": r.severity
            }
            for r in self._rules
        ]

    def get_rules_by_category(self, category: str) -> list[Rule]:
        """Get rules in a specific category."""
        return [r for r in self._rules if r.category == category]

    def create_action_context(
        self,
        action: str,
        file_path: Optional[str] = None,
        value: Optional[Any] = None,
        confirmed: bool = False,
        **kwargs
    ) -> dict:
        """
        Helper to create a context dict for rule checking.

        This ensures consistent context structure.
        """
        ctx = {
            "action": action,
            "confirmed": confirmed,
            **kwargs
        }
        if file_path:
            ctx["file_path"] = file_path
        if value is not None:
            ctx["value"] = value
        return ctx
