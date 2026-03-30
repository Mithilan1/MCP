# Skills Setup Notes

## Current status on 2026-03-30

- The five required skills are present in this repo under both `.claude/skills/` and `.codex/skills/`.
- Codex also has the same five skills available locally.
- Claude Code can use the project-scoped `.claude/skills/` folder as soon as this repo is opened there.

## Matt Pocock source

These five skills match the ones published in Matt Pocock's `skills` repo:

- `grill-me`
- `write-a-prd`
- `prd-to-issues`
- `tdd`
- `improve-codebase-architecture`

Reference:

- `https://github.com/mattpocock/skills/tree/main`

## Skill locations in this repo

This repo now keeps the same five skill folders in both local mirrors:

- `grill-me`
- `write-a-prd`
- `prd-to-issues`
- `tdd`
- `improve-codebase-architecture`

Paths:

- Claude project mirror: `.claude/skills/<skill-name>/SKILL.md`
- Codex repo mirror: `.codex/skills/<skill-name>/SKILL.md`

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

## How to run them in Claude Code

1. Open this repo in Claude Code.
2. Claude Code reads the project-scoped `.claude/skills/` directory automatically.
3. Invoke a skill directly in chat with one of these commands:

```text
/grill-me
/write-a-prd
/prd-to-issues
/tdd
/improve-codebase-architecture
```

4. After the slash command, give the skill a task for RecallFlow. Example:

```text
Use grill-me on RecallFlow, a dashboard that follows up with customers who are 30 minutes late for appointments.
```

5. If you want the same skills available globally in Claude Code, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_claude_skills.ps1
```

Then restart Claude Code.

## How to run them from VS Code

VS Code and Claude skills do different jobs in this repo:

- `.vscode/mcp.json` starts the MCP servers for Context7, NotebookLM, and Playwright.
- the five Matt Pocock skills are still Claude-style skills, so you use them through Claude Code, even if Claude Code is running inside a VS Code workspace or terminal.

Use this flow:

1. Open the repo in VS Code.
2. Keep `.vscode/mcp.json` in place so VS Code can see the same MCP server setup as Claude Code.
3. Open Claude Code against this workspace.
4. Invoke the same slash commands listed above.

If you want the user-level MCP config copied into the normal Windows locations for Codex, VS Code, and Claude, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_codex_vscode_configs.ps1 -InstallClaudeGlobal -Context7ApiKey "YOUR_CONTEXT7_API_KEY"
```

Then restart VS Code and Claude Code.

## What to show in your video

- the project `.claude/skills/` folder in this repo
- the project `.codex/skills/` folder in this repo
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
