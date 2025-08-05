# Plan implementacji widoku Strona Generowania Fiszek

## 1. Przegląd
Widok "Strona Generowania Fiszek" jest kluczowym, wieloetapowym interfejsem aplikacji, który realizuje jej podstawową funkcjonalność. Prowadzi użytkownika przez proces transformacji surowego tekstu w gotowy do zapisu zestaw fiszek. Widok ten obsługuje stan początkowy (wprowadzanie danych), stan ładowania (oczekiwanie na AI) oraz stan prezentacji wyników połączony z możliwością ich zapisu. Implementacja musi być prosta i intuicyjna, aby sprostać potrzebom dzieci, realizując historyjki użytkownika **US-004** i **US-005**.

## 2. Routing widoku
- **Ścieżka URL:** `/generate`
- **Metody HTTP:** `GET`, `POST`
- **Plik backendu:** `app/routers/flashcards.py` (lub dedykowany router dla widoków).
- **Funkcja renderująca:** Nowa, pojedyncza funkcja w routerze, np. `handle_generate_view`, będzie obsługiwać:
    - `GET`: Wyświetlanie początkowego formularza.
    - `POST`: Obsługę dwóch różnych akcji (generowanie i zapisywanie), rozróżnianych za pomocą ukrytego pola w formularzu.

## 3. Struktura komponentów
Widok zostanie zaimplementowany jako jeden szablon Jinja2, `app/templates/generate.html`, dziedziczący z `app/templates/base.html`. Będzie on dynamicznie renderował różne sekcje w zależności od stanu przekazanego w kontekście.

```
generate.html
└── base.html
    ├── Komponent Powiadomień (np. Bootstrap Alert)
    │   (Renderowany warunkowo dla błędów walidacji lub błędów API)
    │
    ├── Formularz Generowania Fiszek
    │   (Zawsze widoczny)
    │
    ├── Nakładka Ładowania (LoadingOverlay)
    │   (Element HTML/CSS, kontrolowany przez JavaScript)
    │
    └── Sekcja Wyników
        (Renderowana warunkowo, gdy w kontekście są wygenerowane fiszki)
        ├── Lista Wygenerowanych Fiszek
        └── Formularz Zapisywania Zestawu
```

## 4. Szczegóły komponentów

### Formularz Generowania Fiszek
- **Opis komponentu:** Służy do zebrania od użytkownika tekstu źródłowego i pożądanej liczby fiszek.
- **Główne elementy:**
    - `<form id="generateForm" method="post" action="/generate">`
    - `<input type="hidden" name="action" value="generate">` (Kluczowy element do rozróżniania akcji w backendzie).
    - `<textarea name="text" required>`: Pole na tekst.
    - `<select name="count">`: Pole wyboru liczby fiszek (5, 10, 15).
    - `<button type="submit">Generuj</button>`: Przycisk wysyłający.
- **Obsługiwane interakcje:** Wysłanie formularza.
- **Obsługiwana walidacja:** Atrybut `required` na `<textarea>`.
- **Typy:** Wysyła dane formularza (`action`, `text`, `count`).
- **Propsy:** Brak.

### Nakładka Ładowania (LoadingOverlay)
- **Opis komponentu:** Wizualny wskaźnik informujący użytkownika o trwającym procesie generowania.
- **Główne elementy:**
    - `<div id="loadingOverlay" style="display: none;">`: Pełnoekranowy `div` z wyższym `z-index`.
    - Wewnątrz `div` animacja (np. spinner Bootstrapa) i przyjazny tekst "Chwileczkę, tworzymy magię!".
- **Obsługiwane interakcje:** Brak (sterowany przez JS).
- **Obsługiwana walidacja:** Brak.
- **Typy:** Brak.
- **Propsy:** Brak.

### Sekcja Wyników
- **Opis komponentu:** Kontener na wyniki z AI i formularz do ich zapisu.
- **Główne elementy:**
    - Blok warunkowy `{% if generated_flashcards %}`.
    - **Lista Wygenerowanych Fiszek:** Pętla `{% for card in generated_flashcards %}` renderująca `card.question` i `card.answer`.
    - **Formularz Zapisywania Zestawu:**
        - `<form id="saveForm" method="post" action="/generate">`
        - `<input type="hidden" name="action" value="save">`
        - `<input type="text" name="name" required>`: Pole na nazwę zestawu.
        - Pętla `{% for card in generated_flashcards %}` renderująca ukryte pola:
            - `<input type="hidden" name="questions" value="{{ card.question }}">`
            - `<input type="hidden" name="answers" value="{{ card.answer }}">`
        - `<button type="submit">Zapisz zestaw</button>`
- **Obsługiwane interakcje:** Wysłanie formularza zapisu.
- **Obsługiwana walidacja:** Atrybut `required` na polu `name`.
- **Typy:** Wymaga `ViewModel.generated_flashcards`.
- **Propsy:** Otrzymuje `generated_flashcards` z kontekstu.

## 5. Typy

### ViewModel (Kontekst Szablonu)
Słownik Pythona przekazywany z FastAPI do szablonu `generate.html`.
```python
# Konceptualna definicja słownika kontekstu
{
    "request": Request,
    "user": schemas.User,
    "error_message": Optional[str],
    "generated_flashcards": Optional[List[schemas.FlashcardCreate]]
}
```
- **`error_message`**: Komunikat o błędzie do wyświetlenia.
- **`generated_flashcards`**: Lista obiektów fiszek zwrócona przez AI.

## 6. Zarządzanie stanem
- **Stan serwera:** Stan aplikacji jest zarządzany przez backend. Każda akcja użytkownika (`POST`) powoduje ponowne renderowanie strony z nowym kontekstem lub przekierowanie.
- **Stan klienta:** Ogranicza się do wyświetlenia/ukrycia `LoadingOverlay`. Skrypt JS nasłuchuje na `submit` formularza `#generateForm`, pokazuje nakładkę, a ta znika automatycznie po otrzymaniu nowej strony z serwera.

## 7. Integracja API
Interakcja z API odbywa się wyłącznie wewnątrz handlera widoku w FastAPI.
- **Akcja "generate":** Handler `POST /generate` odbiera dane z formularza, wywołuje `POST /ai/generate-flashcards` i używa odpowiedzi do ponownego renderowania szablonu z wynikami.
- **Akcja "save":** Handler `POST /generate` odbiera dane z drugiego formularza, rekonstruuje z nich obiekt `FlashcardSetCreate` i wywołuje `POST /flashcard-sets`.

## 8. Interakcje użytkownika
1.  **Wysłanie formularza generowania:** Użytkownik klika "Generuj". Pojawia się `LoadingOverlay`.
2.  **Otrzymanie wyników:** Strona odświeża się, `LoadingOverlay` znika, a pod formularzem pojawia się lista fiszek i nowy formularz zapisu.
3.  **Wysłanie formularza zapisu:** Użytkownik wpisuje nazwę i klika "Zapisz zestaw".
4.  **Przekierowanie:** Użytkownik jest przenoszony na stronę `/dashboard`.

## 9. Warunki i walidacja
- **Pusty tekst źródłowy:** Walidowany w backendzie w handlerze `POST /generate` (dla akcji "generate"). Jeśli jest pusty, strona jest renderowana ponownie z komunikatem błędu.
- **Pusta nazwa zestawu:** Walidowana w backendzie w handlerze `POST /generate` (dla akcji "save"). Jeśli jest pusta, strona jest renderowana ponownie z komunikatem błędu, **zachowując** wygenerowane fiszki w kontekście.

## 10. Obsługa błędów
- **Błąd API (AI lub Zapis):** Handler w backendzie przechwytuje wyjątki z warstwy `crud` lub `services`. Renderuje ponownie szablon `generate.html`, przekazując w kontekście `error_message` oraz `generated_flashcards` (jeśli istnieją), aby użytkownik nie stracił wyników.
- **Błąd walidacji:** Jak opisano w punkcie 9.

## 11. Kroki implementacji
1.  **Utworzenie szablonu:** Stwórz plik `app/templates/generate.html` dziedziczący z `base.html`.
2.  **Implementacja HTML:** Dodaj oba formularze ("generate" i "save"), listę wyników oraz `LoadingOverlay`, używając bloków warunkowych Jinja2 dla sekcji wyników.
3.  **Implementacja JavaScript:** Dodaj krótki skrypt do `generate.html`, który pokazuje `#loadingOverlay` po wysłaniu formularza `#generateForm`.
4.  **Utworzenie Handlera w FastAPI:** W `app/routers/flashcards.py` stwórz jedną funkcję `handle_generate_view` obsługującą ścieżkę `/generate` dla metod `GET` i `POST`.
5.  **Logika `GET`:** Funkcja dla `GET` renderuje szablon `generate.html` z pustym kontekstem.
6.  **Logika `POST`:** Funkcja dla `POST` powinna:
    a. Odczytać dane z formularza: `form_data = await request.form()`.
    b. Sprawdzić wartość `form_data.get("action")`.
    c. **Jeśli `action == "generate"`:**
        - Zwaliduj pole `text`.
        - Wywołaj serwis AI.
        - W bloku `try...except` obsłuż błędy, renderując szablon z komunikatem.
        - W przypadku sukcesu, renderuj szablon z `generated_flashcards` w kontekście.
    d. **Jeśli `action == "save"`:**
        - Zwaliduj pole `name`.
        - Odtwórz listę fiszek z pól `questions` i `answers`.
        - Wywołaj `crud.create_flashcard_set`.
        - W bloku `try...except` obsłuż błędy (np. duplikat nazwy), renderując szablon z błędem i **zachowując fiszki w kontekście**.
        - W przypadku sukcesu, zwróć `RedirectResponse` do `/dashboard`.
7.  **Stylizacja:** Zastosuj klasy Bootstrap, aby zapewnić czytelność i estetykę interfejsu.
