# PR Description Template

`ship` builds on `clickup`'s PR body template (see [../../clickup/references/git_conventions.md](../../clickup/references/git_conventions.md), section 3) and extends it with content pulled from the PRD/FRD when one was resolved during `implement`.

---

## Template A: With ClickUp Task + PRD/FRD

Used when both a ClickUp task and a resolved PRD/FRD document are in scope.

```markdown
## ClickUp Task
- **Task Link**: [CU-<task_id>](https://app.clickup.com/t/<task_id>) — <task title>
- **Spec**: docs/PRD_<feature>.md (or FRD_<feature>.md)

## Summary of Changes
- <2-4 bullets summarizing what was implemented, drawn from implement's Step 5/8 output>

## Acceptance Criteria Covered
- [x] <criterion 1, copied verbatim from the PRD/FRD>
- [x] <criterion 2>
- [x] <criterion 3>

## Files Changed
- `<path>` (new/modified) — <one-line purpose>

## Verification & Testing
- [x] Smoke tests passing (<N>/<N>) — see `smoke-test` run output
- [x] ClickUp task status updated to `IN REVIEW`
```

---

## Template B: With ClickUp Task, No PRD/FRD

Used when a ClickUp task exists but `implement` was not the source (e.g. `ship` invoked standalone on ad-hoc work).

```markdown
## ClickUp Task
- **Task Link**: [CU-<task_id>](https://app.clickup.com/t/<task_id>) — <task title>

## Summary of Changes
- <bullets derived from the diff and the ClickUp task description>

## Verification & Testing
- [ ] <manual verification notes, since no smoke-test run is guaranteed in this path>
```

---

## Template C: No ClickUp Task

Used when `ship` runs in a repository or on a change with no ClickUp task in scope at all.

```markdown
## Summary of Changes
- <bullets derived from the diff>

## Verification & Testing
- [ ] <manual verification notes>
```

---

## Rules

- Never fabricate acceptance criteria, task links, or test results that weren't actually produced — omit a section entirely rather than inventing content for it.
- The "Files Changed" list must match exactly what was staged in `ship`'s Step 2 — no broader scope than the actual commit.
- If `smoke-test` was not run in this session, do not claim "Smoke tests passing" — use an unchecked box or omit the line.
