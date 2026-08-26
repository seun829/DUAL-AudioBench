param(
    [string[]]$RunSlug = @(
        "gemini25_headline",
        "gemini3_headline",
        "gemini25_controls",
        "gemini3_controls"
    ),
    [string]$ReportName = "headline_and_controls",
    [int]$PollSeconds = 60
)

$ErrorActionPreference = "Stop"
$workspace = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$watchRoot = Join-Path $workspace "paper_results\v04\watch"
New-Item -ItemType Directory -Force -Path $watchRoot | Out-Null
$heartbeat = Join-Path $watchRoot "status.json"

function Test-RunEvalProcess([int]$ProcessId) {
    $process = Get-CimInstance Win32_Process -Filter "ProcessId = $ProcessId" `
        -ErrorAction SilentlyContinue
    return [bool]($process -and $process.CommandLine -match "run_eval\.py")
}

while ($true) {
    $live = 0
    $processes = @()
    foreach ($slug in $RunSlug) {
        $manifest = Get-Content -Raw -LiteralPath (
            Join-Path $workspace "paper_results\v04\raw\$slug\launch_manifest.json"
        ) | ConvertFrom-Json
        foreach ($entry in $manifest.processes) {
            if (Test-RunEvalProcess -ProcessId $entry.pid) {
                $live++
                $processes += [ordered]@{ run = $slug; pid = $entry.pid }
            }
        }
    }
    $state = [ordered]@{
        checked_at = (Get-Date).ToUniversalTime().ToString("o")
        live_shards = $live
        runs = $RunSlug
        processes = $processes
    }
    [IO.File]::WriteAllText(
        $heartbeat,
        ($state | ConvertTo-Json -Depth 5) + "`n",
        [Text.UTF8Encoding]::new($false)
    )
    if ($live -eq 0) { break }
    Start-Sleep -Seconds $PollSeconds
}

& (Join-Path $PSScriptRoot "finalize_paid_v04.ps1") `
    -RunSlug $RunSlug `
    -ReportName $ReportName

$state["finalized_at"] = (Get-Date).ToUniversalTime().ToString("o")
$state["report_directory"] = Join-Path $workspace (
    "paper_results\v04\reports\$ReportName"
)
[IO.File]::WriteAllText(
    $heartbeat,
    ($state | ConvertTo-Json -Depth 5) + "`n",
    [Text.UTF8Encoding]::new($false)
)
