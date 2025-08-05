# Plan implementacji widoku Strona Logowania

## 1. Przegląd
Widok "Strona Logowania" jest bramą dostępu do aplikacji dla zarejestrowanych użytkowników. Jego głównym celem jest zebranie poświadczeń (nazwy użytkownika i hasła), bezpieczne ich zweryfikowanie po stronie serwera i w przypadku sukcesu, ustanowienie sesji użytkownika. Widok musi być prosty, intuicyjny i jasno komunikować ewentualne błędy logowania, zgodnie z historyjką użytkownika **US-002**.

## 2. Routing widoku
- **Ścieżka URL:** `/login`
- **Metody HTTP:** `GET`, `POST`
- **Plik backendu:** `app/routers/auth.py` (lub dedykowany router dla widoków, jeśli zostanie wprowadzony).
- **Funkcja renderująca:** Nowa funkcja w routerze, np. `login_view`, będzie obsługiwać żądania `GET` (wyświetlanie formularza) oraz `POST` (przetwarzanie danych logowania).

## 3. Struktura komponentów
Widok będzie renderowany przez jeden plik szablonu Jinja2, `app/templates/login.html`, który dziedziczy ze wspólnego szablonu `app/templates/base.html`.

```
login.html
└── base.html
    ├── Komponent Powiadomień o Błędach (np. Bootstrap Alert)
    │   (Renderowany warunkowo, jeśli w kontekście szablonu znajduje się komunikat o błędzie)
    │
    ├── Formularz Logowania
    │   (Główny element widoku)
    │
    └── Link do Rejestracji
        (Nawigacja dla nowych użytkowników)
```

## 4. Szczegóły komponentów

### Formularz Logowania
- **Opis komponentu:** Centralny element strony, składający się z pól na dane uwierzytelniające i przycisku akcji.
- **Główne elementy:**
    - `<form method="post" action="/login">`: Formularz wysyłający dane na ten sam URL metodą POST.
    - `<div class="form-group">`: Kontener dla każdej pary etykieta-pole.
    - `<label for="username">`: Etykieta dla pola nazwy użytkownika.
    - `<input type="text" id="username" name="username" class="form-control" required autofocus>`: Pole do wpisania nazwy użytkownika.
    - `<label for="password">`: Etykieta dla pola hasła.
    - `<input type="password" id="password" name="password" class="form-control" required>`: Pole do wpisania hasła.
    - `<button type="submit" class="btn btn-primary">Zaloguj się</button>`: Przycisk inicjujący proces logowania.
- **Obsługiwane interakcje:** Wysłanie formularza (submit).
- **Obsługiwana walidacja:** Podstawowa walidacja po stronie klienta za pomocą atrybutów `required`.
- **Typy:** Wysyła dane w formacie `application/x-www-form-urlencoded` z polami `username` i `password`.
- **Propsy:** Brak (komponent statyczny w szablonie).

### Komponent Powiadomień o Błędach
- **Opis komponentu:** Prosty, warunkowo renderowany blok do wyświetlania błędów logowania.
- **Główne elementy:**
    - `{% if error_message %}`: Blok warunkowy Jinja2.
    - `<div class="alert alert-danger" role="alert">{{ error_message }}</div>`: Komunikat o błędzie stylizowany za pomocą Bootstrapa.
- **Obsługiwane interakcje:** Brak.
- **Obsługiwana walidacja:** Brak.
- **Typy:** Wymaga `ViewModel.error_message`.
- **Propsy:** Otrzymuje `error_message` z kontekstu szablonu.

## 5. Typy

### ViewModel (Kontekst Szablonu)
Słownik Pythona przekazywany z handlera FastAPI do szablonu `login.html` podczas renderowania.
```python
# Konceptualna definicja słownika kontekstu
{
    "request": Request,
    "error_message": Optional[str]
}
```
- **`error_message`**: Opcjonalny ciąg znaków zawierający komunikat o błędzie do wyświetlenia użytkownikowi (np. "Nieprawidłowa nazwa użytkownika lub hasło").

## 6. Zarządzanie stanem
Zarządzanie stanem odbywa się w całości po stronie serwera (server-side state).
- **Stan początkowy:** Żądanie `GET /login` renderuje szablon bez komunikatu o błędzie.
- **Stan błędu:** Żądanie `POST /login`, które kończy się niepowodzeniem, ponownie renderuje ten sam szablon, przekazując w kontekście `error_message`.
- **Stan sukcesu:** Pomyślne żądanie `POST /login` nie renderuje ponownie widoku, lecz zwraca odpowiedź `RedirectResponse`, która przekierowuje przeglądarkę na `/dashboard`. Token sesji jest zarządzany za pomocą ciasteczka `HttpOnly`.

## 7. Integracja API
Interfejs użytkownika (formularz HTML) nie komunikuje się bezpośrednio z API `POST /token` za pomocą JavaScript. Zamiast tego, interakcja jest w pełni obsługiwana przez backend FastAPI.

1.  Przeglądarka wysyła standardowe żądanie `POST` z danymi formularza na adres `/login`.
2.  Handler `POST /login` w `app/routers/auth.py` przechwytuje te dane.
3.  Wewnątrz tego handlera, aplikacja (backend) wywołuje swoją własną logikę uwierzytelniania, która korzysta z `auth_service.authenticate_user` i `auth_service.create_access_token` (logika stojąca za endpointem `/token`).
4.  **W przypadku sukcesu:** Handler generuje token, ustawia go w ciasteczku `HttpOnly` w odpowiedzi i zwraca `RedirectResponse(url="/dashboard", status_code=303)`.
5.  **W przypadku porażki:** Handler przechwytuje wyjątek `HTTPException` z serwisu autoryzacji i ponownie renderuje szablon `login.html`, przekazując komunikat o błędzie w kontekście.

## 8. Interakcje użytkownika
- **Wypełnienie formularza:** Użytkownik wpisuje swoją nazwę użytkownika i hasło. Kursor jest domyślnie ustawiony w polu "nazwa użytkownika".
- **Wysłanie formularza:** Użytkownik klika przycisk "Zaloguj się" lub naciska Enter w jednym z pól.
- **Wynik sukcesu:** Przeglądarka zostaje przekierowana na stronę panelu głównego (`/dashboard`).
- **Wynik błędu:** Strona logowania odświeża się, a nad formularzem pojawia się czerwony baner z informacją o błędzie.
- **Nawigacja do rejestracji:** Użytkownik klika link "Nie masz konta? Zarejestruj się", co przenosi go na stronę `/register`.

## 9. Warunki i walidacja
- **Pola wymagane (klient):** Atrybuty `required` na polach `<input>` uniemożliwiają wysłanie pustego formularza w nowoczesnych przeglądarkach.
- **Pola wymagane (serwer):** Handler `POST /login` musi sprawdzić, czy `username` i `password` nie są puste, zanim przekaże je do serwisu autoryzacji. Jeśli są puste, powinien od razu zwrócić błąd walidacji.
- **Poprawność poświadczeń:** Główna walidacja odbywa się w `auth_service`, które sprawdza, czy użytkownik istnieje i czy hasło jest poprawne. Wynik tej walidacji determinuje dalszy przepływ (przekierowanie lub błąd).

## 10. Obsługa błędów
- **Nieprawidłowe dane logowania:** Gdy `auth_service.authenticate_user` zwróci `None`, handler `POST /login` przechwytuje ten stan i renderuje `login.html` z `error_message="Nieprawidłowa nazwa użytkownika lub hasło."`.
- **Błędy serwera:** Wszelkie nieoczekiwane wyjątki (np. błąd połączenia z bazą danych) powinny być logowane, a użytkownikowi powinien zostać wyświetlony ogólny komunikat o błędzie, np. "Wystąpił nieoczekiwany błąd. Spróbuj ponownie później.".

## 11. Kroki implementacji
1.  **Utworzenie szablonu:** Upewnij się, że plik `app/templates/login.html` istnieje i dziedziczy z `base.html`.
2.  **Struktura HTML:** Zaimplementuj w szablonie strukturę formularza z polami `username`, `password` i przyciskiem "Zaloguj się", używając klas Bootstrapa. Dodaj atrybuty `required` i `autofocus`.
3.  **Logika błędów w szablonie:** Dodaj blok `{% if error_message %}` do wyświetlania komunikatów o błędach.
4.  **Handler `GET /login`:** W `app/routers/auth.py` stwórz endpoint `GET /login`, który używa `Jinja2Templates` do renderowania `login.html` z domyślnym kontekstem.
5.  **Handler `POST /login`:** W tym samym pliku stwórz endpoint `POST /login`.
    a. Zdefiniuj go tak, aby przyjmował `request: Request` jako parametr.
    b. Odczytaj dane formularza z `await request.form()`.
    c. Zwaliduj, czy pola nie są puste.
    d. Wywołaj `auth_service.authenticate_user`.
    e. W bloku `try...except` obsłuż przypadek nieudanego logowania: w bloku `except` renderuj ponownie szablon z komunikatem błędu.
    f. W przypadku sukcesu, wywołaj `auth_service.create_access_token`.
    g. Utwórz `RedirectResponse` do `/dashboard`.
    h. Użyj metody `response.set_cookie()` do ustawienia tokena dostępowego w bezpiecznym ciasteczku `HttpOnly`.
    i. Zwróć obiekt `response`.
6.  **Link do rejestracji:** Upewnij się, że link "Zarejestruj się" poprawnie wskazuje na ścieżkę `/register`.
