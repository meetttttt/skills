# Grill-Me Interview Phases & Question Taxonomy

This reference guide provides questioning vectors tailored by **Task Scale** and **Interview Phase**.

---

## 1. Micro-Level Tasks (Functions, Refactoring, Scripts, Bug Fixes)

For small, single-file or single-function changes, pick 2-3 questions from this menu for a single 1-turn interview:

### Function Signatures & Types
- **Input Boundaries**: How should this function handle `null`, `undefined`, empty strings, or zero values?
- **Return Type & Mutability**: Does this function return a new object/array or mutate the input parameter in place?
- **Error Handling**: Should invalid arguments throw a custom exception, return a Result/Either type, or return `null`/`false`?

### Refactoring & Bug Fixes
- **Root Cause & Scope**: Are we fixing the symptom in this single function or updating the contract upstream?
- **Side Effects**: Does modifying this internal utility break any existing callers in the codebase?
- **Test Vectors**: What specific input/output pair will verify that the bug is fixed without regressions?

---

## 2. Module & Feature-Level Tasks (APIs, UI Components, CLI Commands)

For medium-scale changes, pick 1-3 questions per turn over 2-3 turns:

### Component & API Contracts
- **Interface Surface**: What parameters/props are required vs optional, and what are sensible defaults?
- **State Ownership**: Does this component manage its own local state, receive state via props/context, or sync with URL query params?
- **Validation & Sanitization**: Where are user inputs validated (client-side, backend boundary, or database model level)?
- **Error States**: How does the UI or API represent loading, partial success, rate limits, and network errors?

---

## 3. System & Project-Level Tasks (Full Services, Architectural Redesign)

For large-scale projects, traverse these phases over 3-5 turns:

### Phase 1: Scope & Boundaries
- **MVP Definition**: What is the minimum viable capability we must ship first?
- **Explicit Non-Goals**: What related capabilities are explicitly out of scope for this milestone?

### Phase 2: Technical Architecture
- **Data Models & Persistence**: Where does the source of truth live, and how are schema migrations handled?
- **Service Boundaries**: How do components communicate (sync REST, gRPC, async event queue)?

### Phase 3: Non-Functional Requirements & Resilience
- **Performance & SLAs**: What are the latency budget and memory constraints?
- **Concurrency & Failure Modes**: How does the system behave during network partitions, database deadlocks, or instance restarts?
