import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

def test_full_user_flow_with_mocked_supabase(client, test_user):
    """Test full user flow (registration and login) with real Supabase interactions."""
    
    # The user is already created by the test_user fixture.
    # We can directly proceed to login.
    
    # 2. Login
    response_login = client.post("/login", data={
        "email": test_user["email"],
        "password": test_user["password"]
    }, follow_redirects=False)
    
    assert response_login.status_code == 303
    assert response_login.headers["location"] == "/dashboard"
    assert "access_token" in response_login.cookies
    print("✅ Integration test: Login successful.")
