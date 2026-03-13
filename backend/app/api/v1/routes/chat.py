"""
Chat route definitions.

This module contains the main chat endpoint. It uses the chat service
to automatically route requests to either RAG or structured tools.
"""

from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse, EscalationInfo, SourceItem
from app.services.chat_service import handle_chat

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    """Handle a user chat message through the main orchestration service."""
    result = handle_chat(
        session_id=payload.session_id,
        message=payload.message,
    )

    return ChatResponse(
        answer=result["answer"],
        action=result["action"],
        used_tools=result["used_tools"],
        sources=[SourceItem(**source) for source in result["sources"]],
        memory_summary=result["memory_summary"],
        escalation=EscalationInfo(**result["escalation"]),
    )