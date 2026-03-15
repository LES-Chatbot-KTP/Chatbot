"""IndexacaoJob model — tracks embedding indexing jobs."""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func

from app.database import Base


class IndexacaoJob(Base):
    __tablename__ = "indexacao_job"

    id = Column(Integer, primary_key=True, autoincrement=True)
    documento_id = Column(Integer, ForeignKey("documento.id"), nullable=True)
    status = Column(String(30), nullable=False, default="pendente")
    tipo = Column(String(50), nullable=False, default="indexacao")
    total_chunks = Column(Integer, nullable=True)
    chunks_processados = Column(Integer, default=0)
    erro = Column(Text, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    finalizado_em = Column(DateTime(timezone=True), nullable=True)
