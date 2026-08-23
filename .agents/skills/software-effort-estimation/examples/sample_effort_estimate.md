# Sample Effort Estimate — Epic Examples

This document shows one epic at each risk level (High, Medium, Low), plus a sample
executive summary and assumptions log, using the exact required format. Use these as
reference when generating a `software-effort-estimation` report.

---

## Report Metadata (Cover Block)

| Field | Value |
|---|---|
| Project | `Loyalty Rewards Revamp` |
| Company | Quantal AI |
| Source Document | `docs/PRD_loyalty_rewards.md` |
| Date | 2026-08-23 |
| Sprint Length | 2 weeks (confirmed with user) |
| Color Disclosure | Red/amber/teal denote estimation complexity/risk in this report, not bug severity. |

---

## Executive Summary

6 epics extracted, 47 story points total (41 dev + 15% contingency, rounded up).
Confirmed team: 1 Senior Backend, 2 Mid Frontend, 1 Junior QA — team velocity 34
points/sprint. Dev timeline: 2 sprints. Total timeline including QA taper, UAT, and
deployment: 4 sprints. One epic flagged as under-resourced given a single backend
resource against two High-risk epics.

---

## Epic Breakdown

---

### [HIGH] Real-time points ledger with idempotent reconciliation

**Scope:** Build a real-time ledger service that credits/debits loyalty points on
purchase and refund events, per PRD §3.1-3.3, with exactly-once processing across
duplicate webhook deliveries.

**Story points:** 13 — anchored to the "large feature, multiple services, significant
unknowns" tier in references/estimation_methodology.md §2. New idempotency mechanism,
no existing pattern in the codebase.

**Rationale:** New tech (event-sourced ledger), external dependency on the payments
webhook provider's delivery guarantees, and unclear retry semantics per PRD §3.3 ("TBD"
noted in the source document).

**Dependencies:** Blocks the "Points balance API" epic. Depends on payments team
confirming webhook retry behavior — flagged as an external risk.

**Assigned sprint(s):** Sprint 1-2, owned by Senior Backend.

---

### [MEDIUM] Points balance API and caching layer

**Scope:** Expose a read API for current point balance with a caching layer to keep
read latency under the PRD's 200ms budget (§4.2).

**Story points:** 8 — "cross-cutting feature, new integration, meaningful unknowns"
tier. Depends on the ledger epic's schema being finalized first.

**Rationale:** Cache invalidation strategy is a known pattern for this team but the
consistency requirement (§4.2) against the new ledger introduces some unknowns.

**Dependencies:** Depends on the ledger epic (Sprint 1-2) landing first.

**Assigned sprint(s):** Sprint 2, owned by 1 Mid Frontend (API consumer) + Senior
Backend (API design review).

---

### [LOW] Loyalty tier badge on user profile page

**Scope:** Display the user's current loyalty tier (Bronze/Silver/Gold) as a badge on
the existing profile page, per PRD §2.4.

**Story points:** 2 — "small, well-understood, one component" tier. Pure frontend
display change against an already-exposed field.

**Rationale:** No new backend work, no external dependency, uses an existing component
library pattern already present in the codebase.

**Dependencies:** None.

**Assigned sprint(s):** Sprint 1, owned by 1 Mid Frontend.

---

## Assumptions Log

| Item | Value | Status |
|---|---|---|
| Sprint length | 2 weeks | Confirmed by user |
| Contingency | 15% | Default, confirmed by user |
| Team velocity | 34 pts/sprint | Computed from confirmed team + default velocity table (methodology §3) |
| QA/UAT/Deployment tracks | Included | Confirmed by user |
| Junior QA velocity | 5 pts/sprint | Default from methodology §3, not overridden |
