"""Document management service."""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.documento import Documento
from app.models.versao_documento import VersaoDocumento
from app.models.categoria import Categoria
from app.schemas.documento import DocumentoCreate, DocumentoUpdate, CategoriaCreate


# --- Categories ---


def create_categoria(db: Session, data: CategoriaCreate) -> Categoria:
    """Create a new document category."""
    existing = db.query(Categoria).filter(Categoria.nome == data.nome).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Categoria já existe",
        )
    cat = Categoria(nome=data.nome, descricao=data.descricao)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


def list_categorias(db: Session) -> list[Categoria]:
    """List all categories."""
    return db.query(Categoria).all()


def get_categoria(db: Session, categoria_id: int) -> Categoria:
    """Get a category by ID."""
    cat = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada"
        )
    return cat


# --- Documents ---


def create_documento(db: Session, data: DocumentoCreate) -> Documento:
    """Create a new document with its first version."""
    doc = Documento(
        titulo=data.titulo,
        descricao=data.descricao,
        categoria_id=data.categoria_id,
    )
    db.add(doc)
    db.flush()

    versao = VersaoDocumento(
        documento_id=doc.id,
        numero_versao=1,
        conteudo=data.conteudo,
    )
    db.add(versao)
    db.commit()
    db.refresh(doc)
    return doc


def get_documento(db: Session, documento_id: int) -> Documento:
    """Get a document by ID."""
    doc = db.query(Documento).filter(Documento.id == documento_id).first()
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Documento não encontrado"
        )
    return doc


def list_documentos(
    db: Session, skip: int = 0, limit: int = 100, apenas_ativos: bool = True
) -> list[Documento]:
    """List documents with optional active filter."""
    query = db.query(Documento)
    if apenas_ativos:
        query = query.filter(Documento.ativo.is_(True))
    return query.offset(skip).limit(limit).all()


def update_documento(db: Session, documento_id: int, data: DocumentoUpdate) -> Documento:
    """Update document metadata and optionally create a new version."""
    doc = get_documento(db, documento_id)

    if data.titulo is not None:
        doc.titulo = data.titulo
    if data.descricao is not None:
        doc.descricao = data.descricao
    if data.categoria_id is not None:
        doc.categoria_id = data.categoria_id

    if data.conteudo is not None:
        last_version = (
            db.query(VersaoDocumento)
            .filter(VersaoDocumento.documento_id == documento_id)
            .order_by(VersaoDocumento.numero_versao.desc())
            .first()
        )
        next_version = (last_version.numero_versao + 1) if last_version else 1
        versao = VersaoDocumento(
            documento_id=doc.id,
            numero_versao=next_version,
            conteudo=data.conteudo,
        )
        db.add(versao)

    db.commit()
    db.refresh(doc)
    return doc


def deactivate_documento(db: Session, documento_id: int) -> Documento:
    """Soft-delete a document."""
    doc = get_documento(db, documento_id)
    doc.ativo = False
    db.commit()
    db.refresh(doc)
    return doc


def get_versoes(db: Session, documento_id: int) -> list[VersaoDocumento]:
    """Get all versions of a document."""
    return (
        db.query(VersaoDocumento)
        .filter(VersaoDocumento.documento_id == documento_id)
        .order_by(VersaoDocumento.numero_versao.desc())
        .all()
    )
