# Plan implementacji widoku Panel Główny (Lista Zestawów Fiszek)

## 1. Przegląd
Panel Główny jest centralnym widokiem aplikacji dla zalogowanego użytkownika. Służy jako osobiste centrum zarządzania, gdzie użytkownik może zobaczyć wszystkie swoje zapisane zestawy fiszek, przejść do ich szczegółów, usunąć te niepotrzebne oraz zainicjować proces tworzenia nowego zestawu. Widok ten realizuje kluczowe historyjki użytkownika **US-006** (przeglądanie listy) i **US-009** (usuwanie zestawu).

## 2. Routing widoku
- **Ścieżka URL:** `/dashboard` (oraz `/` jako domyślna dla zalogowanych użytkowników).
- **Metody HTTP:** `GET` (do wyświetlania strony), `POST` (do obsługi usuwania, jako obejście dla formularzy HTML).
- **Plik backendu:** `app/routers/flashcards.py` (lub dedykowany router dla widoków).
- **Funkcja renderująca:** Nowa funkcja, np. `dashboard_view`, będzie obsługiwać żądania `GET` (pobieranie i wyświetlanie zestawów) oraz `POST` (obsługa żądania usunięcia zestawu).

## 3. Struktura komponentów
Widok zostanie zaimplementowany w szablonie `app/templates/dashboard.html`, dziedziczącym z `app/templates/base.html`.

```
dashboard.html
└── base.html
    ├── Komponent Powiadomień (np. Bootstrap Alert)
    │   (Renderowany warunkowo dla komunikatów flash, np. po usunięciu zestawu)
    │
    ├── Nagłówek i Przycisk Akcji
    │   ├── Powitanie użytkownika
    │   └── Przycisk "Stwórz nowy zestaw"
    │
    └── Lista Zestawów Fiszek
        ├── (Stan pusty) Komunikat "Nie masz jeszcze żadnych zestawów."
        └── (Stan z danymi) Lista <ul> zawierająca elementy <li> dla każdego zestawu
            ├── Nazwa zestawu (link do szczegółów)
            └── Przycisk "Usuń"
    
└── (Poza główną treścią) Modal Potwierdzenia Usunięcia
    (Ukryty, kontrolowany przez JavaScript)
```

## 4. Szczegóły komponentów

### Przycisk "Stwórz nowy zestaw"
- **Opis komponentu:** Wyraźnie widoczny przycisk, który stanowi główne wezwanie do działania na tej stronie.
- **Główne elementy:** `<a href="/generate" class="btn btn-primary">Stwórz nowy zestaw</a>`.
- **Obsługiwane interakcje:** Kliknięcie.
- **Obsługiwana walidacja:** Brak.
- **Typy:** Brak.
- **Propsy:** Brak.

### Lista Zestawów Fiszek
- **Opis komponentu:** Dynamicznie generowana lista, która wyświetla wszystkie zestawy należące do użytkownika.
- **Główne elementy:**
    - Blok warunkowy `{% if sets %}`.
    - Lista `<ul>` ze stylizacją Bootstrap (np. `list-group`).
    - Wewnątrz pętli `{% for set in sets %}`:
        - Element `<li>` (np. `list-group-item`).
        - Link do szczegółów: `<a href="/sets/{{ set.id }}">{{ set.name }}</a>`.
        - Przycisk usuwania: `<button type="button" class="btn btn-danger btn-sm float-right" data-toggle="modal" data-target="#deleteConfirmationModal" data-set-id="{{ set.id }}" data-set-name="{{ set.name }}">Usuń</button>`.
    - Blok `{% else %}` z komunikatem o braku zestawów.
- **Obsługiwane interakcje:** Kliknięcie na nazwę zestawu (nawigacja), kliknięcie przycisku "Usuń" (otwarcie modala).
- **Obsługiwana walidacja:** Brak.
- **Typy:** Wymaga `ViewModel.sets`.
- **Propsy:** Otrzymuje listę `sets` z kontekstu szablonu.

### Modal Potwierdzenia Usunięcia
- **Opis komponentu:** Okno dialogowe (Bootstrap Modal) zapobiegające przypadkowemu usunięciu zestawu.
- **Główne elementy:**
    - `<div class="modal" id="deleteConfirmationModal">...</div>`.
    - Nagłówek modala: "Potwierdzenie usunięcia".
    - Treść modala: "Czy na pewno chcesz usunąć zestaw <strong id="modalSetName"></strong>?".
    - Stopka modala:
        - Przycisk zamknięcia: `<button type="button" class="btn btn-secondary" data-dismiss="modal">Anuluj</button>`.
        - Formularz usuwania: `<form id="deleteForm" method="post" action=""> <button type="submit" class="btn btn-danger">Usuń</button> </form>`.
- **Obsługiwane interakcje:** Potwierdzenie lub anulowanie usunięcia.
- **Obsługiwana walidacja:** Brak.
- **Typy:** Brak.
- **Propsy:** Brak (stan zarządzany przez JS).

## 5. Typy

### ViewModel (Kontekst Szablonu)
Słownik Pythona przekazywany z FastAPI do szablonu `dashboard.html`.
```python
# Konceptualna definicja słownika kontekstu
{
    "request": Request,
    "user": schemas.User,
    "sets": List[schemas.FlashcardSet],
    "notification": Optional[str] # Np. "Zestaw został usunięty."
}
```
- **`sets`**: Lista obiektów zestawów fiszek do wyświetlenia. Każdy obiekt zawiera co najmniej `id` i `name`.
- **`notification`**: Opcjonalny komunikat do wyświetlenia w banerze.

## 6. Zarządzanie stanem
- **Stan serwera:** Główny stan (lista zestawów) jest pobierany z bazy danych przy każdym żądaniu `GET` do `/dashboard`.
- **Stan klienta:** Minimalny, ograniczony do obsługi modala. JavaScript będzie odpowiedzialny za:
    - Odczytanie `data-set-id` i `data-set-name` z klikniętego przycisku "Usuń".
    - Wstawienie nazwy zestawu do treści modala.
    - Dynamiczne ustawienie atrybutu `action` formularza w modalu na `/sets/{set_id}/delete`.

## 7. Integracja API
- **Pobieranie danych (`GET /dashboard`):**
    - Handler w FastAPI wywołuje `crud.get_flashcard_sets(db=db, user_id=current_user.id)`.
    - Zwrócona lista `FlashcardSet` jest przekazywana do szablonu w kontekście.
- **Usuwanie danych (`POST /sets/{set_id}/delete`):**
    - Handler w FastAPI dla tej ścieżki wywołuje `crud.delete_flashcard_set(db=db, set_id=set_id, user_id=current_user.id)`.
    - Po pomyślnym usunięciu, zwraca `RedirectResponse` z powrotem do `/dashboard`, potencjalnie z komunikatem o sukcesie (np. przez mechanizm flash).

## 8. Interakcje użytkownika
- **Kliknięcie "Stwórz nowy zestaw":** Przekierowuje użytkownika na `/generate`.
- **Kliknięcie nazwy zestawu:** Przekierowuje użytkownika na `/sets/{id_zestawu}`.
- **Kliknięcie "Usuń":**
    1. JavaScript przechwytuje kliknięcie.
    2. Odczytuje ID i nazwę zestawu z atrybutów `data-*`.
    3. Aktualizuje treść i `action` formularza w modalu.
    4. Wyświetla modal.
- **Kliknięcie "Usuń" w modalu:** Formularz jest wysyłany metodą `POST`. Strona przeładowuje się (po przekierowaniu z backendu), a usunięty zestaw znika z listy.
- **Kliknięcie "Anuluj" w modalu:** Modal zostaje zamknięty bez żadnej akcji.

## 9. Warunki i walidacja
- **Brak zestawów:** Szablon sprawdza `{% if sets %}`. Jeśli lista jest pusta, wyświetla stosowny komunikat.
- **Autoryzacja:** Cała logika autoryzacji (sprawdzanie, czy użytkownik może zobaczyć/usunąć dany zasób) jest obsługiwana po stronie backendu w warstwie `crud`. Frontend zakłada, że otrzymane dane są poprawne dla zalogowanego użytkownika.

## 10. Obsługa błędów
- **Błąd pobierania danych:** Jeśli `crud.get_flashcard_sets` zwróci błąd, handler `/dashboard` powinien go obsłużyć i wyświetlić stronę błędu lub komunikat w panelu.
- **Błąd usuwania:** Jeśli `crud.delete_flashcard_set` zwróci błąd (np. zestaw nie istnieje), handler usuwania powinien przekierować z powrotem do `/dashboard` z komunikatem o błędzie wyświetlonym w `NotificationBanner`.

## 11. Kroki implementacji
1.  **Backend (Handler widoku):** W `app/routers/flashcards.py` stwórz endpoint `GET /dashboard`.
    a. Wymaga uwierzytelnionego użytkownika (`Depends(get_current_user)`).
    b. Wywołuje `crud.get_flashcard_sets`, aby pobrać zestawy dla `current_user.id`.
    c. Renderuje szablon `dashboard.html`, przekazując `request`, `user` i `sets` w kontekście.
2.  **Backend (Handler usuwania):** W tym samym routerze stwórz endpoint `POST /sets/{set_id}/delete`.
    a. Wymaga uwierzytelnionego użytkownika.
    b. Wywołuje `crud.delete_flashcard_set` z `set_id` i `current_user.id`.
    c. W przypadku sukcesu, zwraca `RedirectResponse` do `/dashboard`.
    d. Obsługuje błędy (np. gdy zestaw nie istnieje).
3.  **Szablon HTML:** Stwórz plik `app/templates/dashboard.html`.
    a. Dodaj powitanie i przycisk "Stwórz nowy zestaw".
    b. Zaimplementuj pętlę `{% for set in sets %}` do wyświetlania listy.
    c. W pętli dodaj link do szczegółów i przycisk "Usuń" z atrybutami `data-*`.
    d. Dodaj blok `{% else %}` dla przypadku braku zestawów.
4.  **Modal HTML:** W pliku `dashboard.html` dodaj kod HTML dla modala Bootstrapa (`deleteConfirmationModal`).
5.  **JavaScript:** W bloku `<script>` w `dashboard.html` (lub w osobnym pliku JS):
    a. Dodaj listener zdarzeń dla `show.bs.modal` na `#deleteConfirmationModal`.
    b. W listenerze odczytaj `event.relatedTarget` (przycisk, który otworzył modal).
    c. Pobierz `dataset.setId` i `dataset.setName` z przycisku.
    d. Zaktualizuj treść modala i atrybut `action` formularza wewnątrz modala.
