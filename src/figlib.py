import math, html

NAVY = "#23395d"
FAR = "#a9b6ca"
HL = "#e8590c"
HLF = "#f6b78f"
GRD = "#7b8494"
GRN = "#1c7c54"
RED = "#d6336c"
BLU = "#1971c2"
RKT = "#2b8a3e"
FONT = "Noto Sans CJK JP, sans-serif"


def f(v):
    return f"{v:.1f}"


def line(p, q, col, w=5, dash=None, cap="round"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{f(p[0])}" y1="{f(p[1])}" x2="{f(q[0])}" y2="{f(q[1])}" '
            f'stroke="{col}" stroke-width="{w}" stroke-linecap="{cap}"{d}/>')


def dn(p, ang, l):
    r = math.radians(ang)
    return (p[0] + l * math.sin(r), p[1] + l * math.cos(r))


def up(p, ang, l):
    r = math.radians(ang)
    return (p[0] + l * math.sin(r), p[1] - l * math.cos(r))


def text(x, y, s, size=10, col=NAVY, anchor="middle", weight="bold"):
    return (f'<text x="{f(x)}" y="{f(y)}" font-size="{size}" fill="{col}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-family="{FONT}">{html.escape(s)}</text>')


def arrow(x1, y1, x2, y2, col=GRN, w=2.5, dash=None):
    a = math.atan2(y2 - y1, x2 - x1)
    hl, hw = 8, 4.5
    bx, by = x2 - hl * math.cos(a), y2 - hl * math.sin(a)
    px, py = -math.sin(a) * hw, math.cos(a) * hw
    return (line((x1, y1), (bx, by), col, w, dash) +
            f'<polygon points="{f(x2)},{f(y2)} {f(bx+px)},{f(by+py)} {f(bx-px)},{f(by-py)}" fill="{col}"/>')


def carrow(x1, y1, cx, cy, x2, y2, col=GRN, w=2.5, dash=None):
    a = math.atan2(y2 - cy, x2 - cx)
    hl, hw = 8, 4.5
    bx, by = x2 - hl * math.cos(a), y2 - hl * math.sin(a)
    px, py = -math.sin(a) * hw, math.cos(a) * hw
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="M{f(x1)},{f(y1)} Q{f(cx)},{f(cy)} {f(bx)},{f(by)}" fill="none" stroke="{col}" '
            f'stroke-width="{w}" stroke-linecap="round"{d}/>'
            f'<polygon points="{f(x2)},{f(y2)} {f(bx+px)},{f(by+py)} {f(bx-px)},{f(by-py)}" fill="{col}"/>')


def rect(x, y, w, h, fill="#dfe5ee", stroke=GRD, sw=1.5, rx=2):
    return (f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>')


def circle(x, y, r, fill="none", stroke=NAVY, sw=2):
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def ground(y, x1=6, x2=164):
    return line((x1, y), (x2, y), GRD, 2.5, cap="butt")


def badge(x, y, s, col=RED):
    """small label with white background"""
    w = 10.5 * len(s) + 10
    x = min(max(x, w / 2 + 3), 167 - w / 2)
    return (rect(x - w / 2, y - 11, w, 15, fill="#ffffff", stroke=col, sw=1.2, rx=4) +
            text(x, y, s, 9.5, col))


def pose(hx, hy, nt, ns, ft, fs, torso, head, nu, nf, fu, ff):
    P = {}
    hip = (hx, hy)
    P["hip"] = hip
    P["nknee"] = dn(hip, nt, 24)
    P["nank"] = dn(P["nknee"], ns, 24)
    P["fknee"] = dn(hip, ft, 24)
    P["fank"] = dn(P["fknee"], fs, 24)
    P["neck"] = up(hip, torso, 28)
    P["sh"] = up(hip, torso, 25)
    P["head"] = up(P["neck"], torso if head is None else head, 9)
    P["nelb"] = dn(P["sh"], nu, 17)
    P["nhand"] = dn(P["nelb"], nf, 16)
    P["felb"] = dn(P["sh"], fu, 17)
    P["fhand"] = dn(P["felb"], ff, 16)
    return P


def fig(hx, gy, nt=0, ns=0, ft=0, fs=0, torso=0, head=None, nu=0, nf=0, fu=0, ff=0,
        hl=(), lift=0, nfoot=90, ffoot=90, racket=None, front=False, hy=None,
        anchor=None, ball=False, ballcol="#f59f00"):
    def ext(a, b):
        return 24 * math.cos(math.radians(a)) + 24 * math.cos(math.radians(b))

    base_y = (gy - max(ext(nt, ns), ext(ft, fs)) - lift) if hy is None else hy
    if anchor:
        name, ax = anchor
        p0 = pose(0, base_y, nt, ns, ft, fs, torso, head, nu, nf, fu, ff)
        hx = ax - p0[name][0]
    P = pose(hx, base_y, nt, ns, ft, fs, torso, head, nu, nf, fu, ff)
    hip = P["hip"]
    legs, core, arms = "legs" in hl, "core" in hl, "arms" in hl
    cln, clf = (HL, HLF) if legs else (NAVY, FAR)
    can, caf = (HL, HLF) if arms else (NAVY, FAR)
    ct = HL if core else NAVY

    def foot(a, ang, col):
        if front:
            return line((a[0] - 4.5, a[1] + 1), (a[0] + 4.5, a[1] + 1), col, 4)
        return line(a, dn(a, ang, 9), col, 4)

    s = []
    s.append(line(hip, P["fknee"], clf, 5.5))
    s.append(line(P["fknee"], P["fank"], clf, 5))
    s.append(foot(P["fank"], ffoot, clf))
    s.append(line(P["sh"], P["felb"], caf, 4.5))
    s.append(line(P["felb"], P["fhand"], caf, 4))
    s.append(line(hip, P["neck"], ct, 7))
    s.append(line(hip, P["nknee"], cln, 6))
    s.append(line(P["nknee"], P["nank"], cln, 5.5))
    s.append(foot(P["nank"], nfoot, cln))
    s.append(line(P["sh"], P["nelb"], can, 5))
    s.append(line(P["nelb"], P["nhand"], can, 4.5))
    s.append(circle(P["head"][0], P["head"][1], 7, "#ffffff", NAVY, 2.5))
    if racket is not None:
        h = P["nhand"]
        tip = up(h, racket, 20)
        c = up(h, racket, 30)
        s.append(line(h, tip, RKT, 2.5))
        s.append(f'<ellipse cx="{f(c[0])}" cy="{f(c[1])}" rx="6" ry="10" transform="rotate({racket} {f(c[0])} {f(c[1])})" '
                 f'fill="{RKT}" fill-opacity="0.12" stroke="{RKT}" stroke-width="2"/>')
        P["rtip"] = up(h, racket, 41)
        P["rcen"] = c
    if ball:
        mid = ((P["nhand"][0] + P["fhand"][0]) / 2, (P["nhand"][1] + P["fhand"][1]) / 2)
        s.append(circle(mid[0], mid[1] - 2, 7.5, ballcol, "#b36b00", 2))
        P["ball"] = mid
    return "".join(s), P


def svg(inner, vb="0 0 170 150", wpx=200):
    x, y, w, h = [float(v) for v in vb.split()]
    hpx = wpx * h / w
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{wpx}" height="{f(hpx)}" viewBox="{vb}">{inner}</svg>')


def wall(x, y1, y2):
    s = rect(x, y1, 9, y2 - y1, fill="#e9ecef", stroke=GRD, sw=1.5, rx=0)
    for yy in range(int(y1) + 6, int(y2), 10):
        s += line((x + 9, yy), (x + 3, yy + 6), GRD, 1)
    return s


# ---------- court (top view) ----------
def court_svg(wpx=250):
    sc = 28
    x0, y0 = 34, 24
    W, L = 6.1 * sc, 6.7 * sc
    s = []
    s.append(rect(x0, y0, W, L, fill="#e6f4ea", stroke=NAVY, sw=2.5, rx=0))
    xs1, xs2 = x0 + 0.46 * sc, x0 + W - 0.46 * sc
    s.append(line((xs1, y0), (xs1, y0 + L), NAVY, 1.4, cap="butt"))
    s.append(line((xs2, y0), (xs2, y0 + L), NAVY, 1.4, cap="butt"))
    ys = y0 + 1.98 * sc
    s.append(line((x0, ys), (x0 + W, ys), NAVY, 1.4, cap="butt"))
    yl = y0 + L - 0.76 * sc
    s.append(line((x0, yl), (x0 + W, yl), NAVY, 1.4, cap="butt"))
    s.append(line((x0 + W / 2, ys), (x0 + W / 2, y0 + L), NAVY, 1.4, cap="butt"))
    s.append(line((x0 - 8, y0), (x0 + W + 8, y0), "#444", 4, cap="butt"))
    s.append(text(x0 + W / 2, y0 - 8, "ネット", 10, "#444"))
    base = (x0 + W / 2, y0 + 3.4 * sc)
    pts = [("1", x0 + W - 26, y0 + 28), ("2", x0 + 26, y0 + 28),
           ("3", x0 + W - 22, base[1]), ("4", x0 + 22, base[1]),
           ("5", x0 + W - 26, y0 + L - 22), ("6", x0 + 26, y0 + L - 22)]
    for n, px, py in pts:
        dx, dy = px - base[0], py - base[1]
        d = math.hypot(dx, dy)
        ex, ey = px - dx / d * 13, py - dy / d * 13
        s.append(arrow(base[0], base[1], ex, ey, GRN, 2.2, dash="5,3"))
    for n, px, py in pts:
        s.append(circle(px, py, 11, "#ffffff", RED, 2.2))
        s.append(text(px, py + 4, n, 12, RED))
    s.append(circle(base[0], base[1], 6, NAVY, NAVY, 1))
    s.append(text(base[0] + 4, base[1] + 21, "ベース", 9.5, NAVY))
    vb = f"0 0 {x0*2 + W:.0f} {y0 + L + 10:.0f}"
    return svg("".join(s), vb, wpx)


def cross_svg(wpx=200):
    s = []
    cx, cy = 85, 78
    s.append(rect(10, 12, 150, 132, fill="#f1f3f5", stroke="#ced4da", sw=1.2, rx=6))
    s.append(line((cx - 58, cy), (cx + 58, cy), "#e8590c", 3, cap="butt"))
    s.append(line((cx, cy - 56), (cx, cy + 56), "#e8590c", 3, cap="butt"))
    for (px, py, n) in [(cx, cy - 56, "1"), (cx + 58, cy, "2"), (cx, cy + 56, "3"), (cx - 58, cy, "4")]:
        s.append(circle(px, py, 10, "#ffffff", RED, 2.2))
        s.append(text(px, py + 4, n, 12, RED))
    s.append(circle(cx, cy, 11, NAVY, NAVY, 1))
    s.append(text(cx, cy + 4, "自分", 9, "#ffffff"))
    for (dx, dy) in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        s.append(carrow(cx + dx * 14, cy + dy * 14, cx + dx * 28 + dy * 8, cy + dy * 28 + dx * 8, cx + dx * 42, cy + dy * 42, GRN, 2))
    s.append(text(85, 158, "中央→外へタッチ→中央へ戻る", 9.5, NAVY))
    return svg("".join(s), "0 0 170 165", wpx)
