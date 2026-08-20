from pathlib import Path
from PIL import Image, ImageOps

INPUT = Path("source-prepped.png")
OUTPUT = Path("avi-ascii.svg")

WIDTH = 100
FONT_SIZE = 8
LINE_HEIGHT = 10

RAMP = " .`:-=+*cs#%@"

image = Image.open(INPUT).convert("L")

# Crop away most of the white background
bbox = ImageOps.invert(image).getbbox()

if bbox:
    image = image.crop(bbox)

# Resize while compensating for character aspect ratio
aspect = image.height / image.width
height = max(1, int(WIDTH * aspect * 0.48))

image = image.resize((WIDTH, height))

pixels = image.load()

rows = []

for y in range(height):
    row = ""

    for x in range(WIDTH):
        brightness = pixels[x, y]
        index = int((255 - brightness) / 256 * len(RAMP))
        index = min(index, len(RAMP) - 1)
        row += RAMP[index]

    rows.append(row)

svg_width = WIDTH * FONT_SIZE
svg_height = height * LINE_HEIGHT + 20

svg = []

svg.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'viewBox="0 0 {svg_width} {svg_height}" '
    f'width="{svg_width}" height="{svg_height}">'
)

svg.append("""
<style>
.ascii {
    font-family: "Courier New", monospace;
    font-size: 8px;
    font-weight: bold;
    fill: #444;
}

.row {
    animation: reveal 0.8s ease-out forwards;
    opacity: 0;
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
""")

svg.append(
    '<rect width="100%" height="100%" fill="white"/>'
)

for y, row in enumerate(rows):
    escaped = (
        row.replace("&", "&amp;")
           .replace("<", "&lt;")
           .replace(">", "&gt;")
    )

    delay = y * 0.035
    y_position = 12 + y * LINE_HEIGHT

    svg.append(
        f'<text class="ascii row" '
        f'x="0" y="{y_position}" '
        f'style="animation-delay:{delay:.3f}s">'
        f'{escaped}</text>'
    )

svg.append("</svg>")

OUTPUT.write_text("\n".join(svg), encoding="utf-8")

print(f"Created: {OUTPUT}")