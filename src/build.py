import math, subprocess, sys
sys.path.insert(0, ".")
import frames as FR
from figlib import *

CA, CB, CC, CD, CE = "#d9480f", "#0b7285", "#6741d9", "#c92a2a", "#1864ab"

CSS = """
body{font-family:"Noto Sans CJK JP",sans-serif;font-size:12px;color:#212529;margin:0;width:760px;line-height:1.55}
h1{font-size:30px;margin:0 0 4px 0;line-height:1.25}
h2{font-size:20px;margin:0}
.pb{page-break-after:always;height:1px}
.band{padding:10px 16px;color:#fff;margin:0 0 8px 0}
.band .sub{font-size:12px;opacity:.95;margin-top:2px}
.card{width:760px;border:2px solid #adb5bd;margin:0 0 10px 0;page-break-inside:avoid;border-collapse:separate;background:#fff}
.ch{color:#fff;padding:5px 10px;font-size:14px;font-weight:bold}
.ch .no{display:inline-block;background:#fff;border-radius:11px;width:22px;text-align:center;margin-right:6px;font-size:12px}
.ch .tg{font-size:10px;font-weight:normal;margin-left:6px;background:rgba(255,255,255,.25);padding:1px 6px;border-radius:8px}
.fig{text-align:center;vertical-align:top;padding:4px 2px 2px 2px}
.cap{font-size:10.5px;color:#343a40;line-height:1.35;padding-top:2px}
.txt{vertical-align:top;padding:6px 10px 6px 10px;font-size:11.5px}
.txt ol{margin:2px 0 4px 0;padding-left:18px}
.txt li{margin:0 0 1px 0}
.lbl{display:inline-block;font-size:10.5px;font-weight:bold;color:#fff;background:#495057;padding:0 7px;border-radius:7px;margin:3px 0 1px 0}
.lbl.ok{background:#2b8a3e}.lbl.ng{background:#d6336c}.lbl.dose{background:#1971c2}
.box{border:2px solid #dee2e6;background:#f8f9fa;padding:8px 12px;margin:0 0 10px 0}
.key{background:#fff4e6;border:2px solid #ffa94d;padding:8px 12px;margin:0 0 10px 0}
table.t{border-collapse:collapse;width:100%}
table.t td,table.t th{border:1px solid #ced4da;padding:4px 7px;font-size:11.5px;vertical-align:top}
table.t th{background:#e9ecef;text-align:left}
.small{font-size:10.5px;color:#495057}
"""


import re

def rs(frames_, w):
    out = []
    for sv, c in frames_:
        m = re.search(r'viewBox="([-\d. ]+)"', sv)
        vw, vh = [float(x) for x in m.group(1).split()[2:4]]
        sv = re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{w}" height="{w*vh/vw:.1f}"', sv, count=1)
        out.append((sv, c))
    return out

def tags(col, items):
    return "".join(f'<span class="tg">{t}</span>' for t in items)


def text_block(steps, dose, tip, ng):
    s = '<span class="lbl">やり方</span><ol>' + "".join(f"<li>{x}</li>" for x in steps) + "</ol>"
    s += f'<span class="lbl dose">回数の目安</span> {dose}<br>'
    s += f'<span class="lbl ok">コツ</span> {tip}<br>'
    s += f'<span class="lbl ng">NG</span> {ng}'
    return s


def card(col, no, title, tg, frames, steps, dose, tip, ng):
    n = len(frames)
    head = f'<tr><td class="ch" style="background:{col}" colspan="2"><span class="no" style="color:{col}">{no}</span>{title}{tags(col, tg)}</td></tr>'
    txt = text_block(steps, dose, tip, ng)
    if n <= 2:
        cells = "".join(f'<td class="fig" style="width:{100//n}%">{s}<div class="cap">{c}</div></td>' for s, c in frames)
        figtab = f'<table cellspacing="0" cellpadding="0" style="width:100%"><tr>{cells}</tr></table>'
        wfig = 400 if n == 2 else 290
        body = f'<tr><td style="width:{wfig}px;vertical-align:top;border-right:1px dashed #ced4da">{figtab}</td><td class="txt">{txt}</td></tr>'
    else:
        cells = "".join(f'<td class="fig" style="width:{100//n}%">{s}<div class="cap">{c}</div></td>' for s, c in frames)
        figtab = f'<table cellspacing="0" cellpadding="0" style="width:100%"><tr>{cells}</tr></table>'
        steps_html = '<span class="lbl">やり方</span><ol>' + "".join(f"<li>{x}</li>" for x in steps) + "</ol>"
        right = (f'<span class="lbl dose">回数の目安</span> {dose}<br><span class="lbl ok">コツ</span> {tip}<br>'
                 f'<span class="lbl ng">NG</span> {ng}')
        body = (f'<tr><td colspan="2" style="border-bottom:1px dashed #ced4da">{figtab}</td></tr>'
                f'<tr><td class="txt" style="width:50%">{steps_html}</td><td class="txt">{right}</td></tr>')
    return f'<table class="card" cellspacing="0" cellpadding="0" style="border-color:{col}">{head}{body}</table>'


def band(col, letter, title, sub, brk=False):
    b = "page-break-before:always;" if brk else ""
    return (f'<div class="band" style="{b}background:{col}"><h2>{letter}　{title}</h2>'
            f'<div class="sub">{sub}</div></div>')


# ---------- physics table ----------
def phys_rows():
    rows = ""
    prev = None
    for h in (30, 40, 50, 60):
        t = 2 * math.sqrt(2 * (h / 100) / 9.8)
        d = "" if prev is None else f"+{t - prev:.2f}秒"
        rows += f"<tr><td>{h} cm</td><td>{t:.2f} 秒</td><td>{d}</td></tr>"
        prev = t
    return rows


H = []
add = H.append
PB = ''

# ================= 表紙 =================
add(f'''<div style="background:#1f3a5f;color:#fff;padding:22px 22px 18px 22px;margin-bottom:12px">
<div style="font-size:12px;opacity:.9">バドミントン / 図解トレーニングガイド</div>
<h1>ジャンプスマッシュ強化メニュー</h1>
<div style="font-size:14px">高さ・滞空・威力を伸ばす　<b>部位別</b>(脚 / フットワーク / 体幹 / 肩・腕 / 実戦)× <b>家 / 外</b></div>
</div>
<div class="key"><b>結論:滞空時間は単独では鍛えられません。</b> 高さも滞空時間も「踏み切りの瞬間の上向きの速さ」で決まります。
だから狙うのは <b>①脚の爆発力 ②地面を押す時間の短さ ③それを上半身に伝える体幹</b> の3つです。
さらにスマッシュの威力は、脚→体幹→肩→肘→手首の順に力をつなぐ「運動連鎖」で決まります。</div>
<table cellspacing="0" cellpadding="0" style="width:100%"><tr>
<td style="width:56%;vertical-align:top;padding-right:10px">
<div class="box"><b>なぜ「高さ」を伸ばすのか</b><br>
重心の上昇量 h から、空中にいる時間 t は <b>t = 2√(2h/g)</b> で決まります(g=9.8)。
</div>
<table class="t"><tr><th>重心の上昇</th><th>空中にいる時間</th><th>+10cmでの増加</th></tr>{phys_rows()}</table>
<div class="small" style="margin-top:4px">物理計算による目安です。+10cmで約0.06〜0.08秒。短く見えますが、頂点付近で打てる時間の余裕が増えます。</div>
</td>
<td style="vertical-align:top">
<div class="box"><b>図の見かた</b><br>
<span style="color:{HL};font-weight:bold">■ オレンジ</span> = 主に使う(鍛える)部位<br>
<span style="color:{RED};font-weight:bold">赤い矢印</span> = 動かす向き<br>
<span style="color:{GRN};font-weight:bold">緑のラベル</span> = フォームのポイント<br>
<span style="color:{RED};font-weight:bold">赤枠ラベル</span> = 動作の合図 / NG<br>
①②③ = 動作の順番</div>
<div class="box"><b>この資料の構成</b><br>A 脚(家 / 外) → B フットワーク → C 体幹 → D 肩・腕(威力) → E 実戦動作 → 週間メニュー</div>
</td></tr></table>
<div class="small" style="margin-top:6px">※ 一般に知られているスポーツ科学の考え方(プライオメトリクス・筋力トレーニング・運動連鎖)をもとにした内容です。個別の論文を一つずつ検証したものではなく、回数や重さは目安です。痛みやケガ歴がある場合は、無理せず専門家に相談してください。</div>
{PB}''')

# ================= 全体マップ =================
add(f'''<h2 style="margin:0 0 6px 0">全体マップ:部位別にどこを鍛えるか</h2>
<table class="t">
<tr><th style="width:15%">部位</th><th style="width:24%">狙い</th><th>家でできる</th><th>外・体育館でやる</th></tr>
<tr><td style="color:{CA};font-weight:bold">A 脚</td><td>踏み切りの速さ・高さ・着地の安定</td><td>ジャンプスクワット / ブルガリアンスクワット / ポゴジャンプ / 片脚カーフレイズ / ノルディックカール / 縄跳び</td><td>ボックスジャンプ / デプスジャンプ / 坂ダッシュ / バウンディング</td></tr>
<tr><td style="color:{CB};font-weight:bold">B フットワーク</td><td>動き出し・戻り・コート全体の移動</td><td>スプリットステップ / 十字タッチ</td><td>6点フットワーク / ランジ&リカバリー(コートや体育館)</td></tr>
<tr><td style="color:{CC};font-weight:bold">C 体幹</td><td>力の伝達・空中の姿勢・着地のブレ防止</td><td>プランク / サイドプランク / デッドバグ / バードドッグ / パロフプレス</td><td>(Dの回旋スロー・オーバーヘッドスローも体幹種目)</td></tr>
<tr><td style="color:{CD};font-weight:bold">D 肩・腕</td><td>スマッシュの威力・肩のケガ予防</td><td>プッシュアップ / チューブ外旋 / リストカール</td><td>メディシンボール回旋スロー / オーバーヘッドスロー(壁のある場所)</td></tr>
<tr><td style="color:{CE};font-weight:bold">E 実戦</td><td>上の力を1本のスマッシュにつなぐ</td><td>(動作の確認・シャドー)</td><td>ジャンプスマッシュの動作分解 / ノック練習</td></tr>
</table>
<div style="height:8px"></div>
<div class="box"><b>力がつながる順番(運動連鎖)</b>:ムチのように「下から順番に」加速します。どこか1か所が弱いと、上に伝わる力が減ります。
<table class="t" style="margin-top:6px"><tr>
<td style="background:{CA};color:#fff;text-align:center"><b>① 足・脚</b><br>地面を押す</td>
<td style="text-align:center;border:none;width:4%">▶</td>
<td style="background:{CC};color:#fff;text-align:center"><b>② 体幹</b><br>反る→回す</td>
<td style="text-align:center;border:none;width:4%">▶</td>
<td style="background:{CD};color:#fff;text-align:center"><b>③ 肩・胸</b><br>腕を引き出す</td>
<td style="text-align:center;border:none;width:4%">▶</td>
<td style="background:{CD};color:#fff;text-align:center"><b>④ 肘→手首</b><br>しならせる</td>
<td style="text-align:center;border:none;width:4%">▶</td>
<td style="background:{CE};color:#fff;text-align:center"><b>⑤ ラケット</b><br>インパクト</td>
</tr><tr>
<td class="small">ジャンプ系 / スクワット系</td><td style="border:none"></td><td class="small">プランク系 / 回旋スロー</td><td style="border:none"></td><td class="small">プッシュアップ / オーバーヘッドスロー</td><td style="border:none"></td><td class="small">リストカール / 素振り</td><td style="border:none"></td><td class="small">実戦のスマッシュ練習</td>
</tr></table></div>
<div class="box"><b>ウォームアップ(5〜10分・毎回)</b><br>
①軽いジョグ or その場足踏み 2分 → ②レッグスイング(前後・左右)各10回 → ③股関節まわし 各10回 → ④ランジ歩行 10m → ⑤肩を大きくまわす 10回 → ⑥軽いポゴジャンプ 10回。<br>
<b>安全ルール:</b> 爆発系のジャンプは<b>疲れていない最初</b>にやり、回数より質を優先。痛み(膝・アキレス腱・肩・腰)が出たらその種目は中止。硬い床より体育館やマットのほうが膝・足首にやさしいです。</div>
{PB}''')

# ================= A 脚 =================
add(band(CA, "A", "脚:ジャンプの高さをつくる", "踏み切りの垂直方向の速さ=高さ・滞空時間。家では「爆発系+片脚筋力」、外では「高強度ジャンプ+ダッシュ」。", True))
add('<div class="small" style="margin:0 0 6px 0"><b>【家でやる】</b></div>')
add(card(CA, 1, "ジャンプスクワット", ["家", "爆発力", "★☆☆"], FR.jump_squat(),
         ["足を肩幅に開き、太ももが床と平行になる手前までしゃがむ。腕は後ろへ引く",
          "腕を振り上げながら、床を強く蹴って真上に跳ぶ(つま先まで伸ばす)",
          "つま先→足裏全体の順に、膝を曲げて静かに着地する"],
         "5回 × 3〜4セット(セット間 1〜2分)",
         "1回ごとに止まって構え直す(連続で跳ばない)。リュックに少し荷物を入れて負荷を足してもOK。",
         "膝が内側に入る / 着地でドスンと音がする。"))
add(card(CA, 2, "ブルガリアンスクワット", ["家", "片脚筋力", "★★☆"], FR.bulgarian(),
         ["椅子に後ろ足の甲をのせ、前足を一歩半ほど前に出す",
          "上体は少し前傾し、真下へゆっくり沈む(前膝がつま先より少し前に出る程度)",
          "前足のかかと〜足裏全体で床を押して立ち上がる"],
         "左右 8回 × 3セット",
         "前脚の力が主役。軽ければリュックや本を抱えて負荷を足す。バランスは壁や椅子の背で支えてOK。",
         "前膝が内に入る / 後ろ足で床を蹴って立つ。"))
add(card(CA, 3, "ポゴジャンプ", ["家", "足首のバネ", "★☆☆"], FR.pogo(),
         ["足を腰幅に開き、背すじを伸ばして立つ",
          "膝はほぼ伸ばしたまま、足首のバネだけで小さく連続ジャンプ",
          "着地したらすぐ跳ぶ(接地を短く)。つま先は上に引いて着地"],
         "20回 × 3セット",
         "「床が熱い」イメージで接地を一瞬に。高さは3〜5cmで十分。",
         "膝を大きく曲げ伸ばしして跳ぶ(スクワットジャンプになる)。"))
add(card(CA, 4, "片脚カーフレイズ", ["家", "ふくらはぎ", "★☆☆"], FR.calf_raise(),
         ["階段などの段差につま先をのせ、片脚で立つ(壁に軽く手を添える)",
          "かかとをできるだけ高く素早く上げる(1秒キープ)",
          "3秒かけて、段の下までしっかり下ろす"],
         "左右 15回 × 3セット",
         "上げるのは速く、下ろすのはゆっくり。膝は曲げない。アキレス腱のバネを強くする。",
         "反動を使う / つま先が内や外に流れる。"))
add(card(CA, 5, "ノルディックカール", ["家", "ハムストリング", "★★★"], FR.nordic(),
         ["ひざ立ちになり、ソファの下などにかかとを引っかけて固定する(人に押さえてもらってもOK)",
          "体を一直線に保ち、太ももの裏で耐えながらゆっくり前へ倒れる",
          "手で床を受け止め、腕で軽く押して戻る"],
         "5回 × 3セット",
         "最初は途中まで倒れるだけでOK。ひざの下にクッションを敷く。着地時の肉離れ予防にもなる。",
         "腰が曲がってお尻が後ろに引ける。"))
add(card(CA, 6, "縄跳び(基本跳び・二重跳び)", ["家/外", "足首のバネ・リズム", "★☆☆"], FR.jump_rope(),
         ["肘を軽く曲げて脇につけ、腕は大きく回さず手首で縄を回す",
          "ふくらはぎ・足首のバネで床を小さく跳ぶ。膝はやわらかく、つま先から着地",
          "慣れたら二重跳びや片脚跳びで、接地時間をより短くする"],
         "30秒 × 3〜5セット(二重跳びは10回 × 5セット)",
         "目線は正面、背すじを伸ばす。ポゴジャンプと同じく「接地は一瞬」。ウォームアップ代わりにも使える。",
         "高く跳びすぎる / かかとをべったり着く / 硬い床で長時間(ふくらはぎ・アキレス腱を痛めやすい)。"))
add(PB)
add(band(CA, "A", "脚(つづき):外・体育館でやる", "強度が高い種目。家トレで着地とフォームが安定してから。爆発系は週2〜3回、間は48時間以上あける。"))
add(card(CA, 7, "ボックスジャンプ", ["外/体育館", "爆発力", "★★☆"], FR.box_jump(),
         ["膝の高さ以下の、安定して滑らない台の前に立つ",
          "腕を後ろへ引き、スクワットの姿勢から両足で台に跳び乗る",
          "台の上で膝を曲げて静かに着地。立ち上がってから「歩いて」降りる(跳び降りない)"],
         "5回 × 3セット(低い台から始める)",
         "高く跳ぶことが目的。台の中央に乗る。動く台・ぐらつく台は使わない。",
         "疲れてからの連続ジャンプ / 跳び降りて衝撃を受ける。"))
add(card(CA, 8, "デプスジャンプ", ["外/体育館", "上級", "★★★"], FR.depth_jump(),
         ["20〜30cm程度の台の端に立つ",
          "「跳ばずに」一歩踏み出して落ちる",
          "両足で着地した瞬間、できるだけ短い接地時間で全力ジャンプ"],
         "5回 × 2〜3セット(週1〜2回まで)",
         "ジャンプスクワット・ボックスジャンプで着地が安定してから。台は低めで十分。",
         "着地で深くしゃがみ込む(接地が長い) / 台が高すぎる。"))
add(card(CA, 9, "坂ダッシュ(または平地ダッシュ)", ["外", "地面を押す力", "★★☆"], FR.sprint(),
         ["緩い坂の下で、前傾して構える",
          "10〜30mを全力でダッシュ。後ろ脚で地面を強く押し、膝を引き上げる",
          "ゆっくり歩いて戻って、しっかり回復してから次の1本"],
         "5〜8本(歩いて戻る+1分休む)",
         "全力で走り切れる本数まで。フォームが崩れたらそこで終了。平地でもOK。",
         "疲れた状態で追い込む(ケガにつながる)。"))
add(card(CA, 10, "連続バウンディング", ["外", "水平+垂直", "★★☆"], FR.bounding(),
         ["片足で斜め前へ大きく跳ぶ",
          "反対の足で着地し、すぐに蹴って次の一歩へ(走るときのように手足を反対に連動)",
          "着地では膝がつま先の真上にくるように"],
         "10m × 4〜6本",
         "距離より、地面を強く押す感覚を優先。着地はやわらかく。",
         "膝が内に入る / 着地で上体が大きく起きる。"))
add('<div class="small">ジムが使える場合:バーベルスクワットやデッドリフトで、体重の1.5倍前後を扱える筋力があると、ジャンプ系の効果が出やすくなります(フォームはトレーナーに確認を)。</div>')
add(PB)

# ================= B フットワーク =================
add(band(CB, "B", "フットワーク:全体の動きを強くする", "スマッシュ前の「動き出し」と「戻り」を速く。ジャンプの質は、その前のステップで決まる。", True))
add(card(CB, 11, "スプリットステップ", ["家", "動き出し", "★☆☆"], FR.split_step(),
         ["ラケットを構え、軽く膝を曲げて立つ",
          "相手が打つ瞬間に、その場で小さくジャンプ(5〜10cm)",
          "両足同時に着地し、動きたい方向の足で床を蹴って1歩目へ"],
         "20回 × 3セット(スマホの音や友人の合図で)",
         "着地のタイミングは相手の打球と同時。足は肩幅より少し広く着地すると蹴りやすい。",
         "ジャンプが高い / 着地後に一度止まってしまう。"))
add(card(CB, 12, "6点フットワーク", ["コート/体育館", "全体", "★★☆"], FR.six_point(),
         ["コート中央(ベース)に立ち、床に6か所の目印(テープ)を貼る",
          "番号の順に、最後の1歩を大きく踏み込んでラケットを振る動作をする",
          "毎回ベースへ素早く戻る(スプリットステップを入れる)"],
         "30秒 × 3〜5セット(休憩 30〜60秒)",
         "踏み込んだらすぐ戻る。タイマーを使って時間を決めると質が上がる。1〜2は前、3〜4は横、5〜6は後ろ。",
         "上体が前のめりになる / 戻りが遅い。"))
add(card(CB, 13, "ランジ&リカバリー", ["コート/家", "前への踏み込み", "★★☆"], FR.lunge(),
         ["ベースから前へ大きく1歩踏み込む",
          "ラケットを前に伸ばして打つ動作をし、前膝は足首の真上に",
          "かかと側で床を蹴り、1歩で素早くベースへ戻る"],
         "10回 × 3セット(利き足側中心)",
         "前足のつま先と膝の向きをそろえる。戻る動作を速くするのが目的。",
         "膝が内に入る / 戻るときに上体が起きる。"))
add(card(CB, 14, "十字タッチ(狭い場所でOK)", ["家", "反応・切り返し", "★☆☆"], FR.cross_touch(),
         ["床にテープで十字を貼る(1辺1m前後)",
          "中央から外の目印へ1歩でタッチして、中央へ戻る",
          "1〜4を素早く連続で(スプリットステップを混ぜる)"],
         "20秒 × 4〜6セット",
         "視線は落とさず、頭の位置をぶらさない。慣れたら友人が番号を指示して反応力も鍛える。",
         "足元を見る / 戻りで体が流れる。"))
add(PB)

# ================= C 体幹 =================
add(band(CC, "C", "体幹:力をつなぎ、空中と着地を安定させる", "脚で生んだ力を上半身へ伝える「つなぎ役」。反り・回旋・着地のブレを抑える。すべて家でできる。", True))
add(card(CC, 15, "プランク", ["家", "体幹の安定", "★☆☆"], FR.plank(),
         ["肘を肩の真下につき、足は腰幅",
          "頭からかかとまで一直線。おへそを軽く引き込み、お尻を少し締める",
          "呼吸を止めずにキープ"],
         "30秒 × 3セット(慣れたら60秒)",
         "長く耐えるより、「正しい姿勢で」やる。つらくなったら膝つきでOK。",
         "腰が反る・落ちる(その時点で終了)。"))
add(card(CC, 16, "サイドプランク", ["家", "わき腹", "★★☆"], FR.side_plank(),
         ["横向きに寝て、肘を肩の真下につく。足は重ねる",
          "腰を持ち上げ、頭からかかとまで一直線にする",
          "上の腕は天井へ。呼吸を止めない"],
         "左右 20〜30秒 × 2〜3セット",
         "腰を高く保つ。つらければ膝をついて足を軽く曲げてOK。",
         "腰が落ちる / 体が前後に倒れる。"))
add(card(CC, 17, "デッドバグ", ["家", "腹部の安定", "★☆☆"], FR.dead_bug(),
         ["仰向けで腕は天井へ、股関節と膝を90°にする(テーブルトップ)",
          "片手を頭の方へ、反対の脚をゆっくり伸ばして床の少し上まで",
          "元に戻して反対側も。腰は床に押し付けたまま"],
         "左右 8〜10回 × 3セット",
         "腰が浮かない範囲で動かす。ゆっくり、息を止めずに。",
         "腰が反る / 速く動かして反動を使う。"))
add(card(CC, 18, "バードドッグ", ["家", "背中・お尻", "★☆☆"], FR.bird_dog(),
         ["四つ這いになり、背中をまっすぐ",
          "片手と反対の脚を水平に伸ばし、2秒キープ",
          "ゆっくり戻して反対側も"],
         "左右 8回 × 3セット",
         "骨盤が傾かないよう、おへそを軽く引き込む。ゆっくり動く。",
         "腰が反る / 骨盤が横に傾く。"))
add(card(CC, 19, "パロフプレス(回されない力)", ["家", "回旋への耐性", "★★☆"], FR.pallof(),
         ["ゴムバンドを胸の高さのドアノブなどに固定し、横向きに立つ",
          "胸の前でバンドを持ち、真っすぐ前へ押し出す",
          "2〜3秒キープして戻す(体が回らないように耐える)"],
         "左右 10回 × 3セット",
         "肋骨を締め、肩の力を抜く。ゴムの強さは「体が回されない」範囲で。",
         "体が回る / 腰が反る。"))
add(PB)

# ================= D 肩・腕 =================
add(band(CD, "D", "肩・腕:スマッシュの威力をつくる", "腕だけでなく、足→腰→胸→腕の順に力をつなぐ練習が中心。肩のケガ予防(チューブ外旋)もセットで。", True))
add(card(CD, 20, "メディシンボール回旋スロー", ["壁のある場所", "回旋の爆発力", "★★☆"], rs(FR.med_rot(), 138),
         ["壁に横向きに立ち(2〜3m離れる)、ボールを後ろ側の腰へ",
          "後ろ足で床を蹴り、腰→胸→腕の順に回す",
          "壁へ全力で投げる(はね返りを受けて繰り返す)"],
         "左右 8回 × 3セット",
         "足と腰から先に動き出す。1〜3kgのソフトなボールで十分(ない場合は空気を少し抜いたバレーボールなど)。",
         "腕だけで投げる / 腰の回転が途中で止まる。"))
add(card(CD, 21, "オーバーヘッドスロー", ["壁のある場所", "しなり", "★★☆"], rs(FR.overhead(), 138),
         ["壁に向かって立ち、ボールを両手で頭の後ろへ(軽く胸を反らす)",
          "足で踏み込み、体の反りから一気に前へ",
          "頭上の高い位置から、壁の高い所を狙って投げる"],
         "6〜8回 × 3セット",
         "ジャンプスマッシュの「反ってしなる」動きの練習。胸を張って、手首まで力を伝える。",
         "腰だけで反りすぎる(痛みが出たら中止)。"))
add(card(CD, 22, "チューブ外旋(肩のインナー)", ["家", "肩のケガ予防", "★☆☆"], rs(FR.tube_er(), 150),
         ["ゴムを体の内側のドアノブなどに固定し、肘を脇腹につけて90°に曲げる(タオルを挟む)",
          "肘を動かさず、前腕だけをゆっくり外へ開く",
          "ゆっくり元に戻す"],
         "15回 × 3セット(軽い負荷)",
         "スマッシュで酷使する肩の奥の筋肉(回旋筋腱板)を鍛える。軽くていいので丁寧に。",
         "肘が体から離れる / 肩がすくむ。"))
add(card(CD, 23, "プッシュアップ", ["家", "押す力", "★☆☆"], rs(FR.pushup(), 150),
         ["手は肩幅より少し広く、頭からかかとまで一直線",
          "肘を45°くらいに開いて、胸を床へ近づける",
          "一気に押し上げる"],
         "10回 × 3セット(きつければ膝つき)",
         "体幹も同時に使う。降りるのはゆっくり、上がるのは速く。",
         "腰が落ちる / 肩がすくむ。"))
add(card(CD, 24, "リストカール(手首・前腕)", ["家", "インパクトの手首", "★☆☆"], rs(FR.wrist(), 140),
         ["椅子に座り、前腕を台や太ももにのせて手首から先を出す。ペットボトルを持つ",
          "手首を下へゆっくり下ろし、上へ巻き上げる",
          "手のひらを下に向けて、逆向きも同じ回数"],
         "15回 × 2〜3セット(軽い重さ)",
         "手首の力はインパクトの鋭さに直結。軽い重さで回数をこなす。ラケットの素振りも有効。",
         "重すぎて反動を使う / 痛みを我慢する。"))
add(PB)

# ================= E 実戦 =================
add(band(CE, "E", "実戦:ジャンプスマッシュ動作を分解する", "ここまでで鍛えた力を、1本のスマッシュにまとめる。まずはシャドー(素振り)で動きを確認してから、ノックで。"))
jf = FR.jump_smash()
cells = "".join(f'<td class="fig" style="width:25%">{s}<div class="cap">{c}</div></td>' for s, c in jf)
add(f'''<table class="card" cellspacing="0" cellpadding="0" style="border-color:{CE}">
<tr><td class="ch" style="background:{CE}"><span class="no" style="color:{CE}">25</span>ジャンプスマッシュの流れ(右利きの例)<span class="tg">コート</span><span class="tg">★★★</span></td></tr>
<tr><td style="border-bottom:1px dashed #ced4da"><table cellspacing="0" cellpadding="0" style="width:100%"><tr>{cells}</tr></table></td></tr>
<tr><td class="txt">
<span class="lbl">ポイント</span>
<ol>
<li><b>構え:</b> スプリットステップのあと、利き腕の肘を高く上げて胸を張る。反対の手でシャトルの方向を指す。</li>
<li><b>踏み切り:</b> 床を強く蹴って真上〜やや後ろへ。胸を軽く反らして「ため」をつくる。</li>
<li><b>空中・インパクト:</b> 反りから腰→胸→腕の順に回して、最高点付近でシャトルを捉える。反対の腕は体に引き寄せてバランスをとる。</li>
<li><b>着地:</b> 膝を曲げて衝撃を吸収し、すぐ次の構えへ戻る(ここで体幹と脚の筋力が効く)。</li>
</ol>
<span class="lbl dose">練習のしかた</span> ①まず<b>シャドー</b>(シャトルなし)で動きを確認 → ②ノックで「ジャンプ→打つ」だけ反復 → ③ゲーム形式。1回ごとに質を優先し、疲れたら中止。<br>
<span class="lbl ok">高さを活かすコツ</span> 高く跳ぶだけでなく、「最高点付近で打つ」タイミングを合わせると、速い球につながります。
</td></tr></table>''')
add(PB)

# ================= 週間メニュー =================
add(f'''<h2 style="margin:0 0 6px 0;page-break-before:always">週間メニュー例(週5日)</h2>
<table class="t">
<tr><th style="width:9%">曜日</th><th style="width:23%">テーマ</th><th>内容(番号は種目No.)</th></tr>
<tr><td><b>月</b></td><td style="color:{CA};font-weight:bold">ジャンプ(爆発)デー</td><td>ウォームアップ → 縄跳び(6) → ポゴ(3) → ジャンプスクワット(1) → ボックスジャンプ(7) → 体幹(プランク15・サイドプランク16)</td></tr>
<tr><td><b>火</b></td><td style="color:{CB};font-weight:bold">フットワーク+上半身</td><td>6点(12)・スプリットステップ(11)・ランジ(13) → プッシュアップ(23)・チューブ外旋(22)・リストカール(24)</td></tr>
<tr><td><b>水</b></td><td>休養 or 軽い練習</td><td>ストレッチ・軽い体幹(デッドバグ17など)。疲れを残さない</td></tr>
<tr><td><b>木</b></td><td style="color:{CC};font-weight:bold">脚の筋力+回旋</td><td>ブルガリアン(2)・片脚カーフ(4)・ノルディック(5) → 回旋スロー(20)・オーバーヘッド(21) → バードドッグ(18)・パロフ(19)</td></tr>
<tr><td><b>金</b></td><td>休養</td><td>しっかり休む(爆発系のため疲労を抜く)</td></tr>
<tr><td><b>土</b></td><td style="color:{CE};font-weight:bold">実戦+外トレ</td><td>コート練習(ジャンプスマッシュ25)。外ならダッシュ(9)・バウンディング(10)・デプスジャンプ(8)のどれか。練習直前に重い跳躍はしない</td></tr>
<tr><td><b>日</b></td><td>完全休養</td><td>睡眠と食事で回復</td></tr>
</table>
<div class="small" style="margin-top:3px">最小版(週3日)なら:月=ジャンプ+体幹 / 木=脚の筋力+回旋+体幹 / 土=実戦。爆発系(ジャンプ・ダッシュ)は週2〜3回、間は48時間以上あけます。</div>
<div style="height:8px"></div>
<div class="box"><b>効果の確認と進め方</b>
<table class="t" style="margin-top:4px">
<tr><th style="width:24%">測るもの</th><th>やり方</th></tr>
<tr><td>垂直跳びの高さ</td><td>スマホ動画やジャンプ計測アプリで、2週間に1回。同じ条件(時間帯・靴)で測る。4〜6週間で変化が出やすい。</td></tr>
<tr><td>体幹</td><td>プランクのキープ時間、サイドプランクの左右差。</td></tr>
<tr><td>フットワーク</td><td>6点フットワークを30秒間で何周できるか(フォームを崩さず)。</td></tr>
<tr><td>威力</td><td>回旋スローの壁への球速感、シャトルの飛距離など。毎回同じ条件で。</td></tr>
</table>
<div style="margin-top:4px"><b>伸ばし方:</b>2〜4週間ごとに、①回数・セット数 ②台の高さ ③重さ のうち<b>1つだけ</b>少し上げる。疲れが抜けない日が続いたら、量を2〜3割減らす。</div></div>
<div class="box" style="background:#fff0f6;border-color:#faa2c1"><b>やりすぎ注意</b><br>
・痛み(膝・アキレス腱・肩・腰)が出たら、その種目は中止して休む。<br>
・デプスジャンプなど強い種目は<b>週1〜2回まで</b>。着地が安定してから。<br>
・ジャンプは回数より質。フォームが崩れたらやめる。<br>
・体調不良時、過去の大きなケガ、成長期のお子さんが行う場合は、医師やトレーナーに相談してください。</div>
''')

html_doc = f'<!doctype html><html><head><meta charset="utf-8"><title>ジャンプスマッシュ強化メニュー</title><style>{CSS}</style></head><body>{"".join(H)}</body></html>'
open("guide.html", "w", encoding="utf-8").write(html_doc)
print("html bytes", len(html_doc))
