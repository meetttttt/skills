# Finding Status, Priority, and Format Guide

## Two independent scales — do not conflate them

Every checklist item gets a **compliance status** (what it *is*). Every
**Non-Compliant** or **Partially Compliant** item additionally gets a
**priority** (how urgently it should be fixed, used only to order the
executive summary). These are independent axes — a P3 item is still
Non-Compliant, not a lesser degree of compliant.

### Compliance Status (4-state)

| Status | Meaning |
|---|---|
| **Compliant** | The checklist item's compliant criteria are met, evidenced by code/config. |
| **Non-Compliant** | The checklist item's non-compliant criteria are met — a concrete gap exists. |
| **Partially Compliant** | The control exists but is inconsistently applied (see the item's own "Partially compliant" criteria where defined). |
| **Not Verifiable From Code** | The item cannot be assessed by scanning this repository — requires human/organizational verification. Includes every BAA-related item, all of Category H when no artifact is found, and any item where the relevant system lives entirely outside this codebase. |

**Not Applicable** is a fifth, separate label used only for `AI-only` checklist
items when Step 1's AI/ML detection found no AI/ML components — it means the
item doesn't apply to this codebase at all, not that it's unverifiable.

### Priority (P0–P3) — for Non-Compliant / Partially Compliant items only

Reuses this repository's `code-review` P0–P3 scale, applied to compliance risk
instead of bug severity:

| Priority | Definition | HIPAA examples |
|---|---|---|
| **P0** | PHI is actively exposed or unprotected right now with a trivial trigger. | Unauthenticated endpoint returning full patient records; PHI logged in plaintext to a third-party observability tool; hardcoded production DB credential in tracked source. |
| **P1** | Serious gap that should be fixed before this code handles real PHI in production. | No TLS on a PHI-carrying call; missing object-level authorization (any user can fetch any patient by ID); no audit logging on PHI writes. |
| **P2** | Real gap with a clear remediation, not immediately catastrophic. | Session timeout unbounded; backups unencrypted; AI prompt sends a whole record instead of needed fields. |
| **P3** | Lower-impact hardening gap or a control that's inconsistently applied. | MFA missing on one internal admin tool while present elsewhere; incident-response doc absent from repo (may exist elsewhere). |

Compliant and Not-Verifiable-From-Code items never get a priority — they are
not actionable gaps.

---

## PHI Redaction Rule (mandatory, no exceptions)

This is the compliance-report equivalent of `code-review`'s "No secret
disclosure" rule:

- **Never quote a PHI-shaped data value** in a finding — no patient names, no
  SSN/MRN-looking strings, no diagnosis text, no full record dumps — even if
  it's obviously synthetic test data, even if redacting feels like it weakens
  the evidence.
- Evidence must quote **structural code only**: schema/field declarations,
  function signatures, config keys, the logging/HTTP call site itself. Elide
  the data literal with `[REDACTED]` or describe its shape ("a literal
  9-digit numeric string assigned to `ssn`") instead of reproducing it.
- If a finding is about a log statement printing PHI, quote the `logger.info(...)`
  call, not sample output it would produce.
- This rule applies identically in the Markdown report and the PDF manifest —
  there is no lower-sensitivity context where quoting real-looking PHI is
  acceptable.

---

## Qualification Rules

Only report a Non-Compliant or Partially Compliant finding if:

- **Concrete**: demonstrated by actual code/config, not inferred from absence of evidence alone (absence → Not Verifiable, not Non-Compliant, unless the checklist item's own criteria explicitly treat absence as non-compliant, e.g. D1/E1/E3).
- **In-scope**: maps to one of the checklist items in `compliance_checklist.md`.
- **Actionable**: has a concrete remediation direction.
- **Non-duplicate**: not the same root cause already reported under another item.

**Never report**: theoretical AI attack scenarios with no evidence in this
codebase, general HIPAA education unconnected to a specific checklist item, or
findings based on guessing what a third-party vendor does internally.

---

## Exact Finding Format (required for every Non-Compliant / Partially Compliant / Compliant item that gets its own panel)

```markdown
### [P_] [STATUS] Checklist item title

**Requirement:** Plain-language statement of the HIPAA rule this item covers, with its §164.xxx citation.

**Status:** Compliant | Non-Compliant | Partially Compliant

**Evidence:** File path(s) and line reference(s), quoting structural code only per the PHI Redaction Rule above.

**Why it matters:** The concrete risk this gap creates — what could go wrong, for whom, under what trigger condition. (For Compliant items, state briefly why the evidence satisfies the requirement.)

**Remediation:** The smallest concrete fix — name the file/function/config to change. Omit for Compliant items.
```

Not-Verifiable-From-Code items do not get this panel format — list them in a
simple table (Item, Why it can't be verified from code) per `SKILL.md`'s
report structure.

---

## Finding Ordering

1. Executive summary: Non-Compliant and Partially Compliant items only, P0 → P3, most critical first.
2. Full checklist walkthrough: in `compliance_checklist.md` category order (A → H), regardless of status — so a reader can see the complete picture per category, not just the failures.
