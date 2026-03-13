"""
Retriever utilities for the RAG pipeline.

This module loads the persisted Chroma vector store and exposes a retriever
that can fetch the most relevant chunks for a user question.
"""

from langchain_community.vectorstores import Chroma

from app.core.config import settings
from app.rag.embeddings import get_embedding_model


def get_vectorstore() -> Chroma:
    """Load and return the persisted Chroma vector store."""
    return Chroma(
        persist_directory=settings.CHROMA_PERSIST_DIR,
        embedding_function=get_embedding_model(),
    )


def get_retriever(search_k: int = 4):
    """Return a retriever configured to fetch the top matching chunks."""
    vectorstore = get_vectorstore()
    return vectorstore.as_retriever(search_kwargs={"k": search_k})