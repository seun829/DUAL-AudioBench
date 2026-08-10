param(
    [Parameter(Mandatory = $true)]
    [string[]]$RunSlug
)

& (Join-Path $PSScriptRoot "paid_v04_status.ps1") `
    -RunSlug $RunSlug `
    -ResultsVersion "v05"
