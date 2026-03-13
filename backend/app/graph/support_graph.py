"""
LangGraph workflow for the AI Customer Support Copilot.

This module defines a state-based graph that orchestrates memory loading,
routing, RAG execution, tool execution, escalation checks, response
finalization, and assistant message persistence.
"""

from langgraph.graph import END, START, StateGraph

from app.graph.state import SupportGraphState
from app.services.escalation_service import check_escalation
from app.services.memory_service import (
    build_memory_summary,
    get_recent_messages,
    save_assistant_message,
    save_user_message,
)
from app.services.rag_service import answer_with_rag
from app.services.routing_service import classify_route
from app.services.tool_service import lookup_customer, lookup_order, lookup_ticket


def save_user_message_node(state: SupportGraphState) -> dict:
    """Save the current user message into session memory."""
    save_user_message(state["session_id"], state["message"])
    return {}


def load_memory_node(state: SupportGraphState) -> dict:
    """Load recent memory messages for the current session."""
    memory_messages = get_recent_messages(state["session_id"], limit=6)
    return {"memory_messages": memory_messages}


def route_request_node(state: SupportGraphState) -> dict:
    """Classify the request and store routing details in graph state."""
    route_info = classify_route(state["message"])
    return {
        "route": route_info["route"],
        "tool_name": route_info["tool_name"],
        "entity_id": route_info["entity_id"],
    }


def route_decision(state: SupportGraphState) -> str:
    """Return the next graph branch based on the selected route."""
    return state["route"]


def run_rag_node(state: SupportGraphState) -> dict:
    """Run the RAG pipeline for support-document questions."""
    rag_result = answer_with_rag(
        question=state["message"],
        session_id=state["session_id"],
    )

    return {
        "rag_result": rag_result,
        "answer": rag_result["answer"],
        "action": "rag",
        "used_tools": [],
        "sources": rag_result["sources"],
    }


def run_tool_node(state: SupportGraphState) -> dict:
    """Run the appropriate lookup tool for structured data questions."""
    tool_name = state.get("tool_name")
    entity_id = state.get("entity_id")

    if tool_name == "order_lookup":
        tool_result = lookup_order(entity_id)
    elif tool_name == "ticket_lookup":
        tool_result = lookup_ticket(entity_id)
    elif tool_name == "customer_lookup":
        tool_result = lookup_customer(entity_id)
    else:
        tool_result = {"found": False, "message": "Unknown tool route."}

    if tool_result["found"]:
        data = tool_result["data"]

        if tool_name == "order_lookup":
            answer = (
                f"Order {data['order_id']} is currently {data['status']}. "
                f"Estimated delivery is {data['estimated_delivery']}. "
                f"Tracking number: {data['tracking_number']}."
            )
        elif tool_name == "ticket_lookup":
            answer = (
                f"Ticket {data['ticket_id']} is currently {data['status']} "
                f"with priority {data['priority']}. "
                f"Subject: {data['subject']}."
            )
        elif tool_name == "customer_lookup":
            answer = (
                f"Customer {data['customer_id']} is {data['name']} "
                f"with email {data['email']} and tier {data['tier']}."
            )
        else:
            answer = "The requested tool result could not be formatted."
    else:
        answer = tool_result["message"]

    return {
        "tool_result": tool_result,
        "answer": answer,
        "action": "tool",
        "used_tools": [tool_name] if tool_name else [],
        "sources": [],
    }


def check_escalation_node(state: SupportGraphState) -> dict:
    """Check whether the current message should be escalated."""
    escalation = check_escalation(state["message"])
    return {"escalation": escalation}


def finalize_response_node(state: SupportGraphState) -> dict:
    """Finalize the response text and memory summary for API output."""
    answer = state["answer"]
    escalation = state.get("escalation", {"needed": False, "reason": None})

    if escalation["needed"]:
        answer = f"{answer}\n\nThis case should be reviewed by a human support agent."

    return {
        "answer": answer,
        "memory_summary": build_memory_summary(state["session_id"]),
    }


def save_assistant_message_node(state: SupportGraphState) -> dict:
    """Save the final assistant answer into session memory."""
    save_assistant_message(state["session_id"], state["answer"])

    return {
        "memory_summary": build_memory_summary(state["session_id"]),
    }


def build_support_graph():
    """Build and compile the LangGraph support workflow."""
    workflow = StateGraph(SupportGraphState)

    workflow.add_node("save_user_message", save_user_message_node)
    workflow.add_node("load_memory", load_memory_node)
    workflow.add_node("route_request", route_request_node)
    workflow.add_node("run_rag", run_rag_node)
    workflow.add_node("run_tool", run_tool_node)
    workflow.add_node("check_escalation", check_escalation_node)
    workflow.add_node("finalize_response", finalize_response_node)
    workflow.add_node("save_assistant_message", save_assistant_message_node)

    workflow.add_edge(START, "save_user_message")
    workflow.add_edge("save_user_message", "load_memory")
    workflow.add_edge("load_memory", "route_request")

    workflow.add_conditional_edges(
        "route_request",
        route_decision,
        {
            "rag": "run_rag",
            "tool": "run_tool",
        },
    )

    workflow.add_edge("run_rag", "check_escalation")
    workflow.add_edge("run_tool", "check_escalation")
    workflow.add_edge("check_escalation", "finalize_response")
    workflow.add_edge("finalize_response", "save_assistant_message")
    workflow.add_edge("save_assistant_message", END)

    return workflow.compile()


support_graph = build_support_graph()