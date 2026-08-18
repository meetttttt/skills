---
name: repository-audit
description: >-
  Perform an evidence-backed repository, branch, pull-request, or release audit and
  generate a standardized professional Markdown and PDF report. Use when an agent must
  review an entire repository, a standalone branch, a branch-to-branch comparison, a
  PR/commit range, or codebase history for correctness, security, secrets, Git/GitHub
  exposure, performance, reliability, architecture, modularity, technical debt, and test
  gaps, including severity, blast radius, implementation prompts, and smoke tests.
---

# Repository Audit Skill

A comprehensive, project-agnostic code review and audit skill. Produces an evidence-backed Markdown report and a standardized professional PDF report for every engagement.

---

## Core Operating Rules

- **Read-only by default.** Never implement fixes unless the user explicitly requests them.
- **Preserve dirty worktrees.** Never overwrite unrelated user changes.
- **Read `AGENTS.md` first** if present in the repository before starting.
- **No invention.** Do not invent findings, requirements, test results, PRD/FRD details, ClickUp data, or production behavior.
- **Ask when unsure.** If an important requirement, target, comparison base, expected behavior, or risk decision is unclear and cannot safely be discovered, ask the user before proceeding.
- **No secret disclosure.** Never print secret values, access tokens, private keys, PII, or sensitive payloads in findings or reports. If a verified secret is found, report only the affected path/commit/type, advise immediate revocation and history remediation.
- **No speculation.** Only report concrete, actionable findings evidenced by audited code or configuration.

---

## Step 1 — Clarify the Review Scenario

Identify which scenario applies **before** starting. If the user has not specified one and it cannot be safely inferred, ask a single concise clarification question.

### Supported Scenarios

| # | Scenario | What to do |
|---|---|---|
| 1 | **Entire repository audit** | Review the default branch and relevant reachable Git history. Inspect code, config, infra, tests, dependencies, docs, and release controls. |
| 2 | **Branch-to-branch comparison** | e.g. `feature1 → dev`, `dev → main`. Ask for source and target if not supplied. Resolve actual merge base — review the change that would merge, not merely diff of tips. |
| 3 | **Standalone branch review** | Review current contents and history of one branch. Clarify: current state only / all commits on branch / comparison against intended base — ask if unclear. |
| 4 | **PR, commit, or commit-range review** | Determine exact commit range, PR base, and intended behavior. Review the complete relevant diff and validate against existing tests and call sites. |

### Code Review Clarity Checklist (Ask User First)

Before executing the review, confirm:
- **What is the review target?** (Entire repo / branch name / PR number / commit range)
- **If branch-to-branch:** What is the source branch and target branch?
- **What is the primary concern?** (Security, correctness, performance, full-spectrum, pre-release gate)
- **Are fixes requested, or is this a read-only audit?**

---

## Step 2 — Gather Business and Product Context

Before deep code review:

1. Look for PRD, FRD, specifications, architecture documents, acceptance criteria, design documents, issue references, and task descriptions in the repository (typically in `docs/`, `README.md`, or inline comments).
2. If a ClickUp connector or task reference is available, use the `clickup` skill to retrieve the relevant ClickUp task information.
3. If PRD/FRD/ClickUp is unavailable, inaccessible, or not supplied — **state that product context is unavailable and continue**. Do not block.
4. **Always inspect the codebase regardless of whether product documentation exists.**
5. Use PRD/FRD/task context to validate intended behavior, acceptance criteria, non-functional requirements, and business risks.
6. If requirements conflict with implementation or are materially ambiguous, explain the conflict and ask the user for direction rather than assuming intent.

---

## Step 3 — Define Scope and Create a Review Plan

After clarifying scenario and collecting context:

1. State the review target, comparison base (where relevant), known requirements, assumptions, and evidence limitations.
2. Create a concise internal task plan covering:
   - Source code and architecture review
   - Security and secrets review
   - Reliability and correctness review
   - Performance and optimization review
   - Git/GitHub and delivery-pipeline review
   - Test and validation review
   - Report generation (Markdown + PDF)
3. Identify high-risk modules first: authentication, authorization, payments/costly API calls, file upload/download, storage, queues, background workers, persistence, migrations, external integrations, infrastructure, and CI/CD.
4. Use `rg` / `rg --files`, Git metadata, dependency manifests, lockfiles, Docker/IaC, route registration, migrations, test discovery, and targeted static inspection.
5. Read sufficient surrounding code, call paths, tests, and configuration to prove every reported finding.

---

## Step 4 — Mandatory Review Areas

### 4.1 Correctness and Bug Detection

- Input validation and boundary handling
- Incorrect state transitions
- Missing transactions, rollback behavior, and partial commits
- Race conditions, deadlocks, thread/process safety, and distributed locking
- Idempotency and duplicate delivery handling
- Retries, retry amplification, timeout behavior, cancellation, and recovery
- Queue, worker, scheduler, and background-job failure modes
- Data loss, data corruption, stale data, cache invalidation, and migration defects
- Error handling that masks failures or leaves systems in stuck states
- Resource cleanup: file handles, streams, DB sessions, network clients, locks, temp files, memory, worker lifecycle
- API contract mismatches between frontend/backend/services
- Business-rule deviations from PRD/FRD/ClickUp acceptance criteria when available

### 4.2 Security, Authentication, Privacy, and Authorization

- Missing or weak authentication
- Missing authorization, role checks, tenant isolation, or object-level access control
- Public exposure of internal or admin endpoints
- Artifact/download authorization and presigned URL exposure
- CORS misuse — never treat CORS as authentication
- CSRF where cookie/session authentication is used
- Secrets in source code, `.env` examples, logs, Docker images, build output, Git history, issues, PRs, or documentation
- API keys, tokens, passwords, SSH keys, certificates, private keys, connection strings, and cloud credentials
- Injection risks: SQL, shell, template, LDAP, command, path traversal, unsafe deserialization, XSS, SSRF, insecure file handling
- TLS, encryption at rest, insecure HTTP, weak certificate validation, and unsafe trust settings
- Least privilege for cloud, database, storage, queue, and CI credentials
- Sensitive data handling, PII retention, deletion, encryption, access logs, and audit trails
- Publicly exposed databases, object stores, dashboards, admin consoles, queues, debug endpoints, and metrics endpoints

### 4.3 Git, GitHub, and Delivery Controls

- Current working tree and all reachable Git history (when full-history review is requested)
- `.gitignore`, `.dockerignore`, `.npmignore`, packaging manifests, and deployment exclusion files
- Secrets/sensitive artifacts accidentally committed or incorrectly excluded
- Large binaries, database dumps, backups, `.env` files, tokens, private keys, generated reports, and confidential documents
- Dependency lockfiles and reproducible build controls
- CI/CD workflows: security scanning, test gates, image scanning, dependency scanning, SBOM generation, release procedures, and deployment checks
- Branch protections, CODEOWNERS, PR review controls, secret scanning, Dependabot, and security settings — **only when GitHub access/tooling is available and authorized**
- **Never claim GitHub settings were inspected if no authorized GitHub integration exists**

### 4.4 Performance, Optimization, and Cost

- Unbounded request bodies, files, pagination, query limits, recursion, loops, queues, or memory growth
- N+1 queries, repeated scans, full table reads, missing indexes, expensive aggregations, and poor query patterns
- Blocking I/O or CPU work on request/event-loop paths
- Excessive serialization, repeated network calls, duplicate processing, unnecessary object-store downloads, and cache misses
- Memory leaks, file descriptor leaks, connection-pool leaks, thread leaks, temp-file leaks, and unbounded worker resource use
- Retry storms, rate-limit failures, API quota exhaustion, and expensive external-call amplification
- Cache correctness, invalidation, cache-key completeness, and stale-result behavior
- Observability of latency, throughput, failures, resource usage, and cost
- Report optimization opportunities only when evidenced and meaningful; do not report micro-optimizations as defects

### 4.5 Architecture, Modularity, and Technical Debt

- Clear separation of API, domain, persistence, infrastructure, UI, workers, and integrations
- Circular dependencies, leaky abstractions, duplicated business logic, overly large modules, unclear ownership, and hidden side effects
- Contracts/interfaces that are missing, misleading, or unenforced
- Configuration validation and environment-specific safety
- Dead code, stale feature flags, outdated documentation, obsolete migrations, and deprecated dependencies
- Comments and docstrings:
  - **Require** comments/documentation for non-obvious invariants, concurrency assumptions, security decisions, business rules, and operational tradeoffs
  - **Do not report** missing comments for trivial or self-explanatory code
  - **Flag** comments that are inaccurate, misleading, or contradict implementation
- Report maintainability issues only when they materially increase defect risk, operational risk, or future change cost

### 4.6 Testing and Validation

- Use the existing test suite when available.
- Run safe, relevant unit tests, integration tests, type checks, linting, builds, and smoke tests when dependencies and permissions allow.
- Inspect `tests/` directory for material coverage gaps.
- **For UI applications:**
  - Use Playwright for UI automation testing when Playwright MCP tooling is connected and the environment is safe.
  - Otherwise inspect UI behavior through code and existing tests.
  - If appropriate and explicitly authorized, write separate non-production test cases; do not modify application code unless requested.
- **For APIs:** Test authentication, authorization, validation, failure behavior, rate limits, and critical happy paths where safely possible.
- **For worker/queue systems:** Test idempotency, retries, crash recovery, concurrency, cancellation, and failure handling where feasible.
- Clearly distinguish in the report:
  - Tests actually run and **passed**
  - Tests actually run and **failed**
  - Tests that **could not run** (with exact blocker)
  - **Proposed smoke tests** not yet run

---

## Step 5 — Finding Qualification and Severity

Only report findings that are:

- Concrete and actionable
- Demonstrated by code, configuration, history, tests, or safe validation
- Relevant to correctness, security, privacy, performance, reliability, cost, or meaningful maintainability
- Not duplicates of another root-cause finding

**Do not report:** style nits, unproven theoretical attacks, intentional tradeoffs without a concrete downside, or vague "could be improved" observations.

| Severity | Definition |
|---|---|
| **P0** | Universal release blocker, active critical security exposure, likely irreversible corruption, or catastrophic data loss. |
| **P1** | Urgent security, privacy, reliability, correctness, or cost issue that should be fixed before production use. |
| **P2** | Material bug, operational risk, hardening gap, performance problem, or technical debt with a clear remediation. |
| **P3** | Lower-impact but worthwhile issue that should be scheduled. |

See [references/finding_severity_guide.md](references/finding_severity_guide.md) for the exact finding format template.

---

## Step 6 — Markdown Report Structure

Output file: `reports/repository-audit-YYYY-MM-DD.md`

The report must contain in order:

1. **Cover metadata** — Repository/project name, Company (Quantal AI), audited target and revision/branches, date, review scenario, available PRD/FRD/ClickUp context, validation status.
2. **Executive summary**
3. **Scope and methodology**
4. **Findings** — ordered P0 through P3, using the exact finding format below.
5. **Prioritized remediation order**
6. **Validation summary** — commands/tests run, passed/failed/blocked status, exact blockers.
7. **Test gaps and residual risks**
8. **Git/history and technical-debt observations**

### Exact Finding Format (required for every finding)

```markdown
### [P1] Imperative finding title

**Evidence:** Exact file path and line reference, relevant commit/branch context where
applicable, and demonstrated call path or scenario.

**Blast radius:** Explain affected users, services, data, cost, security/privacy
impact, deployment impact, and triggering scenario.

**Remediation:** Describe the smallest safe fix, affected components, rollout/migration
concerns, backward compatibility concerns, and any required operational changes.

**Prompt for a coding agent:**
> Specific implementation prompt. Must name relevant components, preserve intended
> behavior, request focused regression tests, request appropriate security/performance
> validation, and state what must not be changed.

**Smoke test:** Exact focused validation steps. Include the repaired happy path and at
least one failure, authorization, regression, or boundary case.
```

---

## Step 7 — Standardized Professional PDF Report

Output file: `reports/repository-audit-YYYY-MM-DD.pdf`

Generate the PDF from the Markdown report using the fixed visual system defined in [references/pdf_visual_system.md](references/pdf_visual_system.md).

### PDF Validation Checklist (run after generation)

- Verify file creation with `file` or `pdfinfo`
- Verify correct page size and page count
- Extract text with `pdftotext` when available to confirm readable content
- Visually confirm:
  - Cover page contains **only** project/repository name and `Quantal AI` — nothing else
  - Headers and footers do not overlap content
  - Page numbers appear on every interior page
  - Severity colors are consistent (P0/P1 red, P2 amber, P3 teal)
  - Margins and typography are consistent
  - Finding panels and labels are readable
- Report any PDF-generation or validation blocker clearly

---

## Final Response Requirements

Lead with links to both the Markdown and PDF reports. Then provide:

- Total findings count by severity (P0/P1/P2/P3)
- Concise summary of P0 and P1 findings
- Confirmation of review scenario and audited target
- Whether PRD/FRD/ClickUp context was available
- Validation commands that passed, failed, or were blocked
- A statement that **no application code was changed** unless the user explicitly requested fixes

**Do not imply** a test, GitHub check, ClickUp lookup, PDF visual review, or security scan occurred unless it actually occurred.

---

## References

- [references/pdf_visual_system.md](references/pdf_visual_system.md) — Fixed color palette, typography, page geometry, cover spec, header/footer spec, and validation checklist.
- [references/finding_severity_guide.md](references/finding_severity_guide.md) — P0–P3 definitions, qualification rules, and exact finding format template.
- [examples/sample_audit_report.md](examples/sample_audit_report.md) — Sample findings in correct format (P0 through P3).
