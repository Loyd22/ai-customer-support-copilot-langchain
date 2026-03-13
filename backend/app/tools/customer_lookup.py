"""
Customer lookup tool.

This module provides a simple tool function for retrieving customer details
from the customer repository.
"""

from app.repositories.customer_repository import customer_repository


def customer_lookup(customer_id: str) -> dict:
    """Return customer details for the given customer ID."""
    customer = customer_repository.get_by_customer_id(customer_id)

    if not customer:
        return {
            "found": False,
            "message": f"Customer {customer_id} was not found."
        }

    return {
        "found": True,
        "data": customer
    }