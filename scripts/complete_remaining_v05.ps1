param(
    [int]$NumShards = 12,
    [int]$MaxResumeRounds = 4,
    [int]$PollSeconds = 30
)

$ErrorActionPreference = "Stop"
$workspace = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$resultsRoot = Join-Path $workspace "paper_results\v05\raw"

if ([string]::IsNullOrWhiteSpace($env:OPENROUTER_API_KEY)) {
    throw "OPENROUTER_API_KEY must be supplied through the process environment."
}

function Get-RunRoot([string]$RunSlug) {
    return Join-Path $resultsRoot $RunSlug
}

function Get-Manifest([string]$RunSlug) {
    $path = Join-Path (Get-RunRoot $RunSlug) "launch_manifest.json"
    if (-not (Test-Path -LiteralPath $path)) { return $null }
    return Get-Content -Raw -LiteralPath $path | ConvertFrom-Json
}

function Get-LiveShardCount([string]$RunSlug) {
    $manifest = Get-Manifest $RunSlug
    if (-not $manifest) { return 0 }
    $live = 0
    foreach ($processInfo in $manifest.processes) {
        $process = Get-CimInstance Win32_Process `
            -Filter "ProcessId = $($processInfo.pid)" `
            -ErrorAction SilentlyContinue
        if ($process -and $process.CommandLine -match "run_eval\.py") {
            $live++
        }
    }
    return $live
}

function Get-RunProgress([string]$RunSlug) {
    $manifest = Get-Manifest $RunSlug
    $keys = [Collections.Generic.HashSet[string]]::new()
    $attempts = 0
    $errors = 0
    $cost = 0.0
    $root = Get-RunRoot $RunSlug
    if (Test-Path -LiteralPath $root) {
        foreach ($file in Get-ChildItem -LiteralPath $root -Filter "*.jsonl") {
            foreach ($line in Get-Content -LiteralPath $file.FullName) {
                if (-not $line.Trim()) { continue }
                $attempts++
                $row = $line | ConvertFrom-Json
                if ($row.api_usage.cost) { $cost += [double]$row.api_usage.cost }
                if ($row.error) {
                    $errors++
                    continue
                }
                [void]$keys.Add(
                    "$($row.scenario_id)|$($row.condition)|$($row.seed)"
                )
            }
        }
    }
    return [pscustomobject]@{
        Completed = $keys.Count
        Expected = if ($manifest) { [int]$manifest.expected_trajectories } else { 0 }
        Attempts = $attempts
        Errors = $errors
        Cost = $cost
    }
}

function Get-RemainingCredit {
    $headers = @{ Authorization = "Bearer $env:OPENROUTER_API_KEY" }
    $response = Invoke-RestMethod `
        -Uri "https://openrouter.ai/api/v1/key" `
        -Headers $headers `
        -Method Get
    return [double]$response.data.limit_remaining
}

function Start-Run(
    [string]$ModelId,
    [string]$RunSlug,
    [string]$Conditions
) {
    $root = Get-RunRoot $RunSlug
    $resume = @()
    if (Test-Path -LiteralPath $root) {
        $resume = @(
            Get-ChildItem -LiteralPath $root -Filter "*.jsonl" |
                Select-Object -ExpandProperty FullName
        )
    }
    $parameters = @{
        ModelId = $ModelId
        RunSlug = $RunSlug
        NumShards = $NumShards
        Passes = 2
        Conditions = $Conditions
    }
    if ($resume.Count) { $parameters.ResumeFrom = $resume }
    & (Join-Path $PSScriptRoot "run_paid_v05.ps1") @parameters | Out-Null
}

function Complete-Run(
    [string]$ModelId,
    [string]$RunSlug,
    [string]$Conditions
) {
    $resumeRound = 0
    while ($true) {
        $progress = Get-RunProgress $RunSlug
        $live = Get-LiveShardCount $RunSlug
        $now = (Get-Date).ToUniversalTime().ToString("o")
        Write-Output (
            "$now run=$RunSlug completed=$($progress.Completed)/" +
            "$($progress.Expected) attempts=$($progress.Attempts) " +
            "errors=$($progress.Errors) live=$live " +
            "cost=$([math]::Round($progress.Cost, 4))"
        )
        if ($progress.Expected -gt 0 -and
            $progress.Completed -ge $progress.Expected) {
            return
        }
        if ($live -gt 0) {
            Start-Sleep -Seconds $PollSeconds
            continue
        }
        $remaining = Get-RemainingCredit
        if ($remaining -lt 0.50) {
            throw "Less than 0.50 USD credit remains; stopping before another retry round."
        }
        if ($resumeRound -ge $MaxResumeRounds) {
            throw "$RunSlug remains incomplete after $MaxResumeRounds resume rounds."
        }
        $resumeRound++
        Write-Output (
            "Relaunching $RunSlug round=$resumeRound; " +
            "credit_remaining=$([math]::Round($remaining, 2))"
        )
        Start-Run $ModelId $RunSlug $Conditions
        Start-Sleep -Seconds 2
    }
}

$env:OPENROUTER_ATTEMPTS = "6"

$stages = @(
    @{
        Model = "google/gemini-2.5-flash"
        Run = "gemini25_remaining_v05"
        Conditions = "gap_no_state_change,state_change_short,hidden_user_action,neutral_audio,prosody_high,prosody_low"
    },
    @{
        Model = "openai/gpt-audio-mini"
        Run = "gpt_audio_mini_remaining_v05"
        Conditions = "gap_no_state_change,state_change_short,hidden_user_action,neutral_audio,prosody_high,prosody_low"
    },
    @{
        Model = "google/gemini-3-flash-preview"
        Run = "gemini3_priority"
        Conditions = "full_audio,clue_removed,transcript_only"
    },
    @{
        Model = "google/gemini-3-flash-preview"
        Run = "gemini3_controls_v05"
        Conditions = "gap_no_state_change,state_change_short,hidden_user_action,neutral_audio"
    },
    @{
        Model = "google/gemini-3-flash-preview"
        Run = "gemini3_prosody_v05"
        Conditions = "prosody_high,prosody_low"
    }
)

foreach ($stage in $stages) {
    Complete-Run $stage.Model $stage.Run $stage.Conditions
}

& (Join-Path $PSScriptRoot "finalize_paid_v05.ps1") `
    -RunSlug @(
        "gemini25_priority",
        "gemini25_remaining_v05",
        "gpt_audio_mini_causal",
        "gpt_audio_mini_remaining_v05",
        "gemini3_priority",
        "gemini3_controls_v05",
        "gemini3_prosody_v05"
    ) `
    -ReportName "complete"

Write-Output "COMPLETE: finalized paper_results/v05/reports/complete"
