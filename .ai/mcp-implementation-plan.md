### Plan Implementacji Serwera MCP

#### 1. Struktura Projektu
   - `app/`
     - `__init__.py`
     - `main.py` (główna aplikacja FastAPI, włączenie routera MCP)
     - `dependencies.py` (istniejące zależności, np. `get_current_user`)
     - `exceptions.py` (definicje niestandardowych wyjątków, jeśli potrzebne)
     - `routers/`
       - `__init__.py`
       - `mcp.py` (nowy router dla endpointów MCP, logika narzędzi, mapowanie)
       - `auth.py` (istniejący router autentykacji)
       - `flashcards.py` (istniejący router fiszek)
     - `schemas/`
       - `schemas.py` (definicje modeli Pydantic dla MCP i narzędzi)
     - `services/`
       - `ollama.py` (istniejąca usługa komunikacji z Ollamą)
       - `auth_service.py` (istniejąca usługa autentykacji)
     - `models/` (istniejące modele bazodanowe)
   - `tests/`
     - `test_mcp.py` (nowy plik z testami integracyjnymi dla endpointów MCP)
     - `conftest.py` (fixture'y do testów, np. mockowanie zależności)

#### 2. Kluczowe Moduły
   - **`app/main.py`**:
       - Włączenie nowego routera MCP: `app.include_router(mcp.router, prefix="/mcp")`.
       - Konfiguracja globalnej obsługi błędów, jeśli nie jest jeszcze zaimplementowana.
   - **`app/routers/mcp.py`**:
       - Definicja routera FastAPI.
       - Implementacja endpointu `GET /mcp/tools/definitions`.
       - Implementacja endpointu `POST /mcp/tools/execute`.
       - Definicja asynchronicznej funkcji `generate_flashcards_ai_function` (logika narzędzia).
       - Definicja słownika `TOOLS_MAP` mapującego nazwy narzędzi na funkcje.
       - Obsługa dynamicznego wywoływania narzędzi i walidacji parametrów.
   - **`app/schemas/schemas.py`**:
       - Definicja modeli Pydantic:
         - `FlashcardGenerateRequest(BaseModel)`: `text: str`, `count: int`.
         - `AIGenerationResponse(BaseModel)`: `flashcards: List[Dict[str, str]]` (gdzie każdy dict to `{"question": str, "answer": str}`).
         - `ToolDefinition(BaseModel)`: `name: str`, `description: str`, `input_schema: Dict`, `output_schema: Dict`.
         - `ToolExecuteRequest(BaseModel)`: `tool_name: str`, `parameters: Dict`.
         - `ToolExecuteResponse(BaseModel)`: `content: Optional[Dict]`, `error: Optional[Dict]`.
   - **`app/services/ollama.py`**:
       - Istniejąca funkcja `generate_flashcards_from_text(text, count)` będzie wywoływana przez narzędzie MCP.
   - **`app/dependencies.py`**:
       - Istniejąca zależność `get_current_user` będzie używana do ochrony endpointu `POST /mcp/tools/execute`.

#### 3. Definicje Narzędzi/Zasobów/Promptów
   - **Narzędzie: `generateFlashcardsAI`**
       - Opis: Generuje fiszki (pytanie-odpowiedź) na podstawie dostarczonego tekstu źródłowego i określonej liczby fiszek.
       - Schemat Wejściowy (Pydantic):
         ```python
         class FlashcardGenerateRequest(BaseModel):
             text: str
             count: int
         ```
         (JSON Schema będzie generowany za pomocą `.model_json_schema()`)
       - Schemat Wyjściowy (Pydantic):
         ```python
         class AIGenerationResponse(BaseModel):
             flashcards: List[Dict[str, str]] # [{"question": "...", "answer": "..."}]
         ```
         (JSON Schema będzie generowany za pomocą `.model_json_schema()`)
       - Logika `execute` (funkcja `generate_flashcards_ai_function` w `app/routers/mcp.py`):
         1. Przyjmuje parametry `text` i `count` (już zwalidowane przez Pydantic).
         2. Przyjmuje zależności `current_user` i `supabase_client`.
         3. Wywołuje `await app.services.ollama.generate_flashcards_from_text(text, count)`.
         4. Przetwarza wynik z Ollamy do formatu `{"flashcards": [{"question": "...", "answer": "..."}]}`.
         5. Obsługuje potencjalne błędy z `ollama.generate_flashcards_from_text` i zwraca je w ustandaryzowanym formacie błędu MCP.
       - Opakowanie Wyniku dla SDK: Wynik działania narzędzia będzie opakowany w klucz `content` w odpowiedzi JSON, np.:
         ```json
         {
           "content": {
             "flashcards": [
               {"question": "Pytanie 1", "answer": "Odpowiedź 1"},
               {"question": "Pytanie 2", "answer": "Odpowiedź 2"}
             ]
           }
         }
         ```

#### 4. Obsługa Danych
   - Dane wejściowe dla narzędzia `generateFlashcardsAI` będą pochodzić bezpośrednio z ciała żądania POST.
   - Dane do generowania fiszek będą pobierane z usługi Ollama za pośrednictwem funkcji `app.services.ollama.generate_flashcards_from_text`.
   - Brak bezpośredniego użycia plików JSON (`preparedRules.json`) w kontekście tego narzędzia.

#### 5. Konfiguracja Serwera i Wdrożenia
   - Konfiguracja `McpServer`: Serwer MCP jest zintegrowany bezpośrednio z istniejącą aplikacją FastAPI. Nie ma oddzielnej instancji `McpServer` do konfiguracji, a sama aplikacja FastAPI pełni rolę serwera MCP.
   - Konfiguracja Railway: Standardowe wdrożenie aplikacji FastAPI/Uvicorn na Railway. Wymagane pliki to `requirements.txt` (z zależnościami) i opcjonalnie `Procfile` (do określenia komendy startowej Uvicorn).
   - Zmienne Środowiskowe / Sekrety:
     - `SUPABASE_URL`
     - `SUPABASE_KEY`
     - `OLLAMA_API_BASE_URL` (jeśli Ollama jest hostowana zewnętrznie)
     - Inne zmienne środowiskowe wymagane przez istniejącą aplikację FastAPI.

#### 6. Obsługa Błędów
   - Globalna obsługa błędów w FastAPI zostanie zaimplementowana (lub rozszerzona), aby przechwytywać `HTTPException` i inne wyjątki.
   - Błędy będą zwracane w ustandaryzowanym formacie JSON:
     ```json
     {
       "error": {
         "message": "Opis błędu",
         "code": "opcjonalny_kod_błędu",
         "details": "opcjonalne_szczegóły_błędu"
       }
     }
     ```
   - Endpoint `POST /mcp/tools/execute` będzie zwracał statusy `400 Bad Request` (dla błędów walidacji parametrów narzędzia lub nieistniejącego narzędzia) lub `422 Unprocessable Entity` (dla błędów logiki biznesowej narzędzia, np. z Ollamy).

#### 7. Strategia Testowania
   - **Testy Jednostkowe**:
     - Testy dla modeli Pydantic w `app/schemas/schemas.py` (walidacja danych).
     - Testy dla funkcji `generate_flashcards_ai_function` (logika biznesowa, mockowanie `ollama.generate_flashcards_from_text`).
   - **Testy Integracyjne**:
     - Nowy plik `tests/test_mcp.py`.
     - Użycie `FastAPI TestClient` do testowania endpointów `GET /mcp/tools/definitions` i `POST /mcp/tools/execute`.
     - Scenariusze testowe:
       - Pomyślne wywołanie `generateFlashcardsAI` (mockowanie odpowiedzi z Ollamy).
       - Błędy walidacji parametrów dla `generateFlashcardsAI`.
       - Brak autentykacji dla `POST /mcp/tools/execute`.
       - Wywołanie nieistniejącego narzędzia.
       - Obsługa błędów zwracanych przez usługę Ollama.
     - Mockowanie zależności `app.dependencies.get_current_user` oraz `app.services.ollama.generate_flashcards_from_text` w testach integracyjnych.

#### 8. Dodatkowe Uwagi
   - Zapewnienie, że Pythonowe SDK do tworzenia MCP jest poprawnie zintegrowane i używane do obsługi protokołu MCP.
   - Wykorzystanie asynchronicznych możliwości FastAPI i biblioteki HTTPX do komunikacji z Ollamą w celu zapewnienia wysokiej wydajności i responsywności serwera.
   - Dalsze narzędzia MCP mogą być dodawane w przyszłości poprzez rozszerzenie słownika `TOOLS_MAP` i dodanie odpowiednich funkcji narzędziowych.
