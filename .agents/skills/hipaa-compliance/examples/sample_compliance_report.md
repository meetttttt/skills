# Sample HIPAA Compliance Findings

Worked examples of the exact finding format from `references/finding_severity_guide.md`,
covering all status values, plus the always-present BAA section from
`references/manifest_mapping.md`. This is illustrative only — every real
report's findings must come from an actual scan of the target codebase.

---

## Business Associate Agreements

> This scan does not and cannot verify whether Business Associate Agreements
> (BAAs) are signed with every vendor/subprocessor that creates, receives,
> maintains, or transmits PHI on this system's behalf (e.g. cloud host,
> LLM/AI API provider, analytics tools, email/notification services).
> Confirming signed BAAs covering the actual data flows in this deployment is
> the sole responsibility of the organization operating this system, before
> any real PHI reaches it. This is a legal/contractual determination outside
> the scope of any codebase scan.

---

## Full Checklist Walkthrough (excerpt)

### [P1] [NON-COMPLIANT] TLS not enforced on PHI transport

**Requirement:** 45 CFR §164.312(e) — PHI must be encrypted during transmission over an electronic communications network.

**Status:** Non-Compliant

**Evidence:** `src/integrations/labResults.client.ts:L14` — base client URL configured as `http://internal-lab-api/...` (structural reference only; no request/response data reproduced).

**Why it matters:** Lab result payloads containing PHI travel over plaintext HTTP between this service and the lab integration. Any network position between the two (shared VPC, misconfigured proxy, compromised host) can read PHI in transit.

**Remediation:** Change the base URL to `https://` and confirm the lab API supports TLS 1.2+; if it doesn't, route through a TLS-terminating proxy rather than sending plaintext.

---

### [P2] [PARTIALLY COMPLIANT] AI prompt construction sends full patient record

**Requirement:** 45 CFR §164.502(b) — Minimum Necessary Standard; only send the PHI fields a task actually needs.

**Status:** Partially Compliant

**Evidence:** `src/ai/summarize.ts:L22` — `buildPrompt(patientRecord)` serializes the entire `patientRecord` object; a sibling function `buildDischargePrompt()` in the same file already does field-selection correctly.

**Why it matters:** The discharge-summary path already follows minimum-necessary; the general summarization path does not, and unnecessarily exposes unrelated PHI fields (e.g. billing/insurance data) to the LLM provider for tasks that don't need them.

**Remediation:** Apply the same field-selection pattern from `buildDischargePrompt()` to `buildPrompt()`, passing only the fields the specific summarization task requires.

---

### [P0] [NON-COMPLIANT] PHI written to shared application logs

**Requirement:** 45 CFR §164.312(b) — Audit Controls; logs must not expose PHI to anyone with log access.

**Status:** Non-Compliant

**Evidence:** `src/workers/intake.worker.ts:L57` — `logger.info('Processing intake', { patient })` passes the full `patient` object to the logger. `[REDACTED]` — actual field values are not reproduced in this report.

**Why it matters:** This worker's logs are shipped to a third-party observability platform. Every intake event currently writes full PHI (name, DOB, diagnosis fields) into that platform's plaintext log storage, reachable by anyone with log-viewer access, including staff with no clinical need to know.

**Remediation:** Replace `{ patient }` with `{ patientId: patient.id }` in the log call; if broader debugging context is needed, log a redacted/allowlisted subset of non-identifying fields only.

---

### [Compliant] Database encryption at rest configured

**Requirement:** 45 CFR §164.312(a)(2)(iv) — Encryption at rest for ePHI storage.

**Status:** Compliant

**Evidence:** `infra/terraform/rds.tf:L31` — `storage_encrypted = true`, `kms_key_id` set to a customer-managed key.

**Why it matters:** The primary PHI datastore is encrypted at rest with a customer-managed key, satisfying this control as evidenced by IaC configuration.

---

## Not Verifiable From Code (excerpt)

| Item | Category | Why it can't be verified from code |
|---|---|---|
| Workforce HIPAA training records | H (Administrative) | Training completion lives in an HR/LMS system, not this repository. |
| Incident response drills actually conducted | H (Administrative) | `SECURITY.md` describes a procedure, but whether it has been rehearsed is an organizational fact, not a code fact. |
| Signed BAA with LLM API provider | — (see dedicated BAA section above) | Contractual state; not discoverable from source code under any circumstance. |
