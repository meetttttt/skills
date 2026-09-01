# Mapping Findings onto a document-generation Manifest

`document-generation`'s manifest schema is defined in
[../../document-generation/references/manifest_schema.md](../../document-generation/references/manifest_schema.md).
This document is the code-review-specific mapping onto it — build the
manifest from the same findings already written into the Markdown report, do
not re-derive them separately.

## Top-level fields

```json
{
  "report_type": "REPOSITORY AUDIT",
  "cover": {"title": "<repository/project name>", "subtitle": "Quantal AI"},
  "footer_text": "CONFIDENTIAL - Quantal AI Internal Engineering Review",
  "metadata_table": [
    {"label": "Repository", "value": "..."},
    {"label": "Audited Target", "value": "..."},
    {"label": "Date", "value": "..."},
    {"label": "Review Scenario", "value": "..."}
  ],
  "sections": [ ... ]
}
```

## Severity → `level`

| Severity | `level` |
|---|---|
| P0 | `critical` |
| P1 | `critical` |
| P2 | `warning` |
| P3 | `info` |

P0 and P1 intentionally share `critical` (red) — the same as the original
fixed palette, where P0/P1 titles were both red.

## Sections

1. `{"type": "heading", "text": "Executive Summary"}` followed by a `paragraph` with the executive summary text.
2. `{"type": "heading", "text": "Findings"}` followed by one `panel` per finding, ordered P0 → P3 as in the Markdown report:
   ```json
   {
     "type": "panel",
     "level": "critical",
     "title": "[P0] Imperative finding title",
     "fields": [
       {"label": "Evidence", "body": "..."},
       {"label": "Blast radius", "body": "..."},
       {"label": "Remediation", "body": "..."},
       {"label": "Prompt for a coding agent", "style": "quote", "body": "..."},
       {"label": "Smoke test", "style": "list", "items": ["...", "..."]}
     ]
   }
   ```
3. Optionally add further `heading`/`paragraph`/`table` sections for
   "Prioritized remediation order", "Validation summary", "Test gaps and
   residual risks", and "Git/history observations" — same content as the
   Markdown report's sections 5-8, laid out with `heading` + `paragraph` or
   `list` sections.

Do not add a `disclosure` section for a code-review report — `critical` /
`warning` / `info` mean exactly what they say here (bug severity), so no
clarifying note is needed.
