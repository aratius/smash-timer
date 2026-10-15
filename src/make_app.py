import os, re, json, hashlib, zipfile, shutil, sys
sys.path.insert(0, ".")
src = open("build.py", encoding="utf-8").read()
src = src.replace("def card(col, no, title, tg, frames, steps, dose, tip, ng):",
 "CARDS = {}\ndef card(col, no, title, tg, frames, steps, dose, tip, ng):\n    CARDS[no] = dict(col=col, title=title, tags=tg, frames=frames, steps=steps, dose=dose, tip=tip, ng=ng)\n    return ''\ndef _old_card(col, no, title, tg, frames, steps, dose, tip, ng):")
src = src.replace('open("guide.html", "w", encoding="utf-8").write(html_doc)', "pass")
ns = {"__name__": "buildmod"}
exec(compile(src, "build.py", "exec"), ns)
CARDS = ns["CARDS"]; FR = ns["FR"]

def strip(svg):
    return re.sub(r'(<svg [^>]*?) width="[\d.]+" height="[\d.]+"', r'\1', svg, count=1)

DETAIL = {}
for no, c in CARDS.items():
    DETAIL[no] = dict(tags=c["tags"], frames=[[strip(s), cap] for s, cap in c["frames"]], steps=c["steps"], dose=c["dose"], tip=c["tip"], ng=c["ng"])
DETAIL[25] = dict(tags=["コート", "★★★"], frames=[[strip(s), cap] for s, cap in FR.jump_smash()],
  steps=["<b>構え:</b> スプリットステップのあと、利き腕の肘を高く上げて胸を張る。反対の手でシャトルの方向を指す。",
         "<b>踏み切り:</b> 床を強く蹴って真上〜やや後ろへ。胸を軽く反らして「ため」をつくる。",
         "<b>空中・インパクト:</b> 反りから腰→胸→腕の順に回して、最高点付近でシャトルを捉える。反対の腕は体に引き寄せてバランスをとる。",
         "<b>着地:</b> 膝を曲げて衝撃を吸収し、すぐ次の構えへ戻る(体幹と脚の筋力が効く)。"],
  dose="①シャドー(シャトルなし)で動きを確認 → ②ノックで「ジャンプ→打つ」だけ反復 → ③ゲーム形式。1回ごとに質を優先し、疲れたら中止。",
  tip="高く跳ぶだけでなく「最高点付近で打つ」タイミングを合わせると、速い球につながります。", ng="")
detail_json = json.dumps(DETAIL, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

core = open("core.js", encoding="utf-8").read()
html = open("app_template.html", encoding="utf-8").read().replace("%%CORE%%", core).replace("%%DETAIL%%", detail_json)

out = "pwa"; shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
open(f"{out}/index.html", "w", encoding="utf-8").write(html)
ver = hashlib.sha1(html.encode()).hexdigest()[:10]

open(f"{out}/sw.js", "w", encoding="utf-8").write(f"""const V = 'smash-timer-{ver}';
const ASSETS = ['./', './index.html', './manifest.webmanifest', './icon-180.png', './icon-192.png', './icon-512.png', './icon-maskable-512.png'];
self.addEventListener('install', e => {{
  e.waitUntil(caches.open(V).then(c => Promise.all(ASSETS.map(u =>
    fetch(new Request(u, {{cache: 'reload'}})).then(r => {{ if (!r.ok) throw new Error(u); return c.put(u, r); }})
  ))).then(() => self.skipWaiting()));
}});
self.addEventListener('activate', e => {{
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k)))).then(() => self.clients.claim()));
}});
self.addEventListener('fetch', e => {{
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  e.respondWith((async () => {{
    const cache = await caches.open(V);
    const hit = await cache.match(req, {{ignoreSearch: true}});
    const net = fetch(req).then(r => {{ if (r && r.ok) e.waitUntil(cache.put(req, r.clone())); return r; }}).catch(() => null);
    if (hit) {{ e.waitUntil(net); return hit; }}
    const r = await net; if (r) return r;
    if (req.mode === 'navigate') return (await cache.match('./index.html')) || Response.error();
    return Response.error();
  }})());
}});
""")
open(f"{out}/manifest.webmanifest", "w", encoding="utf-8").write(json.dumps({
  "id": "./", "name": "ジャンプスマッシュ・タイマー", "short_name": "スマッシュ", "description": "バドミントン ジャンプスマッシュ強化メニューの自動タイマー",
  "start_url": "./", "scope": "./", "display": "standalone", "orientation": "portrait",
  "background_color": "#0a1511", "theme_color": "#0a1511", "lang": "ja",
  "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}, ensure_ascii=False, indent=1))

for n in (180, 192, 512, 'maskable-512'): shutil.copy(f"icon-{n}.png", f"{out}/icon-{n}.png")

open(f"{out}/README.txt", "w", encoding="utf-8").write("""スマッシュ・タイマー(オフライン対応PWA)

【ファイル】 index.html / sw.js / manifest.webmanifest / icon-*.png (この5種類を同じ場所に置く)

【公開のしかた(どれか1つ。HTTPSが必須です)】
A. Netlify Drop (いちばん簡単・無料)
   1) https://app.netlify.com/drop を開く
   2) このフォルダ(pwa)をドラッグ&ドロップ → URLが発行される
B. GitHub Pages
   1) リポジトリを作り、これらのファイルをアップロード
   2) Settings → Pages → Branch: main / root を選ぶ

【スマホに入れる】
iPhone: Safari でURLを開く → 共有 → 「ホーム画面に追加」
Android: Chrome でURLを開く → ︙ → 「アプリをインストール」/「ホーム画面に追加」
※ 追加する前に、ネットにつないだ状態で一度開く(自動でオフライン用に保存されます)。
※ 以降は機内モード・圏外でも動きます。

【更新するとき】
index.html を差し替えて再公開 → sw.js 内のバージョン名(smash-timer-xxxx)も変える(make_app.py を使えば自動)。
""")
with zipfile.ZipFile("smash-timer-pwa.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(os.listdir(out)): z.write(f"{out}/{f}", f"smash-timer/{f}")
print("index.html bytes", len(html), "ver", ver, "cards", sorted(DETAIL))
