from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base, User, FlashcardSet, Flashcard
from app.services.auth_service import get_password_hash
import pytest

# Użyj innej bazy danych dla testów
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Nadpisz get_db, aby używać testowej bazy danych
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

@pytest.fixture(scope="function")
def test_user(setup_database):
    db = TestingSessionLocal()
    user = User(username="testuser", password_hash=get_password_hash("testpassword"))
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

@pytest.fixture(scope="function")
def test_flashcard_set(test_user):
    db = TestingSessionLocal()
    flashcard_set = FlashcardSet(name="Test Set", user_id=test_user.id)
    db.add(flashcard_set)
    db.commit()
    db.refresh(flashcard_set)
    db.close()
    return flashcard_set

@pytest.fixture(scope="function")
def test_flashcard(test_flashcard_set):
    db = TestingSessionLocal()
    flashcard = Flashcard(set_id=test_flashcard_set.id, question="Test Question", answer="Test Answer")
    db.add(flashcard)
    db.commit()
    db.refresh(flashcard)
    db.close()
    return flashcard

def get_auth_token(username, password):
    client.post("/users", json={"username": username, "password": password})
    response = client.post("/token", data={"username": username, "password": password})
    return response.json()["access_token"]

def test_update_flashcard(test_user, test_flashcard):
    token = get_auth_token("testuser", "testpassword")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(
        f"/flashcards/{test_flashcard.id}",
        headers=headers,
        json={"question": "Updated Question", "answer": "Updated Answer"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "Updated Question"
    assert data["answer"] == "Updated Answer"
