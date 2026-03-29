# Product Requirements Document

## Project

HabitFlow is a tiny habit-tracking web app for students or busy professionals who want a low-friction way to track a few recurring routines.

## Problem

Many habit tools are overloaded with gamification, onboarding, and premium upsells. For this assignment, the goal is a smaller proof of concept that still demonstrates planning, development, testing, and architecture decisions clearly.

## Users

- students managing simple routines like reading, stretching, or study review
- busy professionals tracking a handful of repeatable habits

## Goals

- create habits with a short description
- support daily and weekly habits
- mark a habit complete for the current period
- display a lightweight dashboard with total habits, completions, and streaks
- keep the stack simple enough to explain in a short video

## Non-goals

- authentication
- multi-user collaboration
- reminders and notifications
- complex analytics

## User stories

- As a user, I want to create a habit quickly so I can start tracking without a long setup flow.
- As a user, I want to mark a habit complete so I can see immediate progress.
- As a user, I want to see my streak so I stay motivated.
- As a user, I want the app to run locally with minimal setup so I can demo it easily.

## Functional requirements

- The system must let users create a habit with `name`, `description`, and `frequency`.
- The system must store habits locally in a JSON file.
- The system must expose API endpoints for creating habits, listing habits, and completing habits.
- The UI must show a habit list and summary cards.
- The UI must disable the completion button once the current period is complete.

## Success criteria

- A user can run the project with one Python command.
- The user can create at least one habit and mark it complete.
- The dashboard updates without a full page reload.
- Unit tests pass locally.

## Constraints

- Use only Python standard-library modules.
- Keep the repo small and easy to review.
- Preserve clear separation between storage, business logic, server routing, and frontend assets.
