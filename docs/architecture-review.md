# Architecture Review

## Current structure

- `app/models.py` defines the appointment entity and activity log shape.
- `app/data_store.py` owns JSON persistence.
- `app/service.py` owns lateness detection, follow-up rules, and rescheduling logic.
- `app/server.py` handles HTTP routing and static file serving.
- `app/static/` contains the frontend.

## Why this structure works

- Business rules for the 30-minute late threshold stay out of the HTTP layer, which keeps the tests focused.
- Persistence details stay out of the UI and routing code.
- The frontend remains lightweight and replaceable.
- The project stays small enough for a course assignment while still showing a realistic missed-appointment recovery workflow.

## Improvements already applied

- separated storage from domain logic
- kept late-detection and follow-up logic in a pure service layer
- tested service behavior independently from HTTP routing

## Future improvements

- integrate a real SMS or voice provider
- add staff notes and outcome tracking for failed outreach attempts
- sync appointments with an external scheduling system
- add filters for location, provider, or day
