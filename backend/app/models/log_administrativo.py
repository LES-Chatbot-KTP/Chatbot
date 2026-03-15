"""LogAdministrativo model — admin activity logs."""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class LogAdministrativo(Base):
    __tablename__ = "log_administrativo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    acao = Column(String(100), nullable=False)
    entidade = Column(String(100), nullable=True)
    entidade_id = Column(Integer, nullable=True)
    detalhes = Column(Text, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("Usuario", back_populates="logs")
