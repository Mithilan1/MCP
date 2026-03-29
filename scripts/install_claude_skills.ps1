$requiredSkills = @(
    "grill-me",
    "write-a-prd",
    "prd-to-issues",
    "tdd",
    "improve-codebase-architecture"
)

$codexSkillsRoot = Join-Path $HOME ".codex\skills"
$claudeSkillsRoot = Join-Path $HOME ".claude\skills"

New-Item -ItemType Directory -Path $claudeSkillsRoot -Force | Out-Null

foreach ($skill in $requiredSkills) {
    $source = Join-Path $codexSkillsRoot $skill
    $destination = Join-Path $claudeSkillsRoot $skill

    if (-not (Test-Path $source)) {
        Write-Warning "Skipping $skill because it was not found in $codexSkillsRoot"
        continue
    }

    if (Test-Path $destination) {
        Remove-Item -LiteralPath $destination -Recurse -Force
    }

    Copy-Item -LiteralPath $source -Destination $destination -Recurse -Force
    Write-Host "Installed $skill to $destination"
}

Write-Host "Claude Code skills copied. Restart Claude Code if it is already open."
