"""
Session route definitions.

This module contains endpoints for reading and clearing session
memory/history.
"""

from fastapi import APIRouter

from app.schemas.session import (
    ChatMessage,
    SessionClearResponse,
    SessionResponse,
)
from app.services.memory_service import (
    build_memory_summary,
    clear_session_memory,
    get_session_messages,
)

router = APIRouter()


@router.get("/sessions/{session_id}", response_model=SessionResponse)
def get_session(session_id: str) -> SessionResponse:
    """Return the real session history for the given session ID."""
    stored_messages = get_session_messages(session_id)

    return SessionResponse(
        session_id=session_id,
        messages=[ChatMessage(**message) for message in stored_messages],
        memory_summary=build_memory_summary(session_id),
    )


@router.delete("/sessions/{session_id}", response_model=SessionClearResponse)
def clear_session(session_id: str) -> SessionClearResponse:
    """Clear the real session history for the given session ID."""
    clear_session_memory(session_id)

    return SessionClearResponse(
        status="cleared",
        session_id=session_id,
    )