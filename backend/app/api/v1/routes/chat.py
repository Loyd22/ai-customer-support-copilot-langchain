"""
Chat route definitions.

This module contains the main chat endpoint. It invokes the LangGraph
workflow to process support questions through state-based orchestration.
"""

from fastapi import APIRouter

from app.graph.support_graph import support_graph
from app.schemas.chat import ChatRequest, ChatResponse, EscalationInfo, SourceItem

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    """Handle a user chat message through the LangGraph workflow."""
    result = support_graph.invoke(
        {
            "session_id": payload.session_id,
            "message": payload.message,
        }
    )

    return ChatResponse(
        answer=result["answer"],
        action=result["action"],
        used_tools=result["used_tools"],
        sources=[SourceItem(**source) for source in result["sources"]],
        memory_summary=result["memory_summary"],
        escalation=EscalationInfo(**result["escalation"]),
    )