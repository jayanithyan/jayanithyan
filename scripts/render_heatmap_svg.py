import json
from pathlib import Path
from datetime import datetime

DATA = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")

CELL = 12
GAP = 3
RADIUS = 3

LEFT = 35
TOP = 35

PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0",
]

with DATA.open("r", encoding="utf-8") as file:
    data = json.load(file)

days = data["days"]

days = sorted(days, key=lambda x: x["date"])

if len(days) > 371:
    days = days[-371:]

while days and datetime.strptime(
    days[0]["date"], "%Y-%m-%d"
).weekday() != 6:
    days.pop(0)

weeks = []

for i in range(0, len(days), 7):
    week = days[i:i + 7]

    if len(week) == 7:
        weeks.append(week)

width = LEFT + len(weeks) * (CELL + GAP) + 20
height = TOP + 7 * (CELL + GAP) + 60

svg = [
    f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="{width}"
    height="{height}"
    viewBox="0 0 {width} {height}">''',

    """
    <style>

        .cell {
            opacity: 0;
            animation: reveal 0.45s ease-out forwards;
        }

        @keyframes reveal {
            from {
                opacity: 0;
                transform: translateY(-8px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .terminal {
            font-family: "Courier New", monospace;
        }

    </style>
    """,

    f'<rect width="100%" height="100%" rx="12" fill="#0d1117"/>',

    '''
    <text
        x="20"
        y="22"
        fill="#58a6ff"
        class="terminal"
        font-size="11">
        jayanithyan@github ~ $ contributions
    </text>
    '''
]

for week_index, week in enumerate(weeks):

    for day_index, day in enumerate(week):

        level = max(
            0,
            min(5, int(day.get("level", 0)))
        )

        x = LEFT + week_index * (CELL + GAP)
        y = TOP + day_index * (CELL + GAP)

        delay = (
            week_index * 0.025
            + day_index * 0.01
        )

        svg.append(
            f'''
            <rect
                class="cell"
                x="{x}"
                y="{y}"
                width="{CELL}"
                height="{CELL}"
                rx="{RADIUS}"
                fill="{PALETTE[level]}"
                style="animation-delay:{delay:.3f}s">
            </rect>
            '''
        )


svg.append(
    '''
    <text
        x="35"
        y="145"
        fill="#8b949e"
        class="terminal"
        font-size="9">
        Less
    </text>
    '''
)

legend_x = 65

for level, color in enumerate(PALETTE):

    svg.append(
        f'''
        <rect
            x="{legend_x + level * 16}"
            y="136"
            width="11"
            height="11"
            rx="2"
            fill="{color}">
        </rect>
        '''
    )

svg.append(
    f'''
    <text
        x="{legend_x + len(PALETTE) * 16 + 5}"
        y="145"
        fill="#8b949e"
        class="terminal"
        font-size="9">
        More
    </text>
    '''
)

total = sum(
    int(day.get("count", 0))
    for day in days
)

svg.append(
    f'''
    <text
        x="20"
        y="{height - 12}"
        fill="#8b949e"
        class="terminal"
        font-size="10">
        {total:,} contributions
    </text>
    '''
)

svg.append("</svg>")

OUTPUT.write_text(
    "\n".join(svg),
    encoding="utf-8"
)

print(f"Created: {OUTPUT}")