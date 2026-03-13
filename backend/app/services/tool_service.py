"""
Tool service for structured data lookups.

This module provides a service layer that wraps the available lookup tools
for orders, tickets, and customers.
"""

from app.tools.customer_lookup import customer_lookup
from app.tools.order_lookup import order_lookup
from app.tools.ticket_lookup import ticket_lookup


def lookup_order(order_id: str) -> dict:
    """Look up an order by order ID."""
    return order_lookup(order_id)


def lookup_ticket(ticket_id: str) -> dict:
    """Look up a ticket by ticket ID."""
    return ticket_lookup(ticket_id)


def lookup_customer(customer_id: str) -> dict:
    """Look up a customer by customer ID."""
    return customer_lookup(customer_id)