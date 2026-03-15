"""Usuario model — system users."""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    ativo = Column(Boolean, default=True)
    perfil_id = Column(Integer, ForeignKey("perfil.id"), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    perfil = relationship("Perfil", back_populates="usuarios")
    conversas = relationship("Conversa", back_populates="usuario")
    logs = relationship("LogAdministrativo", back_populates="usuario")
