import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

# client = TestClient(app) # Removed duplicate client initialization

def test_full_user_flow_with_mocked_supabase(client): # Inject client fixture
    """Test full user flow (registration and login) with real Supabase interactions."""
    unique_email = f"integration_{uuid.uuid4()}@test.com"
    # 1. Registration
    response_register = client.post("/register", data={
        "email": unique_email,
        "password": "StrongPassword123!@@@##"
    }, follow_redirects=False)
    

    print(unique_email)
    assert response_register.status_code == 303
    assert response_register.headers["location"] == "/login"
    print("✅ Integration test: Registration successful.")

    # 2. Login
    response_login = client.post("/login", data={
        "email": unique_email,
        "password": "StrongPassword123!@@@##"
    }, follow_redirects=False)
    
    assert response_login.status_code == 303
    assert response_login.headers["location"] == "/dashboard"
    assert "access_token" in response_login.cookies
    print("✅ Integration test: Login successful.")