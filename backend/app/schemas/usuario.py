"""User schemas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    perfil_id: int


class UsuarioUpdate(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    ativo: bool | None = None
    perfil_id: int | None = None


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    ativo: bool
    perfil_id: int
    perfil_nome: str | None = None
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)


class PerfilResponse(BaseModel):
    id: int
    nome: str
    descricao: str | None = None

    model_config = ConfigDict(from_attributes=True)
