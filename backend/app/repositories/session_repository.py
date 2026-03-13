"""
Session repository for in-memory chat storage.

This module stores chat messages by session ID in an in-memory dictionary.
It is suitable for MVP development and can later be replaced by Redis or
a database-backed implementation.
"""

from typing import Dict, List


class SessionRepository:
    """Store and retrieve session messages in memory."""

    def __init__(self) -> None:
        """Initialize the in-memory session store."""
        self._store: Dict[str, List[dict]] = {}

    def get_messages(self, session_id: str) -> List[dict]:
        """Return all messages for a session ID."""
        return self._store.get(session_id, [])

    def add_message(self, session_id: str, role: str, content: str) -> None:
        """Add a chat message to a session."""
        if session_id not in self._store:
            self._store[session_id] = []

        self._store[session_id].append(
            {
                "role": role,
                "content": content,
            }
        )

    def clear_session(self, session_id: str) -> None:
        """Remove all messages for a session."""
        if session_id in self._store:
            del self._store[session_id]


session_repository = SessionRepository()