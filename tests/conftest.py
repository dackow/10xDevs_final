import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="session")
def client():
    """Test client for FastAPI app"""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(autouse=True)
def mock_auth_system():
    """Automatyczne mockowanie systemu autoryzacji"""
    
    # Mock użytkownika
    mock_user = MagicMock()
    mock_user.id = "test-user-id" 
    mock_user.email = "dackow@gmail.com"
    
    # Mock Supabase client
    mock_supabase = MagicMock()

    # Configure mock_supabase for sign_up
    mock_supabase.auth.sign_up.return_value = MagicMock(user=mock_user)

    # Configure mock_supabase for sign_in_with_password
    mock_session = MagicMock(access_token="mock_access_token")
    mock_supabase.auth.sign_in_with_password.return_value = MagicMock(session=mock_session)
    
    with patch("app.dependencies.get_current_user", return_value=mock_user), \
         patch("app.dependencies.get_supabase_client", return_value=mock_supabase):
        
        yield {
            'user': mock_user,
            'supabase': mock_supabase
        }
