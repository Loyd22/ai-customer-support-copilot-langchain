"""
Session-related schemas.

This module defines models for session retrieval and reset operations.
"""

from typing import List

from pydantic import BaseModel


class ChatMessage(BaseModel):
    """Represent a single chat message stored in session history."""

    role: str
    content: str


class SessionResponse(BaseModel):
    """Represent the session history and memory summary response."""

    session_id: str
    messages: List[ChatMessage]
    memory_summary: str


class SessionClearResponse(BaseModel):
    """Represent the response after clearing a session."""

    status: str
    session_id: str