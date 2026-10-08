"""Builds every logo SVG in ../ from the emblem and the outlined wordmark."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import emblem as E
from textpath import text_path

FONTS = os.environ.get("GD_FONTS", os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts"))
LATIN = os.path.join(FONTS, "cinzel-900.ttf")
DEVA = os.path.join(FONTS, "eczar-800.ttf")

# emblem ink box in its own units
EMB = (95, 52, 905, 1031)
EMB_W, EMB_H = EMB[2] - EMB[0], EMB[3] - EMB[1]


def emblem_at(x, y, h):
    """Place the emblem so its ink box has top-left (x, y) and height h."""
    s = h / EMB_H
    return f'<g transform="translate({x - EMB[0] * s:.2f},{y - EMB[1] * s:.2f}) scale({s:.5f})">\n{E.build()}\n</g>', EMB_W * s


def text(font, s, size, x, y, fill, anchor="middle", tracking=0.0):
    d, bb = text_path(font, s, size, x, y, anchor=anchor, tracking=tracking)
    return f'<path d="{d}" fill="{fill}"/>', bb


def recentre(font, s, size, cx, y, fill, tracking=0.0):
    """Centre on the ink box rather than the advance box (trailing sidebearing differs per letter)."""
    _, bb = text_path(font, s, size, 0, y, anchor="start", tracking=tracking)
    x = cx - (bb[0] + bb[2]) / 2
    return text(font, s, size, x, y, fill, anchor="start", tracking=tracking)


def diamond(cx, cy, r, fill):
    return f'<path d="M{cx},{cy - r} L{cx + r},{cy} L{cx},{cy + r} L{cx - r},{cy}Z" fill="{fill}"/>'


def rule(x0, x1, cy, fill, thick=7):
    return f'<rect x="{min(x0, x1):.1f}" y="{cy - thick / 2:.1f}" width="{abs(x1 - x0):.1f}" height="{thick}" fill="{fill}"/>'


def palette(dark):
    if dark:
        return dict(bg=E.NAVY, primary="#FFFFFF", accent=E.GOLD, deva="#FF5C77", rule=E.GOLD)
    return dict(bg=None, primary=E.NAVY, accent=E.CRIMSON, deva=E.BLUE, rule=E.GOLD_D)


def wordmark_block(cx, top, width, c):
    """Stacked wordmark centred on cx. Returns (svg, bottom_y)."""
    out = []
    # GORKHALI
    size1 = 100
    _, bb = text_path(LATIN, "GORKHALI", size1, 0, 0, tracking=0.06)
    size1 = size1 * width / (bb[2] - bb[0])
    _, bb = text_path(LATIN, "GORKHALI", size1, 0, 0, tracking=0.06)
    base1 = top - bb[1]
    t, bb1 = recentre(LATIN, "GORKHALI", size1, cx, base1, c["primary"], tracking=0.06)
    out.append(t)
    # DANAB between rules
    size2 = size1 * 0.62
    gap = size1 * 0.26
    _, bbd = text_path(LATIN, "DANAB", size2, 0, 0, tracking=0.32)
    base2 = bb1[3] + gap - bbd[1]
    t, bb2 = recentre(LATIN, "DANAB", size2, cx, base2, c["accent"], tracking=0.32)
    out.append(t)
    mid = (bb2[1] + bb2[3]) / 2
    pad = size2 * 0.38
    r = size2 * 0.085
    lx0, lx1 = bb1[0] + r, bb2[0] - pad
    rx0, rx1 = bb2[2] + pad, bb1[2] - r
    out.append(rule(lx0, lx1, mid, c["rule"], thick=size2 * 0.07))
    out.append(rule(rx0, rx1, mid, c["rule"], thick=size2 * 0.07))
    out.append(diamond(bb1[0] + r, mid, r, c["rule"]))
    out.append(diamond(bb1[2] - r, mid, r, c["rule"]))
    out.append(diamond(lx1, mid, r * 0.8, c["accent"]))
    out.append(diamond(rx0, mid, r * 0.8, c["accent"]))
    # Devanagari
    size3 = size1 * 0.5
    _, bbn = text_path(DEVA, "गोर्खाली दानव", size3, 0, 0)
    base3 = bb2[3] + gap * 1.15 - bbn[1]
    t, bb3 = recentre(DEVA, "गोर्खाली दानव", size3, cx, base3, c["deva"])
    out.append(t)
    return "\n".join(out), bb3[3]


def svg_doc(w, h, body, bg=None, title="Gorkhali Danab"):
    bgr = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="{title}">\n'
            f'<title>{title}</title>\n{bgr}\n{body}\n</svg>\n')


def vertical(dark=False):
    c = palette(dark)
    W, M = 1200, 90
    emb_h = 820
    emb, emb_w = emblem_at((W - EMB_W * emb_h / EMB_H) / 2, M, emb_h)
    words, bottom = wordmark_block(W / 2, M + emb_h + 56, 900, c)
    H = bottom + M
    return svg_doc(W, H, emb + "\n" + words, c["bg"])


def horizontal(dark=False):
    c = palette(dark)
    M = 70
    emb_h = 560
    emb, emb_w = emblem_at(M, M, emb_h)
    tw = 1000
    words_x = M + emb_w + 70
    # stacked block left-aligned: build centred then shift
    words, bottom = wordmark_block(words_x + tw / 2, 0, tw, c)
    block_h = bottom
    dy = M + (emb_h - block_h) / 2
    W = words_x + tw + M
    H = emb_h + 2 * M
    return svg_doc(W, H, emb + f'\n<g transform="translate(0,{dy:.2f})">\n{words}\n</g>', c["bg"])


def emblem_only():
    pad = 24
    x0, y0 = EMB[0] - pad, EMB[1] - pad
    w, h = EMB_W + 2 * pad, EMB_H + 2 * pad
    side = max(w, h)
    x0 -= (side - w) / 2
    y0 -= (side - h) / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.0f} {y0:.0f} {side:.0f} {side:.0f}" role="img" '
            f'aria-label="Gorkhali Danab emblem">\n<title>Gorkhali Danab</title>\n{E.build()}\n</svg>\n')


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    os.makedirs(out, exist_ok=True)
    files = {
        "gorkhali-danab-emblem.svg": emblem_only(),
        "gorkhali-danab-logo.svg": vertical(),
        "gorkhali-danab-logo-dark.svg": vertical(dark=True),
        "gorkhali-danab-horizontal.svg": horizontal(),
        "gorkhali-danab-horizontal-dark.svg": horizontal(dark=True),
    }
    for name, svg in files.items():
        open(os.path.join(out, name), "w").write(svg)
        print(name, len(svg))
