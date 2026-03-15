"""Documento model — uploaded documents."""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class Documento(Base):
    __tablename__ = "documento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=True)
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=True)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    categoria = relationship("Categoria", back_populates="documentos")
    versoes = relationship(
        "VersaoDocumento",
        back_populates="documento",
        order_by="VersaoDocumento.numero_versao.desc()",
    )
    respostas = relationship("DocumentoResposta", back_populates="documento")
    chunks = relationship("DocumentoChunk", back_populates="documento")
