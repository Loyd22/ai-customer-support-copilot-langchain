"""
Memory service for session-based chat context.

This module provides helper functions for storing chat history, retrieving
recent messages, and generating a simple memory summary for a session.
"""

from typing import List

from app.repositories.session_repository import session_repository


def get_session_messages(session_id: str) -> List[dict]:
    """Return all stored messages for a session."""
    return session_repository.get_messages(session_id)


def get_recent_messages(session_id: str, limit: int = 6) -> List[dict]:
    """Return the most recent messages for a session."""
    messages = session_repository.get_messages(session_id)
    return messages[-limit:]


def save_user_message(session_id: str, content: str) -> None:
    """Save a user message to the session history."""
    session_repository.add_message(session_id, "user", content)


def save_assistant_message(session_id: str, content: str) -> None:
    """Save an assistant message to the session history."""
    session_repository.add_message(session_id, "assistant", content)


def clear_session_memory(session_id: str) -> None:
    """Clear all stored messages for a session."""
    session_repository.clear_session(session_id)


def build_memory_summary(session_id: str) -> str:
    """Build a simple text summary from the recent session messages."""
    messages = get_recent_messages(session_id, limit=4)

    if not messages:
        return "No memory yet for this session."

    summary_parts = []
    for message in messages:
        summary_parts.append(f"{message['role']}: {message['content']}")

    return " | ".join(summary_parts)