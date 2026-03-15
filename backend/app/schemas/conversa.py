"""Conversation and chat schemas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ConversaCreate(BaseModel):
    titulo: str | None = None


class ConversaResponse(BaseModel):
    id: int
    titulo: str | None
    usuario_id: int
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)


class PerguntaRequest(BaseModel):
    texto: str


class FonteResponse(BaseModel):
    documento_titulo: str
    chunk_conteudo: str
    similaridade: float | None = None


class RespostaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pergunta_id: int
    texto: str
    modelo_usado: str | None = None
    fontes: list[FonteResponse] = []
    criado_em: datetime


class PerguntaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    conversa_id: int
    texto_original: str
    texto_processado: str | None = None
    resposta: RespostaResponse | None = None
    criado_em: datetime


class ChatResponse(BaseModel):
    pergunta: PerguntaResponse
    resposta: RespostaResponse
