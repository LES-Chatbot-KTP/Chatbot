"""DocumentoChunk model — text chunks extracted from document versions."""

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class DocumentoChunk(Base):
    __tablename__ = "documento_chunk"

    id = Column(Integer, primary_key=True, autoincrement=True)
    documento_id = Column(Integer, ForeignKey("documento.id"), nullable=False)
    versao_documento_id = Column(
        Integer, ForeignKey("versao_documento.id"), nullable=False
    )
    indice = Column(Integer, nullable=False)
    conteudo = Column(Text, nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    documento = relationship("Documento", back_populates="chunks")
    versao = relationship("VersaoDocumento")
    embedding = relationship(
        "EmbeddingChunk", back_populates="chunk", uselist=False
    )
