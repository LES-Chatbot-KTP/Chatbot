"""Evaluation routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.usuario import Usuario
from app.schemas.avaliacao import AvaliacaoCreate, AvaliacaoResponse
from app.services import avaliacao_service

router = APIRouter(prefix="/api/avaliacoes", tags=["Avaliações"])


@router.post("/", response_model=AvaliacaoResponse, status_code=201)
def create_avaliacao(
    data: AvaliacaoCreate,
    db: Session = Depends(get_db),
    _user: Usuario = Depends(get_current_user),
):
    """Rate an answer."""
    return avaliacao_service.create_avaliacao(db, data)


@router.get("/{avaliacao_id}", response_model=AvaliacaoResponse)
def get_avaliacao(
    avaliacao_id: int,
    db: Session = Depends(get_db),
    _user: Usuario = Depends(get_current_user),
):
    """Get an evaluation by ID."""
    return avaliacao_service.get_avaliacao(db, avaliacao_id)
