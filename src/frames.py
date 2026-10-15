from figlib import *

GY = 130
VB = "0 0 170 150"
VBJ = "0 -24 170 174"      # jump frames (more headroom)


def S(inner, vb=VB, w=185):
    return svg(inner, vb, w)


# ===================== A. 脚(家) =====================
def jump_squat():
    a, _ = fig(70, GY, nt=70, ns=-28, ft=66, fs=-30, torso=36, nu=-40, nf=-30, fu=-35, ff=-25, hl=("legs",))
    f1 = ground(GY) + a + arrow(138, 62, 138, 104, RED) + badge(138, 52, "沈む")
    b, _ = fig(85, GY, nt=2, ns=0, ft=-3, fs=0, torso=0, nu=172, nf=178, fu=165, ff=172, lift=26,
               nfoot=150, ffoot=150, hl=("legs",))
    f2 = ground(GY) + b + arrow(140, 96, 140, 30, RED) + badge(140, 18, "全力で跳ぶ")
    c, _ = fig(72, GY, nt=60, ns=-26, ft=56, fs=-28, torso=28, nu=55, nf=85, fu=45, ff=80, hl=("legs",))
    f3 = ground(GY) + c + badge(130, 60, "静かに着地", GRN)
    return [(S(f1, VBJ), "① 浅くしゃがむ<br>腕は後ろへ"), (S(f2, VBJ), "② 腕を振り上げて<br>真上にジャンプ"),
            (S(f3, VBJ), "③ 膝を曲げて<br>音を立てず着地")]


def bulgarian():
    chair_x = 34
    a, _ = fig(0, GY, nt=35, ns=-8, ft=-35, fs=-86, torso=6, nu=35, nf=95, fu=30, ff=90, ffoot=-90,
               anchor=("fank", chair_x), hl=("legs",))
    chair = (rect(chair_x - 18, 110, 38, 5, fill="#c9b79c", stroke="#8a6d3b", rx=1) +
             line((chair_x - 14, 115), (chair_x - 14, GY), "#8a6d3b", 3) + line((chair_x + 16, 115), (chair_x + 16, GY), "#8a6d3b", 3))
    f1 = ground(GY) + chair + a
    b, _ = fig(0, GY, nt=80, ns=-8, ft=-60, fs=-105, torso=10, nu=35, nf=95, fu=30, ff=90, ffoot=-90,
               anchor=("fank", chair_x), hl=("legs",))
    f2 = ground(GY) + chair + b + arrow(145, 70, 145, 104, RED) + badge(145, 60, "真下へ沈む")
    return [(S(f1), "① 後ろ足を椅子に<br>前足は一歩半前"), (S(f2), "② 上体を真下へ<br>前足のかかとで立つ")]


def pogo():
    a, _ = fig(85, GY, nt=8, ns=-6, ft=8, fs=-6, torso=0, nu=15, nf=35, fu=10, ff=30, lift=0,
               nfoot=105, ffoot=105, hl=("legs",))
    f1 = ground(GY) + a + badge(130, 100, "接地は一瞬", GRN)
    b, _ = fig(85, GY, nt=0, ns=0, ft=0, fs=0, torso=0, nu=15, nf=35, fu=10, ff=30, lift=14,
               nfoot=155, ffoot=155, hl=("legs",))
    f2 = ground(GY) + b + arrow(140, 100, 140, 70, RED) + badge(140, 60, "3〜5cm")
    return [(S(f1, VBJ), "① 着地した瞬間<br>つま先で床を押す"), (S(f2, VBJ), "② 膝は伸ばしたまま<br>足首で小さく跳ぶ")]


def calf_raise():
    step = rect(60, 118, 80, 12, fill="#c9b79c", stroke="#8a6d3b", rx=1)
    a, P = fig(0, 118, nt=0, ns=0, ft=0, fs=-90, torso=0, nu=40, nf=85, fu=40, ff=85, lift=-4,
               nfoot=105, ffoot=90, anchor=("nank", 68), hl=("legs",))
    w1 = wall(P["nhand"][0] + 4, 30, 130)
    f1 = ground(GY) + step + a + w1 + badge(48, 40, "かかと下", GRN)
    b, P2 = fig(0, 118, nt=0, ns=0, ft=0, fs=-90, torso=0, nu=40, nf=85, fu=40, ff=85, lift=7,
                nfoot=60, ffoot=90, anchor=("nank", 68), hl=("legs",))
    w2 = wall(P2["nhand"][0] + 4, 30, 130)
    f2 = ground(GY) + step + b + w2 + arrow(40, 100, 40, 60, RED) + badge(40, 50, "素早く上げる")
    return [(S(f1), "① 段差に片足<br>かかとを下まで下ろす"), (S(f2), "② かかとを高く上げ<br>3秒で下ろす")]


def nordic():
    sofa = rect(4, 104, 30, 26, fill="#b8c4d6", stroke="#5b6b85", rx=4)
    a, _ = fig(0, GY, hy=GY - 26, nt=0, ns=-90, ft=0, fs=-90, torso=3, nu=40, nf=105, fu=35, ff=100,
               nfoot=-90, ffoot=-90, anchor=("nank", 40), hl=("legs",))
    f1 = ground(GY) + sofa + a + text(19, 98, "かかと固定", 8.5, "#5b6b85")
    b, _ = fig(0, GY, hy=GY - 14, nt=-52, ns=-90, ft=-52, fs=-90, torso=52, nu=22, nf=15, fu=18, ff=10,
               nfoot=-90, ffoot=-90, anchor=("nank", 40), hl=("legs",))
    f2 = ground(GY) + sofa + b + carrow(70, 56, 106, 40, 132, 74, RED) + badge(96, 30, "ゆっくり倒れる")
    return [(S(f1), "① ひざ立ち<br>かかとを固定"), (S(f2), "② 体を一直線のまま<br>3〜5秒かけて前へ")]


# ===================== A. 脚(外) =====================
BOXTOP = 104


def box(x1, x2, top=BOXTOP):
    return rect(x1, top, x2 - x1, GY - top, fill="#c9b79c", stroke="#8a6d3b", rx=2)


def box_jump():
    a, _ = fig(45, GY, nt=68, ns=-28, ft=64, fs=-30, torso=34, nu=-40, nf=-30, fu=-35, ff=-25, hl=("legs",))
    f1 = ground(GY) + box(98, 162) + a
    b, _ = fig(104, BOXTOP, nt=88, ns=-8, ft=84, fs=-10, torso=14, nu=110, nf=125, fu=105, ff=120,
               lift=12, hl=("legs",))
    f2 = ground(GY) + box(98, 162) + b + arrow(60, 100, 60, 60, RED)
    c, _ = fig(130, BOXTOP, nt=58, ns=-25, ft=54, fs=-27, torso=26, nu=55, nf=85, fu=45, ff=80, hl=("legs",))
    f3 = ground(GY) + box(98, 162) + c + badge(60, 70, "静かに乗る", GRN)
    return [(S(f1, VBJ), "① しゃがんで<br>腕を後ろへ"), (S(f2, VBJ), "② 膝を引き上げ<br>両足で跳び乗る"),
            (S(f3, VBJ), "③ 台の上で静かに着地<br>降りるときは歩く")]


def depth_jump():
    bx = box(4, 52)
    a, _ = fig(34, BOXTOP, nt=10, ns=-6, ft=8, fs=-6, torso=4, nu=20, nf=50, fu=15, ff=45, hl=("legs",))
    f1 = ground(GY) + bx + a + carrow(54, 70, 80, 60, 96, 96, RED) + badge(108, 52, "跳ばず踏み出す")
    b, _ = fig(112, GY, nt=42, ns=-20, ft=38, fs=-22, torso=22, nu=40, nf=75, fu=35, ff=70, hl=("legs",))
    f2 = ground(GY) + bx + b + arrow(150, 108, 150, 66, RED) + badge(148, 56, "接地は最短!")
    c, _ = fig(112, GY, nt=2, ns=0, ft=-3, fs=0, torso=0, nu=172, nf=178, fu=165, ff=172, lift=26,
               nfoot=150, ffoot=150, hl=("legs",))
    f3 = ground(GY) + bx + c + arrow(150, 96, 150, 30, RED) + badge(148, 18, "全力で跳ぶ")
    return [(S(f1, VBJ), "① 台の端に立ち<br>一歩踏み出して落ちる"), (S(f2, VBJ), "② 着地の瞬間<br>浅く沈むだけ"),
            (S(f3, VBJ), "③ すぐに<br>全力でジャンプ")]


def sprint():
    vb = "0 -10 170 160"
    a, _ = fig(85, GY, nt=-36, ns=-42, ft=84, fs=-6, torso=24, nu=70, nf=125, fu=-55, ff=-25,
               nfoot=120, ffoot=95, hl=("legs",))
    f1 = f'<g transform="rotate(-9 85 {GY})">' + ground(GY, -10, 180) + a + "</g>" + badge(130, 22, "後ろ脚で地面を押す", GRN)
    b, _ = fig(85, GY, nt=92, ns=-10, ft=-45, fs=-75, torso=22, nu=-50, nf=-20, fu=75, ff=120, lift=16,
               nfoot=95, ffoot=150, hl=("legs",))
    f2 = f'<g transform="rotate(-9 85 {GY})">' + ground(GY, -10, 180) + b + "</g>" + badge(130, 22, "膝を前へ引き上げ", GRN)
    return [(S(f1, vb), "① 前傾して<br>地面を強く押す"), (S(f2, vb), "② 膝を高く引き上げ<br>腕を大きく振る")]


def bounding():
    vb = "0 -10 170 160"
    a, _ = fig(70, GY, nt=-38, ns=-42, ft=82, fs=-8, torso=18, nu=75, nf=125, fu=-55, ff=-25,
               nfoot=120, ffoot=95, hl=("legs",))
    f1 = ground(GY) + a + arrow(110, 70, 150, 50, RED)
    b, _ = fig(85, GY, nt=62, ns=28, ft=-45, fs=-82, torso=14, nu=-50, nf=-20, fu=80, ff=120, lift=26,
               nfoot=110, ffoot=150, hl=("legs",))
    f2 = ground(GY) + b + badge(85, 12, "遠くへ", GRN)
    return [(S(f1, vb), "① 片足で強く蹴って<br>斜め前へ"), (S(f2, vb), "② 空中で大きく一歩<br>反対足で着地→すぐ次へ")]


# ===================== B. フットワーク =====================
def split_step():
    a, _ = fig(85, GY, nt=12, ns=2, ft=-12, fs=-2, torso=0, nu=40, nf=30, fu=-30, ff=-25, front=True,
               racket=6, hl=("legs",))
    f1 = ground(GY) + a
    b, _ = fig(85, GY, nt=3, ns=2, ft=-3, fs=-2, torso=0, nu=40, nf=30, fu=-30, ff=-25, front=True,
               racket=6, lift=10, hl=("legs",))
    f2 = ground(GY) + b + badge(85, 14, "相手が打つ瞬間", RED)
    c, _ = fig(85, GY, nt=46, ns=6, ft=-46, fs=-6, torso=0, nu=40, nf=30, fu=-30, ff=-25, front=True,
               racket=6, hl=("legs",))
    f3 = ground(GY) + c + arrow(120, 118, 158, 118, RED) + badge(140, 104, "蹴り出す")
    return [(S(f1, VBJ), "① 軽く膝を曲げ<br>ラケットを構える"), (S(f2, VBJ), "② その場で<br>小さくジャンプ"),
            (S(f3, VBJ), "③ 両足同時に着地<br>片足で蹴って1歩目")]


def six_point():
    return [(court_svg(260), "")]


def lunge():
    a, _ = fig(62, GY, nt=78, ns=-4, ft=-58, fs=-70, torso=14, nu=100, nf=110, fu=-30, ff=-40,
               racket=62, hl=("legs",))
    f1 = ground(GY) + a + badge(120, 40, "膝=つま先の向き", GRN)
    b, _ = fig(85, GY, nt=14, ns=-8, ft=-8, fs=-14, torso=6, nu=40, nf=100, fu=-30, ff=-25,
               racket=40, hl=("legs",))
    f2 = ground(GY) + b + arrow(120, 90, 42, 90, RED) + badge(90, 40, "かかとで蹴って戻る", RED)
    return [(S(f1, VBJ), "① 前へ大きく1歩<br>ラケットを前に伸ばす"), (S(f2, VBJ), "② 1歩で素早く<br>ベースへ戻る")]


def cross_touch():
    return [(cross_svg(220), "")]


# ===================== C. 体幹 =====================
def plank():
    a, P = fig(78, GY, nt=-76, ns=-76, ft=-76, fs=-76, torso=76, head=84, nu=0, nf=90, fu=0, ff=90,
               nfoot=100, ffoot=100, hl=("core",))
    f1 = ground(GY) + a + badge(100, 54, "一直線", GRN)
    b, P = fig(78, GY, nt=-87, ns=-87, ft=-87, fs=-87, torso=52, head=66, nu=0, nf=90, fu=0, ff=90,
               nfoot=100, ffoot=100, hl=("core",))
    f2 = ground(GY) + b + badge(100, 54, "NG:腰が落ちる", RED)
    return [(S(f1), "① 肘は肩の真下<br>頭からかかとまで一直線"), (S(f2), "NG 腰が落ちる/反る<br>→ そこで終了")]


def side_plank():
    def make(sag):
        sh = (50, 110)
        feet = (150, 125)
        if not sag:
            hip = (sh[0] + 0.34 * (feet[0] - sh[0]), sh[1] + 0.34 * (feet[1] - sh[1]))
        else:
            hip = (83, 124)
        d = (feet[0] - sh[0], feet[1] - sh[1])
        n = math.hypot(*d)
        head = (sh[0] - 15 * d[0] / n, sh[1] - 15 * d[1] / n - 3)
        s = ground(GY)
        s += line((34, 127), (62, 127), NAVY, 5)           # forearm on floor
        s += line((50, 127), sh, NAVY, 5)                    # upper arm
        col = HL if not sag else RED
        s += line(sh, hip, col, 7) + line(hip, feet, col, 7)
        s += line((feet[0] - 2, feet[1] + 2), (feet[0] + 6, feet[1] + 2), NAVY, 4)
        s += circle(head[0], head[1], 7, "#fff", NAVY, 2.5)
        s += line(sh, (50, 76), FAR, 4.5)                     # top arm up
        s += badge(110, 70, "NG:腰が落ちる" if sag else "腰を高く一直線", RED if sag else GRN)
        return s
    return [(S(make(False)), "① 肘を肩の真下に<br>足を重ねて腰を持ち上げる"), (S(make(True)), "NG 腰が落ちる<br>→ 浅い時間でOK")]


def dead_bug():
    def legs_up(extra):
        return extra
    a, _ = fig(95, GY, hy=GY - 7, nt=180, ns=90, ft=180, fs=90, torso=-90, head=-90, nu=180, nf=180, fu=180, ff=180,
               nfoot=0, ffoot=0, hl=("core",))
    f1 = ground(GY) + a + badge(95, 50, "腰は床に押し付ける", GRN)
    b, _ = fig(95, GY, hy=GY - 7, nt=180, ns=90, ft=102, fs=102, torso=-90, head=-90, nu=-100, nf=-100, fu=180, ff=180,
               nfoot=0, ffoot=0, hl=("core",))
    f2 = ground(GY) + b + arrow(60, 82, 24, 82, RED, 2) + arrow(120, 86, 156, 86, RED, 2)
    return [(S(f1), "① 仰向けで<br>腕は天井・膝は90°"), (S(f2), "② 反対の手と脚を<br>ゆっくり伸ばす")]


def bird_dog():
    a, _ = fig(62, GY, hy=GY - 27, nt=0, ns=-90, ft=0, fs=-90, torso=82, head=88, nu=0, nf=0, fu=0, ff=0,
               nfoot=-90, ffoot=-90, hl=("core",))
    f1 = ground(GY) + a + badge(100, 70, "背中は水平", GRN)
    b, _ = fig(62, GY, hy=GY - 27, nt=0, ns=-90, ft=-86, fs=-92, torso=84, head=90, nu=90, nf=92, fu=0, ff=0,
               nfoot=-90, ffoot=-90, hl=("core",))
    f2 = ground(GY) + b + arrow(120, 75, 156, 75, RED, 2) + arrow(30, 80, 6, 80, RED, 2)
    return [(S(f1), "① 四つ這い<br>背中をまっすぐ"), (S(f2), "② 対角の手と脚を伸ばし<br>2秒キープ")]


def pallof():
    def top(extended):
        s = rect(8, 56, 14, 38, fill="#c9b79c", stroke="#8a6d3b", rx=2) + text(15, 108, "固定", 9, "#8a6d3b")
        cx = 112
        s += f'<ellipse cx="{cx}" cy="104" rx="26" ry="10" fill="{HL}" fill-opacity="0.85" stroke="{HL}" stroke-width="2"/>'
        s += circle(cx, 104, 8, "#fff", NAVY, 2.5)
        hy = 40 if extended else 78
        s += line((cx - 24, 102), (cx, hy), NAVY, 4.5) + line((cx + 24, 102), (cx, hy), NAVY, 4.5)
        s += line((22, 75), (cx, hy), "#e03131", 2.2, dash="4,3")
        s += circle(cx, hy, 4.5, "#e03131", "#e03131", 1)
        if extended:
            s += carrow(40, 100, 60, 70, 40, 52, RED, 2) + badge(65, 125, "体は回さず耐える", RED)
        else:
            s += badge(65, 125, "胸の前で構える", GRN)
        s += text(cx + 6, 140, "(真上から見た図)", 9, GRD)
        return s
    return [(S(top(False), "0 0 170 150"), "① 横向きに立ち<br>胸の前でゴムを持つ"), (S(top(True), "0 0 170 150"), "② 真っすぐ押し出して<br>回されないよう耐える")]


# ===================== D. スマッシュ威力 =====================
def med_rot():
    W = wall(150, 20, GY)
    a, _ = fig(66, GY, nt=26, ns=4, ft=-26, fs=-4, torso=-14, nu=-52, nf=-50, fu=-55, ff=-52, front=True,
               ball=True, hl=("core",))
    f1 = ground(GY) + a + W + badge(70, 24, "後ろ側の腰へ", GRN)
    b, _ = fig(76, GY, nt=26, ns=4, ft=-26, fs=-4, torso=2, nu=15, nf=22, fu=12, ff=20, front=True,
               ball=True, hl=("core",))
    f2 = ground(GY) + b + W + arrow(70, 36, 112, 36, RED) + badge(90, 24, "腰から回す", RED)
    c, _ = fig(86, GY, nt=26, ns=4, ft=-20, fs=-30, torso=14, nu=106, nf=104, fu=110, ff=105, front=True,
               hl=("core",), nfoot=90)
    f3 = (ground(GY) + c + W + circle(132, 46, 7.5, "#f59f00", "#b36b00", 2) +
          arrow(112, 56, 126, 48, RED, 2) + badge(100, 24, "壁へ全力で", RED))
    return [(S(f1), "① ボールを<br>後ろ側の腰へ"), (S(f2), "② 後ろ足で床を蹴り<br>腰→胸→腕の順に回す"), (S(f3), "③ 壁へ<br>全力で投げる")]


def overhead():
    W = wall(150, 14, GY)
    a, _ = fig(70, GY, nt=18, ns=-8, ft=-10, fs=-14, torso=-16, head=-10, nu=-158, nf=-150, fu=-160, ff=-152,
               ball=True, hl=("core", "arms"))
    f1 = ground(GY) + a + W + badge(60, 12, "胸を反らす", GRN)
    b, _ = fig(78, GY, nt=34, ns=-6, ft=-40, fs=-52, torso=10, nu=152, nf=135, fu=150, ff=132,
               ball=True, hl=("core", "arms"), nfoot=90, ffoot=130)
    f2 = ground(GY) + b + W + badge(70, 12, "反りから一気に", RED)
    c, _ = fig(80, GY, nt=38, ns=-8, ft=-30, fs=-60, torso=38, nu=45, nf=30, fu=40, ff=28,
               hl=("core", "arms"), nfoot=90, ffoot=130)
    f3 = (ground(GY) + c + W + circle(130, 32, 7.5, "#f59f00", "#b36b00", 2) +
          arrow(104, 44, 122, 35, RED, 2) + badge(70, 12, "高い所を狙う", RED))
    return [(S(f1), "① ボールを両手で<br>頭の後ろへ"), (S(f2), "② 体の反りから<br>一気に前へ"), (S(f3), "③ 壁の高い所へ<br>勢いよく投げる")]


def tube_er():
    def make(out):
        s = ""
        s += line((100, 38), (100, 100), NAVY, 7)             # torso
        s += circle(100, 22, 8, "#fff", NAVY, 2.5)
        s += line((100, 42), (66, 42), NAVY, 5)                # shoulder line
        s += line((66, 42), (66, 82), HL, 5.5)                 # upper arm
        hand = (30, 82) if out else (96, 82)
        s += line((66, 82), hand, HL, 5.5)
        s += rect(150, 72, 12, 22, fill="#c9b79c", stroke="#8a6d3b", rx=2)
        s += line((150, 83), hand, "#e03131", 2.2, dash="4,3")
        s += circle(hand[0], hand[1], 4.5, "#e03131", "#e03131", 1)
        s += rect(62, 84, 8, 14, fill="#f1f3f5", stroke=GRD, sw=1, rx=1) + text(66, 112, "タオル", 8.5, GRD)
        if out:
            s += carrow(92, 108, 64, 124, 36, 104, RED, 2) + badge(66, 138, "肘は動かさない", RED)
        else:
            s += badge(66, 138, "前腕をお腹の前へ", GRN)
        return s
    return [(S(make(False)), "① 肘を脇腹に90°<br>(タオルを挟む)"), (S(make(True)), "② 肘を固定し<br>前腕だけ外へ開く")]


def pushup():
    a, _ = fig(70, GY, nt=-63, ns=-63, ft=-63, fs=-63, torso=63, head=72, nu=0, nf=0, fu=0, ff=0,
               nfoot=100, ffoot=100, hl=("arms", "core"))
    f1 = ground(GY) + a
    b, _ = fig(70, GY, nt=-81, ns=-81, ft=-81, fs=-81, torso=81, head=88, nu=-65, nf=74, fu=-65, ff=74,
               nfoot=100, ffoot=100, hl=("arms", "core"))
    f2 = ground(GY) + b + arrow(150, 80, 150, 112, RED, 2)
    return [(S(f1), "① 手は肩幅より少し広く<br>体は一直線"), (S(f2), "② 肘を45°に開いて<br>胸を床へ→一気に押す")]


def wrist():
    def make(up_):
        s = rect(8, 74, 110, 10, fill="#c9b79c", stroke="#8a6d3b", rx=1)
        s += line((20, 66), (112, 66), NAVY, 7)
        hand_end = (136, 44) if up_ else (136, 96)
        s += line((112, 66), hand_end, HL, 6)
        s += rect(hand_end[0] - 4, hand_end[1] - (14 if up_ else 0), 8, 14, fill="#74c0fc", stroke=BLU, sw=1.5, rx=3)
        s += (arrow(150, 90, 150, 58, RED, 2) if up_ else arrow(150, 56, 150, 88, RED, 2))
        return s
    return [(S(make(False), "0 0 170 120", 170), "① 手首を下へ<br>ペットボトルを持つ"), (S(make(True), "0 0 170 120", 170), "② 手首を上へ巻き上げる<br>(逆向きも同じ回数)")]


# ===================== E. 実戦連動 =====================
def jump_smash():
    vb = "0 -52 170 202"
    a, _ = fig(70, GY, nt=38, ns=-14, ft=-8, fs=-14, torso=-14, head=-10, nu=105, nf=-172, fu=150, ff=160,
               racket=-48, hl=("legs", "core"))
    f1 = ground(GY) + a + text(100, 12, "←ネット側", 8.5, GRD, "start") if False else ground(GY) + a
    f1 = ground(GY) + a
    b, _ = fig(76, GY, nt=-5, ns=0, ft=-8, fs=-10, torso=-18, head=-12, nu=105, nf=-172, fu=150, ff=160,
               racket=-48, lift=10, nfoot=140, ffoot=140, hl=("legs", "core"))
    f2 = ground(GY) + b + arrow(140, 100, 140, 66, RED) + badge(140, 56, "床を蹴る")
    c, P = fig(86, GY, nt=-20, ns=-52, ft=30, fs=2, torso=10, head=14, nu=172, nf=178, fu=40, ff=72,
               racket=14, lift=28, nfoot=150, ffoot=100, hl=("legs", "core"))
    sx, sy = P["rtip"][0] + 4, P["rtip"][1] - 6
    shuttle = circle(sx, sy, 3.5, "#ffffff", NAVY, 1.8) + f'<polygon points="{f(sx+3)},{f(sy-2)} {f(sx+13)},{f(sy-8)} {f(sx+12)},{f(sy+4)}" fill="#fff" stroke="{NAVY}" stroke-width="1.2"/>'
    f3 = ground(GY) + c + shuttle + arrow(sx + 14, sy + 4, sx + 36, sy + 40, RED, 2.5) + badge(40, -30, "最高点で打つ", RED)
    d, _ = fig(76, GY, nt=56, ns=-26, ft=46, fs=-30, torso=24, nu=30, nf=60, fu=60, ff=80,
               racket=100, hl=("legs", "core"))
    f4 = ground(GY) + d + badge(125, 48, "膝で衝撃を吸収", GRN)
    return [(S(f1, vb, 165), "① 構え<br>肘を上げ左手でシャトルを指す"), (S(f2, vb, 165), "② 踏み切り<br>胸を反らして床を蹴る"),
            (S(f3, vb, 165), "③ 空中・最高点<br>体を回して打つ"), (S(f4, vb, 165), "④ 着地<br>すぐ次の構えへ")]


# ===================== 縄跳び =====================
def jump_rope():
    def rope(cx, top, bottom, rx=40):
        cy = (top + bottom) / 2
        ry = (bottom - top) / 2
        return (f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{rx}" ry="{f(ry)}" fill="none" stroke="#e67700" '
                f'stroke-width="2.2" stroke-dasharray="5,3"/>')
    a, P = fig(85, GY, nt=3, ns=0, ft=-3, fs=0, torso=0, nu=18, nf=78, fu=14, ff=74, lift=6,
               nfoot=135, ffoot=135, hl=("legs",))
    f1 = (ground(GY) + rope(85, 22, GY - 1) + a +
          carrow(130, 54, 150, 82, 128, 112, RED, 2) + badge(86, 12, "手首で回す", RED))
    b, P2 = fig(85, GY, nt=6, ns=-34, ft=3, fs=-38, torso=0, nu=18, nf=78, fu=14, ff=74, lift=24,
                nfoot=150, ffoot=150, hl=("legs",))
    f2 = (ground(GY) + rope(85, 6, GY - 1) + b +
          arrow(145, 100, 145, 52, RED, 2) + badge(86, -8, "二重跳び:縄を2回通す", GRN))
    return [(S(f1, VBJ), "① 基本跳び<br>肘を脇につけ手首で回す"), (S(f2, VBJ), "② 二重跳び<br>少し高く跳び、縄を2回通す")]
