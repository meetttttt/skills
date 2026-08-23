# Effort Estimation Intake Interview

This skill's intake interview follows the same incremental discipline as the `grill-me` skill: **1-3 questions per turn, never a single wall of questions.** Acknowledge the previous answer briefly before asking the next batch. Do not proceed to estimation until every round below has been resolved (confirmed or explicitly overridden by the user).

Do this analysis (epic extraction, complexity read, proposed team) silently before Round 1 — the user should see proposals to react to, not be asked to generate them from scratch.

---

## Round 1 — Epic Confirmation

After extracting epics/features from the PRD/Scope document, confirm the breakdown before sizing anything:

- Present the extracted epic/feature list (name + one-line scope each).
- Ask: "Does this match your intended scope? Anything missing, merged incorrectly, or out of scope for this estimate?"

Do not proceed to sizing until the epic list is confirmed or corrected.

## Round 2 — Team Composition

- Propose a team (roles from the taxonomy in `estimation_methodology.md`, headcount per role) based on epic count, complexity mix, and any tech-stack signals in the document.
- Ask the user to confirm headcount/seniority per role, or adjust.
- If the user's team looks undersized relative to epic complexity (e.g. 1 person against 5 high-complexity epics), flag it as a risk rather than silently accepting.

## Round 3 — Required Skills Confirmation

- Propose the required skills/tech stack per role, derived from the PRD/Scope document (languages, frameworks, infra, integrations named in the doc).
- Ask the user to confirm, add, or remove skills. Do not invent skills that aren't traceable to the document or a prior answer.

## Round 4 — Velocity & Sprint Length

- State the default (2-week sprints, velocity table from `estimation_methodology.md` section 3) computed against the confirmed team from Round 2.
- Ask: "Use this default velocity, or do you have an observed team velocity to use instead? Any sprint length other than 2 weeks?"

## Round 5 — Contingency & Non-Dev Tracks

- State the default (15% contingency, QA/UAT/deployment/PM tracks per section 4).
- Ask: "Keep these defaults, or adjust the contingency % / which non-dev tracks to include?"

## Round 6 — Complexity/Risk Pass (if not already resolved inline)

- Present the proposed High/Medium/Low classification per epic with rationale.
- Ask the user to confirm or correct any classification before it drives report coloring and the Gantt chart.

---

## Exit Condition

Once Rounds 1-6 are resolved, do not ask further questions — proceed directly to computing story points, sprint count, and generating the Markdown + PDF report per `SKILL.md` Steps 5-7. State clearly in the report which values were user-confirmed vs. left at default, so the estimate's basis is auditable.
