#!/usr/bin/env python3
"""Write small, dependency-free task icons for the documentation site."""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets/tasks"
OUT.mkdir(parents=True, exist_ok=True)

STROKE = "#16877e"
FILL = "#e3f2ef"
INK = "#25364a"
ACCENT = "#b7791f"
SECOND = "#385e85"
GRID = "#cbd7db"

def svg(body: str) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 110" '
        'role="img" aria-hidden="true">\n'
        f'  <g fill="none" stroke-linecap="round" stroke-linejoin="round">\n{body}\n  </g>\n</svg>\n'
    )

icons = {}

icons["point_mass"] = svg(f'''
    <line x1="20" y1="92" x2="146" y2="92" stroke="{GRID}" stroke-width="1.5"/>
    <line x1="20" y1="92" x2="20" y2="14" stroke="{GRID}" stroke-width="1.5"/>
    <circle cx="118" cy="34" r="9" fill="{FILL}" stroke="{STROKE}" stroke-width="2.2"/>
    <path d="M110 41 C86 58 62 72 48 82" stroke="{STROKE}" stroke-width="2" stroke-dasharray="4 4"/>
    <circle cx="40" cy="86" r="6" stroke="{ACCENT}" stroke-width="2.2"/>
    <path d="M40 74 v-7 M28 86 h-7 M40 98 v7 M52 86 h7" stroke="{ACCENT}" stroke-width="2"/>
''')

icons["pendulum"] = svg(f'''
    <line x1="34" y1="22" x2="126" y2="22" stroke="{GRID}" stroke-width="3"/>
    <circle cx="80" cy="22" r="4" fill="{STROKE}" stroke="{STROKE}" stroke-width="2"/>
    <line x1="80" y1="22" x2="112" y2="76" stroke="{STROKE}" stroke-width="2.6"/>
    <circle cx="112" cy="76" r="11" fill="{FILL}" stroke="{STROKE}" stroke-width="2.4"/>
    <path d="M80 40 A36 36 0 0 1 103 54" stroke="{SECOND}" stroke-width="2" stroke-dasharray="4 4"/>
    <path d="M112 76 v18" stroke="{ACCENT}" stroke-width="2"/>
''')

icons["cartpole"] = svg(f'''
    <line x1="18" y1="88" x2="146" y2="88" stroke="{GRID}" stroke-width="2"/>
    <rect x="56" y="68" width="48" height="18" rx="3" fill="{FILL}" stroke="{STROKE}" stroke-width="2.2"/>
    <circle cx="66" cy="90" r="5" stroke="{STROKE}" stroke-width="2"/>
    <circle cx="94" cy="90" r="5" stroke="{STROKE}" stroke-width="2"/>
    <line x1="80" y1="68" x2="108" y2="28" stroke="{STROKE}" stroke-width="2.6"/>
    <circle cx="108" cy="28" r="6" fill="{FILL}" stroke="{STROKE}" stroke-width="2.2"/>
    <path d="M80 52 A24 24 0 0 1 94 48" stroke="{SECOND}" stroke-width="2" stroke-dasharray="4 4"/>
''')

icons["two_link"] = svg(f'''
    <line x1="24" y1="92" x2="140" y2="92" stroke="{GRID}" stroke-width="2"/>
    <circle cx="40" cy="84" r="6" fill="{FILL}" stroke="{STROKE}" stroke-width="2.2"/>
    <line x1="40" y1="84" x2="76" y2="56" stroke="{STROKE}" stroke-width="4"/>
    <circle cx="76" cy="56" r="6" fill="{FILL}" stroke="{STROKE}" stroke-width="2.2"/>
    <line x1="76" y1="56" x2="116" y2="36" stroke="{STROKE}" stroke-width="4"/>
    <circle cx="116" cy="36" r="6" fill="{FILL}" stroke="{STROKE}" stroke-width="2.2"/>
    <path d="M132 26 v20 M122 36 h20" stroke="{ACCENT}" stroke-width="2"/>
''')

icons["multirotor"] = svg(f'''
    <line x1="48" y1="48" x2="112" y2="72" stroke="{STROKE}" stroke-width="3"/>
    <line x1="48" y1="72" x2="112" y2="48" stroke="{STROKE}" stroke-width="3"/>
    <circle cx="80" cy="60" r="9" fill="{FILL}" stroke="{STROKE}" stroke-width="2.4"/>
    <circle cx="48" cy="48" r="9" stroke="{STROKE}" stroke-width="2.2"/>
    <circle cx="112" cy="48" r="9" stroke="{STROKE}" stroke-width="2.2"/>
    <circle cx="48" cy="72" r="9" stroke="{STROKE}" stroke-width="2.2"/>
    <circle cx="112" cy="72" r="9" stroke="{STROKE}" stroke-width="2.2"/>
    <path d="M48 34 v-7 M112 34 v-7 M48 86 v7 M112 86 v7" stroke="{ACCENT}" stroke-width="2"/>
''')

icons["push_disk"] = svg(f'''
    <line x1="18" y1="84" x2="146" y2="84" stroke="{GRID}" stroke-width="2"/>
    <circle cx="104" cy="60" r="15" fill="{FILL}" stroke="{STROKE}" stroke-width="2.4"/>
    <rect x="46" y="48" width="18" height="24" rx="3" fill="{FILL}" stroke="{STROKE}" stroke-width="2.2"/>
    <path d="M64 60 h20" stroke="{SECOND}" stroke-width="2.4"/>
    <path d="M80 60 l-6 -4 v8 z" fill="{SECOND}" stroke="{SECOND}" stroke-width="1.5"/>
    <path d="M40 24 h50" stroke="{ACCENT}" stroke-width="2" stroke-dasharray="4 4"/>
    <path d="M90 24 l-5 -4 v8 z" fill="{ACCENT}" stroke="{ACCENT}" stroke-width="1.5"/>
''')

icons["grid"] = svg(f'''
    <g stroke="{GRID}" stroke-width="1.2">
      {''.join(f'<rect x="{40 + c*15}" y="{12 + r*15}" width="14" height="14" rx="2"/>' for r in range(5) for c in range(5))}
    </g>
    <rect x="40" y="12" width="14" height="14" rx="2" fill="{STROKE}" stroke="{STROKE}" stroke-width="1.2"/>
    <rect x="85" y="72" width="14" height="14" rx="2" fill="{ACCENT}" stroke="{ACCENT}" stroke-width="1.2"/>
    <rect x="100" y="42" width="14" height="14" rx="2" fill="{SECOND}" stroke="{SECOND}" stroke-width="1.2"/>
    <circle cx="70" cy="57" r="4.5" fill="#ffffff" stroke="{INK}" stroke-width="2"/>
''')

icons["rgb_camera"] = svg(f'''
    <rect x="26" y="34" width="42" height="30" rx="4" fill="{FILL}" stroke="{STROKE}" stroke-width="2.2"/>
    <circle cx="47" cy="49" r="9" stroke="{STROKE}" stroke-width="2.2"/>
    <path d="M68 40 L130 24 M68 58 L130 84" stroke="{SECOND}" stroke-width="1.8" stroke-dasharray="4 4"/>
    <rect x="130" y="24" width="22" height="60" rx="3" stroke="{STROKE}" stroke-width="2"/>
    <path d="M130 44 h22 M130 64 h22 M136 24 v60" stroke="{GRID}" stroke-width="1.5"/>
''')

icons["observer"] = svg(f'''
    <path d="M28 55 C46 30 78 30 96 55 C78 80 46 80 28 55 Z" fill="{FILL}" stroke="{STROKE}" stroke-width="2.2"/>
    <circle cx="62" cy="55" r="10" stroke="{STROKE}" stroke-width="2.2"/>
    <circle cx="62" cy="55" r="3.5" fill="{STROKE}" stroke="{STROKE}"/>
    <path d="M104 55 h16 v-22 h24 v44 h-24 v-22" stroke="{SECOND}" stroke-width="2"/>
    <path d="M104 46 v18" stroke="{ACCENT}" stroke-width="2"/>
''')

icons["so101"] = svg(f'''
    <line x1="24" y1="92" x2="140" y2="92" stroke="{GRID}" stroke-width="2"/>
    <rect x="34" y="80" width="30" height="10" rx="3" fill="{FILL}" stroke="{STROKE}" stroke-width="2"/>
    <line x1="50" y1="80" x2="72" y2="52" stroke="{STROKE}" stroke-width="5"/>
    <circle cx="72" cy="52" r="5" fill="{FILL}" stroke="{STROKE}" stroke-width="2"/>
    <line x1="72" y1="52" x2="106" y2="30" stroke="{STROKE}" stroke-width="5"/>
    <circle cx="106" cy="30" r="5" fill="{FILL}" stroke="{STROKE}" stroke-width="2"/>
    <path d="M106 30 l14 -6 M106 30 l14 6" stroke="{STROKE}" stroke-width="2.6"/>
    <path d="M120 24 v12" stroke="{ACCENT}" stroke-width="2"/>
''')

for name, content in icons.items():
    (OUT / f"{name}.svg").write_text(content, encoding="utf-8")
print("wrote", len(icons), "icons to", OUT)
