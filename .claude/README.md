# Claude Setup for HabitFlow

This folder contains the Claude Code files that sit beside the HabitFlow project.

## What is in this folder

- `.claude/skills/` holds the five required Claude skills as project-scoped skills.
- `.claude/.mcp.json` mirrors the project Claude MCP config for reference.
- `.claude/install-skills.sh` copies the local project skills into `~/.claude/skills` on macOS or Linux.
- `../scripts/install_claude_skills.ps1` does the same copy on Windows.

## MCP config paths

Use one of these two Claude MCP paths:

- project scope: `../.mcp.json`
- user scope: `~/.claude/mcp.json`

The repo also keeps `config-examples/claude-project.mcp.json` as a copy-friendly global template.

## Servers used for HabitFlow

All three tool setups in this repo are aligned on the same MCP trio:

- Context7 for current library and framework docs while building HabitFlow
- NotebookLM for assignment notes or outside research after Node.js is installed
- Playwright for local browser checks against `http://127.0.0.1:8000`

## Quick start

1. Install Node.js so `npx` is available for NotebookLM and Playwright.
2. Set `CONTEXT7_API_KEY` and `GOOGLE_API_KEY` in your environment if you need those services.
3. Open this repo in Claude Code. The root `.mcp.json` and project `.claude/skills/` folder are ready to use.
4. If you also want a user-scoped Claude setup, copy `config-examples/claude-project.mcp.json` to `~/.claude/mcp.json`.
5. If you want user-scoped skills too, run one of these helpers:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_claude_skills.ps1
```

```bash
bash ./.claude/install-skills.sh
```

## Skill order for this project

Use the skills in this order when working on HabitFlow:

1. `/grill-me`
2. `/write-a-prd`
3. `/prd-to-issues`
4. `/tdd`
5. `/improve-codebase-architecture`

## Notes

- `.env.example` shows the environment variables used by the MCP setup and other local tooling.
- The repo root `.mcp.json` is the file Claude Code should read for project-scoped MCP servers.
- VS Code and Codex use their own aligned configs in `.vscode/mcp.json` and `config-examples/codex-config.toml`.
