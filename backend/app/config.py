"""Application settings loaded from environment variables."""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Central configuration loaded from environment."""

    # Database
    database_url: str = "postgresql://chatbot:chatbot_secret@localhost:5432/chatbot_db"

    # JWT
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # OpenAI
    openai_api_key: str = ""
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4o-mini"
    embedding_dimension: int = 1536

    # RAG
    top_k: int = 5
    chunk_size: int = 500
    chunk_overlap: int = 50

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
