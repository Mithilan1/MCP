# HabitFlow

HabitFlow is a small proof-of-concept habit tracker built for Assignment 4. It uses a Python standard-library backend, a static frontend, and unit tests so the whole repo stays easy to run and explain on video.

## What this repo includes

- a small working project
- unit tests
- a PRD and workflow notes
- GitHub issue drafts mapped from the PRD
- Codex and VS Code MCP config files for the assignment walkthrough
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
2. Show `.vscode/mcp.json`, `config-examples/codex-config.toml`, and `scripts/install_codex_vscode_configs.ps1`.
3. Start the app with `python -m app.server`.
4. Open `http://127.0.0.1:8000`.
5. Create a habit and mark it complete.
6. Run the tests.
7. Show the PRD, issue drafts, and checklist in `docs/`.

## Repo structure

```text
app/                  Python backend + static frontend
.claude/skills/       Project-scoped Claude Code skills
.vscode/              VS Code MCP config kept with the project
config-examples/      Copy-paste Codex and Claude Code config examples
docs/                 Assignment evidence and walkthrough material
scripts/              Small setup helpers for the assignment
tests/                Unit tests
data/                 Runtime JSON data file location
```
