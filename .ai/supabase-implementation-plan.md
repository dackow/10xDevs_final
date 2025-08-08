# Plan Implementacji Supabase

Ten plan opisuje kroki niezbędne do migracji z lokalnej bazy danych SQLite i własnej autentykacji na platformę Supabase, która zapewni bazę danych PostgreSQL oraz gotowe rozwiązanie do zarządzania użytkownikami.

## 1. Konfiguracja Projektu w Supabase

Pierwszym krokiem jest przygotowanie środowiska w chmurze Supabase.

*   **Krok 1: Utworzenie projektu**
    *   Zaloguj się na [supabase.com](https://supabase.com) i utwórz nowy projekt.
    *   Wybierz region geograficzny najbliższy Twoim użytkownikom.
    *   Zapisz bezpiecznie klucze API (Project URL, `anon` key, `service_role` key) – będą potrzebne w aplikacji.

*   **Krok 2: Definicja schematu bazy danych**
    *   Przejdź do edytora SQL w panelu Supabase.
    *   Utwórz tabelę `flashcard_sets` do przechowywania zestawów fiszek.
        ```sql
        CREATE TABLE flashcard_sets (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID REFERENCES auth.users(id) NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMPTZ DEFAULT now()
        );
        ```
    *   Utwórz tabelę `flashcards` do przechowywania pojedynczych fiszek.
        ```sql
        CREATE TABLE flashcards (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            set_id UUID REFERENCES flashcard_sets(id) ON DELETE CASCADE NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TIMESTAMPTZ DEFAULT now()
        );
        ```

*   **Krok 3: Zabezpieczenie dostępu (Row Level Security)**
    *   Włącz Row Level Security (RLS) dla obu tabel.
    *   Stwórz polityki RLS, aby użytkownicy mogli zarządzać (tworzyć, czytać, aktualizować, usuwać) tylko własne zestawy fiszek i fiszki.
        *   **Przykład polityki dla `flashcard_sets`:**
            ```sql
            -- Użytkownicy mogą zarządzać tylko swoimi zestawami
            CREATE POLICY "Enable all operations for users based on user_id"
            ON flashcard_sets FOR ALL
            USING (auth.uid() = user_id);
            ```

## 2. Integracja z Aplikacją FastAPI

Teraz należy skonfigurować aplikację w taki sposób, aby komunikowała się z Supabase.

*   **Krok 1: Zarządzanie zależnościami**
    *   Dodaj `supabase-py` do pliku `requirements.txt`.
    *   Usuń `SQLAlchemy` oraz `alembic` z `requirements.txt`, ponieważ nie będą już potrzebne.

*   **Krok 2: Konfiguracja aplikacji**
    *   W pliku `app/config.py` dodaj obsługę zmiennych środowiskowych dla URL i klucza Supabase.
    *   Stwórz plik `.env` w głównym katalogu projektu i dodaj do niego `SUPABASE_URL` oraz `SUPABASE_KEY`.
    *   **Ważne:** Dodaj plik `.env` do `.gitignore`, aby uniknąć wycieku kluczy.

*   **Krok 3: Inicjalizacja klienta Supabase**
    *   W pliku `app/dependencies.py` (lub w nowym, dedykowanym module) stwórz funkcję, która inicjalizuje i zwraca klienta Supabase. Będzie on wstrzykiwany jako zależność do endpointów API.

## 3. Implementacja Autentykacji

Należy zastąpić istniejący system uwierzytelniania rozwiązaniem wbudowanym w Supabase.

*   **Krok 1: Refaktoryzacja routera `auth.py`**
    *   Przepisz endpointy `/register`, `/login` i `/logout` w `app/routers/auth.py`, aby korzystały z metod klienta Supabase:
        *   Rejestracja: `supabase.auth.sign_up()`
        *   Logowanie: `supabase.auth.sign_in_with_password()`
        *   Wylogowanie: `supabase.auth.sign_out()`

*   **Krok 2: Zabezpieczenie endpointów**
    *   Stwórz nową zależność (dependency) w FastAPI, która będzie weryfikować token JWT (JSON Web Token) dostarczony w nagłówku `Authorization`.
    *   Zależność powinna używać `supabase.auth.get_user()` do weryfikacji tokenu i zwracania danych zalogowanego użytkownika.
    *   Zastosuj tę zależność do wszystkich endpointów wymagających autentykacji.

## 4. Refaktoryzacja Logiki Biznesowej (CRUD)

Operacje na danych muszą zostać dostosowane do nowego sposobu komunikacji z bazą.

*   **Krok 1: Aktualizacja modułu `crud.py`**
    *   Przepisz wszystkie funkcje w `app/crud/crud.py`, zastępując zapytania SQLAlchemy metodami klienta Supabase.
        *   **Przykład:**
            *   Zamiast `db.query(models.FlashcardSet).all()` użyj `supabase.table('flashcard_sets').select('*').execute()`.
            *   Zamiast `db.add(new_set)` użyj `supabase.table('flashcard_sets').insert(data).execute()`.

*   **Krok 2: Usunięcie starej infrastruktury**
    *   Usuń katalog `migrations` oraz plik `alembic.ini`.
    *   Usuń definicje modeli z `app/models/models.py`, ponieważ schemat bazy danych jest teraz zarządzany bezpośrednio w Supabase.

## 5. Aktualizacja Testów

Na koniec należy dostosować istniejące testy do nowej architektury.

*   **Krok 1: Mockowanie klienta Supabase**
    *   Zmodyfikuj testy jednostkowe i integracyjne tak, aby mockowały (udawały) klienta `supabase-py`.
    *   Dzięki temu testy będą mogły sprawdzać logikę aplikacji bez potrzeby łączenia się z prawdziwą instancją Supabase, co zapewni ich szybkość i niezawodność.
