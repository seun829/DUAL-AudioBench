param(
    [string[]]$RunSlug = @("gemini25_main", "gemini3_main"),
    [string]$ReportName = "main"
)

& (Join-Path $PSScriptRoot "finalize_paid_v04.ps1") `
    -RunSlug $RunSlug `
    -ReportName $ReportName `
    -ResultsVersion "v05"
