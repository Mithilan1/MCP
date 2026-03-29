# HabitFlow

HabitFlow is a small proof-of-concept habit tracker built for Assignment 4. It uses a Python standard-library backend, a static frontend, and unit tests so the whole repo stays easy to run and explain on video.

## What this repo includes

- a small working project
- unit tests
- a PRD and workflow notes
- GitHub issue drafts mapped from the PRD
- aligned Codex, Claude Code, and VS Code MCP config files for the assignment walkthrough
- project-scoped Claude Code skills for the required workflow
- assignment setup notes and helper scripts

## Run the project

```powershell
python -m app.server
```

Then open `http://127.0.0.1:8000`.

## Run the tests

```powershell
python -m unittest discover -s tests -v
```

## Suggested demo flow

1. Show the repo structure and assignment docs.
2. Show `.mcp.json`, `.claude/README.md`, `.vscode/mcp.json`, and `config-examples/codex-config.toml`.
3. Optionally show `scripts/install_codex_vscode_configs.ps1` and `scripts/install_claude_skills.ps1`.
4. Start the app with `python -m app.server`.
5. Open `http://127.0.0.1:8000`.
6. Create a habit and mark it complete.
7. Run the tests.
8. Show the PRD, issue drafts, MCP notes, and checklist in `docs/`.

## Repo structure

```text
app/                  Python backend + static frontend
.mcp.json             Project-scoped Claude Code MCP config
.claude/              Claude Code skills, notes, and helper files
.vscode/              VS Code MCP config kept with the project
config-examples/      Copy-paste Codex and Claude Code config examples
docs/                 Assignment evidence and walkthrough material
scripts/              Small setup helpers for the assignment
tests/                Unit tests
data/                 Runtime JSON data file location
```
