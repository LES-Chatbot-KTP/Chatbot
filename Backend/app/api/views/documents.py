"""
Views para operações sobre documentos.
Usa DocumentFactory (Factory Method) para obter os casos de uso.
Requer autenticação JWT — apenas administradores (is_staff=True).

Rotas:
    GET    /api/documents/                     → listar documentos
    POST   /api/documents/                     → criar documento
    PATCH  /api/documents/<id>/                → editar documento
    DELETE /api/documents/<id>/                → solicitar exclusão (retorna token)
    DELETE /api/documents/<id>/confirm/        → confirmar exclusão com token
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from Backend.app.api.factories import DocumentFactory


class DocumentListView(APIView):
    """
    GET /api/documents/  → lista todos os documentos no banco.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        try:
            documentos = DocumentFactory.make_list().executar()
            return Response(documentos, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DocumentCreateView(APIView):
    """
    POST /api/documents/  → cria documento, faz upload no Gemini e persiste no banco.

    Multipart form-data esperado:
        arquivo  (File)    — PDF obrigatório
        nome     (string)  — nome do documento
        tipo     (string)  — portaria | resolucao | rod
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        arquivo = request.FILES.get("arquivo")
        nome = request.data.get("nome", "").strip()
        tipo = request.data.get("tipo", "").strip()

        if not arquivo:
            return Response(
                {"error": "O campo 'arquivo' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not nome:
            return Response(
                {"error": "O campo 'nome' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if tipo not in ("portaria", "resolucao", "rod"):
            return Response(
                {"error": "O campo 'tipo' deve ser 'portaria', 'resolucao' ou 'rod'."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not arquivo.name.lower().endswith(".pdf"):
            return Response(
                {"error": "Apenas arquivos PDF são aceitos."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            resultado = DocumentFactory.make_create().executar(
                nome=nome,
                tipo=tipo,
                conteudo_arquivo=arquivo.read(),   # ← nome correto do parâmetro
                nome_arquivo=arquivo.name,
            )
            return Response(resultado, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DocumentDetailView(APIView):
    """
    PATCH /api/documents/<id>/  → atualiza metadados e/ou substitui o arquivo no Gemini.

    Multipart form-data (todos opcionais, mas ao menos um obrigatório):
        nome     (string)  — novo nome
        tipo     (string)  — portaria | resolucao | rod
        arquivo  (File)    — novo PDF para substituir o atual
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, id_documento: int):
        nome = request.data.get("nome") or None
        tipo = request.data.get("tipo") or None
        arquivo = request.FILES.get("arquivo")

        if tipo and tipo not in ("portaria", "resolucao", "rod"):
            return Response(
                {"error": "Tipo inválido. Use 'portaria', 'resolucao' ou 'rod'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not nome and not tipo and not arquivo:
            return Response(
                {"error": "Envie ao menos um campo para atualizar: nome, tipo ou arquivo."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            resultado = DocumentFactory.make_update().executar(
                id_documento=id_documento,
                nome=nome,
                tipo=tipo,
                conteudo_arquivo=arquivo.read() if arquivo else None,  # ← nome correto
                nome_arquivo=arquivo.name if arquivo else None,
            )
            return Response(resultado, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except LookupError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DocumentDeleteView(APIView):
    """
    DELETE /api/documents/<id>/

    Passo 1 do fluxo de exclusão: verifica se o documento existe
    e retorna um token de confirmação válido por 5 minutos.

    Resposta 200:
        {
            "message": "Confirme a exclusão do documento 'portaria_001.pdf'.",
            "token": "<token>",
            "expires_in": 300
        }
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, id_documento: int):
        try:
            resultado = DocumentFactory.make_delete().solicitar_exclusao(id_documento)
            return Response(resultado, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except LookupError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DocumentConfirmDeleteView(APIView):
    """
    DELETE /api/documents/<id>/confirm/

    Passo 2 do fluxo de exclusão: recebe o token retornado no passo 1
    e efetivamente remove o documento e seus chunks do banco.

    Body JSON:
        { "token": "<token_recebido_no_passo_1>" }

    Resposta 200:
        {
            "message": "Documento 'portaria_001.pdf' excluído com sucesso.",
            "id": 1
        }
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, id_documento: int):
        token = request.data.get("token", "").strip()

        if not token:
            return Response(
                {"error": "O campo 'token' é obrigatório para confirmar a exclusão."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            resultado = DocumentFactory.make_delete().confirmar_exclusao(id_documento, token)
            return Response(resultado, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except LookupError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)