"""
API router registration for version 1 routes.

This module gathers all v1 route modules into a single router so the
main FastAPI app can include them cleanly.
"""

from fastapi import APIRouter

from app.api.v1.routes import chat, health, ingest, sessions,tools

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(chat.router, tags=["chat"])
api_router.include_router(ingest.router, tags=["ingest"])
api_router.include_router(sessions.router, tags=["sessions"])
api_router.include_router(tools.router, tags=["tools"])