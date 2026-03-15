"""Document schemas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CategoriaCreate(BaseModel):
    nome: str
    descricao: str | None = None


class CategoriaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    descricao: str | None = None
    criado_em: datetime


class DocumentoCreate(BaseModel):
    titulo: str
    descricao: str | None = None
    categoria_id: int | None = None
    conteudo: str


class DocumentoUpdate(BaseModel):
    titulo: str | None = None
    descricao: str | None = None
    categoria_id: int | None = None
    conteudo: str | None = None


class VersaoDocumentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    documento_id: int
    numero_versao: int
    conteudo: str
    criado_em: datetime


class DocumentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    descricao: str | None = None
    categoria_id: int | None = None
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime


class DocumentoDetailResponse(DocumentoResponse):
    versoes: list[VersaoDocumentoResponse] = []


class IndexacaoJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    documento_id: int | None = None
    status: str
    tipo: str
    total_chunks: int | None = None
    chunks_processados: int
    erro: str | None = None
    criado_em: datetime
    finalizado_em: datetime | None = None
