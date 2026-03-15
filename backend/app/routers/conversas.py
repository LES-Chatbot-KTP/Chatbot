"""Conversation and chat routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.usuario import Usuario
from app.schemas.conversa import (
    ConversaCreate,
    ConversaResponse,
    PerguntaRequest,
    PerguntaResponse,
    RespostaResponse,
    FonteResponse,
    ChatResponse,
)
from app.services import chat_service

router = APIRouter(prefix="/api/conversas", tags=["Conversas"])


@router.post("/", response_model=ConversaResponse, status_code=201)
def create_conversa(
    data: ConversaCreate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    """Start a new conversation."""
    conversa = chat_service.create_conversa(db, user.id, data.titulo)
    return conversa


@router.get("/", response_model=list[ConversaResponse])
def list_conversas(
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    """List all conversations for the current user."""
    return chat_service.list_conversas(db, user.id)


@router.get("/{conversa_id}", response_model=ConversaResponse)
def get_conversa(
    conversa_id: int,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    """Get conversation details."""
    return chat_service.get_conversa(db, conversa_id, user.id)


@router.get("/{conversa_id}/historico", response_model=list[PerguntaResponse])
def get_historico(
    conversa_id: int,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    """Get all questions and answers in a conversation."""
    perguntas = chat_service.get_historico(db, conversa_id, user.id)
    result = []
    for p in perguntas:
        resp = None
        if p.resposta:
            fontes = []
            if p.resposta.fontes:
                for f in p.resposta.fontes:
                    fontes.append(
                        FonteResponse(
                            documento_titulo=f.chunk.documento.titulo if f.chunk else "",
                            chunk_conteudo=f.chunk.conteudo if f.chunk else "",
                            similaridade=f.similaridade,
                        )
                    )
            resp = RespostaResponse(
                id=p.resposta.id,
                pergunta_id=p.resposta.pergunta_id,
                texto=p.resposta.texto,
                modelo_usado=p.resposta.modelo_usado,
                fontes=fontes,
                criado_em=p.resposta.criado_em,
            )
        result.append(
            PerguntaResponse(
                id=p.id,
                conversa_id=p.conversa_id,
                texto_original=p.texto_original,
                texto_processado=p.texto_processado,
                resposta=resp,
                criado_em=p.criado_em,
            )
        )
    return result


@router.post("/{conversa_id}/perguntar", response_model=ChatResponse)
def ask_question(
    conversa_id: int,
    data: PerguntaRequest,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    """Send a question in a conversation and get a RAG-based answer."""
    result = chat_service.ask_question(db, conversa_id, user.id, data.texto)

    fontes = [
        FonteResponse(
            documento_titulo=f["documento_titulo"],
            chunk_conteudo=f["chunk_conteudo"],
            similaridade=f.get("similaridade"),
        )
        for f in result["fontes"]
    ]

    pergunta = result["pergunta"]
    resposta = result["resposta"]

    return ChatResponse(
        pergunta=PerguntaResponse(
            id=pergunta.id,
            conversa_id=pergunta.conversa_id,
            texto_original=pergunta.texto_original,
            texto_processado=pergunta.texto_processado,
            criado_em=pergunta.criado_em,
        ),
        resposta=RespostaResponse(
            id=resposta.id,
            pergunta_id=resposta.pergunta_id,
            texto=resposta.texto,
            modelo_usado=resposta.modelo_usado,
            fontes=fontes,
            criado_em=resposta.criado_em,
        ),
    )
