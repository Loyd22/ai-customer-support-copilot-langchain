"""
Order repository for reading mock order data.

This module loads order records from a JSON file and provides lookup
methods for retrieving orders by ID.
"""

import json
from pathlib import Path
from typing import Optional


class OrderRepository:
    """Provide read access to mock order records."""

    def __init__(self) -> None:
        """Initialize the repository with the orders JSON file path."""
        self.file_path = Path("app/data/mock/orders.json")

    def _load_orders(self) -> list[dict]:
        """Load and return all order records from the JSON file."""
        with self.file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def get_by_order_id(self, order_id: str) -> Optional[dict]:
        """Return a single order that matches the given order ID."""
        orders = self._load_orders()

        for order in orders:
            if order["order_id"] == order_id:
                return order

        return None


order_repository = OrderRepository()