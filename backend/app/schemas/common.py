"""
Common response schemas used across backend routes.

This module contains shared Pydantic models for simple and reusable
API responses like health checks and status messages.
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Represent the response returned by the health check endpoint."""

    status: str


class MessageResponse(BaseModel):
    """Represent a simple message response for placeholder endpoints."""

    message: str