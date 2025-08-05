# API Endpoint Implementation Plan: PUT /flashcards/{card_id}

## 1. Przegląd punktu końcowego

Ten punkt końcowy umożliwia aktualizację treści pojedynczej fiszki (pytania i odpowiedzi). Dostęp jest ograniczony do właściciela zestawu, do którego należy fiszka.

## 2. Szczegóły żądania

-   **Metoda HTTP**: `PUT`
-   **Struktura URL**: `/flashcards/{card_id}`
-   **Parametry**: 
    -   `card_id` (integer, wymagane): Unikalny identyfikator fiszki do zaktualizowania.
-   **Request Body**: 
    -   **Content-Type**: `application/json`
    -   **Pola**:
        -   `question` (string, wymagane): Nowa treść pytania fiszki.
        -   `answer` (string, wymagane): Nowa treść odpowiedzi fiszki.
    -   **Schemat**: `schemas.FlashcardUpdate`

## 3. Wykorzystywane typy

-   **Command Model**: `schemas.FlashcardUpdate` (dla danych wejściowych żądania)
-   **DTO (Data Transfer Object)**: `schemas.Flashcard` (dla danych wyjściowych odpowiedzi)
-   **Model Bazy Danych**: `models.Flashcard` (dla interakcji z bazą danych)

## 4. Szczegóły odpowiedzi

-   **Odpowiedź sukcesu (200 OK)**:
    ```json
    {
      "id": 1,
      "set_id": 1,
      "question": "string",
      "answer": "string",
      "created_at": "2025-08-04T10:00:00Z",
      "updated_at": "2025-08-04T11:00:00Z"
    }
    ```
    -   **Schemat**: `schemas.Flashcard`
-   **Odpowiedzi błędów**:
    -   `401 Unauthorized`: Jeśli użytkownik nie jest uwierzytelniony.
    -   `403 Forbidden`: Jeśli uwierzytelniony użytkownik nie jest właścicielem zestawu, do którego należy fiszka.
    -   `404 Not Found`: Jeśli fiszka o podanym `card_id` nie istnieje.
    -   `422 Unprocessable Entity`: Jeśli ciało żądania jest nieprawidłowe (np. puste pola `question` lub `answer`).
    -   `500 Internal Server Error`: W przypadku nieoczekiwanego błędu serwera.

## 5. Przepływ danych

1.  Klient wysyła żądanie `PUT` na adres `/flashcards/{card_id}` z nową treścią fiszki w formacie JSON.
2.  Router FastAPI przechwytuje żądanie.
3.  Punkt końcowy wymaga uwierzytelnienia użytkownika i pobiera `current_user`.
4.  `card_id` jest automatycznie walidowany przez FastAPI.
5.  Dane wejściowe są walidowane przez `schemas.FlashcardUpdate`.
6.  Punkt końcowy wywołuje funkcję serwisową (np. `crud.update_flashcard`), przekazując `card_id`, `user_id` (z `current_user`) i instancję sesji bazy danych, oraz `flashcard_data`.
7.  Funkcja serwisowa najpierw próbuje pobrać fiszkę o podanym `card_id` i sprawdzić, czy należy ona do zestawu, którego właścicielem jest `user_id`.
8.  Jeśli fiszka nie zostanie znaleziona lub nie należy do użytkownika, funkcja serwisowa zgłasza błąd (np. `HTTPException` 404 lub 403).
9.  Jeśli fiszka zostanie znaleziona i autoryzowana, jej pola `question` i `answer` są aktualizowane, a `updated_at` jest ustawiane na bieżącą datę/czas.
10. Zmiany są zatwierdzane w bazie danych.
11. Funkcja serwisowa zwraca zaktualizowany obiekt `models.Flashcard`.
12. Punkt końcowy zwraca odpowiedź `200 OK` z zaktualizowaną fiszką, sformatowaną zgodnie ze schematem `schemas.Flashcard`.

## 6. Względy bezpieczeństwa

-   **Uwierzytelnienie**: Punkt końcowy jest chroniony i dostępny tylko dla uwierzytelnionych użytkowników.
-   **Autoryzacja**: Aktualizacja jest możliwa tylko dla fiszek należących do zestawów, których właścicielem jest uwierzytelniony użytkownik. Zapobiega to modyfikacji danych innych użytkowników.
-   **Walidacja danych wejściowych**: Pydantic waliduje `question` i `answer`, zapobiegając nieprawidłowym danym.

## 7. Obsługa błędów

-   `401 Unauthorized`: Jeśli użytkownik nie jest uwierzytelniony.
-   `403 Forbidden`: Jeśli uwierzytelniony użytkownik próbuje zaktualizować fiszkę, która nie należy do niego.
-   `404 Not Found`: Jeśli fiszka o podanym `card_id` nie istnieje.
-   `422 Unprocessable Entity`: Jeśli ciało żądania jest nieprawidłowe (np. puste `question` lub `answer`).
-   `500 Internal Server Error`: W przypadku nieoczekiwanego błędu serwera.

## 8. Rozważania dotyczące wydajności

-   **Operacja aktualizacji**: Aktualizacja pojedynczego rekordu powinna być szybka, zwłaszcza przy użyciu indeksów.

## 9. Etapy wdrożenia

1.  **CRUD Operations**: W pliku `app/crud/crud.py` zaimplementuj funkcję `update_flashcard(db: Session, card_id: int, user_id: int, flashcard_data: schemas.FlashcardUpdate) -> models.Flashcard`.
    -   Funkcja ta powinna pobrać fiszkę po `card_id` i sprawdzić jej przynależność do użytkownika.
    -   Jeśli fiszka nie istnieje lub nie należy do użytkownika, zgłoś `HTTPException` (404 lub 403).
    -   Zaktualizuj pola `question` i `answer` oraz `updated_at`.
    -   Zatwierdź zmiany i odśwież obiekt.
    -   Zwróć zaktualizowaną fiszkę.
2.  **Router**: W pliku `app/routers/flashcards.py`:
    -   Zaimplementuj punkt końcowy `PUT /flashcards/{card_id}`.
    -   Użyj `schemas.FlashcardUpdate` jako typu dla ciała żądania.
    -   Wstrzyknij zależności: `db: Session = Depends(get_db)` i `current_user: models.User = Depends(get_current_user)`.
    -   Pobierz `card_id` ze ścieżki.
    -   Wywołaj `crud.update_flashcard`, przekazując `card_id`, `current_user.id` i `flashcard_data`.
    -   Zwróć zaktualizowaną fiszkę w formacie `schemas.Flashcard`.
3.  **Integracja**: Upewnij się, że router jest dołączony do głównej instancji aplikacji FastAPI w `app/main.py`.