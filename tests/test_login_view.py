import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_post_login_success(client, test_user):
    """Test successful login"""
    response_login = client.post(
        "/login",
        data={"email": test_user["email"], "password": test_user["password"]},
        follow_redirects=False
    )

    assert response_login.status_code == 303
    assert response_login.headers["location"] == "/dashboard"
    assert "access_token" in response_login.cookies
    assert response_login.cookies["access_token"].strip('"').startswith("Bearer ")

    print(f"✅ Test login passed - status: {response_login.status_code}")

def test_post_login_invalid_credentials(client):
    """Test invalid login"""
    unique_email = f"nonexistent_{uuid.uuid4()}@test.com"
    password = "anypassword"

    response = client.post(
        "/login",
        data={"email": unique_email, "password": password}
    )

    assert response.status_code == 200
    assert "Wystąpił błąd podczas logowania." in response.text
    print(f"✅ Test invalid login passed")
