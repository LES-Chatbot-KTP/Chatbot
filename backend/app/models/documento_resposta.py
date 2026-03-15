"""DocumentoResposta model — link between documents and answers."""

from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class DocumentoResposta(Base):
    __tablename__ = "documento_resposta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    documento_id = Column(Integer, ForeignKey("documento.id"), nullable=False)
    resposta_id = Column(Integer, ForeignKey("resposta.id"), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    documento = relationship("Documento", back_populates="respostas")
    resposta = relationship("Resposta", back_populates="documentos_resposta")
