"""
Order lookup tool.

This module provides a simple tool function for retrieving order details
from the order repository.
"""

from app.repositories.order_repository import order_repository


def order_lookup(order_id: str) -> dict:
    """Return order details for the given order ID."""
    order = order_repository.get_by_order_id(order_id)

    if not order:
        return {
            "found": False,
            "message": f"Order {order_id} was not found."
        }

    return {
        "found": True,
        "data": order
    }