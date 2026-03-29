# GitHub Issue Drafts

Paste these into your separate GitHub repository as real issues so the repo matches the assignment requirement.

## Issue 1: Bootstrap HabitFlow and define the core data model

Create the initial Python project structure for HabitFlow.

Acceptance criteria:

- `app/`, `tests/`, and `docs/` folders exist
- a `Habit` model exists with daily and weekly frequency support
- JSON persistence path is defined
- README includes run and test instructions

## Issue 2: Build the habit service and local persistence workflow

Implement business logic for creating habits, listing them, and completing them.

Acceptance criteria:

- habits can be created and saved locally
- duplicate completion for the same period is ignored
- streak calculation works for daily and weekly habits
- service tests cover the main workflows

## Issue 3: Expose API endpoints and a lightweight frontend

Add the HTTP layer and a simple browser UI.

Acceptance criteria:

- the project serves a home page
- `/api/health` returns success
- users can create habits from the UI
- users can mark a habit complete from the UI
- dashboard cards update after user actions

## Issue 4: Add test coverage and tighten the demo story

Strengthen verification and make the repo easier to review.

Acceptance criteria:

- server tests cover happy-path and invalid requests
- README includes a suggested demo flow
- docs explain how the project maps to the required skill order

## Issue 5: Improve architecture and prepare assignment evidence

Document the architectural split and the assignment checklist.

Acceptance criteria:

- architecture review exists in `docs/`
- assignment checklist exists in `docs/`
- MCP and skills setup notes exist in `docs/`
