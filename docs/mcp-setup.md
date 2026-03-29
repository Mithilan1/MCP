# MCP Setup Notes

This repo now includes assignment-ready config artifacts for Codex, Claude Code, and VS Code, plus a helper script for installing the Codex and VS Code files onto a Windows machine.

## Verified machine status on 2026-03-29

- Codex CLI is installed.
- VS Code is installed.
- Python and Git are installed.
- The five required skills are present in Codex.
- Node.js is still missing from `PATH`.
- Claude Code CLI is still missing from `PATH`.

## Files included in this repo

- Codex config example: `config-examples/codex-config.toml`
- Claude Code project config example: `config-examples/claude-project.mcp.json`
- VS Code project config: `.vscode/mcp.json`
- Windows copy helper: `scripts/install_codex_vscode_configs.ps1`

## Target paths used on this machine

- Codex: `C:\Users\JT\.codex\config.toml`
- VS Code: `%APPDATA%\Code\User\mcp.json`

## What is ready now

- Context7 is configured as a remote HTTP MCP in both Codex and VS Code configs.
- NotebookLM and Playwright are already defined in the configs so they are ready to start once Node.js is installed.
- The VS Code config stored in this repo uses an input prompt for the Context7 API key so no secret needs to be committed.

## What still depends on Node.js

NotebookLM and Playwright are configured as `npx` servers. The config is ready, but the live demo for those two MCPs still requires a working Node.js installation on the machine where you record the video.

## Recommended video proof

- Show `config-examples/codex-config.toml`.
- Show `.vscode/mcp.json`.
- Show `config-examples/claude-project.mcp.json`.
- Demonstrate Context7 in Codex and VS Code.
- After Node.js is installed, demonstrate NotebookLM and Playwright in the same two tools.

## Fastest path to finish the MCP section

1. Install Node.js.
2. Run `scripts/install_codex_vscode_configs.ps1` if you want to copy the repo configs into the user-level Codex and VS Code locations.
3. Restart Codex and VS Code.
4. Demonstrate Context7, NotebookLM, and Playwright live.
5. Record the screen-share walkthrough.
