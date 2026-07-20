import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "info-card.svg")

def make_info_card():
    svg_width = 490
    svg_height = 280

    rows = [
        ("OS", "Developer Workstation (Windows 11 x86_64)", "#58a6ff"),
        ("Host", "Full Stack Engineer & AI Enthusiast", "#79c0ff"),
        ("Uptime", "24/7 Building & Innovating", "#d2a8ff"),
        ("Stack", "Python, JavaScript, TypeScript, React, Node", "#7ee787"),
        ("Tools", "Git, Docker, VSCode, Antigravity AI", "#ffa657"),
        ("Focus", "Web Development & AI Coding Systems", "#ff7b72"),
        ("Status", "🟢 Open for Collaborations & Projects", "#38d8f0"),
    ]

    lines_svg = []
    
    # Title bar line
    title_line = (
        '<text x="25" y="42" class="line title-user" style="animation-delay: 0.1s;">uk0976</text>'
        '<text x="82" y="42" class="line title-at" style="animation-delay: 0.1s;">@</text>'
        '<text x="96" y="42" class="line title-host" style="animation-delay: 0.1s;">github</text>'
    )
    lines_svg.append(title_line)

    # Separator line
    sep_line = (
        '<text x="25" y="60" class="line sep" style="animation-delay: 0.2s;">'
        '---------------------------------------</text>'
    )
    lines_svg.append(sep_line)

    # Key Value Rows
    y_start = 85
    y_step = 24
    for idx, (key, value, color) in enumerate(rows):
        y = y_start + idx * y_step
        delay = 0.3 + idx * 0.1
        line_code = (
            f'<text x="25" y="{y}" class="line" style="animation-delay: {delay:.2f}s;">'
            f'<tspan fill="{color}" font-weight="bold">{key}:</tspan> '
            f'<tspan fill="#c9d1d9">{value}</tspan>'
            f'</text>'
        )
        lines_svg.append(line_code)

    # Terminal Color Palette Swatches
    swatch_y = y_start + len(rows) * y_step + 12
    colors = ["#ff7b72", "#7ee787", "#ffa657", "#58a6ff", "#d2a8ff", "#38d8f0", "#c9d1d9"]
    swatches_svg = []
    for idx, c in enumerate(colors):
        sx = 25 + idx * 22
        delay = 0.3 + (len(rows) + 1) * 0.1 + idx * 0.05
        swatches_svg.append(
            f'<rect class="swatch" x="{sx}" y="{swatch_y}" width="16" height="12" rx="2" fill="{c}" '
            f'style="animation-delay: {delay:.2f}s;" />'
        )

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" fill="none">
  <style>
    .bg {{ fill: #0d1117; rx: 12px; }}
    .line {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
      font-size: 13px;
      opacity: 0;
      animation: slideIn 0.35s ease-out forwards;
    }}
    .title-user {{ fill: #58a6ff; font-weight: bold; font-size: 15px; }}
    .title-at {{ fill: #8b949e; font-size: 15px; }}
    .title-host {{ fill: #7ee787; font-weight: bold; font-size: 15px; }}
    .sep {{ fill: #484f58; font-size: 13px; }}
    
    .swatch {{
      opacity: 0;
      animation: fadeIn 0.3s ease-out forwards;
    }}

    @keyframes slideIn {{
      0% {{
        opacity: 0;
        transform: translateX(-12px);
      }}
      100% {{
        opacity: 1;
        transform: translateX(0);
      }}
    }}

    @keyframes fadeIn {{
      0% {{ opacity: 0; transform: scale(0.5); }}
      100% {{ opacity: 1; transform: scale(1); }}
    }}
  </style>

  <rect width="{svg_width}" height="{svg_height}" class="bg" stroke="#30363d" stroke-width="1" />
  
  {"".join(lines_svg)}
  {"".join(swatches_svg)}
</svg>
'''

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Successfully generated {OUTPUT_PATH}")

if __name__ == "__main__":
    make_info_card()
