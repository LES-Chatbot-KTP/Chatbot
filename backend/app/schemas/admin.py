"""Admin panel schemas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LogAdministrativoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    acao: str
    entidade: str | None = None
    entidade_id: int | None = None
    detalhes: str | None = None
    criado_em: datetime


class MetricasResponse(BaseModel):
    total_usuarios: int
    total_conversas: int
    total_perguntas: int
    total_documentos: int
    total_documentos_ativos: int
    media_avaliacoes: float | None = None
    total_avaliacoes: int
