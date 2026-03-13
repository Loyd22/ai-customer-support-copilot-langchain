"""
RAG service for grounded question answering.

This module retrieves relevant chunks from Chroma, builds grounded context,
uses recent session history, calls the LLM, and formats sources for the
API response.
"""

from typing import Dict, List

from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.prompts.answer_prompt import RAG_ANSWER_PROMPT
from app.rag.retriever import get_retriever
from app.services.memory_service import get_recent_messages


def format_context(documents) -> str:
    """Convert retrieved documents into a single context string."""
    context_parts = []

    for index, doc in enumerate(documents, start=1):
        source_file = doc.metadata.get("source_file", "unknown")
        chunk_id = doc.metadata.get("chunk_id", "unknown")

        context_parts.append(
            f"[Source {index}] file={source_file}, chunk={chunk_id}\n{doc.page_content}"
        )

    return "\n\n".join(context_parts)


def format_sources(documents) -> List[Dict]:
    """Convert retrieved documents into frontend-friendly source objects."""
    sources = []

    for doc in documents:
        sources.append(
            {
                "source_id": f"{doc.metadata.get('source_file', 'unknown')}#chunk-{doc.metadata.get('chunk_id', 'unknown')}",
                "title": doc.metadata.get("source_file", "unknown"),
                "snippet": doc.page_content[:200],
            }
        )

    return sources


def format_chat_history(session_id: str) -> str:
    """Convert recent session messages into prompt-friendly chat history."""
    messages = get_recent_messages(session_id=session_id, limit=6)

    if not messages:
        return "No prior conversation."

    return "\n".join(
        f"{message['role'].capitalize()}: {message['content']}"
        for message in messages
    )


def answer_with_rag(question: str, session_id: str) -> dict:
    """Retrieve relevant chunks and generate a grounded answer with memory."""
    retriever = get_retriever(search_k=4)
    documents = retriever.invoke(question)

    context = format_context(documents)
    chat_history = format_chat_history(session_id=session_id)

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=settings.OPENAI_API_KEY,
        temperature=0,
    )

    prompt = RAG_ANSWER_PROMPT.format(
        chat_history=chat_history,
        question=question,
        context=context,
    )

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": format_sources(documents),
    }