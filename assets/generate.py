"""Generate brand SVGs (light + dark) for the GitHub profile README."""
import os
from html import escape
from PIL import ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))
F = "/System/Library/Fonts/Supplemental/"
_fonts = {}


def width(text, size, face="sans", weight=400, italic=False):
    name = {"sans": "Arial", "serif": "Georgia"}[face]
    style = (" Bold" if weight >= 600 else "") + (" Italic" if italic else "")
    path = F + f"{name}{style}.ttf".replace("Arial Italic", "Arial Italic")
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key].getlength(text)


THEMES = {
    "light": dict(ground="#f5f6f3", ground2="#ebf0ec", surface="#ffffff", ink="#16191d", ink2="#4b535b",
                  ink3="#626b74", line="#dfe4de", accent="#0e7a5a", accent_ink="#ffffff", soft="#dcede4"),
    "dark": dict(ground="#121715", ground2="#18201c", surface="#1b2320", ink="#e9eeeb", ink2="#aeb9b3",
                 ink3="#8f9b95", line="#2a3531", accent="#5ccf9f", accent_ink="#0b1511", soft="#1e3129"),
}

STYLE = """
  <style>
    .serif { font-family: "Source Serif 4", "Iowan Old Style", Georgia, "Times New Roman", serif; }
    .sans  { font-family: "Instrument Sans", -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif; }
    %s
  </style>"""


def svg(w, h, title, body, css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(title)}">\n  <title>{escape(title)}</title>\n  <defs>{STYLE % css}\n'
            f'{body}\n</svg>\n')


def chip(x, y, text, t, size=14, filled=True):
    w = width(text, size) + 28
    h = size + 16
    bg = t["soft"] if filled else t["surface"]
    stroke = "none" if filled else t["line"]
    fg = t["accent"] if filled else t["ink2"]
    return w, (f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{bg}" stroke="{stroke}"/>'
               f'<text x="{x + w/2:.1f}" y="{y + h/2 + size*0.36:.1f}" text-anchor="middle" class="sans" '
               f'font-size="{size}" font-weight="500" fill="{fg}">{escape(text)}</text>')


# ---------- Banner ----------
STAGES = ["Plan", "Foundations", "Architect", "Build", "Test", "Deploy", "Iterate"]


def banner(t):
    W, H = 960, 360
    top, gap, sx = 58, 40, 742
    css = """
    .fill { transform-origin: 0 0; animation: grow 2.8s cubic-bezier(.2,.7,.2,1) .4s backwards; }
    @keyframes grow { from { transform: scaleY(0); } }
    .dot { animation: on .3s ease backwards; }
    .tick { animation: tk .3s ease backwards; }
    @keyframes on { from { fill: %(surface)s; stroke: %(line)s; } }
    @keyframes tk { from { opacity: 0; } }
    .rise { animation: rise .7s cubic-bezier(.2,.7,.2,1) backwards; }
    @keyframes rise { from { opacity: .4; transform: translateY(12px); } }
    @media (prefers-reduced-motion: reduce) { .fill, .dot, .tick, .rise { animation: none; } }
    """ % t
    b = [f'''  <radialGradient id="glow" cx="12%" cy="10%" r="75%">
      <stop offset="0" stop-color="{t["accent"]}" stop-opacity="0.18"/>
      <stop offset="0.6" stop-color="{t["accent"]}" stop-opacity="0.04"/>
      <stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="panel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{t["surface"]}"/><stop offset="1" stop-color="{t["ground2"]}"/>
    </linearGradient>
    <clipPath id="c"><rect width="{W}" height="{H}" rx="20"/></clipPath>
  </defs>
  <g clip-path="url(#c)">
    <rect width="{W}" height="{H}" fill="{t["ground"]}"/>
    <rect width="{W}" height="{H}" fill="url(#glow)"/>
    <circle cx="{W-40}" cy="{H+40}" r="190" fill="{t["accent"]}" opacity="0.07"/>
  </g>
  <rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="19.5" fill="none" stroke="{t["line"]}"/>''']
    # left: identity
    b.append(f'''  <rect x="56" y="52" width="34" height="34" rx="9" fill="{t["ink"]}"/>
  <text x="73" y="75" text-anchor="middle" class="serif" font-size="15" fill="{t["ground"]}">YS</text>
  <text x="104" y="74" class="sans" font-size="13" font-weight="600" letter-spacing="1.3" fill="{t["ink3"]}">YOAV SBOROVSKY · AI ENGINEER</text>
  <g class="rise" style="animation-delay:.05s"><text x="54" y="172" class="serif" font-size="58" letter-spacing="-1.2" fill="{t["ink"]}">I plan AI systems.</text></g>
  <g class="rise" style="animation-delay:.14s"><text x="54" y="236" class="serif" font-size="58" letter-spacing="-1.2" fill="{t["ink"]}">Then I <tspan font-style="italic" fill="{t["accent"]}">ship</tspan> them.</text></g>
  <g class="rise" style="animation-delay:.23s">
    <text x="57" y="286" class="sans" font-size="18" fill="{t["ink2"]}">From idea to production: planned, built,</text>
    <text x="57" y="312" class="sans" font-size="18" fill="{t["ink2"]}">tested, and shipped with care.</text>
  </g>''')
    # right: stage track panel
    px, py, pw, ph = 694, 34, 232, H - 68
    b.append(f'  <rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="18" fill="url(#panel)" stroke="{t["line"]}"/>')
    y0, y1 = top + 8, top + 8 + gap * (len(STAGES) - 1)
    b.append(f'  <rect x="{sx-1.5}" y="{y0}" width="3" height="{y1-y0}" rx="1.5" fill="{t["line"]}"/>')
    b.append(f'  <rect class="fill" x="{sx-1.5}" y="{y0}" width="3" height="{y1-y0}" rx="1.5" fill="{t["accent"]}"/>')
    for i, s in enumerate(STAGES):
        y = y0 + gap * i
        d = 0.4 + 2.8 * i / (len(STAGES) - 1)
        b.append(f'  <circle class="dot" style="animation-delay:{d:.2f}s" cx="{sx}" cy="{y}" r="11" '
                 f'fill="{t["accent"]}" stroke="{t["accent"]}" stroke-width="2"/>')
        b.append(f'  <path class="tick" style="animation-delay:{d:.2f}s" d="M{sx-4.5} {y+.5} l3 3 l6 -6.5" '
                 f'fill="none" stroke="{t["accent_ink"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
        b.append(f'  <text x="{sx+24}" y="{y+5}" class="sans" font-size="15" font-weight="500" fill="{t["ink"]}">{s}</text>')
    return svg(W, H, "Yoav Sborovsky, AI Engineer. I plan AI systems. Then I ship them.", "\n".join(b), css)


# ---------- Project cards ----------
PROJECTS = [
    ("portfolio", "FEATURED · AI-BUILT", "This website", "A portfolio built like a product: planned first, guarded by 7 automatic checks, developed with AI.", ["Astro", "TypeScript", "Claude Code"]),
    ("files-unifier", "CLIENT PROJECT", "Files Unifier", "Spreadsheet in, ready-to-send PDFs out. Sold to a leading law firm and used daily.", ["Python", "Desktop app", "CI/CD"]),
    ("pitch-star", "IOS APP", "Pitch Star", "An iPhone music quiz: guess the year of 800+ FIFA soundtrack songs, with daily challenges.", ["Swift", "SwiftUI", "Firebase"]),
    ("claude-code-tools", "OPEN SOURCE", "Claude Code tools", "The Claude Code skills and automations I use every day, installable with one command.", ["TypeScript", "Node.js", "AI agents"]),
]


def wrap(text, size, maxw):
    lines, cur = [], ""
    for word in text.split():
        cand = (cur + " " + word).strip()
        if width(cand, size) <= maxw:
            cur = cand
        else:
            lines.append(cur)
            cur = word
    return lines + [cur]


def card(t, kicker, title, summary, tags):
    W, H = 460, 236
    b = [f'''  <clipPath id="c"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="20"/></clipPath>
    <radialGradient id="corner"><stop offset="0" stop-color="{t["accent"]}" stop-opacity=".16"/><stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></radialGradient>
  </defs>
  <rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="20" fill="{t["surface"]}" stroke="{t["line"]}"/>
  <g clip-path="url(#c)"><circle cx="{W}" cy="0" r="120" fill="url(#corner)"/>
    <rect x="0" y="0" width="{W}" height="4" fill="{t["accent"]}"/></g>
  <text x="30" y="46" class="sans" font-size="12" font-weight="600" letter-spacing="1.1" fill="{t["accent"]}">{kicker}</text>
  <text x="{W-38}" y="50" class="sans" font-size="22" fill="{t["accent"]}">→</text>
  <text x="29" y="90" class="serif" font-size="30" letter-spacing="-.4" fill="{t["ink"]}">{escape(title)}</text>''']
    for i, line in enumerate(wrap(summary, 15.5, W - 64)):
        b.append(f'  <text x="30" y="{124 + i*23}" class="sans" font-size="15.5" fill="{t["ink2"]}">{escape(line)}</text>')
    x = 30
    for tag in tags:
        w, el = chip(x, H - 58, tag, t, 13)
        b.append("  " + el)
        x += w + 8
    return svg(W, H, f"{title}: {summary}", "\n".join(b))


# ---------- Link buttons ----------
BUTTONS = [
    ("website", "Visit my website  →", True),
    ("linkedin", "LinkedIn", False),
]


def button(t, label, primary):
    size = 15
    w = int(width(label, size, weight=600) + 48)
    h = 44
    bg, fg, stroke = (t["ink"], t["ground"], "none") if primary else (t["surface"], t["ink"], t["line"])
    b = [f'''  </defs>
  <rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{h/2}" fill="{bg}" stroke="{stroke}"/>
  <text x="{w/2}" y="{h/2 + 5.4}" text-anchor="middle" class="sans" font-size="{size}" font-weight="600" fill="{fg}">{escape(label)}</text>''']
    return svg(w, h, label.replace("  →", ""), "\n".join(b))


# ---------- Pipeline (toolkit by stage) ----------
PIPELINE = [
    ("Plan", "", ["Claude Code", "Cursor"]),
    ("Foundations", "", ["Git", "Linux", "Bash"]),
    ("Architect", "", ["REST APIs", "SQL", "Docker"]),
    ("Build", "", ["Python", "TypeScript", "JavaScript", "React", "Flask", "Django"]),
    ("Test", "", ["Playwright", "Pytest", "Vitest"]),
    ("Deploy", "", ["GitHub Actions", "CI/CD", "AWS", "ArgoCD/Kargo"]),
    ("Iterate", "", ["AI agents", "LLM apps"]),
]


def pipeline(t):
    W, n = 960, len(PIPELINE)
    col = W / n
    rail_y, chip_top, chip_h, chip_gap = 26, 100, 30, 8
    rows = max(len(tools) for *_, tools in PIPELINE)
    H = chip_top + rows * (chip_h + chip_gap) + 4
    css = """
    .fill { transform-origin: 0 0; animation: grow 2.6s cubic-bezier(.2,.7,.2,1) .3s backwards; }
    @keyframes grow { from { transform: scaleX(0); } }
    .dot { animation: on .35s ease backwards; }
    @keyframes on { from { fill: %(surface)s; } }
    .num { animation: num .35s ease backwards; }
    @keyframes num { from { fill: %(ink3)s; } }
    .col { animation: rise .6s cubic-bezier(.2,.7,.2,1) backwards; }
    @keyframes rise { from { opacity: 0; transform: translateY(8px); } }
    @media (prefers-reduced-motion: reduce) { .fill, .dot, .num, .col { animation: none; } }
    """ % t
    x0, x1 = col / 2, W - col / 2
    b = ["  </defs>",
         f'  <rect x="{x0}" y="{rail_y-1.5}" width="{x1-x0}" height="3" rx="1.5" fill="{t["line"]}"/>',
         f'  <rect class="fill" x="{x0}" y="{rail_y-1.5}" width="{x1-x0}" height="3" rx="1.5" fill="{t["accent"]}"/>']
    for i, (label, tagline, tools) in enumerate(PIPELINE):
        cx = col * i + col / 2
        d = 0.3 + 2.6 * i / (n - 1)
        b.append(f'  <circle class="dot" style="animation-delay:{d:.2f}s" cx="{cx:.1f}" cy="{rail_y}" r="17" '
                 f'fill="{t["accent"]}" stroke="{t["accent"]}" stroke-width="2"/>')
        b.append(f'  <text class="num sans" style="animation-delay:{d:.2f}s" x="{cx:.1f}" y="{rail_y+4.5}" text-anchor="middle" '
                 f'font-size="12.5" font-weight="700" fill="{t["accent_ink"]}">{i+1:02d}</text>')
        g = [f'<text x="{cx:.1f}" y="{rail_y+54}" text-anchor="middle" class="serif" font-size="20" fill="{t["ink"]}">{label}</text>']
        for j, line in enumerate(wrap(tagline, 12.5, col - 22) if tagline else []):
            g.append(f'<text x="{cx:.1f}" y="{rail_y+76+j*16}" text-anchor="middle" class="sans" font-size="12.5" fill="{t["ink3"]}">{escape(line)}</text>')
        for j, tool in enumerate(tools):
            w = min(width(tool, 13, weight=600) + 26, col - 12)
            y = chip_top + j * (chip_h + chip_gap)
            first = j == 0
            bg, fg, stroke = (t["soft"], t["accent"], "none") if first else (t["surface"], t["ink2"], t["line"])
            g.append(f'<rect x="{cx-w/2:.1f}" y="{y}" width="{w:.1f}" height="{chip_h}" rx="{chip_h/2}" fill="{bg}" stroke="{stroke}"/>'
                     f'<text x="{cx:.1f}" y="{y+chip_h/2+4.6:.1f}" text-anchor="middle" class="sans" font-size="13" font-weight="500" fill="{fg}">{escape(tool)}</text>')
        b.append(f'  <g class="col" style="animation-delay:{d:.2f}s">' + "".join(g) + "</g>")
    alt = "How I work: " + "; ".join(f"{l} ({', '.join(tools)})" for l, _, tools in PIPELINE)
    return svg(W, H, alt, "\n".join(b), css)


if __name__ == "__main__":
    for f in os.listdir(OUT):
        if f.endswith(".svg"):  # regenerate from scratch
            os.remove(os.path.join(OUT, f))
    for name, t in THEMES.items():
        files = {f"banner-{name}.svg": banner(t), f"pipeline-{name}.svg": pipeline(t)}
        for slug, *p in PROJECTS:
            files[f"card-{slug}-{name}.svg"] = card(t, *p)
        for slug, label, primary in BUTTONS:
            files[f"btn-{slug}-{name}.svg"] = button(t, label, primary)
        for fn, s in files.items():
            open(os.path.join(OUT, fn), "w").write(s)
    print(sorted(os.listdir(OUT)))
