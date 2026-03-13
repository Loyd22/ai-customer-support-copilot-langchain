"""
Ticket repository for reading mock ticket data.

This module loads ticket records from a JSON file and provides lookup
methods for retrieving tickets by ID.
"""

import json
from pathlib import Path
from typing import Optional


class TicketRepository:
    """Provide read access to mock ticket records."""

    def __init__(self) -> None:
        """Initialize the repository with the tickets JSON file path."""
        self.file_path = Path("app/data/mock/tickets.json")

    def _load_tickets(self) -> list[dict]:
        """Load and return all ticket records from the JSON file."""
        with self.file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def get_by_ticket_id(self, ticket_id: str) -> Optional[dict]:
        """Return a single ticket that matches the given ticket ID."""
        tickets = self._load_tickets()

        for ticket in tickets:
            if ticket["ticket_id"] == ticket_id:
                return ticket

        return None


ticket_repository = TicketRepository()