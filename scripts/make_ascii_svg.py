from pathlib import Path
from PIL import Image, ImageOps
from html import escape

INPUT = Path("source-prepped.png")
OUTPUT = Path("avi-ascii.svg")

WIDTH = 100
FONT_SIZE = 8
LINE_HEIGHT = 10

RAMP = " .`:-=+*cs#%@"

image = Image.open(INPUT).convert("L")

# Remove large white margins around the subject
bbox = ImageOps.invert(image).getbbox()

if bbox:
    image = image.crop(bbox)

# Preserve the portrait proportions while compensating
# for the height of monospace characters.
aspect_ratio = image.height / image.width
height = max(1, int(WIDTH * aspect_ratio * 0.48))

image = image.resize((WIDTH, height))

pixels = image.load()

rows = []

for y in range(height):
    row = []

    for x in range(WIDTH):
        brightness = pixels[x, y]

        index = int((255 - brightness) / 256 * len(RAMP))
        index = min(index, len(RAMP) - 1)

        row.append(RAMP[index])

    rows.append("".join(row))


svg_width = WIDTH * FONT_SIZE
svg_height = height * LINE_HEIGHT + 20

svg = [
    f'''<svg xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xml:space="preserve"
    viewBox="0 0 {svg_width} {svg_height}"
    width="{svg_width}"
    height="{svg_height}">''',

    """
    <style>
        .ascii {
            font-family: "Courier New", monospace;
            font-size: 8px;
            font-weight: bold;
            fill: #c9d1d9;
        }

        .row {
            opacity: 0;
            animation: reveal 0.7s ease-out forwards;
        }

        @keyframes reveal {
            from {
                opacity: 0;
                transform: translateX(-8px);
            }

            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
    </style>
    """,

]


for y, row in enumerate(rows):

    delay = y * 0.035
    y_position = 12 + y * LINE_HEIGHT

    svg.append(
        f'''<text
            class="ascii row"
            x="0"
            y="{y_position}"
            xml:space="preserve"
            style="animation-delay:{delay:.3f}s">{escape(row)}</text>'''
    )


svg.append("</svg>")

OUTPUT.write_text(
    "\n".join(svg),
    encoding="utf-8"
)

print(f"Created: {OUTPUT}")