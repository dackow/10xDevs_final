# API Endpoint Implementation Plan: DELETE /flashcard-sets/{set_id}

## 1. Przegląd punktu końcowego

Ten punkt końcowy umożliwia usunięcie pojedynczego zestawu fiszek wraz ze wszystkimi powiązanymi z nim fiszkami. Dostęp jest ograniczony do właściciela zestawu.

## 2. Szczegóły żądania

-   **Metoda HTTP**: `DELETE`
-   **Struktura URL**: `/flashcard-sets/{set_id}`
-   **Parametry**: 
    -   `set_id` (integer, wymagane): Unikalny identyfikator zestawu fiszek do usunięcia.

## 3. Wykorzystywane typy

-   **Model Bazy Danych**: `models.FlashcardSet` (dla interakcji z bazą danych)

## 4. Szczegóły odpowiedzi

-   **Odpowiedź sukcesu (200 OK)**:
    ```json
    {
      "message": "Flashcard set deleted successfully"
    }
    ```
-   **Odpowiedzi błędów**:
    -   `401 Unauthorized`: Jeśli użytkownik nie jest uwierzytelniony.
    -   `403 Forbidden`: Jeśli uwierzytelniony użytkownik nie jest właścicielem zestawu fiszek.
    -   `404 Not Found`: Jeśli zestaw fiszek o podanym `set_id` nie istnieje.
    -   `422 Unprocessable Entity`: Jeśli `set_id` jest nieprawidłowy (np. nie jest liczbą całkowitą).
    -   `500 Internal Server Error`: W przypadku nieoczekiwanego błędu serwera.

## 5. Przepływ danych

1.  Klient wysyła żądanie `DELETE` na adres `/flashcard-sets/{set_id}`.
2.  Router FastAPI przechwytuje żądanie.
3.  Punkt końcowy wymaga uwierzytelnienia użytkownika i pobiera `current_user`.
4.  `set_id` jest automatycznie walidowany przez FastAPI.
5.  Punkt końcowy wywołuje funkcję serwisową (np. `crud.delete_flashcard_set`), przekazując `set_id`, `user_id` i instancję sesji bazy danych.
6.  Funkcja serwisowa najpierw próbuje pobrać zestaw fiszek o podanym `set_id` i należący do danego `user_id`.
7.  Jeśli zestaw nie zostanie znaleziony (lub nie należy do użytkownika), funkcja serwisowa zgłasza błąd (np. `HTTPException` 404 lub 403).
8.  Jeśli zestaw zostanie znaleziony, jest on usuwany z bazy danych. Dzięki `ON DELETE CASCADE` w definicji modelu `flashcards`, wszystkie powiązane fiszki zostaną automatycznie usunięte.
9.  Funkcja serwisowa zwraca potwierdzenie usunięcia.
10. Punkt końcowy zwraca odpowiedź `200 OK` z komunikatem o sukcesie.

## 6. Względy bezpieczeństwa

-   **Uwierzytelnienie**: Punkt końcowy jest chroniony i dostępny tylko dla uwierzytelnionych użytkowników.
-   **Autoryzacja**: Usunięcie jest możliwe tylko dla zestawów należących do uwierzytelnionego użytkownika. Zapobiega to przypadkowemu lub złośliwemu usunięciu danych innych użytkowników.
-   **Walidacja parametrów**: FastAPI automatycznie waliduje `set_id`.

## 7. Obsługa błędów

-   `401 Unauthorized`: Jeśli użytkownik nie jest uwierzytelniony.
-   `403 Forbidden`: Jeśli uwierzytelniony użytkownik próbuje usunąć zestaw, który nie należy do niego.
-   `404 Not Found`: Jeśli zestaw fiszek o podanym `set_id` nie istnieje lub nie należy do uwierzytelnionego użytkownika.
-   `422 Unprocessable Entity`: Jeśli `set_id` jest nieprawidłowy.
-   `500 Internal Server Error`: W przypadku nieoczekiwanego błędu serwera podczas interakcji z bazą danych.

## 8. Rozważania dotyczące wydajności

-   **Operacja usunięcia**: Usunięcie zestawu i kaskadowe usunięcie fiszek powinno być szybkie, zwłaszcza przy użyciu indeksów.

## 9. Etapy wdrożenia

1.  **CRUD Operations**: W pliku `app/crud/crud.py` zaimplementuj funkcję `delete_flashcard_set(db: Session, set_id: int, user_id: int)`.
    -   Funkcja ta powinna pobrać zestaw po `set_id` i `user_id`.
    -   Jeśli zestaw nie istnieje lub nie należy do użytkownika, zgłoś `HTTPException` (404 lub 403).
    -   Usuń zestaw z bazy danych.
2.  **Router**: W pliku `app/routers/flashcards.py`:
    -   Zaimplementuj punkt końcowy `DELETE /flashcard-sets/{set_id}`.
    -   Wstrzyknij zależności: `db: Session = Depends(get_db)` i `current_user: models.User = Depends(get_current_user)`.
    -   Pobierz `set_id` ze ścieżki.
    -   Wywołaj `crud.delete_flashcard_set`, przekazując `set_id` i `current_user.id`.
    -   Zwróć odpowiedź `200 OK` z komunikatem o sukcesie.
3.  **Integracja**: Upewnij się, że router jest dołączony do głównej instancji aplikacji FastAPI w `app/main.py`.