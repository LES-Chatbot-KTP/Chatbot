"""Evaluation schemas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class AvaliacaoCreate(BaseModel):
    resposta_id: int
    nota: int = Field(ge=1, le=5)
    comentario: str | None = None


class AvaliacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    resposta_id: int
    nota: int
    comentario: str | None = None
    criado_em: datetime
