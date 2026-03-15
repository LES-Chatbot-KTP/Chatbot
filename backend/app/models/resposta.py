"""Resposta model — AI-generated answers."""

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class Resposta(Base):
    __tablename__ = "resposta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pergunta_id = Column(Integer, ForeignKey("pergunta.id"), unique=True, nullable=False)
    texto = Column(Text, nullable=False)
    modelo_usado = Column(Text, nullable=True)
    tokens_prompt = Column(Integer, nullable=True)
    tokens_resposta = Column(Integer, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    pergunta = relationship("Pergunta", back_populates="resposta")
    avaliacao = relationship("Avaliacao", back_populates="resposta", uselist=False)
    documentos_resposta = relationship("DocumentoResposta", back_populates="resposta")
    fontes = relationship("RespostaFonte", back_populates="resposta")
