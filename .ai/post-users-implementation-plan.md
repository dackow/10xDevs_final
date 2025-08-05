# API Endpoint Implementation Plan: POST /users

## 1. Przegląd punktu końcowego

Celem tego punktu końcowego jest umożliwienie rejestracji nowych użytkowników w systemie. Przyjmuje nazwę użytkownika i hasło, haszuje hasło i zapisuje nowego użytkownika w bazie danych.

## 2. Szczegóły żądania

-   **Metoda HTTP**: `POST`
-   **Struktura URL**: `/users`
-   **Parametry**: Brak parametrów w URL.
-   **Request Body**: 
    -   **Content-Type**: `application/json`
    -   **Pola**:
        -   `username` (string, wymagane): Unikalna nazwa użytkownika.
        -   `password` (string, wymagane): Hasło użytkownika.
    -   **Schemat**: `schemas.UserCreate`

## 3. Wykorzystywane typy

-   **Command Model**: `schemas.UserCreate` (dla danych wejściowych żądania)
-   **DTO (Data Transfer Object)**: `schemas.User` (dla danych wyjściowych odpowiedzi)
-   **Model Bazy Danych**: `models.User` (dla interakcji z bazą danych)

## 4. Szczegóły odpowiedzi

-   **Odpowiedź sukcesu (201 Created)**:
    ```json
    {
      "id": 1,
      "username": "string",
      "created_at": "2025-08-04T10:00:00Z",
      "updated_at": "2025-08-04T10:00:00Z"
    }
    ```
    -   **Schemat**: `schemas.User`
-   **Odpowiedzi błędów**:
    -   `400 Bad Request`: Zwracany, gdy nazwa użytkownika już istnieje.
    -   `422 Unprocessable Entity`: Zwracany automatycznie przez FastAPI, jeśli ciało żądania nie jest zgodne ze schematem `schemas.UserCreate` (np. brakuje pól, nieprawidłowy typ danych).
    -   `500 Internal Server Error`: W przypadku nieoczekiwanego błędu serwera.

## 5. Przepływ danych

1.  Klient wysyła żądanie `POST` na adres `/users` z danymi `username` i `password` w formacie JSON.
2.  Router FastAPI przechwytuje żądanie i automatycznie waliduje ciało żądania za pomocą `schemas.UserCreate`.
3.  Punkt końcowy wywołuje funkcję serwisową (np. `crud.create_user`), przekazując obiekt `schemas.UserCreate` i instancję sesji bazy danych.
4.  Funkcja serwisowa najpierw sprawdza, czy użytkownik o podanej nazwie użytkownika już istnieje w bazie danych.
5.  Jeśli użytkownik istnieje, funkcja serwisowa zgłasza błąd (np. `IntegrityError` lub niestandardowy wyjątek), który zostanie przechwycony w punkcie końcowym.
6.  Jeśli użytkownik nie istnieje, hasło jest haszowane przy użyciu `auth_service.get_password_hash`.
7.  Tworzony jest nowy obiekt `models.User` z haszowanym hasłem i pozostałymi danymi.
8.  Nowy obiekt użytkownika jest dodawany do sesji bazy danych i zatwierdzany.
9.  Funkcja serwisowa zwraca utworzony obiekt `models.User`.
10. Punkt końcowy zwraca odpowiedź `201 Created` z utworzonym obiektem użytkownika, sformatowanym zgodnie ze schematem `schemas.User`.

## 6. Względy bezpieczeństwa

-   **Haszowanie haseł**: Hasła są haszowane przy użyciu silnego algorytmu (Bcrypt) przed zapisaniem w bazie danych. Nigdy nie są przechowywane w postaci jawnego tekstu.
-   **Unikalność nazwy użytkownika**: Baza danych wymusza unikalność nazw użytkowników, zapobiegając duplikatom.
-   **Walidacja danych wejściowych**: Pydantic automatycznie waliduje dane wejściowe, zapobiegając wstrzykiwaniu nieprawidłowych lub złośliwych danych.
-   **HTTPS**: Cała komunikacja powinna odbywać się przez HTTPS, aby chronić dane uwierzytelniające w tranzycie.

## 7. Obsługa błędów

-   **Nazwa użytkownika już istnieje**: Jeśli próba utworzenia użytkownika zakończy się błędem unikalności (np. `IntegrityError` z SQLAlchemy), punkt końcowy powinien przechwycić ten błąd i zwrócić `HTTPException(status_code=400, detail="Username already registered")`.
-   **Nieprawidłowe dane wejściowe**: FastAPI automatycznie obsługuje błędy walidacji Pydantic, zwracając `422 Unprocessable Entity` ze szczegółami błędu.
-   **Błędy wewnętrzne**: Wszelkie inne nieoczekiwane błędy podczas interakcji z bazą danych powinny być przechwytywane, logowane i zwracana powinna być ogólna odpowiedź `500 Internal Server Error`.

## 8. Rozważania dotyczące wydajności

-   **Zapytanie o unikalność**: Sprawdzenie unikalności nazwy użytkownika jest szybkie dzięki indeksowi na kolumnie `username` w tabeli `users`.
-   **Haszowanie hasła**: Operacja haszowania hasła jest celowo intensywna obliczeniowo, ale jest to jednorazowa operacja podczas rejestracji i nie powinna stanowić wąskiego gardła.

## 9. Etapy wdrożenia

1.  **CRUD Operations**: W pliku `app/crud/crud.py` (lub dedykowanym serwisie dla użytkowników) zaimplementuj funkcję `create_user(db: Session, user: schemas.UserCreate) -> models.User`.
    -   Funkcja ta powinna przyjmować obiekt `schemas.UserCreate`.
    -   Sprawdź, czy użytkownik o danej nazwie już istnieje.
    -   Wywołaj `auth_service.get_password_hash` do haszowania hasła.
    -   Utwórz instancję `models.User` i dodaj ją do sesji bazy danych.
2.  **Router**: W pliku `app/routers/auth.py` (lub nowym `app/routers/users.py`):
    -   Zaimplementuj punkt końcowy `POST /users`.
    -   Użyj `schemas.UserCreate` jako typu dla ciała żądania.
    -   Wstrzyknij sesję bazy danych (`db: Session = Depends(get_db)`).
    -   Wywołaj funkcję `create_user` z serwisu/CRUD.
    -   Obsłuż `IntegrityError` (lub niestandardowy wyjątek) dla duplikatu nazwy użytkownika, zwracając `HTTPException` 400.
    -   Zwróć utworzonego użytkownika w formacie `schemas.User` ze statusem `201 Created`.
3.  **Integracja**: Upewnij się, że router jest dołączony do głównej instancji aplikacji FastAPI w `app/main.py`.