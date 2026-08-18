# Requirement Context Resolution Protocol

This guide details how the **Smoke-Test** skill resolves requirements from any single available context source.

---

## Resolution Priority Order

```text
Priority 1: ClickUp Task ID (CU-xxxx or #xxxx)
   ↓ (If absent)
Priority 2: PRD / FRD Document in docs/ folder (PRD_*.md, FRD_*.md)
   ↓ (If absent)
Priority 3: Repository Spec Document (*.md)
   ↓ (If absent)
Priority 4: Git Diff / Modified Files Inspection
```

---

## 1. Extracting Requirements from ClickUp Tasks (Priority 1)

If a ClickUp Task ID (`CU-8675309`, `#8675309`, `8675309`) is present:

1. **Invoke Fetch**:
   - Via MCP: `clickup_get_task({ taskId: "CU-8675309" })`
   - Via CLI: `python3 .agents/skills/clickup/scripts/clickup_helper.py get CU-8675309`
2. **Parse Text**:
   - Extract title, description, and custom fields.
   - Look for section headings like `Acceptance Criteria:`, `Requirements:`, or `- [ ]` checklist items.

---

## 2. Extracting Requirements from PRD / FRD in `docs/` (Priority 2)

If no ClickUp ID is provided, scan `docs/`:

1. Check for `docs/PRD_*.md` or `docs/FRD_*.md`.
2. Parse Section 2 (Scope & Contracts), Section 3 (Data Dictionary), Section 4 (API Contracts), and Section 7 (Edge Case Matrix).

---

## 3. Extracting Requirements from Repository Markdown Specs (Priority 3)

If `docs/` has no PRD/FRD:

1. Search for any `.md` file in the repo root containing headings `# PRD:`, `# FRD:`, or `# Specification:`.
2. Extract requirement bullet points and type interfaces.

---

## 4. Extracting Requirements from Git Diff (Priority 4 Fallback)

If no ticket or documentation exists:

1. Inspect modified files using `git status` / `git diff`.
2. Extract exported function signatures, public methods, and API route handlers.
3. Formulate implicit requirement contracts based on function parameters, return types, and conditional branches.
