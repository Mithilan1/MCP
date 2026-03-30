# Skills Setup Notes

## Current status on 2026-03-29

- The five required skills are already present in this repo under `.claude/skills/`.
- Codex also has the same five skills available locally.
- Claude Code can use the project-scoped `.claude/skills/` folder as soon as this repo is opened there.

## Canonical skill source in this repo

Treat the project `.claude/skills/` directory as the source of truth for the Claude side of the assignment:

- `grill-me`
- `write-a-prd`
- `prd-to-issues`
- `tdd`
- `improve-codebase-architecture`

## Claude Code path rules

Claude supports both of these paths:

- user scope: `~/.claude/skills/<skill-name>/SKILL.md`
- project scope: `.claude/skills/<skill-name>/SKILL.md`

That means you have two valid ways to show Claude skills:

- open this RecallFlow repo in Claude Code and use the project-scoped `.claude/skills/` folder
- copy the same local project skills into `~/.claude/skills/` for a user-scoped setup

## Ready-to-use copy helpers

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_claude_skills.ps1
```

macOS/Linux:

```bash
bash ./.claude/install-skills.sh
```

Both helpers copy the local project `.claude/skills/` folder into `~/.claude/skills/`.

## What to show in your video

- the project `.claude/skills/` folder in this repo
- optionally the user-scoped `~/.claude/skills/` folder after copying
- the Codex skills list if you want to show the same workflow in Codex too
- your chat history for each required skill call in the required order

## Suggested prompts for the required skill order

### `grill-me`

```text
Use grill-me on RecallFlow, a tiny Python-only dashboard for following up with customers who are 30 minutes late for appointments. Push back on anything too large or unclear.
```

### `write-a-prd`

```text
Use write-a-prd for RecallFlow, a small missed-appointment follow-up tool with a local JSON store, simulated MCP call or text outreach, and a reschedule flow.
```

### `prd-to-issues`

```text
Use prd-to-issues on the RecallFlow PRD and turn it into small GitHub issues with acceptance criteria.
```

### `tdd`

```text
Use tdd to implement RecallFlow one slice at a time, starting with late-appointment detection and follow-up.
```

### `improve-codebase-architecture`

```text
Use improve-codebase-architecture on RecallFlow and recommend any structural improvements before submission.
```
