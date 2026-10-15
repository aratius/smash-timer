"""figlib v2 : 教材図用の人体・小物描画ライブラリ
角度の約束: dn(p, a, l) は真下=0°・前方(右)が正・180°が真上。up() はその逆向き。
"""
import math, html

# ---------------------------------------------------------------- palette
NAVY = "#23395d"
GRD = "#7b8494"
GRN = "#1c7c54"      # ポイント(コツ)ラベル
RED = "#d6336c"      # NG 専用
MOV = "#1971c2"      # 動作の矢印・バッジ
BLU = MOV
HL = "#ff7a14"       # 使う部位(オーバーレイ専用)
OUT = "#1b2a44"      # 輪郭線
EQ = "#7048e8"       # ゴム・縄などの用具
FONT = "Noto Sans CJK JP, sans-serif"

SKIN, SKIN_D = "#f3c9a5", "#c99a76"
SHIRT, SHIRT_D = "#2f64a8", "#1d3f6e"
TORSO_SH = "#24508a"
SHORT, SHORT_D = "#1f2d4a", "#0f1626"
HAIR = "#2a2631"
SHOE, SHOE_D = "#ffffff", "#b6bfcc"
SOLE, SOLE_D = "#5c677a", "#465063"
BALL, BALL_D = "#6d5a4a", "#4f4136"     # メディシンボール(茶系)

# ---------------------------------------------------------------- check registry
VBX = [0.0, 170.0, -1e9, 1e9]      # 現在のコマの範囲(バッジ位置クランプ用)


def set_vbx(vb):
    x0, y0, w, h = [float(v) for v in vb.split()]
    VBX[0], VBX[1], VBX[2], VBX[3] = x0, x0 + w, y0, y0 + h
    return vb


CHK = {"pts": [], "rects": [], "tips": [], "arrows": [], "apts": [], "obst": []}


def chk_reset():
    for k in CHK:
        CHK[k] = []


def f(v):
    return f"{v:.1f}"


# ---------------------------------------------------------------- primitives
def line(p, q, col, w=5, dash=None, cap="round", op=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' stroke-opacity="{op}"' if op is not None else ""
    return (f'<line x1="{f(p[0])}" y1="{f(p[1])}" x2="{f(q[0])}" y2="{f(q[1])}" '
            f'stroke="{col}" stroke-width="{w}" stroke-linecap="{cap}"{d}{o}/>')


def dn(p, ang, l):
    r = math.radians(ang)
    return (p[0] + l * math.sin(r), p[1] + l * math.cos(r))


def up(p, ang, l):
    r = math.radians(ang)
    return (p[0] + l * math.sin(r), p[1] - l * math.cos(r))


def add(p, v, k=1.0):
    return (p[0] + v[0] * k, p[1] + v[1] * k)


def lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def unit(p, q):
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy) or 1e-6
    return (dx / L, dy / L)


def dist(p, q):
    return math.hypot(q[0] - p[0], q[1] - p[1])


def text(x, y, s, size=10, col=NAVY, anchor="middle", weight="bold"):
    return (f'<text x="{f(x)}" y="{f(y)}" font-size="{size}" fill="{col}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-family="{FONT}">{html.escape(s)}</text>')


def _head(x2, y2, a, col, hl=7.5, hw=4.3):
    bx, by = x2 - hl * math.cos(a), y2 - hl * math.sin(a)
    px, py = -math.sin(a) * hw, math.cos(a) * hw
    return (bx, by), (f'<polygon points="{f(x2)},{f(y2)} {f(bx+px)},{f(by+py)} {f(bx-px)},{f(by-py)}" '
                      f'fill="{col}" stroke="#ffffff" stroke-width="0.8" stroke-linejoin="round"/>')


def _apts(pts):
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        n = max(1, int(dist(a, b) / 3))
        for k in range(n + 1):
            CHK["apts"].append(lerp(a, b, k / n))


def obst(x, y, w, h):
    CHK["obst"].append((x, y, w, h))


def arrow(x1, y1, x2, y2, col=MOV, w=2.4, dash=None):
    CHK["arrows"] += [(x1, y1), (x2, y2)]
    _apts([(x1, y1), (x2, y2)])
    a = math.atan2(y2 - y1, x2 - x1)
    (bx, by), hd = _head(x2, y2, a, col)
    return (line((x1, y1), (bx, by), "#ffffff", w + 1.8, dash) + line((x1, y1), (bx, by), col, w, dash) + hd)


def carrow(x1, y1, cx, cy, x2, y2, col=MOV, w=2.4, dash=None):
    CHK["arrows"] += [(x1, y1), (x2, y2)]
    _apts([((1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t * t * x2, (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t * t * y2)
           for t in [i / 12 for i in range(13)]])
    a = math.atan2(y2 - cy, x2 - cx)
    (bx, by), hd = _head(x2, y2, a, col)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    pth = f'M{f(x1)},{f(y1)} Q{f(cx)},{f(cy)} {f(bx)},{f(by)}'
    return (f'<path d="{pth}" fill="none" stroke="#ffffff" stroke-width="{w+1.8}" stroke-linecap="round"{d}/>'
            f'<path d="{pth}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"{d}/>' + hd)


def earc(cx, cy, rx, ry, a1, a2, col=MOV, w=2.4):
    """楕円弧の矢印 (a1→a2, 度, 0=右, 90=下)。回旋の表現用"""
    pts = []
    n = 24
    for i in range(n + 1):
        t = math.radians(a1 + (a2 - a1) * i / n)
        pts.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
    CHK["arrows"] += [pts[0], pts[-1]]
    _apts(pts)
    a = math.atan2(pts[-1][1] - pts[-3][1], pts[-1][0] - pts[-3][0])
    (bx, by), hd = _head(pts[-1][0], pts[-1][1], a, col)
    body = pts[:-2] + [(bx, by)]
    d = "M" + " L".join(f"{f(x)},{f(y)}" for x, y in body)
    return (f'<path d="{d}" fill="none" stroke="#ffffff" stroke-width="{w+1.8}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>' + hd)


def rect(x, y, w, h, fill="#dfe5ee", stroke=GRD, sw=1.5, rx=2):
    return (f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>')


def circle(x, y, r, fill="none", stroke=NAVY, sw=2):
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def ground(y, x1=-20, x2=190):
    return (f'<rect x="{f(x1)}" y="{f(y)}" width="{f(x2-x1)}" height="40" fill="#e3e8ef"/>' +
            line((x1, y), (x2, y), "#8d97a8", 2.0, cap="butt"))


def _tw(s, size):
    return sum(size * (0.62 if ord(ch) < 128 else 1.04) for ch in s)


def badge(x, y, s, col=MOV, size=13.0):
    """白地の小ラベル。(x,y) は文字のベースライン中央。緑=フォームのコツ / 青=動作の指示 / 赤=NG"""
    size = max(size * 1.25 if size < 12 else size, 12.5)   # スマホ表示(パネル幅~230px)で13px以上
    w = _tw(s, size) + 10
    x = min(max(x, VBX[0] + 4.2 + w / 2), VBX[1] - 4.2 - w / 2)      # 枠内に収める
    y = min(max(y, VBX[2] + 4.2 + size + 1.5), VBX[3] - 4.2 - 4.5)
    h = size + 6
    CHK["rects"].append((x - w / 2, y - size - 1.5, w, h, s))
    return (rect(x - w / 2, y - size - 1.5, w, h, fill="#ffffff", stroke=col, sw=1.2, rx=4) +
            text(x, y, s, size, col))


def legend(x, y, s="使う部位"):
    """オレンジ=使う部位 の凡例 (x,y は左下)"""
    w = _tw(s, 10.5) + 18
    CHK["rects"].append((x - 1, y - 11, w + 1, 14, s))
    return (f'<rect x="{f(x)}" y="{f(y-10)}" width="12.5" height="9.6" rx="2.8" fill="{HL}" fill-opacity=".58"/>'
            + text(x + 16, y - 1, s, 10.5, "#4a5568", "start"))


def ng_mark(cx, cy, r, vb_right=170, vb_top=0):
    """NG コマ: 悪い部位を赤い輪で囲み、右上に ✕"""
    s = (f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{RED}" fill-opacity=".08" stroke="{RED}" '
         f'stroke-width="2" stroke-dasharray="5,3"/>')
    x, y = vb_right - 14, vb_top + 14
    CHK["rects"].append((x - 10, y - 10, 20, 20, "x"))
    s += circle(x, y, 9.5, RED, "#ffffff", 1.5)
    s += line((x - 4, y - 4), (x + 4, y + 4), "#ffffff", 2.4) + line((x - 4, y + 4), (x + 4, y - 4), "#ffffff", 2.4)
    return s


# ---------------------------------------------------------------- layered renderer
def _poly(pts):
    return " ".join(f"{f(x)},{f(y)}" for x, y in pts)


class Layer:
    def __init__(self):
        self.p = []

    def cap(self, p, q, r1, r2, fill):
        self.p.append(("c", p, q, r1, r2, fill))

    def circ(self, c, r, fill):
        self.p.append(("o", c, r, fill))

    def ell(self, c, rx, ry, rot, fill):
        self.p.append(("e", c, rx, ry, rot, fill))

    def poly(self, pts, fill):
        self.p.append(("p", pts, fill))

    @staticmethod
    def _draw(pr, grow=0.0, fill=None, extra=""):
        k = pr[0]
        if k == "c":
            _, p, q, r1, r2, c = pr
            c = fill or c
            r1, r2 = r1 + grow, r2 + grow
            dx, dy = q[0] - p[0], q[1] - p[1]
            L = math.hypot(dx, dy) or 1e-6
            nx, ny = -dy / L, dx / L
            pts = [(p[0] + nx * r1, p[1] + ny * r1), (q[0] + nx * r2, q[1] + ny * r2),
                   (q[0] - nx * r2, q[1] - ny * r2), (p[0] - nx * r1, p[1] - ny * r1)]
            return (f'<polygon points="{_poly(pts)}" fill="{c}"{extra}/>'
                    f'<circle cx="{f(p[0])}" cy="{f(p[1])}" r="{f(r1)}" fill="{c}"{extra}/>'
                    f'<circle cx="{f(q[0])}" cy="{f(q[1])}" r="{f(r2)}" fill="{c}"{extra}/>')
        if k == "o":
            _, cc, r, c = pr
            return f'<circle cx="{f(cc[0])}" cy="{f(cc[1])}" r="{f(r+grow)}" fill="{fill or c}"{extra}/>'
        if k == "e":
            _, cc, rx, ry, rot, c = pr
            return (f'<ellipse cx="{f(cc[0])}" cy="{f(cc[1])}" rx="{f(rx+grow)}" ry="{f(ry+grow)}" '
                    f'transform="rotate({f(rot)} {f(cc[0])} {f(cc[1])})" fill="{fill or c}"{extra}/>')
        if k == "p":
            _, pts, c = pr
            st = (f' stroke="{fill}" stroke-width="{f(2*grow)}" stroke-linejoin="round"' if grow > 0 else "")
            return f'<polygon points="{_poly(pts)}" fill="{fill or c}"{st}{extra}/>'
        return ""

    def render(self, ow=1.1, outline=True):
        o = ""
        if outline:
            o = '<g opacity=".9">' + "".join(self._draw(pr, ow, OUT) for pr in self.p) + "</g>"
        return o + "".join(self._draw(pr) for pr in self.p)


def cap(p, q, r1, r2, fill, op=1.0):
    L = Layer()
    L.cap(p, q, r1, r2, fill)
    s = L.render(outline=False)
    return f'<g opacity="{op}">{s}</g>' if op < 1 else s


def muscle(c, rx, ry, rot, op=0.66):
    """使う部位のオーバーレイ: 筋肉に沿った細長い半透明オレンジ(手足の輪郭内に収まる寸法)"""
    ry = min(ry, rx / 1.8)
    return (f'<ellipse cx="{f(c[0])}" cy="{f(c[1])}" rx="{f(rx)}" ry="{f(ry)}" transform="rotate({f(rot)} {f(c[0])} {f(c[1])})" '
            f'fill="{HL}" fill-opacity="{op}"/>')


def ang_of(v):
    return math.degrees(math.atan2(v[1], v[0]))


# ---------------------------------------------------------------- head
def _rot(c, a):
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
    return lambda x, y: (c[0] + x * ca - y * sa, c[1] + x * sa + y * ca)


def head_layer(c, ang=0.0, front=False, flip=False):
    """頭部(輪郭つき)。ang: 頭の傾き(度, 時計回り)。横顔は +x を向く(flip で -x)。"""
    s = -1 if flip else 1
    R = _rot(c, ang)
    X = lambda x, y: R(s * x, y)
    L = Layer()
    det = []
    if front:
        L.circ(X(-7.3, 0.9), 1.9, SKIN)
        L.circ(X(7.3, 0.9), 1.9, SKIN)
        L.ell(c, 7.6, 8.2, ang, SKIN)
        hair = [X(8.0 * math.cos(math.radians(t)), 8.4 * math.sin(math.radians(t)) + 0.2) for t in range(-190, 11, 10)]
        hair += [X(6.2, -2.4), X(2.0, -4.6), X(-3.0, -4.2), X(-6.6, -1.6)]
        L.poly(hair, HAIR)
        for ex in (-2.7, 2.7):
            det.append(f'<circle cx="{f(X(ex,0.8)[0])}" cy="{f(X(ex,0.8)[1])}" r="1.0" fill="{HAIR}"/>')
            det.append(line(X(ex - 1.4, -1.6), X(ex + 1.4, -1.8), HAIR, 0.8))
        det.append(line(X(-1.6, 4.6), X(1.6, 4.6), "#a8553a", 0.9))
        det.append(line(X(0, 1.2), X(0.5, 3.0), SKIN_D, 0.8))
    else:
        L.ell(X(1.4, 2.6), 5.8, 5.0, ang, SKIN)                     # jaw
        L.circ(c, 7.8, SKIN)
        L.poly([X(6.6, -1.8), X(9.4, 1.9), X(6.6, 2.7)], SKIN)      # nose
        hair = [X(8.3 * math.cos(math.radians(t)), 8.3 * math.sin(math.radians(t))) for t in range(-55, -245, -10)]
        hair += [X(-5.0, 6.4), X(-2.4, 2.0), X(1.0, -2.0), X(4.6, -4.6)]
        L.poly(hair, HAIR)
        L.ell(X(-0.8, 1.2), 1.8, 2.5, ang, SKIN)                    # ear
        e = X(4.0, -0.4)
        det.append(f'<circle cx="{f(e[0])}" cy="{f(e[1])}" r="1.0" fill="{HAIR}"/>')
        det.append(line(X(2.6, -2.9), X(5.6, -3.2), HAIR, 0.9))
        det.append(line(X(5.0, 4.6), X(6.6, 4.3), "#a8553a", 0.9))
        det.append(line(X(-1.2, 0.0), X(-0.6, 2.4), SKIN_D, 0.7))
    return L.render() + "".join(det)


def head_at(c, front=False, ang=0.0, flip=False):
    return head_layer(c, ang, front, flip)


# ---------------------------------------------------------------- pose
def pose(hx, hy, nt, ns, ft, fs, torso, head, nu, nf, fu, ff, front=False, nb=0, fb=0, nfl=1.0, ffl=1.0, sw=1.0, nul=1.0, ful=1.0, tw=0.0):
    P = {}
    hip = (hx, hy)
    P["hip"] = hip
    tr = math.radians(torso)
    ax = (math.sin(tr), -math.cos(tr))          # 背骨の上方向
    rp = (math.cos(tr), math.sin(tr))           # 体の右(前)方向
    P["ax"], P["rp"] = ax, rp
    if front:
        # n = 本人の右側 = 画面の左
        P["nhipj"] = add(hip, rp, -4.8)
        P["fhipj"] = add(hip, rp, 4.8)
        lt = lambda b: 24 * math.cos(math.radians(0.9 * b))
        ls = lambda b: 24 * math.cos(math.radians(0.45 * b))
        P["nknee"] = dn(P["nhipj"], nt - 0.32 * nb, lt(nb))
        P["nank"] = dn(P["nknee"], ns + 0.22 * nb, ls(nb))
        P["fknee"] = dn(P["fhipj"], ft + 0.32 * fb, lt(fb))
        P["fank"] = dn(P["fknee"], fs - 0.22 * fb, ls(fb))
    else:
        P["nhipj"] = P["fhipj"] = hip
        P["nknee"] = dn(hip, nt, 24)
        P["nank"] = dn(P["nknee"], ns, 24)
        P["fknee"] = dn(hip, ft, 24)
        P["fank"] = dn(P["fknee"], fs, 24)
    P["neck"] = add(hip, ax, 28)
    P["sh"] = add(hip, ax, 24.5)
    ha = torso if head is None else head
    P["head"] = up(P["neck"], ha, 9.5)
    if front:
        P["sh"] = add(hip, ax, 23.5)
        P["nsh"] = add(P["sh"], rp, -11.0 * sw)
        P["fsh"] = add(P["sh"], rp, 11.0 * sw)
    else:
        P["nsh"] = add(P["sh"], rp, -6.5 * tw)
        P["fsh"] = add(P["sh"], rp, 6.5 * tw)
    P["nelb"] = dn(P["nsh"], nu, 17 * nul)
    P["nhand"] = dn(P["nelb"], nf, 15 * nfl)
    P["felb"] = dn(P["fsh"], fu, 17 * ful)
    P["fhand"] = dn(P["felb"], ff, 15 * ffl)
    return P


def ik(hip, ank, bend=1, L1=24, L2=24):
    """股関節と足首の位置から (太もも角, すね角) を返す (dn 角度)。bend=+1 で膝が前。"""
    d = dist(hip, ank)
    d = min(d, L1 + L2 - 1e-3)
    a = math.atan2(ank[0] - hip[0], ank[1] - hip[1])      # dn 角度(ラジアン)
    c = (L1 * L1 + d * d - L2 * L2) / (2 * L1 * d)
    t = math.acos(max(-1, min(1, c)))
    th = a + bend * t
    knee = (hip[0] + L1 * math.sin(th), hip[1] + L1 * math.cos(th))
    sh = math.atan2(ank[0] - knee[0], ank[1] - knee[1])
    return math.degrees(th), math.degrees(sh)


# ---------------------------------------------------------------- body parts
def _shoe_geom(a, ang, front, shin_dir, heel=False):
    """returns (upper(p,q,r1,r2), sole(p,q,r1,r2), lowest_y, toe)"""
    if front:
        d = shin_dir
        n = (-d[1], d[0])
        c = add(a, d, 3.0)
        if heel:
            p, q = add(c, n, -3.0), add(c, n, 3.0)
            s1, s2 = add(add(c, n, -2.6), d, 3.6), add(add(c, n, 2.6), d, 3.6)
            return (p, q, 3.0, 3.0), (s1, s2, 1.2, 1.2), max(s1[1], s2[1]) + 1.2, c, add(c, d, 4.4)
        p, q = add(c, n, -4.0), add(c, n, 4.0)
        s1, s2 = add(p, d, 3.0), add(q, d, 3.0)
        low = max(s1[1], s2[1]) + 1.4
        return (p, q, 3.3, 3.3), (s1, s2, 1.4, 1.4), low, c, add(c, d, 4.4)
    d = (math.sin(math.radians(ang)), math.cos(math.radians(ang)))
    n = (-d[1], d[0])
    heel = add(add(a, d, -3.6), n, 2.4)
    toe = add(add(a, d, 9.2), n, 2.9)
    sh, st = add(heel, n, 2.7), add(toe, n, 2.1)
    low = max(sh[1], st[1]) + 1.45
    return (heel, toe, 3.5, 2.5), (sh, st, 1.45, 1.2), low, add(st, d, 1.5), add(lerp(sh, st, 0.74), n, 1.3)


MUSCLE_ALIAS = {"legs": ("quad", "glute", "calf"), "core": ("abs", "oblique"), "arms": ("tricep", "delt")}


def figP(hx, gy, nt=0, ns=0, ft=0, fs=0, torso=0, head=None, nu=0, nf=0, fu=0, ff=0,
         lift=0, nfoot=90, ffoot=90, front=False, hy=None, anchor=None, nb=0, fb=0, nfl=1.0, ffl=1.0,
         sw=1.0, nul=1.0, ful=1.0, nheel=False, fheel=False, tw=0.0, **kw):
    def build(x, y):
        P = pose(x, y, nt, ns, ft, fs, torso, head, nu, nf, fu, ff, front, nb, fb, nfl, ffl, sw, nul, ful, tw)
        lows = []
        for side, fa in (("n", nfoot), ("f", ffoot)):
            hh = nheel if side == "n" else fheel
            if hh and front:
                P[side + "ank"] = (P[side + "ank"][0], P[side + "ank"][1] - 4.5)
            sd = unit(P[side + "knee"], P[side + "ank"])
            g = _shoe_geom(P[side + "ank"], fa, front, sd, hh and front)
            if hh and front:
                g = (g[0], g[1], g[2] + 4.5, g[3], g[4])
            P[side + "shoe"] = g
            P[side + "toe"] = g[3]
            P[side + "ball"] = g[4]
            lows.append(g[2])
        return P, max(lows)
    if hy is None:
        P0, low = build(0, 0)
        base_y = gy - lift - low
    else:
        base_y = hy
    if anchor:
        name, axv = anchor[0], anchor[1]
        P0, _ = build(0, base_y)
        hx = axv - P0[name][0]
        if len(anchor) > 2:
            base_y += anchor[2] - P0[name][1]
    P, _ = build(hx, base_y)
    return P


def fig(hx, gy, nt=0, ns=0, ft=0, fs=0, torso=0, head=None, nu=0, nf=0, fu=0, ff=0,
        hl=(), lift=0, nfoot=90, ffoot=90, racket=None, front=False, hy=None,
        anchor=None, ball=False, look=0, nb=0, fb=0, nfl=1.0, ffl=1.0, shadow=True,
        flip=False, hand_n=True, hand_f=True, hls="nf", nha=None, fha=None, pre_narm=None,
        sw=1.0, nul=1.0, ful=1.0, post=None, nheel=False, fheel=False, tw=0.0, far_arm_front=False,
        racket_behind=False, fpoint=False):
    P = figP(hx, gy, nt, ns, ft, fs, torso, head, nu, nf, fu, ff, lift, nfoot, ffoot, front, hy, anchor, nb, fb, nfl, ffl,
             sw, nul, ful, nheel, fheel, tw)
    hip, ax, rp = P["hip"], P["ax"], P["rp"]
    ms = set()
    for h in hl:
        ms |= set(MUSCLE_ALIAS.get(h, (h,)))
    out = []

    # ---- ground shadow
    if shadow and hy is None:
        lo = min(P["nank"][0], P["fank"][0]) - 6
        hi = max(P["nank"][0], P["fank"][0]) + 10
        sc = max(0.35, 1 - lift / 40.0)          # 高く跳ぶほど影は小さく薄く
        op = 0.13 * sc
        out.append(f'<ellipse cx="{f((lo+hi)/2)}" cy="{f(gy+1.2)}" rx="{f(((hi-lo)/2+6)*sc)}" ry="{f(2.6*sc)}" fill="#1b2a44" fill-opacity="{op:.3f}"/>')
        for sd in ("n", "f"):
            g = P[sd + "shoe"]
            if g[2] >= gy - 0.8:                  # 接地している足には接地影
                so = g[1]
                cxs = (so[0][0] + so[1][0]) / 2
                hw = abs(so[1][0] - so[0][0]) / 2 + 2.5
                out.append(f'<ellipse cx="{f(cxs)}" cy="{f(gy+0.6)}" rx="{f(hw)}" ry="1.5" fill="#1b2a44" fill-opacity=".28"/>')

    def leg_layer(side, dark):
        L = Layer()
        hj, kn, an = P[side + "hipj"], P[side + "knee"], P[side + "ank"]
        sk = SKIN_D if dark else SKIN
        W = 1.0
        L.cap(hj, kn, 6.5 * W, 4.8 * W, sk)
        t, s_ = unit(hj, kn), unit(kn, an)
        # thigh front bulge / calf bulge
        tp = (-t[1], t[0])
        dif = (s_[0] - t[0], s_[1] - t[1])
        if not front:
            fpv = tp if (tp[0] * dif[0] + tp[1] * dif[1]) < 0 else (-tp[0], -tp[1])
            if math.hypot(*dif) < 0.15:
                fd = (math.sin(math.radians(nfoot if side == "n" else ffoot)), 0)
                fpv = tp if tp[0] * fd[0] >= 0 else (-tp[0], -tp[1])
            P[side + "tfront"] = fpv
            L.ell(add(lerp(hj, kn, 0.5), fpv, 1.2), dist(hj, kn) * 0.42, 5.4, ang_of(t), sk)
            fa = nfoot if side == "n" else ffoot
            fd = (math.sin(math.radians(fa)), math.cos(math.radians(fa)))
            sp = (-s_[1], s_[0])
            comp = fd[0] * sp[0] + fd[1] * sp[1]
            if abs(comp) > 0.3:
                cside = sp if comp < 0 else (-sp[0], -sp[1])
            else:
                # 足が脛と平行(つま先伸ばし) -> 足裏側がふくらはぎ
                cside = (-fd[1], fd[0])
            P[side + "cside"] = cside
            L.ell(add(lerp(kn, an, 0.3), cside, 1.5), dist(kn, an) * 0.3, 3.9, ang_of(s_), sk)
        else:
            L.ell(lerp(hj, kn, 0.45), max(dist(hj, kn) * 0.42, 5.6), 6.2, ang_of(t), sk)
            L.ell(lerp(kn, an, 0.3), dist(kn, an) * 0.3, 4.4, ang_of(s_), sk)
        L.cap(kn, an, 4.6 * W, 3.0 * W, sk)
        L.circ(kn, 5.0, sk)                      # 膝の継ぎ目をなめらかに
        up_, so = P[side + "shoe"][0], P[side + "shoe"][1]
        L.cap(*up_, SHOE_D if dark else SHOE)
        L.cap(*so, SOLE_D if dark else SOLE)
        # shorts leg
        L2 = Layer()
        L2.cap(hj, lerp(hj, kn, 0.44), 7.2, 6.3, SHORT_D if dark else SHORT)
        ow = 0.75 if dark else 1.1
        return L.render(ow) + L2.render(ow)

    def leg_muscles(side, op):
        s = ""
        if side not in hls:
            return s
        hj, kn, an = P[side + "hipj"], P[side + "knee"], P[side + "ank"]
        t, s_ = unit(hj, kn), unit(kn, an)
        lt, ls_ = dist(hj, kn), dist(kn, an)
        if front:
            if "quad" in ms:
                s += muscle(lerp(hj, kn, 0.58), max(lt * 0.4, 6.4), 3.5, ang_of(t), op)
            if "calf" in ms:
                s += muscle(lerp(kn, an, 0.33), ls_ * 0.27, 2.8, ang_of(s_), op)
            return s
        fpv = P[side + "tfront"]
        if "quad" in ms:
            s += muscle(add(lerp(hj, kn, 0.56), fpv, 1.5), lt * 0.37, 3.0, ang_of(t), op)
        if "ham" in ms:
            s += muscle(add(lerp(hj, kn, 0.56), fpv, -1.6), lt * 0.37, 3.0, ang_of(t), op)
        if "calf" in ms:
            s += muscle(add(lerp(kn, an, 0.31), P[side + "cside"], 1.7), ls_ * 0.27, 2.5, ang_of(s_), op)
        return s

    def arm_layer(side, dark):
        L = Layer()
        sh, el, ha = P[side + "sh"], P[side + "elb"], P[side + "hand"]
        sk = SKIN_D if dark else SKIN
        sc = SHIRT_D if dark else SHIRT
        L.cap(sh, el, 3.9, 3.2, sk)
        L.cap(el, ha, 3.2, 2.5, sk)
        L.circ(el, 3.3, sk)
        crease = ""
        if (side == "n" and hand_n) or (side == "f" and hand_f):
            d = unit(el, ha)
            hang = nha if side == "n" else fha
            if hang is not None:
                d = (math.sin(math.radians(hang)), math.cos(math.radians(hang)))
            pp = (-d[1], d[0])
            if pp[0] - pp[1] < 0:
                pp = (-pp[0], -pp[1])
            if side == "f" and fpoint:
                # 開いた手で指さす: 手のひら + 伸ばした人さし指
                L.ell(add(ha, d, 3.4), 4.2, 2.6, ang_of(d), sk)
                L.cap(add(ha, d, 6.0), add(ha, d, 11.5), 1.3, 1.0, sk)
                L.cap(add(add(ha, d, 1.4), pp, 2.0), add(add(ha, d, 4.4), pp, 3.6), 1.3, 1.1, sk)
            else:
                L.ell(add(ha, d, 3.2), 3.9, 2.9, ang_of(d), sk)
                L.cap(add(add(ha, d, 1.2), pp, 2.2), add(add(ha, d, 4.6), pp, 3.9), 1.6, 1.3, sk)   # thumb
            a_ = add(add(ha, d, 1.6), pp, 1.2)
            b_ = add(add(ha, d, 4.2), pp, 2.0)
            crease = line(a_, b_, SKIN_D if not dark else "#a87e5e", 0.7)
        ow = 0.75 if dark else 1.1
        L2 = Layer()
        if front:
            # 正面図: 三角筋を小さく・袖口の線を1本
            L2.circ(sh, 3.4, sc)
            L2.cap(sh, lerp(sh, el, 0.42), 4.0, 3.7, sc)
            cu = lerp(sh, el, 0.42)
            uu = unit(sh, el)
            nn = (-uu[1], uu[0])
            cuff = line(add(cu, nn, 3.9), add(cu, nn, -3.9), OUT, 1.0)
            return L.render(ow) + crease + L2.render(outline=False) + cuff
        L2.circ(sh, 4.4, sc)
        L2.cap(sh, lerp(sh, el, 0.44), 4.4, 4.0, sc)
        return L.render(ow) + crease + L2.render(ow)

    def arm_muscles(side, op):
        s = ""
        if side not in hls:
            return s
        sh, el, ha = P[side + "sh"], P[side + "elb"], P[side + "hand"]
        u = unit(sh, el)
        if "delt" in ms:
            s += muscle(lerp(sh, el, 0.2), 5.0, 2.6, ang_of(u), op)
        if "tricep" in ms:
            s += muscle(lerp(sh, el, 0.64), dist(sh, el) * 0.3, 2.2, ang_of(u), op)
        if "forearm" in ms:
            v = unit(el, ha)
            s += muscle(lerp(el, ha, 0.42), dist(el, ha) * 0.36, 2.0, ang_of(v), op)
        return s

    def torso_layer():
        L = Layer()
        L2 = Layer()
        if front:
            pel, wai, che = add(hip, ax, 2.0), add(hip, ax, 11), add(hip, ax, 19.5)
            Lp = Layer()
            Lp.circ(add(hip, ax, 1.0), 9.8, SHORT)
            Lp.cap(add(hip, ax, 1.0), add(hip, ax, 5.0), 9.8, 9.2, SHORT)
            # shirt : 肩幅広く腰で絞った台形シルエット
            T = lambda a_, r_: add(add(hip, ax, a_), rp, r_)
            ssw = max(abs(dist(P["nsh"], P["fsh"])) / 2, 6.0)
            pts = [T(4.0, -9.6), T(11.0, -8.6), T(17.0, -ssw + 0.4), T(24.5, -ssw - 1.0), T(27.0, -ssw + 2.5),
                   T(28.2, -3.4), T(28.2, 3.4), T(27.0, ssw - 2.5), T(24.5, ssw + 1.0), T(17.0, ssw - 0.4),
                   T(11.0, 8.6), T(4.0, 9.6)]
            L.poly(pts, TORSO_SH)
            inner = [T(4.6, -7.2), T(11.0, -6.6), T(17.5, -ssw + 3.4), T(25.0, -ssw + 4.6), T(27.2, -3.2),
                     T(27.2, 3.2), T(25.0, ssw - 4.6), T(17.5, ssw - 3.4), T(11.0, 6.6), T(4.6, 7.2)]
            L2.poly(inner, SHIRT)
            return Lp.render(), L.render() + L2.render(outline=False)
        Lp = Layer()
        Lp.circ(add(add(hip, ax, 1.0), rp, -0.4), 8.4, SHORT)
        Lp.cap(add(add(hip, ax, 1.0), rp, -0.4), add(hip, ax, 6.0), 8.4, 7.6, SHORT)
        pel = add(add(hip, ax, 6.0), rp, -0.2)
        wai = add(add(hip, ax, 11.0), rp, 0.3)
        che = add(add(hip, ax, 19.0), rp, 1.6)
        L.cap(pel, wai, 7.9, 7.3, TORSO_SH)
        L.cap(wai, che, 7.3, 9.4, TORSO_SH)
        L.cap(che, add(hip, ax, 25.5), 9.4, 5.5, TORSO_SH)
        L2.cap(add(pel, rp, 1.5), add(wai, rp, 1.5), 6.3, 5.8, SHIRT)
        L2.cap(add(wai, rp, 1.5), add(che, rp, 1.6), 5.8, 7.8, SHIRT)
        return Lp.render(), L.render() + L2.render(outline=False)

    def core_muscles():
        s = ""
        A = ang_of(ax)
        if front:
            if "abs" in ms and "oblique" in ms:
                s += muscle(add(hip, ax, 12.0), 8.4, 4.6, A)
            elif "abs" in ms:
                s += muscle(add(hip, ax, 12.0), 7.6, 4.0, A)
            elif "oblique" in ms:
                for k in (-6.6, 6.6):
                    s += muscle(add(add(hip, ax, 11.0), rp, k), 5.6, 2.4, A)
            if "chest" in ms:
                for k in (-4.8, 4.8):
                    s += muscle(add(add(hip, ax, 19.5), rp, k), 4.6, 2.4, 0)
            return s
        if "abs" in ms and "oblique" in ms:
            s += muscle(add(add(hip, ax, 11.5), rp, 2.6), 7.8, 3.6, A)
        elif "abs" in ms:
            s += muscle(add(add(hip, ax, 12.0), rp, 4.0), 7.4, 2.6, A)
        elif "oblique" in ms:
            s += muscle(add(add(hip, ax, 10.5), rp, 0.4), 6.6, 3.0, A)
        if "back" in ms:
            s += muscle(add(add(hip, ax, 12.5), rp, -4.8), 7.6, 2.4, A)
        if "chest" in ms:
            s += muscle(add(add(hip, ax, 19.5), rp, 5.6), 4.8, 2.5, A)
        if "glute" in ms:
            s += muscle(add(add(hip, ax, 1.0), rp, -5.0), 5.4, 2.8, A + 8)
        return s

    def neck_head():
        L = Layer()
        ha = torso if head is None else head
        L.cap(P["neck"], up(P["neck"], ha, 4.5), 3.3, 3.3, SKIN)
        return L.render() + head_layer(P["head"], ha + look, front, flip)

    def racket_svg():
        if racket is None:
            return ""
        h = P["nhand"]
        g0, g1 = up(h, racket, -3), up(h, racket, 8)
        tip = up(h, racket, 21)
        c = up(h, racket, 32.5)
        s = line(g0, g1, OUT, 5.2) + line(g0, g1, "#3d4452", 3.6) + line(g1, tip, OUT, 2.4) + line(g1, tip, "#c5ccd6", 1.2)
        s += f'<ellipse cx="{f(c[0])}" cy="{f(c[1])}" rx="7.2" ry="11.6" transform="rotate({racket} {f(c[0])} {f(c[1])})" fill="#ffffff" fill-opacity="0.6" stroke="{OUT}" stroke-width="2.2"/>'
        g = f'<g transform="rotate({racket} {f(c[0])} {f(c[1])})" stroke="#3d4452" stroke-opacity="0.4" stroke-width="0.6">'
        for k in (-4.5, -1.5, 1.5, 4.5):
            g += f'<line x1="{f(c[0]+k)}" y1="{f(c[1]-10.5)}" x2="{f(c[0]+k)}" y2="{f(c[1]+10.5)}"/>'
        for k in (-7, -3.5, 0, 3.5, 7):
            g += f'<line x1="{f(c[0]-6.4)}" y1="{f(c[1]+k)}" x2="{f(c[0]+6.4)}" y2="{f(c[1]+k)}"/>'
        P["rtip"] = up(h, racket, 44.5)
        P["rcen"] = c
        CHK["tips"].append(P["rtip"])
        CHK["pts"].append((c[0], c[1], 9))
        return s + g + "</g>"

    def ball_svg():
        if not ball:
            return ""
        mid = lerp(P["nhand"], P["fhand"], 0.5)
        bx, by = mid[0], mid[1] - (0 if front else 2)
        P["ball"] = (bx, by)
        CHK["pts"].append((bx, by, 8))
        return med_ball(bx, by)

    if front:
        out.append(leg_layer("f", False))
        out.append(leg_layer("n", False))
        pel, tor = torso_layer()
        out.append(pel)
        out.append(leg_muscles("f", 0.66) + leg_muscles("n", 0.66))
        out.append(tor)
        out.append(core_muscles())
        out.append(neck_head())
        out.append(ball_svg())
        if pre_narm:
            out.append(pre_narm(P))
        out.append(arm_layer("f", False) + arm_muscles("f", 0.66))
        out.append(arm_layer("n", False) + arm_muscles("n", 0.66))
        out.append(racket_svg())
    else:
        if not far_arm_front:
            out.append(arm_layer("f", True) + arm_muscles("f", 0.5))
        out.append(leg_layer("f", True) + leg_muscles("f", 0.5))
        out.append(leg_layer("n", False))
        if racket_behind:
            out.append(racket_svg())         # 背中側に落ちたラケット(胴体の奥)
        pel, tor = torso_layer()
        out.append(pel)
        out.append(leg_muscles("n", 0.66))
        out.append(tor)
        out.append(core_muscles())
        out.append(neck_head())
        if far_arm_front:
            out.append(arm_layer("f", True) + arm_muscles("f", 0.5))
        out.append(ball_svg())
        if pre_narm:
            out.append(pre_narm(P))
        out.append(arm_layer("n", False) + arm_muscles("n", 0.66))
        if not racket_behind:
            out.append(racket_svg())
    if post:
        out.append(post(P))

    # register body points for the overlap check
    for k, r in (("head", 9.5), ("neck", 5), ("sh", 7), ("hip", 8), ("nknee", 5), ("fknee", 5),
                 ("nank", 4), ("fank", 4), ("nelb", 4), ("felb", 4), ("nhand", 4), ("fhand", 4),
                 ("ntoe", 3), ("ftoe", 3)):
        CHK["pts"].append((P[k][0], P[k][1], r))
    for a_, b_ in (("hip", "nknee"), ("nknee", "nank"), ("hip", "fknee"), ("fknee", "fank"), ("hip", "neck"),
                   ("nsh", "nelb"), ("nelb", "nhand"), ("fsh", "felb"), ("felb", "fhand")):
        for i in range(1, 4):
            q = lerp(P[a_], P[b_], i / 4)
            CHK["pts"].append((q[0], q[1], 4.5))
    return "".join(out), P


# ---------------------------------------------------------------- props
def med_ball(x, y, r=8):
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r+1.1)}" fill="{OUT}" fill-opacity=".9"/>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{BALL}"/>'
            f'<path d="M{f(x-r)},{f(y)} Q{f(x)},{f(y+r*0.55)} {f(x+r)},{f(y)}" fill="none" stroke="#e9dccf" stroke-width="1" stroke-opacity=".7"/>'
            f'<path d="M{f(x)},{f(y-r)} Q{f(x-r*0.5)},{f(y)} {f(x)},{f(y+r)}" fill="none" stroke="#e9dccf" stroke-width="1" stroke-opacity=".7"/>'
            f'<circle cx="{f(x-r*0.35)}" cy="{f(y-r*0.38)}" r="{f(r*0.22)}" fill="#fff" fill-opacity=".35"/>')


def shuttle(x, y, ang, s=1.0):
    """本物らしいシャトル。(x,y)=コルク先端, ang=進行方向(度, 0=右, 90=下)。コルクが先頭。"""
    a = math.radians(ang)
    d = (math.cos(a), math.sin(a))
    n = (-d[1], d[0])
    P = lambda u, v: (x + (d[0] * u + n[0] * v) * s, y + (d[1] * u + n[1] * v) * s)
    cork_c = P(-3.0, 0)
    skirt = [P(-4.6, -3.0), P(-17, -7.0), P(-17, 7.0), P(-4.6, 3.0)]
    o = f'<polygon points="{_poly(skirt)}" fill="#ffffff" stroke="{OUT}" stroke-width="1.3" stroke-linejoin="round"/>'
    for v in (-4.6, -1.6, 1.6, 4.6):
        o += line(P(-5.0, v * 0.42), P(-16.6, v), "#9aa5b5", 0.6)
    o += line(P(-9.5, -4.8), P(-9.5, 4.8), "#9aa5b5", 0.8)
    o += line(P(-4.8, -3.1), P(-4.8, 3.1), OUT, 1.6)
    o += (f'<circle cx="{f(cork_c[0])}" cy="{f(cork_c[1])}" r="{f(3.2*s)}" fill="#f1e3c8" stroke="{OUT}" stroke-width="1.3"/>')
    CHK["pts"].append((cork_c[0], cork_c[1], 4))
    CHK["tips"].append(P(-17, 7.0))
    CHK["tips"].append(P(-17, -7.0))
    CHK["tips"].append(P(0.5, 0))
    return o


def svg(inner, vb="0 0 170 150", wpx=200):
    x, y, w, h = [float(v) for v in vb.split()]
    hpx = wpx * h / w
    bg = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#f4f7fb"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{wpx}" height="{f(hpx)}" viewBox="{vb}" '
            f'style="border-radius:9px;overflow:hidden">'
            f'<g>{bg}{inner}</g></svg>')


def prop_rect(x, y, w, h, fill="#c9b79c", stroke="#8a6d3b", sw=1.5, rx=2):
    """家具・台など(ラベル重なりチェック対象)"""
    obst(x, y, w, h)
    return rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, rx=rx)


def wall(x, y1, y2):
    obst(x, y1, 10, y2 - y1)
    s = rect(x, y1, 10, y2 - y1, fill="#e9ecef", stroke=GRD, sw=1.5, rx=0)
    for yy in range(int(y1) + 6, int(y2), 10):
        s += line((x + 10, yy), (x + 3, yy + 6), GRD, 1)
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
    # net
    s.append(line((x0 - 8, y0), (x0 + W + 8, y0), "#444", 4, cap="butt"))
    for k in range(0, int(W) + 16, 8):
        s.append(line((x0 - 8 + k, y0 - 2), (x0 - 8 + k, y0 + 2), "#ffffff", 1))
    s.append(text(x0 + W / 2, y0 - 8, "ネット", 10, "#444"))
    base = (x0 + W / 2, y0 + 3.4 * sc)
    pts = [("1", x0 + W - 26, y0 + 28), ("2", x0 + 26, y0 + 28),
           ("3", x0 + W - 22, base[1]), ("4", x0 + 22, base[1]),
           ("5", x0 + W - 26, y0 + L - 22), ("6", x0 + 26, y0 + L - 22)]
    for n, px, py in pts:
        dx, dy = px - base[0], py - base[1]
        d = math.hypot(dx, dy)
        ex, ey = px - dx / d * 14, py - dy / d * 14
        sx, sy = base[0] + dx / d * 12, base[1] + dy / d * 12
        s.append(arrow(sx, sy, ex, ey, MOV, 2.0, dash="5,3"))
    for n, px, py in pts:
        s.append(circle(px, py, 11, "#ffffff", MOV, 2.2))
        s.append(text(px, py + 4, n, 12, MOV))
    # player (top view)
    bx, by = base
    s.append(f'<ellipse cx="{f(bx)}" cy="{f(by)}" rx="11" ry="6.5" fill="{SHIRT}" stroke="{OUT}" stroke-width="1.2"/>')
    s.append(f'<circle cx="{f(bx)}" cy="{f(by)}" r="4.6" fill="{HAIR}" stroke="{OUT}" stroke-width="1"/>')
    s.append(rect(bx - 19, by + 15, 38, 15, fill="#ffffff", stroke=NAVY, sw=1, rx=6))
    s.append(text(bx, by + 26.5, "ホーム", 10, NAVY))
    vb = f"0 0 {x0*2 + W:.0f} {y0 + L + 10:.0f}"
    return svg("".join(s), vb, wpx)


def cross_svg(wpx=200):
    s = []
    cx, cy = 85, 76
    s.append(rect(10, 10, 150, 132, fill="#eef1f5", stroke="#ced4da", sw=1.2, rx=6))
    s.append(line((cx - 58, cy), (cx + 58, cy), "#adb5bd", 3, cap="butt", dash="2,4"))
    s.append(line((cx, cy - 56), (cx, cy + 56), "#adb5bd", 3, cap="butt", dash="2,4"))
    for (dx, dy) in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        s.append(arrow(cx + dx * 16, cy + dy * 16, cx + dx * 44, cy + dy * 44, MOV, 2.2))
    for (px, py, n) in [(cx, cy - 56, "1"), (cx + 58, cy, "2"), (cx, cy + 56, "3"), (cx - 58, cy, "4")]:
        s.append(rect(px - 11, py - 11, 22, 22, "#ffffff", MOV, 2.2, rx=4))
        s.append(text(px, py + 4, n, 12, MOV))
    # player top view (feet + body)
    s.append(f'<ellipse cx="{cx-5}" cy="{cy+4}" rx="3" ry="5" fill="#ffffff" stroke="{OUT}" stroke-width="1"/>')
    s.append(f'<ellipse cx="{cx+5}" cy="{cy+4}" rx="3" ry="5" fill="#ffffff" stroke="{OUT}" stroke-width="1"/>')
    s.append(f'<ellipse cx="{cx}" cy="{cy}" rx="11" ry="6.5" fill="{SHIRT}" stroke="{OUT}" stroke-width="1.2"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="4.6" fill="{HAIR}" stroke="{OUT}" stroke-width="1"/>')
    s.append(text(85, 158, "中央 → 番号へタッチ → 中央へ戻る", 9.5, NAVY))
    return svg("".join(s), "0 0 170 165", wpx)


# ---------------------------------------------------------------- top view (真上から見た図)
def _rv(v, a):
    c, s_ = math.cos(math.radians(a)), math.sin(math.radians(a))
    return (v[0] * c - v[1] * s_, v[0] * s_ + v[1] * c)


def _ik2(p, q, L1, L2, out_dir):
    d = min(dist(p, q), L1 + L2 - 0.01)
    u = unit(p, q)
    a = (L1 * L1 + d * d - L2 * L2) / (2 * d)
    h = math.sqrt(max(L1 * L1 - a * a, 0))
    n = (-u[1], u[0])
    if n[0] * out_dir[0] + n[1] * out_dir[1] < 0:
        n = (-n[0], -n[1])
    return add(add(p, u, a), n, h)


def top_person(cx, cy, sh_ang=0.0, hip_ang=0.0, hands=None, feet=((0, False), (0, False)), head_ang=None,
               hl=(), k=1.6, lines=True, elbows=None, line_side=-1):
    """真上から見た人物。体は上(-y)を向く。角度は時計回り(度)。k=拡大率。
    hands = (右手, 左手) の絶対座標。右 = +x 側。feet = ((右足の向き, かかと上げ), (左足…))"""
    s = []
    C = (cx, cy)
    L = Layer()
    laces = ""
    for sgn, (fa, heel) in zip((1, -1), feet):
        fc = (cx + 12.0 * k * sgn, cy - 3.0 * k)
        d = _rv((0, -1), fa)
        sc_ = add(fc, d, 2.0 * k)
        s.append(f'<ellipse cx="{f(sc_[0]+1.5)}" cy="{f(sc_[1]+2)}" rx="{f(4.4*k)}" ry="{f(8.2*k)}" transform="rotate({f(fa)} {f(sc_[0]+1.5)} {f(sc_[1]+2)})" fill="#1b2a44" fill-opacity=".12"/>')
    for sgn, (fa, heel) in zip((1, -1), feet):
        fc = (cx + 12.0 * k * sgn, cy - 3.0 * k)
        d = _rv((0, -1), fa)
        heel_p, toe_p = add(fc, d, -3.6 * k), add(fc, d, 7.4 * k)
        if heel:
            # かかとを上げた足: つま先側だけ接地(かかと側は薄く)
            L.cap(add(fc, d, 2.0 * k), toe_p, 2.3 * k, 2.5 * k, SHOE)
            hb = add(fc, d, -1.5 * k)
            laces += (f'<ellipse cx="{f(hb[0])}" cy="{f(hb[1])}" rx="{f(2.8*k)}" ry="{f(4.0*k)}" transform="rotate({f(fa)} {f(hb[0])} {f(hb[1])})" '
                      f'fill="none" stroke="{OUT}" stroke-width="1" stroke-dasharray="2,2" stroke-opacity=".4"/>')
        else:
            L.cap(heel_p, toe_p, 2.0 * k, 2.5 * k, SHOE)
        laces += line(add(fc, d, 1.0 * k), add(fc, d, 6.5 * k), "#9aa5b5", 1.2)
    s.append(L.render() + laces)
    L = Layer()
    L.ell(C, 11.0 * k, 6.6 * k, hip_ang, SHORT)
    s.append(L.render())
    info = {}

    def axis_line(ang, dash, lab, ext, side, col, tag_ext, back=0.0):
        """肩/腰ラインとラベル。両方とも同じ端(side)にラベルを付ける"""
        off = _rv((0, back * k), ang)
        a = add(add(C, off), _rv((-ext * k, 0), ang))
        b = add(add(C, off), _rv((ext * k, 0), ang))
        wdt = 3.4 if lab == "肩" else 1.8
        o = line(a, b, "#ffffff", wdt + 1.8, dash) + line(a, b, col, wdt, dash)
        tp = add(add(C, off), _rv((side * tag_ext * k, 0), ang))
        le = add(add(C, off), _rv((side * ext * k, 0), ang))
        if dist(le, tp) > 8:
            o += line(le, add(le, unit(le, tp), dist(le, tp) - 7.6), col, 1.0)
        o += (f'<circle cx="{f(tp[0])}" cy="{f(tp[1])}" r="7.6" fill="#ffffff" stroke="{col}" stroke-width="1.4"/>'
              + text(tp[0], tp[1] + 3.6, lab, 10, col))
        CHK["pts"].append((tp[0], tp[1], 7.6))
        info[lab] = (a, b)
        return o
    if lines:
        extra = 16.5 / k if abs(sh_ang - hip_ang) < 15 else 0.0
        s.append(axis_line(hip_ang, "5,3", "腰", 33, line_side, "#d9480f", 37 + extra, 2.5))
    shs = [add(C, _rv((sgn * 13.0 * k, 0), sh_ang)) for sgn in (1, -1)]
    fwd = _rv((0, -1), sh_ang)
    arms, sleeves = Layer(), Layer()
    if hands:
        for i, (sgn, sh, hd) in enumerate(zip((1, -1), shs, hands)):
            outd = _rv((sgn, 0), sh_ang)
            el = elbows[i] if (elbows and elbows[i]) else _ik2(sh, hd, 12.5 * k, 12.0 * k, outd)
            skc = SKIN if sgn > 0 else SKIN_D         # 奥(左)の腕は一段暗く
            arms.cap(sh, el, 3.6 * k, 3.0 * k, skc)
            arms.cap(el, hd, 3.0 * k, 2.5 * k, skc)
            arms.circ(el, 3.0 * k, skc)
            arms.circ(hd, 3.3 * k, skc)
            short = dist(sh, el) < 6 * k
            sleeves.cap(sh, lerp(sh, el, 0.42), (3.4 if short else 4.1) * k, (3.1 if short else 3.7) * k,
                        SHIRT if sgn > 0 else SHIRT_D)
            CHK["pts"] += [(el[0], el[1], 4 * k), (hd[0], hd[1], 4 * k)]
    L = Layer()
    L.cap(shs[0], shs[1], 6.4 * k, 6.4 * k, SHIRT)
    s.append(L.render())
    if "oblique" in hl or "abs" in hl:
        s.append(muscle(add(C, fwd, -0.4 * k), 11.0 * k, 4.6 * k, (sh_ang + hip_ang) / 2, 0.62))
    s.append(arms.render() + sleeves.render())
    ha = sh_ang if head_ang is None else head_ang
    hd_ = _rv((0, -1), ha)
    Lh = Layer()
    nn = (-hd_[1], hd_[0])
    Lh.poly([add(add(C, hd_, 5.6 * k), nn, 1.8 * k), add(C, hd_, 8.6 * k), add(add(C, hd_, 5.6 * k), nn, -1.8 * k)], SKIN)
    Lh.circ(C, 6.3 * k, HAIR)
    s.append(Lh.render())
    if lines:
        s.append(axis_line(sh_ang, None, "肩", 35, line_side, NAVY, 39))
    info.update({"sh": shs, "fwd": fwd})
    CHK["pts"] += [(cx, cy, 12 * k), (shs[0][0], shs[0][1], 6 * k), (shs[1][0], shs[1][1], 6 * k)]
    return "".join(s), info
