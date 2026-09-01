#!/usr/bin/env python3
"""Render a report manifest (JSON) into the fixed Quantal AI PDF visual system.

Single fixed pipeline: manifest.json -> self-contained HTML (embedded CSS) ->
`weasyprint` CLI -> PDF. This is the ONLY rendering path this skill supports.
Do not hand-write HTML/CSS for a report and do not substitute a different PDF
tool (reportlab, pandoc, wkhtmltopdf, ...) — tool-per-environment selection is
what caused report layout/fonts to drift by repo in the previous design.

Usage:
    python3 render_report.py --input manifest.json --output report.pdf [--keep-html]

See references/manifest_schema.md for the manifest format and
references/visual_system.md for the fixed palette/geometry this script
implements.
"""

import argparse
import html
import json
import shutil
import subprocess
import sys
from pathlib import Path

LEVEL_COLORS = {
    "critical": "#B8272B",
    "warning": "#AD6108",
    "info": "#076B6B",
    "default": "#144D8B",
}

DARK_NAVY = "#0E1A2F"
PRIMARY_BLUE = "#144D8B"
SLATE_TEXT = "#333D4D"
MUTED_SLATE = "#667385"
PALE_BG = "#F0F5FA"
WHITE = "#FFFFFF"


def esc(s):
    return html.escape(str(s), quote=True)


def render_cover(manifest):
    cover = manifest["cover"]
    subtitle = cover.get("subtitle", "Quantal AI")
    return f'''
<div class="cover">
  <div class="cover-inner">
    <div class="cover-title">{esc(cover["title"])}</div>
    <div class="cover-rule"></div>
    <div class="cover-subtitle">{esc(subtitle)}</div>
  </div>
</div>
'''


def render_metadata_table(rows):
    trs = "\n".join(
        f'<tr><td class="meta-label">{esc(r["label"])}</td><td class="meta-value">{esc(r["value"])}</td></tr>'
        for r in rows
    )
    return f'<table class="meta-table">{trs}</table>'


def render_table(section):
    headers = "".join(f"<th>{esc(h)}</th>" for h in section["headers"])
    rows = ""
    for row in section["rows"]:
        cells = "".join(f"<td>{esc(c)}</td>" for c in row)
        rows += f"<tr>{cells}</tr>"
    return f'<table class="data-table"><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table>'


def render_list(section):
    items = "".join(f"<li>{esc(item)}</li>" for item in section["items"])
    tag = "ol" if section.get("ordered") else "ul"
    return f"<{tag}>{items}</{tag}>"


def render_panel_field(field):
    label = esc(field["label"].upper())
    style = field.get("style", "body")
    body = field.get("body", "")
    if style == "quote":
        body_html = f'<div class="field-quote">{esc(body)}</div>'
    elif style == "list":
        items = "".join(f"<li>{esc(i)}</li>" for i in field.get("items", []))
        body_html = f'<ul class="field-list">{items}</ul>'
    elif style == "code":
        body_html = f'<div class="field-code">{esc(body)}</div>'
    else:
        body_html = f'<div class="field-body">{esc(body)}</div>'
    return f'<div class="field"><div class="field-label">{label}</div>{body_html}</div>'


def render_panel(section):
    level = section.get("level", "default")
    color = section.get("color") or LEVEL_COLORS.get(level, LEVEL_COLORS["default"])
    fields_html = "".join(render_panel_field(f) for f in section.get("fields", []))
    return (
        f'<div class="panel">'
        f'<div class="panel-title" style="color:{color};">{esc(section["title"])}</div>'
        f'{fields_html}'
        f'</div>'
    )


def render_chart(section, base_dir):
    svg_path = base_dir / section["svg_path"]
    if not svg_path.exists():
        raise FileNotFoundError(f"chart svg_path not found: {svg_path}")
    svg_content = svg_path.read_text(encoding="utf-8")
    caption = section.get("caption", "")
    caption_html = f'<div class="chart-caption">{esc(caption)}</div>' if caption else ""
    return f'<div class="chart-frame">{svg_content}</div>{caption_html}'


def render_section(section, base_dir):
    t = section["type"]
    if t == "heading":
        return f'<h2>{esc(section["text"])}</h2>'
    if t == "subheading":
        return f'<h3>{esc(section["text"])}</h3>'
    if t == "paragraph":
        return f'<p>{esc(section["text"])}</p>'
    if t == "panel":
        return render_panel(section)
    if t == "table":
        return render_table(section)
    if t == "list":
        return render_list(section)
    if t == "chart":
        return render_chart(section, base_dir)
    if t == "disclosure":
        return f'<div class="disclosure">{esc(section["text"])}</div>'
    if t == "pagebreak":
        return '<div class="pagebreak"></div>'
    raise ValueError(f"unknown section type: {t}")


CSS_TEMPLATE = f"""
@page {{
  size: letter;
  margin: 96pt 54pt 66pt 54pt;
  @top-left {{ content: ""; }}
  @top-right {{ content: ""; }}
  @top-center {{
    content: "%(header_text)s";
    background: {DARK_NAVY};
    color: {WHITE};
    font-family: Helvetica, Arial, sans-serif;
    font-weight: bold;
    font-size: 10.5pt;
    letter-spacing: 0.06em;
    vertical-align: middle;
    width: 100%%;
    border-bottom: 2pt solid {PRIMARY_BLUE};
    padding-left: 54pt;
  }}
  @bottom-left {{
    content: "%(footer_text)s";
    color: {MUTED_SLATE};
    font-family: Helvetica, Arial, sans-serif;
    font-size: 8pt;
  }}
  @bottom-right {{
    content: counter(page) " / " counter(pages);
    color: {MUTED_SLATE};
    font-family: Helvetica, Arial, sans-serif;
    font-size: 8pt;
  }}
}}

@page cover {{
  margin: 0;
  @top-left {{ content: none; }}
  @top-center {{ content: none; }}
  @top-right {{ content: none; }}
  @bottom-left {{ content: none; }}
  @bottom-right {{ content: none; }}
}}

* {{ box-sizing: border-box; }}

body {{
  font-family: Helvetica, Arial, sans-serif;
  color: {SLATE_TEXT};
  font-size: 10.5pt;
  line-height: 1.5;
  margin: 0;
}}

.cover {{
  page: cover;
  width: 100%%;
  height: 792pt;
  background: {DARK_NAVY};
  display: flex;
  align-items: center;
  justify-content: center;
}}
.cover-inner {{ text-align: center; }}
.cover-title {{
  color: {WHITE};
  font-size: 30pt;
  font-weight: bold;
  margin-bottom: 18pt;
}}
.cover-rule {{
  width: 120pt;
  height: 2pt;
  background: {PRIMARY_BLUE};
  margin: 0 auto 18pt auto;
}}
.cover-subtitle {{
  color: {WHITE};
  font-size: 13pt;
}}

h2 {{
  color: {PRIMARY_BLUE};
  font-size: 15pt;
  font-weight: bold;
  margin: 18pt 0 8pt 0;
  page-break-after: avoid;
}}
h3 {{
  color: {PRIMARY_BLUE};
  font-size: 12pt;
  font-weight: bold;
  margin: 14pt 0 6pt 0;
  page-break-after: avoid;
}}
p {{ margin: 0 0 8pt 0; }}

.meta-table, .data-table {{
  width: 100%%;
  border-collapse: collapse;
  margin: 8pt 0 14pt 0;
  font-size: 10pt;
}}
.meta-table td, .data-table td, .data-table th {{
  border: 0.75pt solid {PALE_BG};
  padding: 5pt 8pt;
  text-align: left;
  vertical-align: top;
}}
.meta-label {{ color: {PRIMARY_BLUE}; font-weight: bold; width: 32%%; background: {PALE_BG}; }}
.data-table th {{ background: {PALE_BG}; color: {PRIMARY_BLUE}; font-weight: bold; }}

.panel {{
  background: {PALE_BG};
  border-radius: 3pt;
  padding: 10pt 12pt;
  margin: 0 0 12pt 0;
  page-break-inside: avoid;
}}
.panel-title {{
  font-size: 12pt;
  font-weight: bold;
  margin-bottom: 8pt;
}}
.field {{ margin-bottom: 7pt; }}
.field:last-child {{ margin-bottom: 0; }}
.field-label {{
  color: {PRIMARY_BLUE};
  font-weight: bold;
  font-size: 8.5pt;
  letter-spacing: 0.05em;
  margin-bottom: 2pt;
}}
.field-body {{ color: {SLATE_TEXT}; }}
.field-quote {{
  color: {LEVEL_COLORS['info']};
  padding-left: 8pt;
  border-left: 2pt solid {LEVEL_COLORS['info']};
}}
.field-list {{ margin: 2pt 0 0 0; padding-left: 16pt; }}
.field-code {{
  font-family: "Courier New", monospace;
  background: {WHITE};
  border: 0.75pt solid {PALE_BG};
  padding: 6pt 8pt;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-size: 9pt;
}}

.disclosure {{
  color: {LEVEL_COLORS['info']};
  font-size: 9.5pt;
  font-style: italic;
  margin: 4pt 0 14pt 0;
  padding-left: 8pt;
  border-left: 2pt solid {LEVEL_COLORS['info']};
}}

.chart-frame {{
  border: 1pt solid {PALE_BG};
  padding: 8pt;
  margin: 8pt 0 4pt 0;
}}
.chart-frame svg {{ width: 100%%; height: auto; display: block; }}
.chart-caption {{
  color: {MUTED_SLATE};
  font-size: 9pt;
  text-align: center;
  margin-bottom: 12pt;
}}

.pagebreak {{ page-break-after: always; }}

ul, ol {{ margin: 0 0 8pt 0; padding-left: 18pt; }}
"""


def build_css(header_text, footer_text):
    return CSS_TEMPLATE % {
        "header_text": esc(header_text).replace('"', '\\"'),
        "footer_text": esc(footer_text).replace('"', '\\"'),
    }


def build_html(manifest, base_dir):
    header_text = f'QUANTAL AI  /  {manifest["report_type"]}'
    footer_text = manifest["footer_text"]
    css = build_css(header_text, footer_text)

    body_parts = [render_cover(manifest)]
    body_parts.append('<div class="content">')
    if manifest.get("metadata_table"):
        body_parts.append(render_metadata_table(manifest["metadata_table"]))
    for section in manifest.get("sections", []):
        body_parts.append(render_section(section, base_dir))
    body_parts.append("</div>")

    body_html = "\n".join(body_parts)
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{esc(manifest["cover"]["title"])}</title>
<style>{css}</style>
</head>
<body>
{body_html}
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", required=True, help="Path to manifest.json")
    parser.add_argument("--output", required=True, help="Path to write the output .pdf")
    parser.add_argument("--keep-html", action="store_true", help="Keep the intermediate .html file next to the output")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    base_dir = input_path.parent

    manifest = json.loads(input_path.read_text(encoding="utf-8"))
    for required in ("report_type", "cover", "footer_text"):
        if required not in manifest:
            print(f"error: manifest missing required field: {required}", file=sys.stderr)
            sys.exit(1)

    html_content = build_html(manifest, base_dir)
    html_path = output_path.with_suffix(".html")
    html_path.write_text(html_content, encoding="utf-8")

    weasyprint_bin = shutil.which("weasyprint")
    if not weasyprint_bin:
        print(
            "error: weasyprint is not installed or not on PATH. "
            "This skill requires weasyprint as the single fixed rendering pipeline "
            "(install with `pip install weasyprint` or `brew install weasyprint`). "
            f"The intermediate HTML was written to {html_path} so it is not lost.",
            file=sys.stderr,
        )
        sys.exit(2)

    result = subprocess.run(
        [weasyprint_bin, str(html_path), str(output_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"error: weasyprint failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(result.returncode)

    if not args.keep_html:
        html_path.unlink(missing_ok=True)

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
