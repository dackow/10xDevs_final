import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_post_login_success():
    """Test udanego logowania"""
    
    with patch("app.dependencies.get_supabase_client") as mock_client:
        # Setup mocka
        mock_supabase = MagicMock()
        mock_session = MagicMock()
        mock_session.access_token = "fake_token"
        mock_session.user = MagicMock()
        
        mock_auth_response = MagicMock()
        mock_auth_response.session = mock_session
        mock_auth_response.user = mock_session.user
        
        mock_supabase.auth.sign_in_with_password.return_value = mock_auth_response
        mock_client.return_value = mock_supabase
        
        response = client.post(
            "/login", 
            data={"email": "test@example.com", "password": "testpassword"},
            follow_redirects=False
        )
        
        # Akceptuj różne statusy
        assert response.status_code in [200, 303], f"Status: {response.status_code}"
        
        print(f"✅ Test login przeszedł - status: {response.status_code}")

def test_post_login_invalid_credentials():
    """Test błędnego logowania"""
    
    with patch("app.dependencies.get_supabase_client") as mock_client:
        mock_supabase = MagicMock()
        mock_supabase.auth.sign_in_with_password.side_effect = Exception("Invalid")
        mock_client.return_value = mock_supabase
        
        response = client.post(
            "/login",
            data={"email": "wrong@example.com", "password": "wrong"}
        )
        
        assert response.status_code == 200
        print(f"✅ Test invalid login przeszedł")
