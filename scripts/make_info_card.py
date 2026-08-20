from pathlib import Path

OUTPUT = Path("info-card.svg")

lines = [
    ("STATUS", "ONLINE"),
    ("DOMAIN", "AI × DATA × SOFTWARE"),
    ("RUNTIME", "PYTHON / JAVA / C"),
    ("API", "FASTAPI / REST"),
    ("UI", "REACT / HTML / CSS"),
    ("DATA", "SQL / ANALYSIS"),
    ("LOGIC", "DSA / ALGORITHMS"),
    ("AUTOMATION", "AI TOOLS / WORKFLOWS"),
    ("VERSIONING", "GIT / GITHUB"),
    ("MODE", "BUILD → DEBUG → OPTIMIZE"),
]

WIDTH = 490
HEIGHT = 430

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<style>
    .terminal {{
        font-family: "Courier New", monospace;
    }}

    .title {{
        font-size: 18px;
        font-weight: bold;
    }}

    .key {{
        font-size: 12px;
        font-weight: bold;
    }}

    .value {{
        font-size: 12px;
    }}

    .row {{
        opacity: 0;
        animation: boot 0.45s ease-out forwards;
    }}

    @keyframes boot {{
        from {{
            opacity: 0;
            transform: translateX(-12px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}

    .cursor {{
        animation: blink 1s steps(2) infinite;
    }}

    @keyframes blink {{
        50% {{ opacity: 0; }}
    }}
</style>

<rect width="100%" height="100%" rx="12" fill="#0d1117"/>

<rect x="1" y="1"
      width="{WIDTH - 2}"
      height="{HEIGHT - 2}"
      rx="12"
      fill="none"
      stroke="#30363d"/>

<circle cx="20" cy="22" r="5" fill="#ff5f56"/>
<circle cx="38" cy="22" r="5" fill="#ffbd2e"/>
<circle cx="56" cy="22" r="5" fill="#27c93f"/>

<text x="75" y="27"
      fill="#8b949e"
      class="terminal"
      font-size="11">
    jayanithyan@github
</text>

<text x="24" y="68"
      fill="#58a6ff"
      class="terminal title">
    $ whoami
</text>

<text x="24" y="94"
      fill="#f0f6fc"
      class="terminal title">
    jayanithyan
</text>

<text x="24" y="116"
      fill="#8b949e"
      class="terminal"
      font-size="11">
    AI &amp; Data Science
</text>
'''

start_y = 150

for i, (key, value) in enumerate(lines):
    y = start_y + i * 25
    delay = 0.5 + i * 0.12

    svg += f'''
<g class="row"
   style="animation-delay:{delay:.2f}s">

    <text x="24"
          y="{y}"
          fill="#58a6ff"
          class="terminal key">
        {key}
    </text>

    <text x="150"
          y="{y}"
          fill="#8b949e"
          class="terminal">
        :
    </text>

    <text x="165"
          y="{y}"
          fill="#c9d1d9"
          class="terminal value">
        {value}
    </text>

</g>
'''

svg += '''
<text x="24" y="410"
      fill="#58a6ff"
      class="terminal"
      font-size="12">
    $
</text>

<text x="38" y="410"
      fill="#8b949e"
      class="terminal"
      font-size="12">
    build --future
</text>

<text x="135" y="410"
      fill="#58a6ff"
      class="terminal cursor"
      font-size="12">
    █
</text>

</svg>
'''

OUTPUT.write_text(svg, encoding="utf-8")

print(f"Created: {OUTPUT}")