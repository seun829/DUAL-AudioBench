param(
    [string[]]$RunSlug = @("gemini25_headline", "gemini3_headline"),
    [string]$ReportName = "headline",
    [string]$ResultsVersion = "v04"
)

$ErrorActionPreference = "Stop"
$workspace = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$reportRoot = Join-Path $workspace "paper_results\$ResultsVersion\reports\$ReportName"
New-Item -ItemType Directory -Force -Path $reportRoot | Out-Null
$allSuccessful = @()

function Test-RunEvalProcess([int]$ProcessId) {
    $process = Get-CimInstance Win32_Process -Filter "ProcessId = $ProcessId" `
        -ErrorAction SilentlyContinue
    return [bool]($process -and $process.CommandLine -match "run_eval\.py")
}

foreach ($slug in $RunSlug) {
    $runRoot = Join-Path $workspace "paper_results\$ResultsVersion\raw\$slug"
    $manifest = Get-Content -Raw -LiteralPath (
        Join-Path $runRoot "launch_manifest.json"
    ) | ConvertFrom-Json
    $live = @($manifest.processes | Where-Object {
        Test-RunEvalProcess -ProcessId $_.pid
    }).Count
    if ($live) { throw "$slug still has $live live shard process(es)." }

    $shards = Get-ChildItem -LiteralPath $runRoot -Filter "*_shard*.jsonl" |
        Sort-Object Name
    $rows = foreach ($file in $shards) {
        foreach ($line in Get-Content -LiteralPath $file.FullName) {
            if ($line.Trim()) { $line | ConvertFrom-Json }
        }
    }
    $successful = @($rows | Where-Object {-not $_.error})
    $keys = @($successful | ForEach-Object {
        "$($_.model)|$($_.scenario_id)|$($_.condition)|$($_.seed)"
    })
    $unique = @($keys | Sort-Object -Unique)
    if ($successful.Count -ne $unique.Count) {
        throw "$slug contains duplicate successful trajectory keys."
    }
    if ($successful.Count -ne [int]$manifest.expected_trajectories) {
        throw "$slug has $($successful.Count)/$($manifest.expected_trajectories) completed rows. Relaunch it to resume."
    }

    $allSuccessful += $successful
}

$modelFiles = @()
foreach ($group in ($allSuccessful | Group-Object model)) {
    $slug = ($group.Name -replace "[^A-Za-z0-9._-]", "_")
    $combined = Join-Path $reportRoot "$slug.jsonl"
    $keys = @($group.Group | ForEach-Object {
        "$($_.scenario_id)|$($_.condition)|$($_.seed)"
    })
    if (@($keys | Sort-Object -Unique).Count -ne $keys.Count) {
        throw "$($group.Name) has duplicate successful keys across run groups."
    }
    $jsonLines = @($group.Group | Sort-Object scenario_id, condition, seed |
        ForEach-Object { $_ | ConvertTo-Json -Depth 100 -Compress })
    [IO.File]::WriteAllLines(
        $combined,
        $jsonLines,
        [Text.UTF8Encoding]::new($false)
    )
    $modelFiles += $combined
}

python (Join-Path $workspace "report_results.py") @modelFiles `
    --out-dir $reportRoot
if ($LASTEXITCODE -ne 0) { throw "report_results.py failed." }

foreach ($combined in $modelFiles) {
    $prefix = Join-Path $reportRoot ([IO.Path]::GetFileNameWithoutExtension($combined))
    python (Join-Path $workspace "analyze_pilot.py") $combined --prefix $prefix
    if ($LASTEXITCODE -ne 0) { throw "analyze_pilot.py failed for $combined." }
}

Write-Output "Finalized readable reports in $reportRoot"
