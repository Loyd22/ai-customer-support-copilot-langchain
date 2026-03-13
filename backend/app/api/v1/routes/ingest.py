"""
Document ingestion route definitions.

This module provides the API endpoint that triggers loading support
documents, splitting them into chunks, embedding them, and storing them
in Chroma for future retrieval.
"""

from fastapi import APIRouter

from app.core.config import settings
from app.schemas.ingest import IngestResponse
from app.services.ingest_service import ingest_documents

router = APIRouter()


@router.post("/ingest", response_model=IngestResponse)
def ingest_route() -> IngestResponse:
    """Run the document ingestion pipeline for support documents."""
    result = ingest_documents(settings.DOCS_DIR)

    return IngestResponse(
        status=result["status"],
        documents_indexed=result["documents_indexed"],
        chunks_created=result["chunks_created"],
    )