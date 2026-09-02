# Mapping Compliance Findings onto a document-generation Manifest

`document-generation`'s manifest schema is defined in
[../../document-generation/references/manifest_schema.md](../../document-generation/references/manifest_schema.md).
Build the manifest from the same content already written into the Markdown
report — do not re-derive it separately.

## Status → `level` (NOT priority → `level`)

The panel's `level` encodes **compliance status**, never P0–P3 priority — the
two are independent scales (see `finding_severity_guide.md`). Priority is
shown only as a `[P_]` prefix in the panel `title`, exactly like `code-review`
already does for its own severity prefix.

| Compliance Status | `level` |
|---|---|
| Non-Compliant | `critical` |
| Partially Compliant | `warning` |
| Compliant | `default` |
| Not Verifiable From Code | `info` |
| Not Applicable (AI-only item, no AI/ML detected) | `info` |

A panel title therefore looks like:
`"[P1] [NON-COMPLIANT] TLS not enforced on PHI transport"` — the bracketed
priority is informational ordering, the bracketed status is the actual
`level`-bearing fact.

## Top-level fields

```json
{
  "report_type": "HIPAA COMPLIANCE AUDIT",
  "cover": {"title": "<repository/project name>", "subtitle": "Quantal AI"},
  "footer_text": "CONFIDENTIAL - Quantal AI Internal Compliance Review",
  "metadata_table": [
    {"label": "Repository", "value": "..."},
    {"label": "Scan Date", "value": "..."},
    {"label": "AI/ML Components Detected", "value": "Yes | No"},
    {"label": "Checklist Version", "value": "compliance_checklist.md, this skill's revision"}
  ],
  "sections": [ ... ]
}
```

## Sections, in order

1. **Standing disclosure** — always first, before anything else:
   ```json
   {"type": "disclosure", "text": "This report is an automated code/configuration scan, not a legal compliance certification and not legal advice. Panel colors denote compliance status (red = non-compliant, amber = partial, blue = compliant, gray = not verifiable from code), not code-defect severity. Bracketed [P_] labels are remediation priority, independent of status."}
   ```

2. **Business Associate Agreements** — always present, always its own heading, never folded into the checklist table:
   ```json
   {"type": "heading", "text": "Business Associate Agreements"},
   {"type": "paragraph", "text": "This scan does not and cannot verify whether Business Associate Agreements (BAAs) are signed with every vendor/subprocessor that creates, receives, maintains, or transmits PHI on this system's behalf (e.g. cloud host, LLM/AI API provider, analytics tools, email/notification services). Confirming signed BAAs covering the actual data flows in this deployment is the sole responsibility of the organization operating this system, before any real PHI reaches it. This is a legal/contractual determination outside the scope of any codebase scan."}
   ```

3. **Executive Summary** — `heading` + `paragraph`, then one `panel` per Non-Compliant/Partially-Compliant item, P0 → P3 order, using the same panels as section 5 (do not duplicate content differently — reference by reusing the identical panel object).

4. **AI/ML Component Detection** — `heading` + `paragraph` stating what was found (or "No AI/ML components detected; Category G and all `AI-only` items are marked Not Applicable below.").

5. **Full Checklist Walkthrough** — one `heading` per category (A–H from `compliance_checklist.md`), then one `panel` per item in that category, in the exact-finding-format fields:
   ```json
   {
     "type": "panel",
     "level": "critical",
     "title": "[P1] [NON-COMPLIANT] TLS not enforced on PHI transport",
     "fields": [
       {"label": "Requirement", "body": "45 CFR §164.312(e) — PHI must be encrypted in transit. ..."},
       {"label": "Status", "body": "Non-Compliant"},
       {"label": "Evidence", "body": "src/integrations/labResults.client.ts:L14 — base URL configured as http://... (structural reference only, no data values)"},
       {"label": "Why it matters", "body": "..."},
       {"label": "Remediation", "body": "..."}
     ]
   }
   ```
   Compliant items use the same shape with `level: "default"` and omit the `Remediation` field. Not-Verifiable/Not-Applicable items do **not** get a panel — list them in a `table` instead (see next).

6. **Not Verifiable From Code** — one `table` with columns `["Item", "Category", "Why it can't be verified from code"]`, covering every item scored that way plus Category H absences.

7. **Proposed / Regulatory Horizon** — `heading` + `paragraph` making clear these are not current law, then a `table` (`["Proposed change", "Current status", "Related checklist item"]`) from `compliance_checklist.md`'s final bucket.

Do not add any other `disclosure` sections — the one standing disclosure at
the top covers both the status/priority distinction and the "not legal
advice" caveat; repeating it dilutes the one that matters.
