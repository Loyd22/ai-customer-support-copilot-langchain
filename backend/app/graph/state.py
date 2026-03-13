"""
State definition for the LangGraph support workflow.

This module defines the shared state passed between LangGraph nodes.
Each node reads from and writes to this state as the workflow progresses.
"""

from typing import Any, Dict, List, Optional

from typing_extensions import TypedDict


class SupportGraphState(TypedDict, total=False):
    """Represent the shared state used across the support workflow graph."""

    session_id: str
    message: str

    memory_messages: List[Dict[str, str]]
    route: str
    tool_name: Optional[str]
    entity_id: Optional[str]

    rag_result: Dict[str, Any]
    tool_result: Dict[str, Any]
    escalation: Dict[str, Any]

    answer: str
    action: str
    used_tools: List[str]
    sources: List[Dict[str, Any]]
    memory_summary: str