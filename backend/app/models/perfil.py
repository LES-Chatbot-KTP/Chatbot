"""Perfil model — user role profiles (e.g. comum, administrador)."""

from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class Perfil(Base):
    __tablename__ = "perfil"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), unique=True, nullable=False)
    descricao = Column(String(255), nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    usuarios = relationship("Usuario", back_populates="perfil")
