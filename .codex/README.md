# Codex Setup for RecallFlow

This folder keeps a repo-local Codex mirror beside the RecallFlow project.

## What is in this folder

- `.codex/skills/` holds the same five required workflow skills that are also kept in `.claude/skills/`.
- `.codex/.mcp.json` mirrors the project MCP server JSON used elsewhere in the repo.
- `config-examples/codex-config.toml` remains the copy-ready user config template for `~/.codex/config.toml`.
- `scripts/install_codex_vscode_configs.ps1` copies the Codex config example into the default Windows user location.

The five project skills align with Matt Pocock's published `skills` collection:

- `grill-me`
- `write-a-prd`
- `prd-to-issues`
- `tdd`
- `improve-codebase-architecture`

## Codex paths

Use these Codex paths in this repo and on your machine:

- repo mirror: `.codex/skills/` and `.codex/.mcp.json`
- user scope: `~/.codex/skills/` and `~/.codex/config.toml`

## Servers used for RecallFlow

The Codex mirror stays aligned to the same MCP trio used elsewhere in the repo:

- Context7 for current library and framework docs while building the missed-appointment workflow
- NotebookLM for assignment notes, outreach scripts, or operating procedures after Node.js is installed
- Playwright for local browser checks against `http://127.0.0.1:8000`

## Quick start

1. Install Node.js so `npx` is available for NotebookLM and Playwright.
2. Set `CONTEXT7_API_KEY` and `GOOGLE_API_KEY` in your environment if you need those services.
3. Copy `config-examples/codex-config.toml` to `~/.codex/config.toml` if you want a user-scoped Codex setup.
4. If you want the same five skills available in the normal Codex user path, copy `.codex/skills/` into `~/.codex/skills/`.
5. Restart Codex after copying the config or skills.

## Notes

- `.codex/.mcp.json` is kept as a repo-local JSON mirror so the assignment can show matching MCP server definitions beside the Claude files.
- The actual Codex user config file remains TOML at `~/.codex/config.toml`.
- The local web app simulates MCP-triggered call and text follow-up instead of sending real telecom traffic.
