# MCP Setup Notes

This repo now keeps the RecallFlow MCP story aligned across Codex, Claude Code, and VS Code.

## Verified machine status on 2026-03-29

- Codex CLI is installed.
- VS Code is installed.
- Python and Git are installed.
- The five required skills are present in the repo under `.claude/skills/`.
- A Claude executable exists locally, but `claude` is still not on `PATH`.
- Node.js is still missing from `PATH`.

## Files included in this repo

- Codex config example: `config-examples/codex-config.toml`
- Claude project MCP config: `.mcp.json`
- Claude global MCP template: `config-examples/claude-project.mcp.json`
- Claude folder mirror and notes: `.claude/.mcp.json` and `.claude/README.md`
- VS Code project config: `.vscode/mcp.json`
- Windows MCP install helper: `scripts/install_codex_vscode_configs.ps1`

## Server alignment across tools

All three clients point at the same MCP trio:

- Context7 as an HTTP MCP for current docs
- NotebookLM through `npx` once Node.js is installed
- Playwright through `npx` in headless mode for local UI checks

## RecallFlow use cases

- Context7: pull up-to-date docs while changing the late-appointment workflow
- NotebookLM: query assignment notes, outreach language, or operating procedures
- Playwright: verify the local RecallFlow UI at `http://127.0.0.1:8000`

## Scope note

The local app simulates MCP-triggered call and text follow-up inside the dashboard. Real telecom delivery is intentionally out of scope for this assignment proof of concept.

## Target paths used on this machine

- Codex: `C:\Users\JT\.codex\config.toml`
- Claude global: `C:\Users\JT\.claude\mcp.json`
- VS Code: `%APPDATA%\Code\User\mcp.json`

## What is ready now

- The repo root `.mcp.json` is ready for project-scoped Claude Code use.
- The VS Code config is ready to copy into the VS Code user MCP location.
- The Codex config example uses the same three MCP servers as the Claude and VS Code configs.
- `.env.example` documents the environment variables used by the setup.

## What still depends on Node.js

NotebookLM and Playwright are configured through `npx`. The config is ready, but the live demo for those two MCPs still requires a working Node.js installation on the machine where you record the video.

## Recommended setup steps

1. Install Node.js.
2. Set `CONTEXT7_API_KEY` and `GOOGLE_API_KEY` in your environment if you need those services.
3. Open this repo in Claude Code so it picks up the project `.mcp.json`.
4. Run `scripts/install_codex_vscode_configs.ps1 -InstallClaudeGlobal` if you also want user-level Codex, Claude, and VS Code configs copied into their default locations.
5. Restart Codex, Claude Code, and VS Code.

## Recommended video proof

- Show `config-examples/codex-config.toml`.
- Show `.mcp.json`.
- Show `.claude/README.md`.
- Show `.vscode/mcp.json`.
- Demonstrate Context7, NotebookLM, and Playwright against RecallFlow after Node.js is installed.
