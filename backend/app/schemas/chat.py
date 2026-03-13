"""
Chat-related request and response schemas.

This module defines the input and output contracts for the main chat API.
The current version is a skeleton and will be expanded later.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class EscalationInfo(BaseModel):
    """Represent escalation status returned by the chat endpoint."""

    needed: bool = False
    reason: Optional[str] = None


class SourceItem(BaseModel):
    """Represent a single retrieval source item for grounded answers."""

    source_id: str
    title: str
    snippet: str


class ChatRequest(BaseModel):
    """Represent the request body sent to the chat endpoint."""

    session_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    """Represent the structured response returned by the chat endpoint."""

    answer: str
    action: str
    used_tools: List[str]
    sources: List[SourceItem]
    memory_summary: str
    escalation: EscalationInfo