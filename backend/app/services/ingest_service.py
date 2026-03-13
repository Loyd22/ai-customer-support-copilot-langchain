"""
Document ingestion service for the RAG pipeline.

This module orchestrates document loading, chunking, embedding, and
indexing into the Chroma vector store.
"""

from app.rag.loader import load_pdf_documents
from app.rag.splitter import split_documents
from app.rag.vectorstore import index_documents


def ingest_documents(docs_dir: str) -> dict:
    """Load, split, and index documents from the given directory."""
    documents = load_pdf_documents(docs_dir)
    chunks = split_documents(documents)
    index_documents(chunks)

    return {
        "status": "success",
        "documents_indexed": len(documents),
        "chunks_created": len(chunks),
    }