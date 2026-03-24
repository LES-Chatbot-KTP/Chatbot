"""
Caso de uso: listar todos os documentos cadastrados no banco de dados.
Repository Pattern — recebe o repositório via injeção de dependência (Factory).
"""

from Backend.app.domain.repositories.document_repository import DocumentRepository


class ListDocuments:

    def __init__(self, repository: DocumentRepository):
        self.repository = repository

    def executar(self) -> list[dict]:
        """
        Retorna a lista de todos os documentos persistidos no PostgreSQL.
        """
        return self.repository.list_all()