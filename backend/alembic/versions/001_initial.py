"""Initial schema with all DER entities and embedding extensions

Revision ID: 001_initial
Revises:
Create Date: 2026-03-15
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable pgvector extension
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # perfil
    op.create_table(
        "perfil",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("nome", sa.String(50), unique=True, nullable=False),
        sa.Column("descricao", sa.String(255), nullable=True),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    # usuario
    op.create_table(
        "usuario",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("nome", sa.String(150), nullable=False),
        sa.Column("email", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("senha_hash", sa.String(255), nullable=False),
        sa.Column("ativo", sa.Boolean(), default=True),
        sa.Column("perfil_id", sa.Integer(), sa.ForeignKey("perfil.id"), nullable=False),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
        sa.Column(
            "atualizado_em",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )

    # conversa
    op.create_table(
        "conversa",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("titulo", sa.String(255), nullable=True),
        sa.Column(
            "usuario_id", sa.Integer(), sa.ForeignKey("usuario.id"), nullable=False
        ),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
        sa.Column(
            "atualizado_em",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )

    # pergunta
    op.create_table(
        "pergunta",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "conversa_id", sa.Integer(), sa.ForeignKey("conversa.id"), nullable=False
        ),
        sa.Column("texto_original", sa.Text(), nullable=False),
        sa.Column("texto_processado", sa.Text(), nullable=True),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    # categoria
    op.create_table(
        "categoria",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("nome", sa.String(150), unique=True, nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    # documento
    op.create_table(
        "documento",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("titulo", sa.String(255), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column(
            "categoria_id",
            sa.Integer(),
            sa.ForeignKey("categoria.id"),
            nullable=True,
        ),
        sa.Column("ativo", sa.Boolean(), default=True),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
        sa.Column(
            "atualizado_em",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )

    # versao_documento
    op.create_table(
        "versao_documento",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "documento_id",
            sa.Integer(),
            sa.ForeignKey("documento.id"),
            nullable=False,
        ),
        sa.Column("numero_versao", sa.Integer(), nullable=False, default=1),
        sa.Column("conteudo", sa.Text(), nullable=False),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    # resposta
    op.create_table(
        "resposta",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "pergunta_id",
            sa.Integer(),
            sa.ForeignKey("pergunta.id"),
            unique=True,
            nullable=False,
        ),
        sa.Column("texto", sa.Text(), nullable=False),
        sa.Column("modelo_usado", sa.Text(), nullable=True),
        sa.Column("tokens_prompt", sa.Integer(), nullable=True),
        sa.Column("tokens_resposta", sa.Integer(), nullable=True),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    # avaliacao
    op.create_table(
        "avaliacao",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "resposta_id",
            sa.Integer(),
            sa.ForeignKey("resposta.id"),
            unique=True,
            nullable=False,
        ),
        sa.Column("nota", sa.Integer(), nullable=False),
        sa.Column("comentario", sa.Text(), nullable=True),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    # documento_resposta
    op.create_table(
        "documento_resposta",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "documento_id",
            sa.Integer(),
            sa.ForeignKey("documento.id"),
            nullable=False,
        ),
        sa.Column(
            "resposta_id",
            sa.Integer(),
            sa.ForeignKey("resposta.id"),
            nullable=False,
        ),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    # log_administrativo
    op.create_table(
        "log_administrativo",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "usuario_id",
            sa.Integer(),
            sa.ForeignKey("usuario.id"),
            nullable=False,
        ),
        sa.Column("acao", sa.String(100), nullable=False),
        sa.Column("entidade", sa.String(100), nullable=True),
        sa.Column("entidade_id", sa.Integer(), nullable=True),
        sa.Column("detalhes", sa.Text(), nullable=True),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    # --- Embedding extension tables ---

    # documento_chunk
    op.create_table(
        "documento_chunk",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "documento_id",
            sa.Integer(),
            sa.ForeignKey("documento.id"),
            nullable=False,
        ),
        sa.Column(
            "versao_documento_id",
            sa.Integer(),
            sa.ForeignKey("versao_documento.id"),
            nullable=False,
        ),
        sa.Column("indice", sa.Integer(), nullable=False),
        sa.Column("conteudo", sa.Text(), nullable=False),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    # embedding_chunk (uses pgvector)
    op.execute("""
        CREATE TABLE embedding_chunk (
            id SERIAL PRIMARY KEY,
            chunk_id INTEGER UNIQUE NOT NULL REFERENCES documento_chunk(id),
            embedding vector(1536) NOT NULL,
            modelo VARCHAR(100),
            criado_em TIMESTAMPTZ DEFAULT NOW()
        )
    """)

    # Create index for cosine distance search
    op.execute("""
        CREATE INDEX idx_embedding_chunk_cosine
        ON embedding_chunk
        USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100)
    """)

    # resposta_fonte
    op.create_table(
        "resposta_fonte",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "resposta_id",
            sa.Integer(),
            sa.ForeignKey("resposta.id"),
            nullable=False,
        ),
        sa.Column(
            "chunk_id",
            sa.Integer(),
            sa.ForeignKey("documento_chunk.id"),
            nullable=False,
        ),
        sa.Column("similaridade", sa.Float(), nullable=True),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    # indexacao_job
    op.create_table(
        "indexacao_job",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "documento_id",
            sa.Integer(),
            sa.ForeignKey("documento.id"),
            nullable=True,
        ),
        sa.Column("status", sa.String(30), nullable=False, server_default="pendente"),
        sa.Column("tipo", sa.String(50), nullable=False, server_default="indexacao"),
        sa.Column("total_chunks", sa.Integer(), nullable=True),
        sa.Column("chunks_processados", sa.Integer(), server_default="0"),
        sa.Column("erro", sa.Text(), nullable=True),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
        sa.Column("finalizado_em", sa.DateTime(timezone=True), nullable=True),
    )

    # Seed default profiles
    op.execute(
        "INSERT INTO perfil (nome, descricao) VALUES "
        "('administrador', 'Perfil de administrador do sistema'), "
        "('comum', 'Perfil de usuário comum')"
    )


def downgrade() -> None:
    op.drop_table("indexacao_job")
    op.drop_table("resposta_fonte")
    op.execute("DROP TABLE IF EXISTS embedding_chunk CASCADE")
    op.drop_table("documento_chunk")
    op.drop_table("log_administrativo")
    op.drop_table("documento_resposta")
    op.drop_table("avaliacao")
    op.drop_table("resposta")
    op.drop_table("versao_documento")
    op.drop_table("documento")
    op.drop_table("categoria")
    op.drop_table("pergunta")
    op.drop_table("conversa")
    op.drop_table("usuario")
    op.drop_table("perfil")
    op.execute("DROP EXTENSION IF EXISTS vector")
