param(
    [Parameter(Mandatory = $true)]
    [string[]]$RunSlug,
    [string]$ResultsVersion = "v04"
)

function Test-RunEvalProcess([int]$ProcessId) {
    $process = Get-CimInstance Win32_Process -Filter "ProcessId = $ProcessId" `
        -ErrorAction SilentlyContinue
    return [bool]($process -and $process.CommandLine -match "run_eval\.py")
}

$workspace = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$rows = foreach ($slug in $RunSlug) {
    $runRoot = Join-Path $workspace "paper_results\$ResultsVersion\raw\$slug"
    $manifestPath = Join-Path $runRoot "launch_manifest.json"
    if (-not (Test-Path -LiteralPath $manifestPath)) {
        [pscustomobject]@{ Run = $slug; Status = "missing" }
        continue
    }
    $manifest = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json
    $outputs = Get-ChildItem -LiteralPath $runRoot -Filter "*.jsonl" -ErrorAction SilentlyContinue
    $attempts = 0
    $completed = 0
    $errors = 0
    $cost = 0.0
    foreach ($output in $outputs) {
        foreach ($line in Get-Content -LiteralPath $output.FullName) {
            if (-not $line.Trim()) { continue }
            $attempts++
            $row = $line | ConvertFrom-Json
            if ($row.error) { $errors++ } else { $completed++ }
            if ($row.api_usage.cost) { $cost += [double]$row.api_usage.cost }
        }
    }
    $live = @($manifest.processes | Where-Object {
        Test-RunEvalProcess -ProcessId $_.pid
    }).Count
    $startedAt = [datetime]::Parse($manifest.started_at).ToUniversalTime()
    $elapsedMinutes = [math]::Max(
        ((Get-Date).ToUniversalTime() - $startedAt).TotalMinutes,
        0.01
    )
    $resumeBaseline = if (
        $manifest.PSObject.Properties.Name -contains "resume_completed_at_start"
    ) { [int]$manifest.resume_completed_at_start } else { 0 }
    $newCompleted = [math]::Max($completed - $resumeBaseline, 0)
    $rate = $newCompleted / $elapsedMinutes
    $etaHours = if ($rate -gt 0) {
        ($manifest.expected_trajectories - $completed) / $rate / 60
    } else { $null }
    $projectedCost = if ($completed -gt 0) {
        $cost / $completed * $manifest.expected_trajectories
    } else { $null }
    [pscustomobject]@{
        Run = $slug
        Model = $manifest.model
        Completed = $completed
        Expected = $manifest.expected_trajectories
        Attempts = $attempts
        Errors = $errors
        CostUSD = [math]::Round($cost, 4)
        ProjectedUSD = if ($projectedCost) {
            [math]::Round($projectedCost, 2)
        } else { $null }
        TrajPerMin = [math]::Round($rate, 2)
        ETAHours = if ($etaHours -ne $null) {
            [math]::Round($etaHours, 2)
        } else { $null }
        LiveShards = $live
    }
}
$rows | Format-Table -AutoSize
