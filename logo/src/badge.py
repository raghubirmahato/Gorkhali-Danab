"""Refine the painted Gorkhali Danab badge: crisp banner, authentic khukuris and sun, Devanagari name."""
import sys, os, base64, io, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from PIL import Image, ImageFilter
from textpath import text_path
import emblem as E
from geom import poly, star_sun

FONTS = os.path.join(HERE, "fonts")
SLAB = os.path.join(FONTS, "alfa-slab.ttf")
DEVA = os.path.join(FONTS, "eczar-800.ttf")

BLACK = "#0B0B10"
CRIMSON = "#D7132F"
CRIMSON_D = "#8E0C1F"
WHITE = "#F4F4F2"
NAVY = "#0A1A3F"

W, H = 765, 830          # artwork units (source painting is 765 x 767)
UPSCALE = 2


def base_image(path):
    im = Image.open(path)
    im = im.resize((im.width * UPSCALE, im.height * UPSCALE), Image.LANCZOS)
    rgb = im.convert("RGB").filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    rgb.putalpha(im.getchannel("A"))
    buf = io.BytesIO()
    rgb.save(buf, "PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


def lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


# banner corners (slants up to the right like the original)
TL, TR, BR, BL = (12, 520), (764, 456), (750, 640), (36, 700)
ANGLE = math.degrees(math.atan2(TR[1] - TL[1], TR[0] - TL[0]))
CX = 388


def inset(pts, d):
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    out = []
    for x, y in pts:
        vx, vy = cx - x, cy - y
        n = math.hypot(vx, vy)
        out.append((x + vx / n * d * 1.6, y + vy / n * d))
    return out


def rotated_text(font, s, size, cx, cy, fill, angle, tracking=0.0, stroke=None, sw=0, extra=""):
    _, bb = text_path(font, s, size, 0, 0, tracking=tracking)
    x = -(bb[0] + bb[2]) / 2
    y = -(bb[1] + bb[3]) / 2
    d, _ = text_path(font, s, size, x, y, tracking=tracking)
    st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" paint-order="stroke"' if stroke else ""
    return (f'<path transform="translate({cx:.1f},{cy:.1f}) rotate({angle:.2f})" d="{d}" fill="{fill}"{st} {extra}/>',
            bb[2] - bb[0], bb[3] - bb[1])


def shield():
    """Pointed shield hanging under the banner."""
    top_l, top_r = (176, 640), (600, 610)
    pt = (CX, 812)
    d = (f"M{top_l[0]},{top_l[1]} L{top_r[0]},{top_r[1]} "
         f"C{top_r[0] - 4},{top_r[1] + 80} {pt[0] + 120},{pt[1] - 50} {pt[0]},{pt[1]} "
         f"C{pt[0] - 120},{pt[1] - 50} {top_l[0] + 6},{top_l[1] + 80} {top_l[0]},{top_l[1]}Z")
    di = (f"M{top_l[0] + 18},{top_l[1] + 4} L{top_r[0] - 18},{top_r[1] + 2} "
          f"C{top_r[0] - 24},{top_r[1] + 74} {pt[0] + 104},{pt[1] - 62} {pt[0]},{pt[1] - 18} "
          f"C{pt[0] - 104},{pt[1] - 62} {top_l[0] + 26},{top_l[1] + 74} {top_l[0] + 18},{top_l[1] + 4}Z")
    return d, di


def khukuri_pair(cx, cy, scale, angle):
    t = f"translate({cx},{cy}) rotate({angle}) scale({scale}) translate(-226,0)"
    tm = f"translate({2 * cx},0) scale(-1,1) " + t
    # use a slimmer outline at this size
    saved = (E.OUT, E.NAVY, E.STEEL, E.STEEL_D, E.HANDLE, E.GOLD)
    E.OUT, E.NAVY, E.STEEL, E.STEEL_D, E.HANDLE, E.GOLD = 8, BLACK, "url(#blade)", "#6E7886", "#24160F", "#C9A24A"
    s = (E.khukuri(t, outline_only=True, sw=24) + E.khukuri(tm, outline_only=True, sw=24) +
         E.khukuri(t) + E.khukuri(tm))
    E.OUT, E.NAVY, E.STEEL, E.STEEL_D, E.HANDLE, E.GOLD = saved
    return s


def build(src):
    b64 = base_image(src)
    parts = []
    parts.append("""<defs>
  <filter id="rough" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.09" numOctaves="2" seed="7" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="7" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="grunge" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="3" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -22 16.6" result="m"/>
    <feComposite in="SourceGraphic" in2="m" operator="in"/>
  </filter>
  <filter id="shadow" x="-10%" y="-10%" width="120%" height="130%">
    <feDropShadow dx="0" dy="3" stdDeviation="2.5" flood-color="#000" flood-opacity="0.65"/>
  </filter>
  <linearGradient id="blade" x1="0" y1="-1" x2="0" y2="1" gradientUnits="objectBoundingBox">
    <stop offset="0" stop-color="#FFFFFF"/><stop offset="0.45" stop-color="#D5DAE2"/><stop offset="1" stop-color="#7D8796"/>
  </linearGradient>
  <linearGradient id="steelText" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFFFF"/><stop offset="0.55" stop-color="#ECECEA"/><stop offset="1" stop-color="#BFC3C9"/>
  </linearGradient>
</defs>""")
    parts.append(f'<image href="data:image/png;base64,{b64}" x="0" y="0" width="765" height="767"/>')

    # --- shield (behind the banner)
    sd, sdi = shield()
    parts.append(f'<path d="{sd}" fill="{BLACK}" stroke="{BLACK}" stroke-width="14" stroke-linejoin="round" filter="url(#rough)"/>')
    parts.append(f'<path d="{sdi}" fill="none" stroke="{CRIMSON}" stroke-width="3.5"/>')

    # --- banner
    ban = [TL, TR, BR, BL]
    parts.append(f'<path d="{poly(ban)}" fill="{BLACK}" stroke="{BLACK}" stroke-width="10" stroke-linejoin="round" filter="url(#rough)"/>')
    parts.append(f'<path d="{poly(inset(ban, 11))}" fill="none" stroke="{CRIMSON}" stroke-width="3.5"/>')
    parts.append(f'<path d="{poly(inset(ban, 17))}" fill="none" stroke="{CRIMSON_D}" stroke-width="1.5"/>')

    # GORKHALI
    mid_top = lerp(TL, TR, 0.5)
    g_cy = mid_top[1] + 70
    _, bbg = text_path(SLAB, "GORKHALI", 100, 0, 0, tracking=0.02)
    gsize = 100 * 640 / (bbg[2] - bbg[0])
    t, gw, gh = rotated_text(SLAB, "GORKHALI", gsize, CX, g_cy, "url(#steelText)", ANGLE, tracking=0.02,
                             stroke=BLACK, sw=8, extra='filter="url(#shadow)"')
    parts.append(f'<g filter="url(#grunge)">{t}</g>')

    # DANAB with rules
    d_cy = g_cy + 78
    t, dw, dh = rotated_text(SLAB, "DANAB", 50, CX, d_cy, CRIMSON, ANGLE, tracking=0.16)
    parts.append(f'<g filter="url(#grunge)">{t}</g>')
    a = math.radians(ANGLE)
    ux, uy = math.cos(a), math.sin(a)
    for sgn in (-1, 1):
        r0 = dw / 2 + 22
        r1 = 296 if sgn < 0 else 292
        x0, y0 = CX + sgn * r0 * ux, d_cy + sgn * r0 * uy
        x1, y1 = CX + sgn * r1 * ux, d_cy + sgn * r1 * uy
        nx, ny = -uy, ux
        th = 3.2
        thin = 0.6
        pts = [(x0 + nx * th, y0 + ny * th), (x1 + nx * thin, y1 + ny * thin),
               (x1 - nx * thin, y1 - ny * thin), (x0 - nx * th, y0 - ny * th)]
        parts.append(f'<path d="{poly(pts)}" fill="{CRIMSON}"/>')
        parts.append(f'<path d="M{x0 - sgn * 6 * ux},{y0 - sgn * 6 * uy} m-5,0 l5,-5 l5,5 l-5,5z" fill="{CRIMSON}"/>')

    # --- inside the shield: Devanagari name, crossed khukuris, the flag's 12-rayed sun
    t, nw, nh = rotated_text(DEVA, "गोर्खाली दानव", 31, CX, 694, WHITE, 0)
    parts.append(t)
    parts.append(khukuri_pair(CX, 770, 0.27, -30))
    parts.append(f'<path d="{star_sun(CX, 733, 11.5, 23, 12)}" fill="{WHITE}" stroke="{BLACK}" stroke-width="2.5" stroke-linejoin="round"/>')
    parts.append(f'<circle cx="{CX}" cy="733" r="10" fill="{CRIMSON}"/>')

    body = "\n".join(parts)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Gorkhali Danab">\n'
            f'<title>Gorkhali Danab</title>\n{body}\n</svg>\n')


if __name__ == "__main__":
    # python3 badge.py [painting.png] [out.svg]
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "badge", "source", "badge-painting.png")
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "badge", "gorkhali-danab-badge.svg")
    open(out, "w").write(build(src))
