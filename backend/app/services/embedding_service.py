"""Embedding and indexing service — chunking, embedding generation, vector search."""

import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.config import settings
from app.models.documento import Documento
from app.models.versao_documento import VersaoDocumento
from app.models.documento_chunk import DocumentoChunk
from app.models.embedding_chunk import EmbeddingChunk
from app.models.indexacao_job import IndexacaoJob

logger = logging.getLogger(__name__)


def chunk_text(text_content: str, chunk_size: int = None, overlap: int = None) -> list[str]:
    """Split text into overlapping chunks."""
    size = chunk_size or settings.chunk_size
    lap = overlap or settings.chunk_overlap
    if len(text_content) <= size:
        return [text_content]

    chunks = []
    start = 0
    while start < len(text_content):
        end = start + size
        chunks.append(text_content[start:end])
        start += size - lap
    return chunks


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Generate embeddings via OpenAI API."""
    import openai

    client = openai.OpenAI(api_key=settings.openai_api_key)
    response = client.embeddings.create(input=texts, model=settings.embedding_model)
    return [item.embedding for item in response.data]


def index_documento(db: Session, documento_id: int) -> IndexacaoJob:
    """Index a document: chunk its latest version, generate embeddings, store them."""
    doc = db.query(Documento).filter(Documento.id == documento_id).first()
    if not doc:
        raise ValueError(f"Documento {documento_id} não encontrado")

    latest_version = (
        db.query(VersaoDocumento)
        .filter(VersaoDocumento.documento_id == documento_id)
        .order_by(VersaoDocumento.numero_versao.desc())
        .first()
    )
    if not latest_version:
        raise ValueError(f"Nenhuma versão encontrada para documento {documento_id}")

    job = IndexacaoJob(
        documento_id=documento_id,
        status="em_andamento",
        tipo="indexacao",
    )
    db.add(job)
    db.flush()

    try:
        # Remove old chunks and embeddings for this document
        old_chunks = (
            db.query(DocumentoChunk)
            .filter(DocumentoChunk.documento_id == documento_id)
            .all()
        )
        old_chunk_ids = [c.id for c in old_chunks]
        if old_chunk_ids:
            db.query(EmbeddingChunk).filter(
                EmbeddingChunk.chunk_id.in_(old_chunk_ids)
            ).delete(synchronize_session=False)
            db.query(DocumentoChunk).filter(
                DocumentoChunk.documento_id == documento_id
            ).delete(synchronize_session=False)

        # Create new chunks
        chunks_text = chunk_text(latest_version.conteudo)
        job.total_chunks = len(chunks_text)

        new_chunks = []
        for i, chunk_content in enumerate(chunks_text):
            chunk = DocumentoChunk(
                documento_id=documento_id,
                versao_documento_id=latest_version.id,
                indice=i,
                conteudo=chunk_content,
            )
            db.add(chunk)
            new_chunks.append(chunk)

        db.flush()

        # Generate embeddings
        embeddings = generate_embeddings(chunks_text)

        for chunk, emb in zip(new_chunks, embeddings):
            embedding_record = EmbeddingChunk(
                chunk_id=chunk.id,
                embedding=emb,
                modelo=settings.embedding_model,
            )
            db.add(embedding_record)
            job.chunks_processados += 1

        job.status = "concluido"
        job.finalizado_em = datetime.now(timezone.utc)
        db.commit()

    except Exception as e:
        logger.exception("Erro na indexação do documento %s", documento_id)
        job.status = "erro"
        job.erro = str(e)
        job.finalizado_em = datetime.now(timezone.utc)
        db.commit()

    db.refresh(job)
    return job


def search_similar_chunks(
    db: Session, query_embedding: list[float], top_k: int = None
) -> list[dict]:
    """Search for the most similar chunks using pgvector cosine distance."""
    k = top_k or settings.top_k
    embedding_str = "[" + ",".join(str(x) for x in query_embedding) + "]"

    sql = text("""
        SELECT
            dc.id AS chunk_id,
            dc.conteudo,
            dc.documento_id,
            d.titulo AS documento_titulo,
            ec.embedding <=> :embedding AS distance
        FROM embedding_chunk ec
        JOIN documento_chunk dc ON dc.id = ec.chunk_id
        JOIN documento d ON d.id = dc.documento_id
        WHERE d.ativo = true
        ORDER BY ec.embedding <=> :embedding
        LIMIT :limit
    """)

    results = db.execute(sql, {"embedding": embedding_str, "limit": k}).fetchall()
    return [
        {
            "chunk_id": row.chunk_id,
            "conteudo": row.conteudo,
            "documento_id": row.documento_id,
            "documento_titulo": row.documento_titulo,
            "distance": row.distance,
            "similaridade": 1 - row.distance,
        }
        for row in results
    ]
