```markdown
# Plan implementacji widoku Strona Rejestracji

## 1. Przegląd
Widok "Strona Rejestracji" jest pierwszym krokiem dla nowych użytkowników, umożliwiając im utworzenie osobistego konta w aplikacji. Jego zadaniem jest zebranie unikalnej nazwy użytkownika i hasła, a następnie bezpieczne przetworzenie tych danych w celu stworzenia nowego rekordu w systemie. Proces musi być prosty, bezpieczny i zapewniać jasną informację zwrotną, realizując w pełni historyjkę użytkownika **US-001**.

## 2. Routing widoku
- **Ścieżka URL:** `/register`
- **Metody HTTP:** `GET`, `POST`
- **Plik backendu:** `app/routers/auth.py`
- **Funkcja renderująca:** Nowa funkcja w routerze, np. `register_view`, będzie odpowiedzialna za obsługę żądań `GET` (wyświetlenie pustego formularza) oraz `POST` (przetworzenie danych z formularza rejestracyjnego).

## 3. Struktura komponentów
Widok zostanie zaimplementowany jako pojedynczy szablon Jinja2, `app/templates/register.html`, który będzie rozszerzał główny szablon aplikacji `app/templates/base.html`.

```
register.html
└── base.html
    ├── Komponent Powiadomień o Błędach (np. Bootstrap Alert)
    │   (Renderowany warunkowo, gdy wystąpi błąd walidacji)
    │
    ├── Formularz Rejestracji
    │   (Główny komponent widoku)
    │
    └── Link do Logowania
        (Nawigacja dla powracających użytkowników)
```

## 4. Szczegóły komponentów

### Formularz Rejestracji
- **Opis komponentu:** Służy do zbierania danych niezbędnych do utworzenia nowego konta użytkownika.
- **Główne elementy:**
    - `<form method="post" action="/register">`: Formularz wysyłający dane na ten sam URL metodą POST.
    - `<div class="form-group">`: Kontener Bootstrap dla każdej pary etykieta-pole.
    - `<label for="username">Nazwa użytkownika</label>`: Etykieta dla pola nazwy użytkownika.
    - `<input type="text" id="username" name="username" class="form-control" required autofocus>`: Pole tekstowe na nazwę użytkownika.
    - `<label for="password">Hasło</label>`: Etykieta dla pola hasła.
    - `<input type="password" id="password" name="password" class="form-control" required>`: Pole hasła.
    - `<button type="submit" class="btn btn-primary">Zarejestruj się</button>`: Przycisk wysyłający formularz.
- **Obsługiwane interakcje:** Wysłanie formularza (submit).
- **Obsługiwana walidacja:** Podstawowa walidacja po stronie klienta za pomocą atrybutów `required`.
- **Typy:** Wysyła dane w formacie `application/x-www-form-urlencoded` z polami `username` i `password`.
- **Propsy:** Brak.

### Komponent Powiadomień o Błędach
- **Opis komponentu:** Wyświetla komunikaty o błędach walidacji po stronie serwera, np. gdy nazwa użytkownika jest już zajęta.
- **Główne elementy:**
    - `{% if error_message %}`: Blok warunkowy Jinja2 sprawdzający obecność błędu w kontekście.
    - `<div class="alert alert-danger" role="alert">{{ error_message }}</div>`: Komunikat o błędzie.
- **Obsługiwane interakcje:** Brak.
- **Obsługiwana walidacja:** Brak.
- **Typy:** Wymaga `ViewModel.error_message`.
- **Propsy:** Otrzymuje `error_message` z kontekstu szablonu.

## 5. Typy

### ViewModel (Kontekst Szablonu)
Słownik Pythona przekazywany z handlera FastAPI do szablonu `register.html`.
```python
# Konceptualna definicja słownika kontekstu
{
    "request": Request,
    "error_message": Optional[str]
}
```
- **`error_message`**: Opcjonalny ciąg znaków z komunikatem o błędzie, który ma zostać wyświetlony (np. "Ta nazwa użytkownika jest już zajęta").

## 6. Zarządzanie stanem
Stan jest zarządzany w całości po stronie serwera.
- **Stan początkowy:** Żądanie `GET /register` renderuje szablon bez żadnych komunikatów.
- **Stan błędu:** Nieudane żądanie `POST /register` (np. z powodu zajętej nazwy użytkownika) ponownie renderuje ten sam szablon `register.html`, przekazując w kontekście `error_message`.
- **Stan sukcesu:** Pomyślne żądanie `POST /register` nie renderuje ponownie widoku, lecz wykonuje przekierowanie na stronę logowania (`/login`), informując użytkownika o sukcesie (np. poprzez parametr w URL lub mechanizm flash messages).

## 7. Integracja API
Interakcja z API odbywa się wewnątrz backendu. Formularz HTML nie wykonuje bezpośrednich wywołań JavaScript do API.
1.  Przeglądarka wysyła standardowe żądanie `POST` z danymi formularza na ścieżkę `/register`.
2.  Handler `POST /register` w `app/routers/auth.py` odbiera te dane.
3.  Wewnątrz handlera tworzony jest obiekt `schemas.UserCreate`.
4.  Handler wywołuje funkcję `crud.create_user`, która realizuje logikę endpointu `POST /users` (sprawdzenie unikalności, haszowanie hasła, zapis do bazy danych).
5.  **W przypadku sukcesu:** Handler zwraca `RedirectResponse` na stronę `/login`.
6.  **W przypadku porażki:** Handler przechwytuje `HTTPException` (np. o kodzie 400 dla zduplikowanego użytkownika) i ponownie renderuje szablon `register.html` z odpowiednim komunikatem błędu.

## 8. Interakcje użytkownika
- **Wypełnianie formularza:** Użytkownik wpisuje żądaną nazwę użytkownika i hasło. Kursor jest domyślnie ustawiony w polu "nazwa użytkownika".
- **Wysłanie formularza:** Użytkownik klika przycisk "Zarejestruj się" lub naciska Enter.
- **Wynik sukcesu:** Użytkownik zostaje przekierowany na stronę logowania (`/login`), gdzie może zobaczyć komunikat o pomyślnej rejestracji.
- **Wynik błędu:** Strona rejestracji odświeża się, a nad formularzem pojawia się komunikat wyjaśniający błąd (np. "Nazwa użytkownika zajęta").
- **Nawigacja do logowania:** Użytkownik, który ma już konto, klika link "Masz już konto? Zaloguj się", co przenosi go na stronę `/login`.

## 9. Warunki i walidacja
- **Pola wymagane (klient):** Atrybuty `required` na polach `<input>` zapewniają podstawową walidację w przeglądarce.
- **Pola wymagane (serwer):** Handler `POST /register` musi zweryfikować, czy otrzymane pola `username` i `password` nie są puste.
- **Unikalność nazwy użytkownika:** Najważniejsza walidacja biznesowa. Jest realizowana w `crud.create_user` poprzez próbę zapytania do bazy o istniejącego użytkownika przed próbą zapisu. Jeśli użytkownik istnieje, zgłaszany jest błąd.

## 10. Obsługa błędów
- **Nazwa użytkownika zajęta:** `crud.create_user` zgłasza `HTTPException(status_code=400, detail="Username already registered")`. Handler `POST /register` przechwytuje ten wyjątek i renderuje stronę ponownie, przekazując `detail` jako `error_message`.
- **Inne błędy walidacji (np. puste pola):** Handler `POST /register` powinien obsłużyć te przypadki przed wywołaniem `crud` i zwrócić stronę z odpowiednim komunikatem.
- **Błędy serwera:** W przypadku nieoczekiwanego błędu (np. problem z bazą danych), powinien zostać zalogowany błąd, a użytkownikowi wyświetlony ogólny komunikat.

## 11. Kroki implementacji
1.  **Utworzenie szablonu:** Sprawdź, czy plik `app/templates/register.html` istnieje i dziedziczy z `base.html`.
2.  **Implementacja HTML:** W szablonie `register.html` zaimplementuj formularz z polami `username` i `password` oraz przyciskiem "Zarejestruj się". Użyj klas Bootstrapa dla stylizacji.
3.  **Logika błędów w szablonie:** Dodaj blok warunkowy `{% if error_message %}` do wyświetlania komunikatów o błędach.
4.  **Handler `GET /register`:** W `app/routers/auth.py` stwórz endpoint `GET /register`, który renderuje szablon `register.html` za pomocą `Jinja2Templates`.
5.  **Handler `POST /register`:** W tym samym pliku stwórz endpoint `POST /register`.
    a. Odczytaj dane z formularza (`await request.form()`).
    b. Zwaliduj, czy dane nie są puste.
    c. Użyj bloku `try...except HTTPException`.
    d. W bloku `try` wywołaj `crud.create_user` z danymi z formularza. Po sukcesie, zwróć `RedirectResponse(url="/login", status_code=303)`.
    e. W bloku `except` przechwyć wyjątek i ponownie wyrenderuj szablon `register.html`, przekazując `e.detail` jako `error_message`.
6.  **Link do logowania:** Upewnij się, że link "Masz już konto? Zaloguj się" poprawnie kieruje na ścieżkę `/login`.
