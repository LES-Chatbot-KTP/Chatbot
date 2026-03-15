"""VersaoDocumento model — document version history."""

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class VersaoDocumento(Base):
    __tablename__ = "versao_documento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    documento_id = Column(Integer, ForeignKey("documento.id"), nullable=False)
    numero_versao = Column(Integer, nullable=False, default=1)
    conteudo = Column(Text, nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    documento = relationship("Documento", back_populates="versoes")
