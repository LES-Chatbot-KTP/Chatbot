"""Tests for user management endpoints."""

from tests.conftest import auth_header


def test_create_user(client, admin_token, seed_perfis):
    """Test creating a user as admin."""
    response = client.post(
        "/api/usuarios/",
        json={
            "nome": "Novo Usuário",
            "email": "novo@test.com",
            "senha": "senha123",
            "perfil_id": seed_perfis["comum"].id,
        },
        headers=auth_header(admin_token),
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Novo Usuário"
    assert data["email"] == "novo@test.com"


def test_create_user_forbidden_for_regular_user(client, user_token, seed_perfis):
    """Test that regular users cannot create users."""
    response = client.post(
        "/api/usuarios/",
        json={
            "nome": "Outro",
            "email": "outro@test.com",
            "senha": "senha123",
            "perfil_id": seed_perfis["comum"].id,
        },
        headers=auth_header(user_token),
    )
    assert response.status_code == 403


def test_list_users(client, admin_token):
    """Test listing users as admin."""
    response = client.get("/api/usuarios/", headers=auth_header(admin_token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_deactivate_user(client, admin_token, db, seed_perfis):
    """Test deactivating a user."""
    from app.models.usuario import Usuario
    from app.utils.security import hash_password

    user = Usuario(
        nome="To Delete",
        email="delete@test.com",
        senha_hash=hash_password("pass"),
        perfil_id=seed_perfis["comum"].id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    response = client.delete(
        f"/api/usuarios/{user.id}", headers=auth_header(admin_token)
    )
    assert response.status_code == 200
    assert response.json()["ativo"] is False
