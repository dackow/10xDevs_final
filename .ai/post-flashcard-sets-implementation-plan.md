# API Endpoint Implementation Plan: POST /flashcard-sets

## 1. Przegląd punktu końcowego

Ten punkt końcowy umożliwia tworzenie nowego zestawu fiszek dla uwierzytelnionego użytkownika. Zestaw może zawierać listę fiszek, które zostaną do niego przypisane.

## 2. Szczegóły żądania

-   **Metoda HTTP**: `POST`
-   **Struktura URL**: `/flashcard-sets`
-   **Parametry**: Brak parametrów w URL.
-   **Request Body**: 
    -   **Content-Type**: `application/json`
    -   **Pola**:
        -   `name` (string, wymagane): Nazwa nowego zestawu fiszek.
        -   `flashcards` (array of objects, wymagane): Lista obiektów fiszek do dodania do zestawu. Każdy obiekt powinien zawierać `question` i `answer`.
    -   **Schemat**: `schemas.FlashcardSetCreate`

## 3. Wykorzystywane typy

-   **Command Model**: `schemas.FlashcardSetCreate` (dla danych wejściowych żądania)
-   **DTO (Data Transfer Object)**: `schemas.FlashcardSetDetail` (dla danych wyjściowych odpowiedzi, zawiera zagnieżdżone fiszki)
-   **Model Bazy Danych**: `models.FlashcardSet`, `models.Flashcard` (dla interakcji z bazą danych)

## 4. Szczegóły odpowiedzi

-   **Odpowiedź sukcesu (201 Created)**:
    ```json
    {
      "id": 1,
      "user_id": 1,
      "name": "string",
      "created_at": "2025-08-04T10:00:00Z",
      "flashcards": [
        {
          "id": 1,
          "question": "string",
          "answer": "string"
        }
      ]
    }
    ```
    -   **Schemat**: `schemas.FlashcardSetDetail`
-   **Odpowiedzi błędów**:
    -   `400 Bad Request`: Jeśli zestaw o tej samej nazwie już istnieje dla danego użytkownika.
    -   `401 Unauthorized`: Jeśli użytkownik nie jest uwierzytelniony.
    -   `422 Unprocessable Entity`: Jeśli ciało żądania jest nieprawidłowe (np. pusta nazwa, nieprawidłowa struktura fiszek).
    -   `500 Internal Server Error`: W przypadku nieoczekiwanego błędu serwera.

## 5. Przepływ danych

1.  Klient wysyła żądanie `POST` na adres `/flashcard-sets` z nazwą zestawu i listą fiszek w formacie JSON.
2.  Router FastAPI przechwytuje żądanie.
3.  Punkt końcowy wymaga uwierzytelnienia użytkownika i pobiera `current_user`.
4.  Dane wejściowe są walidowane przez `schemas.FlashcardSetCreate`.
5.  Punkt końcowy wywołuje funkcję serwisową (np. `crud.create_flashcard_set`), przekazując `schemas.FlashcardSetCreate`, `user_id` i instancję sesji bazy danych.
6.  Funkcja serwisowa najpierw sprawdza, czy zestaw o podanej nazwie już istnieje dla danego `user_id`.
7.  Jeśli zestaw istnieje, funkcja serwisowa zgłasza błąd (np. `IntegrityError` lub niestandardowy wyjątek).
8.  Jeśli zestaw nie istnieje, tworzony jest nowy obiekt `models.FlashcardSet`.
9.  Dla każdej fiszki w `schemas.FlashcardSetCreate.flashcards`, tworzony jest nowy obiekt `models.Flashcard` i przypisywany do nowo utworzonego zestawu.
10. Nowy zestaw i jego fiszki są dodawane do sesji bazy danych i zatwierdzane.
11. Funkcja serwisowa zwraca utworzony obiekt `models.FlashcardSet` (z załadowanymi relacjami do fiszek).
12. Punkt końcowy zwraca odpowiedź `201 Created` z utworzonym zestawem fiszek, sformatowanym zgodnie ze schematem `schemas.FlashcardSetDetail`.

## 6. Względy bezpieczeństwa

-   **Uwierzytelnienie**: Punkt końcowy jest chroniony i dostępny tylko dla uwierzytelnionych użytkowników.
-   **Autoryzacja**: Zestawy fiszek są zawsze tworzone w kontekście uwierzytelnionego użytkownika (`user_id` z tokena), co zapobiega tworzeniu zestawów dla innych użytkowników.
-   **Walidacja danych wejściowych**: Pydantic waliduje nazwę zestawu i strukturę fiszek, zapobiegając nieprawidłowym danym.
-   **Unikalność nazwy zestawu**: Baza danych wymusza unikalność nazwy zestawu dla danego użytkownika.

## 7. Obsługa błędów

-   `401 Unauthorized`: Jeśli użytkownik nie jest uwierzytelniony.
-   `400 Bad Request`: Jeśli zestaw o tej samej nazwie już istnieje dla danego użytkownika (wynik `IntegrityError`).
-   `422 Unprocessable Entity`: Jeśli ciało żądania jest nieprawidłowe (np. pusta nazwa, pusta lista fiszek, nieprawidłowa struktura fiszki).
-   `500 Internal Server Error`: W przypadku nieoczekiwanego błędu serwera.

## 8. Rozważania dotyczące wydajności

-   **Operacje na bazie danych**: Tworzenie wielu fiszek w jednej transakcji jest wydajne. Należy jednak uważać na bardzo duże zestawy fiszek, które mogą spowolnić operację.
-   **Indeksy**: Indeksy na `user_id` w `flashcard_sets` i `set_id` w `flashcards` zapewniają szybkie operacje wyszukiwania i tworzenia relacji.

## 9. Etapy wdrożenia

1.  **CRUD Operations**: W pliku `app/crud/crud.py` zaimplementuj funkcję `create_flashcard_set(db: Session, set_data: schemas.FlashcardSetCreate, user_id: int) -> models.FlashcardSet`.
    -   Funkcja ta powinna przyjmować `set_data` i `user_id`.
    -   Sprawdź unikalność nazwy zestawu dla danego użytkownika.
    -   Utwórz `models.FlashcardSet`.
    -   Iteruj po `set_data.flashcards` i utwórz `models.Flashcard` dla każdej z nich, przypisując `set_id`.
    -   Dodaj wszystkie obiekty do sesji i zatwierdź.
    -   Zwróć utworzony zestaw (z załadowanymi fiszkami).
2.  **Router**: W pliku `app/routers/flashcards.py`:
    -   Zaimplementuj punkt końcowy `POST /flashcard-sets`.
    -   Użyj `schemas.FlashcardSetCreate` jako typu dla ciała żądania.
    -   Wstrzyknij zależności: `db: Session = Depends(get_db)` i `current_user: models.User = Depends(get_current_user)`.
    -   Wywołaj `crud.create_flashcard_set`, przekazując `set_data` i `current_user.id`.
    -   Obsłuż `IntegrityError` dla duplikatu nazwy zestawu, zwracając `HTTPException` 400.
    -   Zwróć utworzony zestaw w formacie `schemas.FlashcardSetDetail` ze statusem `201 Created`.
3.  **Integracja**: Upewnij się, że router jest dołączony do głównej instancji aplikacji FastAPI w `app/main.py`.