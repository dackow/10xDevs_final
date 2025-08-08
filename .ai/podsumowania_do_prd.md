<conversation_summary>
<decisions>
Grupa docelowa: Dzieci ze szkoły podstawowej.
Treści do przetwarzania: Materiały szkolne z różnych przedmiotów (np. język polski, angielski, historia, przyroda), z wyłączeniem tabliczki mnożenia.
System powtórek: Algorytm SM-2 został wybrany jako docelowy, ale jego implementacja została odłożona na etap po MVP, aby zmieścić się w ramach czasowych.
Mechanizm logowania: Zostanie zaimplementowany najprostszy system oparty na loginie i haśle.
Generowanie fiszek przez AI: Użytkownik będzie miał kontrolę nad ilością generowanych fiszek poprzez opcje "mało", "średnio", "dużo".
Technologia AI: Zostanie wykorzystany model Mistral uruchomiony na platformie Ollama, dostępny przez wewnętrzne API. Backend będzie napisany w języku Python.
Zarządzanie fiszkami (CRUD): Aplikacja umożliwi pełne operacje CRUD: tworzenie (zapisywanie) zestawów, przeglądanie ich listy i zawartości (Read), edycję pojedynczych fiszek (Update) oraz usuwanie całych zestawów (Delete).
Proces edycji: Po wygenerowaniu zestawu, użytkownik będzie mógł przejrzeć wszystkie fiszki, a następnie edytować każdą z nich osobno na dedykowanym, prostym ekranie edycji.
Zbieranie opinii: W pierwszej wersji MVP nie będzie dedykowanego mechanizmu do zbierania opinii od użytkowników.
Ramy czasowe i zakres: Projekt musi zostać zrealizowany w ciągu 28 godzin (7 dni po 4 godziny) i musi spełniać 5 konkretnych wymagań zaliczeniowych (auth, logika biznesowa z LLM, CRUD, test, CI/CD).
Architektura techniczna: Backend oparty na lekkim frameworku (Flask/FastAPI), baza danych Supabase (PostgreSQL) oraz prosty frontend w HTML.
Definicja ilości fiszek: Opcje "mało", "średnio", "dużo" zostaną zmapowane na konkretne liczby: 5, 10 i 15 fiszek.
Komunikacja z AI: Wybrana liczba fiszek zostanie przekazana do modelu AI jako precyzyjna, bezpośrednia instrukcja w prompcie (np. "wygeneruj dokładnie 10 fiszek").
</decisions>
<matched_recommendations>
Rekomendacja dotycząca prostego scenariusza i architektury: Została w pełni zaakceptowana. Zdefiniowano kluczowy "happy path" użytkownika oraz wybrano minimalistyczny stos technologiczny (Python/Flask, Supabase (PostgreSQL), prosty HTML), aby zapewnić realizację projektu w wyznaczonym czasie.
Rekomendacja dotycząca skupienia się na "master-prompcie": Została zaakceptowana jako kluczowy element projektu. Ustalono, że stworzenie precyzyjnego i łatwo modyfikowalnego promptu będzie priorytetem w celu zapewnienia jakości generowanych fiszek.
Rekomendacja dotycząca podziału pracy na bloki: Została zaakceptowana i stała się podstawą planu działania. Praca zostanie podzielona na cztery logiczne etapy: szkielet aplikacji, implementacja Auth i CRUD, integracja z AI, a na końcu testy i CI/CD.
Rekomendacja dotycząca uproszczenia zakresu: Pierwotna rekomendacja o radykalnym uproszczeniu została odrzucona na rzecz planu, który spełniałby wymagania zaliczeniowe. Jednak jej duch został zachowany poprzez świadome odłożenie na później wszystkich funkcji (jak system powtórek), które nie były absolutnie konieczne do zaliczenia.
</matched_recommendations>
<prd_planning_summary>
Celem projektu jest stworzenie w ciągu 28 godzin aplikacji webowej do generowania fiszek dla dzieci, która spełnia 5 kluczowych wymagań zaliczeniowych. Poniższe podsumowanie stanowi podstawę do dalszych prac.
a. Główne wymagania funkcjonalne produktu:
System Uwierzytelniania: Użytkownicy muszą mieć możliwość rejestracji i logowania za pomocą loginu i hasła.
Generator Fiszek AI: Aplikacja musi pozwalać zalogowanemu użytkownikowi na wklejenie tekstu, wybranie pożądanej ilości fiszek ("mało", "średnio", "dużo") i otrzymanie zestawu wygenerowanego przez model Mistral.
Zarządzanie Zestawami Fiszek (Pełny CRUD): Użytkownik musi mieć możliwość zapisania wygenerowanego zestawu na swoim koncie (Create), przeglądania listy swoich zestawów i ich zawartości (Read), edycji pojedynczych fiszek w zestawie (Update) oraz usuwania całych zestawów (Delete).
b. Kluczowe historie użytkownika i ścieżki korzystania:
Rejestracja i logowanie: "Jako nowy użytkownik, chcę założyć konto używając loginu i hasła, aby móc zapisywać swoje fiszki."
Generowanie i zapisywanie: "Jako zalogowany użytkownik, chcę wkleić tekst z moich notatek, wygenerować z niego fiszki i zapisać je na moim koncie, aby móc do nich wrócić później."
Przeglądanie i edycja: "Jako użytkownik, chcę przejrzeć wygenerowane fiszki, poprawić te, które zawierają błędy lub są niejasne, aby mieć pewność, że uczę się z poprawnych materiałów."
Zarządzanie listą: "Jako użytkownik, chcę widzieć listę wszystkich moich zestawów fiszek i mieć możliwość ich usunięcia, gdy nie są mi już potrzebne."
c. Ważne kryteria sukcesu i sposoby ich mierzenia:
Kryterium Główne (Zaliczeniowe): Dostarczenie w ciągu 28 godzin działającej aplikacji, która implementuje wszystkie 5 wymaganych komponentów: uwierzytelnianie, logikę biznesową z LLM, pełny CRUD, test jednostkowy oraz CI/CD. Miarą sukcesu jest 100% zgodność z tymi wymaganiami.
Kryteria Produktowe (Wtórne dla MVP): Pierwotne cele (75% akceptacji fiszek AI, 75% fiszek tworzonych przez AI) pozostają w tle jako cele dla przyszłego rozwoju produktu, ale nie są priorytetem dla tego konkretnego, ograniczonego czasowo zadania.
</prd_planning_summary>
<unresolved_issues>
Finalna treść "master-promptu": Chociaż zgodzono się co do jego kluczowej roli, ostateczna, zoptymalizowana treść promptu dla modelu Mistral będzie musiała zostać stworzona i przetestowana w trakcie developmentu.
Dokładny interfejs użytkownika: Ustalono, że interfejs będzie minimalistyczny (prosty HTML), ale dokładny wygląd i przepływ między ekranami (zwłaszcza w procesie edycji fiszki i powrotu do listy) nie został wizualnie zaprojektowany.
</unresolved_issues>
</conversation_summary>