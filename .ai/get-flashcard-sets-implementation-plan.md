# API Endpoint Implementation Plan: GET /flashcard-sets

## 1. Przegląd punktu końcowego

Ten punkt końcowy umożliwia pobranie listy wszystkich zestawów fiszek należących do uwierzytelnionego użytkownika. Obsługuje paginację.

## 2. Szczegóły żądania

-   **Metoda HTTP**: `GET`
-   **Struktura URL**: `/flashcard-sets`
-   **Parametry**: 
    -   `skip` (integer, opcjonalne, domyślnie: 0): Liczba rekordów do pominięcia (dla paginacji).
    -   `limit` (integer, opcjonalne, domyślnie: 100): Maksymalna liczba rekordów do zwrócenia.

## 3. Wykorzystywane typy

-   **DTO (Data Transfer Object)**: `schemas.FlashcardSet` (dla każdego zestawu na liście)
-   **Model Bazy Danych**: `models.FlashcardSet` (dla interakcji z bazą danych)

## 4. Szczegóły odpowiedzi

-   **Odpowiedź sukcesu (200 OK)**:
    ```json
    [
      {
        "id": 1,
        "user_id": 1,
        "name": "string",
        "created_at": "2025-08-04T10:00:00Z",
        "updated_at": "2025-08-04T10:00:00Z"
      }
    ]
    ```
    -   **Schemat**: `List[schemas.FlashcardSet]`
-   **Odpowiedzi błędów**:
    -   `401 Unauthorized`: Jeśli użytkownik nie jest uwierzytelniony.
    -   `422 Unprocessable Entity`: Jeśli parametry zapytania są nieprawidłowe (np. `skip` lub `limit` są ujemne).
    -   `500 Internal Server Error`: W przypadku nieoczekiwanego błędu serwera.

## 5. Przepływ danych

1.  Klient wysyła żądanie `GET` na adres `/flashcard-sets` z opcjonalnymi parametrami `skip` i `limit`.
2.  Router FastAPI przechwytuje żądanie.
3.  Punkt końcowy wymaga uwierzytelnienia użytkownika i pobiera `current_user`.
4.  Parametry `skip` i `limit` są automatycznie walidowane przez FastAPI.
5.  Punkt końcowy wywołuje funkcję serwisową (np. `crud.get_flashcard_sets`), przekazując `user_id`, `skip`, `limit` i instancję sesji bazy danych.
6.  Funkcja serwisowa wykonuje zapytanie do bazy danych, aby pobrać zestawy fiszek należące do danego `user_id`, stosując `offset` (skip) i `limit`.
7.  Funkcja serwisowa zwraca listę obiektów `models.FlashcardSet`.
8.  Punkt końcowy zwraca odpowiedź `200 OK` z listą zestawów fiszek, sformatowanych zgodnie ze schematem `List[schemas.FlashcardSet]`.

## 6. Względy bezpieczeństwa

-   **Uwierzytelnienie**: Punkt końcowy jest chroniony i dostępny tylko dla uwierzytelnionych użytkowników.
-   **Autoryzacja**: Zapytania są filtrowane po `user_id` z tokena, co zapewnia, że użytkownik może pobrać tylko swoje własne zestawy fiszek.
-   **Walidacja parametrów**: FastAPI automatycznie waliduje parametry zapytania, zapobiegając nieprawidłowym wartościom.

## 7. Obsługa błędów

-   `401 Unauthorized`: Jeśli użytkownik nie jest uwierzytelniony.
-   `422 Unprocessable Entity`: Jeśli `skip` lub `limit` są nieprawidłowe (np. ujemne).
-   `500 Internal Server Error`: W przypadku nieoczekiwanego błędu serwera podczas interakcji z bazą danych.

## 8. Rozważania dotyczące wydajności

-   **Paginacja**: Użycie `skip` i `limit` (offset/limit) jest standardową metodą paginacji, która jest wydajna dla większości przypadków. Indeks na `user_id` w tabeli `flashcard_sets` przyspiesza zapytania.
-   **Liczba rekordów**: Domyślny limit 100 rekordów zapobiega pobieraniu zbyt dużych zbiorów danych w jednym żądaniu.

## 9. Etapy wdrożenia

1.  **CRUD Operations**: W pliku `app/crud/crud.py` zaimplementuj funkcję `get_flashcard_sets(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.FlashcardSet]`.
    -   Funkcja ta powinna wykonywać zapytanie do bazy danych, filtrując po `user_id` i stosując `offset` oraz `limit`.
2.  **Router**: W pliku `app/routers/flashcards.py`:
    -   Zaimplementuj punkt końcowy `GET /flashcard-sets`.
    -   Wstrzyknij zależności: `db: Session = Depends(get_db)`, `current_user: models.User = Depends(get_current_user)`, `skip: int = Query(0, ge=0)` i `limit: int = Query(100, ge=0, le=100)`.
    -   Wywołaj `crud.get_flashcard_sets`, przekazując `current_user.id`, `skip` i `limit`.
    -   Zwróć listę zestawów w formacie `List[schemas.FlashcardSet]`.
3.  **Integracja**: Upewnij się, że router jest dołączony do głównej instancji aplikacji FastAPI w `app/main.py`.