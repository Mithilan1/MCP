param(
    [string]$Context7ApiKey = "",
    [switch]$InstallClaudeGlobal
)

$repoRoot = Split-Path $PSScriptRoot -Parent
$codexTemplate = Join-Path $repoRoot "config-examples\codex-config.toml"
$vscodeTemplate = Join-Path $repoRoot ".vscode\mcp.json"
$claudeTemplate = Join-Path $repoRoot "config-examples\claude-project.mcp.json"

$codexTargetDir = Join-Path $HOME ".codex"
$codexTarget = Join-Path $codexTargetDir "config.toml"
$vscodeTargetDir = Join-Path $env:APPDATA "Code\User"
$vscodeTarget = Join-Path $vscodeTargetDir "mcp.json"
$claudeTargetDir = Join-Path $HOME ".claude"
$claudeTarget = Join-Path $claudeTargetDir "mcp.json"

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
    $codexContent = $codexContent.Replace("YOUR_CONTEXT7_API_KEY", $Context7ApiKey)
}

Backup-File -Path $codexTarget
Set-Content -LiteralPath $codexTarget -Value $codexContent -NoNewline

Backup-File -Path $vscodeTarget
Copy-Item -LiteralPath $vscodeTemplate -Destination $vscodeTarget -Force

if ($InstallClaudeGlobal) {
    New-Item -ItemType Directory -Path $claudeTargetDir -Force | Out-Null
    Backup-File -Path $claudeTarget
    Copy-Item -LiteralPath $claudeTemplate -Destination $claudeTarget -Force
}

Write-Host "Installed Codex config to $codexTarget"
Write-Host "Installed VS Code MCP config to $vscodeTarget"

if (-not $Context7ApiKey) {
    Write-Warning "Codex config still contains the YOUR_CONTEXT7_API_KEY placeholder. Re-run this script with -Context7ApiKey if you want Context7 ready immediately."
}

if ($InstallClaudeGlobal) {
    Write-Host "Installed Claude global MCP config to $claudeTarget"
} else {
    Write-Host "Skipped Claude global MCP install. The repo root .mcp.json is already ready for project-scoped Claude Code use."
}

Write-Host "Set CONTEXT7_API_KEY and GOOGLE_API_KEY in your environment before launching clients if you want Context7 and NotebookLM ready immediately."
