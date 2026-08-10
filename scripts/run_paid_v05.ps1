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
