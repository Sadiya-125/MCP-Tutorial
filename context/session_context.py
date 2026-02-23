"""
Session Context
===============
Current session state - ephemeral, resets on restart.
"""

from dataclasses import dataclass, field
from typing import Optional, Any
from datetime import datetime


@dataclass
class SessionContext:
    """
    Session context - current session state.

    Contains:
    - Session metadata
    - Conversation history summary
    - Temporary state
    """

    # Session identity
    session_id: str = field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S"))
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())

    # User info (for this session)
    user_name: Optional[str] = None
    user_preferences: dict = field(default_factory=dict)

    # Conversation summary
    topics_discussed: list = field(default_factory=list)
    decisions_made: list = field(default_factory=list)
    questions_asked: list = field(default_factory=list)

    # Temporary state
    temp_data: dict = field(default_factory=dict)
    clipboard: Optional[str] = None
    last_response: Optional[str] = None

    # Interaction tracking
    message_count: int = 0
    error_count: int = 0

    def add_topic(self, topic: str) -> None:
        """Add a topic to the discussion list."""
        if topic not in self.topics_discussed:
            self.topics_discussed.append(topic)

    def add_decision(self, decision: str) -> None:
        """Record a decision made."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.decisions_made.append(f"[{timestamp}] {decision}")

    def set_temp(self, key: str, value: Any) -> None:
        """Set temporary data."""
        self.temp_data[key] = value

    def get_temp(self, key: str, default: Any = None) -> Any:
        """Get temporary data."""
        return self.temp_data.get(key, default)

    def increment_messages(self) -> None:
        """Increment message counter."""
        self.message_count += 1

    def increment_errors(self) -> None:
        """Increment error counter."""
        self.error_count += 1

    def get_duration(self) -> str:
        """Get session duration."""
        start = datetime.fromisoformat(self.started_at)
        duration = datetime.now() - start
        minutes = int(duration.total_seconds() // 60)
        seconds = int(duration.total_seconds() % 60)
        return f"{minutes}m {seconds}s"

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "session_id": self.session_id,
            "started_at": self.started_at,
            "user_name": self.user_name,
            "topics_discussed": self.topics_discussed,
            "message_count": self.message_count,
            "duration": self.get_duration()
        }

    def to_prompt_string(self) -> str:
        """Convert to string for prompt injection."""
        lines = [
            "[SESSION CONTEXT]",
            f"Session: {self.session_id}",
            f"Duration: {self.get_duration()}",
            f"Messages: {self.message_count}",
        ]

        if self.user_name:
            lines.append(f"User: {self.user_name}")

        if self.topics_discussed:
            lines.append(f"Topics: {', '.join(self.topics_discussed[-5:])}")

        if self.decisions_made:
            lines.append("Recent Decisions:")
            for decision in self.decisions_made[-3:]:
                lines.append(f"  - {decision}")

        return "\n".join(lines)
