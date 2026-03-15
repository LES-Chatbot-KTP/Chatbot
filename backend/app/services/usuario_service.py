"""User management service."""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.utils.security import hash_password


def create_usuario(db: Session, data: UsuarioCreate) -> Usuario:
    """Create a new user."""
    existing = db.query(Usuario).filter(Usuario.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado",
        )
    user = Usuario(
        nome=data.nome,
        email=data.email,
        senha_hash=hash_password(data.senha),
        perfil_id=data.perfil_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_usuario(db: Session, usuario_id: int) -> Usuario:
    """Get a user by ID."""
    user = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
        )
    return user


def list_usuarios(db: Session, skip: int = 0, limit: int = 100) -> list[Usuario]:
    """List all users."""
    return db.query(Usuario).offset(skip).limit(limit).all()


def update_usuario(db: Session, usuario_id: int, data: UsuarioUpdate) -> Usuario:
    """Update user fields."""
    user = get_usuario(db, usuario_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def deactivate_usuario(db: Session, usuario_id: int) -> Usuario:
    """Soft-delete a user by setting ativo=False."""
    user = get_usuario(db, usuario_id)
    user.ativo = False
    db.commit()
    db.refresh(user)
    return user
