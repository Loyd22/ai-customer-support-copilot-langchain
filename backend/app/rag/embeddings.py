"""
Embedding utilities for the RAG pipeline.

This module creates the embedding model used to convert text chunks into
vector representations for semantic search.
"""

from langchain_openai import OpenAIEmbeddings

from app.core.config import settings


def get_embedding_model() -> OpenAIEmbeddings:
    """Return the OpenAI embedding model configured for the app."""
    print("DEBUG OPENAI_API_KEY loaded:", bool(settings.OPENAI_API_KEY))
    print("DEBUG EMBEDDING_MODEL:", settings.EMBEDDING_MODEL)

    return OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        api_key=settings.OPENAI_API_KEY,
    )