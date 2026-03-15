"""Tests for conversation endpoints."""

from tests.conftest import auth_header


def test_create_conversa(client, user_token):
    """Test starting a new conversation."""
    response = client.post(
        "/api/conversas/",
        json={"titulo": "Minha Conversa"},
        headers=auth_header(user_token),
    )
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == "Minha Conversa"


def test_list_conversas(client, user_token):
    """Test listing user's conversations."""
    client.post(
        "/api/conversas/",
        json={"titulo": "Conversa 1"},
        headers=auth_header(user_token),
    )
    client.post(
        "/api/conversas/",
        json={"titulo": "Conversa 2"},
        headers=auth_header(user_token),
    )
    response = client.get("/api/conversas/", headers=auth_header(user_token))
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_get_conversa(client, user_token):
    """Test getting a specific conversation."""
    create_resp = client.post(
        "/api/conversas/",
        json={"titulo": "Detalhe"},
        headers=auth_header(user_token),
    )
    conversa_id = create_resp.json()["id"]

    response = client.get(
        f"/api/conversas/{conversa_id}", headers=auth_header(user_token)
    )
    assert response.status_code == 200
    assert response.json()["titulo"] == "Detalhe"


def test_get_historico_empty(client, user_token):
    """Test getting empty history for a new conversation."""
    create_resp = client.post(
        "/api/conversas/",
        json={"titulo": "Vazia"},
        headers=auth_header(user_token),
    )
    conversa_id = create_resp.json()["id"]

    response = client.get(
        f"/api/conversas/{conversa_id}/historico",
        headers=auth_header(user_token),
    )
    assert response.status_code == 200
    assert response.json() == []
