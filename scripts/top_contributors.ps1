<#
.SYNOPSIS
    Analizuje top kontrybutorów w repozytorium Git na podstawie liczby commitów.

.DESCRIPTION
    Ten skrypt PowerShell pobiera historię commitów z bieżącego repozytorium Git
    i identyfikuje najbardziej aktywnych kontrybutorów w określonym okresie.
    Wyniki są sortowane malejąco według liczby commitów, a następnie wyświetlane
    wraz z imieniem i adresem e-mail kontrybutora.

.PARAMETER Since
    Określa okres, od którego mają być analizowane commity.
    Akceptuje formaty zrozumiałe dla `git log --since`, np. "1 year ago", "2 months ago", "2023-01-01".
    Domyślna wartość to "1 year ago".

.PARAMETER Top
    Określa liczbę top kontrybutorów do wyświetlenia.
    Domyślna wartość to 5.

.EXAMPLE
    .\top_contributors.ps1
    Wyświetla 5 top kontrybutorów z ostatniego roku.

.EXAMPLE
    .\top_contributors.ps1 -Since "3 months ago" -Top 10
    Wyświetla 10 top kontrybutorów z ostatnich 3 miesięcy.

.NOTES
    Wymaga zainstalowanego Git'a i dostępu do repozytorium Git.
    Skrypt ignoruje commity scalające (merge commits).
#> 
# top_contributors.ps1
# Analiza top kontrybutorów w repo (ostatni rok)

param(
    [string]$Since = "1 year ago",
    [int]$Top = 5
)

# Pobierz autorów commitów (imię + email)
$authors = git log --since="$Since" --pretty=format:"%an <%ae>" --no-merges |
    Where-Object { $_ -ne "" } |
    ForEach-Object { $_.Trim() }

# Policz commity na autora
$stats = $authors | Group-Object | Sort-Object Count -Descending | Select-Object -First $Top

Write-Host "👥 Top $Top kontrybutorów (od $Since):" -ForegroundColor Cyan
foreach ($s in $stats) {
    "{0,-30} {1,5} commits" -f $s.Name, $s.Count
}