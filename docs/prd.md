# Product Requirements Document

## Project

RecallFlow is a tiny missed-appointment follow-up web app for clinics, salons, and service businesses that need a fast way to recover appointments after a customer is 30 minutes late.

## Problem

Missed appointments create empty calendar slots and lost revenue. Staff often notice the late arrival too late, then have to manually decide whether to call or text the customer and how to offer a new time. For this assignment, the goal is a compact proof of concept that demonstrates a clear workflow for flagging late customers, sending a follow-up, and rescheduling them.

## Users

- front-desk staff managing appointment calendars
- coordinators who follow up with customers that miss their slot

## Goals

- create an appointment with customer details and a scheduled time
- identify when an appointment is at least 30 minutes late
- trigger an MCP follow-up by call or text
- let the operator reschedule the missed appointment in the same workflow
- display a lightweight dashboard with totals for late appointments, follow-ups, and reschedules

## Non-goals

- real telecom provider integration
- calendar sync with external scheduling software
- authentication
- advanced analytics or billing

## User stories

- As a front-desk coordinator, I want to add appointments quickly so I can monitor today’s schedule in one place.
- As a coordinator, I want the dashboard to tell me when a customer is 30 minutes late so I know when follow-up should begin.
- As a coordinator, I want to trigger a call or text follow-up with a reschedule option so I can recover the appointment quickly.
- As a coordinator, I want to update the customer to a new slot after follow-up so the queue stays accurate.
- As a user, I want the app to run locally with minimal setup so I can demo it easily.

## Functional requirements

- The system must let users create an appointment with `customer_name`, `phone_number`, `appointment_type`, `scheduled_at`, and `preferred_channel`.
- The system must store appointments locally in a JSON file.
- The system must expose API endpoints for creating appointments, listing appointments, following up on an appointment, and rescheduling it.
- The system must treat an appointment as follow-up eligible once it is 30 minutes late.
- The UI must show a queue of appointments with lateness status, follow-up actions, and reschedule controls.
- The UI must let the user set a reference time so lateness can be demonstrated without waiting in real time.

## Success criteria

- A user can run the project with one Python command.
- The user can create at least one appointment, trigger follow-up, and reschedule it.
- The dashboard updates without a full page reload.
- Unit tests pass locally.

## Constraints

- Use only Python standard-library modules.
- Keep the repo small and easy to review.
- Preserve clear separation between storage, business logic, server routing, and frontend assets.
- Simulate MCP-triggered outreach locally instead of calling real SMS or voice APIs.
