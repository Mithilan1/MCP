# RecallFlow

RecallFlow is a small proof-of-concept dashboard for teams who need to follow up with customers that miss appointments. If a customer is 30 minutes late, the app flags the appointment, lets the operator trigger an MCP follow-up by text or call, and offers a reschedule flow in the same screen.

## What this repo includes

- a small working project
- unit tests
- a PRD and workflow notes
- GitHub issue drafts mapped from the PRD
- aligned Codex, Claude Code, and VS Code MCP config files for the assignment walkthrough
- project-scoped Claude Code skills for the required workflow, aligned to the five Matt Pocock skills used in the assignment
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
3. Start the app with `python -m app.server`.
4. Open `http://127.0.0.1:8000`.
5. Create an appointment that is already more than 30 minutes old, or adjust the simulation clock to make it late.
6. Trigger an MCP text or call follow-up.
7. Reschedule the missed appointment from the dashboard.
8. Run the tests.
9. Show the PRD, issue drafts, MCP notes, and checklist in `docs/`.

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

## Scope note

This local proof of concept simulates the call/text follow-up step inside the dashboard. It does not integrate a real telecom provider.

## Skills note

The five required skills are already available in `.claude/skills/` for Claude Code and are documented in `docs/skills-setup.md`.
