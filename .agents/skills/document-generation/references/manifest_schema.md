# Manifest Schema

Every report handed to `document-generation` is a single JSON file. This
document is the authoritative field reference — `scripts/render_report.py`
implements exactly this schema; nothing else is supported.

---

## Top-Level Fields

| Field | Required | Type | Description |
|---|---|---|---|
| `report_type` | yes | string | Short label shown in the header band, e.g. `"REPOSITORY AUDIT"`, `"EFFORT ESTIMATION"`. Rendered as `QUANTAL AI  /  {report_type}`. |
| `cover` | yes | object | `{"title": "...", "subtitle": "Quantal AI"}`. `title` is required; `subtitle` defaults to `"Quantal AI"` if omitted. |
| `footer_text` | yes | string | Left-aligned footer text on every interior page, e.g. `"CONFIDENTIAL - Quantal AI Internal Engineering Review"`. |
| `metadata_table` | no | array | Cover-metadata rows rendered as a two-column table at the top of the first interior page. Each item: `{"label": "...", "value": "..."}`. |
| `sections` | yes | array | Ordered list of section objects (see below). This is the report body. |

---

## Section Types

Every item in `sections` has a `"type"` field. Unknown types are a hard
error — do not invent new types without extending `render_report.py`.

### `heading`
```json
{"type": "heading", "text": "Executive Summary"}
```
Major section heading, primary blue.

### `subheading`
```json
{"type": "subheading", "text": "Team Composition"}
```

### `paragraph`
```json
{"type": "paragraph", "text": "Plain body text."}
```

### `panel`
The core repeating unit for findings/epics/any leveled item.
```json
{
  "type": "panel",
  "level": "critical",
  "title": "[P0] User passwords stored as plaintext in PostgreSQL",
  "fields": [
    {"label": "Evidence", "body": "src/auth/user.service.ts:L88 - ..."},
    {"label": "Blast radius", "body": "..."},
    {"label": "Remediation", "body": "..."},
    {"label": "Prompt for a coding agent", "style": "quote", "body": "..."},
    {"label": "Smoke test", "style": "list", "items": ["...", "..."]}
  ]
}
```
- `level`: `"critical"` | `"warning"` | `"info"` | `"default"` — see the mapping in `visual_system.md`. Optional; defaults to `"default"`. A panel may instead set an explicit `"color"` hex value to bypass the mapping (rare — prefer `level`).
- `fields[].style`: `"body"` (default, plain text) | `"quote"` (teal, indented — for AI prompts or notable callouts) | `"list"` (bulleted, uses `items` instead of `body`) | `"code"` (monospace block).

### `table`
```json
{"type": "table", "headers": ["Item", "Value", "Status"], "rows": [["Sprint length", "2 weeks", "Confirmed"]]}
```

### `list`
```json
{"type": "list", "ordered": false, "items": ["First point", "Second point"]}
```

### `chart`
```json
{"type": "chart", "chart_type": "gantt", "svg_path": "gantt.svg", "caption": "Sprint plan"}
```
`svg_path` is resolved relative to the manifest's own directory. The
referenced SVG must already exist — generate it first (see `SKILL.md` Step 2
for the Gantt case). `caption` is optional.

### `disclosure`
```json
{"type": "disclosure", "text": "Red/amber/teal denote estimation complexity here, not bug severity."}
```
A single italic teal note. Use sparingly — most report types don't need one,
since `level` is a neutral name (see `visual_system.md`). Use it when a
report's own domain language could otherwise be misread as literal defect
severity.

### `pagebreak`
```json
{"type": "pagebreak"}
```
Forces a page break before the next section. Use to keep a chart from
splitting awkwardly across pages, or to separate major report parts.

---

## Gantt Chart Data (separate file, referenced by `svg_path`)

Build a `gantt_data.json` (any filename) matching this schema, then run
`scripts/generate_gantt_svg.py` (see `SKILL.md` Step 2) to produce the SVG the
manifest's `chart` section points to:

```json
{
  "sprint_count": 4,
  "epics": [
    {"name": "Epic title", "start_sprint": 1, "end_sprint": 2, "risk": "high"}
  ],
  "tracks": [
    {"name": "QA / Testing", "start_sprint": 1, "end_sprint": 4, "kind": "band"},
    {"name": "PM / Coordination", "kind": "continuous"}
  ]
}
```
- `epics[].risk`: `"high"` / `"medium"` / `"low"` → maps to the same
  critical/warning/info colors as `level` (kept as `risk` here, not `level`,
  because this file is consumed directly by the chart script, which predates
  and is reused unchanged by this skill).
- `tracks[].kind`: `"band"` (uses `start_sprint`/`end_sprint`) or
  `"continuous"` (auto-spans the full `sprint_count`).
- Any epic or track may set an explicit `"color"` hex to override the default.

---

## Full Worked Examples

- [examples/sample_manifest_findings.json](../examples/sample_manifest_findings.json) — a two-finding code-review-style report.
- [examples/sample_manifest_gantt.json](../examples/sample_manifest_gantt.json) — a report including a Gantt chart section, disclosure note, and metadata table.
