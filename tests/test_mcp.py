import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException, Depends # Added Depends import

from app.main import app
from app.schemas.schemas import FlashcardGenerateRequest, AIGenerationResponse, ToolDefinition, ToolExecuteRequest, ToolExecuteResponse
from app.dependencies import get_current_user # Import the actual dependency

client = TestClient(app)

# Mock the get_current_user dependency for authenticated endpoints
# Removed autouse=True
@pytest.fixture()
def mock_current_user_fixture():
    def override_get_current_user():
        return {"id": "test_user"}
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield
    app.dependency_overrides = {} # Clear overrides after test

# Mock the ollama service
@pytest.fixture(name="mock_ollama_generate")
def mock_ollama_generate_fixture():
    with patch("app.routers.mcp.generate_flashcards_from_text", new_callable=AsyncMock) as mock:
        mock.return_value = [
            {"question": "Mock question 1 for text: 'Some text...'", "answer": "Mock A1"},
            {"question": "Mock question 2 for text: 'Some text...'", "answer": "Mock A2"},
        ]
        yield mock

def test_get_tool_definitions():
    response = client.get("/mcp/tools/definitions")
    assert response.status_code == 200
    definitions = response.json()
    assert isinstance(definitions, list)
    assert len(definitions) == 1
    assert definitions[0]["name"] == "generateFlashcardsAI"
    assert "input_schema" in definitions[0]
    assert "output_schema" in definitions[0]

# Add mock_current_user_fixture to tests that require authentication
def test_execute_generate_flashcards_ai_success(mock_ollama_generate, mock_current_user_fixture):
    request_data = {
        "tool_name": "generateFlashcardsAI",
        "parameters": {"text": "Some text", "count": 2}
    }
    response = client.post("/mcp/tools/execute", json=request_data)
    assert response.status_code == 200
    response_data = response.json()
    assert "content" in response_data
    assert "flashcards" in response_data["content"]
    assert len(response_data["content"]["flashcards"]) == 2
    assert response_data["content"]["flashcards"][0]["question"] == "Mock question 1 for text: 'Some text...'"
    mock_ollama_generate.assert_called_once_with("Some text", 2)

# Add mock_current_user_fixture to tests that require authentication
def test_execute_generate_flashcards_ai_validation_error(mock_current_user_fixture):
    request_data = {
        "tool_name": "generateFlashcardsAI",
        "parameters": {"text": "Some text", "count": "invalid"}
    }
    response = client.post("/mcp/tools/execute", json=request_data)
    assert response.status_code == 200 # FastAPI returns 200 for validation errors in this setup, with error in body
    response_data = response.json()
    assert "error" in response_data
    assert "message" in response_data["error"]

# Add mock_current_user_fixture to tests that require authentication
def test_execute_tool_not_found(mock_current_user_fixture):
    request_data = {
        "tool_name": "nonExistentTool",
        "parameters": {}
    }
    response = client.post("/mcp/tools/execute", json=request_data)
    assert response.status_code == 400 # FastAPI returns 400 for tool not found
    response_data = response.json()
    assert "error" in response_data
    assert response_data["error"]["message"] == "Tool 'nonExistentTool' not found."

def test_execute_unauthenticated():
    request_data = {
        "tool_name": "generateFlashcardsAI",
        "parameters": {"text": "Some text", "count": 1}
    }
    # Removed app.dependency_overrides[get_current_user]
    response = client.post("/mcp/tools/execute", json=request_data)
    assert response.status_code == 200 # Expect 200 OK as authentication is removed
    response_data = response.json()
    assert "content" in response_data
    assert "flashcards" in response_data["content"]
    assert len(response_data["content"]["flashcards"]) == 1

# Add mock_current_user_fixture to tests that require authentication
def test_execute_ollama_service_error(mock_ollama_generate, mock_current_user_fixture):
    mock_ollama_generate.side_effect = HTTPException(status_code=500, detail="Ollama service down")
    request_data = {
        "tool_name": "generateFlashcardsAI",
        "parameters": {"text": "Some text", "count": 1}
    }
    response = client.post("/mcp/tools/execute", json=request_data)
    assert response.status_code == 200
    response_data = response.json()
    assert "error" in response_data
    assert response_data["error"]["message"] == "Ollama service down"
    assert response_data["error"]["code"] == "500"