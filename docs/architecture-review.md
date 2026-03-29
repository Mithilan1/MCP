# Architecture Review

## Current structure

- `app/models.py` defines the habit entity.
- `app/data_store.py` owns JSON persistence.
- `app/service.py` owns business rules and streak logic.
- `app/server.py` handles HTTP routing and static file serving.
- `app/static/` contains the frontend.

## Why this structure works

- Business logic stays out of the HTTP layer, which makes testing easier.
- Persistence details stay out of the UI and routing code.
- The frontend is lightweight and replaceable.
- The project remains small enough for a course assignment while still showing real modularity.

## Improvements already applied

- separated storage from domain logic
- kept streak logic in a pure service layer
- tested service behavior independently from HTTP routing

## Future improvements

- add delete and edit endpoints
- support custom completion dates from the UI
- extract static rendering into templates if the UI grows
- add CLI import and export commands
