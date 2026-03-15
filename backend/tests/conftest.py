"""Test fixtures for the backend API tests."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app
from app.models.perfil import Perfil
from app.utils.security import hash_password


# Use in-memory SQLite for tests (pgvector features are not tested here)
SQLALCHEMY_TEST_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test and drop them after."""
    # Skip pgvector-specific tables that need the extension
    # We create all non-vector tables
    from app.models import (  # noqa: F401
        Perfil,
        Usuario,
        Conversa,
        Pergunta,
        Resposta,
        Avaliacao,
        Categoria,
        Documento,
        VersaoDocumento,
        DocumentoResposta,
        LogAdministrativo,
        DocumentoChunk,
        RespostaFonte,
        IndexacaoJob,
    )

    # Filter out embedding_chunk which requires pgvector
    tables_to_create = [
        t
        for t in Base.metadata.sorted_tables
        if t.name != "embedding_chunk"
    ]
    Base.metadata.create_all(bind=engine, tables=tables_to_create)
    yield
    Base.metadata.drop_all(bind=engine, tables=tables_to_create)


@pytest.fixture
def db():
    """Provide a database session for direct use in tests."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client():
    """Provide a FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def seed_perfis(db):
    """Seed the default profiles."""
    admin_perfil = Perfil(nome="administrador", descricao="Admin do sistema")
    comum_perfil = Perfil(nome="comum", descricao="Usuário comum")
    db.add_all([admin_perfil, comum_perfil])
    db.commit()
    db.refresh(admin_perfil)
    db.refresh(comum_perfil)
    return {"administrador": admin_perfil, "comum": comum_perfil}


@pytest.fixture
def admin_token(client, db, seed_perfis):
    """Create an admin user and return a valid token."""
    from app.models.usuario import Usuario

    user = Usuario(
        nome="Admin Test",
        email="admin@test.com",
        senha_hash=hash_password("admin123"),
        perfil_id=seed_perfis["administrador"].id,
    )
    db.add(user)
    db.commit()

    response = client.post(
        "/api/auth/login",
        json={"email": "admin@test.com", "senha": "admin123"},
    )
    return response.json()["access_token"]


@pytest.fixture
def user_token(client, db, seed_perfis):
    """Create a regular user and return a valid token."""
    from app.models.usuario import Usuario

    user = Usuario(
        nome="User Test",
        email="user@test.com",
        senha_hash=hash_password("user123"),
        perfil_id=seed_perfis["comum"].id,
    )
    db.add(user)
    db.commit()

    response = client.post(
        "/api/auth/login",
        json={"email": "user@test.com", "senha": "user123"},
    )
    return response.json()["access_token"]


def auth_header(token: str) -> dict:
    """Build authorization header."""
    return {"Authorization": f"Bearer {token}"}
