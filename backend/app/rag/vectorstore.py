"""
Vector store utilities for the RAG pipeline.

This module creates and persists the Chroma vector store that indexes
document chunks for semantic retrieval.
"""

from typing import List

from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

from app.core.config import settings
from app.rag.embeddings import get_embedding_model


def index_documents(chunks: List[Document]) -> Chroma:
    """Embed and store document chunks in Chroma."""
    embedding_model = get_embedding_model()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=settings.CHROMA_PERSIST_DIR,
    )

    return vectorstore