"""Pergunta model — user questions within a conversation."""

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class Pergunta(Base):
    __tablename__ = "pergunta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversa_id = Column(Integer, ForeignKey("conversa.id"), nullable=False)
    texto_original = Column(Text, nullable=False)
    texto_processado = Column(Text, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    conversa = relationship("Conversa", back_populates="perguntas")
    resposta = relationship("Resposta", back_populates="pergunta", uselist=False)
