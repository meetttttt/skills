# HIPAA Compliance Checklist (Code/Config-Verifiable)

Every item below is written to be checked by reading a codebase — source, config,
infrastructure-as-code, CI/CD, and dependency manifests. Items HHS enforces but
that no code scan can ever verify (signed BAAs, workforce training records,
sanctions policy enforcement, incident-response drills actually run) are **not**
in this list — see `SKILL.md`'s dedicated "Business Associate Agreements" and
"Organizational Items — Not Verifiable From Code" sections instead. Do not
score those against the repository.

For every item marked `AI-only: yes`, only evaluate it if Step 1 of `SKILL.md`
(AI/ML component detection) found LLM/ML components in the codebase; otherwise
mark it `Not Applicable` and say why in one line.

Citations refer to 45 CFR. Where a control is a proposed (not yet final) rule,
that is called out explicitly — see the "Proposed / Regulatory Horizon" bucket
at the end of this file, never mixed into the scored checklist.

---

## A. Access Control & Authentication — §164.312(a), §164.312(d)

### A1. Unique identity per user/service accessing PHI
- **Requirement**: Every human user and every service/API client that can reach PHI must be individually identifiable — no shared logins, no shared API keys used by multiple humans.
- **Look for**: hardcoded shared credentials, a single "admin" account used app-wide, service accounts shared across environments/teams.
- **Compliant**: Each user/service has a distinct identity (DB row, IdP account, or per-service credential).
- **Non-compliant**: A single shared credential is used for multiple humans or multiple unrelated services to reach PHI-handling code paths.
- **Code-verifiable**: yes

### A2. Authentication enforced on PHI-handling endpoints/functions
- **Requirement**: No route, RPC, or function that reads/writes PHI may be reachable without authentication.
- **Look for**: route definitions/middleware chains for endpoints touching patient/health data models; any route explicitly marked public/no-auth that also touches those models.
- **Compliant**: Every PHI-touching route/function sits behind an auth middleware/decorator.
- **Non-compliant**: At least one PHI-touching route/function has no authentication check on its call path.
- **Code-verifiable**: yes

### A3. Authorization / access-control checks beyond authentication
- **Requirement**: Being logged in is not sufficient — the caller must be authorized for the specific patient/record (role checks, tenant isolation, object-level ownership checks).
- **Look for**: whether handlers that fetch a record by ID also verify the caller is permitted to see that specific record (not just "any authenticated user").
- **Compliant**: Object-level/role-based authorization checks exist before returning or mutating PHI.
- **Non-compliant**: Any authenticated user can access any patient's record by ID with no ownership/role check (IDOR-style gap).
- **Code-verifiable**: yes

### A4. Session timeout / automatic logoff
- **Requirement**: Sessions with access to PHI must expire after inactivity.
- **Look for**: session/cookie/JWT configuration for `maxAge`/`expiresIn`/idle-timeout settings.
- **Compliant**: A finite, reasonable session/token expiry is configured.
- **Non-compliant**: Sessions/tokens are configured with no expiry, or an expiry effectively unbounded (e.g. years).
- **Code-verifiable**: yes

### A5. Multi-factor authentication available for privileged/PHI-admin access
- **Requirement**: Accounts with broad PHI access (admin panels, support tooling, data-export functions) should support MFA.
- **Look for**: auth provider config/SDK usage; presence or absence of an MFA/2FA step for admin or bulk-export paths.
- **Compliant**: MFA is implemented or delegated to an identity provider that enforces it for privileged roles.
- **Partially compliant**: MFA exists for some privileged surfaces but not others (e.g., web admin has it, an internal CLI/script bypasses it).
- **Non-compliant**: No MFA path exists anywhere for privileged/PHI-admin access.
- **Code-verifiable**: yes
- Note: current Security Rule treats this as "addressable"; see Proposed/Regulatory Horizon bucket for the pending change.

---

## B. Audit Controls — §164.312(b)

### B1. Audit logging of PHI access and mutation
- **Requirement**: Every read/create/update/delete of PHI must be logged with who, what, and when.
- **Look for**: logging/audit middleware around PHI data-access layers (repositories/DAOs/ORM hooks); absence of any audit trail around those layers.
- **Compliant**: PHI-touching operations write an audit record (actor, action, record identifier, timestamp).
- **Partially compliant**: Some PHI operations are audited (e.g. writes) but others are not (e.g. reads/exports).
- **Non-compliant**: No audit logging exists around PHI access at all.
- **Code-verifiable**: yes

### B2. Logs do not contain raw PHI
- **Requirement**: Application/audit logs must not contain PHI values in plaintext.
- **Look for**: `log`/`console`/`print`/logger calls that interpolate patient name, DOB, SSN, MRN, diagnosis, or full record objects directly into log output.
- **Compliant**: Logs reference records by non-identifying ID only; PHI fields are redacted/omitted from log statements.
- **Non-compliant**: At least one log statement writes a raw PHI field or a whole PHI object to logs/stdout/observability tooling.
- **Code-verifiable**: yes
- **Evidence rule**: quote only the logging call site (the code), never the actual data value that would be printed — see `finding_severity_guide.md`'s PHI redaction rule.

### B3. Audit logs are tamper-resistant / not trivially deletable by the same actors they audit
- **Requirement**: Audit trails should not be alterable by the standard application role being audited.
- **Look for**: whether audit-log writes go to an append-only store/table separate from normal CRUD permissions, or whether the same DB role that can edit PHI can also edit/delete its own audit rows.
- **Compliant**: Audit records are append-only or write-restricted separately from normal application data permissions.
- **Non-compliant**: Audit records live in a normal, fully-mutable table with no separate write protection.
- **Code-verifiable**: yes

---

## C. Integrity Controls — §164.312(c)

### C1. Protection against improper alteration/destruction of PHI
- **Requirement**: Mechanisms must exist to detect or prevent unauthorized modification of PHI records.
- **Look for**: DB constraints, checksums/hashes, optimistic locking/versioning columns, soft-delete vs hard-delete patterns on PHI tables/models.
- **Compliant**: At least one integrity mechanism (versioning, constraints, checksum, or soft-delete with audit trail) protects PHI records.
- **Non-compliant**: PHI records can be silently overwritten or hard-deleted with no trace and no constraint enforcement.
- **Code-verifiable**: yes

### C2. Input validation on PHI-related fields
- **Requirement**: PHI-bearing inputs must be validated before persistence to prevent corruption or injection.
- **Look for**: schema/validation layers (e.g. Zod/Pydantic/Joi/Bean Validation) applied to PHI models; raw unchecked writes from request bodies straight to the PHI store.
- **Compliant**: A validation layer sits between input and PHI persistence.
- **Non-compliant**: Request data is written to PHI storage with no validation layer.
- **Code-verifiable**: yes

---

## D. Transmission Security — §164.312(e)

### D1. TLS enforced for external transmission of PHI
- **Requirement**: PHI must never travel over plaintext HTTP.
- **Look for**: HTTP client base URLs using `http://` instead of `https://` where PHI is in the request/response; disabled certificate verification (`verify=False`, `rejectUnauthorized: false`, `NODE_TLS_REJECT_UNAUTHORIZED=0`, `InsecureSkipVerify: true`).
- **Compliant**: All PHI-carrying network calls use HTTPS/TLS with certificate verification enabled.
- **Non-compliant**: Any PHI-carrying call uses plain HTTP, or has certificate verification disabled.
- **Code-verifiable**: yes

### D2. TLS enforced for internal/service-to-service PHI transmission
- **Requirement**: Same as D1, applied to internal microservice/queue/database traffic that carries PHI, where the platform doesn't already guarantee an encrypted private network.
- **Look for**: internal service client configs, message-queue connection strings (`amqp://` vs `amqps://`), DB connection strings without `sslmode=require`/`ssl=true`.
- **Compliant**: Internal PHI-carrying connections are encrypted, or documented as running on a provider-guaranteed encrypted private network.
- **Partially compliant**: Encrypted for some internal hops but not others.
- **Non-compliant**: Internal PHI-carrying traffic is unencrypted with no compensating documented network guarantee.
- **Code-verifiable**: yes

### D3. AI/LLM API calls carrying PHI use TLS and an enterprise-tier endpoint
- **Requirement**: If PHI is sent to an LLM/AI API, that transmission must be encrypted, and should target an enterprise/HIPAA-eligible endpoint rather than a consumer-tier one. (Whether a signed BAA is actually in place is out of scope — see the BAA section.)
- **Look for**: LLM SDK/API base URLs and whether PHI-shaped data (patient records, clinical notes) is passed into prompt/request payloads.
- **Compliant**: Calls use HTTPS and target a vendor's enterprise/business API tier.
- **Partially compliant**: Calls use HTTPS but target a consumer-tier endpoint/product with PHI in the payload.
- **Non-compliant**: PHI is sent to an LLM API over plaintext, or with certificate verification disabled.
- **Code-verifiable**: yes
- **AI-only**: yes

---

## E. Encryption at Rest — §164.312(a)(2)(iv)

### E1. Database/storage encryption at rest
- **Requirement**: PHI storage must be encrypted at rest.
- **Look for**: IaC/config for the database, object storage, or managed service (encryption flags/parameters in Terraform, CloudFormation, Docker Compose, ORM/connection config).
- **Compliant**: Encryption at rest is explicitly enabled in config/IaC, or the managed service used encrypts by default and that default is not disabled.
- **Non-compliant**: Encryption at rest is explicitly disabled, or self-managed storage has no encryption configuration at all.
- **Code-verifiable**: yes

### E2. Backups encrypted
- **Requirement**: Backup/export artifacts containing PHI must also be encrypted.
- **Look for**: backup scripts/jobs/cron configs and whether output is encrypted before being written to disk/object storage.
- **Compliant**: Backup pipeline encrypts output or writes to storage that encrypts at rest.
- **Non-compliant**: Backup/export routine writes unencrypted PHI dumps to disk or unencrypted storage.
- **Code-verifiable**: yes

### E3. No hardcoded secrets/credentials
- **Requirement**: Credentials that gate access to PHI (DB passwords, API keys, encryption keys) must not be hardcoded in source.
- **Look for**: literal credential-shaped strings in source files vs use of environment variables/secret managers.
- **Compliant**: Secrets are loaded from environment variables, a secret manager, or a gitignored local config.
- **Non-compliant**: A live-looking credential is hardcoded in a tracked source file.
- **Code-verifiable**: yes
- **Evidence rule**: report the file/line and variable name only — never the secret value itself (same rule as `code-review`'s "No secret disclosure").

---

## F. Minimum Necessary & Data Handling — §164.502(b), §164.514

### F1. No PHI hardcoded in source, fixtures, or seed data
- **Requirement**: Realistic-looking PHI (real or plausible SSNs, MRNs, patient names tied to real conditions) should not live in tracked source, test fixtures, or seed scripts.
- **Look for**: fixture/seed files with PHI-shaped literal data.
- **Compliant**: Fixtures use clearly synthetic/placeholder data (e.g. `Jane Test`, `000-00-0000` patterns marked as fake).
- **Non-compliant**: Fixture/seed data contains realistic, unlabeled PHI-shaped values.
- **Code-verifiable**: yes
- **Evidence rule**: cite the file/field name only, never reproduce the literal value in the report.

### F2. AI/LLM prompts send only necessary fields
- **Requirement**: When PHI is passed into an LLM prompt or agent context, only the fields the task actually needs should be included — not a full patient record dumped into every call.
- **Look for**: how PHI objects are serialized into prompt/request payloads — whole-object dumps vs field-selected payloads.
- **Compliant**: Prompt construction selects specific needed fields.
- **Non-compliant**: A full PHI record/object is serialized wholesale into every LLM call regardless of task.
- **Code-verifiable**: yes
- **AI-only**: yes

### F3. De-identification before training/analytics use
- **Requirement**: If PHI is used to train/fine-tune a model or feed bulk analytics, it should be de-identified first (Safe Harbor or Expert Determination) unless the full Security Rule is otherwise applied to that pipeline.
- **Look for**: training/fine-tuning/data-export scripts and whether they call a de-identification/anonymization step before use.
- **Compliant**: A de-identification step precedes training/analytics use, or the training pipeline is documented as running under full Security Rule controls.
- **Non-compliant**: Raw PHI is fed directly into a training/fine-tuning/bulk-analytics pipeline with no de-identification step and no compensating controls.
- **Code-verifiable**: yes
- **AI-only**: yes

---

## G. AI/ML-Specific Risk Controls (evaluate only if AI/ML detected)

### G1. Cross-tenant / cross-patient isolation in AI context construction
- **Requirement**: RAG/context-building code must not let one patient's or tenant's data leak into another's AI session.
- **Look for**: how retrieval/context-building code scopes queries — filtered by patient/tenant ID vs global retrieval.
- **Compliant**: Context/retrieval queries are scoped to the requesting patient/tenant.
- **Non-compliant**: Retrieval/context code has no patient/tenant filter, or the filter is applied after retrieval rather than as part of the query.
- **Code-verifiable**: yes
- **AI-only**: yes

### G2. Human-in-the-loop review for AI-generated clinical content
- **Requirement**: AI-generated notes, summaries, or decisions that affect patient care or get filed in a record should pass through a review/approval step before being persisted or acted on.
- **Look for**: whether AI output is written directly to the record/sent to the patient with no intermediate approval step, vs a draft/pending-review state.
- **Compliant**: AI output lands in a draft/pending state requiring human approval before being finalized.
- **Partially compliant**: Some AI-output paths are gated, others auto-finalize.
- **Non-compliant**: AI-generated clinical content is auto-persisted/auto-sent with no review step.
- **Code-verifiable**: yes
- **AI-only**: yes

### G3. Output filtering against PHI leakage in AI responses
- **Requirement**: Guardrails should exist to catch a model reproducing PHI it shouldn't (memorized training data, cross-context bleed) before it reaches the end user.
- **Look for**: any output-filtering/guardrail step between model response and what's returned to the caller.
- **Compliant**: An output filter/guardrail step exists on the AI response path.
- **Non-compliant**: Model output is returned to the caller with no filtering step at all.
- **Code-verifiable**: yes
- **AI-only**: yes

---

## H. Administrative Artifacts Visible in the Repo — §164.308

These are administrative safeguards that mostly live outside any codebase — score them cautiously. Absence of evidence in the repo means **Not Verifiable From Code**, not **Non-Compliant**, since the artifact may legitimately live in an external system (wiki, GRC tool, HR system).

### H1. Documented incident response / breach procedure
- **Look for**: `SECURITY.md`, `docs/incident-response*`, or equivalent.
- **Compliant**: Present in-repo with concrete steps.
- **Not verifiable from code**: Absent from the repo (may exist elsewhere).
- **Code-verifiable**: partial — can only confirm presence, never confirm real-world execution.

### H2. AI system inventory / data-flow documentation
- **Look for**: any README/docs enumerating which AI systems/vendors touch PHI and how.
- **Compliant**: Present and appears current.
- **Not verifiable from code**: Absent from the repo.
- **Code-verifiable**: partial.
- Note: becoming a formal expectation under the pending Security Rule NPRM — see Proposed/Regulatory Horizon bucket.

---

## Proposed / Regulatory Horizon (track only — do not score as compliant/non-compliant)

List these in their own report bucket, clearly labeled as **not yet in force**:

- Mandatory MFA (currently "addressable" under the Security Rule; a 2025 NPRM proposes making it required) — relates to A5.
- Formal written inventory of every AI system that creates/receives/maintains/transmits ePHI, reviewed as part of ongoing risk analysis — relates to H2.
- Reduced "addressable" flexibility generally for encryption, asset inventories, and audit controls under the same proposed rule.

Do not present any of the above as current law. If the report is likely to be handed to counsel or compliance staff, this distinction matters.
