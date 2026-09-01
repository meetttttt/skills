# MN-Skills — AI Coding Agent Skills Library

A collection of project-agnostic, vendor-neutral skills for AI coding agents.  
Works across **Antigravity, Gemini CLI, Claude Code, Codex, Cursor, Windsurf**, and any agent that reads markdown instructions.

> **For agents**: Read this file to identify which skill to load for a given task. Only read a skill's `SKILL.md` when you are about to execute it — do not pre-load all skills.

---

## Skills at a Glance

| Skill | Purpose | Trigger Phrases |
|---|---|---|
| [`grill-me`](#-grill-me) | Interactive requirements interview | "grill me", `/grill-me`, "interview me about..." |
| [`prd-frd`](#-prd-frd) | Generate internal PRD / FRD spec document | "create PRD", "write FRD", "generate spec" |
| [`clickup`](#-clickup) | ClickUp task management + PRD→task generation | "ClickUp task", "create ticket", "update CU-..." |
| [`implement`](#-implement) | Task-driven feature implementation (PRD/FRD hard-gated) | "implement CU-xxxx", "build the feature from ClickUp task CU-xxxx" |
| [`smoke-test`](#-smoke-test) | Requirement-driven smoke test generation | "create smoke tests", "verify implementation", "write test cases" |
| [`ship`](#-ship) | Commit, push, and open a GitHub PR | "ship this", "create a PR", "commit and push this" |
| [`code-review`](#-code-review) | Full repo / branch / PR audit — findings content only | "audit repo", "code review", "review this PR", "compare branches" |
| [`software-effort-estimation`](#-software-effort-estimation) | Agile effort estimate + Gantt chart from a PRD/Scope doc | "estimate effort", "size this PRD", "how long will this take", "sprint plan" |
| [`document-generation`](#-document-generation) | Shared Quantal AI PDF renderer for any report-producing skill | (invoked by `code-review` / `software-effort-estimation`, not directly) |

---

## Skill Workflow Chain

These skills form a natural end-to-end development workflow — each can also be used standalone:

```
grill-me  ──►  prd-frd  ──►  clickup  ──►  implement  ──►  smoke-test  ──►  ship (optional)
(Gather        (Write         (Create        (Hard-gated      (Verify        (Commit, push,
 reqs)          spec)          tickets)        on PRD/FRD;      impl)          open PR;
                                                syncs status,                  syncs status
                                                calls smoke-test               to "in review")
                                                internally)

                    ▲
             code-review
          (Audit at any stage:
           branch, PR, or full repo)

grill-me  ──►  prd-frd  ──►  software-effort-estimation
                              (Standalone: size the PRD into an
                               Agile sprint plan + Gantt chart)

code-review  ──►  document-generation
software-effort-estimation  ──┘
(Both hand their findings/epics to document-generation,
 the single shared renderer for the Quantal AI PDF visual system)
```

---

## 📋 grill-me

**Purpose**: Conduct a structured technical interview to gather and align on requirements before writing any code. Covers function-level, module-level, and system-level scope.

**Activate when**: User says `/grill-me`, "grill me", or "interview me about [feature/module/product]".

**Key outputs**:
- Structured requirement summary (approved by user before implementation begins)
- Documented edge cases, constraints, and design decisions

**File structure**:
```
grill-me/
├── SKILL.md                        ← Main instructions
├── references/
│   ├── interview_phases.md         ← Question phase guide
│   └── output_templates.md         ← Requirement summary templates
└── examples/
    └── sample_interview.md         ← Sample transcript
```
📄 [Read full instructions](grill-me/SKILL.md)

---

## 📝 prd-frd

**Purpose**: Convert any conversation (standalone, or after `/grill-me`) into a formal internal PRD or FRD markdown specification. Documents are highly descriptive, technically precise, and jargon-heavy — intended for internal engineering teams only, never client-facing.

**Activate when**: User says "create PRD", "write FRD", "generate spec", or "document this feature".

**Key outputs**:
- `docs/PRD_<name>.md` or `docs/FRD_<name>.md` saved at the repository root
- Creates `docs/` directory automatically if it doesn't exist

**File structure**:
```
prd-frd/
├── SKILL.md                        ← Main instructions
├── references/
│   ├── prd_template.md             ← PRD section template
│   └── frd_template.md             ← FRD section template
└── examples/
    └── sample_internal_prd.md      ← Sample output document
```
📄 [Read full instructions](prd-frd/SKILL.md)

---

## 🎯 clickup

**Purpose**: Full ClickUp workspace management — fetch tasks, create/update tickets, manage assignees and priorities, link git branches, and auto-generate task hierarchies from PRD/FRD documents.

**Activate when**: User mentions a ClickUp task ID (`CU-xxxx`), says "create ClickUp tasks from PRD", "update ticket", "assign task", or "sync progress to ClickUp".

**Integration priority**: MCP tools first (`clickup_*`) → REST API fallback (`clickup_helper.py`) → diagnostic guidance if neither available.

**Key outputs**:
- Task and subtask hierarchies in ClickUp
- Git branch names (`<type>/<slug>`, e.g. `feat/login` — no ClickUp ID in the branch name) and commit tags (`[CU-<id>]`)

**PRD/FRD → ClickUp search order**:
1. `docs/PRD_*.md` or `docs/FRD_*.md`
2. Repo-wide `.md` search
3. Ask user for filepath

**File structure**:
```
clickup/
├── SKILL.md                        ← Main instructions
├── references/
│   ├── mcp_setup.md                ← MCP server setup guide
│   ├── api_reference.md            ← ClickUp API v2 endpoints
│   └── git_conventions.md          ← Branch & commit naming conventions
├── scripts/
│   └── clickup_helper.py           ← Pure Python stdlib CLI (no pip needed)
└── examples/
    └── sample_clickup_workflow.md  ← Sample workflow transcripts
```
📄 [Read full instructions](clickup/SKILL.md)

---

## 🛠️ implement

**Purpose**: Implement a feature end-to-end from a ClickUp task. Enforces a hard gate — a matching PRD/FRD document must exist and be validated before any code is written. Fetches the task, syncs ClickUp status throughout, and runs the `smoke-test` skill on completion.

**Activate when**: User says "implement CU-xxxx", "build the feature from ClickUp task CU-xxxx", "code this task: CU-xxxx", or "work on CU-xxxx".

**Hard gate**: If no matching `docs/PRD_*.md` / `FRD_*.md` is found (via the same 3-step resolution as `clickup`), the skill stops completely and tells the user to run `prd-frd` first — no code is written without a validated spec.

**Key outputs**:
- ClickUp status synced: `in progress` → `in review`
- Dedicated feature branch created before any code is written — `<type>/<slug>` (e.g. `feat/login`, `fix/pagination-offset`, `docs/v1-tech-arch`), industry-standard Conventional Commits naming, no ClickUp ID in the branch name
- PRD/FRD auto-linked to the ClickUp task description
- Implementation aligned strictly to PRD/FRD acceptance criteria
- Smoke tests generated and run via the `smoke-test` skill before completion

**File structure**:
```
implement/
├── SKILL.md                              ← Main instructions (10-step workflow)
├── references/
│   └── prd_resolution.md                ← PRD/FRD resolution & validation guide
└── examples/
    └── sample_implement_workflow.md     ← Sample end-to-end transcript
```
📄 [Read full instructions](implement/SKILL.md)

---

## 🧪 smoke-test

**Purpose**: Read requirements from the first available source (ClickUp task, PRD/FRD, repo spec, or git diff), map them to the implemented code, generate isolated executable smoke tests, and run them immediately.

**Activate when**: User says "create smoke tests", "run smoke test", "verify implementation against spec", or "write test cases from FRD/ClickUp".

**Context resolution order** (first match wins):
1. ClickUp Task ID provided in prompt or branch name
2. `docs/PRD_*.md` or `docs/FRD_*.md`
3. Any repo `.md` spec file
4. `git diff` / modified files

**Key outputs**:
- Auto-detected framework test file (`jest`/`vitest`/`pytest`/`go test`/`bash`)
- Saved to the project's standard test folder
- Test suite executed immediately with pass/fail result

**File structure**:
```
smoke-test/
├── SKILL.md                              ← Main instructions
├── references/
│   ├── context_resolution.md            ← Requirement source resolution guide
│   └── smoke_test_guidelines.md         ← Test patterns (Jest/pytest/Go/cURL)
└── examples/
    └── sample_smoke_test_generation.md  ← Sample end-to-end transcript
```
📄 [Read full instructions](smoke-test/SKILL.md)

---

## 🚢 ship

**Purpose**: Commit implemented changes, push a conventionally-named branch, and open a GitHub PR with a description auto-generated from the ClickUp task and PRD/FRD. Uses `gh` CLI and `git` directly — no MCP dependency.

**Activate when**: User says "ship this", "ship CU-xxxx", "create a PR", "raise a PR", "commit and push this", or accepts `implement`'s optional Step 10 hand-off.

**Key Behaviour**:
- Stages **only** the files `implement` reported as created/modified — never `git add -A`.
- Reuses `clickup`'s branch (`<type>/<slug>`, e.g. `feat/login` — no ClickUp ID in the branch name) and commit (`[CU-<id>] <type>: <desc>`) conventions. `implement` creates the branch upfront (its Step 4); `ship` confirms and reuses it rather than creating a new one, or creates it itself when invoked standalone.
- **Hard confirmation checkpoint**: shows the branch name, commit message, staged files, and diff summary, and will not push or open a PR until the user explicitly confirms.
- Stops once the PR is opened and ClickUp is synced to "in review" — does not poll for or react to the PR being merged.

**Key outputs**:
- Pushed branch + committed changes
- Opened (or updated, if one already exists) GitHub PR
- ClickUp task synced to "in review" with the PR link appended to its description

**File structure**:
```
ship/
├── SKILL.md                              ← Main instructions (6-step workflow)
├── references/
│   ├── git_conventions.md               ← Fallback naming when no ClickUp task is in scope
│   └── pr_description_template.md       ← PR body templates (with/without PRD/FRD, with/without ClickUp)
└── examples/
    └── sample_ship_workflow.md          ← Auto-chained, standalone, and cancelled-confirmation transcripts
```
📄 [Read full instructions](ship/SKILL.md)

---

## 🔍 code-review

**Purpose**: Perform a comprehensive, evidence-backed audit of a repository, branch, PR, or commit range. Covers correctness, security, secrets, Git exposure, performance, architecture, and test gaps. Produces the Markdown report itself, then hands findings to `document-generation` for the PDF — this skill owns review content only, not PDF layout.

**Activate when**: User says "audit repo", "code review", "review this PR", "compare branches", "pre-release audit", or "security review".

**Supported scenarios**:
| Scenario | Example |
|---|---|
| Entire repository | "audit the whole repo" |
| Branch-to-branch | "review dev → main", "compare feature1 → dev" |
| Standalone branch | "review the payments branch" |
| PR / commit range | "review PR #42", "review commits abc..def" |

**Key outputs**:
- `reports/repository-audit-YYYY-MM-DD.md` — Markdown report
- `reports/repository-audit-YYYY-MM-DD.pdf` — Quantal AI branded PDF, rendered by `document-generation` (navy cover, severity-colored findings, page headers/footers)

**Finding severities**: P0 (release blocker) → P1 (urgent) → P2 (material defect) → P3 (improvement)

**File structure**:
```
code-review/
├── SKILL.md                          ← Main instructions (7-step workflow)
├── references/
│   ├── finding_severity_guide.md    ← P0–P3 definitions + finding format template
│   └── manifest_mapping.md          ← How a finding maps onto a document-generation manifest panel
└── examples/
    └── sample_audit_report.md       ← Sample P0/P1/P2/P3 findings in exact format
```
📄 [Read full instructions](code-review/SKILL.md)

---

## 📐 software-effort-estimation

**Purpose**: Read a PRD/FRD/Scope document, run an incremental confirmation interview (team composition, seniority, required skills, velocity, contingency), size the work in Agile story points, and produce a Markdown report plus a Gantt chart — the PDF (same Quantal AI visual identity as every other report) is rendered by `document-generation`. This skill owns estimation content only, not PDF layout.

**Activate when**: User says "estimate effort", "size this PRD", "how long will this take", "sprint plan", or "effort estimate for [feature/project]".

**Key outputs**:
- `reports/effort-estimate-<project-slug>-YYYY-MM-DD.md` — Markdown report
- `reports/effort-estimate-<project-slug>-YYYY-MM-DD.pdf` — Quantal AI branded PDF, rendered by `document-generation` (navy cover, risk-colored epic panels, embedded Gantt chart, page headers/footers)

**Risk/complexity classification** (reuses the shared palette for a different meaning — disclosed explicitly in the report via a `disclosure` section): High (red) → Medium (amber) → Low (teal)

**File structure**:
```
software-effort-estimation/
├── SKILL.md                              ← Main instructions (7-step workflow)
├── references/
│   ├── estimation_methodology.md        ← Role taxonomy, story point scale, velocity/contingency defaults, sprint-count formula
│   ├── interview_flow.md                ← Incremental intake interview structure
│   └── manifest_mapping.md              ← How epics + the Gantt chart map onto a document-generation manifest
└── examples/
    └── sample_effort_estimate.md        ← Sample epics in correct format across all three risk levels
```
📄 [Read full instructions](software-effort-estimation/SKILL.md)

---

## 📄 document-generation

**Purpose**: The single, shared PDF renderer for every Quantal AI report. Any skill (`code-review`, `software-effort-estimation`, or a future report type) hands it a content-agnostic JSON manifest; it renders the fixed visual system — exact colors, cover page, header/footer, typography, page geometry — via one locked pipeline (`manifest.json` → HTML with embedded CSS → `weasyprint` → PDF). This exists so report layout can never drift by repo or by which PDF tool happens to be installed.

**Activate when**: Invoked by another skill (or the user directly) that already has report content ready and needs it turned into the standardized PDF. It does not gather content itself.

**Key outputs**:
- `<report>.pdf` rendered from a caller-supplied `manifest.json`
- Also renders any Gantt chart a manifest references (`scripts/generate_gantt_svg.py`, pure stdlib — no pip install required)

**File structure**:
```
document-generation/
├── SKILL.md                              ← Main instructions (4-step workflow)
├── references/
│   ├── visual_system.md                 ← Fixed color palette, typography, page geometry, cover/header/footer spec
│   └── manifest_schema.md               ← Full JSON manifest field reference (sections, panels, charts, tables, ...)
├── scripts/
│   ├── render_report.py                 ← The single fixed manifest-to-PDF renderer
│   └── generate_gantt_svg.py            ← Pure stdlib Python — renders a Gantt chart section as SVG
└── examples/
    ├── sample_manifest_findings.json    ← Worked manifest for a findings-style report (e.g. code-review)
    └── sample_manifest_gantt.json       ← Worked manifest including a Gantt chart section (e.g. effort estimation)
```
📄 [Read full instructions](document-generation/SKILL.md)

---

## Universal Rules (apply to all skills)

- All skills are **100% agent-agnostic** — no hardcoded tool calls, no agent name references.
- All skills default to **read-only** unless the user explicitly requests changes.
- Install via `npx mn-skills` (or `npx github:meetttttt/skills`), which detects and mirrors every skill identically across Claude Code (`~/.claude/skills/`), Codex CLI (`~/.codex/skills/`), and Gemini CLI (`~/.gemini/config/skills/`) — see the root [README](../../README.md) for details.
- When updating any skill in this repo, re-run the installer (or manually sync) so all installed agent targets pick up the change.
