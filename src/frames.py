from figlib import *
import inspect

GY = 130
VB = "0 0 170 150"
WARN = []          # 自動チェックの警告 (はみ出し・重なり)
_cnt = {}


# ===================== 自動チェック =====================
def _check(vb, tag):
    x0, y0, w, h = [float(v) for v in vb.split()]
    x1, y1 = x0 + w, y0 + h
    m = 4
    out = []
    rects = CHK["rects"]
    CLR = 8          # ラベルと人物・用具の最小すき間
    for (rx, ry, rw, rh, s) in rects:
        if s == "使う部位":
            if ry < GY + 1:
                out.append("legend must sit in the grey band below the floor line")
            if rx < x0 + m - 0.01 or rx + rw > x1 - m + 0.01 or ry + rh > y1 - m + 0.01:
                out.append("legend out of frame")
            continue
        if rx < x0 + m - 0.01 or ry < y0 + m - 0.01 or rx + rw > x1 - m + 0.01 or ry + rh > y1 - m + 0.01:
            out.append(f"badge out of frame: {s} ({rx:.0f},{ry:.0f},{rw:.0f},{rh:.0f})")
        for (px, py, r) in CHK["pts"]:
            cx = min(max(px, rx), rx + rw)
            cy = min(max(py, ry), ry + rh)
            if math.hypot(px - cx, py - cy) < r + CLR - 0.3:
                out.append(f"badge '{s}' too close to body/racket point ({px:.0f},{py:.0f})")
                break
    for (rx, ry, rw, rh, s) in rects:
        if s == "使う部位":
            continue
        for (ox, oy, ow, oh) in CHK["obst"]:
            if rx < ox + ow + CLR and ox - CLR < rx + rw and ry < oy + oh + CLR and oy - CLR < ry + rh:
                out.append(f"badge '{s}' overlaps prop/wall ({ox:.0f},{oy:.0f})")
                break
        for (px, py) in CHK["apts"]:
            if rx - 1.5 < px < rx + rw + 1.5 and ry - 1.5 < py < ry + rh + 1.5:
                out.append(f"badge '{s}' overlaps arrow ({px:.0f},{py:.0f})")
                break
    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            a, b = rects[i], rects[j]
            if a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]:
                out.append(f"badges overlap: {a[4]} / {b[4]}")
    for (px, py) in CHK["tips"]:
        if px < x0 + m or py < y0 + m or px > x1 - m or py > y1 - m:
            out.append(f"racket/shuttle tip out of frame ({px:.0f},{py:.0f})")
    for (px, py) in CHK["arrows"]:
        if px < x0 + 3 or py < y0 + 3 or px > x1 - 3 or py > y1 - 3:
            out.append(f"arrow end out of frame ({px:.0f},{py:.0f})")
    for (px, py, r) in CHK["pts"]:
        mm = max(2, r * 0.8)
        if px < x0 + mm or py < y0 + mm or px > x1 - mm or py > y1 - mm:
            out.append(f"body point out of frame ({px:.0f},{py:.0f})")
    for o in out:
        WARN.append(f"[{tag}] {o}")
    chk_reset()


def S(inner, vb=VB, w=185):
    fn = inspect.stack()[1].function
    if fn in ("make", "<listcomp>", "fr"):
        fn = inspect.stack()[2].function
    _cnt[fn] = _cnt.get(fn, 0) + 1
    _check(vb, f"{fn}#{_cnt[fn]}")
    return svg(inner, vb, w)


def ghost(**kw):
    """前のコマの残像(薄く)。チェック対象には含めない"""
    n = {k: len(v) for k, v in CHK.items()}
    s, P = fig(shadow=False, **kw)
    for k in CHK:
        del CHK[k][n[k]:]
    return f'<g opacity=".18">{s}</g>', P


def solve(fn, lo, hi, it=40):
    """fn(lo) と fn(hi) の符号が異なる区間で根を求める(二分法)"""
    flo = fn(lo)
    for _ in range(it):
        mid = (lo + hi) / 2
        fm = fn(mid)
        if (fm < 0) == (flo < 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def ik_knee(hip, ank, forward=True):
    a1 = ik(hip, ank, 1)
    a2 = ik(hip, ank, -1)
    k1 = dn(hip, a1[0], 24)
    k2 = dn(hip, a2[0], 24)
    if forward:
        return a1 if k1[0] >= k2[0] else a2
    return a1 if k1[1] >= k2[1] else a2       # 膝を下へ


from figlib import _tw, _rv


def LG(vb, side="l"):
    """凡例は床線より下のグレー帯の左下に固定"""
    x0, y0, w, h = [float(v) for v in vb.split()]
    x = x0 + 7 if side == "l" else x0 + w - 7 - (_tw("使う部位", 9) + 16)
    return legend(x, GY + 16.5)


def guide_line(p, q, op=1.0, ext=8):
    """緑の点線基準線 (p→q を少し延長)"""
    a = add(p, unit(q, p), ext)
    b = add(q, unit(p, q), ext)
    return f'<g opacity="{op}">' + line(a, b, GRN, 1.4, dash="3,3") + "</g>"


def leader(bx, by, tx, ty, col=GRN):
    """ラベルから対象への引き出し線"""
    return line((bx, by), (tx, ty), col, 1.1) + circle(tx, ty, 1.8, col, col, 0.5)


# ===================== A. 脚(家) =====================
VBJ = "0 -18 170 172"
TOE = 40          # 空中でつま先を伸ばした足の角度


def jump_squat():
    res = []
    vb = set_vbx("8 -16 150 170")
    hl = ("quad", "glute")
    a, P = fig(64, GY, nt=50, ns=-24, ft=46, fs=-26, torso=30, nu=-62, nf=-46, fu=-56, ff=-40, hl=hl)
    f1 = ground(GY) + a + arrow(132, 44, 132, 86) + badge(132, 30, "浅く沈む") + LG(vb)
    res.append((S(f1, vb), "① 浅くしゃがむ<br>腕は後ろへ"))
    b, P = fig(70, GY, nt=2, ns=-2, ft=-4, fs=-2, torso=4, nu=186, nf=182, fu=176, ff=170, lift=16,
               nfoot=TOE, ffoot=TOE, hl=hl)
    f2 = ground(GY) + b + arrow(132, 114, 132, 56) + badge(128, 50, "真上へ")
    res.append((S(f2, vb), "② 腕を振り上げて<br>真上にジャンプ"))
    c, P = fig(60, GY, nt=56, ns=-26, ft=52, fs=-28, torso=32, nu=55, nf=82, fu=45, ff=76, hl=hl)
    f3 = ground(GY) + c + badge(120, 2, "静かに着地", GRN) + badge(118, 24, "膝はつま先の向き", GRN)
    res.append((S(f3, vb), "③ 膝を曲げて<br>音を立てず着地"))
    return res

def bulgarian():
    res = []
    vb = set_vbx("0 6 170 148")
    bench_top = 110
    rear = (28, bench_top - 1.6)
    front = (92, GY - 6.55)

    def bench():
        return (prop_rect(0, bench_top, 40, 6) +
                line((6, bench_top + 6), (6, GY), "#8a6d3b", 3) + line((34, bench_top + 6), (34, GY), "#8a6d3b", 3))

    def kw(hip, torso):
        nt, ns = ik_knee(hip, front, True)
        ft, fs = ik_knee(hip, rear, False)
        return dict(hx=hip[0], gy=GY, hy=hip[1], nt=nt, ns=ns, ft=ft, fs=fs, torso=torso, nu=12, nf=30, fu=8, ff=26,
                    ffoot=-97, nfoot=90)
    a, P = fig(hl=("quad", "glute"), hls="n", shadow=False, **kw((54, 88), 6))
    f1 = ground(GY) + bench() + a + LG(vb) + badge(124, 32, "前足は固定", GRN)
    res.append((S(f1, vb), "① 後ろ足の甲を台に<br>前足は大きく一歩前"))
    g, _ = ghost(**kw((54, 88), 6))
    b, P = fig(hl=("quad", "glute"), hls="n", shadow=False, **kw((52, 103), 10))
    f2 = (ground(GY) + bench() + g + b + arrow(136, 62, 136, 100) + badge(136, 50, "真下へ沈む") +
          badge(66, 22, "後ろ膝は床近く", GRN))
    res.append((S(f2, vb), "② 後ろ膝を床すれすれまで<br>真下へ下ろす"))
    return res


def pogo():
    res = []
    vb = set_vbx("6 -8 152 162")
    a, P = fig(52, GY, nt=6, ns=-4, ft=4, fs=-6, torso=4, nu=14, nf=40, fu=8, ff=34, nfoot=58, ffoot=58, hl=("calf",))
    bt = P["nball"]
    tick = "".join(line((bt[0] + dx * 2.2, GY - 2), (bt[0] + dx * 3.4, GY - 6), MOV, 1.4) for dx in (-3, 3))
    f1 = ground(GY) + a + tick + badge(112, 56, "接地は一瞬", GRN) + badge(114, 104, "かかと上げ", GRN) + LG(vb)
    res.append((S(f1, vb), "① つま先で着地し<br>すぐ床をはじく"))
    b, P = fig(52, GY, nt=0, ns=0, ft=-2, fs=-2, torso=2, nu=14, nf=40, fu=8, ff=34, lift=24,
               nfoot=32, ffoot=32, hl=("calf",))
    f2 = ground(GY) + b + arrow(118, 124, 118, 98) + badge(118, 84, "3〜5cm") + badge(114, 30, "膝は伸ばす", GRN)
    res.append((S(f2, vb), "② 膝は伸ばしたまま<br>足首のバネで小さく跳ぶ"))
    return res

def calf_raise():
    res = []
    vb = set_vbx("0 0 164 154")
    top = 112
    E = 96

    def make(foot):
        kw = dict(nt=-2, ns=0, ft=6, fs=-96, torso=2, nu=48, nf=78, fu=40, ff=70, nfoot=foot, ffoot=-50,
                  anchor=("nball", E + 1.5, top + 0.6))
        a, P = fig(0, GY, hl=("calf",), hls="n", shadow=False, **kw)
        wx = P["nhand"][0] + 6.5
        st = prop_rect(E, top, wx - E, GY - top)
        return st + wall(wx, 4, GY) + a, P
    a, P = make(130)
    hp = P["nshoe"][0][0]
    f1 = ground(GY) + a + LG(vb) + badge(30, 46, "かかと↓") + arrow(hp[0] - 12, hp[1] - 14, hp[0] - 12, hp[1] + 3) + line((20, top), (E, top), GRD, 1.2, dash="3,3")
    res.append((S(f1, vb), "① 片脚で、つま先だけ段の端に乗せ<br>かかとを段より下へ"))
    b, P = make(26)
    hp = P["nshoe"][0][0]
    f2 = ground(GY) + b + arrow(hp[0] - 12, hp[1] + 16, hp[0] - 12, hp[1] - 2) + line((20, top), (E, top), GRD, 1.2, dash="3,3") + badge(30, 40, "高く上げる")
    res.append((S(f2, vb), "② かかとを高く上げ<br>3秒かけて下ろす"))
    return res

def nordic():
    res = []
    vb = set_vbx("0 16 170 143")
    knee = (70, GY - 7.5)

    def sofa():
        s = prop_rect(2, 80, 50, 34, fill="#b8c4d6", stroke="#5b6b85", rx=5)
        s += prop_rect(2, 66, 14, 48, fill="#a6b4c9", stroke="#5b6b85", rx=4)
        s += line((10, 114), (10, GY), "#5b6b85", 3) + line((46, 114), (46, GY), "#5b6b85", 3)
        return s
    mat = rect(50, GY - 3, 50, 4, fill="#74c0fc", stroke="#4a8fc4", sw=1, rx=2)

    def kw(lean, **k):
        return dict(hx=0, gy=GY, nt=lean, ns=-90, ft=lean, fs=-90, torso=lean, head=lean + 4, ffoot=-92, nfoot=-92,
                    anchor=("nknee", knee[0], knee[1]), **k)
    a, P = fig(hl=("ham",), shadow=False, **kw(0, nu=24, nf=150, fu=18, ff=146))
    ank = P["nank"]
    ring = circle(ank[0] - 2, ank[1], 7, "none", GRN, 1.6)
    f1 = (ground(GY) + mat + a + sofa() + ring + line((ank[0] + 5, ank[1] + 4), (79, 139), GRN, 1.2) +
          badge(120, 150, "足首を固定", GRN) + LG(vb) + badge(124, 34, "膝〜頭が一直線", GRN) + guide_line(P["nknee"], P["head"], 0.9, 6))
    res.append((S(f1, vb), "① ひざ立ちになり<br>足首をソファの下に固定"))
    g, _ = ghost(**kw(0, nu=24, nf=150, fu=18, ff=146))
    b, P = fig(hl=("ham",), shadow=False, **kw(56, nu=70, nf=90, fu=64, ff=86))
    f2 = (ground(GY) + mat + g + b + sofa() + guide_line(P["nknee"], P["head"], 0.9, 6) +
          carrow(106, 60, 136, 58, 150, 90) + badge(122, 46, "ゆっくり倒れる"))
    res.append((S(f2, vb), "② 膝〜頭を一直線のまま<br>3〜5秒かけて前へ"))
    return res


# ===================== A. 脚(外) =====================
BOXTOP = 100


def box(x1, x2, top=BOXTOP):
    return (prop_rect(x1, top, x2 - x1, GY - top) +
            line((x1 + 4, top + 7), (x2 - 4, top + 7), "#8a6d3b", 1, op=.5))


def box_jump():
    res = []
    vb = set_vbx("0 -6 170 160")
    hl = ("quad", "glute")
    a, _ = fig(46, GY, nt=58, ns=-26, ft=54, fs=-28, torso=34, nu=-64, nf=-48, fu=-58, ff=-42, hl=hl)
    f1 = ground(GY) + box(104, 164) + a + LG(vb) + badge(130, 60, "腕を後ろへ")
    res.append((S(f1, vb), "① しゃがんで<br>腕を後ろへ"))
    b, _ = fig(96, BOXTOP, nt=96, ns=-6, ft=90, fs=-10, torso=16, nu=100, nf=128, fu=94, ff=122, lift=14,
               nfoot=70, ffoot=70, hl=hl, shadow=False)
    traj = f'<path d="M40,124 Q52,30 92,40" fill="none" stroke="{MOV}" stroke-width="1.6" stroke-dasharray="3,4" stroke-opacity=".7"/>'
    f2 = ground(GY) + box(104, 164) + traj + b + badge(34, 14, "膝を胸へ")
    res.append((S(f2, vb), "② 膝を引き上げ<br>両足で跳び乗る"))
    c, _ = fig(118, BOXTOP, nt=56, ns=-24, ft=52, fs=-26, torso=30, nu=58, nf=84, fu=50, ff=78, hl=hl)
    f3 = ground(GY) + box(104, 164) + c + badge(46, 40, "静かに乗る", GRN) + badge(50, 62, "降りは歩いて", GRN)
    res.append((S(f3, vb), "③ 台の上で静かに着地<br>降りるときは歩く"))
    return res


def depth_jump():
    res = []
    vb = set_vbx("0 -14 170 168")
    bx = box(4, 52)
    hl = ("quad", "calf")
    a, _ = fig(0, BOXTOP, nt=24, ns=6, ft=-4, fs=-4, torso=6, nu=18, nf=40, fu=12, ff=34, nfoot=100,
               anchor=("fank", 40), hl=hl)
    f1 = ground(GY) + bx + a + carrow(66, 66, 86, 70, 98, 104) + badge(120, 40, "踏み出すだけ") + LG(vb)
    res.append((S(f1, vb), "① 台の端に立ち<br>一歩踏み出して落ちる"))
    b, _ = fig(104, GY, nt=40, ns=-18, ft=36, fs=-20, torso=22, nu=-40, nf=-26, fu=-34, ff=-22, hl=hl)
    f2 = ground(GY) + bx + b + badge(40, 20, "接地は最短", GRN) + badge(40, 44, "浅く沈むだけ", GRN)
    res.append((S(f2, vb), "② 着地の瞬間<br>浅く沈むだけ"))
    c, _ = fig(98, GY, nt=2, ns=-2, ft=-4, fs=-2, torso=4, nu=186, nf=182, fu=176, ff=170, lift=20,
               nfoot=TOE, ffoot=TOE, hl=hl)
    f3 = ground(GY) + bx + c + arrow(152, 100, 152, 52) + badge(30, 80, "すぐ跳ぶ")
    res.append((S(f3, vb), "③ すぐに<br>全力でジャンプ"))
    return res


def sprint():
    res = []
    vb = set_vbx("0 -10 170 164")
    hl = ("glute", "ham")
    # 近い脚=前(膝を引き上げ) / 遠い脚=後ろで地面を押す / 近い腕=後ろ / 遠い腕=前。前傾は体の角度で表す
    a, _ = fig(92, GY, nt=72, ns=-22, ft=-34, fs=-50, torso=32, head=24, nu=-64, nf=-30, fu=58, ff=150,
               nfoot=96, ffoot=-12, hl=hl)
    f1 = ground(GY) + a + badge(64, 12, "後ろ脚で地面を押す", GRN) + LG(vb)
    res.append((S(f1, vb), "① 体ごと前傾して<br>後ろ脚で地面を強く押す"))
    b, _ = fig(84, GY, nt=98, ns=0, ft=-10, fs=-14, torso=14, head=10, nu=-52, nf=38, fu=84, ff=158,
               nfoot=92, ffoot=60, hl=hl)
    f2 = ground(GY) + b + badge(64, 12, "膝を前へ高く", GRN)
    res.append((S(f2, vb), "② 膝を高く引き上げ<br>腕を大きく振る"))
    return res

def bounding():
    res = []
    vb = set_vbx("0 -4 170 158")
    hl = ("glute", "ham")
    a, _ = fig(54, GY, nt=84, ns=6, ft=-38, fs=-40, torso=10, head=6, nu=-40, nf=-10, fu=40, ff=120,
               nfoot=100, ffoot=-4, hl=hl)
    f1 = ground(GY) + a + carrow(98, 64, 128, 22, 160, 50) + badge(126, 86, "斜め前へ") + LG(vb)
    res.append((S(f1, vb), "① 後ろ足で強く蹴り<br>前の膝を高く上げる"))
    b, _ = fig(86, GY, nt=70, ns=10, ft=-60, fs=-86, torso=14, nu=-56, nf=-12, fu=70, ff=150, lift=24,
               nfoot=100, ffoot=-36, hl=hl, shadow=False)
    f2 = (ground(GY) + f'<path d="M14,118 Q86,20 158,118" fill="none" stroke="{MOV}" stroke-width="1.6" stroke-dasharray="3,4" stroke-opacity=".6"/>'
          + b + badge(40, 14, "大きく一歩", GRN))
    res.append((S(f2, vb), "② 空中で大きく一歩<br>反対足で着地→すぐ次へ"))
    return res


# ===================== B. フットワーク =====================
def split_step():
    res = []
    vb = set_vbx("0 -22 170 176")
    kw = dict(front=True, nu=-4, nf=162, fu=22, ff=-150, racket=-22, hl=("quad",))
    a, _ = fig(74, GY, nt=-12, ns=-8, ft=12, fs=8, nb=30, fb=30, **kw)
    f1 = ground(GY) + a + badge(134, -3, "膝を軽く", GRN) + LG(vb)
    res.append((S(f1, vb), "① 足は肩幅・膝を軽く曲げ<br>ラケットを胸の前で構える"))
    b, _ = fig(74, GY, nt=-12, ns=-9, ft=12, fs=9, nb=12, fb=12, lift=15, **kw)
    f2 = ground(GY) + b + arrow(140, 118, 140, 90) + badge(148, 78, "跳ぶ") + badge(128, -3, "相手の打球時")
    res.append((S(f2, vb), "② 相手が打つ瞬間に<br>その場で小さくジャンプ"))
    c, P3 = fig(74, GY, nt=-32, ns=-48, ft=32, fs=48, nb=86, fb=86, torso=10, nheel=True, **kw)
    na = P3["nank"]
    kick = carrow(na[0] - 4, GY - 4, na[0] - 14, GY - 18, na[0] + 2, GY - 24, MOV, 1.8)
    f3 = ground(GY) + c + kick + arrow(124, 120, 162, 120) + badge(150, 146, "蹴る") + badge(124, -3, "肩幅より広く", GRN)
    res.append((S(f3, vb), "③ 肩幅より広く着地し腰を落とす<br>片足で蹴って1歩目"))
    return res


def six_point():
    s = court_svg(260)
    chk_reset()
    return [(s, "")]


def lunge():
    res = []
    vb = set_vbx("0 0 170 154")
    kwa = dict(nt=82, ns=-2, ft=-56, fs=-68, torso=16, head=10, nu=86, nf=96, fu=-62, ff=-46, racket=72, nfoot=104, ffoot=118)
    a, _ = fig(54, GY, hl=("quad", "glute"), hls="n", **kwa)
    f1 = ground(GY) + a + badge(56, 22, "膝はつま先の向き", GRN) + LG(vb)
    res.append((S(f1, vb), "① 前へ大きく1歩<br>かかとから着地"))
    b, P = fig(46, GY, nt=46, ns=10, ft=-12, fs=-18, torso=6, head=6, nu=62, nf=100, fu=-34, ff=-30, racket=60,
               nfoot=116, ffoot=96, hl=("quad", "glute"), hls="n")
    f2 = (ground(GY) + b + arrow(150, 96, 112, 96) + badge(138, 82, "戻る") +
          badge(120, 18, "かかとで押す", GRN))
    res.append((S(f2, vb), "② 前足のかかとで押し<br>1歩で素早くベースへ戻る"))
    return res

def cross_touch():
    s = cross_svg(220)
    chk_reset()
    return [(s, "")]


# ===================== C. 体幹 =====================
VBP = "10 52 152 102"


def _plank(torso, leg):
    return dict(nt=-leg, ns=-leg, ft=-leg, fs=-leg, torso=torso, head=torso + 2, nu=0, nf=90, fu=0, ff=90,
                nfoot=90 - leg, ffoot=90 - leg, nha=90, fha=90)


def plank():
    res = []
    set_vbx(VBP)
    t = solve(lambda t: figP(76, GY, **_plank(t, t))["nelb"][1] - (GY - 3.6), 60, 89)
    a, P = fig(76, GY, hl=("abs",), **_plank(t, t))
    f1 = ground(GY) + a + guide_line(P["sh"], P["nank"], 1, 14) + badge(86, 70, "肩〜かかとが一直線", GRN) + LG(VBP)
    res.append((S(f1, VBP), "① 肘は肩の真下<br>頭からかかとまで一直線"))
    leg = 99
    t2 = solve(lambda t: (figP(76, GY, **_plank(t, leg))["nelb"][1] - (GY - 3.6)), 30, 89)
    b, P = fig(76, GY, hl=("abs",), **_plank(t2, leg))
    f2 = (ground(GY) + b + guide_line(P["sh"], P["nank"], 0.55, 14) +
          ng_mark(P["hip"][0], P["hip"][1] + 1, 14, 162, 52) + badge(76, 70, "腰が落ちる", RED))
    res.append((S(f2, VBP), "NG 腰が落ちる/反る<br>→ そこで終了"))
    return res


def side_plank():
    res = []
    vb = set_vbx("0 40 170 114")

    def kw(t, leg):
        return dict(front=True, torso=t, head=t, nt=leg, ns=leg, ft=leg, fs=leg, nu=0, nf=-84, nfl=0.6,
                    fu=180, ff=180, nha=-84)

    def place(t, leg):
        P = figP(0, GY, hy=0, **kw(t, leg))
        low = max(P["nshoe"][2], P["fshoe"][2])
        dy = GY - low
        return P["nelb"][1] + dy - (GY - 3.8), dy

    def make(leg_off, hl_):
        t = solve(lambda t: place(t, -t + leg_off)[0], -88, -30)
        leg = -t + leg_off
        dy = place(t, leg)[1]
        P0 = figP(0, GY, hy=dy, **kw(t, leg))
        hx = 46 - P0["nelb"][0]
        return fig(hx, GY, hy=dy, hl=hl_, shadow=False, **kw(t, leg))
    a, P = make(-4, ("oblique",))
    f1 = ground(GY) + a + guide_line(P["nsh"], P["nank"], 1, 12) + badge(130, 60, "腰を高く", GRN) + LG(vb)
    res.append((S(f1, vb), "① 肘を肩の真下に<br>足を重ねて腰を持ち上げる"))
    b, P = make(58, ("oblique",))
    f2 = (ground(GY) + b + guide_line(P["nsh"], P["nank"], 0.55, 12) +
          ng_mark(P["hip"][0], P["hip"][1] + 2, 14, 170, 40) + badge(120, 82, "腰が落ちる", RED))
    res.append((S(f2, vb), "NG 腰が落ちる<br>→ 落ちたらそこで終了"))
    return res


def dead_bug():
    res = []
    vb = set_vbx("6 40 156 114")
    hy = GY - 9.2
    base = dict(hy=hy, torso=-90, head=-90, nt=180, ns=90, ft=180, fs=90, nfoot=180, ffoot=180, hl=("abs",), shadow=False)
    a, P = fig(90, GY, nu=180, nf=180, fu=180, ff=180, **base)
    wx = P["hip"][0] - 12
    f1 = (ground(GY) + a + arrow(wx, hy - 34, wx, hy - 13) + badge(84, 56, "腰を床へ押し付ける", GRN) + LG(vb) +
          f'<path d="M{f(P["hip"][0]+4)},{f(P["nknee"][1])} h-4 v4" fill="none" stroke="{GRN}" stroke-width="1.2"/>')
    res.append((S(f1, vb), "① 仰向けで腕は天井<br>股関節と膝は90°"))
    base2 = dict(base)
    base2.update(ft=96, fs=94)
    b, P = fig(90, GY, nu=-96, nf=-94, fu=180, ff=180, **base2)
    f2 = (ground(GY) + b + arrow(42, 88, 12, 88) + arrow(138, 88, 157, 88) +
          arrow(wx, hy - 34, wx, hy - 13) + badge(84, 56, "腰は浮かせない", GRN))
    res.append((S(f2, vb), "② 反対の手と脚を<br>ゆっくり伸ばす"))
    return res


def bird_dog():
    res = []
    vb = set_vbx("0 40 170 114")
    kw = dict(nt=-4, ns=-90, ft=-4, fs=-90, torso=80, head=86, nfoot=-92, ffoot=-92, nha=96, fha=96,
              hl=("back", "glute"))
    a, P = fig(62, GY, nu=-2, nf=-2, fu=-2, ff=-2, **kw)
    f1 = ground(GY) + a + guide_line(P["hip"], P["neck"], 1, 10) + badge(118, 62, "背中はまっすぐ", GRN) + LG(vb)
    res.append((S(f1, vb), "① 四つ這い<br>手は肩の下・膝は腰の下"))
    kw2 = dict(kw)
    kw2.update(ft=-88, fs=-90, ffoot=-4)
    b, P = fig(74, GY, nu=92, nf=92, fu=-2, ff=-2, **kw2)
    hy_, ay_ = P["nhand"][1], P["fank"][1]
    f2 = (ground(GY) + b + arrow(P["nhand"][0] + 10, hy_, P["nhand"][0] + 24, hy_) +
          arrow(P["fank"][0] - 6, ay_ - 2, P["fank"][0] - 20, ay_ - 2) + badge(86, 58, "2秒キープ", GRN))
    res.append((S(f2, vb), "② 対角の手と脚を伸ばし<br>2秒キープ"))
    return res


def _topnote(vb):
    x0, y0, w, h = [float(v) for v in vb.split()]
    CHK["rects"].append((x0 + w - 74, y0 + h - 16, 68, 12, "note"))
    return text(x0 + w - 6, y0 + h - 6, "真上から見た図", 9, GRD, "end")


def pallof():
    """真上から見た図: 柱(左)・ゴム・人物。腕を伸ばしても肩ラインは正面のまま"""
    res = []
    vb = set_vbx("0 0 170 154")
    k = 1.6
    cx, cy = 102, 90

    def post():
        return prop_rect(6, 40, 18, 18, fill="#c9b79c", stroke="#8a6d3b", rx=3) + text(15, 72, "柱", 10, "#8a6d3b")

    def band(h):
        return line((24, 49), h, "#ffffff", 4.4) + line((24, 49), h, EQ, 2.6)
    h1 = (cx, cy - 13 * k)
    p1, T = top_person(cx, cy, 0, 0, ((cx + 3 * k, h1[1]), (cx - 3 * k, h1[1])), hl=("oblique",), k=k)
    f1 = post() + band(h1) + p1 + badge(108, 18, "胸の前で持つ", GRN) + _topnote(vb)
    res.append((S(f1, vb), "① 柱の横に立ち<br>ゴムを胸の前で持つ(真上から見た図)"))
    h2 = (cx, cy - 33 * k)
    p2, T = top_person(cx, cy, 0, 0, ((cx + 2.6 * k, h2[1]), (cx - 2.6 * k, h2[1])),
                       elbows=((cx + 6 * k, cy - 17 * k), (cx - 6 * k, cy - 17 * k)), hl=("oblique",), k=k)
    f2 = (post() + band(h2) + p2 + arrow(cx - 16, h2[1] - 8, cx - 40, h2[1] - 8, EQ, 1.8) +
          badge(40, 128, "肩は正面", GRN) + _topnote(vb))
    res.append((S(f2, vb), "② 腕を真っすぐ前へ伸ばし<br>ゴムに引かれても肩・腰を回さない"))
    return res


# ===================== D. スマッシュ威力 =====================
def med_rot():
    """真上から見た図(拡大): 壁は右。腰が先に回り(①で肩と腰が約35°ずれる)、③で肩が追いつく"""
    res = []
    vb = set_vbx("0 0 170 172")
    k = 1.85
    cx, cy = 90, 102
    C = (cx, cy)
    W = prop_rect(160, 6, 8, 160, fill="#e9ecef", stroke=GRD, rx=0)
    lheel = (cx - 12.5 * k, cy + 1.5 * k)
    # ① 肩を大きく壁と反対へ、腰は先に戻り始める(差35°)
    sh1, hp1 = -55, -20
    b1 = add(C, _rv((-23 * k, 2 * k), sh1))
    p1, T = top_person(cx, cy, sh1, hp1, (add(b1, _rv((4 * k, -5 * k), sh1)), add(b1, _rv((3 * k, 6 * k), sh1))),
                       head_ang=0, hl=("oblique",), k=k, line_side=1)
    f1 = W + p1 + med_ball(*b1) + badge(96, 16, "反対へひねる") + arrow(130, 160, 154, 160, MOV, 1.8, dash="4,3")
    res.append((S(f1, vb), "① 肩を壁と反対へひねり<br>ボールを後ろの腰へ(真上から見た図)"))
    # ② 腰が先に回り、肩は遅れる(差22°)。後ろ足のかかとを上げる
    sh2, hp2 = -10, 12
    b2 = add(C, _rv((-4 * k, -17 * k), sh2))
    p2, T = top_person(cx, cy, sh2, hp2, (add(b2, _rv((6 * k, 2 * k), sh2)), add(b2, _rv((-6 * k, 2 * k), sh2))),
                       feet=((0, False), (30, True)), head_ang=10, hl=("oblique",), k=k)
    f2 = (W + p2 + med_ball(*b2) + badge(96, 16, "腰から先に回す") + arrow(130, 160, 154, 160, MOV, 1.8, dash="4,3") +
          leader(40, 146, lheel[0] - 2, lheel[1] + 4) + badge(48, 160, "後ろ足かかと↑", GRN))
    res.append((S(f2, vb), "② 後ろ足のかかとを上げ<br>腰→胸→腕の順に回す"))
    # ③ 肩が腰に追いつき(差0°)、腕を壁へ伸ばして投げる
    sh3, hp3 = 40, 40
    h3 = (add(C, _rv((7 * k, -25 * k), sh3)), add(C, _rv((-1 * k, -26 * k), sh3)))
    p3, T = top_person(cx, cy, sh3, hp3, h3, feet=((0, False), (40, True)), head_ang=50, hl=("oblique",), k=k)
    bp = (126, 34)
    f3 = W + p3 + med_ball(*bp) + arrow(bp[0] + 12, bp[1], 156, bp[1]) + badge(60, 16, "壁へ全力で")
    res.append((S(f3, vb), "③ 肩が腰に追いつき<br>壁へ全力で投げる"))
    return res

def overhead():
    res = []
    vb = set_vbx("0 -6 170 160")
    W = wall(156, 0, GY)
    hl = ("abs", "tricep")
    kw = dict(nt=-16, ns=-8, ft=22, fs=-4, ffoot=90, nfoot=110, hl=hl)
    a, P = fig(66, GY, torso=-18, head=-24, look=-6, nu=-150, nf=-128, fu=-150, ff=-128, ball=True, **kw)
    f1 = ground(GY) + W + a + badge(110, 40, "胸を反る", GRN) + LG(vb)
    res.append((S(f1, vb), "① ボールを両手で<br>頭の後ろへ・胸を反らす"))
    b, P = fig(70, GY, torso=0, head=4, nu=178, nf=176, fu=178, ff=176, ball=True, **kw)
    f2 = ground(GY) + W + b + carrow(46, 22, 76, -6, 112, 18)
    res.append((S(f2, vb), "② 反りを戻しながら<br>腕を頭上から前へ"))
    c, P = fig(78, GY, torso=24, head=16, nu=128, nf=118, fu=128, ff=118, nt=-36, ns=-30, ft=26, fs=-6,
               nfoot=130, ffoot=90, hl=hl)
    f3 = ground(GY) + W + c + med_ball(140, 26) + arrow(118, 36, 129, 30) + badge(54, 12, "高い所を狙う")
    res.append((S(f3, vb), "③ 壁の高い所へ<br>勢いよく投げる"))
    return res


def tube_er():
    """真上から見た図: 右肘を脇に固定(タオル)し、前腕だけを外へ約70°開く"""
    res = []
    vb = set_vbx("0 0 170 162")
    k = 2.3
    cx, cy = 84, 98
    post = prop_rect(4, 26, 18, 18, fill="#c9b79c", stroke="#8a6d3b", rx=3) + text(13, 58, "柱", 10, "#8a6d3b")
    rsh = (cx + 13 * k, cy)
    el = (cx + 17.5 * k, cy + 1.0 * k)
    lsh = (cx - 13 * k, cy)
    lel, lh = (cx - 15 * k, cy + 1.5 * k), (cx - 15.5 * k, cy - 1 * k)

    def make(ang):
        d = _rv((0, -1), ang)
        hd = add(el, d, 13 * k)
        p, T = top_person(cx, cy, 0, 0, (hd, lh), elbows=(el, lel), hl=(), k=k, lines=False)
        towel = (f'<ellipse cx="{f(el[0]-3.6*k)}" cy="{f(el[1]+0.5*k)}" rx="{f(2.2*k)}" ry="{f(3.6*k)}" fill="#ffffff" stroke="{OUT}" stroke-width="1"/>')
        band = line((22, 35), hd, "#ffffff", 4.2) + line((22, 35), hd, EQ, 2.4)
        delt = muscle(rsh, 6.0 * k * 0.8, 2.6 * k * 0.8, 0, 0.6)
        return post + band + p + towel + delt, hd
    s1, h1 = make(-50)
    f1 = s1 + leader(60, 140, el[0] - 4 * k, el[1] + 3 * k) + badge(40, 152, "タオルを挟む", GRN) + badge(96, 16, "肘は脇腹に90°", GRN) + _topnote(vb)
    res.append((S(f1, vb), "① 肘を脇腹につけ90°<br>前腕はお腹の前(真上から見た図)"))
    s2, h2 = make(20)
    gst = add(el, _rv((0, -1), -50), 13 * k)
    arc = (f'<g opacity=".35">{line(el, gst, OUT, 6.4)}{line(el, gst, SKIN, 4.6)}</g>' +
           earc(el[0], el[1], 13 * k + 6, 13 * k + 6, -140, -70, MOV, 2.2) +
           f'<rect x="{f(el[0]-30)}" y="{f(el[1]-13*k-27)}" width="26" height="14" rx="4" fill="#ffffff" stroke="{MOV}" stroke-width="1"/>' +
           text(el[0] - 17, el[1] - 13 * k - 16.5, "70°", 10, MOV))
    f2 = s2 + arc + badge(96, 16, "肘は動かさない", GRN) + badge(40, 152, "前腕だけ外へ", MOV) + _topnote(vb)
    res.append((S(f2, vb), "② 肘を固定したまま<br>前腕だけ外へ約70°開く"))
    return res

def _push(t, leg, nu, nf):
    return dict(nt=-leg, ns=-leg, ft=-leg, fs=-leg, torso=t, head=t + 8, nu=nu, nf=nf, fu=nu, ff=nf,
                nfoot=90 - leg, ffoot=90 - leg, nha=96, fha=96)


def pushup():
    res = []
    vb = set_vbx("10 36 152 118")
    HX = 120

    def inset(x, y):
        """真上から見た肘の角度: 45°(OK) / 90°(NG)"""
        o = rect(x, y, 62, 42, fill="#ffffff", stroke=GRD, sw=1, rx=5)
        for cx_, ang, lab, col in ((x + 16, 45, "OK", GRN), (x + 46, 90, "NG", RED)):
            cy_ = y + 17
            L = Layer()
            L.circ((cx_, cy_ - 10), 3.2, HAIR)
            for sg in (-1, 1):
                shp = (cx_ + 4.5 * sg, cy_ - 4)
                elp = add(shp, (math.sin(math.radians(ang)) * sg, math.cos(math.radians(ang))), 8)
                L.cap(shp, elp, 1.7, 1.5, SKIN)
            L.cap((cx_, cy_ - 4), (cx_, cy_ + 10), 4.6, 4.0, SHIRT)
            o += L.render(0.8)
            o += text(cx_, y + 39, f"{ang}°{lab}", 8, col)
        CHK["rects"].append((x, y, 62, 42, "inset"))
        return o
    hand_y = GY - 3.4

    def make(nu, nf, lo, hi):
        t = solve(lambda t: figP(0, GY, **_push(t, t, nu, nf))["nhand"][1] - hand_y, lo, hi)
        P = figP(0, GY, **_push(t, t, nu, nf))
        return fig(HX - P["nhand"][0], GY, hl=("chest", "tricep"), **_push(t, t, nu, nf))
    a, P = make(0, 0, 50, 85)
    f1 = ground(GY) + a + guide_line(P["sh"], P["nank"], 1, 10) + badge(60, 56, "体は一直線", GRN) + LG(vb)
    res.append((S(f1, vb), "① 手は肩幅より少し広く<br>体は一直線"))
    b, P = make(-62, -2, 60, 89)
    f2 = ground(GY) + b + arrow(84, 66, 84, 92) + badge(52, 52, "肘は約45°", GRN) + inset(96, 40)
    res.append((S(f2, vb), "② 胸を床近くまで下ろし<br>一気に押し上げる"))
    return res


def wrist():
    res = []
    vb = set_vbx("0 20 170 134")

    def chair(P):
        hp = P["hip"]
        s = prop_rect(hp[0] - 22, hp[1] + 8, 34, 6)
        s += line((hp[0] - 18, hp[1] + 14), (hp[0] - 18, GY), "#8a6d3b", 3) + line((hp[0] + 8, hp[1] + 14), (hp[0] + 8, GY), "#8a6d3b", 3)
        s += line((hp[0] - 20, hp[1] + 10), (hp[0] - 26, hp[1] - 30), "#8a6d3b", 3.4)
        return s

    def make(ha):
        def bottle(P):
            h = P["nhand"]
            d = (math.sin(math.radians(ha)), math.cos(math.radians(ha)))
            c = add(h, d, 3.4)
            ang = ang_of(d) + 90        # 手の向きに直交・拳の中心を通る
            return (f'<g transform="rotate({f(ang)} {f(c[0])} {f(c[1])})">'
                    f'<rect x="{f(c[0]-11)}" y="{f(c[1]-4.2)}" width="22" height="8.4" rx="3.5" fill="#a5d8ff" stroke="{OUT}" stroke-width="1.2"/>'
                    f'<rect x="{f(c[0]+11)}" y="{f(c[1]-2.4)}" width="3.2" height="4.8" rx="1" fill="{MOV}" stroke="{OUT}" stroke-width="0.8"/>'
                    f'<line x1="{f(c[0]-6)}" y1="{f(c[1]-4)}" x2="{f(c[0]-6)}" y2="{f(c[1]+4)}" stroke="#ffffff" stroke-width="1"/></g>')
        return fig(52, GY, nt=90, ns=0, ft=86, fs=-4, torso=20, nu=31, nf=90, fu=27, ff=90, nfoot=90, ffoot=90,
                   nha=ha, hl=("forearm",), hls="n", pre_narm=lambda P: chair(P) + bottle(P))
    a, P = make(48)
    h = P["nhand"]
    f1 = (ground(GY) + a + carrow(h[0] + 18, h[1] - 8, h[0] + 26, h[1] + 6, h[0] + 18, h[1] + 20) +
          badge(122, 38, "前腕は太ももに", GRN) + LG(vb))
    res.append((S(f1, vb), "① 前腕を太ももに乗せ<br>手首を下へ"))
    b, P = make(122)
    h = P["nhand"]
    f2 = (ground(GY) + b + carrow(h[0] + 18, h[1] + 16, h[0] + 26, h[1] + 2, h[0] + 18, h[1] - 12) +
          badge(122, 38, "手首だけ動かす", GRN))
    res.append((S(f2, vb), "② 手首を上へ巻き上げる<br>(逆向きも同じ回数)"))
    return res


# ===================== E. 実戦連動 =====================
def jump_smash():
    res = []
    vb = set_vbx("0 -72 170 226")
    hl = ("quad", "abs", "oblique")
    # 近い側 = 右(利き腕・右脚) / 遠い側(暗い) = 左腕・左脚
    kw1 = dict(nt=-12, ns=-16, ft=32, fs=-6, torso=-10, head=-8, look=-22, nu=-112, nf=-168, racket=-42,
               fu=150, nfoot=96, ffoot=90, tw=1.5)
    shp1 = (150, -30)
    fe = figP(70, GY, ff=158, **kw1)["felb"]
    ff1 = math.degrees(math.atan2(shp1[0] - fe[0], shp1[1] - fe[1]))      # 前腕の延長線がシャトルを通る
    a, P = fig(70, GY, ff=ff1, hl=hl, fpoint=True, **kw1)
    f1 = (ground(GY) + a + shuttle(shp1[0], shp1[1], 100) + badge(96, -53, "半身で構える", GRN) +
          badge(140, 104, "肘を高く", GRN) + LG(vb))
    res.append((S(f1, vb, 165), "① 構え(右利き)・半身<br>左足前・左手でシャトルを指す"))
    b, P = fig(70, GY, nt=44, ns=-16, ft=50, fs=-10, torso=-14, head=20, look=-44, nu=176, nf=-70, racket=218,
               fu=160, ff=170, nfoot=90, ffoot=90, hl=hl, tw=0.3, racket_behind=True)
    shp = P["nsh"]
    mot = carrow(shp[0] - 16, shp[1] + 2, shp[0] - 10, shp[1] - 44, shp[0] + 16, shp[1] - 44)
    f2 = (ground(GY) + b + mot + arrow(146, 124, 146, 90) + badge(138, 78, "沈んで蹴る") +
          badge(98, -36, "反ってラケットを背中へ", GRN))
    res.append((S(f2, vb, 165), "② 沈み込み(膝約120°)<br>胸を反らしラケットを背中へ"))
    c, P = fig(66, GY, nt=32, ns=6, ft=-28, fs=-62, torso=16, head=26, look=-52, nu=160, nf=160, racket=40,
               fu=-12, ff=64, lift=30, nfoot=80, ffoot=-12, hl=hl, tw=-0.4, far_arm_front=True)
    rc = P["rcen"]
    sx, sy = rc[0] + 18, rc[1] + 12
    hx_ = P["head"][0]
    vline = line((hx_, P["head"][1] + 8), (hx_, -66), GRD, 1.2, dash="2,3")
    rt = P["rtip"]
    swing = carrow(rt[0] - 2, rt[1] - 6, rc[0] + 40, rc[1] - 10, rc[0] + 34, rc[1] + 30)
    f3 = (ground(GY) + vline + c + shuttle(sx, sy, 40) + swing +
          badge(40, -50, "少し前で打つ", MOV) + badge(134, 138, "脚の入れ替え", GRN))
    res.append((S(f3, vb, 165), "③ 空中・最高点の少し前で打つ<br>左腕は脇へ引きつける"))

    def kw4(ns_):
        return dict(nt=-34, ns=ns_, ft=22, fs=-22, torso=16, head=12, nu=-20, nf=60, racket=80, fu=-30, ff=-10,
                    nfoot=ns_ + 62, ffoot=92)
    ns4 = solve(lambda v: figP(70, GY, **kw4(v))["nshoe"][2] - figP(70, GY, **kw4(v))["fshoe"][2], -70, -10)
    d, P = fig(70, GY, hl=hl, **kw4(ns4))
    f4 = ground(GY) + d + badge(54, -20, "左足で着地", GRN) + badge(58, 2, "ラケットは胸の前", GRN)
    res.append((S(f4, vb, 165), "④ 左足で着地(右はつま先だけ)<br>ラケットを胸の前へ戻して次へ"))
    return res

def jump_rope():
    res = []
    vb = set_vbx("0 -16 170 170")

    def rope(P, under):
        hl_, hr = P["nhand"], P["fhand"]
        dv = (0, 1) if under else (0, -1)
        gl = add(add(hl_, dv, 7), (-2, 0))
        gr = add(add(hr, dv, 7), (2, 0))
        cx = (gl[0] + gr[0]) / 2
        if under:
            low = GY - 1.2
            path = (f'M{f(gl[0])},{f(gl[1])} C{f(gl[0]-3)},{f(gl[1]+30)} {f(gl[0]-2)},{f(low)} {f(cx)},{f(low)} '
                    f'C{f(gr[0]+2)},{f(low)} {f(gr[0]+3)},{f(gr[1]+30)} {f(gr[0])},{f(gr[1])}')
        else:
            top = P["head"][1] - 20
            path = (f'M{f(gl[0])},{f(gl[1])} C{f(gl[0]-6)},{f(gl[1]-40)} {f(gl[0]-2)},{f(top)} {f(cx)},{f(top)} '
                    f'C{f(gr[0]+2)},{f(top)} {f(gr[0]+6)},{f(gr[1]-40)} {f(gr[0])},{f(gr[1])}')
        s = f'<path d="{path}" fill="none" stroke="#ffffff" stroke-width="3.6"/><path d="{path}" fill="none" stroke="{EQ}" stroke-width="2"/>'
        for g, hnd in ((gl, hl_), (gr, hr)):
            s += line(add(hnd, dv, -1), g, OUT, 4.6) + line(add(hnd, dv, -1), g, "#495057", 3.0)
        return s

    def pose_(lift, under):
        kw = dict(front=True, nt=-3, ns=2, ft=3, fs=-2, nb=8, fb=8, nu=-6, nf=-88, nfl=0.6, fu=6, ff=88, ffl=0.6,
                  lift=lift, hl=("calf",), nha=180 if not under else 0, fha=180 if not under else 0)
        a, P = fig(80, GY, **kw)
        return a + rope(P, under), P
    a, P = pose_(7, True)
    h = P["fhand"]
    f1 = (ground(GY) + a + carrow(h[0] + 12, h[1] - 10, h[0] + 22, h[1] + 2, h[0] + 12, h[1] + 14) +
          badge(134, 0, "手首で回す") + LG(vb))
    res.append((S(f1, vb), "① 基本跳び<br>脇を締め、縄が足の下を通る瞬間に跳ぶ"))
    b, P = pose_(18, False)
    f2 = ground(GY) + b + arrow(146, 120, 146, 92) + badge(140, 80, "少し高く")
    res.append((S(f2, vb), "② 二重跳び<br>少し高く跳び、縄を2回通す"))
    return res
