#!/usr/bin/env python3
"""Render an Agile effort-estimation Gantt chart as SVG from a JSON data file.

Pure standard library — no pip install required, so chart generation never
depends on whatever happens to be available in the execution environment.

Usage:
    python3 generate_gantt_svg.py --input gantt_data.json --output gantt.svg

Input JSON schema:
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

- epics[].risk: "high" | "medium" | "low" -> maps to the fixed risk palette.
- tracks[].kind: "band" (uses start_sprint/end_sprint) or "continuous"
  (auto-spans the full sprint_count, per the PM/Coordination track convention).
- Any epic or track may set an explicit "color" (hex string) to override the
  default palette mapping.
- Rows render epics first (ordered by start_sprint), then tracks in the given
  order, matching pdf_visual_system.md's Y-axis ordering rule.

Output is a self-contained SVG sized to its own content (label column + sprint
grid, or the legend row, whichever is wider). It's vector, not raster, so it
stays crisp at any print DPI — but callers MUST embed it at `width: 100%` of
the page's content area rather than at its raw pixel size, or the widest rows
will be clipped. See references/pdf_visual_system.md "Embedding the SVG".
"""

import argparse
import html
import json
import sys

RISK_COLORS = {
    "high": "#B8272B",
    "medium": "#AD6108",
    "low": "#076B6B",
}
TRACK_COLORS = ["#144D8B", "#667385"]  # cycled across tracks in order
PALE_BG = "#F0F5FA"
SLATE_TEXT = "#333D4D"
MUTED_SLATE = "#667385"
PRIMARY_BLUE = "#144D8B"

SPRINT_WIDTH = 100
LABEL_COL_WIDTH = 300
ROW_HEIGHT = 40
ROW_GAP = 6
TOP_MARGIN = 40
BOTTOM_MARGIN = 50
RIGHT_MARGIN = 20
LABEL_FONT_SIZE = 12
AVG_CHAR_WIDTH = 6.4  # rough Helvetica width at 12px, used only for wrapping estimate
LABEL_PADDING = 12


def esc(s):
    return html.escape(str(s), quote=True)


def wrap_label(text, max_width_px, max_lines=2):
    """Word-wrap text to fit max_width_px, truncating with an ellipsis past max_lines."""
    max_chars = max(int(max_width_px / AVG_CHAR_WIDTH), 4)
    words = str(text).split()
    lines = []
    i = 0
    while i < len(words) and len(lines) < max_lines:
        current = words[i]
        i += 1
        while i < len(words) and len(current) + 1 + len(words[i]) <= max_chars:
            current += " " + words[i]
            i += 1
        lines.append(current)

    if i < len(words):  # words remain unconsumed -> truncated, add ellipsis
        last = lines[-1]
        while len(last) > 1 and len(last) + 1 > max_chars:
            last = last[:-1]
        lines[-1] = last.rstrip() + "…"
    return lines or [""]


def build_rows(data):
    epics = sorted(data.get("epics", []), key=lambda e: e.get("start_sprint", 1))
    rows = []
    for e in epics:
        color = e.get("color") or RISK_COLORS.get(str(e.get("risk", "")).lower(), MUTED_SLATE)
        rows.append({
            "label": e["name"],
            "start": e["start_sprint"],
            "end": e["end_sprint"],
            "color": color,
        })

    sprint_count = data["sprint_count"]
    for i, t in enumerate(data.get("tracks", [])):
        if t.get("kind") == "continuous":
            start, end = 1, sprint_count
        else:
            start, end = t["start_sprint"], t["end_sprint"]
        color = t.get("color") or TRACK_COLORS[i % len(TRACK_COLORS)]
        rows.append({
            "label": t["name"],
            "start": start,
            "end": end,
            "color": color,
        })
    return rows


def render_svg(data):
    sprint_count = data["sprint_count"]
    rows = build_rows(data)

    legend_items = [
        ("High risk", RISK_COLORS["high"]),
        ("Medium risk", RISK_COLORS["medium"]),
        ("Low risk", RISK_COLORS["low"]),
        ("Non-dev track", TRACK_COLORS[0]),
    ]
    legend_item_width = 150
    legend_width = LABEL_COL_WIDTH + len(legend_items) * legend_item_width

    chart_width = sprint_count * SPRINT_WIDTH
    grid_width = LABEL_COL_WIDTH + chart_width + RIGHT_MARGIN
    total_width = max(grid_width, legend_width)
    total_height = TOP_MARGIN + len(rows) * (ROW_HEIGHT + ROW_GAP) + BOTTOM_MARGIN

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_width} {total_height}" '
        f'width="{total_width}" height="{total_height}" font-family="Helvetica, Arial, sans-serif">'
    )
    parts.append(f'<rect x="0" y="0" width="{total_width}" height="{total_height}" fill="#FFFFFF"/>')

    # Vertical sprint gridlines + top axis labels
    for s in range(sprint_count + 1):
        x = LABEL_COL_WIDTH + s * SPRINT_WIDTH
        parts.append(
            f'<line x1="{x}" y1="{TOP_MARGIN - 10}" x2="{x}" y2="{total_height - BOTTOM_MARGIN}" '
            f'stroke="{PALE_BG}" stroke-width="2"/>'
        )
        if s < sprint_count:
            label_x = x + SPRINT_WIDTH / 2
            parts.append(
                f'<text x="{label_x}" y="{TOP_MARGIN - 16}" text-anchor="middle" '
                f'font-size="13" font-weight="bold" fill="{PRIMARY_BLUE}">Sprint {s + 1}</text>'
            )

    # Rows
    y = TOP_MARGIN
    for row in rows:
        bar_x = LABEL_COL_WIDTH + (row["start"] - 1) * SPRINT_WIDTH
        bar_w = (row["end"] - row["start"] + 1) * SPRINT_WIDTH

        # Row background band (alternating, matches finding-panel pale style)
        parts.append(
            f'<rect x="0" y="{y}" width="{total_width}" height="{ROW_HEIGHT}" fill="{PALE_BG}" opacity="0.5"/>'
        )
        # Label (word-wrapped to fit the label column, so long epic titles
        # never silently truncate against the chart grid)
        lines = wrap_label(row["label"], LABEL_COL_WIDTH - LABEL_PADDING * 2)
        line_height = LABEL_FONT_SIZE + 3
        block_height = len(lines) * line_height
        text_y = y + (ROW_HEIGHT - block_height) / 2 + LABEL_FONT_SIZE
        for line in lines:
            parts.append(
                f'<text x="{LABEL_PADDING}" y="{text_y}" font-size="{LABEL_FONT_SIZE}" fill="{SLATE_TEXT}">'
                f'{esc(line)}</text>'
            )
            text_y += line_height
        # Bar
        parts.append(
            f'<rect x="{bar_x + 4}" y="{y + 6}" width="{max(bar_w - 8, 4)}" height="{ROW_HEIGHT - 12}" '
            f'rx="4" fill="{row["color"]}"/>'
        )
        # Sprint span label inside bar
        parts.append(
            f'<text x="{bar_x + bar_w / 2}" y="{y + ROW_HEIGHT / 2 + 5}" text-anchor="middle" '
            f'font-size="12" font-weight="bold" fill="#FFFFFF">S{row["start"]}-S{row["end"]}</text>'
        )
        y += ROW_HEIGHT + ROW_GAP

    # Legend
    legend_y = total_height - BOTTOM_MARGIN + 24
    lx = LABEL_COL_WIDTH
    for label, color in legend_items:
        parts.append(f'<rect x="{lx}" y="{legend_y - 10}" width="14" height="14" rx="3" fill="{color}"/>')
        parts.append(
            f'<text x="{lx + 20}" y="{legend_y + 1}" font-size="12" fill="{MUTED_SLATE}">{esc(label)}</text>'
        )
        lx += legend_item_width

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", required=True, help="Path to gantt_data.json")
    parser.add_argument("--output", required=True, help="Path to write the output .svg")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "sprint_count" not in data:
        print("error: input JSON must include sprint_count", file=sys.stderr)
        sys.exit(1)
    if not data.get("epics") and not data.get("tracks"):
        print("error: input JSON must include at least one epic or track", file=sys.stderr)
        sys.exit(1)

    svg = render_svg(data)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
