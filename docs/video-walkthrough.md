# Video Walkthrough Script

## Opening

- State the assignment title and show the GitHub repository.
- Explain that the project is RecallFlow, a small missed-appointment follow-up proof of concept.

## MCP section

- Show `config-examples/codex-config.toml`.
- Show the project Claude config in `.mcp.json`.
- Show the Claude notes in `.claude/README.md`.
- Show `.vscode/mcp.json`.
- Demonstrate Context7 working.
- Demonstrate NotebookLM working.
- Demonstrate Playwright working.

## Skills section

- Show the required skills in the project `.claude/skills/` folder.
- Show the required skills installed in Codex.
- Show the required skills installed in Claude Code if you copied them to user scope.
- Open chat history for each required skill call.
- Point to the PRD, issue drafts, tests, and architecture notes.

## Project demo section

- Run `python -m app.server`.
- Open `http://127.0.0.1:8000`.
- Create an appointment.
- Move the simulation clock so the customer becomes 30 minutes late.
- Trigger an MCP text or call follow-up.
- Reschedule the appointment.
- Run `python -m unittest discover -s tests -v`.

## Closing

- Show the repository URL.
- Show the issues created from the workflow.
- Confirm the final checklist is complete.
