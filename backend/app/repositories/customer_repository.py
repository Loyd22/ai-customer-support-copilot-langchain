"""
Customer repository for reading mock customer data.

This module loads customer records from a JSON file and provides lookup
methods for retrieving customers by ID.
"""

import json
from pathlib import Path
from typing import Optional


class CustomerRepository:
    """Provide read access to mock customer records."""

    def __init__(self) -> None:
        """Initialize the repository with the customers JSON file path."""
        self.file_path = Path("app/data/mock/customers.json")

    def _load_customers(self) -> list[dict]:
        """Load and return all customer records from the JSON file."""
        with self.file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def get_by_customer_id(self, customer_id: str) -> Optional[dict]:
        """Return a single customer that matches the given customer ID."""
        customers = self._load_customers()

        for customer in customers:
            if customer["customer_id"] == customer_id:
                return customer

        return None


customer_repository = CustomerRepository()