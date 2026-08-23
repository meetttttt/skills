# Estimation Methodology — Defaults & Formulas

All values in this document are **defaults**, not facts about any real team. Every default must be presented to the user as an assumption during the intake interview and is overridable. Never state a default as if it were confirmed information about the user's actual team, unless the user has confirmed it.

---

## 1. Role Taxonomy

Use this fixed taxonomy unless the user's PRD/Scope document or prior answers imply a different one:

| Role | Typical scope |
|---|---|
| Junior | Well-specified, low-ambiguity tasks; needs review on design decisions |
| Mid | Owns a feature end-to-end within an established pattern |
| Senior | Owns ambiguous or cross-cutting features; makes local design calls |
| Lead / Architect | Cross-team design, integration points, unblocking, review overhead |

Do not invent additional roles (e.g. "DevOps Engineer", "QA Automation Engineer") unless the PRD/Scope document's tech stack or explicit user answers justify them.

---

## 2. Story Point Scale

Use a Fibonacci-like scale for epic/feature sizing. Anchor every estimate to a description, not a gut number:

| Points | Complexity anchor |
|---|---|
| 1 | Trivial change, single file, no new logic |
| 2 | Small, well-understood, one component |
| 3 | Standard feature, one service/module, known patterns |
| 5 | Multi-component feature, some design decisions needed |
| 8 | Cross-cutting feature, new integration, meaningful unknowns |
| 13 | Large feature, multiple services, significant unknowns or new tech |
| 21 | Should be split further — flag as a risk rather than estimate directly |

If an epic scores 21, do not silently accept it: recommend splitting it into sub-epics before including it in the Gantt chart.

---

## 3. Default Velocity (points/sprint per resource)

Default sprint length: **2 weeks**. State this explicitly in the report and ask the user to confirm or override during intake.

| Role | Points/sprint (default) |
|---|---|
| Junior | 5 |
| Mid | 8 |
| Senior | 13 |
| Lead / Architect | 8 (reduced for review/unblocking overhead) |

**Team velocity** = sum of (headcount × points/sprint) across all confirmed roles, unless the user supplies a real observed velocity, which always takes precedence over the table.

---

## 4. Contingency & Non-Dev Tracks

Default contingency: **15%** added on top of total dev story points, rounded up to the nearest sprint. Ask the user to confirm or adjust (typical range 10-25% depending on requirement maturity).

Default non-dev tracks to include as separate Gantt rows when the user confirms them (per intake):
- **QA / Testing** — runs partially overlapped with dev, tapering into a dedicated hardening sprint at the end
- **UAT** — one sprint after QA closes, unless the user specifies otherwise
- **Deployment / Release** — final short track (typically 2-5 working days, not a full sprint)
- **PM / Coordination overhead** — shown as a continuous track spanning the full timeline, not sized in points

Do not invent specific dates. Express the Gantt chart in **sprint numbers** (Sprint 1, Sprint 2, ...), not calendar dates, unless the user has supplied a project start date.

---

## 5. Risk / Complexity Classification (drives report color coding)

Classify each epic using this rubric, reusing the audit report's severity palette for a different meaning (complexity/risk, not bug severity — the report must state this explicitly so readers don't confuse the two):

| Classification | Color | Trigger |
|---|---|---|
| High | Red (`#B8272B`) | New/unproven tech, external dependency outside team control, unclear requirements, 13+ points |
| Medium | Amber (`#AD6108`) | Some unknowns, cross-team dependency, 5-8 points |
| Low | Teal (`#076B6B`) | Well-understood pattern, no external dependency, 1-3 points |

Classification must be justified with a one-line rationale in the report, not assigned silently.

---

## 6. Sprint Count Formula

```
total_points = sum(epic points) + contingency (15% default, rounded up)
sprint_count = ceil(total_points / team_velocity)
```

Non-dev tracks (QA tapering, UAT, deployment) extend the timeline beyond `sprint_count` per the defaults in Section 4 — state the final total timeline (dev sprints + QA/UAT/deployment) as the headline number, not just the dev sprint count.
