import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "info-card.svg")

def make_info_card():
    svg_width = 490
    svg_height = 280

    rows = [
        ("OS", "Developer Workstation (Windows 11 x86_64)", "#58a6ff"),
        ("Host", "Umerkhan Junaidkhan (AI & Data Science Student)", "#79c0ff"),
        ("Focus", "AI/ML, RAG Systems & Computer Vision", "#d2a8ff"),
        ("Stack", "Python, TensorFlow, SpaCy, OpenCV, JS, SQL", "#7ee787"),
        ("Projects", "NSERS, StockSage, MedInsight, Smart Scheduler", "#ffa657"),
        ("Uptime", "24/7 Learning, Coding & Innovating", "#ff7b72"),
        ("Status", "🚀 Open for Collaborations & Internships", "#38d8f0"),
    ]

    lines_svg = []
    
    # Title bar line
    title_line = (
        '<text x="25" y="42" class="line title-user">'
        '<tspan fill="#58a6ff" font-weight="bold" font-size="15">uk0976</tspan>'
        '<tspan fill="#8b949e" font-size="15">@</tspan>'
        '<tspan fill="#7ee787" font-weight="bold" font-size="15">github</tspan>'
        '</text>'
    )
    lines_svg.append(title_line)

    # Separator line
    sep_line = (
        '<text x="25" y="60" class="line sep">'
        '---------------------------------------</text>'
    )
    lines_svg.append(sep_line)

    # Key Value Rows
    y_start = 85
    y_step = 24
    for idx, (key, value, color) in enumerate(rows):
        y = y_start + idx * y_step
        delay = 0.2 + idx * 0.08
        line_code = (
            f'<g class="fade-row" style="animation-delay: {delay:.2f}s;">'
            f'<text x="25" y="{y}" class="line">'
            f'<tspan fill="{color}" font-weight="bold">{key}:</tspan> '
            f'<tspan fill="#c9d1d9">{value}</tspan>'
            f'</text>'
            f'</g>'
        )
        lines_svg.append(line_code)

    # Terminal Color Palette Swatches
    swatch_y = y_start + len(rows) * y_step + 12
    colors = ["#ff7b72", "#7ee787", "#ffa657", "#58a6ff", "#d2a8ff", "#38d8f0", "#c9d1d9"]
    swatches_svg = []
    for idx, c in enumerate(colors):
        sx = 25 + idx * 22
        swatches_svg.append(
            f'<rect class="swatch" x="{sx}" y="{swatch_y}" width="16" height="12" rx="2" ry="2" fill="{c}" />'
        )

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" fill="none">
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1px; }}
    .line {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
      font-size: 13px;
    }}
    .sep {{ fill: #484f58; font-size: 13px; }}
    
    .fade-row {{
      opacity: 0;
      animation: fadeIn 0.4s ease-in-out forwards;
    }}

    @keyframes fadeIn {{
      0% {{ opacity: 0; }}
      100% {{ opacity: 1; }}
    }}
  </style>

  <rect width="{svg_width}" height="{svg_height}" rx="12" ry="12" class="bg" />
  
  {"".join(lines_svg)}
  {"".join(swatches_svg)}
</svg>
'''

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Successfully generated {OUTPUT_PATH}")

if __name__ == "__main__":
    make_info_card()
