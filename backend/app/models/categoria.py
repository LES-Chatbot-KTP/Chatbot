"""Categoria model — document categories."""

from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), unique=True, nullable=False)
    descricao = Column(Text, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    documentos = relationship("Documento", back_populates="categoria")
