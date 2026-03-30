# Claude Setup for RecallFlow

This folder contains the Claude Code files that sit beside the RecallFlow project.

## What is in this folder

- `.claude/skills/` holds the five required Claude skills as project-scoped skills.
- `.claude/.mcp.json` mirrors the project Claude MCP config for reference.
- `.claude/install-skills.sh` copies the local project skills into `~/.claude/skills` on macOS or Linux.
- `../scripts/install_claude_skills.ps1` does the same copy on Windows.

The five project skills align with Matt Pocock's published `skills` collection:

- `grill-me`
- `write-a-prd`
- `prd-to-issues`
- `tdd`
- `improve-codebase-architecture`

## MCP config paths

Use one of these two Claude MCP paths:

- project scope: `../.mcp.json`
- user scope: `~/.claude/mcp.json`

The repo also keeps `config-examples/claude-project.mcp.json` as a copy-friendly global template.

## Servers used for RecallFlow

All three tool setups in this repo are aligned on the same MCP trio:

- Context7 for current library and framework docs while building the missed-appointment workflow
- NotebookLM for assignment notes, outreach scripts, or operating procedures after Node.js is installed
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

## Running the skills

Claude Code picks up `.claude/skills/` automatically for this project. Invoke a skill in chat with:

```text
/grill-me
/write-a-prd
/prd-to-issues
/tdd
/improve-codebase-architecture
```

If you are working from a VS Code workspace, keep `.vscode/mcp.json` for the MCP servers and run the same skill commands through Claude Code against this repo.

## Skill order for this project

Use the skills in this order when working on RecallFlow:

1. `/grill-me`
2. `/write-a-prd`
3. `/prd-to-issues`
4. `/tdd`
5. `/improve-codebase-architecture`

## Notes

- `.env.example` shows the environment variables used by the MCP setup and other local tooling.
- The repo root `.mcp.json` is the file Claude Code should read for project-scoped MCP servers.
- The local web app simulates MCP-triggered call and text follow-up instead of sending real telecom traffic.
