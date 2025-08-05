# API Endpoint Implementation Plan: POST /ai/generate-flashcards

## 1. Przegląd punktu końcowego

Ten punkt końcowy umożliwia generowanie fiszek za pomocą modelu AI (Ollama) na podstawie dostarczonego tekstu źródłowego. Jest to chroniony punkt końcowy, wymagający uwierzytelnienia użytkownika.

## 2. Szczegóły żądania

-   **Metoda HTTP**: `POST`
-   **Struktura URL**: `/ai/generate-flashcards`
-   **Parametry**: Brak parametrów w URL.
-   **Request Body**: 
    -   **Content-Type**: `application/json`
    -   **Pola**:
        -   `text` (string, wymagane): Tekst źródłowy do generowania fiszek.
        -   `count` (integer, wymagane): Liczba fiszek do wygenerowania (5, 10 lub 15).
    -   **Schemat**: `schemas.AIGenerationRequest`

## 3. Wykorzystywane typy

-   **Command Model**: `schemas.AIGenerationRequest` (dla danych wejściowych żądania)
-   **DTO (Data Transfer Object)**: `schemas.AIGenerationResponse` (dla danych wyjściowych odpowiedzi)
-   **DTO (nested)**: `schemas.FlashcardCreate` (dla pojedynczych fiszek w odpowiedzi)

## 4. Szczegóły odpowiedzi

-   **Odpowiedź sukcesu (200 OK)**:
    ```json
    {
      "flashcards": [
        {
          "question": "string",
          "answer": "string"
        }
      ]
    }
    ```
    -   **Schemat**: `schemas.AIGenerationResponse`
-   **Odpowiedzi błędów**:
    -   `401 Unauthorized`: Jeśli użytkownik nie jest uwierzytelniony.
    -   `422 Unprocessable Entity`: Jeśli ciało żądania jest nieprawidłowe (np. puste pole `text`, `count` poza zakresem).
    -   `500 Internal Server Error`: Jeśli komunikacja z usługą Ollama zakończy się niepowodzeniem lub wystąpi inny błąd po stronie serwera.

## 5. Przepływ danych

1.  Klient wysyła żądanie `POST` na adres `/ai/generate-flashcards` z tekstem źródłowym i żądaną liczbą fiszek.
2.  Router FastAPI przechwytuje żądanie.
3.  Punkt końcowy wymaga uwierzytelnienia użytkownika (np. za pomocą `Depends(oauth2_scheme)` i `Depends(get_current_user)`).
4.  Dane wejściowe są walidowane przez `schemas.AIGenerationRequest`.
5.  Punkt końcowy wywołuje funkcję serwisową (np. `ollama_service.generate_flashcards`), przekazując tekst i liczbę fiszek.
6.  Funkcja serwisowa komunikuje się z lokalnym modelem Ollama (np. Mistral) za pomocą biblioteki `httpx`.
7.  Żądanie do Ollamy zawiera instrukcje dotyczące formatu odpowiedzi (np. JSON z listą obiektów `question`/`answer`).
8.  Odpowiedź z Ollamy jest parsowana i walidowana.
9.  Jeśli generowanie powiedzie się, funkcja serwisowa zwraca listę obiektów `schemas.FlashcardCreate`.
10. Jeśli komunikacja z Ollamą zakończy się błędem lub zwróci nieprawidłowy format, funkcja serwisowa zgłasza odpowiedni wyjątek.
11. Punkt końcowy zwraca odpowiedź `200 OK` z wygenerowanymi fiszkami, sformatowanymi zgodnie ze schematem `schemas.AIGenerationResponse`.

## 6. Względy bezpieczeństwa

-   **Uwierzytelnienie**: Punkt końcowy jest chroniony i dostępny tylko dla uwierzytelnionych użytkowników.
-   **Walidacja danych wejściowych**: Pydantic waliduje `text` i `count`, zapobiegając nieprawidłowym danym.
-   **Ograniczenie rozmiaru tekstu**: Należy rozważyć ograniczenie maksymalnego rozmiaru `text`, aby zapobiec atakom DoS i nadmiernemu zużyciu zasobów AI.
-   **Sanityzacja danych AI**: Chociaż model AI powinien zwracać czysty tekst, zawsze należy rozważyć, czy odpowiedź AI nie zawiera złośliwego kodu lub treści, jeśli miałaby być renderowana bezpośrednio na frontendzie. W tym przypadku, ponieważ jest to tylko tekst, ryzyko jest mniejsze.
-   **HTTPS**: Komunikacja z API powinna odbywać się przez HTTPS.

## 7. Obsługa błędów

-   `401 Unauthorized`: Jeśli użytkownik nie jest uwierzytelniony.
-   `422 Unprocessable Entity`: Jeśli `text` jest pusty lub `count` jest poza zakresem (np. nie 5, 10, 15).
-   `500 Internal Server Error`: 
    -   Błędy komunikacji z usługą Ollama (np. usługa niedostępna, timeout).
    -   Błędy parsowania odpowiedzi z Ollamy.
    -   Inne nieoczekiwane błędy serwera.

## 8. Rozważania dotyczące wydajności

-   **Czas odpowiedzi AI**: Generowanie fiszek przez model AI może być czasochłonne. Należy monitorować czasy odpowiedzi Ollamy.
-   **Asynchroniczność**: Użycie `httpx` w trybie asynchronicznym jest kluczowe, aby nie blokować głównego wątku FastAPI podczas oczekiwania na odpowiedź z Ollamy.
-   **Limitowanie zapytań**: Należy rozważyć ograniczenie liczby zapytań do AI na użytkownika/IP, aby zapobiec nadużyciom i przeciążeniu serwera Ollama.

## 9. Etapy wdrożenia

1.  **Serwis Ollama**: Utwórz nowy plik `app/services/ollama_service.py`.
    -   Zaimplementuj funkcję `generate_flashcards(text: str, count: int) -> List[schemas.FlashcardCreate]`.
    -   Użyj `httpx.AsyncClient` do wysyłania żądań `POST` do endpointu Ollamy.
    -   Sformatuj prompt dla Ollamy, aby uzyskać odpowiedź w JSON z fiszkami.
    -   Obsłuż błędy komunikacji i parsowania odpowiedzi.
2.  **Router AI**: W pliku `app/routers/flashcards.py` (lub nowym `app/routers/ai.py`):
    -   Zaimplementuj punkt końcowy `POST /ai/generate-flashcards`.
    -   Użyj `schemas.AIGenerationRequest` jako typu dla ciała żądania.
    -   Wstrzyknij zależności uwierzytelnienia (np. `current_user: models.User = Depends(get_current_user)`).
    -   Wywołaj `ollama_service.generate_flashcards`.
    -   Obsłuż potencjalne `HTTPException` z serwisu Ollama.
    -   Zwróć odpowiedź w formacie `schemas.AIGenerationResponse`.
3.  **Integracja**: Upewnij się, że router jest dołączony do głównej instancji aplikacji FastAPI w `app/main.py`.