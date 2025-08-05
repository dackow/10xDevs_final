# API Endpoint Implementation Plan: GET /flashcard-sets/{set_id}

## 1. Przegląd punktu końcowego

Ten punkt końcowy umożliwia pobranie szczegółowych informacji o pojedynczym zestawie fiszek, w tym wszystkich fiszek należących do tego zestawu. Dostęp jest ograniczony do właściciela zestawu.

## 2. Szczegóły żądania

-   **Metoda HTTP**: `GET`
-   **Struktura URL**: `/flashcard-sets/{set_id}`
-   **Parametry**: 
    -   `set_id` (integer, wymagane): Unikalny identyfikator zestawu fiszek.

## 3. Wykorzystywane typy

-   **DTO (Data Transfer Object)**: `schemas.FlashcardSetDetail` (dla danych wyjściowych odpowiedzi, zawiera zagnieżdżone fiszki)
-   **Model Bazy Danych**: `models.FlashcardSet`, `models.Flashcard` (dla interakcji z bazą danych)

## 4. Szczegóły odpowiedzi

-   **Odpowiedź sukcesu (200 OK)**:
    ```json
    {
      "id": 1,
      "user_id": 1,
      "name": "string",
      "created_at": "2025-08-04T10:00:00Z",
      "flashcards": [
        {
          "id": 1,
          "set_id": 1,
          "question": "string",
          "answer": "string"
        }
      ]
    }
    ```
    -   **Schemat**: `schemas.FlashcardSetDetail`
-   **Odpowiedzi błędów**:
    -   `401 Unauthorized`: Jeśli użytkownik nie jest uwierzytelniony.
    -   `403 Forbidden`: Jeśli uwierzytelniony użytkownik nie jest właścicielem zestawu fiszek.
    -   `404 Not Found`: Jeśli zestaw fiszek o podanym `set_id` nie istnieje.
    -   `422 Unprocessable Entity`: Jeśli `set_id` jest nieprawidłowy (np. nie jest liczbą całkowitą).
    -   `500 Internal Server Error`: W przypadku nieoczekiwanego błędu serwera.

## 5. Przepływ danych

1.  Klient wysyła żądanie `GET` na adres `/flashcard-sets/{set_id}`.
2.  Router FastAPI przechwytuje żądanie.
3.  Punkt końcowy wymaga uwierzytelnienia użytkownika i pobiera `current_user`.
4.  `set_id` jest automatycznie walidowany przez FastAPI.
5.  Punkt końcowy wywołuje funkcję serwisową (np. `crud.get_flashcard_set`), przekazując `set_id`, `user_id` i instancję sesji bazy danych.
6.  Funkcja serwisowa wykonuje zapytanie do bazy danych, aby pobrać zestaw fiszek o podanym `set_id` i należący do danego `user_id`.
7.  Jeśli zestaw nie zostanie znaleziony (lub nie należy do użytkownika), funkcja serwisowa zwraca `None`.
8.  Jeśli zestaw zostanie znaleziony, funkcja serwisowa zwraca obiekt `models.FlashcardSet` (z załadowanymi relacjami do fiszek).
9.  Jeśli funkcja serwisowa zwróci `None`, punkt końcowy zgłasza `HTTPException` ze statusem `404 Not Found`.
10. Punkt końcowy zwraca odpowiedź `200 OK` z zestawem fiszek, sformatowanym zgodnie ze schematem `schemas.FlashcardSetDetail`.

## 6. Względy bezpieczeństwa

-   **Uwierzytelnienie**: Punkt końcowy jest chroniony i dostępny tylko dla uwierzytelnionych użytkowników.
-   **Autoryzacja**: Zapytanie jest filtrowane po `user_id` z tokena, co zapewnia, że użytkownik może pobrać tylko swoje własne zestawy fiszek. Próba dostępu do zestawu innego użytkownika skutkuje błędem `404 Not Found` (lub `403 Forbidden`, jeśli chcemy rozróżnić).
-   **Walidacja parametrów**: FastAPI automatycznie waliduje `set_id`.

## 7. Obsługa błędów

-   `401 Unauthorized`: Jeśli użytkownik nie jest uwierzytelniony.
-   `403 Forbidden`: Jeśli uwierzytelniony użytkownik próbuje uzyskać dostęp do zestawu, który nie należy do niego (alternatywa dla 404, jeśli chcemy ujawnić istnienie zasobu).
-   `404 Not Found`: Jeśli zestaw fiszek o podanym `set_id` nie istnieje lub nie należy do uwierzytelnionego użytkownika.
-   `422 Unprocessable Entity`: Jeśli `set_id` jest nieprawidłowy (np. nie jest liczbą całkowitą).
-   `500 Internal Server Error`: W przypadku nieoczekiwanego błędu serwera podczas interakcji z bazą danych.

## 8. Rozważania dotyczące wydajności

-   **Zapytanie do bazy danych**: Pobieranie pojedynczego zestawu i jego fiszek powinno być szybkie, zwłaszcza przy użyciu indeksów na `id` i `set_id`.
-   **Eager Loading**: Należy użyć `joinedload` lub `selectinload` w SQLAlchemy, aby pobrać fiszki wraz z zestawem w jednym zapytaniu, unikając problemu N+1.

## 9. Etapy wdrożenia

1.  **CRUD Operations**: W pliku `app/crud/crud.py` zaimplementuj funkcję `get_flashcard_set(db: Session, set_id: int, user_id: int) -> models.FlashcardSet | None`.
    -   Funkcja ta powinna pobierać zestaw fiszek po `id` i `user_id`, z załadowanymi fiszkami.
2.  **Router**: W pliku `app/routers/flashcards.py`:
    -   Zaimplementuj punkt końcowy `GET /flashcard-sets/{set_id}`.
    -   Wstrzyknij zależności: `db: Session = Depends(get_db)` i `current_user: models.User = Depends(get_current_user)`.
    -   Pobierz `set_id` ze ścieżki.
    -   Wywołaj `crud.get_flashcard_set`, przekazując `set_id` i `current_user.id`.
    -   Jeśli zestaw nie zostanie znaleziony, zgłoś `HTTPException` ze statusem 404.
    -   Zwróć zestaw w formacie `schemas.FlashcardSetDetail`.
3.  **Integracja**: Upewnij się, że router jest dołączony do głównej instancji aplikacji FastAPI w `app/main.py`.