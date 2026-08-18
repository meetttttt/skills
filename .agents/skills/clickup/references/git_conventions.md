# ClickUp Git Integration & Naming Conventions

To seamlessly connect ClickUp task tracking with Git repositories, follow these conventions when creating branches, writing commits, and opening Pull Requests (PRs).

---

## Task ID Formats

ClickUp task IDs typically appear as:
- Short format: `CU-8675309` or `8675309`
- Hash format: `#CU-8675309` or `#8675309`
- Full URL: `https://app.clickup.com/t/8675309`

All formats map to the same underlying ID (`8675309` or `CU-8675309`).

---

## 1. Branch Naming Conventions

Format: `<type>/<lowercase_kebab_slug>` — **no ClickUp ID in the branch name.** This follows industry-standard, human-readable branch naming (Conventional Commits type vocabulary). Traceability back to the ClickUp task comes from the commit message tag (below) and the PR link synced to the task, not the branch name itself.

### `<type>` Vocabulary

| Type | When |
|---|---|
| `feat` | New user-facing capability |
| `fix` | Bug fix / defect correction |
| `docs` | Documentation-only change (specs, READMEs, architecture docs) |
| `refactor` | Behavior-preserving code restructure |
| `perf` | Performance improvement |
| `test` | Test-only changes |
| `chore` | Build tooling, dependencies, config |
| `ci` | CI/CD pipeline changes |

### `<slug>`
A short (2-4 word), lowercase, kebab-case slug derived from the task/spec title. Strip filler words ("Implement", "Add support for").

### Examples
- **New Feature**: `feat/login`, `feat/webpage-login`, `feat/realtime-notifications`
- **Bug Fix**: `fix/null-pointer-date-parse`
- **Refactoring**: `refactor/slugify-utf8`
- **Documentation**: `docs/v1-tech-arch`
- **Chore / Infra**: `chore/clickup-skill-setup`

### Resuming Work
Before creating a branch, check whether one matching this task already exists locally or on the remote (`git branch --list <name>` / `git ls-remote --heads origin <name>`). If so, check it out instead of creating a duplicate.

---

## 2. Commit Message Conventions

Format: `[CU-<task_id>] <type>: <short description>` — this is where ClickUp traceability lives, since the branch name no longer carries the task ID. `<type>` matches the branch's type exactly.

### Examples
```bash
git commit -m "[CU-8675309] feat(utils): add unicode slugify support"
git commit -m "[CU-8675309] fix(api): resolve race condition on SSE reconnect"
git commit -m "[CU-8675309] test: add unit test suite for date parser"
```

---

## 3. Pull Request (PR) Body Template

Include the ClickUp task link in the PR description so GitHub/GitLab and ClickUp auto-link the PR:

```markdown
## ClickUp Task
- **Task Link**: [CU-8675309](https://app.clickup.com/t/8675309)

## Summary of Changes
- Refactored `slugify()` helper in `utils.py` to preserve UTF-8 unicode characters.
- Added regex validation for non-Latin scripts (Chinese, Cyrillic, Spanish).
- Added unit tests in `test_utils.py` covering edge case inputs (`null`, `undefined`, empty strings).

## Verification & Testing
- [x] Unit tests passing (12/12)
- [x] Local build clean
- [x] ClickUp task status updated to `IN REVIEW`
```
