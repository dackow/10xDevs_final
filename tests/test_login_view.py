import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.dependencies import get_db
from app.models.models import Base, User
from app.services.auth_service import get_password_hash

# Ustawienie testowej bazy danych SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="db_session")
def db_session_fixture():
    Base.metadata.create_all(bind=engine) # Tworzy tabele
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine) # Usuwa tabele po teście

@pytest.fixture(name="client")
def client_fixture(db_session):
    # Nadpisz zależność get_db, aby używała testowej sesji DB
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear() # Wyczyść nadpisania po teście

def test_get_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert "Logowanie" in response.text
    assert "Nazwa użytkownika" in response.text
    assert "Hasło" in response.text

def test_post_login_success(client, db_session):
    # Stwórz testowego użytkownika
    hashed_password = get_password_hash("testpassword")
    test_user = User(username="testuser", password_hash=hashed_password)
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    response = client.post("/login", data={"username": "testuser", "password": "testpassword"}, follow_redirects=False)
    assert response.status_code == 303 # Oczekiwane przekierowanie
    assert response.headers["location"] == "/dashboard"
    # Sprawdź, czy ciasteczko zostało ustawione (może wymagać bardziej szczegółowej weryfikacji)
    assert "access_token" in response.cookies

def test_post_login_invalid_credentials(client):
    response = client.post("/login", data={"username": "nonexistent", "password": "wrongpassword"})
    assert response.status_code == 200 # Strona logowania jest ponownie renderowana
    assert "Nieprawidłowa nazwa użytkownika lub hasło." in response.text

def test_post_login_empty_fields(client):
    response = client.post("/login", data={"username": "", "password": ""})
    assert response.status_code == 200
    assert "Nazwa użytkownika i hasło są wymagane." in response.text

    response = client.post("/login", data={"username": "user", "password": ""})
    assert response.status_code == 200
    assert "Nazwa użytkownika i hasło są wymagane." in response.text

    response = client.post("/login", data={"username": "", "password": "password"})
    assert response.status_code == 200
    assert "Nazwa użytkownika i hasło są wymagane." in response.text
