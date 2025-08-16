import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
import uuid
from app.dependencies import get_supabase_client

@pytest.fixture(scope="session")
def supabase_client():
    return get_supabase_client()

@pytest.fixture(scope="session")
def client():
    """Test client for FastAPI app"""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function")
def test_user(supabase_client):
    """Create a user in Supabase for testing and clean it up after."""
    unique_email = f"test_user_{uuid.uuid4()}@example.com"
    password = "password123"
    
    # Create user in auth.users
    auth_response = supabase_client.auth.admin.create_user({"email": unique_email, "password": password, "email_confirm": True})
    user = auth_response.user
    assert user is not None

    # Insert user into public.users
    user_data = {"id": user.id, "email": unique_email}
    insert_response = supabase_client.table("users").insert(user_data).execute()
    assert insert_response.data is not None

    yield {"email": unique_email, "password": password, "id": user.id}

    # Teardown: delete the user
    supabase_client.auth.admin.delete_user(user.id)

@pytest.fixture()
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
    
    with patch("app.dependencies.get_current_user", return_value=mock_user), patch("app.dependencies.get_supabase_client", return_value=mock_supabase):
        
        yield {
            'user': mock_user,
            'supabase': mock_supabase
        }
