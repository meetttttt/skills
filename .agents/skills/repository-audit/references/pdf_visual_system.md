# PDF Visual System — Repository Audit Reports

This document defines the **fixed, immutable visual standard** applied to every `repository-audit` PDF report. All values must be used exactly as specified to ensure a consistent professional appearance across all projects and engagements.

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

Never allow content to overlap headers, footers, page numbers, or margins. Maintain consistent spacing between headings, sections, findings, paragraphs, and footers.

---

## Color Palette (Exact Hex Values)

| Role | Hex | Usage |
|---|---|---|
| **Dark navy** | `#0E1A2F` | Cover background, header band |
| **Primary blue** | `#144D8B` | Major headings, accent rules, labels |
| **Slate text** | `#333D4D` | All body text |
| **Muted slate** | `#667385` | Footer text, secondary metadata |
| **Pale blue-gray** | `#F0F5FA` | Finding background panels, subtle section backgrounds |
| **P0/P1 red** | `#B8272B` | P0 and P1 finding titles |
| **P2 amber** | `#AD6108` | P2 finding titles |
| **P3 teal** | `#076B6B` | P3 finding titles, AI prompt labels |
| **White** | `#FFFFFF` | Cover page text, header text |

---

## Required First Page — Cover Page

The first page must be **exclusively** a cover page. It contains **only two elements**:

1. **Project / repository name** — large, bold, white text
2. **`Quantal AI`** — smaller white text, directly beneath the repository name

**Cover page must NOT include:**
- Audit title
- Date
- Findings count
- Branch name
- Subtitle
- Scope
- Methodology
- Confidentiality label
- Footer
- Page number
- Any other metadata or content

**Cover page layout:**
- Full-page dark navy background (`#0E1A2F`)
- Both items centered vertically and horizontally on the page
- A thin accent line in primary blue (`#144D8B`) between or below the two text items

---

## Interior Page Layout

Every interior page (all pages after the cover) must have three zones:

### 1. Header Band (top of every interior page)
- Dark navy band (`#0E1A2F`), approximately 48 points tall, full page width
- White text (`#FFFFFF`): `QUANTAL AI / REPOSITORY AUDIT`
- Primary-blue horizontal accent rule (`#144D8B`) immediately below the header band

### 2. Main Content Area
Between the header rule and the footer rule:

| Element | Style |
|---|---|
| Major section headings | Primary blue (`#144D8B`), bold |
| P0/P1 finding title | Red (`#B8272B`), bold, pale blue-gray panel background |
| P2 finding title | Amber (`#AD6108`), bold, pale blue-gray panel background |
| P3 finding title | Teal (`#076B6B`), bold, pale blue-gray panel background |
| Label text (EVIDENCE, BLAST RADIUS, REMEDIATION, AI IMPLEMENTATION PROMPT, SMOKE TEST) | Primary blue (`#144D8B`) or teal (`#076B6B`), bold uppercase |
| Body text | Slate (`#333D4D`) |
| AI implementation prompts | Teal (`#076B6B`), indented |
| Code snippets / commands | Monospace, wrapped safely, pale blue-gray background |

### 3. Footer (bottom of every interior page)
- Thin pale blue-gray horizontal rule (`#F0F5FA`) above footer text
- **Left:** `CONFIDENTIAL - Quantal AI Internal Engineering Review`
- **Right:** Page number in format `X / Y` (current page / total pages)
- Footer text color: muted slate (`#667385`)
- **The cover page has no footer and no page number**

---

## PDF Generation Notes

- The agent should use whatever PDF generation capability is available in the environment (e.g. Python `reportlab`, `weasyprint`, `pandoc` + `LaTeX`, `pdfkit`, `md-to-pdf`, etc.).
- When choosing a method, prefer one that supports custom fonts, background colors, and page-level headers/footers.
- Always verify the output using the validation checklist in the main `SKILL.md`.
- If PDF generation is fully blocked (no suitable tool available), report the blocker clearly and deliver the Markdown report as the primary output.
