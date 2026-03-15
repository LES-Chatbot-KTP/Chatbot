"""Avaliacao model — user ratings for answers."""

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class Avaliacao(Base):
    __tablename__ = "avaliacao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    resposta_id = Column(Integer, ForeignKey("resposta.id"), unique=True, nullable=False)
    nota = Column(Integer, nullable=False)
    comentario = Column(Text, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    resposta = relationship("Resposta", back_populates="avaliacao")
