"""
Chat route definitions.

This module contains the main chat endpoint. In this step, the chat route
uses session memory and the RAG service to answer support-document
questions from Chroma.
"""

from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse, EscalationInfo, SourceItem
from app.services.memory_service import (
    build_memory_summary,
    save_assistant_message,
    save_user_message,
)
from app.services.rag_service import answer_with_rag

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    """Answer a user question using session memory and the RAG pipeline."""
    save_user_message(payload.session_id, payload.message)

    result = answer_with_rag(
        question=payload.message,
        session_id=payload.session_id,
    )

    save_assistant_message(payload.session_id, result["answer"])

    return ChatResponse(
        answer=result["answer"],
        action="rag",
        used_tools=[],
        sources=[SourceItem(**source) for source in result["sources"]],
        memory_summary=build_memory_summary(payload.session_id),
        escalation=EscalationInfo(needed=False, reason=None),
    )