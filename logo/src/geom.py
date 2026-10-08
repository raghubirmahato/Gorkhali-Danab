"""Geometry helpers: symmetric paths mirrored about x = CX."""
import math

CX = 500


def f(v):
    s = f"{v:.1f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def pt(p):
    return f"{f(p[0])},{f(p[1])}"


def mx(p):
    return (2 * CX - p[0], p[1])


def seg_str(seg):
    kind = seg[0]
    return kind + " ".join(pt(p) for p in seg[1:])


def reverse_segments(start, segs):
    """Reverse a polyline/bezier chain. Returns (new_start, new_segs)."""
    pts = [start] + [s[-1] for s in segs]
    out = []
    for i in range(len(segs) - 1, -1, -1):
        s = segs[i]
        p_prev = pts[i]
        if s[0] == "L":
            out.append(("L", p_prev))
        elif s[0] == "Q":
            out.append(("Q", s[1], p_prev))
        elif s[0] == "C":
            out.append(("C", s[2], s[1], p_prev))
    return pts[-1], out


def mirror_segs(segs):
    return [tuple([s[0]] + [mx(p) for p in s[1:]]) for s in segs]


def sym(start, segs):
    """Closed symmetric path. `start` lies on the axis; the right-half chain
    `segs` ends on the axis. Left half is the mirrored chain, reversed."""
    d = "M" + pt(start) + " " + " ".join(seg_str(s) for s in segs)
    end, rev = reverse_segments(mx(start), mirror_segs(segs))
    d += " " + " ".join(seg_str(s) for s in rev) + "Z"
    return d


def path(start, segs, close=True):
    return "M" + pt(start) + " " + " ".join(seg_str(s) for s in segs) + ("Z" if close else "")


def mirror_path(start, segs, close=True):
    return path(mx(start), mirror_segs(segs), close)


def pair(start, segs, close=True):
    """Right-half shape plus its mirror, as one d string."""
    return path(start, segs, close) + " " + mirror_path(start, segs, close)


def poly(points, close=True):
    return "M" + " L".join(pt(p) for p in points) + ("Z" if close else "")


def mpoly(points, close=True):
    return poly([mx(p) for p in points], close)


def rot(p, ang, c=(0, 0)):
    a = math.radians(ang)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))


def star_sun(cx, cy, r_in, r_out, n=12, phase=0.0):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(phase + i * 180 / n - 90)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return poly(pts)
