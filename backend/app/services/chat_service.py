"""
Chat orchestration service for the AI Customer Support Copilot.

This module coordinates routing, memory, RAG answering, tool lookups,
and escalation detection so the chat endpoint can return one structured response.
"""

from app.services.escalation_service import check_escalation
from app.services.memory_service import (
    build_memory_summary,
    save_assistant_message,
    save_user_message,
)
from app.services.rag_service import answer_with_rag
from app.services.routing_service import classify_route
from app.services.tool_service import lookup_customer, lookup_order, lookup_ticket


def format_tool_answer(tool_name: str, result: dict) -> str:
    """Format tool lookup results into a user-friendly answer."""
    data = result["data"]

    if tool_name == "order_lookup":
        return (
            f"Order {data['order_id']} is currently {data['status']}. "
            f"Estimated delivery is {data['estimated_delivery']}. "
            f"Tracking number: {data['tracking_number']}."
        )

    if tool_name == "ticket_lookup":
        return (
            f"Ticket {data['ticket_id']} is currently {data['status']} "
            f"with priority {data['priority']}. "
            f"Subject: {data['subject']}."
        )

    if tool_name == "customer_lookup":
        return (
            f"Customer {data['customer_id']} is {data['name']} "
            f"with email {data['email']} and tier {data['tier']}."
        )

    return "The requested tool result could not be formatted."


def handle_chat(session_id: str, message: str) -> dict:
    """Handle a chat message by routing it to RAG or a lookup tool."""
    save_user_message(session_id, message)

    route_info = classify_route(message)
    escalation = check_escalation(message)

    if route_info["route"] == "tool":
        tool_name = route_info["tool_name"]
        entity_id = route_info["entity_id"]

        if tool_name == "order_lookup":
            result = lookup_order(entity_id)
        elif tool_name == "ticket_lookup":
            result = lookup_ticket(entity_id)
        elif tool_name == "customer_lookup":
            result = lookup_customer(entity_id)
        else:
            result = {"found": False, "message": "Unknown tool route."}

        if result["found"]:
            answer = format_tool_answer(tool_name, result)
            used_tools = [tool_name]
        else:
            answer = result["message"]
            used_tools = [tool_name] if tool_name else []

        if escalation["needed"]:
            answer = f"{answer} This case should be reviewed by a human support agent."

        save_assistant_message(session_id, answer)

        return {
            "answer": answer,
            "action": "tool",
            "used_tools": used_tools,
            "sources": [],
            "memory_summary": build_memory_summary(session_id),
            "escalation": escalation,
        }

    rag_result = answer_with_rag(
        question=message,
        session_id=session_id,
    )

    answer = rag_result["answer"]

    if escalation["needed"]:
        answer = f"{answer}\n\nThis case should be reviewed by a human support agent."

    save_assistant_message(session_id, answer)

    return {
        "answer": answer,
        "action": "rag",
        "used_tools": [],
        "sources": rag_result["sources"],
        "memory_summary": build_memory_summary(session_id),
        "escalation": escalation,
    }