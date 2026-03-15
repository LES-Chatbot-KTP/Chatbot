"""Authentication routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.usuario import UsuarioResponse
from app.services.auth_service import authenticate_user, create_token_for_user
from app.dependencies import get_current_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/api/auth", tags=["Autenticação"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate a user and return a JWT token."""
    user = authenticate_user(db, data.email, data.senha)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_token_for_user(user)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UsuarioResponse)
def get_me(current_user: Usuario = Depends(get_current_user)):
    """Return the currently authenticated user."""
    return UsuarioResponse(
        id=current_user.id,
        nome=current_user.nome,
        email=current_user.email,
        ativo=current_user.ativo,
        perfil_id=current_user.perfil_id,
        perfil_nome=current_user.perfil.nome,
        criado_em=current_user.criado_em,
    )
