import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_register_user_success():
    """Test successful user registration."""
    unique_email = f"register_success_{uuid.uuid4()}@test.com"
    password = "StrongPassword123!@@@##"

    response = client.post(
        "/register",
        data={"email": unique_email, "password": password},
        follow_redirects=False # Do not follow redirect to check status code
    )

    assert response.status_code == 303 # Expect redirect to login page
    assert response.headers["location"] == "/login"

def test_register_user_existing_email():
    """Test registration with an email that already exists."""
    unique_email = f"existing_email_{uuid.uuid4()}@test.com"
    password = "StrongPassword123!@@@##"

    # Register the user first
    client.post(
        "/register",
        data={"email": unique_email, "password": password},
        follow_redirects=False
    )

    # Try to register the same user again
    response = client.post(
        "/register",
        data={"email": unique_email, "password": password}
    )

    assert response.status_code == 200 # Stays on the same page with an error
    assert "User already registered" in response.text

def test_register_user_missing_fields():
    """Test registration with missing email or password."""
    response = client.post(
        "/register",
        data={"email": "missing@example.com", "password": ""} # Missing password
    )
    assert response.status_code == 200
    assert "Email i hasło są wymagane." in response.text

    response = client.post(
        "/register",
        data={"email": "", "password": "password123"} # Missing email
    )
    assert response.status_code == 200
    assert "Email i hasło są wymagane." in response.text
    print("✅ Test registration with missing fields passed.")