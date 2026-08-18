# Grill-Me Output Templates

Upon completing a Grill-Me interview, choose the template matching your Task Scale.

---

## Template 1: Micro / Function-Level Inline Summary (Tier 1)

For small refactors, bug fixes, helper functions, or scripts, output a simple inline summary in the chat response:

```markdown
### 🎯 Quick Alignment Summary

- **Task**: Refactor `parseDate()` helper function to handle ISO-8601 strings.
- **Agreed Behavior**:
  - Return `null` on invalid date strings (do not throw).
  - Treat zero timestamps (`0`) as epoch start.
  - Return a new `Date` instance (pure function, no mutation).
- **Test Strategy**: Add unit test with 5 edge-case strings.
```

---

## Template 2: Module & Feature Alignment Spec (Tier 2 & 3)

For API endpoints, UI components, or feature modules, output an `alignment_spec.md` artifact:

```markdown
# Technical Alignment Specification: [Module / Feature Name]

## 1. Executive Summary
Brief 2-3 sentence overview of what is being changed or built.

## 2. Scope & Contract
- **Inputs & Parameters**: [Function arguments, API request payload, UI props]
- **Outputs & Side Effects**: [Return values, DB writes, state changes]
- **Explicit Non-Goals**: What is deferred or out of scope.

## 3. Edge Cases & Error Mitigations

| Risk / Edge Case | Agreed Handling | Verification |
| :--- | :--- | :--- |
| Empty / null input | Return default value / 400 Bad Request | Unit test |
| Network timeout | Client retry with backoff | Integration test |

## 4. Execution Steps
- [ ] Task 1: Contract / Interface definition
- [ ] Task 2: Core implementation
- [ ] Task 3: Edge case & error handling
- [ ] Task 4: Unit & integration testing
```
