# Finding Severity Guide

Qualification rules, severity definitions, and the exact finding format for every `repository-audit` report.

---

## Qualification Rules

Only report a finding if **all** of the following are true:

- **Concrete**: demonstrated by code, configuration, Git history, tests, or safe live validation.
- **Actionable**: has a clear, achievable remediation.
- **In-scope**: relevant to correctness, security, privacy, performance, reliability, cost, or meaningful maintainability.
- **Non-duplicate**: is not the same root cause as another finding already reported.
- **Significant**: would realistically be fixed by the repository owner if known.

**Never report:**
- Style nits or formatting preferences
- Unproven theoretical attacks without a demonstrated reachable path
- Intentional tradeoffs that have no concrete downside
- Vague "could be improved" observations without specifics
- Speculative vulnerabilities with no evidence of exploitability

---

## Severity Definitions

### P0 — Critical Release Blocker
**Definition:** Universal release blocker, active critical security exposure, likely irreversible corruption, or catastrophic data loss.

**Examples:**
- Unauthenticated RCE or SQL injection on a production-reachable endpoint
- Plaintext storage of user passwords
- Unrecoverable data-loss migration with no rollback
- API key with admin cloud access committed to public history

**Action:** Must be fixed before any release. Escalate immediately.

---

### P1 — Urgent
**Definition:** Urgent security, privacy, reliability, correctness, or cost issue that should be fixed before production use.

**Examples:**
- Authorization bypass allowing cross-tenant data access
- Missing CSRF protection on a state-changing authenticated endpoint
- Unhandled exception that crashes a critical background worker
- PII logged to a third-party observability service

**Action:** Fix before production. Can ship to staging but not production.

---

### P2 — Material Defect / Operational Risk
**Definition:** Material bug, operational risk, hardening gap, performance problem, or technical debt with a clear remediation.

**Examples:**
- N+1 query in a high-traffic list endpoint causing degraded response times
- Missing retry/backoff on a critical third-party integration
- Secrets committed in example `.env` file in a private repo
- Missing index causing full table scan on a large table

**Action:** Schedule and fix in the current or next sprint.

---

### P3 — Lower-Impact Improvement
**Definition:** Lower-impact but worthwhile issue that should be scheduled.

**Examples:**
- Dead code or stale feature flag not cleaned up
- Non-obvious concurrency assumption missing a comment
- Dependency pinned to a major version without a lockfile
- Missing observability metric on a non-critical path

**Action:** Track and fix when bandwidth allows.

---

## Exact Finding Format (copy this template for every finding)

```markdown
### [P_] Imperative finding title in present tense

**Evidence:** Exact file path(s) and line reference(s). Relevant commit or branch context
where applicable. Demonstrated call path, trigger condition, or request scenario.

**Blast radius:** Which users, services, datasets, cost categories, or systems are
affected. What is the triggering scenario. What is the operational and security/privacy
impact. What is the worst-case outcome.

**Remediation:** The smallest safe design-level fix. Name the components to change.
Describe migration or rollout considerations. Note backward compatibility concerns.
Identify any required operational steps (revocation, re-encryption, re-index, etc.).

**Prompt for a coding agent:**
> Specific implementation prompt. Must name the exact files and functions to change.
> Must preserve intended behavior. Must request focused regression tests covering the
> fix and a relevant failure path. Must state clearly what must not be changed.

**Smoke test:**
- Happy path: [exact command or step that demonstrates the fixed behavior]
- Failure/regression path: [exact command or step that demonstrates the vulnerability
  or bug is gone, e.g. unauthorized request returns 403, duplicate request is idempotent]
```

---

## Finding Ordering

In the final report, order findings:

1. P0 (most critical first within each severity tier)
2. P1
3. P2
4. P3

Within each severity tier, lead with security findings, then correctness, then performance, then architecture/debt.
