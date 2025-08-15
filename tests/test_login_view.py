import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid # Import uuid for unique email generation

client = TestClient(app)

def test_post_login_success():
    """Test udanego logowania"""
    unique_email = f"login_view_{uuid.uuid4()}@test.com"
    password = "StrongPassword123!@@@##" # Use a strong password

    # 1. Register the user
    response_register = client.post("/register", data={
        "email": unique_email,
        "password": password
    }, follow_redirects=False)

    assert response_register.status_code == 303
    assert response_register.headers["location"] == "/login"

    # 2. Login the user
    response_login = client.post(
        "/login",
        data={"email": unique_email, "password": password},
        follow_redirects=False
    )

    assert response_login.status_code == 303
    assert response_login.headers["location"] == "/dashboard"
    assert "access_token" in response_login.cookies
    # The actual token will be from Supabase, so we can't assert "Bearer fake_token"
    # We can assert that it starts with "Bearer "
    assert response_login.cookies["access_token"].strip('"').startswith("Bearer ")

    print(f"✅ Test login przeszedł - status: {response_login.status_code}")

def test_post_login_invalid_credentials():
    """Test błędnego logowania"""
    # This test can remain largely the same, as it tests an invalid login
    # without needing to register a user first.
    # However, it should use a non-existent email to ensure it's truly invalid.
    unique_email = f"nonexistent_{uuid.uuid4()}@test.com"
    password = "anypassword"

    response = client.post(
        "/login",
        data={"email": unique_email, "password": password}
    )

    assert response.status_code == 200
    assert "Wystąpił błąd podczas logowania." in response.text
    print(f"✅ Test invalid login przeszedł")