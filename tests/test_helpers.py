"""
Pomocne funkcje dla testów
"""

def debug_response(response):
    """Helper do debugowania odpowiedzi testowych"""
    print(f"\n=== DEBUG RESPONSE ===")
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Content (first 500 chars): {response.text[:500]}")
    if hasattr(response, 'cookies'):
        print(f"Cookies: {dict(response.cookies)}")
    print(f"======================\n")

def assert_response_contains_any(response, keywords):
    """Sprawdza czy odpowiedź zawiera którekolwiek z podanych słów kluczowych"""
    response_text = response.text.lower()
    found_keywords = [keyword for keyword in keywords if keyword.lower() in response_text]
    
    assert found_keywords, f"Nie znaleziono żadnego z słów: {keywords} w odpowiedzi. Treść: {response.text[:200]}..."
    return found_keywords

def mock_supabase_auth_success():
    """Tworzy mock dla udanego uwierzytelnienia Supabase"""
    from unittest.mock import MagicMock
    
    mock_user = MagicMock()
    mock_user.id = "test-user-id"
    mock_user.email = "test@example.com"
    
    mock_session = MagicMock()
    mock_session.access_token = "fake_token"
    mock_session.user = mock_user
    
    mock_auth_response = MagicMock()
    mock_auth_response.session = mock_session
    mock_auth_response.user = mock_user
    
    return mock_auth_response

def mock_supabase_auth_error(error_message="Authentication failed"):
    """Tworzy mock dla błędu uwierzytelnienia Supabase"""
    from unittest.mock import MagicMock
    
    def side_effect(*args, **kwargs):
        raise Exception(error_message)
    
    return side_effect
