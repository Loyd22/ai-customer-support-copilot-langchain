"""
Routing service for deciding how a chat request should be handled.

This module uses simple deterministic rules to decide whether a user
question should go to the RAG pipeline or to a structured lookup tool.
"""

import re


def extract_order_id(message: str) -> str | None:
    """Extract an order ID from the user message if present."""
    match = re.search(r"\b(10\d{2,})\b", message)
    return match.group(1) if match else None


def extract_ticket_id(message: str) -> str | None:
    """Extract a ticket ID from the user message if present."""
    match = re.search(r"\b(T-\d+)\b", message, re.IGNORECASE)
    return match.group(1).upper() if match else None


def extract_customer_id(message: str) -> str | None:
    """Extract a customer ID from the user message if present."""
    match = re.search(r"\b(cust_\d+)\b", message, re.IGNORECASE)
    return match.group(1).lower() if match else None


def classify_route(message: str) -> dict:
    """Classify the user message into rag or tool route."""
    lowered = message.lower()

    order_id = extract_order_id(message)
    ticket_id = extract_ticket_id(message)
    customer_id = extract_customer_id(message)

    if "order" in lowered and order_id:
        return {
            "route": "tool",
            "tool_name": "order_lookup",
            "entity_id": order_id,
        }

    if "ticket" in lowered and ticket_id:
        return {
            "route": "tool",
            "tool_name": "ticket_lookup",
            "entity_id": ticket_id,
        }

    if "customer" in lowered and customer_id:
        return {
            "route": "tool",
            "tool_name": "customer_lookup",
            "entity_id": customer_id,
        }

    return {
        "route": "rag",
        "tool_name": None,
        "entity_id": None,
    }