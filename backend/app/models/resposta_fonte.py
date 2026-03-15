"""RespostaFonte model — links answers to the specific chunks used as sources."""

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class RespostaFonte(Base):
    __tablename__ = "resposta_fonte"

    id = Column(Integer, primary_key=True, autoincrement=True)
    resposta_id = Column(Integer, ForeignKey("resposta.id"), nullable=False)
    chunk_id = Column(Integer, ForeignKey("documento_chunk.id"), nullable=False)
    similaridade = Column(Float, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    resposta = relationship("Resposta", back_populates="fontes")
    chunk = relationship("DocumentoChunk")
