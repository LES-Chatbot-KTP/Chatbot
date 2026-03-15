"""SQLAlchemy models for the Chatbot database."""

from app.models.perfil import Perfil
from app.models.usuario import Usuario
from app.models.conversa import Conversa
from app.models.pergunta import Pergunta
from app.models.resposta import Resposta
from app.models.avaliacao import Avaliacao
from app.models.categoria import Categoria
from app.models.documento import Documento
from app.models.versao_documento import VersaoDocumento
from app.models.documento_resposta import DocumentoResposta
from app.models.log_administrativo import LogAdministrativo
from app.models.documento_chunk import DocumentoChunk
from app.models.embedding_chunk import EmbeddingChunk
from app.models.resposta_fonte import RespostaFonte
from app.models.indexacao_job import IndexacaoJob

__all__ = [
    "Perfil",
    "Usuario",
    "Conversa",
    "Pergunta",
    "Resposta",
    "Avaliacao",
    "Categoria",
    "Documento",
    "VersaoDocumento",
    "DocumentoResposta",
    "LogAdministrativo",
    "DocumentoChunk",
    "EmbeddingChunk",
    "RespostaFonte",
    "IndexacaoJob",
]
