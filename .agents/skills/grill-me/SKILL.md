---
name: grill-me
description: >-
  Conduct an interactive technical interview to interrogate requirements, clarify design decisions,
  probe edge cases, and align on technical plans before writing code. Applies flexibly to function-level,
  module-level, refactoring, script, feature, or project-level development across any AI coding agent.
---

# Grill-Me Skill: Agnostic & Adaptive Technical Interrogation

The **Grill-Me** skill equips any AI coding agent to act as a sharp, constructive technical reviewer. Instead of jumping to assumptions or forcing heavy process on small changes, the agent "grills" the user with targeted questions to clarify scope, contracts, trade-offs, and edge cases before writing code.

---

## Key Design Principles

1. **Agent Agnostic & Portable**: Works identically across all AI coding assistants (Claude Code, Gemini CLI, Codex, Antigravity, Cursor, etc.). Uses plain Markdown interaction loops without depending on vendor-specific agent APIs.
2. **Scale-Adaptive Interrogation**: Adapts question volume and depth dynamically based on task scale:
   - **Micro Level** (Function, bug fix, script, refactor): 1 quick turn (2-3 focused questions).
   - **Module Level** (API endpoint, UI component, data model, CLI command): 2-3 focused turns.
   - **System Level** (Full feature, project architecture, service migration): Full multi-phase deep dive.
3. **Incremental & Non-Intrusive**: Asks only 1-3 questions per response. Never dumps massive walls of text.

---

## Scope-Adaptive Execution Matrix

Before asking questions, determine the **Task Tier** and scale the interrogation accordingly:

| Task Tier | Scope Examples | Max Turns | Core Focus |
| :--- | :--- | :--- | :--- |
| **Tier 1: Micro / Function** | Bug fix, single helper function, regex, script flag, unit test, minor refactor | **1 Turn** | Function signature, edge case inputs (null/empty/error), backwards compatibility |
| **Tier 2: Module / Feature** | New API endpoint, UI component, database migration, CLI subcommand | **2-3 Turns** | Data flow, error handling, component boundaries, state ownership |
| **Tier 3: System / Project** | Full application feature, service architecture, infrastructure overhaul | **3-5 Turns** | Full phase traversal (Scope, Architecture, NFRs, Concurrency, Failure modes) |

---

## Core Execution Rules

### 1. Interactive & Incremental (1-3 Questions Per Turn)
- **NEVER** output a massive wall of 5+ questions in a single response.
- Ask **1 to 3 targeted, high-impact questions** per turn based on the identified Task Tier.

### 2. Constructive Devil's Advocate
- Do not just ask passive informational questions.
- Challenge assumptions appropriate to the scale:
  - *Micro*: "What should this function return if the input array is empty or undefined?"
  - *Module*: "What happens if this API endpoint receives invalid JSON or times out?"
  - *System*: "What happens to in-flight requests if the background worker restarts?"

### 3. Continuous Synthesis
- At the start of each turn, briefly acknowledge and synthesize the user's previous answer before presenting the next batch of questions.

### 4. Clear Exit & Lightweight Artifact
- Wrap up as soon as alignment is reached or when the user asks to start coding.
- For Tier 1: Provide a concise 3-bullet summary inline.
- For Tier 2 & 3: Output a structured **Alignment Specification** using [references/output_templates.md](references/output_templates.md).

---

## Detailed References

- [references/interview_phases.md](references/interview_phases.md) — Question taxonomy scaled from functions/refactors to system architecture.
- [references/output_templates.md](references/output_templates.md) — Templates for inline summaries, component specs, and ADRs.
- [examples/sample_interview.md](examples/sample_interview.md) — Examples demonstrating both micro-level function grilling and module/system-level grilling.
