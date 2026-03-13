"""
Document loading utilities for the RAG pipeline.

This module loads PDF documents from a directory and returns them as
LangChain Document objects for downstream chunking and indexing.
"""

from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader


def load_pdf_documents(docs_dir: str) -> List[Document]:
    """Load all PDF documents from the given directory."""
    documents: List[Document] = []

    pdf_paths = list(Path(docs_dir).glob("*.pdf"))

    for pdf_path in pdf_paths:
        loader = PyPDFLoader(str(pdf_path))
        loaded_docs = loader.load()

        for doc in loaded_docs:
            doc.metadata["source_file"] = pdf_path.name

        documents.extend(loaded_docs)

    return documents