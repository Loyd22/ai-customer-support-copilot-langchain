"""
Ingestion-related schemas.

This module defines placeholder response shapes for the future document
ingestion flow of the RAG pipeline.
"""

from pydantic import BaseModel


class IngestResponse(BaseModel):
    """Represent the response returned by the ingestion endpoint."""

    status: str
    documents_indexed: int
    chunks_created: int