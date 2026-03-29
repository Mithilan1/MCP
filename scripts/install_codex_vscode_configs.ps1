param(
    [string]$Context7ApiKey = ""
)

$repoRoot = Split-Path $PSScriptRoot -Parent
$codexTemplate = Join-Path $repoRoot "config-examples\codex-config.toml"
$vscodeTemplate = Join-Path $repoRoot ".vscode\mcp.json"

$codexTargetDir = Join-Path $HOME ".codex"
$codexTarget = Join-Path $codexTargetDir "config.toml"
$vscodeTargetDir = Join-Path $env:APPDATA "Code\User"
$vscodeTarget = Join-Path $vscodeTargetDir "mcp.json"

function Backup-File {
    param([string]$Path)

    if (-not (Test-Path $Path)) {
        return
    }

    $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
    Copy-Item -LiteralPath $Path -Destination "$Path.assignment4-$timestamp.bak" -Force
}

New-Item -ItemType Directory -Path $codexTargetDir -Force | Out-Null
New-Item -ItemType Directory -Path $vscodeTargetDir -Force | Out-Null

$codexContent = Get-Content -LiteralPath $codexTemplate -Raw
if ($Context7ApiKey) {
    $codexContent = $codexContent.Replace("YOUR_API_KEY", $Context7ApiKey)
}

Backup-File -Path $codexTarget
Set-Content -LiteralPath $codexTarget -Value $codexContent -NoNewline

Backup-File -Path $vscodeTarget
Copy-Item -LiteralPath $vscodeTemplate -Destination $vscodeTarget -Force

Write-Host "Installed Codex config to $codexTarget"
Write-Host "Installed VS Code MCP config to $vscodeTarget"

if (-not $Context7ApiKey) {
    Write-Warning "Codex config still contains the YOUR_API_KEY placeholder. Re-run this script with -Context7ApiKey if you want Context7 ready immediately."
}
