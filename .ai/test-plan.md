## Plan Testów Projektu "10xDevs_final"

### 1. Wprowadzenie i Cele Testowania

Niniejszy dokument przedstawia kompleksowy plan testów dla aplikacji "10xDevs_final", systemu do zarządzania fiszkami z funkcjonalnością generowania ich za pomocą AI. Głównym celem testowania jest zapewnienie wysokiej jakości oprogramowania, jego stabilności, bezpieczeństwa oraz zgodności z wymaganiami funkcjonalnymi i niefunkcjonalnymi.

**Główne cele testowania:**
*   Weryfikacja poprawności działania wszystkich funkcjonalności aplikacji.
*   Zapewnienie bezpieczeństwa danych użytkowników i ich prywatności.
*   Potwierdzenie stabilności i wydajności aplikacji pod obciążeniem.
*   Identyfikacja i raportowanie defektów w celu ich usunięcia.
*   Zapewnienie pozytywnego doświadczenia użytkownika (UX).

### 2. Zakres Testów

Zakres testów obejmuje wszystkie komponenty aplikacji, od interfejsu użytkownika, przez logikę biznesową, po integrację z zewnętrznymi usługami.

**Włączone do zakresu:**
*   **Moduł Uwierzytelniania i Autoryzacji:** Rejestracja, logowanie, wylogowanie, zarządzanie sesjami.
*   **Moduł Zarządzania Fiszami:** Tworzenie, przeglądanie, edycja, usuwanie zestawów fiszek i pojedynczych fiszek.
*   **Moduł Generowania Fisz AI:** Generowanie fiszek na podstawie tekstu wejściowego za pomocą modelu Ollama.
*   **Interfejs Użytkownika (UI):** Poprawność wyświetlania, responsywność, nawigacja.
*   **Integracja z Bazą Danych (Supabase):** Poprawność operacji CRUD, spójność danych.
*   **Obsługa Błędów:** Reakcja aplikacji na nieoczekiwane dane wejściowe i błędy systemowe.

**Wyłączone z zakresu:**
*   Testowanie infrastruktury Supabase (zakłada się, że usługa działa poprawnie).
*   Testowanie samego modelu AI (Ollama) poza kontekstem jego integracji z aplikacją.

### 3. Typy Testów do Przeprowadzenia

*   **Testy Jednostkowe (Unit Tests):**
    *   Cel: Weryfikacja poprawności działania najmniejszych, izolowanych części kodu (funkcje, metody).
    *   Zakres: Logika biznesowa w `app/crud/`, `app/services/`, `app/dependencies/`.
*   **Testy Integracyjne (Integration Tests):**
    *   Cel: Weryfikacja interakcji między różnymi komponentami aplikacji (np. API z bazą danych, API z usługą AI).
    *   Zakres: Endpointy API (`app/routers/`), interakcje z Supabase, wywołania Ollama.
*   **Testy Funkcjonalne (Functional Tests):**
    *   Cel: Weryfikacja, czy aplikacja spełnia określone wymagania funkcjonalne.
    *   Zakres: Wszystkie ścieżki użytkownika (rejestracja, logowanie, tworzenie zestawów, generowanie fiszek, nauka fiszek).
*   **Testy UI/UX (User Interface/User Experience Tests):**
    *   Cel: Weryfikacja poprawności interfejsu użytkownika, jego responsywności i użyteczności.
    *   Zakres: Wszystkie szablony HTML (`app/templates/`), nawigacja, formularze.
*   **Testy Bezpieczeństwa (Security Tests):**
    *   Cel: Identyfikacja podatności na ataki (np. nieautoryzowany dostęp, wstrzykiwanie SQL, XSS).
    *   Zakres: Moduł uwierzytelniania, walidacja danych wejściowych.
*   **Testy Wydajnościowe (Performance Tests):**
    *   Cel: Ocena szybkości, responsywności i stabilności aplikacji pod różnym obciążeniem.
    *   Zakres: Generowanie fiszek AI, operacje CRUD na dużej liczbie danych.
*   **Testy Regresji (Regression Tests):**
    *   Cel: Zapewnienie, że nowe zmiany w kodzie nie wprowadziły błędów do istniejących funkcjonalności.
    *   Zakres: Cała aplikacja po każdej istotnej zmianie lub nowej wersji.

### 4. Scenariusze Testowe dla Kluczowych Funkcjonalności

**A. Uwierzytelnianie i Autoryzacja:**
*   **Rejestracja:**
    *   Pomyślna rejestracja nowego użytkownika.
    *   Rejestracja z istniejącym adresem e-mail.
    *   Rejestracja z niepoprawnym formatem e-maila.
    *   Rejestracja z pustymi polami.
*   **Logowanie:**
    *   Pomyślne logowanie z poprawnymi danymi.
    *   Logowanie z niepoprawnym hasłem.
    *   Logowanie z nieistniejącym e-mailem.
    *   Logowanie z pustymi polami.
*   **Wylogowanie:**
    *   Pomyślne wylogowanie użytkownika.
*   **Dostęp autoryzowany:**
    *   Próba dostępu do zasobów wymagających autoryzacji bez zalogowania.
    *   Próba dostępu do zasobów innego użytkownika.

**B. Zarządzanie Zestawami Fiszek:**
*   **Tworzenie zestawu:**
    *   Pomyślne utworzenie nowego zestawu fiszek.
    *   Tworzenie zestawu z pustą nazwą.
    *   Tworzenie zestawu z fiszkami i bez fiszek.
*   **Przeglądanie zestawów:**
    *   Wyświetlanie wszystkich zestawów należących do użytkownika.
    *   Wyświetlanie szczegółów konkretnego zestawu.
    *   Próba wyświetlenia zestawu należącego do innego użytkownika.
*   **Edycja fiszki:**
    *   Pomyślna edycja pytania i odpowiedzi istniejącej fiszki.
    *   Edycja fiszki z pustym pytaniem/odpowiedzią.
    *   Próba edycji nieistniejącej fiszki.
*   **Usuwanie zestawu:**
    *   Pomyślne usunięcie zestawu fiszek.
    *   Próba usunięcia nieistniejącego zestawu.
    *   Próba usunięcia zestawu należącego do innego użytkownika.

**C. Generowanie Fisz AI:**
*   **Generowanie:**
    *   Generowanie fiszek z krótkiego, prostego tekstu.
    *   Generowanie fiszek z długiego, złożonego tekstu.
    *   Generowanie fiszek z tekstu zawierającego błędy ortograficzne/gramatyczne.
    *   Generowanie fiszek z tekstu w innym języku niż polski (jeśli wspierane).
    *   Generowanie fiszek z pustym tekstem wejściowym.
    *   Generowanie określonej liczby fiszek.
*   **Zapisywanie wygenerowanych fiszek:**
    *   Pomyślne zapisanie wygenerowanych fiszek jako nowy zestaw.
    *   Zapisywanie z pustą nazwą zestawu.
    *   Zapisywanie bez wybranych fiszek.

### 5. Środowisko Testowe

*   **Środowisko deweloperskie:** Lokalna maszyna deweloperska.
*   **Środowisko testowe (staging):** Docelowo dedykowane środowisko odzwierciedlające produkcję.
*   **Baza danych:** Supabase (instancja deweloperska/testowa).
*   **Model AI:** Lokalna instancja Ollama lub zdalna usługa.
*   **Przeglądarki:** Chrome (najnowsza wersja), Firefox (najnowsza wersja), Edge (najnowsza wersja).
*   **System operacyjny:** Windows, macOS, Linux (w zależności od dostępności).

### 6. Narzędzia do Testowania

*   **Testy jednostkowe/integracyjne (Backend):** `pytest`, `FastAPI TestClient`.
*   **Testy UI/UX (automatyzacja):** `Playwright` lub `Selenium` (do rozważenia w przyszłości).
*   **Testy API (manualne/automatyczne):** `Postman`, `curl`, `pytest-httpx`.
*   **Testy wydajnościowe:** `Locust` lub `JMeter` (do rozważenia w przyszłości).
*   **Zarządzanie testami:** Arkusze kalkulacyjne lub dedykowane narzędzie (np. TestLink, Zephyr).
*   **Raportowanie błędów:** System śledzenia błędów (np. Jira, GitHub Issues).

### 7. Harmonogram Testów

Harmonogram testów będzie zintegrowany z cyklem życia rozwoju oprogramowania (SDLC).

*   **Faza 1: Testy jednostkowe i integracyjne (ciągłe):** Wykonywane przez deweloperów w trakcie implementacji.
*   **Faza 2: Testy funkcjonalne i UI (po zakończeniu modułu):** Wykonywane przez QA po dostarczeniu stabilnej wersji modułu.
*   **Faza 3: Testy regresji (przed każdym wdrożeniem):** Wykonywane przed każdym wdrożeniem na środowisko staging.
*   **Faza 4: Testy bezpieczeństwa i wydajności (okresowo/przed wdrożeniem produkcyjnym):** Wykonywane po osiągnięciu stabilności funkcjonalnej.

### 8. Kryteria Akceptacji Testów

*   Wszystkie krytyczne i ważne defekty zostały usunięte i zweryfikowane.
*   Pokrycie testami jednostkowymi i integracyjnymi na poziomie co najmniej 80% dla kluczowej logiki biznesowej.
*   Wszystkie kluczowe scenariusze funkcjonalne zostały wykonane pomyślnie.
*   Aplikacja działa stabilnie i responsywnie na wszystkich wspieranych platformach.
*   Brak znanych luk bezpieczeństwa o wysokim priorytecie.
*   Wydajność aplikacji spełnia zdefiniowane wymagania (np. czas odpowiedzi API < 500ms).

### 9. Role i Odpowiedzialności w Procesie Testowania

*   **Deweloperzy:**
    *   Pisanie i utrzymywanie testów jednostkowych.
    *   Wykonywanie testów integracyjnych na poziomie komponentów.
    *   Naprawianie zgłoszonych defektów.
*   **Inżynier QA (Ja):**
    *   Tworzenie i utrzymywanie planu testów, przypadków testowych i scenariuszy.
    *   Wykonywanie testów funkcjonalnych, integracyjnych, UI/UX, bezpieczeństwa i wydajności.
    *   Raportowanie i śledzenie defektów.
    *   Zapewnienie jakości całego procesu.
*   **Product Owner/Manager Projektu:**
    *   Definiowanie wymagań i kryteriów akceptacji.
    *   Akceptacja ukończonych funkcjonalności.

### 10. Procedury Raportowania Błędów

1.  **Identyfikacja defektu:** Tester identyfikuje defekt podczas wykonywania testów.
2.  **Dokumentacja defektu:** Defekt jest dokumentowany w systemie śledzenia błędów, zawierając:
    *   Tytuł (zwięzły i opisowy).
    *   Opis (szczegółowy opis problemu).
    *   Kroki do reprodukcji.
    *   Oczekiwany wynik.
    *   Rzeczywisty wynik.
    *   Załączniki (screeny, logi, nagrania wideo).
    *   Priorytet (krytyczny, wysoki, średni, niski).
    *   Waga (blokujący, poważny, średni, drobny, kosmetyczny).
    *   Przypisanie do dewelopera.
3.  **Weryfikacja defektu:** Po naprawieniu defektu przez dewelopera, tester weryfikuje poprawkę.
4.  **Zamknięcie defektu:** Po pomyślnej weryfikacji, defekt jest zamykany.
5.  **Raporty:** Regularne raporty o stanie testów i defektów będą generowane i udostępniane zespołowi projektowemu.
