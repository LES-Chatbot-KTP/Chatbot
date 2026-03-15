"""Tests for document management endpoints."""

from tests.conftest import auth_header


def test_create_categoria(client, admin_token):
    """Test creating a category."""
    response = client.post(
        "/api/documentos/categorias",
        json={"nome": "Editais", "descricao": "Editais do IFES"},
        headers=auth_header(admin_token),
    )
    assert response.status_code == 201
    assert response.json()["nome"] == "Editais"


def test_list_categorias(client, user_token, admin_token):
    """Test listing categories as a regular user."""
    # Create a category first
    client.post(
        "/api/documentos/categorias",
        json={"nome": "Regulamentos"},
        headers=auth_header(admin_token),
    )
    response = client.get(
        "/api/documentos/categorias", headers=auth_header(user_token)
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_create_documento(client, admin_token):
    """Test creating a document."""
    response = client.post(
        "/api/documentos/",
        json={
            "titulo": "Edital 01/2026",
            "descricao": "Edital de seleção",
            "conteudo": "Conteúdo completo do edital de seleção do IFES.",
        },
        headers=auth_header(admin_token),
    )
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == "Edital 01/2026"
    assert data["ativo"] is True


def test_get_documento_with_versions(client, admin_token):
    """Test getting a document includes version history."""
    # Create
    create_resp = client.post(
        "/api/documentos/",
        json={
            "titulo": "Doc Versionado",
            "conteudo": "Versão 1 do documento.",
        },
        headers=auth_header(admin_token),
    )
    doc_id = create_resp.json()["id"]

    # Update with new content (creates version 2)
    client.put(
        f"/api/documentos/{doc_id}",
        json={"conteudo": "Versão 2 do documento."},
        headers=auth_header(admin_token),
    )

    # Get detail
    response = client.get(
        f"/api/documentos/{doc_id}", headers=auth_header(admin_token)
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["versoes"]) == 2


def test_deactivate_documento(client, admin_token):
    """Test deactivating a document."""
    create_resp = client.post(
        "/api/documentos/",
        json={
            "titulo": "Doc para Inativar",
            "conteudo": "Conteúdo do documento.",
        },
        headers=auth_header(admin_token),
    )
    doc_id = create_resp.json()["id"]

    response = client.delete(
        f"/api/documentos/{doc_id}", headers=auth_header(admin_token)
    )
    assert response.status_code == 200
    assert response.json()["ativo"] is False


def test_list_documentos(client, user_token, admin_token):
    """Test listing documents."""
    client.post(
        "/api/documentos/",
        json={"titulo": "Listável", "conteudo": "Conteúdo"},
        headers=auth_header(admin_token),
    )
    response = client.get("/api/documentos/", headers=auth_header(user_token))
    assert response.status_code == 200
    assert len(response.json()) >= 1
