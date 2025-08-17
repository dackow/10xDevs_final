<#
.SYNOPSIS
    Analizuje najczęściej zmieniane pliki w repozytorium Git.

.DESCRIPTION
    Ten skrypt PowerShell analizuje historię commitów w repozytorium Git,
    aby zidentyfikować pliki, które były najczęściej modyfikowane w określonym okresie.
    Skrypt wyklucza pliki konfiguracyjne, testowe, dokumentację, pliki budowania,
    zasoby statyczne i pliki cache Pythona, aby skupić się na kodzie źródłowym.
    Dodatkowo, skrypt osobno analizuje i wyświetla najczęściej zmieniane pliki testowe.

.PARAMETER Since
    Określa okres, od którego mają być analizowane zmiany plików.
    Akceptuje formaty zrozumiałe dla `git log --since`, np. "1 year ago", "2 months ago", "2023-01-01".
    Domyślna wartość to "1 year ago".

.PARAMETER Top
    Określa liczbę top najczęściej zmienianych plików do wyświetlenia.
    Domyślna wartość to 10.

.EXAMPLE
    .\top_modified_files.ps1
    Wyświetla 10 najczęściej zmienianych plików z ostatniego roku, z wyłączeniem typowych plików pomocniczych.

.EXAMPLE
    .\top_modified_files.ps1 -Since "3 months ago" -Top 5
    Wyświetla 5 najczęściej zmienianych plików z ostatnich 3 miesięcy.

.NOTES
    Wymaga zainstalowanego Git'a i dostępu do repozytorium Git.
    Skrypt ignoruje commity scalające (merge commits).
    Wzorce wykluczeń są dostosowane do projektów Python/FastAPI/Supabase.
#> 
# top_modified_files.ps1
# Skrypt PowerShell do analizy najczęściej zmienianych plików w repo (ostatni rok)
# Dostosowany do technologii Python/FastAPI/Supabase
# Autor: [Twój nick]

param(
    [string]$Since = "1 year ago",
    [int]$Top = 10
)

# Wzorce do wykluczeń – dostosowane do Twojego stacku
$excludePatterns = @(
    '\.yml$', '\.yaml$', '\.toml$',       # configi
    'test', 'spec',                       # testy (będą osobno analizowane)
    '\.md$', 'docs?/',                    # dokumentacja/markdown
    'node_modules', 'dist', 'build',      # build/node
    '\.svg$', '\.png$', '\.jpg$', '\.jpeg$', '\.ico$',  # assety
    '__pycache__', '\.pyc$',              # python cache
    '\.gitignore', '\.env.*'              # ignore/config sensitive
)

# Pobierz listę zmodyfikowanych plików z git log
$files = git log --since="$Since" --pretty=format:"" --name-only --no-merges |
    Where-Object { $_ -ne "" } |
    ForEach-Object { $_.Trim() }

# Filtruj pliki
$filteredFiles = $files | Where-Object {
    $exclude = $false
    foreach ($pattern in $excludePatterns) {
        if ($_ -match $pattern) { $exclude = $true; break }
    }
    -not $exclude
}

# Policz ile razy każdy plik był zmieniany
$stats = $filteredFiles | Group-Object | Sort-Object Count -Descending | Select-Object -First $Top

Write-Host "📊 Top $Top zmienianych plików (od $Since):" -ForegroundColor Cyan
foreach ($s in $stats) {
    "{0,-50} {1,5} changes" -f $s.Name, $s.Count
}

# Sekcja dodatkowa – analiza testów
$testFiles = $files | Where-Object { $_ -match '(test|spec)' }
if ($testFiles) {
    Write-Host "`n🧪 Najczęściej zmieniane pliki testowe:" -ForegroundColor Green
    $testStats = $testFiles | Group-Object | Sort-Object Count -Descending | Select-Object -First 5
    foreach ($s in $testStats) {
        "{0,-50} {1,5} changes" -f $s.Name, $s.Count
    }
}