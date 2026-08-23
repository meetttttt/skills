---
name: software-effort-estimation
description: >-
  Produce an evidence-backed Agile effort estimate from a PRD/Scope document and
  generate a standardized professional Markdown and PDF report, including a rendered
  Gantt chart. Use when an agent must read a PRD/FRD/Scope document, confirm team
  composition, seniority, and required skills with the user, size the work in story
  points, convert it to a sprint-based timeline, and report the plan with the same
  visual identity as the repository-audit skill.
---

# Software Effort Estimation Skill

A project-agnostic Agile effort estimation skill. Reads a PRD/Scope document, runs an
incremental confirmation interview with the user, sizes the work, and produces an
evidence-backed Markdown report plus a standardized professional PDF report (with a
Gantt chart) for every engagement.

This skill assumes **Agile delivery** (story points, sprints, iterative epics) — never
produce a Waterfall-style single critical-path schedule.

---

## Core Operating Rules

- **No invented estimates.** Every story point value and risk classification must trace to the PRD/Scope document's stated scope, a confirmed user answer, or a documented default from `references/estimation_methodology.md`. Never fabricate scope not present in the source document.
- **Ask when unsure.** If the document is ambiguous about scope, or team/skills/velocity are not yet confirmed, ask — do not guess and proceed silently.
- **Defaults are disclosed, not assumed.** Any value pulled from `references/estimation_methodology.md` (velocity, sprint length, contingency %) must be explicitly labeled as a default and offered for override during the interview, never presented as a fact about the user's real team.
- **Read-only against the codebase.** This skill produces a planning document; it must not modify application code.
- **Read `AGENTS.md` first** if present in the repository before starting.
- **No secret disclosure.** If the PRD/Scope document contains credentials or sensitive data, do not reproduce them in the report.

---

## Step 1 — Locate the Source Document

1. Look for a PRD, FRD, or Scope document, typically in `docs/` (same convention as the `prd-frd` skill).
2. If the user references a ClickUp task instead of a file, use the `clickup` skill to retrieve it.
3. If nothing is found automatically, ask the user for a file path or to paste the scope directly. Do not proceed to estimation without a source document — this skill does not estimate from memory or assumption.
4. State which source was used (file path, or ClickUp task ID) in the report's cover metadata.

---

## Step 2 — Extract Epics and Read Complexity Signals

1. Break the document into a candidate list of epics/features (name + one-line scope each). Prefer the document's own section/feature boundaries over inventing new groupings.
2. Note any tech stack, integrations, or non-functional requirements mentioned — these feed both the required-skills proposal and the risk classification in Step 3.
3. Do not size anything yet. This is extraction only.

---

## Step 3 — Intake Interview

Run the incremental, grill-me-style interview defined in
[references/interview_flow.md](references/interview_flow.md): **1-3 questions per turn**,
never a single wall of questions, acknowledging the prior answer before asking the next
batch. Cover, in order: epic confirmation, team composition, required skills, velocity
and sprint length, contingency and non-dev tracks, and complexity/risk classification.

Do not proceed to Step 4 until every round in that interview is resolved (confirmed or
explicitly overridden by the user).

---

## Step 4 — Size the Work

1. Assign story points per epic using the Fibonacci-like scale in
   [references/estimation_methodology.md](references/estimation_methodology.md) §2.
   Any epic scoring 21 must be flagged for splitting rather than accepted as-is.
2. Compute team velocity from the confirmed team composition and confirmed/overridden
   points-per-sprint figures (§3 of the methodology doc; user-supplied observed velocity
   always wins over the default table).
3. Apply the confirmed contingency % (§4), rounded up to the nearest sprint.
4. Compute `sprint_count = ceil(total_points_with_contingency / team_velocity)` per §6.
5. Lay out non-dev tracks (QA, UAT, Deployment, PM/Coordination) per the confirmed
   choices from Step 3, extending the timeline as described in §4.
6. Classify each epic High/Medium/Low per §5, with a one-line rationale — this drives
   both the report panel color and the Gantt chart bar color.

---

## Step 5 — Generate the Gantt Chart

Use the bundled script — **do not hand-write chart code.** Freeform chart generation is
what made earlier reports unreliable (missing rows, clipped columns, garbled text); the
script is tested and fixes those failure modes structurally.

1. Build `gantt_data.json` from the sized epics and confirmed non-dev tracks, matching
   the schema documented in
   [references/pdf_visual_system.md](references/pdf_visual_system.md) "Gantt Chart
   Generation" section.
2. Run:
   ```
   python3 scripts/generate_gantt_svg.py --input gantt_data.json --output gantt.svg
   ```
   This is pure Python standard library — no `pip install` required, so it cannot fail
   due to a missing dependency.
3. Embed the resulting SVG into the report HTML exactly as documented in
   `pdf_visual_system.md` (UTF-8 charset + full-width scaling are both required — see
   that doc for why).
4. If step 2 fails for a reason other than malformed input (e.g. `python3` unavailable
   in the environment), fall back to a markdown table (epics × sprint columns) and state
   the blocker clearly — do not silently omit the Gantt chart.

---

## Step 6 — Markdown Report Structure

Output file: `reports/effort-estimate-<project-slug>-YYYY-MM-DD.md`

The report must contain, in order:

1. **Cover metadata** — Project/initiative name, Company (Quantal AI), source document
   (path or ClickUp task ID), date, confirmed team composition, sprint length, and a
   one-line disclosure that red/amber/teal denote complexity/risk here, not bug
   severity.
2. **Executive summary** — total epics, total story points, contingency applied, total
   sprint count, total timeline including non-dev tracks.
3. **Scope and methodology** — what was read, what was confirmed vs. defaulted, and any
   assumptions still outstanding.
4. **Team composition and required skills** — confirmed roles, headcount, seniority,
   and skills per role.
5. **Epic breakdown** — every epic using the exact format below, ordered by planned
   sprint.
6. **Gantt chart** — the embedded/rendered chart (or markdown-table fallback).
7. **Risks and dependencies** — cross-epic dependencies, external blockers, anything
   flagged for splitting.
8. **Assumptions log** — every default used and whether it was confirmed or left at
   default value.

### Exact Epic Format (required for every epic)

```markdown
### [HIGH] Epic title

**Scope:** One to three sentences describing what this epic covers, traceable to a
specific section of the source document.

**Story points:** 13 — anchored to the complexity table in
references/estimation_methodology.md §2.

**Rationale:** Why this point value and risk classification were chosen — new tech,
external dependency, ambiguity, or lack thereof.

**Dependencies:** What this epic depends on or blocks, if anything.

**Assigned sprint(s):** Sprint 3-4, owned by [role(s)].
```

---

## Step 7 — Standardized Professional PDF Report

Output file: `reports/effort-estimate-<project-slug>-YYYY-MM-DD.pdf`

Generate the PDF from the Markdown report using the fixed visual system defined in
[references/pdf_visual_system.md](references/pdf_visual_system.md) — identical palette,
cover page, header/footer, and page geometry to the `repository-audit` skill's reports,
plus the embedded Gantt chart.

### PDF Validation Checklist (run after generation)

- Verify file creation with `file` or `pdfinfo`.
- Verify correct page size and page count.
- Extract text with `pdftotext` when available to confirm readable content.
- Visually confirm:
  - Cover page contains **only** the project/initiative name and `Quantal AI` — nothing else.
  - Headers and footers do not overlap content.
  - Page numbers appear on every interior page.
  - Risk colors are consistent (High red, Medium amber, Low teal) and match the Gantt chart bar colors.
  - The Gantt chart is legible and not cut off by a page break.
  - Margins and typography are consistent.
- Report any PDF-generation or validation blocker clearly.

---

## Final Response Requirements

Lead with links to both the Markdown and PDF reports. Then provide:

- Total epics, total story points, contingency applied, total sprint count, and total
  timeline (dev + QA/UAT/deployment).
- Confirmed team composition and confirmed velocity.
- Which inputs were user-confirmed vs. left at documented default.
- Any epics flagged for splitting (21-point epics) or flagged as under-resourced risks.
- A statement that **no application code was changed** — this is a planning artifact only.

**Do not imply** a ClickUp lookup, PDF visual review, or Gantt chart render occurred
unless it actually occurred.

---

## References

- [references/estimation_methodology.md](references/estimation_methodology.md) — role taxonomy, story point scale, default velocity, contingency rules, risk classification rubric, and the sprint-count formula.
- [references/interview_flow.md](references/interview_flow.md) — the incremental, grill-me-style intake interview structure.
- [references/pdf_visual_system.md](references/pdf_visual_system.md) — fixed color palette, typography, page geometry, cover spec, header/footer spec, the `gantt_data.json` schema, and SVG-embedding rules.
- [scripts/generate_gantt_svg.py](scripts/generate_gantt_svg.py) — pure-stdlib Gantt chart renderer; run this in Step 5, never hand-write chart code.
- [examples/sample_effort_estimate.md](examples/sample_effort_estimate.md) — sample epics in correct format across all three risk levels, plus a sample executive summary.
