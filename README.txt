スマッシュ・タイマー(オフライン対応PWA)

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
