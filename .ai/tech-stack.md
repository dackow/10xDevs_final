# Proponowany Stos Technologiczny

Na podstawie analizy dokumentu wymagań produktu (PRD), w szczególności z naciskiem na prostotę, szybkość wdrożenia MVP i jasno określone granice, proponowany jest następujący stos technologiczny:

## Backend

*   **Framework:** **FastAPI**
    *   **Uzasadnienie:** Nowoczesny, wysokowydajny framework idealny do budowy API. Jego wbudowana walidacja danych (dzięki Pydantic) będzie niezwykle pomocna przy obsłudze danych od użytkownika i odpowiedzi z modelu LLM. Automatycznie generowana dokumentacja (Swagger UI) znacząco przyspieszy testowanie endpointów. Jest prostszy w konfiguracji niż Django dla projektu o tym zakresie.

*   **Baza Danych i Autentykacja:** **Supabase**
    *   **Uzasadnienie:** Supabase to platforma "Backend as a Service" (BaaS), która dostarcza bazę danych PostgreSQL, wbudowany system uwierzytelniania, API oraz przechowywanie plików. Wybór Supabase zamiast SQLite i własnej implementacji autentykacji znacząco upraszcza i przyspiesza rozwój. Zapewnia gotowe, bezpieczne rozwiązanie do zarządzania użytkownikami (rejestracja, logowanie, odzyskiwanie hasła), co jest zgodne z wymaganiami z PRD (US-001, US-002, US-010). Użycie PostgreSQLa daje możliwość łatwego skalowania w przyszłości.

*   **Klient Bazy Danych:** **supabase-py**
    *   **Uzasadnienie:** Oficjalna biblioteka kliencka dla Pythona do interakcji z API Supabase. Umożliwia łatwe wykonywanie operacji na bazie danych (CRUD) oraz zarządzanie autentykacją w sposób, który dobrze integruje się z logiką backendu w FastAPI.

*   **Komunikacja z AI (Ollama):** **HTTPX**
    *   **Uzasadnienie:** Nowoczesna biblioteka do wykonywania zapytań HTTP, która wspiera zarówno operacje synchroniczne, jak i asynchroniczne. Ponieważ FastAPI jest frameworkiem asynchronicznym, użycie `HTTPX` pozwoli na nieblokującą komunikację z API Ollamy, co jest kluczowe dla wydajności.

## Frontend

*   **Silnik Szablonów:** **Jinja2**
    *   **Uzasadnienie:** Standardowy silnik szablonów, który integruje się z FastAPI "prosto z pudełka". Pozwala na generowanie dynamicznych stron HTML po stronie serwera, bez konieczności budowania skomplikowanego frontendu w JavaScripcie, co jest zgodne z granicami projektu zdefiniowanymi w PRD.

*   **Framework CSS:** **Bootstrap**
    *   **Uzasadnienie:** Umożliwi stworzenie czystego i responsywnego interfejsu użytkownika przy minimalnym wysiłku. Zamiast pisać własny CSS od zera, można będzie skorzystać z gotowych komponentów (formularze, przyciski, listy), co znacząco przyspieszy pracę.

## Serwer

*   **Serwer ASGI:** **Uvicorn**
    *   **Uzasadnienie:** Standardowy serwer do uruchamiania aplikacji opartych na FastAPI. Jest szybki i prosty w użyciu.

## Podsumowanie

| Komponent                  | Technologia | Uzasadnienie                                       |
| -------------------------- | ----------- | -------------------------------------------------- |
| **Framework Backend**      | FastAPI     | Szybkość, walidacja danych, auto-dokumentacja API. |
| **Baza Danych i Auth**     | Supabase    | Gotowe rozwiązanie do autentykacji i baza PostgreSQL. |
| **Klient Bazy Danych**     | supabase-py | Oficjalna biblioteka do interakcji z Supabase.      |
| **Klient HTTP (do Ollama)**| HTTPX       | Wsparcie dla asynchroniczności w FastAPI.          |
| **Silnik Szablonów HTML**  | Jinja2      | Proste generowanie HTML po stronie serwera.        |
| **Framework CSS**          | Bootstrap   | Szybkie budowanie estetycznego interfejsu.         |
| **Serwer Aplikacji**       | Uvicorn     | Standardowy serwer dla FastAPI.                    |