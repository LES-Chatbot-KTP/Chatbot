"""Document and category management routes (admin only for mutations)."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, get_admin_user
from app.models.usuario import Usuario
from app.schemas.documento import (
    CategoriaCreate,
    CategoriaResponse,
    DocumentoCreate,
    DocumentoUpdate,
    DocumentoResponse,
    DocumentoDetailResponse,
    VersaoDocumentoResponse,
    IndexacaoJobResponse,
)
from app.services import documento_service
from app.services.embedding_service import index_documento
from app.services.admin_service import create_log

router = APIRouter(prefix="/api/documentos", tags=["Documentos"])


# --- Categories ---


@router.post("/categorias", response_model=CategoriaResponse, status_code=201)
def create_categoria(
    data: CategoriaCreate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_admin_user),
):
    """Create a document category (admin only)."""
    cat = documento_service.create_categoria(db, data)
    create_log(db, admin.id, "criar_categoria", "categoria", cat.id)
    return cat


@router.get("/categorias", response_model=list[CategoriaResponse])
def list_categorias(
    db: Session = Depends(get_db),
    _user: Usuario = Depends(get_current_user),
):
    """List all categories."""
    return documento_service.list_categorias(db)


# --- Documents ---


@router.post("/", response_model=DocumentoResponse, status_code=201)
def create_documento(
    data: DocumentoCreate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_admin_user),
):
    """Create a new document with its first version (admin only)."""
    doc = documento_service.create_documento(db, data)
    create_log(db, admin.id, "criar_documento", "documento", doc.id)
    return doc


@router.get("/", response_model=list[DocumentoResponse])
def list_documentos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _user: Usuario = Depends(get_current_user),
):
    """List active documents."""
    return documento_service.list_documentos(db, skip, limit)


@router.get("/{documento_id}", response_model=DocumentoDetailResponse)
def get_documento(
    documento_id: int,
    db: Session = Depends(get_db),
    _user: Usuario = Depends(get_current_user),
):
    """Get document details including versions."""
    doc = documento_service.get_documento(db, documento_id)
    versoes = documento_service.get_versoes(db, documento_id)
    return DocumentoDetailResponse(
        id=doc.id,
        titulo=doc.titulo,
        descricao=doc.descricao,
        categoria_id=doc.categoria_id,
        ativo=doc.ativo,
        criado_em=doc.criado_em,
        atualizado_em=doc.atualizado_em,
        versoes=[
            VersaoDocumentoResponse(
                id=v.id,
                documento_id=v.documento_id,
                numero_versao=v.numero_versao,
                conteudo=v.conteudo,
                criado_em=v.criado_em,
            )
            for v in versoes
        ],
    )


@router.put("/{documento_id}", response_model=DocumentoResponse)
def update_documento(
    documento_id: int,
    data: DocumentoUpdate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_admin_user),
):
    """Update a document. If content is provided, creates a new version (admin only)."""
    doc = documento_service.update_documento(db, documento_id, data)
    create_log(db, admin.id, "atualizar_documento", "documento", doc.id)
    return doc


@router.delete("/{documento_id}", response_model=DocumentoResponse)
def deactivate_documento(
    documento_id: int,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_admin_user),
):
    """Deactivate a document (admin only)."""
    doc = documento_service.deactivate_documento(db, documento_id)
    create_log(db, admin.id, "desativar_documento", "documento", doc.id)
    return doc


@router.post("/{documento_id}/indexar", response_model=IndexacaoJobResponse)
def reindex_documento(
    documento_id: int,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_admin_user),
):
    """Re-index a document's embeddings (admin only)."""
    job = index_documento(db, documento_id)
    create_log(
        db,
        admin.id,
        "reindexar_documento",
        "documento",
        documento_id,
        f"Job {job.id} - status: {job.status}",
    )
    return job
