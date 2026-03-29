$repoRoot = Split-Path $PSScriptRoot -Parent
$projectSkillsRoot = Join-Path $repoRoot ".claude\skills"
$claudeSkillsRoot = Join-Path $HOME ".claude\skills"

if (-not (Test-Path $projectSkillsRoot)) {
    throw "Project Claude skills were not found at $projectSkillsRoot"
}

New-Item -ItemType Directory -Path $claudeSkillsRoot -Force | Out-Null

Get-ChildItem -LiteralPath $projectSkillsRoot -Directory | ForEach-Object {
    $source = $_.FullName
    $destination = Join-Path $claudeSkillsRoot $_.Name

    if (Test-Path $destination) {
        Remove-Item -LiteralPath $destination -Recurse -Force
    }

    Copy-Item -LiteralPath $source -Destination $destination -Recurse -Force
    Write-Host "Installed $($_.Name) to $destination"
}

Write-Host "Claude Code skills copied from the project .claude/skills folder."
Write-Host "Restart Claude Code if it is already open."
