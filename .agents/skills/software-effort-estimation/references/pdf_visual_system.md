# PDF Visual System — Effort Estimation Reports

This document defines the **fixed, immutable visual standard** applied to every `software-effort-estimation` PDF report. It is deliberately identical to the `repository-audit` skill's visual system (same palette, cover page, header/footer, layout) so that every Quantal AI-generated report family looks like one consistent product line. The only additions are the Gantt chart and the reuse of the severity palette for complexity/risk instead of bug severity.

---

## Document Format

| Property | Value |
|---|---|
| Page size | US Letter, portrait — 612 × 792 points |
| Left margin | 54 points |
| Right margin | 54 points |
| Top content start | 710 points (below header band) |
| Bottom content boundary | 58 points (above footer) |
| Primary typeface | Helvetica / Helvetica Bold (sans-serif) |
| Fallback typeface | Any highly legible sans-serif (e.g. Arial, DejaVu Sans) |

Never allow content to overlap headers, footers, page numbers, or margins. Maintain consistent spacing between headings, sections, epic panels, the Gantt chart, and footers.

---

## Color Palette (Exact Hex Values — identical to repository-audit)

| Role | Hex | Usage |
|---|---|---|
| **Dark navy** | `#0E1A2F` | Cover background, header band |
| **Primary blue** | `#144D8B` | Major headings, accent rules, labels |
| **Slate text** | `#333D4D` | All body text |
| **Muted slate** | `#667385` | Footer text, secondary metadata |
| **Pale blue-gray** | `#F0F5FA` | Epic panel backgrounds, subtle section backgrounds |
| **High-risk red** | `#B8272B` | High-complexity/high-risk epic titles (reused P0/P1 meaning: complexity, not bug severity) |
| **Medium-risk amber** | `#AD6108` | Medium-complexity epic titles |
| **Low-risk teal** | `#076B6B` | Low-complexity epic titles, assumption labels |
| **White** | `#FFFFFF` | Cover page text, header text |

**Required disclosure:** because this palette is borrowed from the audit report's severity system, the report must state once, near the top (Scope & Methodology section), that red/amber/teal here denote estimation complexity/risk — not defects or bug severity.

---

## Required First Page — Cover Page

Identical rules to `repository-audit`. The first page must be **exclusively** a cover page with **only two elements**:

1. **Project / initiative name** — large, bold, white text
2. **`Quantal AI`** — smaller white text, directly beneath the project name

**Cover page must NOT include:** report title, date, sprint count, team size, subtitle, scope, methodology, confidentiality label, footer, page number, or any other metadata.

**Cover page layout:**
- Full-page dark navy background (`#0E1A2F`)
- Both items centered vertically and horizontally on the page
- A thin accent line in primary blue (`#144D8B`) between or below the two text items

---

## Interior Page Layout

Every interior page (all pages after the cover) must have three zones:

### 1. Header Band (top of every interior page)
- Dark navy band (`#0E1A2F`), approximately 48 points tall, full page width
- White text (`#FFFFFF`): `QUANTAL AI / EFFORT ESTIMATION`
- Primary-blue horizontal accent rule (`#144D8B`) immediately below the header band

### 2. Main Content Area

| Element | Style |
|---|---|
| Major section headings | Primary blue (`#144D8B`), bold |
| High-risk epic title | Red (`#B8272B`), bold, pale blue-gray panel background |
| Medium-risk epic title | Amber (`#AD6108`), bold, pale blue-gray panel background |
| Low-risk epic title | Teal (`#076B6B`), bold, pale blue-gray panel background |
| Label text (SCOPE, RATIONALE, ASSUMPTIONS, DEPENDENCIES) | Primary blue (`#144D8B`) or teal (`#076B6B`), bold uppercase |
| Body text | Slate (`#333D4D`) |
| Assumptions / overridable defaults | Teal (`#076B6B`), indented, explicitly labeled "Default — confirm or override" |
| Gantt chart | Full-width embedded image, framed by a thin pale blue-gray (`#F0F5FA`) border, own page or section if it would otherwise force an awkward page break |

### 3. Footer (bottom of every interior page)
- Thin pale blue-gray horizontal rule (`#F0F5FA`) above footer text
- **Left:** `CONFIDENTIAL - Quantal AI Internal Engineering Estimate`
- **Right:** Page number in format `X / Y` (current page / total pages)
- Footer text color: muted slate (`#667385`)
- **The cover page has no footer and no page number**

---

## Gantt Chart Generation

Use `scripts/generate_gantt_svg.py` — a pure-standard-library Python script (no `pip
install` needed, so it can't fail on a missing dependency the way ad hoc
matplotlib/reportlab code can). It renders a vector SVG, not a raster PNG, so it stays
legible at any print resolution instead of needing a DPI target.

**Do not hand-write chart-generation code.** Generate `gantt_data.json`, run the script,
embed the resulting SVG.

### `gantt_data.json` schema

```json
{
  "sprint_count": 4,
  "epics": [
    {"name": "Epic title", "start_sprint": 1, "end_sprint": 2, "risk": "high"}
  ],
  "tracks": [
    {"name": "QA / Testing", "start_sprint": 1, "end_sprint": 4, "kind": "band"},
    {"name": "UAT", "start_sprint": 3, "end_sprint": 4, "kind": "band"},
    {"name": "Deployment / Release", "start_sprint": 4, "end_sprint": 4, "kind": "band"},
    {"name": "PM / Coordination", "kind": "continuous"}
  ]
}
```

- `epics[].risk`: `"high"` / `"medium"` / `"low"` → maps to the fixed risk palette
  (red/amber/teal). Rows render epics first, ordered by `start_sprint`.
- `tracks[].kind`: `"band"` (uses `start_sprint`/`end_sprint`) or `"continuous"` (spans
  the full `sprint_count` automatically — use this for the PM/Coordination track). Track
  bars cycle through primary blue (`#144D8B`) and muted slate (`#667385`), not the risk
  palette, since they aren't risk-classified epics.
- Any epic or track may set an explicit `"color"` hex value to override the default.
- X-axis is always sprint numbers (Sprint 1, Sprint 2, ...), not calendar dates, unless
  the user supplied a real project start date during intake — in that case, label the
  sprint columns with the corresponding date ranges when building `gantt_data.json`
  (the script itself is sprint-number-only; date labels are a caller-side naming choice
  via the epic/track `name`/sprint mapping, not a script feature).

### Embedding the SVG (both are required — verified empirically, not optional polish)

1. **Declare UTF-8** on the wrapping HTML document (`<meta charset="utf-8">`). Without
   it, some renderers fall back to Latin-1 and the truncation ellipsis (`…`) the script
   emits for long epic titles renders as mojibake (`â€¦`).
2. **Scale to the page content width**, don't embed at the SVG's raw pixel size:
   ```html
   <div class="gantt-frame" style="border:1px solid #F0F5FA; padding:8px;">
     <svg ...>...</svg>   <!-- paste the script's output inline -->
   </div>
   <style>.gantt-frame svg { width: 100%; height: auto; display: block; }</style>
   ```
   The script sizes its `viewBox` to whatever is wider — the sprint grid or the legend —
   which is usually wider than the page's ~504pt content area (7in at the standard
   54pt margins). Embedding at raw pixel size silently clips the rightmost sprint
   column(s) off the page; `width:100%` scales the whole chart down to fit instead.
3. Frame the chart in a thin pale blue-gray (`#F0F5FA`) border, on its own page or
   section if it would otherwise force an awkward page break.

---

## PDF Generation Notes

- **Prefer an HTML+CSS route (e.g. `weasyprint`, `wkhtmltopdf`, headless Chrome print-to-PDF)** over a raster-image-based pipeline (`reportlab` + matplotlib). The Gantt chart is generated as SVG specifically so it can be embedded inline in the report HTML with zero conversion step — no PNG rasterization, no extra dependency. This path is validated: `weasyprint <report>.html <report>.pdf` produces correct output when the embedding rules above are followed.
- If only a raster-based tool is available (e.g. `reportlab` without an HTML layer), the SVG must first be rasterized to PNG by some available means (e.g. a headless-browser screenshot) — do not hand-roll SVG rasterization.
- Generate the Gantt chart SVG first (Step 5), then assemble the full report HTML around it, then render to PDF.
- Always verify the output using the validation checklist in the main `SKILL.md`.
- If PDF generation is fully blocked (no suitable tool available), report the blocker clearly and deliver the Markdown report as the primary output, with the Gantt chart described as a markdown table fallback.
