### Plan Wdrożenia Aplikacji na Railway

Ten dokument opisuje kroki niezbędne do wdrożenia aplikacji AI Flashcard Generator na platformie Railway.

**Cel:** Uruchomienie stabilnej, produkcyjnej wersji aplikacji dostępnej publicznie.

---

#### **Faza 1: Przygotowanie Lokalne**

1.  **Weryfikacja Zmiennych Środowiskowych:**
    *   **Cel:** Zidentyfikować wszystkie sekrety i zmienne konfiguracyjne wymagane do uruchomienia aplikacji.
    *   **Akcja:** Przejrzeć kod aplikacji, w szczególności pliki `app/config.py`, `app/dependencies.py` i inne miejsca, gdzie ładowana jest konfiguracja (np. przez `os.getenv`).
    *   **Oczekiwany rezultat:** Stworzenie listy wszystkich wymaganych zmiennych, np.:
        *   `SUPABASE_URL`
        *   `SUPABASE_KEY`
        *   `SECRET_KEY` (dla JWT)
        *   `OLLAMA_API_URL`
        *   `ALGORITHM`
        *   `ACCESS_TOKEN_EXPIRE_MINUTES`

2.  **Weryfikacja Komendy Startowej:**
    *   **Cel:** Upewnić się, że komenda do uruchomienia serwera jest poprawna dla środowiska produkcyjnego.
    *   **Akcja:** Komenda `uvicorn app.main:app --reload` jest przeznaczona do dewelopmentu. Dla produkcji należy użyć komendy, która będzie nasłuchiwać na odpowiednim porcie i hoście.
    *   **Oczekiwany rezultat:** Przygotowanie komendy startowej: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
        *   `--host 0.0.0.0`: Umożliwia przyjmowanie połączeń z zewnątrz kontenera.
        *   `--port $PORT`: Railway dynamicznie przypisuje port, na którym aplikacja musi nasłuchiwać, i udostępnia go poprzez zmienną środowiskową `$PORT`.

3.  **Sprawdzenie `requirements.txt`:**
    *   **Cel:** Upewnić się, że plik `requirements.txt` zawiera wszystkie niezbędne zależności.
    *   **Akcja:** Zweryfikować, czy wszystkie biblioteki (np. `fastapi`, `uvicorn`, `sqlalchemy`, `supabase-py`, `httpx`, `python-jose[cryptography]`, `passlib[bcrypt]`) są w pliku.
    *   **Oczekiwany rezultat:** Kompletny i aktualny plik `requirements.txt`.

---

#### **Faza 2: Konfiguracja na Platformie Railway**

1.  **Utworzenie Nowego Projektu:**
    *   **Cel:** Stworzyć projekt na Railway i połączyć go z repozytorium GitHub.
    *   **Akcja:**
        1.  Zaloguj się na swoje konto Railway.
        2.  Kliknij "New Project".
        3.  Wybierz opcję "Deploy from GitHub repo".
        4.  Wybierz repozytorium z aplikacją.

2.  **Konfiguracja Usługi (Service):**
    *   **Cel:** Skonfigurować sposób budowania i uruchamiania aplikacji.
    *   **Akcja:**
        1.  Po utworzeniu projektu, przejdź do zakładki "Settings" nowo utworzonej usługi.
        2.  W sekcji "Build", upewnij się, że Railway poprawnie wykrył projekt jako aplikację Python (używając buildpacka Nixpacks).
        3.  W sekcji "Deploy", znajdź pole "Start Command" i wklej przygotowaną wcześniej komendę: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.

3.  **Dodanie Zmiennych Środowiskowych:**
    *   **Cel:** Bezpieczne przekazanie sekretów do aplikacji.
    *   **Akcja:**
        1.  Przejdź do zakładki "Variables" w ustawieniach usługi na Railway.
        2.  Dodaj wszystkie zidentyfikowane w Fazie 1 zmienne środowiskowe (np. `SUPABASE_URL`, `SUPABASE_KEY`, `SECRET_KEY` itd.) wraz z ich produkcyjnymi wartościami.
        3.  **Ważne:** Upewnij się, że wartości pochodzą z produkcyjnego projektu Supabase, a nie deweloperskiego.

---

#### **Faza 3: Wdrożenie i Weryfikacja**

1.  **Uruchomienie Wdrożenia (Deploy):**
    *   **Cel:** Zbudowanie i uruchomienie aplikacji na platformie.
    *   **Akcja:**
        1.  Railway automatycznie rozpocznie proces wdrożenia po każdej zmianie w głównej gałęzi repozytorium (np. `main` lub `master`).
        2.  Można również ręcznie uruchomić wdrożenie z poziomu interfejsu Railway.

2.  **Analiza Logów Wdrożenia:**
    *   **Cel:** Sprawdzenie, czy proces budowania i uruchamiania przebiegł pomyślnie.
    *   **Akcja:**
        1.  Przejdź do zakładki "Deployments" i obserwuj logi na żywo.
        2.  Zwróć uwagę na ewentualne błędy podczas instalacji zależności z `requirements.txt` lub podczas uruchamiania serwera Uvicorn.

3.  **Generowanie i Użycie Publicznej Domeny:**
    *   **Cel:** Uzyskanie dostępu do wdrożonej aplikacji.
    *   **Akcja:**
        1.  W zakładce "Settings" usługi, w sekcji "Networking", Railway automatycznie wygeneruje publiczny adres URL (np. `twoja-aplikacja.up.railway.app`).
        2.  Możesz również podpiąć własną domenę.

4.  **Testy Akceptacyjne:**
    *   **Cel:** Potwierdzenie, że aplikacja działa poprawnie w środowisku produkcyjnym.
    *   **Akcja:**
        1.  Otwórz publiczny adres URL w przeglądarce.
        2.  Przetestuj kluczowe funkcjonalności:
            *   Rejestracja nowego użytkownika.
            *   Logowanie i wylogowywanie.
            *   Generowanie nowego zestawu fiszek.
            *   Wyświetlanie, edycja i usuwanie istniejących zestawów.
        3.  Sprawdź konsolę deweloperską w przeglądarce pod kątem błędów.

---