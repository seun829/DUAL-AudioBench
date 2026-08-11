param(
    [Parameter(Mandatory = $true)]
    [string]$ModelId,
    [Parameter(Mandatory = $true)]
    [string]$RunSlug,
    [int]$NumShards = 12,
    [int]$Passes = 2,
    [string]$Conditions = "full_audio,transcript_only,clue_removed,prosody_high,prosody_low,neutral_audio,gap_no_state_change,state_change_short,hidden_user_action",
    [string[]]$ResumeFrom = @()
)

$ErrorActionPreference = "Stop"
$workspace = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$scenarioRoot = Join-Path $workspace "data\scenarios_v05"
$scenarioFiles = @(Get-ChildItem -LiteralPath $scenarioRoot -Filter "*.json" |
    Sort-Object Name)
if ($scenarioFiles.Count -ne 84) {
    throw "Schema-v0.5 requires exactly 84 frozen scenarios; found $($scenarioFiles.Count)."
}
$hashMaterial = ($scenarioFiles | ForEach-Object {
    $_.Name + ":" + (
        Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName
    ).Hash.ToLowerInvariant()
}) -join "`n"
$hashBytes = [Text.Encoding]::UTF8.GetBytes($hashMaterial)
$hasher = [Security.Cryptography.SHA256]::Create()
$scenarioHash = ([BitConverter]::ToString(
    $hasher.ComputeHash($hashBytes)
)).Replace("-", "").ToLowerInvariant()
$hasher.Dispose()
$expectedHash = "e16319a791ab4600f88a33f7957e66eec18be262649caac03845c161119044b9"
if ($scenarioHash -ne $expectedHash) {
    throw "Scenario freeze mismatch: expected $expectedHash, found $scenarioHash."
}

$envFile = Join-Path $workspace ".env"
$hasEnvKey = -not [string]::IsNullOrWhiteSpace($env:OPENROUTER_API_KEY)
$hasFileKey = (Test-Path -LiteralPath $envFile) -and
    [bool](Select-String -LiteralPath $envFile `
        -Pattern '^\s*(OPENROUTER_API_KEY|key)\s*=\s*\S+' -Quiet)
if (-not ($hasEnvKey -or $hasFileKey)) {
    throw "No OpenRouter key is configured in OPENROUTER_API_KEY or .env."
}

$parameters = @{
    ModelId = $ModelId
    RunSlug = $RunSlug
    NumShards = $NumShards
    Passes = $Passes
    Conditions = $Conditions
    ResumeFrom = $ResumeFrom
    SchemaVersion = "0.5"
    Scenarios = "data/scenarios_v05"
    ResultsVersion = "v05"
}
& (Join-Path $PSScriptRoot "run_paid_v04.ps1") @parameters
