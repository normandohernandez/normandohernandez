"""Contribution graph as a paint-splattered sneaker upper.
Every commit day lands as a splatter (bigger for busier days), in date order.
Usage: gen_splatter.py grid.json out.svg light|dark   (grid: [[week, weekday, level 0-4], ...])"""
import json, sys, math, random
grid = json.load(open(sys.argv[1])); out = sys.argv[2]; mode = sys.argv[3]
TH = {
  "light": dict(bg="#f7f6f2", dot="#dedbd3", paints=["#1d3bff", "#e63b2e", "#f5c518", "#111111", "#7fb2ff", "#1a7f5a"]),
  "dark":  dict(bg="#141416", dot="#2a2a2e", paints=["#5c74ff", "#ff5a4e", "#ffd23f", "#f5f5f2", "#9cc4ff", "#3fbf8a"]),
}[mode]
C = 16; PX, PY = 24, 26
cols = max(x for x, _, _ in grid) + 1
W = PX * 2 + cols * C; H = PY * 2 + 7 * C + 8
def ctr(x, y): return PX + x * C + C / 2, PY + y * C + C / 2

def blob(cx, cy, r, rnd, n=14):
    pts = []
    for i in range(n):
        a = i / n * 2 * math.pi
        rr = r * (0.72 + rnd.random() * 0.5) * (1.5 if rnd.random() < 0.18 else 1)
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d = f"M{(pts[0][0]+pts[-1][0])/2:.1f},{(pts[0][1]+pts[-1][1])/2:.1f}"
    for i in range(n):
        p, q = pts[i], pts[(i + 1) % n]
        d += f" Q{p[0]:.1f},{p[1]:.1f} {(p[0]+q[0])/2:.1f},{(p[1]+q[1])/2:.1f}"
    return d + "Z"

rnd_bg = random.Random(1988)
flecks = "".join(
    f'<circle cx="{rnd_bg.uniform(8, W-8):.1f}" cy="{rnd_bg.uniform(8, H-8):.1f}" r="{rnd_bg.choice([.5,.6,.8,1.1]):.1f}" fill="{rnd_bg.choice(TH["paints"])}" opacity=".35"/>'
    for _ in range(70))
dots = "".join(f'<circle cx="{ctr(x,y)[0]}" cy="{ctr(x,y)[1]}" r="1.2" fill="{TH["dot"]}"/>' for x, y, _ in grid)

commits = sorted((x, y, l) for x, y, l in grid if l > 0)
T = 6.0; splats = []
for i, (x, y, l) in enumerate(commits):
    rnd = random.Random(x * 7 + y)
    cx, cy = ctr(x, y); r = 3.2 + l * 1.6
    col = rnd.choice(TH["paints"]); t = 0.4 + (i / max(1, len(commits) - 1)) * T
    parts = [f'<path d="{blob(cx, cy, r, rnd)}" fill="{col}"/>']
    for _ in range(3 + l * 2):  # satellite droplets
        a = rnd.uniform(0, 2 * math.pi); d = r * rnd.uniform(1.3, 2.8)
        parts.append(f'<circle cx="{cx+math.cos(a)*d:.1f}" cy="{cy+math.sin(a)*d:.1f}" r="{rnd.uniform(.5, 1.2+l*.25):.1f}" fill="{col}"/>')
    if l >= 2:  # a flick trail on busier days
        a = rnd.uniform(0, 2 * math.pi); L = r * rnd.uniform(2.5, 4)
        parts.append(f'<path d="M{cx:.1f},{cy:.1f} q{math.cos(a+.6)*L/2:.1f},{math.sin(a+.6)*L/2:.1f} {math.cos(a)*L:.1f},{math.sin(a)*L:.1f}" stroke="{col}" stroke-width="1.1" fill="none" stroke-linecap="round"/>')
    splats.append(
        f'<g transform="translate({cx:.1f} {cy:.1f})"><g opacity="0" transform="scale(.4)">'
        f'<g transform="translate({-cx:.1f} {-cy:.1f})">{"".join(parts)}</g>'
        f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur=".08s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="scale" values=".4;1.12;1" keyTimes="0;.6;1" begin="{t:.2f}s" dur=".28s" fill="freeze"/>'
        f'</g></g>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<title>Contribution graph as paint splatter: every commit day is a drop of paint</title>
<rect width="{W}" height="{H}" rx="8" fill="{TH["bg"]}"/>{dots}{flecks}{"".join(splats)}</svg>'''
open(out, "w").write(svg)
