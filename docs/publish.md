# Publish to GitHub

Target repository:

- `https://github.com/Mithilan1/MCP`
- Published from this workspace on `2026-03-29`

## Local git commands

```powershell
git add .
git commit -m "Build HabitFlow assignment project"
git remote add origin https://github.com/Mithilan1/MCP.git
git branch -M main
git push -u origin main
```

## Real GitHub Issues

Create the issues in the target repository using the titles and acceptance criteria from [docs/issues.md](docs/issues.md).

Suggested titles:

1. Bootstrap HabitFlow and define the core data model
2. Build the habit service and local persistence workflow
3. Expose API endpoints and a lightweight frontend
4. Add test coverage and tighten the demo story
5. Improve architecture and prepare assignment evidence

If GitHub CLI is already logged in, the UI is still the easiest option because `docs/issues.md` contains multiple issue bodies in one file.
