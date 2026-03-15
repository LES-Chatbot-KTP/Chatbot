"""EmbeddingChunk model — vector embeddings for document chunks."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.database import Base
from app.config import settings


class EmbeddingChunk(Base):
    __tablename__ = "embedding_chunk"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chunk_id = Column(
        Integer, ForeignKey("documento_chunk.id"), unique=True, nullable=False
    )
    embedding = Column(Vector(settings.embedding_dimension), nullable=False)
    modelo = Column(String(100), nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    chunk = relationship("DocumentoChunk", back_populates="embedding")
