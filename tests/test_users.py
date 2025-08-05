from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base
import pytest

# Użyj innej bazy danych dla testów
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Nadpisz get_db, aby używać testowej bazy danych
@pytest.fixture(name="db_session")
def db_session_fixture():
    Base.metadata.create_all(bind=engine)  # Utwórz tabele
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Usuń tabele po testach

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/users",
        json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_create_existing_user():
    # Utwórz użytkownika po raz pierwszy
    client.post(
        "/users",
        json={"username": "existinguser", "password": "testpassword"}
    )
    # Spróbuj utworzyć tego samego użytkownika ponownie
    response = client.post(
        "/users",
        json={"username": "existinguser", "password": "anotherpassword"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}
