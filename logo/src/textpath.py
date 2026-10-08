"""Shape text with HarfBuzz and emit it as SVG path data (no font dependency)."""
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

_cache = {}


def _load(path):
    if path not in _cache:
        blob = hb.Blob.from_file_path(path)
        face = hb.Face(blob)
        font = hb.Font(face)
        tt = TTFont(path)
        _cache[path] = (font, tt, tt["head"].unitsPerEm)
    return _cache[path]


def shape(path, text, features=None):
    font, tt, upem = _load(path)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, features or {"kern": True, "liga": True})
    order = tt.getGlyphOrder()
    out = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        out.append((order[info.codepoint], pos.x_advance, pos.x_offset, pos.y_offset, info.cluster))
    return out


def measure(path, text, size, tracking=0.0, features=None):
    """Advance width in px. tracking is in em units added after each cluster."""
    _, _, upem = _load(path)
    glyphs = shape(path, text, features)
    s = size / upem
    w = 0
    clusters = sorted({g[4] for g in glyphs})
    for g in glyphs:
        w += g[1] * s
    w += tracking * size * (len(clusters) - 1)
    return w


def text_path(path, text, size, x=0, y=0, anchor="start", tracking=0.0, features=None, precision=2):
    """Return (d, bbox) for text with baseline at y. bbox = (xmin, ymin, xmax, ymax) in output coords."""
    font, tt, upem = _load(path)
    glyphs = shape(path, text, features)
    s = size / upem
    width = measure(path, text, size, tracking, features)
    if anchor == "middle":
        x -= width / 2
    elif anchor == "end":
        x -= width
    gs = tt.getGlyphSet()
    spen = SVGPathPen(gs, ntos=lambda v: (f"{v:.{precision}f}").rstrip("0").rstrip("."))
    bpen = BoundsPen(gs)
    cx = x
    last_cluster = None
    for name, adv, xo, yo, cl in glyphs:
        if last_cluster is not None and cl != last_cluster:
            cx += tracking * size
        last_cluster = cl
        t = (s, 0, 0, -s, cx + xo * s, y - yo * s)
        gs[name].draw(TransformPen(spen, t))
        gs[name].draw(TransformPen(bpen, t))
        cx += adv * s
    return spen.getCommands(), bpen.bounds
