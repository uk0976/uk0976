import os
import cv2
import numpy as np
from PIL import Image

PREPPED_PATH = os.path.join(os.path.dirname(__file__), "..", "source-prepped.png")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "avi-ascii.svg")

RAMP = " .`:-=+*cs#%@"  # Bright -> Dark density ramp

DEFAULT_AVATAR_ASCII = [
    "                      .::-::.                      ",
    "                   .-=========-.                   ",
    "                 .-=============--.                ",
    "                .==================.               ",
    "               .====================.              ",
    "              .======================.             ",
    "             .========================.            ",
    "            .====+----------------+====.           ",
    "           .====|                  |====.          ",
    "          .====|  (o)          (o)  |====.         ",
    "         .=====|       ______       |=====.        ",
    "        .======|      \\______/      |======.       ",
    "       .=======|                    |=======.      ",
    "      .========+\\__________________/+=.======.     ",
    "     .========================================.    ",
    "    .==========================================.   ",
    "   :============================================:  ",
    "  :==============================================: ",
    "  :==============================================: ",
    "  :==============================================: ",
    "  .++++++++++++++++++++++++++++++++++++++++++++++. ",
    "  |    [!] DEVELOPER TERMINAL // UK0976         | ",
    "  +----------------------------------------------+ ",
    "   |  SYSTEM: ONLINE    STATUS: READY          |  ",
    "   +-------------------------------------------+   ",
    "    \\_________________________________________/    ",
    "                      |    |                       ",
    "                   ___|____|___                    ",
    "                  /            \\                   ",
    "                 /______________\\                  "
]

def image_to_ascii(image_path, width=54):
    if not os.path.exists(image_path):
        return DEFAULT_AVATAR_ASCII

    img = Image.open(image_path).convert("L")
    aspect_ratio = img.height / img.width
    # Character aspect ratio is roughly 0.55
    height = int(width * aspect_ratio * 0.55)
    img = img.resize((width, height), Image.Resampling.LANCZOS)

    pixels = np.array(img)
    lines = []
    for row in pixels:
        line_chars = []
        for p in row:
            # Map 0..255 to 0..len(RAMP)-1
            idx = int((p / 255.0) * (len(RAMP) - 1))
            line_chars.append(RAMP[idx])
        lines.append("".join(line_chars))
    return lines

def make_ascii_svg():
    lines = image_to_ascii(PREPPED_PATH, width=52)

    svg_width = 370
    svg_height = 280
    
    font_size = 8
    line_height = 8.5
    start_y = 20

    # Wrap each row in a clipPath that animates width from 0 to 100%
    clip_paths = []
    text_elements = []

    total_lines = len(lines)
    duration_per_line = 0.05
    start_delay = 0.1

    for idx, line_str in enumerate(lines):
        clip_id = f"clip-row-{idx}"
        y = start_y + idx * line_height
        delay = start_delay + idx * duration_per_line

        # Escaping XML entities
        safe_line = (
            line_str.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace(" ", "&#160;")
        )

        clip_paths.append(
            f'<clipPath id="{clip_id}">'
            f'<rect x="0" y="{y - font_size}" width="0" height="{line_height + 2}">'
            f'<animate attributeName="width" from="0" to="{svg_width}" dur="0.15s" begin="{delay:.2f}s" fill="freeze" />'
            f'</rect>'
            f'</clipPath>'
        )

        text_elements.append(
            f'<text x="15" y="{y}" class="ascii-row" clip-path="url(#{clip_id})">{safe_line}</text>'
        )

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" fill="none">
  <style>
    .bg {{ fill: #0d1117; rx: 12px; }}
    .ascii-row {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
      font-size: {font_size}px;
      fill: #8b949e;
      white-space: pre;
      letter-spacing: 0.5px;
    }}
  </style>

  <rect width="{svg_width}" height="{svg_height}" class="bg" stroke="#30363d" stroke-width="1" />
  
  <defs>
    {"".join(clip_paths)}
  </defs>

  {"".join(text_elements)}
</svg>
'''

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Successfully generated {OUTPUT_PATH}")

if __name__ == "__main__":
    make_ascii_svg()
