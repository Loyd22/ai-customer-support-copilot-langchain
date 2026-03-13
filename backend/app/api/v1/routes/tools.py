"""
Tool testing route definitions.

This module provides temporary endpoints for testing mock lookup tools
before automatic routing is added.
"""

from fastapi import APIRouter, HTTPException

from app.services.tool_service import lookup_customer, lookup_order, lookup_ticket

router = APIRouter()


@router.get("/tools/orders/{order_id}")
def get_order(order_id: str) -> dict:
    """Return order lookup results for the given order ID."""
    result = lookup_order(order_id)

    if not result["found"]:
        raise HTTPException(status_code=404, detail=result["message"])

    return result


@router.get("/tools/tickets/{ticket_id}")
def get_ticket(ticket_id: str) -> dict:
    """Return ticket lookup results for the given ticket ID."""
    result = lookup_ticket(ticket_id)

    if not result["found"]:
        raise HTTPException(status_code=404, detail=result["message"])

    return result


@router.get("/tools/customers/{customer_id}")
def get_customer(customer_id: str) -> dict:
    """Return customer lookup results for the given customer ID."""
    result = lookup_customer(customer_id)

    if not result["found"]:
        raise HTTPException(status_code=404, detail=result["message"])

    return result