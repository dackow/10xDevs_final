# Architektura UI dla Generatora Fiszek AI

## 1. Przegląd struktury UI

Architektura interfejsu użytkownika (UI) została zaprojektowana z myślą o prostocie i intuicyjności, aby sprostać potrzebom docelowej grupy użytkowników – dzieci ze szkoły podstawowej. Aplikacja składa się z dwóch głównych obszarów: publicznego (logowanie, rejestracja) i prywatnego (dostępnego po zalogowaniu).

Struktura opiera się na sześciu kluczowych widokach, które prowadzą użytkownika przez cały cykl życia fiszek: od rejestracji, przez generowanie treści za pomocą AI, aż po zarządzanie zapisanymi zestawami. Nawigacja wewnątrz aplikacji jest scentralizowana w stałym pasku nawigacyjnym, zapewniając łatwy dostęp do najważniejszych funkcji z każdego miejsca. Projekt kładzie nacisk na jasne komunikaty zwrotne, wizualne prowadzenie użytkownika i minimalizację kroków potrzebnych do osiągnięcia celu, co bezpośrednio rozwiązuje problem czasochłonnego tworzenia materiałów do nauki.

## 2. Lista widoków

### Widok 1: Strona Logowania
- **Ścieżka widoku:** `/login`
- **Główny cel:** Umożliwienie zarejestrowanym użytkownikom dostępu do aplikacji (US-002).
- **Kluczowe informacje do wyświetlenia:** Formularz z polami na nazwę użytkownika i hasło, link do strony rejestracji.
- **Kluczowe komponenty widoku:**
    - Formularz logowania (`FormInput` dla nazwy użytkownika i hasła).
    - Przycisk "Zaloguj się" (`PrimaryButton`).
    - Link nawigacyjny "Nie masz konta? Zarejestruj się".
    - Komponent do wyświetlania błędów (np. "Nieprawidłowa nazwa użytkownika lub hasło").
- **UX, dostępność i względy bezpieczeństwa:**
    - **UX:** Prosty, jednoznaczny formularz. Automatyczne ustawienie fokusu na polu "nazwa użytkownika".
    - **Dostępność:** Poprawne etykiety (`<label>`) dla pól formularza. Obsługa nawigacji klawiaturą.
    - **Bezpieczeństwo:** Komunikacja z API (`POST /token`) odbywa się przez HTTPS. Hasło przesyłane jest w ciele żądania, a nie w URL.

### Widok 2: Strona Rejestracji
- **Ścieżka widoku:** `/register`
- **Główny cel:** Umożliwienie nowym użytkownikom założenia konta (US-001).
- **Kluczowe informacje do wyświetlenia:** Formularz z polami na nazwę użytkownika i hasło, link do strony logowania.
- **Kluczowe komponenty widoku:**
    - Formularz rejestracji (`FormInput` dla nazwy użytkownika i hasła).
    - Przycisk "Zarejestruj się" (`PrimaryButton`).
    - Link nawigacyjny "Masz już konto? Zaloguj się".
    - Komponent do wyświetlania błędów (np. "Ta nazwa użytkownika jest już zajęta").
- **UX, dostępność i względy bezpieczeństwa:**
    - **UX:** Po pomyślnej rejestracji użytkownik jest informowany o sukcesie i przekierowywany na stronę logowania.
    - **Dostępność:** Poprawne etykiety dla pól. Wskazówki dotyczące wymagań dla hasła (jeśli istnieją).
    - **Bezpieczeństwo:** Komunikacja z API (`POST /users`) przez HTTPS.

### Widok 3: Panel Główny (Lista Zestawów Fiszek)
- **Ścieżka widoku:** `/dashboard` (lub `/` dla zalogowanych)
- **Główny cel:** Wyświetlenie wszystkich zapisanych zestawów użytkownika (US-006), umożliwienie usunięcia zestawu (US-009) oraz zainicjowanie tworzenia nowego.
- **Kluczowe informacje do wyświetlenia:** Lista nazw zapisanych zestawów, data utworzenia.
- **Kluczowe komponenty widoku:**
    - Przycisk "Stwórz nowy zestaw" (`PrimaryButton`).
    - Lista zestawów, gdzie każdy element zawiera nazwę (będącą linkiem do widoku szczegółów) i przycisk "Usuń" (`SecondaryButton`).
    - `NotificationBanner` do wyświetlania komunikatów (np. "Zestaw został pomyślnie zapisany").
    - `ConfirmationModal` pojawiający się po kliknięciu "Usuń".
- **UX, dostępność i względy bezpieczeństwa:**
    - **UX:** Domyślny widok po zalogowaniu. Nowo dodane zestawy pojawiają się na górze listy. Czytelne oddzielenie akcji (przejście do zestawu vs. usunięcie).
    - **Dostępność:** Lista zaimplementowana jako semantyczna lista (`<ul>`, `<li>`). Przyciski mają jasne etykiety.
    - **Bezpieczeństwo:** Widok dostępny tylko dla zalogowanych użytkowników. API (`GET /flashcard-sets`) zwraca tylko zestawy należące do uwierzytelnionego użytkownika.

### Widok 4: Strona Generowania Fiszek
- **Ścieżka widoku:** `/generate`
- **Główny cel:** Umożliwienie użytkownikowi wklejenia tekstu i wygenerowania fiszek przez AI (US-004), a następnie zapisanie ich jako nowy zestaw (US-005).
- **Kluczowe informacje do wyświetlenia:**
    - **Stan początkowy:** Pole tekstowe, opcje wyboru liczby fiszek.
    - **Stan ładowania:** Animacja z przyjaznym komunikatem.
    - **Stan po wygenerowaniu:** Lista par pytanie-odpowiedź, formularz do nazwania i zapisania zestawu.
- **Kluczowe komponenty widoku:**
    - Duże pole tekstowe (`<textarea>`).
    - Grupa przycisków lub pole wyboru dla liczby fiszek ("mało", "średnio", "dużo").
    - Przycisk "Generuj" (`PrimaryButton`).
    - `LoadingOverlay` do komunikacji stanu ładowania.
    - `FlashcardList` do wyświetlenia wyników.
    - Formularz zapisu (`FormInput` na nazwę, `PrimaryButton` "Zapisz zestaw").
- **UX, dostępność i względy bezpieczeństwa:**
    - **UX:** Płynne przejście między stanami (formularz -> ładowanie -> wyniki z opcją zapisu) na jednej stronie. Jasna informacja zwrotna na każdym etapie.
    - **Dostępność:** Wszystkie elementy formularza mają etykiety. Stan ładowania jest komunikowany nie tylko wizualnie, ale i tekstowo.
    - **Bezpieczeństwo:** Endpoint (`POST /ai/generate-flashcards`) jest chroniony i wymaga uwierzytelnienia.

### Widok 5: Widok Szczegółów Zestawu Fiszek
- **Ścieżka widoku:** `/sets/{set_id}`
- **Główny cel:** Przeglądanie zawartości konkretnego zestawu fiszek (US-007) i inicjowanie edycji pojedynczej fiszki (US-008).
- **Kluczowe informacje do wyświetlenia:** Nazwa zestawu, lista wszystkich par pytanie-odpowiedź w zestawie.
- **Kluczowe komponenty widoku:**
    - Nagłówek z nazwą zestawu.
    - `FlashcardList`, gdzie każda fiszka ma dodatkowo przycisk "Edytuj" (`SecondaryButton`).
- **UX, dostępność i względy bezpieczeństwa:**
    - **UX:** Czytelna prezentacja pytań i odpowiedzi. Łatwy dostęp do funkcji edycji.
    - **Dostępność:** Struktura fiszek oparta na semantycznych tagach.
    - **Bezpieczeństwo:** API (`GET /flashcard-sets/{set_id}`) sprawdza, czy zalogowany użytkownik jest właścicielem zestawu, zapobiegając dostępowi do cudzych danych.

### Widok 6: Strona Edycji Fiszki
- **Ścieżka widoku:** `/cards/{card_id}/edit`
- **Główny cel:** Umożliwienie użytkownikowi poprawienia treści pytania lub odpowiedzi w istniejącej fiszce (US-008).
- **Kluczowe informacje do wyświetlenia:** Formularz z istniejącą treścią pytania i odpowiedzi.
- **Kluczowe komponenty widoku:**
    - Formularz z dwoma polami tekstowymi (`FormInput` lub `<textarea>`) na pytanie i odpowiedź, wstępnie wypełnionymi danymi.
    - Przycisk "Zapisz zmiany" (`PrimaryButton`).
- **UX, dostępność i względy bezpieczeństwa:**
    - **UX:** Dedykowany, skupiony widok do edycji. Po zapisaniu użytkownik jest automatycznie przekierowywany z powrotem do widoku szczegółów zestawu.
    - **Dostępność:** Pola formularza mają etykiety.
    - **Bezpieczeństwo:** API (`PUT /flashcards/{card_id}`) weryfikuje własność fiszki przed dokonaniem aktualizacji.

## 3. Mapa podróży użytkownika

**Główny przepływ: Tworzenie i zapisywanie nowego zestawu fiszek**

1.  **Logowanie:** Użytkownik wchodzi na `/login`, podaje dane i klika "Zaloguj się". Po pomyślnej autoryzacji (`POST /token`) zostaje przekierowany na `/dashboard`.
2.  **Inicjacja tworzenia:** Na `/dashboard` użytkownik klika przycisk "Stwórz nowy zestaw".
3.  **Przejście do generatora:** Użytkownik ląduje na stronie `/generate`.
4.  **Generowanie fiszek:** Użytkownik wkleja tekst, wybiera liczbę fiszek i klika "Generuj".
5.  **Oczekiwanie na AI:** Interfejs wyświetla animację ładowania, podczas gdy w tle wysyłane jest żądanie do `POST /ai/generate-flashcards`.
6.  **Przeglądanie i zapis:** Po otrzymaniu odpowiedzi, na tej samej stronie (`/generate`) wyświetlana jest lista wygenerowanych fiszek oraz formularz do ich zapisania. Użytkownik wpisuje nazwę zestawu i klika "Zapisz zestaw".
7.  **Zapis w systemie:** Aplikacja wysyła żądanie do `POST /flashcard-sets`.
8.  **Powrót i potwierdzenie:** Po pomyślnym zapisie użytkownik jest przekierowywany z powrotem na `/dashboard`, gdzie na górze ekranu widzi komunikat o sukcesie, a nowo utworzony zestaw jest widoczny na liście.

## 4. Układ i struktura nawigacji

Nawigacja dla zalogowanego użytkownika opiera się na stałym, poziomym pasku nawigacyjnym umieszczonym na górze każdej strony.

-   **Kompozycja paska nawigacyjnego:**
    -   **Po lewej:** Logo aplikacji (działające jako link do `/dashboard`).
    -   **W centrum:** Główne linki nawigacyjne:
        -   **"Moje zestawy"**: Link do `/dashboard` (lista wszystkich zestawów).
        -   **"Stwórz nowy"**: Link do `/generate` (strona generowania fiszek).
    -   **Po prawej:**
        -   **"Wyloguj"**: Przycisk kończący sesję i przekierowujący na `/login` (US-003).

Taki układ zapewnia spójność i stały, łatwy dostęp do kluczowych funkcji aplikacji z dowolnego miejsca, co jest szczególnie ważne dla młodszych użytkowników.

## 5. Kluczowe komponenty

-   **`MainLayout`**: Główny szablon strony dla zalogowanych użytkowników, zawierający stały pasek nawigacyjny i obszar na treść konkretnego widoku.
-   **`FormInput`**: Standardowy komponent pola tekstowego z etykietą i miejscem na komunikat o błędzie walidacji.
-   **`PrimaryButton`**: Duży, wyraźny przycisk dla głównych akcji (np. "Zaloguj", "Generuj", "Zapisz").
-   **`SecondaryButton`**: Mniejszy, mniej wyróżniający się przycisk dla akcji drugorzędnych (np. "Edytuj", "Usuń").
-   **`FlashcardList`**: Komponent renderujący listę fiszek (pytanie i odpowiedź). Używany w widoku szczegółów zestawu oraz na stronie generowania po otrzymaniu wyników z AI.
-   **`NotificationBanner`**: Pasek na górze strony do wyświetlania tymczasowych komunikatów o sukcesie lub błędzie (np. "Zestaw usunięty pomyślnie").
-   **`ConfirmationModal`**: Okno dialogowe wymagające od użytkownika potwierdzenia operacji destrukcyjnej, takiej jak usunięcie całego zestawu fiszek.
-   **`LoadingOverlay`**: Pełnoekranowa nakładka z przyjazną animacją i tekstem, używana do informowania o procesach w tle (głównie podczas generowania fiszek przez AI).
```