---
name: hipaa-compliance
description: >-
  Scan an entire codebase (source, config, infrastructure-as-code, CI/CD, and
  dependency manifests) against a fixed, code-verifiable HIPAA compliance
  checklist, and generate a standardized Markdown report plus a PDF rendered
  via the document-generation skill. Use when a user asks for a HIPAA
  compliance check, HIPAA audit, PHI handling review, or "is this codebase
  HIPAA compliant". Works on any project, healthcare-specific or not, and
  auto-detects whether AI/ML components are present before scoring
  AI-specific risk items. Explicitly does not and cannot verify Business
  Associate Agreements or any other organizational/legal artifact that lives
  outside the codebase — those are always called out as the reader's
  responsibility, never silently assumed.
---

# HIPAA Compliance Skill

A project-agnostic HIPAA compliance auditor. Scans a codebase against a fixed
checklist in [references/compliance_checklist.md](references/compliance_checklist.md),
produces an evidence-backed Markdown report, then hands the findings to the
`document-generation` skill to render the standardized PDF.

**This skill owns compliance content only — it does not implement PDF
layout, fonts, or colors.** That is owned by the separate `document-generation`
skill shared by every report-producing skill in this repo. See
[references/manifest_mapping.md](references/manifest_mapping.md) for how
checklist results become that skill's input.

**This skill is a standalone audit, not part of the main delivery chain** —
run it any time on any codebase, independent of `grill-me`/`prd-frd`/`implement`.

---

## Core Operating Rules

- **Read-only. Always.** This skill never modifies application code, even when a fix looks trivial. It only reports.
- **No PHI disclosure, ever.** Never quote a PHI-shaped data value (names, SSNs, MRNs, diagnoses, full record dumps) in a finding, the Markdown report, or the PDF — not even synthetic-looking test data. Quote structural code only (schema fields, function signatures, config keys, call sites). See `references/finding_severity_guide.md`'s PHI Redaction Rule.
- **No secret disclosure.** Never print an actual credential/API key value found during the scan — report only its location and that it's hardcoded, exactly like the `code-review` skill's equivalent rule.
- **No invention.** Every finding must be evidenced by actual code/config read during the scan. If something can't be verified from the codebase, say so explicitly — never guess or assume compliance or non-compliance.
- **BAAs are explicitly out of scope.** This skill never claims to check, imply, or infer whether a Business Associate Agreement is signed with any vendor. Every report contains a dedicated, unmissable section stating BAA verification is the reader's sole responsibility. See Step 5.
- **Not legal advice, not a certification.** Every report states this plainly. This is an automated code-level scan, not a HIPAA compliance certification and not a substitute for legal or compliance counsel review.
- **Ask when unsure.** If the codebase's nature (healthcare-adjacent or not, which parts touch PHI) is genuinely ambiguous after inspection, ask the user rather than guessing scope.

---

## Step 1 — Detect AI/ML Components

Before scoring anything, determine whether the codebase has AI/ML components,
since Category G and every checklist item marked `AI-only: yes` in
`references/compliance_checklist.md` only apply when this is true.

Look for signals such as:
- LLM/AI SDK imports or dependencies (OpenAI, Anthropic, Google Vertex/Gemini, Azure OpenAI, Bedrock, Hugging Face, LangChain, LlamaIndex, etc.) in dependency manifests or source.
- Direct HTTP calls to known LLM/AI API hosts.
- Model training/fine-tuning scripts, embedding generation code, or vector database usage (Pinecone, Weaviate, pgvector, FAISS, Chroma, etc.).
- RAG/context-retrieval code, prompt-construction modules, or an `agents`/`ml`/`models` directory pattern.

State the result plainly in the report (Section: "AI/ML Component Detection").
If none found, mark Category G and every `AI-only` item **Not Applicable** and
move on — do not force-fit AI risk language onto a non-AI codebase.

---

## Step 2 — Define Scan Surface

Scan the entire codebase as of its current working tree state:

- Application source code (all languages present).
- Configuration files (`.env.example`, YAML/JSON/TOML configs, feature flags).
- Infrastructure-as-code (Docker/Compose, Kubernetes manifests, Terraform/CloudFormation/Pulumi).
- CI/CD pipeline definitions (GitHub Actions, GitLab CI, CircleCI, etc.).
- Dependency manifests and lockfiles (to identify AI/ML libraries and known-vulnerable crypto/auth packages).
- Test fixtures and seed data (for hardcoded PHI-shaped literals — checklist item F1).

Do not scan git history for this skill's purpose unless the user explicitly
asks for a history-inclusive scan — default to current working tree, since
history mining is `code-review`'s job, not this skill's.

If the repository has no identifiable PHI-handling code path at all (no
patient/health/clinical data models, no healthcare-domain naming, no such
concepts anywhere), still produce the full report: state this finding clearly
up front, then walk the checklist marking nearly everything **Not Verifiable
From Code** or **Not Applicable**, rather than skipping report generation.
Never silently do nothing.

---

## Step 3 — Apply the Checklist

Work through every item in `references/compliance_checklist.md`, category by
category (A → H). For each item, determine one of:

- **Compliant** — evidence matches the item's compliant criteria.
- **Non-Compliant** — evidence matches the item's non-compliant criteria.
- **Partially Compliant** — control exists but is inconsistently applied.
- **Not Verifiable From Code** — cannot be assessed from this repository (BAA-adjacent items, Category H when no artifact is found, anything living entirely outside this codebase).
- **Not Applicable** — an `AI-only` item and Step 1 found no AI/ML components.

Assign a P0–P3 priority (see `references/finding_severity_guide.md`) to every
Non-Compliant or Partially Compliant item only. Compliant and
Not-Verifiable/Not-Applicable items never get a priority.

Use the exact finding format in `references/finding_severity_guide.md` for
every item that gets a panel (Compliant, Non-Compliant, Partially Compliant).
List Not-Verifiable/Not-Applicable items in a simple table instead.

---

## Step 4 — Markdown Report Structure

Output file: `reports/hipaa-compliance-<repo-slug>-YYYY-MM-DD.md`

The report must contain, in order:

1. **Cover metadata** — repository/project name, scan date, whether AI/ML components were detected, checklist version.
2. **Standing disclosure** — automated scan, not legal advice, not a certification; panel-color legend (status, not code-defect severity); `[P_]` = remediation priority, independent of status.
3. **Business Associate Agreements** — dedicated section, always present, stating this scan does not and cannot verify BAAs, and that confirming them is the operator's sole responsibility before real PHI reaches this system.
4. **Executive Summary** — every Non-Compliant/Partially-Compliant item, P0 → P3, most critical first. State "No compliance gaps identified" if none exist — do not omit the section.
5. **AI/ML Component Detection** — what was found, and which categories/items were consequently marked Not Applicable.
6. **Full Checklist Walkthrough** — category by category (A → H), every item, exact finding format, in category order regardless of status.
7. **Not Verifiable From Code** — table of every such item and why.
8. **Proposed / Regulatory Horizon** — table of not-yet-final rules from `compliance_checklist.md`, clearly labeled as proposed, not current law.

---

## Step 5 — Render the PDF via document-generation

Output file: `reports/hipaa-compliance-<repo-slug>-YYYY-MM-DD.pdf`

1. Convert the report into a `manifest.json` per
   [references/manifest_mapping.md](references/manifest_mapping.md) — status
   (not priority) drives panel `level`; priority is a `[P_]` prefix in the
   panel title only. Build it from the same content already in the Markdown
   report, do not re-derive it separately.
2. Invoke the `document-generation` skill with that manifest and the desired
   output path. Never render the PDF any other way.
3. This report exercises the manifest's `panel` section type — if this is the
   first time `panel` has been rendered in this project, perform
   `document-generation`'s full visual check (`pdftoppm -png` + inspect),
   per its `SKILL.md` Step 4, not just `pdfinfo`/`pdftotext`.

---

## Final Response Requirements

Lead with links to both the Markdown and PDF reports. Then provide:

- Whether AI/ML components were detected, and what that changed in scope.
- Count of findings by status (Compliant / Non-Compliant / Partially Compliant / Not Verifiable / Not Applicable).
- Concise summary of P0 and P1 gaps, if any.
- A restated reminder that BAA verification was not and cannot be performed by this scan, and is the reader's responsibility.
- A restated reminder that this report is not legal advice or a compliance certification.
- Confirmation that **no application code was changed**.

**Do not imply** that a legal review, a signed-BAA check, a penetration test,
or a live security scan occurred — only the code/config scan described above.

---

## References

- [references/compliance_checklist.md](references/compliance_checklist.md) — the full code-verifiable checklist (categories A–H) plus the Proposed/Regulatory Horizon bucket.
- [references/finding_severity_guide.md](references/finding_severity_guide.md) — 4-state status definitions, P0–P3 priority scale, the PHI Redaction Rule, and the exact finding format.
- [references/manifest_mapping.md](references/manifest_mapping.md) — how a checklist result maps onto a `document-generation` manifest panel (status → level, priority → title prefix).
- [examples/sample_compliance_report.md](examples/sample_compliance_report.md) — worked findings across all five status values, plus the BAA section.
