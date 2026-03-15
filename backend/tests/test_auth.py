"""Tests for authentication endpoints."""

from tests.conftest import auth_header


def test_login_success(client, db, seed_perfis):
    """Test successful login."""
    from app.models.usuario import Usuario
    from app.utils.security import hash_password

    user = Usuario(
        nome="Test User",
        email="test@example.com",
        senha_hash=hash_password("password123"),
        perfil_id=seed_perfis["comum"].id,
    )
    db.add(user)
    db.commit()

    response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "senha": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, seed_perfis):
    """Test login with wrong credentials."""
    response = client.post(
        "/api/auth/login",
        json={"email": "wrong@example.com", "senha": "wrong"},
    )
    assert response.status_code == 401


def test_get_me(client, admin_token):
    """Test fetching current user info."""
    response = client.get("/api/auth/me", headers=auth_header(admin_token))
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "admin@test.com"
    assert data["perfil_nome"] == "administrador"


def test_get_me_unauthorized(client):
    """Test accessing /me without authentication."""
    response = client.get("/api/auth/me")
    assert response.status_code == 401
