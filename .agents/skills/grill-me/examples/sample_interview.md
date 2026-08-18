# Sample Grill-Me Interview Transcripts

This document shows sample interview flows demonstrating how **Grill-Me** scales dynamically across different task granularities.

---

## Example 1: Micro Level (Refactoring a Single Helper Function)

**User**:  
> /grill-me I want to refactor our `slugify()` utility function to support non-Latin unicode characters.

**Agent** *(Recognizes Tier 1: Function-level refactor -> 1 Turn, 3 targeted questions)*:  
> Let's quickly align on `slugify()` behavior before changing the code:
> 1. **Separator & Lowercasing**: Should non-Latin characters (e.g. `中文`, `español`, `русский`) be preserved as lowercased UTF-8 slugs or transliterated to ASCII equivalent (e.g. `e` for `é`)?
> 2. **Whitespace & Special Chars**: How should whitespace, punctuation (punctuation like `!`, `?`), and trailing dashes be handled?
> 3. **Backwards Compatibility**: Are existing DB records using the old slug format, or is this function only used for newly generated slugs?

**User**:  
> 1. Preserved as UTF-8 slugs, lowercased.
> 2. Replace whitespace with dashes, strip punctuation, trim leading/trailing dashes.
> 3. Only for newly generated slugs, no migration needed.

**Agent**:  
> Perfect! Here is our quick alignment summary:
> 
> ### 🎯 Quick Alignment Summary
> - **Function**: `slugify(input: string): string`
> - **Behavior**: Lowercase UTF-8 preservation, space to `-`, strip punctuation (`/[^\p{L}\p{N}\s-]/gu`), trim dashes.
> - **Scope**: New slugs only, backwards compatible with current callers.
> 
> I am ready to implement this function and its unit test suite!

---

## Example 2: Module Level (Adding a Server-Sent Events Feature)

**User**:  
> /grill-me We need to add real-time notifications to our dashboard when background jobs finish.

**Agent** *(Recognizes Tier 2: Module/Feature-level -> 2-3 turns on transport, state, and edge cases)*:  
> Great! Let's grill this design:
> 1. **Delivery Guarantee**: Is it acceptable if an offline user misses a live update and sees it upon refresh, or must unread notifications be stored in Postgres?
> 2. **Transport**: Are you thinking SSE (Server-Sent Events), WebSockets, or polling?
> 3. **Multi-Tab**: How should reading a notification in Tab 1 update Tab 2?

*(Interview continues over 2 turns to establish Postgres `notifications` table, SSE transport, and Redis Pub/Sub multi-node relay, producing an `alignment_spec.md` artifact).*
