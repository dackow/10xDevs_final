<conversation_summary>
<decisions>
1.  **System Bazodanowy:** Zostanie użyty najprostszy system bazodanowy, czyli SQLite, zgodnie z proponowanym stosem technologicznym.
2.  **Zachowanie Kaskadowe (ON DELETE):** Usunięcie użytkownika będzie kaskadowo usuwać wszystkie powiązane zestawy fiszek i fiszki. Usunięcie zestawu fiszek będzie kaskadowo usuwać wszystkie fiszki w tym zestawie.
3.  **Długości Pól Tekstowych:** Przyjęto następujące maksymalne długości: `username` - 50 znaków, `name` (nazwa zestawu) - 100 znaków, `question` - 255 znaków, `answer` - 500 znaków.
4.  **Unikalność Nazwy Zestawu:** Nazwy zestawów fiszek będą unikalne w obrębie danego użytkownika (unikalny indeks na parze `user_id`, `name`).
5.  **Metadane Czasowe:** Do wszystkich głównych tabel (`User`, `FlashcardSet`, `Flashcard`) zostaną dodane kolumny `created_at` i `updated_at`.
6.  **Haszowanie Haseł:** Hasła użytkowników będą haszowane przy użyciu algorytmu Bcrypt za pośrednictwem biblioteki `passlib`.
7.  **Dane Użytkownika:** W tabeli `User` nie będzie przechowywany adres e-mail użytkownika w ramach MVP.
8.  **Indeksy Kluczy Obcych:** Zostaną jawnie utworzone indeksy na kolumnach kluczy obcych (`user_id` w `FlashcardSet` i `set_id` w `Flashcard`).
</decisions>

<matched_recommendations>
1.  **Rekomendacja dotycząca wyboru systemu bazodanowego:** Została zaakceptowana decyzja o pozostaniu przy SQLite ze względu na prostotę i szybkość wdrożenia MVP.
2.  **Rekomendacja dotycząca zachowania kaskadowego:** Została zaakceptowana reguła `ON DELETE CASCADE` dla relacji między `User` a `FlashcardSet` oraz `FlashcardSet` a `Flashcard`.
3.  **Rekomendacja dotycząca limitów długości pól tekstowych:** Została zaakceptowana propozycja konkretnych limitów długości dla pól tekstowych.
4.  **Rekomendacja dotycząca unikalności nazwy zestawu:** Została zaakceptowana propozycja nałożenia ograniczenia unikalności na parę (`user_id`, `name`) w tabeli `FlashcardSet`.
5.  **Rekomendacja dotycząca metadanych czasowych:** Została zaakceptowana propozycja dodania kolumn `created_at` i `updated_at` do głównych tabel.
6.  **Rekomendacja dotycząca haszowania haseł:** Została zaakceptowana propozycja użycia `passlib` z `bcrypt` jako najprostszej i najbezpieczniejszej implementacji.
7.  **Rekomendacja dotycząca danych użytkownika (email):** Moja rekomendacja rozważenia emaila została odrzucona na rzecz nieprzechowywania go w MVP.
8.  **Rekomendacja dotycząca indeksów kluczy obcych:** Została zaakceptowana propozycja jawnego zdefiniowania indeksów na kolumnach kluczy obcych.
9.  **Rekomendacja dotycząca gotowości do schematu:** Została zaakceptowana gotowość do przejścia do tworzenia ostatecznego schematu bazy danych.
</matched_recommendations>

<database_planning_summary>
Planowanie schematu bazy danych dla MVP Generatora Fiszek AI skupiło się na minimalizmie i efektywności, aby sprostać wyzwaniu 28-godzinnego czasu realizacji. Wybrano bazę danych SQLite ze względu na jej prostotę i brak konieczności konfiguracji serwera, co jest kluczowe dla szybkiego wdrożenia.

**a. Główne wymagania dotyczące schematu bazy danych:**
Schemat będzie obejmował trzy główne tabele: `User`, `FlashcardSet` i `Flashcard`. Wszystkie tabele będą zawierały kolumny `id` (klucz główny) oraz `created_at` i `updated_at` do śledzenia czasu utworzenia i modyfikacji. Hasła użytkowników będą bezpiecznie haszowane przy użyciu Bcrypt.

**b. Kluczowe encje i ich relacje:**
*   **User (Użytkownik):**
    *   Atrybuty: `id` (PRIMARY KEY), `username` (VARCHAR(50), UNIQUE), `password_hash` (VARCHAR(255)), `created_at`, `updated_at`.
    *   Relacje: Jeden użytkownik może posiadać wiele zestawów fiszek (One-to-Many z `FlashcardSet`).
*   **FlashcardSet (Zestaw Fiszek):**
    *   Atrybuty: `id` (PRIMARY KEY), `user_id` (FOREIGN KEY do `User.id`), `name` (VARCHAR(100)), `created_at`, `updated_at`.
    *   Ograniczenia: Para (`user_id`, `name`) musi być unikalna.
    *   Relacje: Jeden zestaw fiszek należy do jednego użytkownika (Many-to-One z `User`). Jeden zestaw fiszek może zawierać wiele pojedynczych fiszek (One-to-Many z `Flashcard`).
*   **Flashcard (Fiszka):**
    *   Atrybuty: `id` (PRIMARY KEY), `set_id` (FOREIGN KEY do `FlashcardSet.id`), `question` (TEXT/VARCHAR(255)), `answer` (TEXT/VARCHAR(500)), `created_at`, `updated_at`.
    *   Relacje: Jedna fiszka należy do jednego zestawu fiszek (Many-to-One z `FlashcardSet`).

**c. Ważne kwestie dotyczące bezpieczeństwa i skalowalności:**
*   **Bezpieczeństwo:** Hasła użytkowników będą bezpiecznie haszowane przy użyciu Bcrypt. Ze względu na użycie SQLite, bezpieczeństwo na poziomie wierszy (RLS) nie będzie implementowane w bazie danych; zamiast tego, logika autoryzacji (zapewniająca, że użytkownik ma dostęp tylko do swoich danych) zostanie zaimplementowana w warstwie aplikacji (FastAPI).
*   **Skalowalność:** Dla MVP, SQLite jest wystarczający. Jawne indeksowanie kluczy obcych zapewni dobrą wydajność zapytań. W przyszłości, w przypadku wzrostu liczby użytkowników i danych, migracja do bardziej skalowalnej bazy danych (np. PostgreSQL) będzie wymagała dostosowania, ale podstawowy schemat relacji pozostanie stabilny.

**d. Wszelkie nierozwiązane kwestie lub obszary wymagające dalszego wyjaśnienia:**
Wszystkie kluczowe aspekty planowania schematu bazy danych zostały rozwiązane i podjęto decyzje. Nie ma nierozwiązanych kwestii dotyczących samego schematu bazy danych.
</database_planning_summary>

<unresolved_issues>
Brak nierozwiązanych kwestii dotyczących planowania schematu bazy danych.
</unresolved_issues>
</conversation_summary>