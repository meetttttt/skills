# Ship Branch & Commit Conventions

`ship` reuses the `clickup` skill's git conventions exactly — see [../../clickup/references/git_conventions.md](../../clickup/references/git_conventions.md) for the authoritative reference. In short:

- **Branch**: `<type>/<lowercase-kebab-slug>` — no ClickUp ID in the branch name, regardless of whether a ClickUp task is in scope. `<type>` follows the Conventional Commits vocabulary (`feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `chore`, `ci`).
- **Commit**: `[CU-<task_id>] <type>: <short description>` when a ClickUp task is in scope — this is where traceability lives, since the branch name doesn't carry it. Without a ClickUp task, the `[CU-<id>]` prefix is simply omitted: `<type>: <short description>`.

`<type>` and `<slug>` are the same regardless of ClickUp context — only the commit message tag differs. This file covers what's specific to `ship`: `<type>` inference when it wasn't already established by a prior `implement` run.

---

## `<type>` Inference

If `ship` runs standalone (no prior `implement` session established the branch/type already), infer `<type>` from the nature of the change:

| Change Pattern | Type |
|---|---|
| New user-facing capability | `feat` |
| Bug fix / defect correction | `fix` |
| Behavior-preserving code restructure | `refactor` |
| Build tooling, dependencies, CI config | `chore` |
| Test-only changes | `test` |
| Documentation-only changes | `docs` |
| Performance improvement | `perf` |
| CI/CD pipeline changes | `ci` |

If a change spans multiple categories, pick the type of its primary intent and mention the rest in the commit body, not the subject line. If genuinely ambiguous, ask the user to confirm rather than guessing.

## `<slug>` Inference

A short (2-4 word), lowercase, kebab-case slug derived from the ClickUp task title (if in scope) or the diff/change summary otherwise. Strip filler words.
