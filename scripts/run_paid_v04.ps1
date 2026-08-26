param(
    [Parameter(Mandatory = $true)]
    [string]$ModelId,

    [Parameter(Mandatory = $true)]
    [string]$RunSlug,

    [int]$NumShards = 6,
    [int]$Passes = 2,
    [string]$Conditions = "full_audio,transcript_only,clue_removed,prosody_high,prosody_low",
    [string[]]$ResumeFrom = @(),
    [string]$SchemaVersion = "0.4",
    [string]$Scenarios = "data/scenarios_v04",
    [string]$ResultsVersion = "v04"
)

$ErrorActionPreference = "Stop"
$workspace = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$python = (Get-Command python).Source

if (-not $env:ESPEAK_NG_BIN) {
    $env:ESPEAK_NG_BIN = (
        Resolve-Path (Join-Path $workspace ".tools\espeak-ng\SourceDir\eSpeak NG\espeak-ng.exe")
    ).Path
}
if (-not $env:ESPEAK_NG_DATA_DIR) {
    $env:ESPEAK_NG_DATA_DIR = Split-Path $env:ESPEAK_NG_BIN -Parent
}
if (-not $env:FFMPEG_BIN) {
    $ffmpeg = Get-ChildItem (
        Join-Path $env:LOCALAPPDATA "Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_*"
    ) -Recurse -Filter "ffmpeg.exe" | Select-Object -First 1
    if (-not $ffmpeg) {
        throw "ffmpeg.exe was not found; set FFMPEG_BIN explicitly."
    }
    $env:FFMPEG_BIN = $ffmpeg.FullName
}

$env:OPENROUTER_MODEL = $ModelId
$scenarioRoot = Join-Path $workspace $Scenarios
$scenarioFiles = @(Get-ChildItem -LiteralPath $scenarioRoot -Filter "*.json" |
    Sort-Object Name)
$scenarioCount = $scenarioFiles.Count
if (-not $scenarioCount) { throw "No scenarios found in $scenarioRoot" }
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
$runRoot = Join-Path $workspace "paper_results\$ResultsVersion\raw\$RunSlug"
$logRoot = Join-Path $runRoot "logs"
New-Item -ItemType Directory -Force -Path $runRoot, $logRoot | Out-Null

$resumeKeys = [Collections.Generic.HashSet[string]]::new()
foreach ($resumePath in $ResumeFrom) {
    if (-not (Test-Path -LiteralPath $resumePath)) { continue }
    foreach ($line in Get-Content -LiteralPath $resumePath) {
        if (-not $line.Trim()) { continue }
        $row = $line | ConvertFrom-Json
        if (-not $row.error) {
            [void]$resumeKeys.Add(
                "$($row.scenario_id)|$($row.condition)|$($row.seed)"
            )
        }
    }
}

$started = @()
for ($shard = 0; $shard -lt $NumShards; $shard++) {
    $tag = "shard{0:d2}-of-{1:d2}" -f $shard, $NumShards
    $output = Join-Path $runRoot "$RunSlug`_$tag.jsonl"
    $env:OPENROUTER_USAGE_PATH = Join-Path $runRoot "$RunSlug`_$tag`_usage.json"
    $stdout = Join-Path $logRoot "$tag.out.log"
    $stderr = Join-Path $logRoot "$tag.err.log"
    $arguments = @(
        "run_eval.py",
        "--model", "openrouter",
        "--scenarios", $Scenarios,
        "--conditions", $Conditions,
        "--passes", "$Passes",
        "--num-shards", "$NumShards",
        "--shard-index", "$shard",
        "--out", $output,
        "--rate-limit-seconds", "0"
    )
    if ($ResumeFrom.Count) {
        $arguments += "--resume-from"
        $arguments += $ResumeFrom
    }
    $process = Start-Process -FilePath $python `
        -ArgumentList $arguments `
        -WorkingDirectory $workspace `
        -RedirectStandardOutput $stdout `
        -RedirectStandardError $stderr `
        -WindowStyle Hidden `
        -PassThru
    $started += [ordered]@{
        shard = $shard
        pid = $process.Id
        output = $output
        stdout = $stdout
        stderr = $stderr
    }
}

$manifest = [ordered]@{
    schema_version = $SchemaVersion
    model = $ModelId
    run_slug = $RunSlug
    conditions = $Conditions.Split(",")
    passes = $Passes
    shards = $NumShards
    expected_trajectories = $scenarioCount * $Conditions.Split(",").Count * $Passes
    scenario_root = $Scenarios
    scenario_files = $scenarioCount
    scenario_manifest_sha256 = $scenarioHash
    resume_from = $ResumeFrom
    resume_completed_at_start = $resumeKeys.Count
    started_at = (Get-Date).ToUniversalTime().ToString("o")
    processes = $started
}
$manifestPath = Join-Path $runRoot "launch_manifest.json"
$manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $manifestPath -Encoding utf8
$manifest | ConvertTo-Json -Depth 5
