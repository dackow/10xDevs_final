# Dokument wymagań produktu (PRD) - Generator Fiszek AI

## 1. Przegląd produktu
Celem projektu jest stworzenie aplikacji webowej (MVP), która rozwiązuje problem czasochłonnego tworzenia fiszek edukacyjnych. Aplikacja jest skierowana do dzieci ze szkoły podstawowej i umożliwia im automatyczne generowanie fiszek na podstawie dostarczonych przez nie materiałów (np. notatek z lekcji). Użytkownicy mogą zarządzać swoimi zestawami fiszek, edytować je i przygotowywać do nauki.

## 2. Problem użytkownika
Manualne tworzenie wysokiej jakości fiszek jest procesem powolnym i żmudnym. Uczniowie, zwłaszcza młodsi, często rezygnują z tej efektywnej metody nauki z powodu wysiłku wymaganego do przygotowania materiałów. Brak łatwego i szybkiego sposobu na przekształcanie własnych materiałów (takich jak notatki z lekcji, fragmenty podręczników czy artykuły) w zestawy fiszek stanowi barierę w regularnym stosowaniu metody powtórek interwałowych (spaced repetition).

## 3. Wymagania funkcjonalne
### 3.1. Uwierzytelnianie użytkownika
- Użytkownicy muszą mieć możliwość założenia konta za pomocą nazwy użytkownika i hasła.
- Użytkownicy muszą mieć możliwość zalogowania się na istniejące konto.
- System musi zapewniać, że tylko zalogowani użytkownicy mają dostęp do swoich zestawów fiszek.

### 3.2. Generowanie fiszek przez AI
- Aplikacja musi udostępniać pole tekstowe do wklejania treści źródłowej (np. notatek z lekcji), na podstawie której AI wygeneruje fiszki.
- Użytkownik musi mieć możliwość wyboru jednej z trzech opcji określających liczbę generowanych fiszek: "mało" (5), "średnio" (10), "dużo" (15).
- Backend musi komunikować się z API modelu językowego uruchomionego na Ollama (np. Mistral) w celu przetworzenia tekstu.
- Wynik generowania (zestaw par pytanie-odpowiedź) musi być wyświetlony użytkownikowi w czytelny sposób.

### 3.3. Zarządzanie fiszkami i zestawami (CRUD)
- Użytkownicy muszą mieć możliwość zapisania wygenerowanego zestawu fiszek na swoim koncie.
- Użytkownicy muszą mieć możliwość przeglądania listy wszystkich swoich zapisanych zestawów.
- Użytkownicy muszą mieć możliwość edycji treści pojedynczych fiszek (pytania i odpowiedzi) w zapisanym zestawie.
- Użytkownicy muszą mieć możliwość usunięcia całego zestawu fiszek.

## 4. Granice produktu
Następujące funkcje są świadomie wyłączone z zakresu tego MVP, aby zapewnić realizację projektu w wyznaczonym czasie:
- Generowanie fiszek przez AI na podstawie samego tematu (bez dostarczonego przez użytkownika tekstu źródłowego).
- Implementacja algorytmu powtórek (np. SM-2) do aktywnej nauki.
- Ręczne tworzenie fiszek od zera w istniejącym zestawie.
- Usuwanie pojedynczych fiszek z zestawu.
- Import plików w formatach innych niż czysty tekst (np. PDF, DOCX).
- Funkcje społecznościowe, takie jak współdzielenie zestawów fiszek między użytkownikami.
- Integracje z zewnętrznymi platformami edukacyjnymi.
- Dedykowane aplikacje mobilne (projekt jest wyłącznie webowy).
- Zaawansowany interfejs użytkownika i rozbudowany frontend oparty na frameworkach JavaScript.
- Logowanie za pośrednictwem zewnętrznych dostawców (np. Google, Facebook).
- Zaawansowane mechanizmy zbierania opinii od użytkowników.

## 5. Historyjki użytkowników
### 5.1. Zarządzanie kontem
- ID: US-001
- Tytuł: Rejestracja nowego użytkownika
- Opis: Jako nowy użytkownik, chcę móc założyć konto za pomocą unikalnej nazwy użytkownika i hasła, aby uzyskać dostęp do aplikacji i zapisywać swoje postępy.
- Kryteria akceptacji:
  - 1. Formularz rejestracji zawiera pola na nazwę użytkownika i hasła.
  - 2. Po pomyślnym przesłaniu formularza, nowe konto użytkownika jest tworzone w bazie danych.
  - 3. Użytkownik jest informowany o sukcesie i przekierowywany na stronę logowania.
  - 4. Jeśli nazwa użytkownika już istnieje, wyświetlany jest odpowiedni komunikat o błędzie.

- ID: US-002
- Tytuł: Logowanie do aplikacji
- Opis: Jako zarejestrowany użytkownik, chcę móc zalogować się na moje konto, aby uzyskać dostęp do moich zestawów fiszek.
- Kryteria akceptacji:
  - 1. Formularz logowania zawiera pola na nazwę użytkownika i hasło.
  - 2. Po pomyślnym zalogowaniu, użytkownik jest przekierowywany do głównego panelu aplikacji.
  - 3. W przypadku podania błędnych danych, wyświetlany jest odpowiedni komunikat o błędzie.

- ID: US-003
- Tytuł: Wylogowanie z aplikacji
- Opis: Jako zalogowany użytkownik, chcę móc się wylogować, aby bezpiecznie zakończyć sesję.
- Kryteria akceptacji:
  - 1. W interfejsie aplikacji widoczny jest przycisk "Wyloguj".
  - 2. Po kliknięciu przycisku, sesja użytkownika jest kończona.
  - 3. Użytkownik jest przekierowywany na stronę logowania.

### 5.2. Tworzenie i zarządzanie fiszkami
- ID: US-004
- Tytuł: Generowanie fiszek z notatek
- Opis: Jako zalogowany użytkownik, chcę wkleić tekst moich notatek z lekcji do formularza, wybrać liczbę fiszek do wygenerowania i zainicjować proces, aby szybko stworzyć materiały do nauki.
- Kryteria akceptacji:
  - 1. Na stronie głównej znajduje się pole tekstowe oraz opcje wyboru ilości fiszek ("mało", "średnio", "dużo").
  - 2. Po kliknięciu przycisku "Generuj", aplikacja wysyła zapytanie do API modelu AI z treścią notatek.
  - 3. Po otrzymaniu odpowiedzi, wygenerowane pary pytanie-odpowiedź są wyświetlane na ekranie w czytelnej liście.
  - 4. Jeśli pole tekstowe jest puste, po kliknięciu "Generuj" wyświetlany jest komunikat o błędzie.

- ID: US-005
- Tytuł: Zapisywanie nowego zestawu fiszek
- Opis: Jako użytkownik, po wygenerowaniu fiszek, chcę móc zapisać je jako nowy zestaw, nadając mu nazwę, aby móc do niego wrócić w przyszłości.
- Kryteria akceptacji:
  - 1. Po wygenerowaniu fiszek widoczny jest przycisk "Zapisz zestaw" oraz pole na jego nazwę.
  - 2. Po kliknięciu przycisku "Zapisz zestaw" z poprawnie wypełnioną nazwą, nowy zestaw jest zapisywany w bazie danych i powiązany z kontem użytkownika.
  - 3. Użytkownik jest przekierowywany do listy swoich zestawów, gdzie widoczny jest nowo dodany element.
  - 4. Jeśli użytkownik spróbuje zapisać zestaw z pustą nazwą, operacja jest blokowana i wyświetlany jest odpowiedni komunikat o błędzie (np. "Nazwa zestawu nie może być pusta").

- ID: US-006
- Tytuł: Przeglądanie listy zapisanych zestawów
- Opis: Jako zalogowany użytkownik, chcę widzieć listę wszystkich moich zapisanych zestawów fiszek, aby móc wybrać jeden z nich do przeglądania lub edycji.
- Kryteria akceptacji:
  - 1. W głównym panelu aplikacji wyświetlana jest lista nazw wszystkich zestawów należących do użytkownika.
  - 2. Każda nazwa na liście jest linkiem prowadzącym do widoku szczegółowego danego zestawu.

- ID: US-007
- Tytuł: Przeglądanie zawartości zestawu
- Opis: Jako użytkownik, chcę móc kliknąć na wybrany zestaw z mojej listy, aby zobaczyć wszystkie fiszki, które się w nim znajdują.
- Kryteria akceptacji:
  - 1. Po kliknięciu na nazwę zestawu, wyświetlana jest strona ze wszystkimi parami pytanie-odpowiedź z tego zestawu.
  - 2. Przy każdej fiszce widoczna jest opcja "Edytuj".

- ID: US-008
- Tytuł: Edycja pojedynczej fiszki
- Opis: Jako użytkownik, chcę móc edytować treść pytania i odpowiedzi w istniejącej fiszce, aby poprawić błędy lub doprecyzować informacje.
- Kryteria akceptacji:
  - 1. Po kliknięciu przycisku "Edytuj" przy fiszce, użytkownik jest przenoszony do formularza edycji.
  - 2. Formularz jest wypełniony aktualną treścią pytania i odpowiedzi.
  - 3. Po zapisaniu zmian, dane fiszki w bazie danych są aktualizowane.
  - 4. Użytkownik jest przekierowywany z powrotem do widoku zestawu, gdzie widzi zaktualizowaną treść.

- ID: US-009
- Tytuł: Usuwanie całego zestawu fiszek
- Opis: Jako użytkownik, chcę móc usunąć cały zestaw fiszek, gdy nie jest mi już potrzebny.
- Kryteria akceptacji:
  - 1. Na liście zestawów, przy każdej nazwie znajduje się przycisk "Usuń".
  - 2. Po kliknięciu przycisku, wyświetlane jest potwierdzenie operacji.
  - 3. Po potwierdzeniu, cały zestaw wraz ze wszystkimi powiązanymi fiszkami jest usuwany z bazy danych.

## 6. Metryki sukcesu
### 6.1. Metryki sukcesu projektu (MVP)
Głównym kryterium sukcesu dla tego etapu jest dostarczenie działającej aplikacji, która w 100% spełnia poniższe wymagania zaliczeniowe w wyznaczonym czasie:
- 1. Wdrożona funkcjonalność uwierzytelniania użytkowników.
- 2. Wdrożona kluczowa logika biznesowa wykorzystująca model LLM.
- 3. Wdrożona pełna funkcjonalność CRUD dla danych aplikacji.
- 4. Istnienie w projekcie co najmniej jednego działającego testu jednostkowego.
- 5. Skonfigurowany i działający scenariusz CI/CD na GitHub Actions.

### 6.2. Metryki sukcesu produktu (dla przyszłego rozwoju)
Po wdrożeniu MVP i ewentualnym dalszym rozwoju, sukces produktu będzie mierzony na podstawie następującego wskaźnika:
- Wskaźnik akceptacji AI: Co najmniej 75% fiszek wygenerowanych przez AI jest akceptowanych przez użytkowników (tzn. nie są przez nich edytowane).
