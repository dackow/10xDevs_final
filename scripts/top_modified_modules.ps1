<#
.SYNOPSIS
    Analizuje najczęściej zmieniane moduły (katalogi) w repozytorium Git.

.DESCRIPTION
    Ten skrypt PowerShell analizuje historię commitów w repozytorium Git,
    aby zidentyfikować moduły (katalogi), które były najczęściej modyfikowane
    w określonym okresie. Skrypt grupuje zmiany według katalogów najwyższego poziomu,
    pomijając pliki konfiguracyjne, testowe, dokumentację, pliki budowania,
    zasoby statyczne i pliki cache Pythona.

.PARAMETER Since
    Określa okres, od którego mają być analizowane zmiany modułów.
    Akceptuje formaty zrozumiałe dla `git log --since`, np. "1 year ago", "2 months ago", "2023-01-01".
    Domyślna wartość to "1 year ago".

.PARAMETER Top
    Określa liczbę top najczęściej zmienianych modułów do wyświetlenia.
    Domyślna wartość to 10.

.EXAMPLE
    .\top_modified_modules.ps1
    Wyświetla 10 najczęściej zmienianych modułów z ostatniego roku.

.EXAMPLE
    .\top_modified_modules.ps1 -Since "6 months ago" -Top 5
    Wyświetla 5 najczęściej zmienianych modułów z ostatnich 6 miesięcy.

.NOTES
    Wymaga zainstalowanego Git'a i dostępu do repozytorium Git.
    Skrypt ignoruje commity scalające (merge commits).
    Wzorce wykluczeń są dostosowane do projektów Python/FastAPI/Supabase.
    Moduły są identyfikowane na podstawie katalogów najwyższego poziomu.
#>
# top_modified_modules.ps1
# Analiza najczęściej zmienianych modułów (folderów) w repo – ostatni rok
# Dostosowane do Pythona / FastAPI / Supabase

param(
    [string]$Since = "1 year ago",
    [int]$Top = 10
)

# Wzorce wykluczeń – jak w poprzednim pliku
$excludePatterns = @(
    '\.yml$', '\.yaml$', '\.toml$',       # configi
    'test', 'spec',                       # testy
    '\.md$', 'docs?/',                    # dokumentacja
    'node_modules', 'dist', 'build',      # build/node
    '\.svg$', '\.png$', '\.jpg$', '\.jpeg$', '\.ico$',
    '__pycache__', '\.pyc$',              # python cache
    '\.gitignore', '\.env.*'
)

# Pobierz listę zmienionych plików
$files = git log --since="$Since" --pretty=format:"" --name-only --no-merges |
    Where-Object { $_ -ne "" } |
    ForEach-Object { $_.Trim() }

# Filtrowanie
$filteredFiles = $files | Where-Object {
    $exclude = $false
    foreach ($pattern in $excludePatterns) {
        if ($_ -match $pattern) { $exclude = $true; break }
    }
    -not $exclude
}

# Grupowanie po katalogu (modułach)
$modules = $filteredFiles | ForEach-Object {
    if ($_ -match "/") {
        # weź pierwszy poziom folderów (np. app/, tests/, scripts/)
        ($_ -split "/")[0]
    }
    else {
        "project root"
    }
}

# Policz zmiany i zwróć top N
$stats = $modules | Group-Object | Sort-Object Count -Descending | Select-Object -First $Top

Write-Host "📂 Top $Top najczęściej zmienianych modułów (od $Since):" -ForegroundColor Cyan
foreach ($s in $stats) {
    "{0,-20} {1,5} changes" -f $s.Name, $s.Count
}