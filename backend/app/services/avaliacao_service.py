"""Evaluation service."""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.avaliacao import Avaliacao
from app.models.resposta import Resposta
from app.schemas.avaliacao import AvaliacaoCreate


def create_avaliacao(db: Session, data: AvaliacaoCreate) -> Avaliacao:
    """Create a rating for an answer."""
    resposta = db.query(Resposta).filter(Resposta.id == data.resposta_id).first()
    if not resposta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resposta não encontrada"
        )

    existing = (
        db.query(Avaliacao).filter(Avaliacao.resposta_id == data.resposta_id).first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta resposta já foi avaliada",
        )

    avaliacao = Avaliacao(
        resposta_id=data.resposta_id,
        nota=data.nota,
        comentario=data.comentario,
    )
    db.add(avaliacao)
    db.commit()
    db.refresh(avaliacao)
    return avaliacao


def get_avaliacao(db: Session, avaliacao_id: int) -> Avaliacao:
    """Get an evaluation by ID."""
    av = db.query(Avaliacao).filter(Avaliacao.id == avaliacao_id).first()
    if not av:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Avaliação não encontrada"
        )
    return av
