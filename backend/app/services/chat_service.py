"""Chat service — conversation management and RAG-based answer generation."""

import logging

from sqlalchemy.orm import Session

from app.config import settings
from app.models.conversa import Conversa
from app.models.pergunta import Pergunta
from app.models.resposta import Resposta
from app.models.documento_resposta import DocumentoResposta
from app.models.resposta_fonte import RespostaFonte
from app.services.embedding_service import generate_embeddings, search_similar_chunks

logger = logging.getLogger(__name__)


def create_conversa(db: Session, usuario_id: int, titulo: str | None = None) -> Conversa:
    """Start a new conversation."""
    conversa = Conversa(usuario_id=usuario_id, titulo=titulo)
    db.add(conversa)
    db.commit()
    db.refresh(conversa)
    return conversa


def get_conversa(db: Session, conversa_id: int, usuario_id: int) -> Conversa:
    """Get a conversation owned by the user."""
    conversa = (
        db.query(Conversa)
        .filter(Conversa.id == conversa_id, Conversa.usuario_id == usuario_id)
        .first()
    )
    if not conversa:
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conversa não encontrada"
        )
    return conversa


def list_conversas(db: Session, usuario_id: int) -> list[Conversa]:
    """List all conversations for a user."""
    return (
        db.query(Conversa)
        .filter(Conversa.usuario_id == usuario_id)
        .order_by(Conversa.atualizado_em.desc())
        .all()
    )


def get_historico(db: Session, conversa_id: int, usuario_id: int) -> list[Pergunta]:
    """Get all questions (with responses) in a conversation."""
    conversa = get_conversa(db, conversa_id, usuario_id)
    return (
        db.query(Pergunta)
        .filter(Pergunta.conversa_id == conversa.id)
        .order_by(Pergunta.criado_em)
        .all()
    )


def ask_question(db: Session, conversa_id: int, usuario_id: int, texto: str) -> dict:
    """Process a user question through the RAG pipeline and return the answer."""
    conversa = get_conversa(db, conversa_id, usuario_id)

    # Save the question
    pergunta = Pergunta(
        conversa_id=conversa.id,
        texto_original=texto,
        texto_processado=texto.strip().lower(),
    )
    db.add(pergunta)
    db.flush()

    try:
        # Generate embedding for the question
        query_embedding = generate_embeddings([texto])[0]

        # Search similar chunks
        similar_chunks = search_similar_chunks(db, query_embedding)

        # Build context from retrieved chunks
        context_parts = []
        for chunk in similar_chunks:
            context_parts.append(
                f"[Fonte: {chunk['documento_titulo']}]\n{chunk['conteudo']}"
            )
        context = "\n\n---\n\n".join(context_parts) if context_parts else ""

        # Generate answer using OpenAI
        answer_text, model_used, tokens_prompt, tokens_response = _generate_answer(
            texto, context
        )

    except Exception as e:
        logger.exception("Erro ao gerar resposta para pergunta %s", pergunta.id)
        answer_text = (
            "Desculpe, não foi possível gerar uma resposta no momento. "
            "Tente novamente mais tarde."
        )
        model_used = None
        tokens_prompt = None
        tokens_response = None
        similar_chunks = []

    # Save the response
    resposta = Resposta(
        pergunta_id=pergunta.id,
        texto=answer_text,
        modelo_usado=model_used,
        tokens_prompt=tokens_prompt,
        tokens_resposta=tokens_response,
    )
    db.add(resposta)
    db.flush()

    # Save source references
    doc_ids_seen = set()
    for chunk in similar_chunks:
        fonte = RespostaFonte(
            resposta_id=resposta.id,
            chunk_id=chunk["chunk_id"],
            similaridade=chunk.get("similaridade"),
        )
        db.add(fonte)

        if chunk["documento_id"] not in doc_ids_seen:
            doc_resp = DocumentoResposta(
                documento_id=chunk["documento_id"],
                resposta_id=resposta.id,
            )
            db.add(doc_resp)
            doc_ids_seen.add(chunk["documento_id"])

    db.commit()
    db.refresh(pergunta)
    db.refresh(resposta)

    fontes = [
        {
            "documento_titulo": c["documento_titulo"],
            "chunk_conteudo": c["conteudo"],
            "similaridade": c.get("similaridade"),
        }
        for c in similar_chunks
    ]

    return {"pergunta": pergunta, "resposta": resposta, "fontes": fontes}


def _generate_answer(
    question: str, context: str
) -> tuple[str, str | None, int | None, int | None]:
    """Call OpenAI chat completion to generate an answer with context."""
    import openai

    client = openai.OpenAI(api_key=settings.openai_api_key)

    system_prompt = (
        "Você é um assistente inteligente do IFES que responde perguntas com base "
        "nos documentos fornecidos. Responda de forma clara e objetiva. "
        "Se não encontrar informação suficiente nos documentos, informe ao usuário."
    )

    user_prompt = f"Contexto dos documentos:\n{context}\n\nPergunta: {question}"

    response = client.chat.completions.create(
        model=settings.chat_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=1024,
    )

    message = response.choices[0].message.content
    usage = response.usage
    return (
        message,
        settings.chat_model,
        usage.prompt_tokens if usage else None,
        usage.completion_tokens if usage else None,
    )
