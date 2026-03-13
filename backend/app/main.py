"""
Main FastAPI application entry point.

This module creates the FastAPI app, applies metadata, and registers the
versioned API routes for the AI Customer Support Copilot backend.
"""

from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.config import settings


def create_application() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI(
        title=settings.APP_NAME,
        version="0.1.0",
        debug=settings.DEBUG,
    )

    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    return app


app = create_application()