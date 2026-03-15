"""Evaluation schemas."""

from datetime import datetime
from pydantic import BaseModel, Field


class AvaliacaoCreate(BaseModel):
    resposta_id: int
    nota: int = Field(ge=1, le=5)
    comentario: str | None = None


class AvaliacaoResponse(BaseModel):
    id: int
    resposta_id: int
    nota: int
    comentario: str | None = None
    criado_em: datetime

    class Config:
        from_attributes = True
