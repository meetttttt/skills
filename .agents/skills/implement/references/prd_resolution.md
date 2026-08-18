# PRD/FRD Resolution and Validation Guide

This guide explains how the **Implement** skill finds, matches, and validates a PRD or FRD document against a ClickUp task before allowing code to be written.

---

## Why This Gate Exists

Implementing without a specification leads to:
- Misaligned acceptance criteria
- Missing edge cases
- Unverifiable smoke tests
- Rework after stakeholder review

The hard gate ensures every implementation is traceable back to a written, approved specification.

---

## Resolution Priority

Same 3-step strategy used by the `clickup` skill for PRD/FRD → ClickUp task generation:

```text
Step 1: docs/PRD_*.md or docs/FRD_*.md
   ↓ (If not found)
Step 2: Repo-wide *.md search for # PRD: or # FRD: headers
   ↓ (If not found)
Step 3: Ask user for filepath
   ↓ (If user has none)
HARD STOP — instruct user to run /prd-frd first
```

---

## Step 1: Search `docs/` Folder

Check the `docs/` directory for any file matching `PRD_*.md` or `FRD_*.md`.

**Matching heuristics** (any of these is sufficient):
- Filename contains words from the ClickUp task title (e.g. task "Notifications Feature" → `PRD_notifications.md`)
- Document `# Title` or first heading matches the ClickUp task title or feature area
- Document body references the ClickUp task ID (e.g. `CU-xxxx`)
- Document describes the same functional domain as the task description

If multiple documents are found, present the options to the user and ask which one applies.

---

## Step 2: Repo-wide Search

If `docs/` has no match:

1. Search all `.md` files in the repository for `# PRD:` or `# FRD:` headings.
2. Apply the same matching heuristics as Step 1.
3. If a match is found outside `docs/`, note its path but recommend the user move it to `docs/` for consistency.

---

## Step 3: Ask User for Filepath

If no match is found after both searches, pause and ask the user directly:

> "I couldn't locate a PRD/FRD document in `docs/` or the repository. Do you have one at a different filepath?"

- If the user provides a valid path, read and validate it as if it had been found in Step 1 or 2.
- If the user confirms no document exists, proceed to the hard stop below.

---

## Hard Stop Message

If Step 3 confirms no document exists anywhere, stop and output exactly:

```
⛔ No PRD or FRD document was found for ClickUp task CU-xxxx.

Implementing without a specification is not permitted.

Please generate one first:
  1. Run the `prd-frd` skill to create docs/PRD_<feature>.md
  2. Then retry: "implement CU-xxxx"
```

---

## Validation Checklist

Once a document is found, validate it contains sufficient content to implement from:

| Check | Required |
|---|---|
| Has a clear feature title / scope | ✅ |
| Has acceptance criteria or functional requirements | ✅ |
| Describes at least one API contract, data model, or component behaviour | ✅ |
| Has edge cases or error handling requirements | Preferred |
| References non-functional requirements (performance, security, etc.) | Preferred |

If mandatory items are missing, ask the user to complete the document or enrich it before proceeding.

---

## Auto-Linking the Document to ClickUp

After resolving the PRD/FRD, append a reference to the ClickUp task description to create a permanent traceability link:

```
📄 Spec: docs/PRD_<feature>.md
```

This ensures anyone viewing the ClickUp task can immediately find the specification document.
