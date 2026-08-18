# Sample Audit Report — Finding Examples

This document shows one finding at each severity level (P0 through P3) using the exact required format. Use these as reference when generating a `repository-audit` report.

---

## Report Metadata (Cover Block)

| Field | Value |
|---|---|
| Repository | `acme-api` |
| Company | Quantal AI |
| Audited Target | `main` branch @ `a3f9c12` |
| Date | 2024-11-15 |
| Review Scenario | Entire repository audit |
| Product Context | `docs/PRD_authentication.md` available |
| Validation Status | Unit tests run (47/47 pass). Integration tests blocked — no test database. |

---

## Executive Summary

4 findings across 3 severity levels. One P0 critical release blocker (plaintext password storage). One P1 authorization bypass. One P2 performance defect. One P3 dead-code cleanup item. No application code was changed during this review.

---

## Findings

---

### [P0] User passwords stored as plaintext in PostgreSQL

**Evidence:**
`src/auth/user.service.ts:L88` — `await db.query("INSERT INTO users (email, password) VALUES ($1, $2)", [email, plaintext])`. No hashing is applied anywhere in the call chain. Confirmed by tracing `registerUser()` → `UserService.create()` → `db.query()`. Reproduction: `POST /api/auth/register` stores password column verbatim.

**Blast radius:**
All registered users. A single database read (via SQL injection, insider access, or backup theft) exposes all user credentials in plaintext. Passwords are commonly reused across services, making this a cross-service credential compromise. Full credential database is immediately usable without any cracking step.

**Remediation:**
Hash passwords with `bcrypt` (cost factor ≥ 12) or `argon2id` before storage. Add a migration to invalidate existing plaintext passwords and force reset on next login. Never log or return password fields. Update `UserService.create()` and `AuthService.login()` (comparison path). No schema change required — only the stored value changes.

**Prompt for a coding agent:**
> In `src/auth/user.service.ts` and `src/auth/auth.service.ts`, replace all plaintext password storage and comparison with `bcrypt` (cost 12). The `registerUser()` function must hash before the `INSERT`. The `loginUser()` function must use `bcrypt.compare()` instead of `===`. Do not change the `users` table schema. Add focused regression tests: (1) a registered user can log in with the correct password, (2) login is rejected for an incorrect password, (3) the stored `password` column value is never equal to the plaintext input. Do not change any other auth logic.

**Smoke test:**
- Happy path: `POST /api/auth/register` then `POST /api/auth/login` with correct credentials → `200 OK` with valid session token.
- Regression path: Query `SELECT password FROM users WHERE email='test@example.com'` → value must not equal the plaintext password used at registration.

---

### [P1] Missing authorization check allows cross-tenant document access

**Evidence:**
`src/documents/document.controller.ts:L42` — `GET /api/documents/:id` calls `DocumentService.findById(id)` with no tenant scoping. `DocumentService.findById()` at `src/documents/document.service.ts:L19` executes `SELECT * FROM documents WHERE id = $1` — no `tenant_id` filter. Any authenticated user can fetch any document by guessing or iterating IDs.

**Blast radius:**
All tenants and all documents. An authenticated user of Tenant A can read, and potentially extract, all documents belonging to all other tenants by incrementing the document ID. Severity is P1 rather than P0 because it requires authentication; unauthenticated access is not possible.

**Remediation:**
Add `AND tenant_id = $2` to the `findById` query and pass `req.user.tenantId` from the controller. Apply the same fix to all other document queries in `document.service.ts`. Add a test asserting that a valid session from Tenant B cannot fetch a document owned by Tenant A.

**Prompt for a coding agent:**
> In `src/documents/document.service.ts`, add `tenant_id` scoping to every query that retrieves documents. The `findById(id)` method must accept a `tenantId` parameter and append `AND tenant_id = $tenantId` to the WHERE clause. In `src/documents/document.controller.ts`, pass `req.user.tenantId` to all `DocumentService` calls. Do not change the HTTP route paths or response shapes. Add a regression test: a valid JWT for tenant B must receive a 404 (not 200) when requesting a document owned by tenant A.

**Smoke test:**
- Happy path: Authenticated Tenant A user fetches their own document → `200 OK`.
- Authorization path: Authenticated Tenant B user fetches Tenant A's document ID → `404 Not Found` (not `200 OK`).

---

### [P2] N+1 query pattern on `/api/projects` list endpoint

**Evidence:**
`src/projects/project.service.ts:L67-L81` — `listProjects()` fetches all projects with one query, then loops and calls `UserService.findById(project.ownerId)` inside the loop (L74). For a workspace with 200 projects, this generates 201 database queries per request. Confirmed by reading the loop — no batching or join is used.

**Blast radius:**
All users of the projects list view. At 200 projects, each page load issues 201 queries. At 1,000 projects, 1,001 queries. Observed P99 latency will scale linearly with project count. Database connection pool saturation under moderate concurrent traffic is likely.

**Remediation:**
Replace the in-loop `UserService.findById` call with a single `JOIN users ON users.id = projects.owner_id` in the projects query, or collect all `ownerIds` and batch-fetch with `WHERE id = ANY($1)`. Remove the per-iteration lookup. This is a read-path change with no migration needed.

**Prompt for a coding agent:**
> In `src/projects/project.service.ts`, fix the N+1 query in `listProjects()` by adding a JOIN to `users` on the initial projects query instead of calling `UserService.findById()` inside the loop. The response shape must remain identical. Do not change pagination logic. Add a test asserting that fetching a list of 50 projects results in exactly 1 database query (use query-counting middleware or mock).

**Smoke test:**
- `GET /api/projects?page=1&limit=50` → responds in under 200ms with correct owner data embedded.
- Query log or mock confirms exactly 1 SQL query issued (not 51).

---

### [P3] Stale `generateLegacyToken()` function unreachable since v2 migration

**Evidence:**
`src/auth/token.service.ts:L112-L134` — `generateLegacyToken()` is exported but has zero call sites across the repository (`rg "generateLegacyToken"` returns only the definition). Git log shows this was used in v1 (commit `d4a21bb`, 14 months ago) and the v2 migration removed the last call site. The function references a deprecated JWT signing key constant that no longer appears in any active configuration.

**Blast radius:**
No user or production impact. Dead code increases cognitive load and surface area for future confusion. The deprecated signing key constant it references could mislead a future engineer into thinking it is still active.

**Remediation:**
Delete `generateLegacyToken()` from `token.service.ts` and remove the associated deprecated signing key constant. Update the module's export index if present. No migration or deployment step needed.

**Prompt for a coding agent:**
> Delete the `generateLegacyToken()` function from `src/auth/token.service.ts` and remove the `LEGACY_JWT_SECRET` constant it references. Verify with `rg "generateLegacyToken"` and `rg "LEGACY_JWT_SECRET"` that no other call sites exist before deleting. Remove the export from the module index if listed. Do not change any other functions in the file. No new tests needed — confirm existing tests still pass after removal.

**Smoke test:**
- `rg "generateLegacyToken"` returns zero results after deletion.
- Existing test suite passes with no changes.
