# Plan implementacji widoku Strona Edycji Fiszki

## 1. Przegląd
Widok "Strona Edycji Fiszki" to dedykowany interfejs, który pozwala użytkownikowi na modyfikację treści pojedynczej, istniejącej fiszki. Jego głównym celem jest dostarczenie prostego formularza, wstępnie wypełnionego aktualnymi danymi (pytaniem i odpowiedzią), oraz umożliwienie zapisu zmian. Po pomyślnej aktualizacji, użytkownik jest automatycznie przekierowywany z powrotem do widoku szczegółów zestawu, z którego przyszedł. Widok ten realizuje kryteria akceptacji dla historyjki użytkownika **US-008**.

## 2. Routing widoku
- **Ścieżka URL:** `/cards/{card_id}/edit`
- **Metody HTTP:** `GET`, `POST`
- **Plik backendu:** `app/routers/flashcards.py` (lub dedykowany router dla widoków).
- **Funkcja renderująca:** Nowa funkcja w routerze, np. `edit_flashcard_view`, będzie obsługiwać:
    - `GET`: Pobranie danych fiszki i wyświetlenie formularza edycji.
    - `POST`: Przetworzenie danych z formularza i zaktualizowanie fiszki w bazie danych.

## 3. Struktura komponentów
Widok zostanie zaimplementowany w nowym pliku szablonu `app/templates/edit_flashcard.html`, który będzie dziedziczył z `app/templates/base.html`.

```
edit_flashcard.html
└── base.html
    ├── Komponent Powiadomień (np. Bootstrap Alert)
    │   (Renderowany warunkowo dla błędów walidacji)
    │
    ├── Nagłówek "Edytuj Fiszkę"
    │
    └── Formularz Edycji Fiszki
        ├── Pole tekstowe na pytanie
        ├── Pole tekstowe na odpowiedź
        ├── Przycisk "Zapisz zmiany"
        └── Link "Anuluj"
```

## 4. Szczegóły komponentów

### Formularz Edycji Fiszki
- **Opis komponentu:** Główny i jedyny komponent interaktywny na stronie, służący do modyfikacji danych fiszki.
- **Główne elementy:**
    - `<form method="post" action="/cards/{{ flashcard.id }}/edit">`: Formularz wysyłający dane na ten sam URL.
    - `<div class="form-group">`: Kontener dla pola "Pytanie".
        - `<label for="question">Pytanie</label>`
        - `<textarea id="question" name="question" class="form-control" required>{{ flashcard.question }}</textarea>`: Pole na pytanie, wstępnie wypełnione danymi.
    - `<div class="form-group">`: Kontener dla pola "Odpowiedź".
        - `<label for="answer">Odpowiedź</label>`
        - `<textarea id="answer" name="answer" class="form-control" required>{{ flashcard.answer }}</textarea>`: Pole na odpowiedź, wstępnie wypełnione danymi.
    - `<button type="submit" class="btn btn-primary">Zapisz zmiany</button>`: Przycisk zapisu.
    - `<a href="/sets/{{ flashcard.set_id }}" class="btn btn-secondary">Anuluj</a>`: Link powrotny do widoku zestawu.
- **Obsługiwane interakcje:** Wysłanie formularza (submit), kliknięcie linku "Anuluj" (nawigacja).
- **Obsługiwana walidacja:** Atrybuty `required` na polach `<textarea>`.
- **Typy:** Wysyła dane formularza (`question`, `answer`).
- **Propsy:** Otrzymuje obiekt `flashcard` z kontekstu szablonu.

## 5. Typy

### ViewModel (Kontekst Szablonu)
Słownik Pythona przekazywany z handlera FastAPI do szablonu `edit_flashcard.html`.
```python
# Konceptualna definicja słownika kontekstu
{
    "request": Request,
    "user": schemas.User,
    "flashcard": schemas.Flashcard,
    "error_message": Optional[str]
}
```
- **`flashcard`**: Obiekt fiszki, której dane (`id`, `question`, `answer`, `set_id`) są używane do wypełnienia formularza i zbudowania linku powrotnego.
- **`error_message`**: Opcjonalny komunikat o błędzie walidacji.

## 6. Zarządzanie stanem
Stan jest w całości zarządzany po stronie serwera.
- **Stan początkowy:** Żądanie `GET` pobiera dane fiszki i renderuje formularz wypełniony tymi danymi.
- **Stan błędu:** Nieudane żądanie `POST` (np. puste pola) ponownie renderuje ten sam formularz, przekazując komunikat o błędzie i zachowując wprowadzone przez użytkownika dane.
- **Stan sukcesu:** Pomyślne żądanie `POST` nie renderuje widoku, lecz wykonuje przekierowanie na stronę szczegółów zestawu (`/sets/{set_id}`).

## 7. Integracja API
Interakcja z API odbywa się wewnątrz handlera widoku w FastAPI.
1.  **Handler `GET`:**
    - Musi pobrać dane fiszki, weryfikując jednocześnie jej własność. W tym celu potrzebna będzie nowa funkcja w `crud.py`, np. `get_flashcard_for_editing(db, card_id, user_id)`, która pobierze fiszkę tylko jeśli należy do zestawu danego użytkownika.
    - Jeśli fiszka zostanie znaleziona, renderuje szablon, przekazując ją w kontekście.
2.  **Handler `POST`:**
    - Odbiera dane z formularza.
    - Tworzy obiekt `schemas.FlashcardUpdate`.
    - Wywołuje istniejącą funkcję `crud.update_flashcard`, która realizuje logikę endpointu `PUT /flashcards/{card_id}`. Ta funkcja już zawiera logikę weryfikacji własności.
    - Po pomyślnym zapisie, odczytuje `set_id` ze zwróconego, zaktualizowanego obiektu fiszki i wykonuje przekierowanie.

## 8. Interakcje użytkownika
- **Modyfikacja danych:** Użytkownik zmienia tekst w polach "Pytanie" i/lub "Odpowiedź".
- **Zapis zmian:** Użytkownik klika "Zapisz zmiany". Przeglądarka wysyła dane i zostaje przekierowana na stronę szczegółów zestawu, gdzie widoczna jest zaktualizowana treść fiszki.
- **Anulowanie:** Użytkownik klika "Anuluj", co natychmiast przerywa edycję i przenosi go z powrotem na stronę szczegółów zestawu bez zapisywania zmian.

## 9. Warunki i walidacja
- **Własność fiszki:** Kluczowa walidacja bezpieczeństwa. Musi być wykonana zarówno przy `GET` (aby nie wyświetlić formularza edycji cudzej fiszki), jak i przy `POST` (aby nie zapisać zmian w cudzej fiszce). W obu przypadkach brak uprawnień powinien skutkować błędem 404.
- **Puste pola:** Handler `POST` musi sprawdzić, czy pola `question` i `answer` nie są puste po stronie serwera. Jeśli są, powinien ponownie wyrenderować formularz z komunikatem błędu.

## 10. Obsługa błędów
- **Fiszka nie istnieje / Brak uprawnień:** Handler `GET` i `POST` po wywołaniu odpowiednich funkcji `crud` powinien obsłużyć przypadek, gdy fiszka nie zostanie znaleziona (lub użytkownik nie ma do niej dostępu), zgłaszając `HTTPException(status_code=404)`.
- **Błąd walidacji:** Handler `POST` w przypadku pustych pól renderuje ponownie szablon `edit_flashcard.html`, przekazując w kontekście `error_message` oraz dane fiszki, aby formularz pozostał wypełniony.

## 11. Kroki implementacji
1.  **Utworzenie szablonu:** Stwórz plik `app/templates/edit_flashcard.html` dziedziczący z `base.html`.
2.  **Implementacja HTML:** W szablonie zaimplementuj formularz z polami `<textarea>` dla pytania i odpowiedzi. Użyj Jinja2 (`{{ flashcard.question }}`) do wstępnego wypełnienia pól. Dodaj przycisk zapisu i link anulowania.
3.  **Nowa funkcja CRUD:** W `app/crud/crud.py` dodaj funkcję `get_flashcard_for_editing(db: Session, card_id: int, user_id: int)`. Powinna ona pobrać fiszkę, wykonując `join` do tabeli `flashcard_sets` i filtrując po `user_id`.
4.  **Utworzenie Handlera w FastAPI:** W `app/routers/flashcards.py` stwórz nową funkcję `edit_flashcard_view` obsługującą ścieżkę `GET` i `POST` dla `/cards/{card_id}/edit`.
5.  **Logika `GET`:**
    a. Wywołaj nową funkcję `crud.get_flashcard_for_editing`.
    b. Jeśli zwróci `None`, zgłoś `HTTPException(404)`.
    c. Jeśli zwróci fiszkę, renderuj szablon `edit_flashcard.html`, przekazując ją w kontekście.
6.  **Logika `POST`:**
    a. Odczytaj dane z `await request.form()`.
    b. Zwaliduj, czy pola nie są puste. Jeśli tak, ponownie renderuj szablon z błędem.
    c. Wywołaj istniejącą funkcję `crud.update_flashcard`.
    d. W bloku `try...except` obsłuż ewentualne błędy z `crud`.
    e. Po sukcesie, użyj `updated_flashcard.set_id` do zbudowania URL i zwróć `RedirectResponse`.
7.  **Stylizacja:** Użyj klas Bootstrap, aby formularz był czytelny i spójny z resztą aplikacji.
