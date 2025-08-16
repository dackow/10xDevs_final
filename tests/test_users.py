import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_register_user_existing_email(client, test_user):
    """Test registration with an email that already exists."""
    # The test_user fixture has already created a user.
    # Try to register the same user again.
    response = client.post(
        "/register",
        data={"email": test_user["email"], "password": test_user["password"]}
    )

    assert response.status_code == 200 # Stays on the same page with an error
    assert "Użytkownik o tym adresie email już istnieje." in response.content.decode("utf-8")

def test_register_user_missing_fields(client):
    """Test registration with missing email or password."""
    response = client.post(
        "/register",
        data={"email": "missing@example.com", "password": ""} # Missing password
    )
    assert response.status_code == 200
    assert "Email i hasło są wymagane." in response.content.decode("utf-8")

    response = client.post(
        "/register",
        data={"email": "", "password": "password123"} # Missing email
    )
    assert response.status_code == 200
    assert "Email i hasło są wymagane." in response.content.decode("utf-8")
    print("✅ Test registration with missing fields passed.")
