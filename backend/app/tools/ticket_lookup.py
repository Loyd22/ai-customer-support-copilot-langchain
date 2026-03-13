"""
Ticket lookup tool.

This module provides a simple tool function for retrieving ticket details
from the ticket repository.
"""

from app.repositories.ticket_repository import ticket_repository


def ticket_lookup(ticket_id: str) -> dict:
    """Return ticket details for the given ticket ID."""
    ticket = ticket_repository.get_by_ticket_id(ticket_id)

    if not ticket:
        return {
            "found": False,
            "message": f"Ticket {ticket_id} was not found."
        }

    return {
        "found": True,
        "data": ticket
    }