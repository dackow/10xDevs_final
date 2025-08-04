# Proponowany Stos Technologiczny

Na podstawie analizy dokumentu wymagań produktu (PRD), w szczególności z naciskiem na prostotę, szybkość wdrożenia MVP i jasno określone granice, proponowany jest następujący stos technologiczny:

## Backend

*   **Framework:** **FastAPI**
    *   **Uzasadnienie:** Nowoczesny, wysokowydajny framework idealny do budowy API. Jego wbudowana walidacja danych (dzięki Pydantic) będzie niezwykle pomocna przy obsłudze danych od użytkownika i odpowiedzi z modelu LLM. Automatycznie generowana dokumentacja (Swagger UI) znacząco przyspieszy testowanie endpointów. Jest prostszy w konfiguracji niż Django dla projektu o tym zakresie.

*   **Baza Danych:** **SQLite**
    *   **Uzasadnienie:** Wbudowana w Pythona, bezserwerowa baza danych. Jest to najprostsze możliwe rozwiązanie, które w pełni zaspokaja potrzeby MVP (przechowywanie użytkowników i zestawów fiszek). Eliminuje potrzebę konfiguracji i zarządzania osobnym serwerem bazodanowym. Cała baza danych to pojedynczy plik.

*   **ORM (Object-Relational Mapping):** **SQLAlchemy**
    *   **Uzasadnienie:** Standard de facto w świecie Pythona do pracy z relacyjnymi bazami danych. Umożliwia definiowanie struktury bazy danych za pomocą klas Pythona i wykonywanie zapytań w sposób obiektowy, co jest znacznie czytelniejsze i bezpieczniejsze niż pisanie surowego SQL. Doskonale integruje się z FastAPI.

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
| **Baza Danych**            | SQLite      | Prostota, brak konfiguracji, idealna dla MVP.      |
| **ORM**                    | SQLAlchemy  | Standard branżowy, bezpieczna interakcja z bazą.   |
| **Klient HTTP (do Ollama)**| HTTPX       | Wsparcie dla asynchroniczności w FastAPI.          |
| **Silnik Szablonów HTML**  | Jinja2      | Proste generowanie HTML po stronie serwera.        |
| **Framework CSS**          | Bootstrap   | Szybkie budowanie estetycznego interfejsu.         |
| **Serwer Aplikacji**       | Uvicorn     | Standardowy serwer dla FastAPI.                    |
