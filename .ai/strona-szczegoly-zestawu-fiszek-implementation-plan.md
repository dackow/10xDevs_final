# Plan implementacji widoku Widok Szczegółów Zestawu Fiszek

## 1. Przegląd
Widok "Szczegółów Zestawu Fiszek" stanowi dedykowaną przestrzeń do przeglądania zawartości pojedynczego, zapisanego zestawu. Jego głównym celem jest czytelne zaprezentowanie wszystkich par pytanie-odpowiedź wchodzących w skład zestawu oraz zapewnienie intuicyjnego punktu wejścia do edycji każdej fiszki. Widok ten jest bezpośrednią realizacją historyjek użytkownika **US-007** (przeglądanie zawartości) i **US-008** (inicjowanie edycji).

## 2. Routing widoku
- **Ścieżka URL:** `/sets/{set_id}`
- **Metody HTTP:** `GET`
- **Plik backendu:** `app/routers/flashcards.py` (lub dedykowany router dla widoków).
- **Funkcja renderująca:** Nowa funkcja w routerze, np. `set_detail_view`, będzie obsługiwać żądania `GET`. Będzie przyjmować `set_id` jako parametr ścieżki.

## 3. Struktura komponentów
Widok zostanie zaimplementowany w nowym pliku szablonu `app/templates/set_detail.html`, który będzie dziedziczył z `app/templates/base.html`.

```
set_detail.html
└── base.html
    ├── Przycisk nawigacyjny "Wróć do panelu"
    │
    ├── Nagłówek z nazwą zestawu
    │
    └── Lista Fiszek
        ├── (Stan pusty) Komunikat "Ten zestaw nie zawiera żadnych fiszek."
        └── (Stan z danymi) Lista <ul> zawierająca elementy <li> dla każdej fiszki
            ├── Treść pytania
            ├── Treść odpowiedzi
            └── Przycisk "Edytuj"
```

## 4. Szczegóły komponentów

### Nagłówek Zestawu
- **Opis komponentu:** Wyświetla nazwę przeglądanego zestawu jako główny tytuł strony.
- **Główne elementy:** `<h1>{{ set.name }}</h1>`.
- **Obsługiwane interakcje:** Brak.
- **Obsługiwana walidacja:** Brak.
- **Typy:** Wymaga `ViewModel.set.name`.
- **Propsy:** Otrzymuje obiekt `set` z kontekstu szablonu.

### Lista Fiszek
- **Opis komponentu:** Główny komponent widoku, odpowiedzialny za renderowanie zawartości zestawu.
- **Główne elementy:**
    - Blok warunkowy `{% if set.flashcards %}`.
    - Lista `<ul>` (np. ze stylizacją `list-group` z Bootstrapa).
    - Wewnątrz pętli `{% for card in set.flashcards %}`:
        - Element `<li>` (np. `list-group-item`).
        - Treść pytania: `<strong>Pytanie:</strong> {{ card.question }}`.
        - Treść odpowiedzi: `<strong>Odpowiedź:</strong> {{ card.answer }}`.
        - Przycisk edycji: `<a href="/cards/{{ card.id }}/edit" class="btn btn-secondary btn-sm">Edytuj</a>`.
    - Blok `{% else %}` z komunikatem o braku fiszek w zestawie.
- **Obsługiwane interakcje:** Kliknięcie przycisku "Edytuj".
- **Obsługiwana walidacja:** Brak.
- **Typy:** Wymaga `ViewModel.set.flashcards`.
- **Propsy:** Otrzymuje obiekt `set` z kontekstu szablonu.

## 5. Typy

### ViewModel (Kontekst Szablonu)
Słownik Pythona przekazywany z handlera FastAPI do szablonu `set_detail.html`.
```python
# Konceptualna definicja słownika kontekstu
{
    "request": Request,
    "user": schemas.User,
    "set": schemas.FlashcardSetDetail
}
```
- **`set`**: Kluczowy obiekt typu `FlashcardSetDetail`, który zawiera wszystkie informacje o zestawie, w tym jego nazwę (`name`) oraz zagnieżdżoną listę fiszek (`flashcards`).

## 6. Zarządzanie stanem
Stan jest w całości zarządzany po stronie serwera. Widok jest bezstanowy po stronie klienta. Każde żądanie `GET` do `/sets/{set_id}` powoduje pobranie aktualnych danych z bazy i wyrenderowanie strony.

## 7. Integracja API
Interakcja z API odbywa się wewnątrz handlera widoku w FastAPI.
1.  Handler `GET /sets/{set_id}` w `app/routers/flashcards.py` jest punktem wejścia.
2.  Wewnątrz handlera następuje wywołanie funkcji `crud.get_flashcard_set(db=db, set_id=set_id, user_id=current_user.id)`. Ta funkcja realizuje logikę endpointu `GET /flashcard-sets/{set_id}`.
3.  Jeśli funkcja `crud` zwróci obiekt `FlashcardSet`, jest on przekazywany do szablonu `set_detail.html` jako `set` w słowniku kontekstu.
4.  Jeśli funkcja `crud` zwróci `None`, handler zgłasza `HTTPException` o statusie 404.

## 8. Interakcje użytkownika
- **Przeglądanie:** Użytkownik przewija stronę, aby zobaczyć wszystkie fiszki w zestawie.
- **Inicjowanie edycji:** Użytkownik klika przycisk "Edytuj" przy wybranej fiszce, co powoduje natychmiastowe przejście przeglądarki na stronę edycji tej konkretnej fiszki (`/cards/{card_id}/edit`).
- **Powrót:** Użytkownik klika przycisk "Wróć do panelu", co przenosi go na stronę `/dashboard`.

## 9. Warunki i walidacja
- **Własność zestawu:** Najważniejsza walidacja odbywa się w backendzie. Funkcja `crud.get_flashcard_set` musi filtrować wyniki nie tylko po `set_id`, ale również po `user_id` pochodzącym z tokena zalogowanego użytkownika. To gwarantuje, że użytkownik nie zobaczy danych, które do niego nie należą. Próba dostępu do cudzego zestawu poskutkuje błędem 404.
- **Pusty zestaw:** Szablon sprawdza, czy lista `set.flashcards` jest pusta i wyświetla odpowiedni komunikat, jeśli tak jest.

## 10. Obsługa błędów
- **Zestaw nie istnieje lub brak uprawnień:** Jeśli `crud.get_flashcard_set` zwróci `None`, handler widoku musi zgłosić `HTTPException(status_code=404, detail="Flashcard set not found")`. Użytkownik zobaczy standardową stronę błędu 404.
- **Błąd serwera:** W przypadku nieoczekiwanego błędu podczas pobierania danych z bazy, użytkownik powinien zobaczyć stronę błędu 500.

## 11. Kroki implementacji
1.  **Utworzenie szablonu:** Stwórz nowy plik `app/templates/set_detail.html`, który dziedziczy z `base.html`.
2.  **Implementacja HTML:** W szablonie dodaj nagłówek `<h1>{{ set.name }}</h1>` oraz przycisk powrotu do panelu.
3.  **Implementacja listy:** Dodaj blok warunkowy `{% if set.flashcards %}`. Wewnątrz zaimplementuj pętlę `{% for card in set.flashcards %}` renderującą pytanie, odpowiedź oraz link "Edytuj" z dynamicznie generowanym `href="/cards/{{ card.id }}/edit"`. Dodaj blok `{% else %}`.
4.  **Utworzenie Handlera w FastAPI:** W `app/routers/flashcards.py` stwórz nową funkcję `set_detail_view` obsługującą ścieżkę `GET /sets/{set_id}`.
5.  **Logika Handlera:**
    a. Funkcja musi przyjmować `set_id: int` z parametru ścieżki oraz zależeć od `db: Session` i `current_user: models.User`.
    b. Wywołaj `db_set = crud.get_flashcard_set(db=db, set_id=set_id, user_id=current_user.id)`.
    c. Sprawdź `if db_set is None:` i jeśli tak, zgłoś `HTTPException(status_code=404)`.
    d. Jeśli zestaw istnieje, zwróć `templates.TemplateResponse("set_detail.html", {"request": request, "user": current_user, "set": db_set})`.
6.  **Stylizacja:** Użyj klas Bootstrap (np. `list-group`, `list-group-item`, `d-flex`, `justify-content-between`, `align-items-center`) aby lista była czytelna i estetyczna.
