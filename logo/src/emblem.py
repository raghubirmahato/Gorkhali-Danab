"""Gorkhali Danab emblem: a Lakhey-style danab (demon) mask crowned with Himalayan peaks,
crescent-moon horns, the flag's sun as a third eye, over crossed Gurkha khukuris."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geom import *

NAVY = "#0A1A3F"
BLUE = "#003893"
BLUE_RAY = "#0A47AD"
CRIMSON = "#DC143C"
CRIMSON_D = "#A60F2D"
CRIMSON_L = "#F23A57"
MAROON = "#6B0A1C"
MAROON_D = "#4A0613"
GOLD = "#FFC233"
GOLD_D = "#E0950B"
GOLD_L = "#FFE08A"
WHITE = "#FFFFFF"
SNOW = "#E6EEFF"
STEEL = "#E9EDF4"
STEEL_D = "#A3AFC4"
HANDLE = "#5B2A12"
IVORY = "#FFF4D6"
MOUTH = "#2A0510"

OUT = 9  # outline width
BADGE_C = (500, 520)


def el(tag, **kw):
    attrs = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items())
    return f"<{tag} {attrs}/>"


def P(d, fill, stroke=NAVY, sw=OUT, **kw):
    if stroke:
        return el("path", d=d, fill=fill, stroke=stroke, stroke_width=sw, stroke_linejoin="round", **kw)
    return el("path", d=d, fill=fill, **kw)


# ================================================================ khukuri
def khukuri_parts():
    """Khukuri in local coords: butt at x=0, tip near x=728, cutting edge toward +y."""
    blade = path((150, -22), [
        ("C", (300, -40), (470, -52), (590, -26)),   # spine
        ("C", (650, -12), (700, 14), (728, 48)),      # drop to the tip
        ("C", (690, 76), (610, 86), (548, 72)),       # belly
        ("C", (450, 52), (360, 26), (270, 20)),       # recurved edge
        ("L", (200, 18)),
        ("L", (192, 32)), ("L", (184, 18)),           # cho notch
        ("L", (150, 22)),
    ])
    bevel = path((270, 20), [
        ("C", (360, 26), (450, 52), (548, 72)),
        ("C", (610, 86), (690, 76), (728, 48)),
        ("C", (680, 54), (610, 60), (550, 50)),
        ("C", (450, 34), (360, 12), (270, 8)),
    ])
    fuller = path((178, -8), [("C", (320, -22), (460, -32), (575, -14))], close=False)
    guard = poly([(130, -36), (160, -31), (160, 31), (130, 36)])
    handle = path((12, -27), [
        ("C", (50, -35), (90, -31), (130, -27)), ("L", (130, 27)),
        ("C", (90, 31), (50, 35), (12, 27)), ("C", (-4, 14), (-4, -14), (12, -27)),
    ])
    rings = " ".join(poly([(x, -32), (x + 9, -32), (x + 9, 32), (x, 32)]) for x in (44, 92))
    cap = path((12, -27), [("C", (-6, -14), (-6, 14), (12, 27)), ("L", (2, 27)),
                           ("C", (-16, 14), (-16, -14), (2, -27))])
    return dict(blade=blade, bevel=bevel, fuller=fuller, guard=guard, handle=handle, rings=rings, cap=cap)


def khukuri(transform, outline_only=False, sw=OUT):
    k = khukuri_parts()
    g = [f'<g transform="{transform}">']
    if outline_only:
        for key in ("blade", "handle", "guard", "cap"):
            g.append(P(k[key], NAVY, sw=sw))
    else:
        g.append(P(k["blade"], STEEL))
        g.append(P(k["bevel"], STEEL_D, stroke=None))
        g.append(P(k["blade"], "none"))
        g.append(el("path", d=k["fuller"], fill="none", stroke=STEEL_D, stroke_width=5, stroke_linecap="round"))
        g.append(P(k["handle"], HANDLE))
        g.append(P(k["rings"], GOLD, sw=5))
        g.append(P(k["cap"], GOLD, sw=6))
        g.append(P(k["guard"], GOLD))
    g.append("</g>")
    return "\n".join(g)


KHUKURI_T = "translate(500,872) rotate(-37) scale(0.9) translate(-226,0)"
KHUKURI_T_M = "translate(1000,0) scale(-1,1) " + KHUKURI_T


# ================================================================ badge
def badge():
    cx, cy = BADGE_C
    out = [el("circle", cx=cx, cy=cy, r=380, fill=NAVY),
           el("circle", cx=cx, cy=cy, r=367, fill=GOLD),
           el("circle", cx=cx, cy=cy, r=352, fill=NAVY),
           el("circle", cx=cx, cy=cy, r=342, fill=BLUE),
           f'<clipPath id="gd-inner"><circle cx="{cx}" cy="{cy}" r="342"/></clipPath>']
    rays = []
    n = 24
    for i in range(0, n, 2):
        a0 = math.radians(i * 360 / n - 90 - 360 / n / 2)
        a1 = math.radians(i * 360 / n - 90 + 360 / n / 2)
        rays.append(poly([(500, 470), (500 + 600 * math.cos(a0), 470 + 600 * math.sin(a0)),
                          (500 + 600 * math.cos(a1), 470 + 600 * math.sin(a1))]))
    out.append('<g clip-path="url(#gd-inner)">' + P(" ".join(rays), BLUE_RAY, stroke=None))
    out.append("</g>")
    return "\n".join(out)


# ================================================================ head
MANE = ((500, 236), [
    ("Q", (600, 218), (664, 262)),
    ("Q", (740, 270), (800, 330)),      # tongue 1
    ("Q", (750, 362), (744, 392)),
    ("Q", (810, 410), (842, 470)),      # tongue 2
    ("Q", (786, 482), (768, 512)),
    ("Q", (826, 560), (830, 628)),      # tongue 3
    ("Q", (782, 614), (744, 630)),
    ("Q", (770, 700), (754, 758)),      # tongue 4
    ("Q", (706, 734), (676, 744)),
    ("Q", (680, 812), (648, 866)),      # tongue 5
    ("Q", (612, 826), (585, 818)),
    ("Q", (560, 860), (500, 888)),      # beard point
])


def mane():
    d = sym(*MANE)
    inner = sym((500, 290), [
        ("Q", (620, 290), (692, 330)),
        ("Q", (712, 380), (752, 440)),
        ("Q", (716, 462), (712, 496)),
        ("Q", (756, 552), (756, 600)),
        ("Q", (716, 600), (702, 622)),
        ("Q", (708, 690), (688, 716)),
        ("Q", (650, 716), (636, 728)),
        ("Q", (622, 790), (596, 812)),
        ("Q", (566, 800), (550, 806)),
        ("Q", (534, 846), (500, 868)),
    ])
    # flame licks on each tongue
    licks = pair((700, 300), [("Q", (740, 300), (772, 330)), ("Q", (735, 325), (712, 330))]) + " " + \
        pair((752, 420), [("Q", (790, 430), (812, 466)), ("Q", (780, 456), (760, 452))]) + " " + \
        pair((770, 540), [("Q", (800, 570), (804, 610)), ("Q", (785, 585), (764, 574))]) + " " + \
        pair((728, 660), [("Q", (744, 690), (738, 730)), ("Q", (726, 700), (712, 690))]) + " " + \
        pair((646, 760), [("Q", (652, 800), (634, 838)), ("Q", (630, 805), (620, 790))])
    return P(d, CRIMSON_D) + P(inner, MAROON, stroke=None) + P(licks, CRIMSON, stroke=None)


HORN = ((662, 334), [
    ("C", (770, 350), (868, 300), (866, 196)),
    ("C", (866, 146), (842, 104), (806, 70)),       # tip
    ("C", (822, 136), (808, 228), (724, 266)),
    ("C", (694, 280), (664, 284), (640, 286)),
])


def horns():
    d = pair(*HORN)
    shade = pair((662, 334), [
        ("C", (770, 350), (868, 300), (866, 196)),
        ("C", (866, 146), (842, 104), (806, 70)),
        ("C", (840, 130), (840, 250), (740, 300)),
        ("C", (712, 314), (690, 318), (662, 318)),
    ])
    ridges = []
    for (a, b) in [((712, 268), (726, 330)), ((758, 244), (786, 316)), ((792, 206), (830, 270)),
                   ((810, 160), (852, 196)), ((815, 116), (846, 132))]:
        ridges.append(path(a, [("L", b)], close=False))
        ridges.append(mirror_path(a, [("L", b)], close=False))
    return (P(d, GOLD) + P(shade, GOLD_D, stroke=None) +
            el("path", d=" ".join(ridges), fill="none", stroke=NAVY, stroke_width=5, stroke_linecap="round") +
            P(d, "none"))


FACE = ((500, 272), [
    ("C", (572, 272), (642, 280), (670, 314)),
    ("C", (694, 360), (702, 420), (720, 472)),
    ("L", (694, 548)),
    ("C", (684, 618), (644, 692), (594, 740)),
    ("C", (562, 767), (532, 780), (500, 782)),
])


def face():
    out = [P(sym(*FACE), CRIMSON)]
    # side facets
    out.append(P(pair((670, 314), [
        ("C", (694, 360), (702, 420), (720, 472)), ("L", (694, 548)),
        ("C", (684, 618), (644, 692), (594, 740)),
        ("C", (612, 680), (640, 610), (648, 540)), ("L", (662, 470)),
        ("C", (652, 420), (650, 360), (670, 314)),
    ]), CRIMSON_D, stroke=None))
    # forehead highlight (V up from the brow ridge)
    out.append(P(sym((500, 300), [("C", (540, 300), (580, 304), (612, 312)),
                                  ("C", (580, 340), (540, 370), (500, 392))]), CRIMSON_L, stroke=None))
    # cheek highlights
    out.append(P(pair((600, 462), [("L", (664, 446)), ("L", (650, 500))]), CRIMSON_L, stroke=None))
    # chin highlight
    out.append(P(sym((500, 730), [("C", (530, 730), (556, 724), (570, 716)),
                                  ("C", (556, 748), (530, 764), (500, 766))]), CRIMSON_D, stroke=None))
    out.append(P(sym(*FACE), "none"))
    return "\n".join(out)


def crown():
    peaks = sym((500, 98), [
        ("L", (522, 140)), ("L", (532, 136)),
        ("L", (552, 190)),
        ("L", (604, 136)),
        ("L", (636, 200)),
        ("L", (686, 178)),
        ("L", (676, 262)),
        ("C", (612, 254), (556, 252), (500, 252)),
    ])
    ridge = [(314, 178), (364, 200), (396, 136), (448, 190), (500, 98), (552, 190), (604, 136),
             (636, 200), (686, 178)]
    base = 262
    shade = []
    for i in range(0, len(ridge) - 1, 2):
        (tx, ty), (vx, vy) = ridge[i], ridge[i + 1]
        if (tx, ty) == (500, 98):
            pts = [(500, 98), (522, 140), (532, 136), (552, 190), (552, base), (512, base)]
        else:
            pts = [(tx, ty), (vx, vy), (vx, base), (tx + 8, base)]
        shade.append(poly(pts))
    shade.append(poly([(686, 178), (676, base), (686, base)]))
    shade = " ".join(shade)
    snow = sym((500, 98), [("L", (522, 140)), ("L", (532, 136)), ("L", (540, 158)), ("L", (526, 152)),
                           ("L", (514, 166)), ("L", (500, 150))])
    snow2 = pair((604, 136), [("L", (624, 176)), ("L", (612, 170)), ("L", (602, 184)), ("L", (592, 168)),
                              ("L", (580, 176))])
    snow3 = pair((686, 178), [("L", (683, 204)), ("L", (674, 198)), ("L", (664, 206)), ("L", (660, 190))])
    band = sym((500, 240), [("C", (560, 238), (626, 244), (680, 250)), ("L", (674, 294)),
                            ("C", (612, 286), (556, 284), (500, 284))])
    rim = sym((500, 240), [("C", (560, 238), (626, 244), (680, 250)), ("L", (679, 258)),
                           ("C", (626, 252), (560, 246), (500, 248))])
    rim2 = sym((500, 276), [("C", (556, 276), (612, 278), (675, 286)), ("L", (674, 294)),
                            ("C", (612, 286), (556, 284), (500, 284))])
    gems = " ".join(f"M{x},{y} m-8,0 a8,8 0 1,0 16,0 a8,8 0 1,0 -16,0" for x, y in
                    [(580, 266), (420, 266), (640, 270), (360, 270)])
    return (P(peaks, GOLD) + P(shade, GOLD_D, stroke=None) + P(snow + " " + snow2 + " " + snow3, WHITE, stroke=None) +
            P(peaks, "none") + P(band, BLUE) + P(rim + " " + rim2, GOLD, stroke=None) + P(band, "none") +
            P(gems, CRIMSON, sw=4) + moon(500, 266))


def moon(cx, cy):
    """Nepal flag moon: upturned crescent beneath a rayed half-disc."""
    cres = (f"M{cx-30},{cy-6} A30,26 0 0,0 {cx+30},{cy-6} "
            f"A34,22 0 0,1 {cx-30},{cy-6}Z")
    rays = []
    n = 8
    for i in range(n + 1):
        a = math.radians(180 + i * 180 / n)
        r1, r2 = 9, 16
        a0, a1 = a - math.radians(7), a + math.radians(7)
        rays.append(poly([(cx + r1 * math.cos(a0), cy - 2 + r1 * math.sin(a0)),
                          (cx + r2 * math.cos(a), cy - 2 + r2 * math.sin(a)),
                          (cx + r1 * math.cos(a1), cy - 2 + r1 * math.sin(a1))]))
    disc = f"M{cx-10},{cy-2} A10,10 0 0,1 {cx+10},{cy-2}Z"
    return P(cres, WHITE, sw=4) + P(" ".join(rays) + " " + disc, WHITE, stroke=None)


def sun_eye():
    return (P(star_sun(500, 336, 21, 40, 12), WHITE, sw=6) +
            el("circle", cx=500, cy=336, r=19, fill=WHITE, stroke=NAVY, stroke_width=5) +
            el("circle", cx=500, cy=336, r=9, fill=GOLD))


def brows():
    d = sym((500, 446), [
        ("C", (512, 420), (526, 404), (546, 396)),
        ("C", (600, 378), (660, 346), (728, 304)),
        ("C", (726, 330), (716, 350), (700, 362)),
        ("C", (648, 386), (594, 404), (552, 420)),
        ("C", (532, 428), (516, 446), (500, 470)),
    ])
    return P(d, NAVY)


def eyes():
    eye = [("C", (590, 420), (640, 400), (690, 372)),
           ("C", (672, 430), (616, 462), (560, 458)),
           ("C", (544, 456), (536, 446), (544, 436))]
    glow = [("C", (594, 424), (636, 408), (670, 392)),
            ("C", (648, 420), (606, 438), (564, 442))]
    slit = [("C", (630, 416), (630, 444), (620, 462)), ("C", (610, 444), (610, 416), (620, 396))]
    glint = " ".join(f"M{x},{y} m-6,0 a6,6 0 1,0 12,0 a6,6 0 1,0 -12,0" for x, y in [(650, 410), (350, 410)])
    eyes_d = pair((544, 436), eye)
    return (f'<clipPath id="gd-eyes"><path d="{eyes_d}"/></clipPath>' +
            P(eyes_d, GOLD, stroke=None) +
            f'<g clip-path="url(#gd-eyes)">' + P(pair((552, 440), glow), GOLD_L, stroke=None) +
            P(pair((620, 396), slit), NAVY, stroke=None) + "</g>" +
            P(eyes_d, "none", sw=6) + P(glint, WHITE, stroke=None))


def nose():
    d = sym((500, 438), [
        ("L", (520, 470)),
        ("C", (538, 500), (574, 504), (580, 534)),
        ("C", (584, 560), (552, 572), (530, 560)),
        ("C", (520, 570), (508, 570), (500, 570)),
    ])
    bridge = sym((500, 446), [("L", (512, 470)), ("L", (512, 530)), ("L", (500, 540))])
    nost = pair((540, 544), [("C", (548, 534), (566, 536), (566, 550)), ("C", (558, 556), (546, 554), (540, 544))])
    return P(d, CRIMSON_D, sw=6) + P(bridge, CRIMSON, stroke=None) + P(nost, NAVY, stroke=None)


def mouth():
    cav = sym((500, 604), [
        ("C", (556, 598), (616, 590), (660, 614)),
        ("C", (634, 670), (572, 714), (500, 718)),
    ])
    upper_lip = sym((500, 588), [
        ("C", (560, 576), (626, 570), (676, 602)),
        ("L", (660, 616)),
        ("C", (614, 594), (556, 604), (500, 610)),
    ])
    lower_lip = sym((500, 716), [("C", (566, 712), (628, 670), (656, 620)),
                                 ("C", (650, 680), (590, 734), (500, 740))])
    teeth = [pair((500, 608), [("L", (500, 632)), ("L", (513, 632)), ("L", (522, 607))]),
             pair((522, 607), [("L", (529, 630)), ("L", (541, 628)), ("L", (546, 605))])]
    low_teeth = pair((500, 716), [("L", (500, 696)), ("L", (512, 696)), ("L", (522, 715))]) + " " + \
        pair((522, 715), [("L", (530, 694)), ("L", (542, 694)), ("L", (548, 712))])
    fang = pair((548, 604), [("C", (558, 634), (566, 656), (574, 684)), ("C", (586, 656), (596, 628), (602, 598))])
    tusk = pair((604, 696), [("C", (622, 654), (646, 610), (670, 552)),
                             ("C", (674, 610), (660, 664), (638, 706))])
    tusk_shade = pair((620, 690), [("C", (640, 650), (660, 610), (670, 552)),
                                   ("C", (674, 610), (660, 664), (638, 706))])
    return (P(cav, MOUTH) + P(" ".join(teeth) + " " + low_teeth, WHITE, sw=4) +
            P(lower_lip, CRIMSON_D, sw=6) + P(upper_lip, CRIMSON_D, sw=6) +
            P(fang, WHITE, sw=6) + P(tusk, IVORY, sw=7) + P(tusk_shade, "#E8D3A0", stroke=None) + P(tusk, "none", sw=7))


def silhouette(extra=26):
    """Thick outer keyline behind everything so the mark reads on any background."""
    sw = OUT + extra
    return "\n".join([
        f'<g stroke="{NAVY}" stroke-width="{sw}" stroke-linejoin="round" fill="{NAVY}">',
        el("circle", cx=BADGE_C[0], cy=BADGE_C[1], r=380),
        khukuri(KHUKURI_T, outline_only=True, sw=sw / 0.9),
        khukuri(KHUKURI_T_M, outline_only=True, sw=sw / 0.9),
        f'<path d="{sym(*MANE)}"/>', f'<path d="{pair(*HORN)}"/>',
        "</g>",
    ])


def build(keyline=True):
    parts = []
    if keyline:
        parts.append(silhouette())
    parts.append(badge())
    parts.append(mane())
    parts.append(khukuri(KHUKURI_T))
    parts.append(khukuri(KHUKURI_T_M))
    parts.append(horns())
    parts.append(face())
    parts.append(crown())
    parts.append(sun_eye())
    parts.append(brows())
    parts.append(eyes())
    parts.append(nose())
    parts.append(mouth())
    return "\n".join(parts)
