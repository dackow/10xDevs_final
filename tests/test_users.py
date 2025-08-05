import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.dependencies import get_db
from app.models.models import Base, User
from app.services.auth_service import get_password_hash
import uuid

# Ustawienie testowej bazy danych SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_user():
    unique_username = f"uniqueuser_{uuid.uuid4()}"
    response = client.post(
        "/users",
        json={"username": unique_username, "password": "testpassword"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == unique_username
    assert "id" in data

def test_create_user_duplicate_username():
    # First, create a user
    client.post(
        "/users",
        json={"username": "duplicateuser", "password": "testpassword"}
    )

    # Then, try to create another user with the same username
    response = client.post(
        "/users",
        json={"username": "duplicateuser", "password": "anotherpassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"
