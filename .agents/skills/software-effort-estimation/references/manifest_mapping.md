# Mapping an Effort Estimate onto a document-generation Manifest

`document-generation`'s manifest schema is defined in
[../../document-generation/references/manifest_schema.md](../../document-generation/references/manifest_schema.md).
This document is the effort-estimation-specific mapping onto it — build the
manifest from the same epics already written into the Markdown report, do not
re-derive them separately.

## Top-level fields

```json
{
  "report_type": "EFFORT ESTIMATION",
  "cover": {"title": "<project/initiative name>", "subtitle": "Quantal AI"},
  "footer_text": "CONFIDENTIAL - Quantal AI Internal Engineering Estimate",
  "metadata_table": [
    {"label": "Project", "value": "..."},
    {"label": "Source Document", "value": "..."},
    {"label": "Date", "value": "..."},
    {"label": "Sprint Length", "value": "..."}
  ],
  "sections": [ ... ]
}
```

## Risk → `level`

| Epic risk classification | `level` |
|---|---|
| High | `critical` |
| Medium | `warning` |
| Low | `info` |

## Sections

1. `{"type": "heading", "text": "Executive Summary"}` followed by a `paragraph` with the executive summary text.
2. A `disclosure` section right after the executive summary:
   ```json
   {"type": "disclosure", "text": "Red/amber/teal below denote estimation complexity/risk in this report, not bug severity."}
   ```
   This is the one report type that keeps the disclosure — "High/Medium/Low
   risk" read next to red/amber/teal can otherwise be mistaken for the
   severity meaning used in code-review reports.
3. `{"type": "heading", "text": "Epic Breakdown"}` followed by one `panel` per epic, ordered by planned sprint:
   ```json
   {
     "type": "panel",
     "level": "critical",
     "title": "[HIGH] Epic title",
     "fields": [
       {"label": "Scope", "body": "..."},
       {"label": "Story points", "body": "13 - anchored to ... methodology §2."},
       {"label": "Rationale", "body": "..."},
       {"label": "Dependencies", "body": "..."},
       {"label": "Assigned sprint(s)", "body": "Sprint 1-2, owned by ..."}
     ]
   }
   ```
4. `{"type": "heading", "text": "Sprint Plan"}` followed by the Gantt chart:
   ```json
   {"type": "chart", "chart_type": "gantt", "svg_path": "gantt.svg", "caption": "Epics and non-dev tracks by sprint"}
   ```
   `svg_path` points at the SVG produced in `SKILL.md` Step 5.
5. `{"type": "heading", "text": "Risks and Dependencies"}` — a `list` or further `paragraph` sections covering cross-epic dependencies, external blockers, and anything flagged for splitting.
6. `{"type": "heading", "text": "Assumptions Log"}` followed by a `table` section (headers: Item, Value, Status) — same content as the Markdown report's assumptions log.
