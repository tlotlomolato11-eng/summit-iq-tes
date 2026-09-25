"""Exam-style biology diagrams for Lekopanye's worksheet.

Clean black-line textbook style: thin outlines, flat colour only (no gradients,
shading or shadows), white background, clear labels.

    python3 build_diagrams.py        # writes svg/*.svg
Then render PNGs with render_png.sh.
"""
import math
from pathlib import Path

OUT = Path(__file__).parent / "svg"
OUT.mkdir(exist_ok=True)

FONT = "Arial, 'Liberation Sans', Helvetica, sans-serif"
INK = "#111"
GREEN = "#5aa84f"
DARKGREEN = "#2f7a33"
YELLOW = "#f1df72"
WATER = "#e3f1fa"


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
            f'<rect width="{w}" height="{h}" fill="#fff"/>\n'
            f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>\n'
            f'<g font-family="{FONT}" font-size="17" fill="{INK}">\n{body}\n</g>\n</svg>\n')


def text(x, y, s, anchor="start", size=None, weight=None, style=None):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    if size: a += f' font-size="{size}"'
    if weight: a += f' font-weight="{weight}"'
    if style: a += f' font-style="{style}"'
    return f'<text x="{x}" y="{y}"{a}>{s}</text>'


def line(x1, y1, x2, y2, w=1.3, extra=""):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" stroke-width="{w}"{extra}/>'


def label(px, py, lx, ly, s, anchor="start", dot=True, size=17):
    """Label text at (lx,ly) with a leader line to the point (px,py) on the drawing.

    The leader starts at whichever end of the text faces the point, so it never runs through the words."""
    w = len(s) * size * 0.56  # rough Arial advance width
    if anchor == "start":
        ex = lx + w + 4 if px > lx + w else lx - 4
    else:
        ex = lx - w - 4 if px < lx - w else lx + 4
    out = line(px, py, ex, ly - size * .32, 1.2)
    if dot: out += f'<circle cx="{px}" cy="{py}" r="2.2" fill="{INK}"/>'
    return out + text(lx, ly, s, anchor)


def tube(d, fill, width, outline=1.6):
    """Outlined tube along a path: black stroke underneath, colour on top."""
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{width + 2 * outline}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{fill}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')


def write(name, content):
    (OUT / name).write_text(content)
    print("wrote", name)


# ---------------------------------------------------------------- 3.3(d)
def graph_photosynthesis():
    ox, oy, xe, yt = 100, 360, 580, 40
    b = [line(ox, oy, xe, oy, 2), line(ox, oy, ox, yt, 2)]
    b.append(f'<path d="M{ox},{oy} C{ox + 70},{oy - 190} {ox + 150},{yt + 68} {ox + 250},{yt + 60} L{xe - 20},{yt + 60}" fill="none" stroke="{INK}" stroke-width="2.6"/>')
    b.append(text((ox + xe) / 2, oy + 36, "Light intensity", "middle"))
    b.append(f'<line x1="{(ox + xe) / 2 - 80}" y1="{oy + 56}" x2="{(ox + xe) / 2 + 80}" y2="{oy + 56}" stroke="{INK}" stroke-width="1.6" marker-end="url(#ah)"/>')
    b.append(f'<text x="{ox - 22}" y="{(oy + yt) / 2}" text-anchor="middle" transform="rotate(-90 {ox - 22} {(oy + yt) / 2})">Rate of photosynthesis</text>')
    write("3-3d_photosynthesis_graph.svg", svg(640, 440, "\n".join(b)))


# ---------------------------------------------------------------- 3.4(a)
def leaf_path(L=260, W=150):
    h = L / 2
    return f"M0,{-h} C{W * .47},{-h * .7} {W * .55},{h * .3} 0,{h} C{-W * .55},{h * .3} {-W * .47},{-h * .7} 0,{-h} Z"


def leaf_veins(L=260, W=150, colour=GREEN, width=9):
    h = L / 2
    out = [f'<path d="M0,{-h + 8} L0,{h + 40}" stroke="{colour}" stroke-width="{width}" stroke-linecap="round"/>']
    for y in range(-80, 100, 30):
        # half-width of the blade at this height, scaled in so veins stay inside the margin
        t = (y + h) / L
        half = W * .5 * math.sin(math.pi * t ** .8) * .78
        for s in (-1, 1):
            out.append(f'<path d="M0,{y} Q{s * half * .5},{y - 16} {s * half},{y - 40}" fill="none" stroke="{colour}" stroke-width="{width * .6}" stroke-linecap="round"/>')
    return "".join(out)


def deficiency():
    b = []
    # Leaf A: pale yellow blade, veins (with a narrow green band) stay green: interveinal chlorosis
    b.append('<g transform="translate(200,230)">')
    b.append(f'<clipPath id="blade"><path d="{leaf_path()}"/></clipPath>')
    b.append(f'<path d="{leaf_path()}" fill="{YELLOW}" stroke="none"/>')
    b.append(f'<g clip-path="url(#blade)">{leaf_veins(colour=GREEN, width=12)}{leaf_veins(colour=DARKGREEN, width=3)}</g>')
    b.append(f'<path d="M0,130 L0,175" stroke="{GREEN}" stroke-width="7"/>')
    b.append(f'<path d="{leaf_path()}" fill="none" stroke="{INK}" stroke-width="1.8"/>')
    b.append(line(0, 130, 0, 175, 2.2))
    b.append('</g>')
    b.append(text(200, 440, "Leaf A", "middle", weight="bold"))
    # Plant B: older, lower leaves uniformly pale yellow; young upper leaves green
    px, base = 590, 390
    b.append(f'<path d="M{px - 120},{base} L{px + 120},{base}" stroke="{INK}" stroke-width="2"/>')
    b.append(f'<path d="M{px},{base} L{px},{base - 300}" stroke="{DARKGREEN}" stroke-width="7" stroke-linecap="round"/>')
    leaves = [(base - 50, 150, YELLOW, 0), (base - 110, 130, YELLOW, 1), (base - 170, 108, GREEN, 0), (base - 230, 82, GREEN, 1), (base - 280, 56, GREEN, 0)]
    for y, size, col, flip in leaves:
        for s in (-1, 1):
            ang = s * (62 - (base - y) / 12)
            sc = size / 260
            b.append(f'<g transform="translate({px + s * 5},{y}) rotate({ang}) translate(0,{-size / 2 - 4}) scale({sc * 1.0},{sc})">'
                     f'<path d="{leaf_path()}" fill="{col}" stroke="{INK}" stroke-width="{1.8 / sc}"/>'
                     f'<path d="M0,-118 L0,130" stroke="{INK}" stroke-width="{1.2 / sc}" opacity=".55"/></g>')
    b.append(f'<path d="M{px - 3},{base} L{px - 3},{base - 300} M{px + 3},{base} L{px + 3},{base - 300}" stroke="{INK}" stroke-width="1.2"/>')
    b.append(f'<path d="M{px},{base} l-18,24 M{px},{base} l14,28 M{px},{base} l2,30" stroke="{INK}" stroke-width="1.4" fill="none"/>')
    b.append(text(px, 440, "Leaf B", "middle", weight="bold"))
    write("3-4a_deficiency_comparison.svg", svg(800, 470, "\n".join(b)))


# ---------------------------------------------------------------- 3.4(b)/(c)
def jar(cx, top, letter, caption_lines):
    w, h = 160, 250
    x0, x1, y1 = cx - w / 2, cx + w / 2, top + h
    liquid = top + 40
    b = [f'<path d="M{x0},{liquid} L{x0},{y1 - 16} Q{x0},{y1} {x0 + 16},{y1} L{x1 - 16},{y1} Q{x1},{y1} {x1},{y1 - 16} L{x1},{liquid} Z" fill="{WATER}"/>',
         f'<path d="M{x0},{top} L{x0},{y1 - 16} Q{x0},{y1} {x0 + 16},{y1} L{x1 - 16},{y1} Q{x1},{y1} {x1},{y1 - 16} L{x1},{top}" fill="none" stroke="{INK}" stroke-width="2"/>',
         line(x0, liquid, x1, liquid, 1.2)]
    # perforated lid: a bar with gaps (holes), seedling through the centre hole
    lid_y = top - 12
    for a, c in ((x0 - 8, cx - 44), (cx - 32, cx - 8), (cx + 8, cx + 32), (cx + 44, x1 + 8)):
        b.append(f'<rect x="{a}" y="{lid_y}" width="{c - a}" height="12" fill="#c9c9c9" stroke="{INK}" stroke-width="1.4"/>')
    # roots in the solution
    r = [f'M{cx},{top} L{cx},{top + 150}', f'M{cx},{top + 40} Q{cx - 20},{top + 70} {cx - 34},{top + 120}',
         f'M{cx},{top + 50} Q{cx + 22},{top + 80} {cx + 36},{top + 130}', f'M{cx},{top + 90} Q{cx - 14},{top + 120} {cx - 18},{top + 165}',
         f'M{cx},{top + 100} Q{cx + 16},{top + 130} {cx + 20},{top + 170}', f'M{cx - 20},{top + 78} l-18,18', f'M{cx + 22},{top + 90} l18,16']
    b += [f'<path d="{d}" fill="none" stroke="#8a6d3b" stroke-width="2" stroke-linecap="round"/>' for d in r]
    # shoot and leaves
    b.append(f'<path d="M{cx},{lid_y} L{cx},{lid_y - 110}" stroke="{DARKGREEN}" stroke-width="5" stroke-linecap="round"/>')
    for y, s, size in ((lid_y - 50, -1, 70), (lid_y - 50, 1, 70), (lid_y - 100, -1, 52), (lid_y - 100, 1, 52)):
        sc = size / 260
        b.append(f'<g transform="translate({cx},{y}) rotate({s * 58}) translate(0,{-size / 2}) scale({sc})"><path d="{leaf_path()}" fill="{GREEN}" stroke="{INK}" stroke-width="{1.6 / sc}"/></g>')
    b.append(text(cx, top - 150, letter, "middle", size=20, weight="bold"))
    for i, cap in enumerate(caption_lines):
        b.append(text(cx, y1 + 30 + i * 21, cap, "middle"))
    return "\n".join(b), (x0, lid_y, top, liquid, cx)


def hydroponics():
    top = 190
    a, (ax0, alid, atop, aliq, acx) = jar(210, top, "A", ["Complete", "nutrient solution"])
    bb, _ = jar(590, top, "B", ["Nutrient solution —", "nitrate omitted"])
    lab = [label(acx + 44, alid + 6, 350, alid - 30, "perforated lid"),
           label(acx + 30, top + 118, 350, top + 110, "roots"),
           label(acx + 60, aliq + 130, 350, aliq + 160, "nutrient solution"),
           # "glass jar" sits left of jar A, text to the left of its leader line
           line(ax0, top + 60, 72, top + 34, 1.2) + f'<circle cx="{ax0}" cy="{top + 60}" r="2.2" fill="{INK}"/>' + text(66, top + 30, "glass jar", "end")]
    write("3-4bc_investigation_setup.svg", svg(800, 520, "\n".join([a, bb] + lab)))


# ---------------------------------------------------------------- 3.6(b)/(c) enzyme panels
ENZ = "#cfe0f3"
SUB = "#f5c38b"


def enzyme(notch):
    n = " ".join(f"L{x},{y}" for x, y in notch)
    x0, y0 = notch[0]
    xn, yn = notch[-1]
    return (f'<path d="M{x0},{y0} {n} C{xn + 60},{yn - 12} {xn + 82},{yn + 50} {xn + 66},{yn + 90} '
            f'C{xn + 50},{yn + 136} {x0 - 50},{y0 + 136} {x0 - 66},{y0 + 90} C{x0 - 82},{y0 + 50} {x0 - 60},{y0 - 12} {x0},{y0} Z" '
            f'fill="{ENZ}" stroke="{INK}" stroke-width="2"/>')


FIT = [(-30, -60), (-15, -26), (15, -26), (30, -60)]
BENT = [(-34, -60), (-20, -52), (-4, -34), (6, -48), (22, -40), (36, -58)]
SUB_PATH = "M-30,0 L-15,34 L15,34 L30,0 C28,-26 -28,-26 -30,0 Z"


def substrate(x, y, rot=0):
    return f'<path d="{SUB_PATH}" transform="translate({x},{y}) rotate({rot})" fill="{SUB}" stroke="{INK}" stroke-width="2"/>'


def motion(x, y, length, n=3, gap=9):
    return "".join(line(x - length, y + (i - (n - 1) / 2) * gap, x, y + (i - (n - 1) / 2) * gap, 1.6) for i in range(n))


def enzyme_panels():
    W = 320
    b = []
    heads = ["Low temperature (5 °C)", "Optimum (35 °C)", "Denatured (80 °C)"]
    for i, h in enumerate(heads):
        x = i * W
        if i: b.append(line(x, 20, x, 360, 1, ' stroke-dasharray="5 5"'))
        b.append(text(x + W / 2, 42, h, "middle", weight="bold"))
    # panel 1: slow substrate nearby, short motion lines
    b.append(f'<g transform="translate(150,230)">{enzyme(FIT)}</g>')
    b.append(substrate(250, 110, 12) + motion(212, 112, 18))
    b.append(label(150, 184, 20, 120, "active site"))
    b.append(label(244, 96, 140, 76, "substrate"))
    b.append(label(96, 262, 20, 332, "enzyme"))
    # panel 2: substrate fits the active site; a second substrate approaches fast
    x = W
    b.append(f'<g transform="translate({x + 150},230)">{enzyme(FIT)}{substrate(0, -60, 0)}</g>')
    b.append(substrate(x + 262, 96, 8) + motion(x + 224, 100, 50))
    b.append(label(x + 146, 156, x + 20, 110, "substrate"))
    b.append(label(x + 178, 190, x + 212, 158, "active site"))
    b.append(text(x + 150, 340, "substrate fits: lock and key", "middle", size=15, style="italic"))
    # panel 3: active site changed shape, substrate cannot fit, no motion
    x = 2 * W
    b.append(f'<g transform="translate({x + 150},230)">{enzyme(BENT)}</g>')
    b.append(substrate(x + 184, 100, 0))
    b.append(label(x + 126, 176, x + 124, 128, "active site", anchor="end"))
    b.append(text(x + 124, 148, "(shape changed)", "end", size=14))
    b.append(label(x + 206, 110, x + 228, 80, "substrate"))
    b.append(text(x + 150, 340, "substrate cannot fit", "middle", size=15, style="italic"))
    write("3-6bc_enzyme_active_site.svg", svg(3 * W + 20, 370, "\n".join(b)))


# ---------------------------------------------------------------- 3.6(b) water baths
def thermometer(x, top, bottom, level):
    return (f'<rect x="{x - 5}" y="{top}" width="10" height="{bottom - top}" rx="5" fill="#fff" stroke="{INK}" stroke-width="1.6"/>'
            f'<rect x="{x - 2}" y="{level}" width="4" height="{bottom - level}" fill="#d9483b"/>'
            f'<circle cx="{x}" cy="{bottom + 4}" r="8" fill="#d9483b" stroke="{INK}" stroke-width="1.6"/>')


def water_baths():
    b = []
    cfg = [("Ice bath (5 °C)", "#d6ecf8", False, None), ("Water bath (35 °C)", "#e6f2f9", True, 205), ("Water bath (80 °C)", "#e6f2f9", True, 150)]
    for i, (cap, water, therm, lvl) in enumerate(cfg):
        cx = 150 + i * 300
        x0, x1, top, bot, wl = cx - 110, cx + 110, 160, 380, 200
        b.append(f'<rect x="{x0}" y="{wl}" width="{x1 - x0}" height="{bot - wl}" fill="{water}"/>')
        b.append(f'<path d="M{x0},{top} L{x0},{bot} L{x1},{bot} L{x1},{top}" fill="none" stroke="{INK}" stroke-width="2.2"/>')
        b.append(line(x0, wl, x1, wl, 1.2))
        # test tube with pale starch–amylase mixture
        tx = cx - 24
        b.append(f'<path d="M{tx - 16},{wl + 60} L{tx - 16},{330} A16,16 0 0 0 {tx + 16},{330} L{tx + 16},{wl + 60} Z" fill="#f3ead0"/>')
        b.append(f'<path d="M{tx - 16},{100} L{tx - 16},{330} A16,16 0 0 0 {tx + 16},{330} L{tx + 16},{100}" fill="none" stroke="{INK}" stroke-width="1.8"/>')
        b.append(line(tx - 16, wl + 60, tx + 16, wl + 60, 1.2))
        if i == 0:
            for (ix, iy) in ((x1 - 58, wl + 10), (x1 - 46, wl + 66), (cx + 14, wl + 124), (x0 + 12, wl + 134), (x1 - 60, wl + 128)):
                b.append(f'<rect x="{ix}" y="{iy}" width="30" height="26" fill="#fff" stroke="{INK}" stroke-width="1.4" transform="rotate(12 {ix + 15} {iy + 13})"/>')
        if therm:
            b.append(thermometer(cx + 48, 90, 340, lvl))
        if i == 2:
            for sx in (x0 + 22, cx + 12, cx + 84):
                b.append(f'<path d="M{sx},{top - 14} q-10,-16 0,-32 q10,-16 0,-32" fill="none" stroke="#9aa3ad" stroke-width="1.6"/>')
        b.append(text(cx, 418, cap, "middle"))
    b.append(label(110, 290, 20, 60, "starch–amylase mixture"))
    write("3-6b_water_baths.svg", svg(900, 440, "\n".join(b)))


# ---------------------------------------------------------------- 3.7 food tests
def food_tests():
    b = []
    rack_y, rack_x0, rack_x1 = 150, 60, 800
    tubes = [("Iodine test", "#1f2346", None, None), ("Biuret test", "#b48ad8", None, None),
             ("Benedict's test", "#e2743d", "#9b3316", None), ("Emulsion test", "#eaf4fa", None, "#ececec")]
    body = []
    for i, (cap, col, ppt, layer) in enumerate(tubes):
        cx = 150 + i * 190
        top, bottom, r = 100, 330, 20
        liq = 190
        body.append(f'<path d="M{cx - r},{liq} L{cx - r},{bottom} A{r},{r} 0 0 0 {cx + r},{bottom} L{cx + r},{liq} Z" fill="{col}"/>')
        if ppt:
            body.append(f'<path d="M{cx - r},{bottom - 6} A{r},{r} 0 0 0 {cx + r},{bottom - 6} L{cx + r},{bottom} A{r},{r} 0 0 1 {cx - r},{bottom} Z" fill="{ppt}"/>')
            body.append(f'<path d="M{cx - r},{bottom - 2} L{cx - r},{bottom} A{r},{r} 0 0 0 {cx + r},{bottom} L{cx + r},{bottom - 2}" fill="{ppt}"/>')
        if layer:
            body.append(f'<rect x="{cx - r}" y="{liq}" width="{2 * r}" height="34" fill="{layer}"/>')
            for dx, dy in ((-10, 8), (4, 14), (12, 6), (-4, 24), (9, 26), (-13, 20)):
                body.append(f'<circle cx="{cx + dx}" cy="{liq + dy}" r="2" fill="#bdbdbd"/>')
            body.append(line(cx - r, liq + 34, cx + r, liq + 34, 1, ' stroke-dasharray="3 3"'))
        body.append(line(cx - r, liq, cx + r, liq, 1.2))
        body.append(f'<path d="M{cx - r},{top} L{cx - r},{bottom} A{r},{r} 0 0 0 {cx + r},{bottom} L{cx + r},{top}" fill="none" stroke="{INK}" stroke-width="1.8"/>')
        body.append(f'<ellipse cx="{cx}" cy="{top}" rx="{r + 3}" ry="4" fill="#fff" stroke="{INK}" stroke-width="1.6"/>')
        body.append(text(cx, 400, f"{i + 1}", "middle", weight="bold"))
        body.append(text(cx, 424, cap, "middle"))
    # test-tube rack: a top bar the tubes pass through, uprights and a base
    rack = [f'<rect x="{rack_x0}" y="{rack_y}" width="{rack_x1 - rack_x0}" height="16" fill="#e2c9a0" stroke="{INK}" stroke-width="1.6"/>',
            f'<rect x="{rack_x0}" y="360" width="{rack_x1 - rack_x0}" height="14" fill="#e2c9a0" stroke="{INK}" stroke-width="1.6"/>',
            f'<rect x="{rack_x0}" y="{rack_y}" width="14" height="{360 - rack_y}" fill="#e2c9a0" stroke="{INK}" stroke-width="1.6"/>',
            f'<rect x="{rack_x1 - 14}" y="{rack_y}" width="14" height="{360 - rack_y}" fill="#e2c9a0" stroke="{INK}" stroke-width="1.6"/>']
    b = rack[1:] + body + [rack[0]]
    # redraw the tube walls over the top bar so the tubes read as passing through it
    for i in range(4):
        cx = 150 + i * 190
        b.append(f'<rect x="{cx - 20}" y="{rack_y}" width="40" height="16" fill="none" stroke="{INK}" stroke-width="1.8"/>')
    b.append(label(720 + 16, 203, 820, 230, "cloudy white"))
    b.append(text(826, 250, "layer"))
    b.append(label(540, 342, 596, 292, "precipitate"))
    write("3-7_food_test_results.svg", svg(940, 440, "\n".join(b)))


# ---------------------------------------------------------------- 3.8 alimentary canal
ORGANS = [  # name, anchor point in body coordinates, side, label y
    ("mouth", (310, 152), "L", 152),
    ("oesophagus", (313, 250), "L", 250),
    ("stomach", (430, 380), "R", 360),
    ("liver", (240, 350), "L", 345),
    ("gall bladder", (272, 410), "L", 420),
    ("pancreas", (420, 470), "R", 455),
    ("small intestine", (350, 590), "R", 610),
    ("large intestine", (412, 540), "R", 535),
    ("rectum", (322, 695), "L", 690),
    ("anus", (320, 744), "R", 750),
]


def canal_body():
    b = []
    # torso outline: head, neck, shoulders, trunk
    b.append(f'<path d="M270,178 C220,160 222,48 310,42 C398,48 400,160 350,178 L352,215 C420,222 470,238 492,262 '
             f'C505,380 500,560 470,770 L150,770 C120,560 115,380 128,262 C150,238 200,222 268,215 Z" fill="#fff" stroke="{INK}" stroke-width="2.2"/>')
    # mouth
    b.append(f'<path d="M292,150 Q310,162 328,150" fill="#e89a9a" stroke="{INK}" stroke-width="1.8"/>')
    # oesophagus
    b.append(tube("M310,160 C312,210 316,280 330,320 C338,338 350,345 366,344", "#e6aaa4", 12))
    # liver (person's right = viewer's left)
    b.append(f'<path d="M180,330 C230,296 330,300 370,338 C352,382 300,398 206,402 C184,396 174,356 180,330 Z" fill="#b8664b" stroke="{INK}" stroke-width="2"/>')
    # gall bladder
    b.append(f'<ellipse cx="274" cy="410" rx="16" ry="11" fill="#86b86b" stroke="{INK}" stroke-width="1.8"/>')
    # pancreas
    b.append(f'<path d="M330,470 C360,452 420,452 452,462 C456,474 420,482 380,482 C352,484 332,482 330,470 Z" fill="#ecc57b" stroke="{INK}" stroke-width="1.8"/>')
    # stomach
    b.append(f'<path d="M362,340 C410,318 468,338 466,400 C464,452 410,468 366,452 C350,446 350,428 364,426 '
             f'C396,428 420,416 420,396 C420,372 394,360 368,366 Z" fill="#ec9f9f" stroke="{INK}" stroke-width="2"/>')
    # small intestine: duodenum from the stomach, then coils in the centre, joining the large intestine low on the left
    si = ("M368,446 C340,462 316,480 300,500 L300,510 "
          "C 330,512 370,512 380,528 C 386,548 340,546 300,548 C 262,552 262,572 300,574 "
          "C 340,576 384,574 384,596 C 384,618 330,614 296,616 C 262,620 262,640 300,642 C 330,644 360,646 360,660 "
          "C 358,676 300,664 262,652")
    b.append(tube(si, "#f3bba3", 12))
    # large intestine: caecum, ascending, transverse, descending, then rectum and anus
    li = "M250,668 L236,660 L236,510 C236,496 246,492 260,492 L400,492 C414,492 420,500 420,512 L420,640 C420,672 380,680 342,684 L326,690"
    b.append(tube(li, "#d99077", 26))
    b.append(tube("M326,690 L322,736", "#d99077", 18))
    b.append(f'<circle cx="321" cy="744" r="4" fill="{INK}"/>')
    return "\n".join(b)


def canal(blank):
    OX = 160  # body drawn at x+OX so labels fit on both sides
    b = [f'<g transform="translate({OX},0)">{canal_body()}</g>']
    for n, (name, (ax, ay), side, ly) in enumerate(ORGANS, 1):
        px = ax + OX
        if side == "L":
            lx = 196
            b.append(line(px, ay, lx, ly, 1.2) + f'<circle cx="{px}" cy="{ay}" r="2.4" fill="{INK}"/>')
            if blank:
                b.append(f'<rect x="{lx - 146}" y="{ly - 14}" width="140" height="28" fill="#fff" stroke="{INK}" stroke-width="1.3"/>')
                b.append(text(lx - 152, ly + 6, f"{n}", "end", weight="bold"))
            else:
                b.append(text(lx - 8, ly + 6, name, "end"))
        else:
            lx = 730
            b.append(line(px, ay, lx, ly, 1.2) + f'<circle cx="{px}" cy="{ay}" r="2.4" fill="{INK}"/>')
            if blank:
                b.append(f'<rect x="{lx + 6}" y="{ly - 14}" width="140" height="28" fill="#fff" stroke="{INK}" stroke-width="1.3"/>')
                b.append(text(lx + 152, ly + 6, f"{n}", weight="bold"))
            else:
                b.append(text(lx + 8, ly + 6, name))
    name = "3-8_alimentary_canal_blank.svg" if blank else "3-8_alimentary_canal_labelled.svg"
    write(name, svg(940, 800, "\n".join(b)))


# ---------------------------------------------------------------- 3.9(d) chewing
FOOD = "#e5b877"


def chewing():
    b = []
    # stage 1: one large piece
    b.append(f'<path d="M60,190 L120,160 L185,172 L210,220 L190,272 L120,286 L66,262 L50,226 Z" fill="{FOOD}" stroke="{INK}" stroke-width="2"/>')
    b.append(text(130, 322, "one large piece", "middle", size=15))
    b.append(f'<line x1="228" y1="224" x2="286" y2="224" stroke="{INK}" stroke-width="2" marker-end="url(#ah)"/>')
    # stage 2: molars crushing the piece
    tooth = "M0,0 L0,58 C0,70 10,72 14,62 L20,50 L26,62 C30,72 40,70 40,58 L40,0 Z"
    for k in range(3):
        x = 300 + k * 46
        b.append(f'<path d="{tooth}" transform="translate({x},98)" fill="#fff" stroke="{INK}" stroke-width="1.8"/>')
        b.append(f'<path d="{tooth}" transform="translate({x},340) scale(1,-1)" fill="#fff" stroke="{INK}" stroke-width="1.8"/>')
    b.append(f'<rect x="292" y="82" width="152" height="16" fill="#f0b2b2" stroke="{INK}" stroke-width="1.6"/>')
    b.append(f'<rect x="292" y="340" width="152" height="16" fill="#f0b2b2" stroke="{INK}" stroke-width="1.6"/>')
    for pts in ("304,212 336,200 350,226 318,240", "352,206 382,198 394,222 366,236", "340,244 372,238 380,262 348,266", "388,236 420,228 432,250 402,262"):
        b.append(f'<polygon points="{pts}" fill="{FOOD}" stroke="{INK}" stroke-width="1.8"/>')
    b.append(f'<line x1="276" y1="112" x2="276" y2="160" stroke="{INK}" stroke-width="1.8" marker-end="url(#ah)"/>')
    b.append(f'<line x1="276" y1="326" x2="276" y2="278" stroke="{INK}" stroke-width="1.8" marker-end="url(#ah)"/>')
    b.append(label(386, 150, 480, 120, "teeth"))
    b.append(f'<line x1="456" y1="224" x2="514" y2="224" stroke="{INK}" stroke-width="2" marker-end="url(#ah)"/>')
    # stage 3: many small pieces coated with saliva droplets
    pieces = [(540, 180), (596, 170), (650, 186), (560, 236), (618, 226), (676, 240), (590, 282), (648, 290), (706, 196)]
    for i, (x, y) in enumerate(pieces):
        b.append(f'<polygon points="{x},{y} {x + 26},{y - 8} {x + 36},{y + 14} {x + 10},{y + 26}" fill="{FOOD}" stroke="{INK}" stroke-width="1.6"/>')
        for dx, dy in ((-4, -6), (34, 4), (14, 30)):
            b.append(f'<circle cx="{x + dx}" cy="{y + dy}" r="4" fill="#bfe0f5" stroke="{INK}" stroke-width="1"/>')
    b.append(text(630, 352, "many small pieces", "middle", size=15))
    b.append(label(710, 200, 760, 150, "saliva"))
    b.append(text(766, 170, "(contains amylase)", size=15))
    # captions
    b.append(text(40, 398, "Mechanical digestion", weight="bold"))
    b.append(text(40, 420, "physical breakdown, increases surface area", size=15))
    b.append(text(520, 398, "Chemical digestion", weight="bold"))
    b.append(text(520, 420, "amylase begins breaking down starch", size=15))
    b.append(line(40, 380, 440, 380, 1) + line(520, 380, 900, 380, 1))
    write("3-9d_mechanical_chemical_digestion.svg", svg(940, 440, "\n".join(b)))


# ---------------------------------------------------------------- 3.10 villus
def villus():
    cx, cy, R, r, bottom = 330, 230, 122, 98, 700
    b = []
    # lumen side colour, then epithelium band, then core
    b.append(f'<path d="M{cx - R},{bottom} L{cx - R},{cy} A{R},{R} 0 0 1 {cx + R},{cy} L{cx + R},{bottom} Z" fill="#f7d9cf" stroke="{INK}" stroke-width="2.2"/>')
    b.append(f'<path d="M{cx - r},{bottom} L{cx - r},{cy} A{r},{r} 0 0 1 {cx + r},{cy} L{cx + r},{bottom} Z" fill="#fdf1ec" stroke="{INK}" stroke-width="1.6"/>')
    # epithelial cell walls: horizontal on the sides, radial on the tip
    cells = []
    for y in range(cy + 20, bottom, 26):
        cells += [line(cx - R, y, cx - r, y, 1), line(cx + r, y, cx + R, y, 1)]
    for a in range(0, 181, 14):
        t = math.radians(a)
        cells.append(line(cx - R * math.cos(t), cy - R * math.sin(t), cx - r * math.cos(t), cy - r * math.sin(t), 1))
    b += cells
    # capillary network: arteriole up the left, loops across, venule down the right
    red, blue = "#d9493f", "#3f6fbf"
    b.append(tube(f"M{cx - 62},{bottom + 30} L{cx - 62},{cy + 10} A62,62 0 0 1 {cx},{cy - 52}", red, 7, 1.2))
    b.append(tube(f"M{cx},{cy - 52} A62,62 0 0 1 {cx + 62},{cy + 10} L{cx + 62},{bottom + 30}", blue, 7, 1.2))
    for y in range(cy + 50, bottom - 30, 70):
        b.append(f'<path d="M{cx - 62},{y} C{cx - 30},{y + 26} {cx + 30},{y - 10} {cx + 62},{y + 18}" fill="none" stroke="#a24a6f" stroke-width="3"/>')
    # lacteal: blind-ended lymph vessel in the centre
    b.append(f'<path d="M{cx - 18},{bottom + 30} L{cx - 18},{cy + 90} A18,18 0 0 1 {cx + 18},{cy + 90} L{cx + 18},{bottom + 30}" fill="#fbf4cf" stroke="{INK}" stroke-width="1.8"/>')
    # absorption arrows
    b.append(f'<line x1="120" y1="430" x2="{cx - 70}" y2="430" stroke="{INK}" stroke-width="1.8" marker-end="url(#ah)"/>')
    b.append(text(40, 402, "glucose and"))
    b.append(text(40, 422, "amino acids"))
    b.append(f'<line x1="560" y1="560" x2="{cx + 24}" y2="560" stroke="{INK}" stroke-width="1.8" marker-end="url(#ah)"/>')
    b.append(text(572, 552, "fatty acids"))
    b.append(text(572, 572, "and glycerol"))
    # labels
    b.append(label(cx + R - 10, cy - 70, 520, 130, "epithelium"))
    b.append(label(cx + 44, cy - 34, 520, 330, "capillary network"))
    b.append(label(cx, 650, 520, 660, "lacteal"))
    b.append(label(cx + 62, bottom + 22, 520, bottom + 40, "vein"))
    b.append(line(cx - 62, bottom + 22, 150, bottom + 34, 1.2) + f'<circle cx="{cx - 62}" cy="{bottom + 22}" r="2.2" fill="{INK}"/>' + text(144, bottom + 40, "artery", "end"))
    write("3-10ab_villus.svg", svg(720, 770, "\n".join(b)))


if __name__ == "__main__":
    graph_photosynthesis()
    deficiency()
    hydroponics()
    enzyme_panels()
    water_baths()
    food_tests()
    canal(blank=True)
    canal(blank=False)
    chewing()
    villus()
