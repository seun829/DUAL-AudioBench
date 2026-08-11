param(
    [string[]]$RunSlug = @("gemini25_main", "gpt_audio_mini_main"),
    [string]$ReportName = "main"
)

$workspace = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$expectedHash = "e16319a791ab4600f88a33f7957e66eec18be262649caac03845c161119044b9"
foreach ($slug in $RunSlug) {
    $manifestPath = Join-Path $workspace (
        "paper_results\v05\raw\$slug\launch_manifest.json"
    )
    if (-not (Test-Path -LiteralPath $manifestPath)) {
        throw "Missing launch manifest for $slug."
    }
    $manifest = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json
    if ($manifest.scenario_manifest_sha256 -ne $expectedHash) {
        throw "$slug used scenario hash $($manifest.scenario_manifest_sha256), expected $expectedHash."
    }
}

& (Join-Path $PSScriptRoot "finalize_paid_v04.ps1") `
    -RunSlug $RunSlug `
    -ReportName $ReportName `
    -ResultsVersion "v05"
