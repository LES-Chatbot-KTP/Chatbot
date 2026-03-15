"""User management routes (admin only)."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_admin_user
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.services import usuario_service
from app.services.admin_service import create_log

router = APIRouter(prefix="/api/usuarios", tags=["Usuários"])


@router.post("/", response_model=UsuarioResponse, status_code=201)
def create_user(
    data: UsuarioCreate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_admin_user),
):
    """Create a new user (admin only)."""
    user = usuario_service.create_usuario(db, data)
    create_log(db, admin.id, "criar_usuario", "usuario", user.id)
    return UsuarioResponse(
        id=user.id,
        nome=user.nome,
        email=user.email,
        ativo=user.ativo,
        perfil_id=user.perfil_id,
        perfil_nome=user.perfil.nome if user.perfil else None,
        criado_em=user.criado_em,
    )


@router.get("/", response_model=list[UsuarioResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_admin_user),
):
    """List all users (admin only)."""
    users = usuario_service.list_usuarios(db, skip, limit)
    return [
        UsuarioResponse(
            id=u.id,
            nome=u.nome,
            email=u.email,
            ativo=u.ativo,
            perfil_id=u.perfil_id,
            perfil_nome=u.perfil.nome if u.perfil else None,
            criado_em=u.criado_em,
        )
        for u in users
    ]


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def get_user(
    usuario_id: int,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_admin_user),
):
    """Get a user by ID (admin only)."""
    user = usuario_service.get_usuario(db, usuario_id)
    return UsuarioResponse(
        id=user.id,
        nome=user.nome,
        email=user.email,
        ativo=user.ativo,
        perfil_id=user.perfil_id,
        perfil_nome=user.perfil.nome if user.perfil else None,
        criado_em=user.criado_em,
    )


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def update_user(
    usuario_id: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_admin_user),
):
    """Update a user (admin only)."""
    user = usuario_service.update_usuario(db, usuario_id, data)
    create_log(db, admin.id, "atualizar_usuario", "usuario", user.id)
    return UsuarioResponse(
        id=user.id,
        nome=user.nome,
        email=user.email,
        ativo=user.ativo,
        perfil_id=user.perfil_id,
        perfil_nome=user.perfil.nome if user.perfil else None,
        criado_em=user.criado_em,
    )


@router.delete("/{usuario_id}", response_model=UsuarioResponse)
def deactivate_user(
    usuario_id: int,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_admin_user),
):
    """Deactivate a user (admin only)."""
    user = usuario_service.deactivate_usuario(db, usuario_id)
    create_log(db, admin.id, "desativar_usuario", "usuario", user.id)
    return UsuarioResponse(
        id=user.id,
        nome=user.nome,
        email=user.email,
        ativo=user.ativo,
        perfil_id=user.perfil_id,
        perfil_nome=user.perfil.nome if user.perfil else None,
        criado_em=user.criado_em,
    )
