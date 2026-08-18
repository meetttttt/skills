---
name: ship
description: >-
  Commit implemented changes, push a conventionally-named branch, and open a GitHub PR with an
  auto-generated description derived from the ClickUp task and PRD/FRD. Uses `gh` CLI and `git`
  directly — no MCP dependency. Pauses for explicit user confirmation before pushing or opening
  the PR. Can run standalone or as an optional final step after the `implement` skill.
---

# Ship Skill: Branch, Commit, and PR Automation

The **Ship** skill handles the git/GitHub side of shipping a change: staging exactly the files that were implemented, generating a ClickUp-tagged commit and branch name, and opening a pull request with a description derived from the ClickUp task and its linked PRD/FRD — pausing for confirmation before anything leaves the local machine.

---

## When to Activate This Skill

Activate when the user says:
- "ship this" / "ship CU-xxxx"
- "create a PR" / "raise a PR"
- "commit and push this"
- "create a branch for this"

Or when the `implement` skill offers it as an optional final step (see [../implement/SKILL.md](../implement/SKILL.md)) and the user accepts.

A repository with an existing git remote is required. GitHub is assumed as the host (via `gh` CLI).

---

## Step 1 — Gather Scope

Determine what is being shipped:

1. **File scope**: Prefer the exact file list reported by `implement`'s "Files created/modified" summary (Step 8 of that skill), if this run followed an `implement` session. Otherwise, ask the user which files to include, or confirm the current `git status` diff with them explicitly — never silently stage unrelated working-tree changes.
2. **ClickUp context**: If a ClickUp Task ID is available (from the conversation, branch name, or a prior `implement` run), fetch the task title and description via the `clickup` skill's integration hierarchy. If no ClickUp task is available, proceed without it — branch/commit naming falls back to a generic scheme (Step 2) and the ClickUp status sync (Step 5) is skipped.
3. **PRD/FRD context**: If a PRD/FRD was resolved during `implement`, reuse it as the source for the PR description. Otherwise, the PR description is generated from the diff and any ClickUp task description alone.

---

## Step 2 — Confirm Branch and Generate Commit

**Branch**: `<type>/<slug>` — no ClickUp ID in the branch name, pure semantic naming (see [references/git_conventions.md](references/git_conventions.md)). Same `<type>` vocabulary either way (`feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `chore`, `ci`) — presence of a ClickUp task does not change branch naming, only the commit message.

- **If this run follows `implement`**: the branch was already created there (Step 4 of `implement`). Confirm the current branch matches `<type>/<slug>` for this task — do not create a new one.
- **If invoked standalone** (no prior `implement` run in this session): create it now — check whether a matching branch already exists locally/remotely first (resume instead of duplicate), otherwise branch from the up-to-date default branch: `git checkout -b <type>/<slug>`.

**Commit message**:
- With a ClickUp task: `[CU-<task_id>] <type>: <short description>`, generated from the ClickUp task title and the PRD/FRD acceptance criteria covered.
- Without one: `<type>: <short description>`, generated from the diff summary.
- `<type>` matches the branch's type exactly — inferred from the nature of the change if not already established by `implement`.

Stage **only** the files identified in Step 1. Do not run `git add -A` or `git add .`.

---

## Step 3 — Confirmation Checkpoint (Hard Gate)

> ⛔ **Do not push or open a PR until the user explicitly confirms.**

Present to the user, before touching the remote:
- The generated branch name
- The generated commit message
- The full list of staged files
- A short diff summary (files changed, insertions/deletions)

Ask the user to confirm, edit, or cancel. If they cancel, stop — leave the commit staged locally, make no remote changes. If they edit the branch name or commit message, use their version.

---

## Step 4 — Push and Open PR

Once confirmed:

1. Commit the staged files with the confirmed message.
2. Push the branch: `git push -u origin <branch-name>`.
3. Check for an existing open PR on this branch first: `gh pr view <branch-name>` (or `--json` for scripting). If one exists, update its description instead of creating a duplicate: `gh pr edit <branch-name> --body "..."`.
4. Otherwise, open a new PR: `gh pr create --title "<title>" --body "<description>" --base <default-branch>`.
   - Detect the base branch via `gh repo view --json defaultBranchRef` rather than assuming `main`.
   - Build the PR description from [references/pr_description_template.md](references/pr_description_template.md).

If `gh` is not installed or not authenticated, stop and give the user the exact remediation command (`gh auth login`) rather than attempting a raw REST fallback.

---

## Step 5 — Sync ClickUp Status

If a ClickUp task is in scope, update its status to **"in review"** (same status `implement` sets after smoke tests pass — this step is idempotent if already there) and append the PR link to the task description:

- **MCP**: `clickup_update_task({ taskId: "CU-xxxx", status: "in review", description: "<existing>\n\n🔗 PR: <pr_url>" })`
- **CLI**: `python3 .agents/skills/clickup/scripts/clickup_helper.py update-status CU-xxxx "in review"` then `python3 .agents/skills/clickup/scripts/clickup_helper.py update-description CU-xxxx "<existing>\n\n🔗 PR: <pr_url>"`

This skill does **not** poll for or react to the PR being merged. Checking merge status later is a separate, explicit request (e.g. "did CU-xxxx merge?").

---

## Step 6 — Final Summary

Respond to the user with:

- ✅ Branch: `<type>/<slug>` (e.g. `feat/login`)
- 📝 Commit: `[CU-xxxx] <type>: <description>`
- 🔗 PR: `<pr_url>`
- 🔁 ClickUp status: updated to "in review" (or "skipped — no ClickUp task in scope")

---

## References & Examples

- [references/git_conventions.md](references/git_conventions.md) — Branch naming and commit tag conventions (mirrors `clickup`'s conventions).
- [references/pr_description_template.md](references/pr_description_template.md) — PR body structure derived from ClickUp task and PRD/FRD.
- [examples/sample_ship_workflow.md](examples/sample_ship_workflow.md) — Standalone invocation and auto-chain-from-`implement` transcripts.
- [../clickup/SKILL.md](../clickup/SKILL.md) — ClickUp task management skill.
- [../implement/SKILL.md](../implement/SKILL.md) — Task-driven implementation skill (optional upstream step).
