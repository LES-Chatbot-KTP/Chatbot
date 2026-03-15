"""Authentication service."""

from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.utils.security import verify_password, create_access_token


def authenticate_user(db: Session, email: str, senha: str) -> Usuario | None:
    """Validate credentials and return the user or None."""
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user or not verify_password(senha, user.senha_hash):
        return None
    if not user.ativo:
        return None
    return user


def create_token_for_user(user: Usuario) -> str:
    """Generate a JWT access token for the given user."""
    return create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "perfil": user.perfil.nome,
        }
    )
