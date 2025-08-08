import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# test_integration.py
def test_full_user_flow():
    """Test pełnego przepływu użytkownika"""
    
    # 1. Rejestracja
    with patch("app.dependencies.get_supabase_client"):
        response = client.post("/register", data={
            "email": "integration@test.com", 
            "password": "testpass"
        })
        assert response.status_code in [200, 303]
    
    # 2. Logowanie  
    with patch("app.dependencies.get_supabase_client"):
        response = client.post("/login", data={
            "email": "integration@test.com", 
            "password": "testpass"
        })
        assert response.status_code in [200, 303]
