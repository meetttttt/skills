# Visual System — Document Generation

This document defines the **fixed, immutable visual standard** implemented by
`scripts/render_report.py`. Every report rendered by this skill — regardless
of which skill produced its content — looks like one consistent Quantal AI
product line. Nothing here is configurable per project; only the manifest's
*content* varies.

---

## Document Format

| Property | Value |
|---|---|
| Page size | US Letter, portrait — 612 × 792 points |
| Left/right margin | 54 points |
| Top margin (reserved for header band) | 96 points |
| Bottom margin (reserved for footer) | 66 points |
| Primary typeface | Helvetica / Helvetica Bold (sans-serif) |
| Fallback typeface | Any highly legible sans-serif (e.g. Arial, DejaVu Sans) |

Content never overlaps the header band, footer, or page numbers — this is
enforced structurally by CSS Paged Media margin boxes in
`render_report.py`, not by manual spacing per report.

---

## Color Palette (Exact Hex Values)

| Role | Hex | Usage |
|---|---|---|
| **Dark navy** | `#0E1A2F` | Cover background, header band |
| **Primary blue** | `#144D8B` | Major headings, accent rules, labels, metadata table headers |
| **Slate text** | `#333D4D` | All body text |
| **Muted slate** | `#667385` | Footer text, secondary metadata |
| **Pale blue-gray** | `#F0F5FA` | Panel backgrounds, table borders, chart frame border |
| **White** | `#FFFFFF` | Cover page text, header text, bar labels |

### The `level` → color mapping (shared across every report type)

| `level` | Hex | Meaning is defined by the calling skill |
|---|---|---|
| `critical` | `#B8272B` (red) | e.g. P0/P1 findings, High-risk/complexity epics |
| `warning` | `#AD6108` (amber) | e.g. P2 findings, Medium-risk/complexity epics |
| `info` | `#076B6B` (teal) | e.g. P3 findings, Low-risk/complexity epics, assumption/default labels |
| `default` | `#144D8B` (primary blue) | Unleveled content — a panel with no severity/risk connotation |

`level` is deliberately a neutral name, not "severity" or "risk" — the same
three colors mean different things in different report types (bug severity in
a code review, estimation complexity in an effort estimate). Because the
manifest field itself is neutral, **no calling skill needs to disclose or
apologize for reusing the palette** — just don't use `critical`/`warning` to
imply a defect exists when the report is about something else (e.g. schedule
risk) without making that clear in the section text itself.

---

## Required First Page — Cover Page

The first page is **exclusively** a cover page with **only two elements**:

1. **Report title** (`cover.title`) — large, bold, white text
2. **Subtitle** (`cover.subtitle`, defaults to `Quantal AI`) — smaller white text, directly beneath the title

**Cover page must NOT include:** report type label, date, counts/metrics,
subtitle beyond the one field above, scope, methodology, confidentiality
label, footer, or page number. `render_report.py` enforces this structurally
— the cover uses a separate `@page cover` rule with all header/footer margin
boxes explicitly cleared.

**Cover page layout:**
- Full-page dark navy background (`#0E1A2F`)
- Both items centered vertically and horizontally
- A thin primary-blue (`#144D8B`) accent line between the two text items

---

## Interior Page Layout

Every interior page (all pages after the cover) has three zones, all
produced automatically by the fixed CSS in `render_report.py` — a calling
skill only supplies the two text values (`report_type`, `footer_text`) that
appear in them:

### 1. Header Band
- Dark navy band (`#0E1A2F`), full page width
- White bold text: `QUANTAL AI  /  {report_type}` (from the manifest's `report_type` field, e.g. `REPOSITORY AUDIT`, `EFFORT ESTIMATION`)
- Primary-blue accent rule immediately below

### 2. Main Content Area

| Element | Style |
|---|---|
| Major section heading (`type: "heading"`) | Primary blue, bold |
| Subheading (`type: "subheading"`) | Primary blue, bold, smaller |
| Panel title (`type: "panel"`) | Colored per `level` (see mapping above), bold, pale blue-gray panel background |
| Field label inside a panel (EVIDENCE, SCOPE, RATIONALE, ...) | Primary blue, bold, uppercase |
| Body text | Slate |
| `style: "quote"` field (e.g. an AI implementation prompt) | Teal, left border, indented |
| `style: "code"` field | Monospace, pale blue-gray background |
| `type: "disclosure"` | Teal, italic, left border — for a one-line clarifying note |
| `type: "chart"` | Full-width embedded SVG, framed by a thin pale blue-gray border |
| `type: "table"` | Pale blue-gray header row, thin pale blue-gray cell borders |

### 3. Footer
- Thin pale blue-gray rule above footer text
- **Left:** `footer_text` from the manifest (e.g. `CONFIDENTIAL - Quantal AI Internal Engineering Review`)
- **Right:** Page number, format `X / Y`
- Footer text color: muted slate
- **The cover page has no footer and no page number**

---

## Rendering Pipeline (fixed, do not substitute)

`scripts/render_report.py` implements this visual system as embedded CSS
(CSS Paged Media: `@page` margin boxes for the repeating header/footer,
`@page cover` for the cover page) and renders via the `weasyprint` CLI. This
was chosen and validated over a raster-image pipeline (`reportlab` +
matplotlib) specifically because:

- CSS Paged Media margin boxes reproduce the header band, accent rule, and
  footer identically on every interior page without per-report layout code.
- The Gantt chart (or any future chart) is generated as SVG and embedded
  inline — no rasterization step, so it stays sharp at any print size.
- It is one deterministic path, not "whatever tool is available," which is
  what caused the original layout/font drift this skill exists to fix.

Do not add a fallback to another PDF tool. If `weasyprint` is unavailable,
that is a blocker to report, not a reason to render differently.
