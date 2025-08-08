**Cel Główny:**
Stworzenie w ciągu 28 godzin w pełni funkcjonalnej aplikacji webowej, która spełnia wszystkie wymagania zaliczeniowe. Aplikacja będzie służyć dzieciom ze szkoły podstawowej do automatycznego generowania fiszek edukacyjnych z podanego tekstu.

**Kluczowe Funkcjonalności:**
1.  **Logowanie:** Prosta rejestracja i logowanie użytkownika na podstawie loginu i hasła.
2.  **Generowanie Fiszek:** Użytkownik wkleja tekst, wybiera jedną z trzech opcji ilości ("mało", "średnio", "dużo"), a AI (model Mistral przez Ollama) generuje zestaw fiszek.
3.  **Zarządzanie Fiszkami (Pełny CRUD):** Użytkownik może:
    *   **Zapisywać** wygenerowane zestawy (Create).
    *   **Przeglądać** listę swoich zestawów oraz fiszki wewnątrz nich (Read).
    *   **Edytować** pojedyncze fiszki w zapisanym zestawie (Update).
    *   **Usuwać** całe zestawy fiszek (Delete).

**Stos Technologiczny:**
*   **Backend:** Python (Flask lub FastAPI).
*   **Baza Danych:** Supabase (PostgreSQL).
*   **Frontend:** Podstawowy HTML z formularzami.
*   **AI:** Model Mistral dostępny przez API z Ollamy.

**Co jest Poza Zakresem:**
*   Właściwy system nauki i powtórek (algorytm SM-2).
*   Zaawansowany interfejs użytkownika.
*   Logowanie przez zewnętrzne serwisy (np. Google).

**Główne Ryzyko i Strategia:**
Największym ryzykiem jest bardzo krótki czas (28 godzin), zwłaszcza po dodaniu funkcji edycji. Kluczowe dla sukcesu jest ścisłe trzymanie się ustalonego, minimalistycznego zakresu i planu pracy, bez dodawania jakichkolwiek nowych funkcjonalności.
