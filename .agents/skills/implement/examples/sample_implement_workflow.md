# Sample Implement Workflow Transcript

This transcript demonstrates the full 10-step `implement` skill execution — from ClickUp task fetch through branch creation, smoke test pass, and status sync.

---

## Scenario: Implementing Real-Time Notifications from CU-9900112

**User**:
> Implement CU-9900112

---

### Step 1: Fetch ClickUp Task

**Agent**:
> Fetching task details via ClickUp MCP...
>
> **Task**: `CU-9900112 — Real-Time Event Delivery Engine (SSE + Redis Pub/Sub)`
> **Priority**: High
> **Status**: To Do
> **Acceptance Criteria**:
> - `GET /api/v1/notifications/stream` must establish an SSE connection
> - Redis Pub/Sub listener must fan out events to connected clients
> - Client must implement exponential backoff reconnect (max 5 retries)
> - All events must be persisted to `user_notifications` table before delivery

---

### Step 2: Sync Status → In Progress

**Agent**:
> Updating CU-9900112 status to **"in progress"**... ✅

---

### Step 3: Locate PRD/FRD (Hard Gate)

**Agent**:
> Searching `docs/` for matching PRD/FRD...
> Found: `docs/PRD_realtime_notifications.md`
>
> Validating document — contains API contracts, data model, edge cases ✅
>
> Auto-linking spec to CU-9900112 task description... ✅
> Added: `📄 Spec: docs/PRD_realtime_notifications.md`

---

### Step 4: Create Feature Branch

**Agent**:
> Checking for an existing branch for this task... none found.
>
> Inferring `<type>` from PRD title "Real-Time Event Delivery Engine" → `feat`
> Deriving `<slug>` from PRD title → `realtime-event-delivery`
>
> Branching from up-to-date `main`: `git checkout -b feat/realtime-event-delivery` ✅

---

### Step 5: Understand the Codebase

**Agent**:
> Reading PRD acceptance criteria and exploring codebase...
>
> - Existing pattern: Express.js controllers in `src/controllers/`, services in `src/services/`
> - Redis client already configured in `src/config/redis.ts`
> - `user_notifications` table DDL missing — migration required
> - Files to create:
>   - `src/controllers/notifications.controller.ts`
>   - `src/services/notifications.service.ts`
>   - `migrations/0042_add_user_notifications.sql`
> - Files to modify:
>   - `src/routes/index.ts` (register new route)

---

### Step 6: Implement

**Agent**:
> Implementing per PRD acceptance criteria...
>
> ✅ Created `migrations/0042_add_user_notifications.sql`
> ✅ Created `src/services/notifications.service.ts` (Redis Pub/Sub subscriber)
> ✅ Created `src/controllers/notifications.controller.ts` (SSE endpoint)
> ✅ Modified `src/routes/index.ts` (registered `/api/v1/notifications/stream`)

---

### Step 7: Run Smoke Tests

**Agent**:
> Invoking `smoke-test` skill with context: CU-9900112 / `docs/PRD_realtime_notifications.md`
>
> Framework detected: `jest` (`package.json`)
> Generated: `tests/smoke/notifications.smoke.test.ts`
>
> Running: `npx jest tests/smoke/notifications.smoke.test.ts`
>
> ```
> ✓ SSE endpoint returns 200 with content-type text/event-stream (142ms)
> ✓ Redis Pub/Sub delivers event to connected client within 500ms (89ms)
> ✓ Duplicate event delivery is idempotent (61ms)
> ✓ Client reconnect after drop returns correct backoff headers (73ms)
>
> 4/4 smoke tests passing ✅
> ```

---

### Step 8: Sync Status → In Review

**Agent**:
> Updating CU-9900112 status to **"in review"**... ✅

---

### Step 9: Final Summary

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

---

## Scenario: Hard Stop — No PRD/FRD Found

**User**:
> Implement CU-5512233

**Agent**:
> Fetching task CU-5512233 — "User Invitation Flow"... ✅
> Updating status to "in progress"... ✅
>
> Searching `docs/` for matching PRD/FRD...
> Searching repo-wide for spec documents...
>
> I couldn't locate a PRD/FRD document in `docs/` or the repository. Do you have one at a different filepath?

**User**:
> No, one doesn't exist yet.

**Agent**:
> ⛔ **No PRD or FRD document was found for ClickUp task CU-5512233.**
>
> Implementing without a specification is not permitted.
>
> Please generate one first:
> 1. Run the `prd-frd` skill to create `docs/PRD_user_invitation.md`
> 2. Then retry: "implement CU-5512233"
