"""Admin service — metrics and administrative logs."""

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.usuario import Usuario
from app.models.conversa import Conversa
from app.models.pergunta import Pergunta
from app.models.documento import Documento
from app.models.avaliacao import Avaliacao
from app.models.log_administrativo import LogAdministrativo
from app.schemas.admin import MetricasResponse


def get_metricas(db: Session) -> MetricasResponse:
    """Compute administrative dashboard metrics."""
    total_usuarios = db.query(func.count(Usuario.id)).scalar() or 0
    total_conversas = db.query(func.count(Conversa.id)).scalar() or 0
    total_perguntas = db.query(func.count(Pergunta.id)).scalar() or 0
    total_documentos = db.query(func.count(Documento.id)).scalar() or 0
    total_documentos_ativos = (
        db.query(func.count(Documento.id)).filter(Documento.ativo.is_(True)).scalar()
        or 0
    )
    media_avaliacoes = db.query(func.avg(Avaliacao.nota)).scalar()
    total_avaliacoes = db.query(func.count(Avaliacao.id)).scalar() or 0

    return MetricasResponse(
        total_usuarios=total_usuarios,
        total_conversas=total_conversas,
        total_perguntas=total_perguntas,
        total_documentos=total_documentos,
        total_documentos_ativos=total_documentos_ativos,
        media_avaliacoes=round(media_avaliacoes, 2) if media_avaliacoes else None,
        total_avaliacoes=total_avaliacoes,
    )


def create_log(
    db: Session,
    usuario_id: int,
    acao: str,
    entidade: str | None = None,
    entidade_id: int | None = None,
    detalhes: str | None = None,
) -> LogAdministrativo:
    """Create an admin log entry."""
    log = LogAdministrativo(
        usuario_id=usuario_id,
        acao=acao,
        entidade=entidade,
        entidade_id=entidade_id,
        detalhes=detalhes,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def list_logs(
    db: Session, skip: int = 0, limit: int = 100
) -> list[LogAdministrativo]:
    """List admin logs (most recent first)."""
    return (
        db.query(LogAdministrativo)
        .order_by(LogAdministrativo.criado_em.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
