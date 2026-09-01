---
name: document-generation
description: >-
  Render any structured report (code review findings, effort estimates, or any
  future report type) into the fixed Quantal AI PDF visual system — exact
  colors, cover page, header/footer, typography, and page geometry, every
  time, regardless of repo or environment. Use when another skill (or the
  user) has report content ready and needs it turned into a standardized
  professional PDF. This skill does not gather content itself — it only
  renders a manifest another skill or the user hands it.
---

# Document Generation Skill

A content-agnostic report renderer. Any skill that produces a report (code
review findings, effort estimates, status reports, etc.) hands this skill a
structured JSON manifest; this skill turns it into a Markdown-equivalent PDF
using one fixed, locked rendering pipeline.

**Why this exists as its own skill:** report generation was previously
duplicated inside each report-producing skill, each free to pick "whatever
PDF tool is available in the environment" (reportlab, weasyprint, pandoc,
wkhtmltopdf...). Different tools render fonts, spacing, and page-break
behavior differently, so the same report looked different depending on which
tool happened to be installed in a given repo's environment. This skill
removes that choice entirely — there is exactly one rendering path.

---

## Core Operating Rules

- **One fixed pipeline, no exceptions.** Manifest → HTML (embedded CSS defined in `scripts/render_report.py`) → `weasyprint` CLI → PDF. Never hand-write report HTML/CSS, never substitute a different PDF tool, and never render a report any other way — that reintroduces exactly the drift problem this skill exists to remove.
- **This skill does not gather or invent content.** The calling skill (or the user) is responsible for the manifest's content being accurate. This skill only lays it out.
- **Do not edit the visual system per-project.** Colors, fonts, cover layout, header/footer are fixed in `references/visual_system.md` and implemented in `scripts/render_report.py`. A calling skill supplies content and a `report_type`/`footer_text` label — never a different palette or layout.
- **Fail loudly, never silently degrade.** If `weasyprint` is unavailable, stop and report the blocker (with the intermediate HTML path, which is preserved) rather than falling back to an alternate tool or a differently-styled output.

---

## Step 1 — Receive the Manifest

The calling skill provides (or the user supplies directly):

1. A `manifest.json` file conforming to [references/manifest_schema.md](references/manifest_schema.md).
2. Any chart data files it references (e.g. `gantt_data.json` for a Gantt chart section — see Step 2).
3. The desired output path for the PDF.

If content is handed to you as prose/Markdown instead of a manifest, convert it into a manifest per the schema before rendering — do not invent a one-off layout instead.

---

## Step 2 — Generate Any Charts the Manifest References

If the manifest contains a `"type": "chart"` section with `"chart_type": "gantt"`:

1. Build the chart's data JSON per the schema documented in
   [references/manifest_schema.md](references/manifest_schema.md) "Gantt chart
   data".
2. Run:
   ```
   python3 scripts/generate_gantt_svg.py --input gantt_data.json --output gantt.svg
   ```
   Pure Python standard library — no `pip install` required.
3. Reference the resulting SVG's path in the manifest section's `svg_path` field. `scripts/render_report.py` inlines it automatically at render time.

Other chart types are not yet supported — if a calling skill needs a new chart type, extend `generate_gantt_svg.py`'s pattern (pure-stdlib SVG generation) rather than hand-writing chart markup inline in the manifest.

---

## Step 3 — Render the PDF

Run the bundled script — **do not hand-write HTML/CSS or call a different PDF tool:**

```
python3 scripts/render_report.py --input manifest.json --output <report>.pdf
```

This writes `<report>.pdf` using the fixed visual system. If `weasyprint` is not installed, the script exits with a clear error and preserves the intermediate `<report>.html` so no work is lost — report this blocker to the user rather than substituting another tool.

---

## Step 4 — Validate

- Verify file creation and page count with `pdfinfo`.
- Extract text with `pdftotext` when available to confirm readable content.
- Visually confirm at least the cover page and one interior page (render to PNG with `pdftoppm -png -r 100 <report>.pdf page` and view the images) whenever this skill's rendering logic has changed, or whenever a manifest exercises a section type not previously exercised in this project. For routine reports using already-proven section types, `pdfinfo`/`pdftotext` checks are sufficient.
- Confirm: cover page contains only the title and subtitle (nothing else); header band and footer appear on every interior page, not the cover; page numbers are sequential; panel/level colors match `references/visual_system.md` exactly; any chart is not clipped.
- Report any generation or validation blocker clearly — do not claim a visual check occurred if it did not.

---

## References

- [references/manifest_schema.md](references/manifest_schema.md) — the JSON manifest format every calling skill must produce, with a full field reference and worked examples.
- [references/visual_system.md](references/visual_system.md) — the fixed, immutable color palette, typography, page geometry, cover/header/footer spec, and the `level` → color mapping every report type shares.
- [scripts/render_report.py](scripts/render_report.py) — the single fixed manifest-to-PDF renderer. Never bypass it.
- [scripts/generate_gantt_svg.py](scripts/generate_gantt_svg.py) — pure-stdlib Gantt chart renderer, used when a manifest includes a Gantt chart section.
- [examples/sample_manifest_findings.json](examples/sample_manifest_findings.json) — a worked manifest for a findings-style report (e.g. code review).
- [examples/sample_manifest_gantt.json](examples/sample_manifest_gantt.json) — a worked manifest including a Gantt chart section (e.g. effort estimation).
