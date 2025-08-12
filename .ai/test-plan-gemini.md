# Plan Testów Projektu: AI Flashcard Generator

## 1. Wprowadzenie i Cele Testowania

Niniejszy dokument przedstawia kompleksowy plan testów dla aplikacji "AI Flashcard Generator". Celem jest systematyczna weryfikacja jakości, funkcjonalności, bezpieczeństwa i wydajności aplikacji, aby zapewnić jej stabilne i niezawodne działanie oraz pozytywne doświadczenia użytkowników.

**Główne cele testowania:**
*   Weryfikacja pełnej zgodności aplikacji z wymaganiami funkcjonalnymi opisanymi w dokumentacji (`README.md`, `history.txt`).
*   Zapewnienie bezpieczeństwa danych użytkowników poprzez rygorystyczne testy autoryzacji i izolacji danych.
*   Potwierdzenie stabilności integracji z usługami zewnętrznymi (Supabase, Ollama) i odporności aplikacji na ich awarie.
*   Identyfikacja, dokumentacja i śledzenie defektów w celu ich eliminacji przed wdrożeniem.
*   Zapewnienie, że kluczowe przepływy użytkownika są intuicyjne i działają bezbłędnie.

## 2. Zakres Testów

### Włączone do zakresu:
*   **Testy funkcjonalne:** Pełen zakres operacji CRUD na zestawach fiszek i fiszkach, procesy rejestracji, logowania i wylogowywania.
*   **Testy logiki biznesowej:** Generowanie fiszek na podstawie tekstu, walidacja danych wejściowych (np. puste pola, duplikaty nazw).
*   **Testy integracji:** Weryfikacja poprawnej komunikacji pomiędzy backendem (FastAPI) a usługami zewnętrznymi (Supabase, Ollama) poprzez mockowanie ich odpowiedzi.
*   **Testy bezpieczeństwa:** Weryfikacja mechanizmów autoryzacji (dostęp do zasobów tylko dla ich właścicieli) i zarządzania sesją (obsługa tokenów w ciasteczkach).
*   **Testy interfejsu użytkownika (UI):** Podstawowa weryfikacja poprawności renderowania szablonów Jinja2, obsługi formularzy i działania kluczowych elementów interaktywnych (np. modal potwierdzenia usunięcia).

### Wyłączone z zakresu:
*   Szczegółowe testy wydajnościowe i obciążeniowe (np. przy użyciu Locust, JMeter).
*   Testowanie samej infrastruktury Supabase i modelu językowego Ollama.
*   Testy kompatybilności na szerokiej gamie przeglądarek i urządzeń (testy ograniczone do najnowszych wersji Chrome/Firefox).
*   Zaawansowane testy penetracyjne.

## 3. Typy Testów do Przeprowadzenia

*   **Testy Jednostkowe (Unit Tests):**
    *   **Cel:** Izolowana weryfikacja poprawności działania poszczególnych funkcji, zwłaszcza w warstwie logiki (`crud.py`) i usług (`services/ollama.py`).
    *   **Narzędzia:** `pytest`, `unittest.mock`.
*   **Testy Integracyjne (Integration Tests):**
    *   **Cel:** Sprawdzenie współpracy między komponentami aplikacji, głównie na poziomie endpointów API.
    *   **Narzędzia:** `pytest`, `FastAPI TestClient`.
*   **Testy End-to-End (E2E):**
    *   **Cel:** Weryfikacja kompletnych przepływów użytkownika w środowisku zbliżonym do produkcyjnego.
    *   **Narzędzia:** Testy manualne na środowisku stagingowym.
*   **Testy Regresji (Regression Tests):**
    *   **Cel:** Zapewnienie, że nowe zmiany nie zepsuły istniejących funkcjonalności.
    *   **Narzędzia:** Uruchomienie pełnego zestawu zautomatyzowanych testów (`pytest`).

## 4. Scenariusze Testowe dla Kluczowych Funkcjonalności

### A. Uwierzytelnianie i Zarządzanie Kontem (US-001, US-002, US-003)
*   **TC-AUTH-01 (Sukces):** Użytkownik może pomyślnie zarejestrować się z unikalnym e-mailem i hasłem, a następnie zalogować się na nowo utworzone konto.
*   **TC-AUTH-02 (Błąd):** Próba rejestracji z e-mailem, który już istnieje w bazie danych, kończy się wyświetleniem komunikatu o błędzie.
*   **TC-AUTH-03 (Błąd):** Próba logowania z nieprawidłowym hasłem lub nieistniejącym e-mailem kończy się wyświetleniem komunikatu o błędzie.
*   **TC-AUTH-04 (Sukces):** Zalogowany użytkownik może się wylogować, co kończy jego sesję i uniemożliwia dostęp do chronionych zasobów.
*   **TC-AUTH-05 (Bezpieczeństwo):** Niezalogowany użytkownik, próbując uzyskać dostęp do `/dashboard`, jest przekierowywany na stronę logowania.

### B. Generowanie i Zarządzanie Fiszkami (US-004 do US-009)
*   **TC-GEN-01 (Sukces):** Zalogowany użytkownik wkleja tekst, wybiera liczbę fiszek i klika "Generuj". Po chwili na stronie wyświetla się poprawna liczba wygenerowanych par pytanie-odpowiedź.
*   **TC-GEN-02 (Błąd):** Próba generowania fiszek z pustego pola tekstowego skutkuje wyświetleniem błędu walidacji.
*   **TC-GEN-03 (Odporność):** Aplikacja poprawnie obsługuje sytuację, w której serwis AI zwraca błąd lub niepoprawny format JSON, wyświetlając użytkownikowi stosowny komunikat.
*   **TC-CRUD-01 (Sukces):** Użytkownik może zapisać wygenerowane fiszki jako nowy zestaw, podając unikalną dla siebie nazwę. Po zapisie jest przekierowywany na pulpit, gdzie widoczny jest nowy zestaw.
*   **TC-CRUD-02 (Błąd):** Próba zapisania zestawu bez podania nazwy lub z nazwą, która już istnieje, kończy się błędem walidacji.
*   **TC-CRUD-03 (Sukces):** Użytkownik może przejrzeć szczegóły swojego zestawu, a następnie edytować treść wybranej fiszki. Zmiany są poprawnie zapisywane.
*   **TC-CRUD-04 (Sukces):** Użytkownik może usunąć cały zestaw fiszek po potwierdzeniu operacji w oknie modalnym.
*   **TC-CRUD-05 (Bezpieczeństwo):** Użytkownik nie może przeglądać, edytować ani usuwać zestawów należących do innych użytkowników (próba dostępu przez bezpośredni URL).

## 5. Środowisko Testowe

*   **Środowisko deweloperskie/testowe:** Lokalna maszyna z Python 3.13, `pytest` do uruchamiania testów. Zależności zewnętrzne (Supabase, Ollama) są mockowane.
*   **Środowisko Staging:** Dedykowana instancja aplikacji wdrożona na platformie hostingowej, połączona z deweloperską instancją Supabase i testowym endpointem Ollama. Służy do testów E2E.
*   **Przeglądarki:** Google Chrome (najnowsza wersja), Mozilla Firefox (najnowsza wersja).

## 6. Narzędzia do Testowania

*   **Framework do testów automatycznych:** `pytest`
*   **Biblioteka do mockowania:** `unittest.mock`
*   **Klient HTTP do testów API:** `FastAPI TestClient`
*   **Zarządzanie zależnościami:** `pip` z `requirements.txt`
*   **System CI/CD:** GitHub Actions (do automatycznego uruchamiania testów po każdym pushu do repozytorium).
*   **Raportowanie błędów:** GitHub Issues.

## 7. Harmonogram Testów

Testowanie jest procesem ciągłym, zintegrowanym z cyklem deweloperskim.
*   **Testy jednostkowe i integracyjne:** Pisane przez deweloperów równolegle z implementacją nowych funkcji. Uruchamiane automatycznie przy każdym commicie.
*   **Testy E2E (manualne):** Wykonywane na środowisku staging po wdrożeniu nowej, stabilnej wersji funkcjonalności.
*   **Testy regresji:** Pełen zestaw testów automatycznych uruchamiany przed każdym planowanym wdrożeniem na środowisko produkcyjne.

## 8. Kryteria Akceptacji Testów

*   **Kryterium wyjścia:** Wdrożenie może nastąpić, jeśli:
    *   100% zautomatyzowanych testów (jednostkowych i integracyjnych) przechodzi pomyślnie.
    *   Wszystkie zdefiniowane scenariusze testowe dla kluczowych funkcjonalności (E2E) zostały wykonane i zakończyły się sukcesem.
    *   Nie istnieją żadne otwarte defekty o priorytecie krytycznym lub wysokim.
    *   Pokrycie kodu testami (code coverage) dla kluczowych modułów (`crud.py`, `services/ollama.py`) wynosi co najmniej 85%.

## 9. Role i Odpowiedzialności w Procesie Testowania

*   **Inżynier QA (autor planu):** Odpowiedzialny za projektowanie, implementację i utrzymanie planu testów, tworzenie i wykonywanie scenariuszy testowych (automatycznych i manualnych), raportowanie defektów i weryfikację poprawek.
*   **Deweloperzy:** Odpowiedzialni za pisanie testów jednostkowych dla swojego kodu, naprawianie zgłoszonych defektów oraz wsparcie w analizie skomplikowanych problemów.

## 10. Procedury Raportowania Błędów

Każdy zidentyfikowany defekt zostanie zaraportowany jako "Issue" w repozytorium GitHub projektu, zgodnie z następującym szablonem:

*   **Tytuł:** Zwięzły i jasny opis problemu.
*   **Opis:**
    *   **Kroki do reprodukcji:** Szczegółowa, numerowana lista kroków potrzebnych do odtworzenia błędu.
    *   **Oczekiwany wynik:** Co powinno się wydarzyć.
    *   **Rzeczywisty wynik:** Co faktycznie się wydarzyło.
*   **Środowisko:** Wersja przeglądarki, system operacyjny, środowisko (np. Staging).
*   **Załączniki:** Zrzuty ekranu, logi, nagrania wideo.
*   **Etykiety:** Przypisanie etykiet (np. `bug`, `high-priority`, `ui`, `backend`).
*   **Przypisanie:** Przypisanie do odpowiedniego dewelopera.

Błąd pozostaje otwarty do momentu dostarczenia poprawki, która zostanie pomyślnie zweryfikowana przez QA na środowisku staging.