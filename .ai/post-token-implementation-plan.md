# API Endpoint Implementation Plan: POST /token

## 1. Przegląd punktu końcowego

Celem tego punktu końcowego jest uwierzytelnienie użytkownika na podstawie jego nazwy użytkownika i hasła. Po pomyślnej weryfikacji, punkt końcowy generuje i zwraca token dostępowy JWT (JSON Web Token), który może być używany do autoryzacji w chronionych zasobach API.

## 2. Szczegóły żądania

-   **Metoda HTTP**: `POST`
-   **Struktura URL**: `/token`
-   **Parametry**: Brak parametrów w URL.
-   **Request Body**: 
    -   **Content-Type**: `application/x-www-form-urlencoded`
    -   **Pola**:
        -   `username` (string, wymagane): Nazwa użytkownika.
        -   `password` (string, wymagane): Hasło użytkownika.

## 3. Wykorzystywane typy

-   **FastAPI Dependency**: `OAuth2PasswordRequestForm` zostanie użyty do przechwycenia i walidacji danych formularza `username` i `password`.
-   **DTOs (Data Transfer Objects)**:
    -   `schemas.Token`: Używany do strukturyzowania odpowiedzi zawierającej token dostępowy.
    -   `schemas.TokenData`: Używany do definiowania danych, które zostaną zakodowane wewnątrz tokena JWT.
-   **Modele Bazy Danych**:
    -   `models.User`: Używany do pobrania danych użytkownika z bazy danych w celu weryfikacji.

## 4. Szczegóły odpowiedzi

-   **Odpowiedź sukcesu (200 OK)**:
    ```json
    {
      "access_token": "string",
      "token_type": "bearer"
    }
    ```
-   **Odpowiedzi błędów**:
    -   `400 Bad Request`: Zwracany, gdy podane poświadczenia (nazwa użytkownika lub hasło) są nieprawidłowe.
    -   `422 Unprocessable Entity`: Zwracany automatycznie przez FastAPI, jeśli ciało żądania nie jest poprawnie sformatowane (np. brakuje pól).

## 5. Przepływ danych

1.  Klient wysyła żądanie `POST` na adres `/token` z danymi `username` i `password` w formacie `application/x-www-form-urlencoded`.
2.  Router FastAPI przechwytuje żądanie.
3.  Zależność `OAuth2PasswordRequestForm` jest wstrzykiwana do funkcji endpointu, walidując obecność wymaganych pól.
4.  Punkt końcowy wywołuje funkcję serwisową (np. `auth_service.authenticate_user`), przekazując nazwę użytkownika i hasło.
5.  Funkcja serwisowa pobiera użytkownika z bazy danych na podstawie nazwy użytkownika przy użyciu SQLAlchemy.
6.  Jeśli użytkownik nie zostanie znaleziony, funkcja zwraca `False`.
7.  Jeśli użytkownik zostanie znaleziony, funkcja używa biblioteki `passlib` do bezpiecznego porównania dostarczonego hasła z hashem przechowywanym w bazie danych (`password_hash`).
8.  Jeśli hasła nie pasują, funkcja zwraca `False`. W przeciwnym razie zwraca obiekt `User`.
9.  Jeśli uwierzytelnienie w punkcie końcowym nie powiedzie się, zgłaszany jest `HTTPException` ze statusem `400`.
10. Jeśli uwierzytelnienie się powiedzie, wywoływana jest kolejna funkcja serwisowa (np. `auth_service.create_access_token`) w celu wygenerowania tokena JWT.
11. Punkt końcowy zwraca odpowiedź `200 OK` z tokenem sformatowanym zgodnie ze schematem `schemas.Token`.

## 6. Względy bezpieczeństwa

-   **Haszowanie haseł**: Hasła muszą być haszowane przy użyciu silnego, adaptacyjnego algorytmu, takiego jak **Bcrypt**. Biblioteka `passlib` zostanie użyta do obsługi haszowania i weryfikacji.
-   **Bezpieczeństwo JWT**: 
    -   Klucz tajny (`SECRET_KEY`) używany do podpisywania tokenów musi być silny, losowy i przechowywany jako zmienna środowiskowa, a nie zakodowany na stałe w kodzie.
    -   Tokeny powinny mieć krótki czas wygaśnięcia (np. 15-60 minut), aby zminimalizować ryzyko ich przejęcia.
-   **Ochrona przed atakami Brute-Force**: Należy zaimplementować ograniczanie liczby żądań (rate limiting) na tym punkcie końcowym, aby spowolnić próby odgadnięcia haseł. Można do tego użyć biblioteki `slowapi`.
-   **Transport**: Cała komunikacja musi odbywać się przez HTTPS, aby chronić dane uwierzytelniające i tokeny w tranzycie.

## 7. Obsługa błędów

-   **Nieprawidłowe poświadczenia**: Jeśli `authenticate_user` zwróci `False`, punkt końcowy musi zwrócić `HTTPException(status_code=400, detail="Incorrect username or password")`.
-   **Błędy wewnętrzne**: Wszelkie nieoczekiwane błędy podczas interakcji z bazą danych lub generowania tokena powinny być przechwytywane i logowane, a do klienta powinna być zwracana ogólna odpowiedź `500 Internal Server Error`.

## 8. Rozważania dotyczące wydajności

-   **Zapytanie do bazy danych**: Zapytanie o użytkownika po nazwie użytkownika powinno być szybkie. Należy upewnić się, że kolumna `users.username` ma założony indeks (zgodnie z `db-plan.md`).
-   **Haszowanie haseł**: Operacje haszowania (szczególnie weryfikacja) są celowo intensywne obliczeniowo, aby zapobiegać atakom. Jest to oczekiwane i akceptowalne zachowanie dla tego punktu końcowego.

## 9. Etapy wdrożenia

1.  **Zależności**: Dodaj `passlib[bcrypt]` i `python-jose[cryptography]` do pliku `requirements.txt`.
2.  **Konfiguracja**: Zdefiniuj `SECRET_KEY`, `ALGORITHM` i `ACCESS_TOKEN_EXPIRE_MINUTES` w module konfiguracyjnym, ładując wartości ze zmiennych środowiskowych.
3.  **Serwis uwierzytelniania**: Utwórz nowy plik `app/services/auth_service.py`.
    -   Zaimplementuj funkcję `verify_password(plain_password, hashed_password)` używając `passlib`.
    -   Zaimplementuj funkcję `get_password_hash(password)` używając `passlib`.
    -   Zaimplementuj funkcję `authenticate_user(db: Session, username: str, password: str) -> models.User | bool`, która pobiera użytkownika i weryfikuje hasło.
    -   Zaimplementuj funkcję `create_access_token(data: dict, expires_delta: timedelta | None = None)` używając `jose.jwt`.
4.  **Router**: W pliku `app/routers/auth.py`:
    -   Zdefiniuj `OAuth2PasswordBearer`.
    -   Stwórz router FastAPI (`APIRouter`).
    -   Zaimplementuj punkt końcowy `POST /token`.
    -   Użyj `Annotated[OAuth2PasswordRequestForm, Depends()]` do wstrzyknięcia danych formularza.
    -   Wywołaj `auth_service.authenticate_user` w celu weryfikacji poświadczeń.
    -   W przypadku niepowodzenia, zgłoś `HTTPException` ze statusem 400.
    -   W przypadku powodzenia, wywołaj `auth_service.create_access_token` w celu stworzenia tokena.
    -   Zwróć odpowiedź w formacie `schemas.Token`.
5.  **Integracja**: W głównym pliku aplikacji (`app/main.py`), dołącz nowo utworzony router do głównej instancji aplikacji FastAPI.