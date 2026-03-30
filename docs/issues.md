# GitHub Issue Drafts

Paste these into your separate GitHub repository as real issues so the repo matches the assignment requirement.

## Issue 1: Bootstrap RecallFlow and define the appointment model

Create the initial Python project structure for RecallFlow.

Acceptance criteria:

- `app/`, `tests/`, and `docs/` folders exist
- an `Appointment` model exists with customer details, scheduled time, and follow-up preferences
- a JSON persistence path is defined
- README includes run and test instructions

## Issue 2: Build late-detection and follow-up service logic

Implement business logic for creating appointments, detecting 30-minute lateness, sending follow-up actions, and rescheduling.

Acceptance criteria:

- appointments can be created and saved locally
- appointments become follow-up eligible at 30 minutes late
- follow-up actions record whether the outreach was by text or call
- rescheduling updates the appointment slot after follow-up
- service tests cover the main workflows

## Issue 3: Expose API endpoints and the missed-appointment dashboard

Add the HTTP layer and a simple browser UI.

Acceptance criteria:

- the project serves a home page
- `/api/health` returns success
- users can create appointments from the UI
- users can trigger a call or text follow-up from the UI
- users can reschedule an appointment from the UI
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
