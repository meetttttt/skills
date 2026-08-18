# Sample Ship Workflow Transcripts

Two scenarios: `ship` chained automatically after `implement`, and `ship` invoked standalone.

---

## Scenario 1: Auto-Chained After `implement`

**User**:
> Implement CU-9900112

**Agent**:
> *(implement Steps 1-3 run: fetch task, sync "in progress", resolve PRD/FRD)*
>
> 🌿 Created branch `feat/realtime-event-delivery` (task type inferred as `feat` from PRD title "Real-Time Event Delivery Engine")
>
> *(implement Steps 5-8 run: understand codebase, implement, smoke tests 4/4 passing, sync "in review")*
>
> ✅ **Task implemented**: `CU-9900112 — Real-Time Event Delivery Engine`
> 🌿 **Branch**: `feat/realtime-event-delivery`
> 📄 **PRD/FRD used**: `docs/PRD_realtime_notifications.md`
> 📁 **Files created/modified**:
>   - `migrations/0042_add_user_notifications.sql` (new)
>   - `src/services/notifications.service.ts` (new)
>   - `src/controllers/notifications.controller.ts` (new)
>   - `src/routes/index.ts` (modified)
> 🧪 **Smoke tests**: 4/4 passing
> 🔁 **ClickUp status**: updated to "in review"
>
> Want me to ship this now — commit, push, and open a PR? (yes / no)

**User**:
> yes

**Agent** *(ship Step 1-2)*:
> Gathering scope from the implement run above (4 files) and CU-9900112. Already on branch `feat/realtime-event-delivery` (created by implement) — no new branch needed.
>
> Generated:
> - **Branch**: `feat/realtime-event-delivery` (confirmed, already checked out)
> - **Commit**: `[CU-9900112] feat(notifications): add real-time SSE delivery engine`
> - **Files staged**: `migrations/0042_add_user_notifications.sql`, `src/services/notifications.service.ts`, `src/controllers/notifications.controller.ts`, `src/routes/index.ts`
> - **Diff**: +187 / -3 across 4 files

**Agent** *(ship Step 3 — confirmation checkpoint)*:
> Confirm branch name, commit message, and file list above before I push and open a PR? (yes / edit / cancel)

**User**:
> yes

**Agent** *(ship Step 4-6)*:
> ✅ Committed and pushed `feat/realtime-event-delivery`
> ✅ Opened PR: https://github.com/acme/webapp/pull/482
> 🔁 ClickUp status: "in review" (already set), PR link appended to task description
>
> **Summary**:
> - 🔗 PR: https://github.com/acme/webapp/pull/482
> - Branch: `feat/realtime-event-delivery`
> - Commit: `[CU-9900112] feat(notifications): add real-time SSE delivery engine`

---

## Scenario 2: Standalone Invocation, No ClickUp Task

**User**:
> Ship this — I fixed the off-by-one bug in the pagination helper.

**Agent** *(ship Step 1)*:
> No ClickUp task ID found in the conversation. Proceeding without one — using generic branch/commit naming and skipping ClickUp status sync.
>
> `git status` shows changes in `src/utils/pagination.ts` and `tests/pagination.test.ts`. Should I stage exactly these two files?

**User**:
> yes

**Agent** *(ship Step 2)*:
> Generated:
> - **Branch**: `fix/pagination-off-by-one`
> - **Commit**: `fix(pagination): correct off-by-one error in page offset calculation`
> - **Files staged**: `src/utils/pagination.ts`, `tests/pagination.test.ts`
> - **Diff**: +6 / -4 across 2 files

**Agent** *(ship Step 3)*:
> Confirm the above before I push and open a PR? (yes / edit / cancel)

**User**:
> edit branch to fix/pagination-page-offset

**Agent** *(ship Step 4-6)*:
> ✅ Committed and pushed `fix/pagination-page-offset`
> ✅ Opened PR: https://github.com/acme/webapp/pull/483 (base: `main`, auto-detected via `gh repo view`)
> 🔁 ClickUp status: skipped — no ClickUp task in scope
>
> **Summary**:
> - 🔗 PR: https://github.com/acme/webapp/pull/483
> - Branch: `fix/pagination-page-offset`
> - Commit: `fix(pagination): correct off-by-one error in page offset calculation`

---

## Scenario 3: Confirmation Declined

**User**:
> Ship CU-5512298

**Agent** *(ship Step 1-3)*:
> Generated:
> - **Branch**: `feat/bulk-export`
> - **Commit**: `[CU-5512298] feat(export): add bulk CSV export endpoint`
> - **Files staged**: `src/controllers/export.controller.ts`
>
> Confirm before I push and open a PR? (yes / edit / cancel)

**User**:
> cancel, I need to add error handling first

**Agent**:
> Stopped. The commit remains staged locally on `feat/bulk-export` — nothing was pushed and no PR was opened. Run "ship this" again once you've made your changes.
