"""
Health check route for the backend.

This module provides a simple endpoint used to verify that the FastAPI
application is running correctly.
"""

from fastapi import APIRouter

from app.schemas.common import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Return a simple health status for backend verification."""
    return HealthResponse(status="ok")