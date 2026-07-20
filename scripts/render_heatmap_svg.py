import os
import json
from datetime import datetime

INPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "contrib-heatmap.svg")

PALETTE = [
    "#161b22",  # level 0 (none)
    "#0e4429",  # level 1
    "#006d32",  # level 2
    "#26a641",  # level 3
    "#39d353",  # level 4
    "#69f0a0",  # level 5 (neon top end)
]

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def render_heatmap():
    if not os.path.exists(INPUT_PATH):
        print(f"Error: {INPUT_PATH} not found. Run fetch_contributions.py first.")
        return

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total_contributions = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)

    BOX_SIZE = 11
    BOX_GAP = 3
    PADDING_LEFT = 40
    PADDING_TOP = 40
    
    svg_width = 860
    svg_height = 175

    weeks = []
    current_week = []
    for day in days:
        current_week.append(day)
        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []
    if current_week:
        weeks.append(current_week)

    weeks = weeks[-53:]

    rects_svg = []
    months_svg = []
    last_month = -1

    for w_idx, week in enumerate(weeks):
        x = PADDING_LEFT + w_idx * (BOX_SIZE + BOX_GAP)
        
        if week:
            first_day_date = datetime.strptime(week[0]["date"], "%Y-%m-%d")
            month = first_day_date.month
            if month != last_month and w_idx < 50:
                month_name = MONTH_NAMES[month - 1]
                months_svg.append(
                    f'<text x="{x}" y="{PADDING_TOP - 10}" class="month-text">{month_name}</text>'
                )
                last_month = month

        for d_idx, day in enumerate(week):
            y = PADDING_TOP + d_idx * (BOX_SIZE + BOX_GAP)
            lvl = day.get("level", 0)
            lvl = min(lvl, len(PALETTE) - 1)
            color = PALETTE[lvl]
            count = day.get("count", 0)
            date = day.get("date", "")

            delay = (w_idx * 0.015) + (d_idx * 0.02)
            
            rects_svg.append(
                f'<rect class="day-box" x="{x}" y="{y}" width="{BOX_SIZE}" height="{BOX_SIZE}" rx="2" ry="2" '
                f'fill="{color}" style="animation-delay: {delay:.3f}s;">'
                f'<title>{count} contributions on {date}</title></rect>'
            )

    day_labels_svg = []
    day_names = [("", 0), ("Mon", 1), ("", 2), ("Wed", 3), ("", 4), ("Fri", 5), ("", 6)]
    for name, idx in day_names:
        if name:
            y = PADDING_TOP + idx * (BOX_SIZE + BOX_GAP) + 9
            day_labels_svg.append(
                f'<text x="{PADDING_LEFT - 10}" y="{y}" class="day-label" text-anchor="end">{name}</text>'
            )

    legend_x_start = svg_width - 150
    legend_y = svg_height - 18
    legend_rects = []
    for idx, c in enumerate(PALETTE):
        lx = legend_x_start + idx * (BOX_SIZE + 2)
        legend_rects.append(
            f'<rect x="{lx}" y="{legend_y}" width="{BOX_SIZE}" height="{BOX_SIZE}" rx="2" ry="2" fill="{c}" />'
        )

    legend_svg = (
        f'<text x="{legend_x_start - 28}" y="{legend_y + 9}" class="legend-text">Less</text>'
        + "".join(legend_rects) +
        f'<text x="{legend_x_start + len(PALETTE) * (BOX_SIZE + 2) + 6}" y="{legend_y + 9}" class="legend-text">More</text>'
    )

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" fill="none">
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1px; }}
    .header-title {{ fill: #c9d1d9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 600; }}
    .header-stat {{ fill: #8b949e; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 12px; }}
    .month-text {{ fill: #8b949e; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 10px; }}
    .day-label {{ fill: #8b949e; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 9px; }}
    .legend-text {{ fill: #8b949e; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 10px; }}
    
    .day-box {{
      opacity: 0;
      animation: fadeIn 0.4s ease-out forwards;
    }}
    
    @keyframes fadeIn {{
      0% {{ opacity: 0; }}
      100% {{ opacity: 1; }}
    }}
  </style>

  <rect width="{svg_width}" height="{svg_height}" rx="12" ry="12" class="bg" />
  
  <!-- Header -->
  <text x="{PADDING_LEFT}" y="22" class="header-title">{total_contributions:,} contributions in the last year</text>
  <text x="{svg_width - 250}" y="22" class="header-stat" text-anchor="end">🔥 Current Streak: {current_streak} days | Longest: {longest_streak} days</text>
  
  <!-- Month Labels -->
  {"".join(months_svg)}
  
  <!-- Day Labels -->
  {"".join(day_labels_svg)}

  <!-- Heatmap Boxes -->
  {"".join(rects_svg)}

  <!-- Legend -->
  {legend_svg}
</svg>
'''

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Successfully generated {OUTPUT_PATH}")

if __name__ == "__main__":
    render_heatmap()
