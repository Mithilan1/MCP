# Workflow Log

This file is meant to support the assignment video and repository narrative.

## Required skill order

1. `grill-me`
2. `write-a-prd`
3. `prd-to-issues`
4. `tdd`
5. `improve-codebase-architecture`

## Suggested story for the demo

### 1. `grill-me`

Use it to challenge the project choice and keep scope tight:

- Why a habit tracker instead of a larger app?
- Why use Python standard library only?
- What is the smallest useful version of the product?

Expected output to show in chat:

- narrowed scope
- project risks
- tradeoff decisions

### 2. `write-a-prd`

Use the final scope to produce the PRD in [docs/prd.md](docs/prd.md).

Expected output to show in chat:

- problem statement
- users
- goals and non-goals
- success criteria

### 3. `prd-to-issues`

Turn the PRD into GitHub issues. Draft issue content is ready in [docs/issues.md](docs/issues.md).

Expected output to show in chat:

- vertical slices
- issue titles
- acceptance criteria

### 4. `tdd`

Show that tests drove the implementation in [tests/test_service.py](../tests/test_service.py) and [tests/test_server.py](../tests/test_server.py).

Expected output to show in chat:

- failing test
- implementation step
- passing test

### 5. `improve-codebase-architecture`

Use it to explain why the codebase is split into store, service, server, and static layers. See [docs/architecture-review.md](docs/architecture-review.md).

Expected output to show in chat:

- modular boundaries
- improved testability
- future extension ideas
