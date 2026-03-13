"""
Application configuration for the AI Customer Support Copilot backend.

This module centralizes environment-based settings so the app can read
its app metadata, document paths, model choices, and vector store paths
from one place.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Store application settings loaded from environment variables."""

    APP_NAME: str = "AI Customer Support Copilot"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    OPENAI_API_KEY: str = ""
    EMBEDDING_MODEL: str = "text-embedding-3-small"

    DOCS_DIR: str = "app/data/docs"
    CHROMA_PERSIST_DIR: str = "app/data/chroma"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def get_settings() -> Settings:
    """Return a Settings instance for the application."""
    return Settings()


settings = get_settings()