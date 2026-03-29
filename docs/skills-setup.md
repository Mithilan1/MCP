# Skills Setup Notes

## Current status on 2026-03-25

- The five required Matt Pocock skills are installed in Codex at `C:\Users\JT\.codex\skills\`.
- The repo now also includes the same five skills under `.claude/skills/` as project-scoped Claude Code skills.
- Claude Code is not installed on this machine yet, so I could not verify them live in Claude Code.

## Codex status

Installed skills:

- `grill-me`
- `write-a-prd`
- `prd-to-issues`
- `tdd`
- `improve-codebase-architecture`

After installation, restart Codex so the new skills are picked up cleanly.

## Claude Code path rules

Anthropic documents these locations:

- personal skills: `~/.claude/skills/<skill-name>/SKILL.md`
- project skills: `.claude/skills/<skill-name>/SKILL.md`

That means you have two valid ways to show Claude Code skills:

- open this repo in Claude Code and show the project-scoped `.claude/skills/` folder
- copy the same skills into `~/.claude/skills/` for a user-scoped setup

## Ready-to-use copy helper

This repo includes [scripts/install_claude_skills.ps1](../scripts/install_claude_skills.ps1), which copies the five required skill folders from your Codex skills directory into `~/.claude/skills/`.

Use it after Claude Code is installed:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_claude_skills.ps1
```

## What to show in your video

- the `C:\Users\JT\.codex\skills\` folder with the five required skills
- the project `.claude/skills/` folder in this repo
- optionally the Claude user skills folder after copying
- your chat history for each skill call in the required order

## Suggested prompts for the required skill order

### `grill-me`

```text
Use grill-me on this project idea: HabitFlow, a tiny Python-only habit tracker for Assignment 4. Push back on anything too large or unclear.
```

### `write-a-prd`

```text
Use write-a-prd for HabitFlow, a small habit tracker with daily and weekly habits, a local JSON store, and a tiny web UI.
```

### `prd-to-issues`

```text
Use prd-to-issues on the HabitFlow PRD and turn it into small GitHub issues with acceptance criteria.
```

### `tdd`

```text
Use tdd to implement HabitFlow one slice at a time, starting with creating and completing a habit.
```

### `improve-codebase-architecture`

```text
Use improve-codebase-architecture on HabitFlow and recommend any structural improvements before submission.
```
