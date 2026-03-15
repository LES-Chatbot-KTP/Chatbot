"""Conversa model — user conversations/sessions."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class Conversa(Base):
    __tablename__ = "conversa"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    usuario = relationship("Usuario", back_populates="conversas")
    perguntas = relationship(
        "Pergunta", back_populates="conversa", order_by="Pergunta.criado_em"
    )
