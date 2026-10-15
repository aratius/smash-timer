/* ===== core: menu data + timeline + runner (pure logic, testable in node) ===== */
const LEVELS = ['小', '中', '大'];
const DAYS = ['日', '月', '火', '水', '木', '金', '土'];

// w=運動秒, r=セット間休憩秒, side=左右それぞれ行う, card=やり方カード番号
const LIB = {
  // --- ウォームアップ ---
  w_jog:   { n: '足踏みジョグ',     amt: '軽く', w: 60, r: 0, light: 1, cue: '呼吸を整えながら体を温める' , how: 'その場で軽く足踏み、または軽いジョグ。呼吸が少し上がる程度で十分です。' },
  w_leg:   { n: 'レッグスイング',   amt: '前後・左右', w: 30, r: 0, light: 1, cue: '脚を大きく振る(壁や椅子につかまってOK)' , how: '壁や椅子につかまり、片脚を前後に大きく振ります。次に横にも振ります。左右とも行います。' },
  w_hip:   { n: '股関節まわし',     amt: '大きく', w: 30, r: 0, light: 1, cue: '膝で大きな円を描く' , how: '片膝を上げて、外へ大きく円を描くように回します。反対回しも行います。' },
  w_lunge: { n: 'ランジ歩行',       amt: '10m', w: 30, r: 0, light: 1, cue: '一歩ずつ深く踏み込む' , how: '一歩ずつ大きく踏み出して深く沈み、前へ歩きます。上体は立てたままにします。' },
  w_sh:    { n: '肩まわし',         amt: '大きく', w: 20, r: 0, light: 1, cue: '肩甲骨から大きくまわす' , how: '肘を軽く曲げ、肩甲骨から大きく前まわし・後ろまわしをします。' },
  w_skip:  { n: 'スキップ',           amt: '軽く弾む', w: 30, r: 0, light: 1, cue: '腕を大きく振って高く弾む', how: '腕を大きく振り、高く弾むスキップをします。着地は静かに、足裏全体で。' },
  w_shuf:  { n: 'サイドシャッフル',   amt: '左右往復', w: 30, r: 0, light: 1, cue: '腰を落として横へ素早く', how: '腰を落とし、足を交差させずに横へ素早く動きます。数メートルを左右に往復します。' },
  w_ramp:  { n: '加速ステップ',       amt: '50→70→90%', w: 30, r: 0, light: 1, cue: '少しずつスピードを上げる', how: '数メートルの距離で、50%→70%→90%と段階的にスピードを上げます。ここで体を爆発系に切り替えます。' },
  w_pogo:  { n: '軽いポゴジャンプ', amt: '10回', w: 20, r: 0, light: 1, cue: '足首だけで軽く弾む' , how: '膝を軽く曲げたまま、足首だけで小さく弾みます。接地は短く。' },
  // --- ストレッチ・クールダウン ---
  s_jog:   { n: 'ジョグ(ゆっくり)', amt: '5分', w: 300, r: 0, light: 1, cue: '会話できるペースで' , how: '会話できるペースでゆっくり走ります。心拍を落ち着かせます。' },
  s_calf:  { n: 'ふくらはぎストレッチ', amt: '各側', w: 20, r: 0, side: 1, light: 1, cue: 'かかとを床につけたまま伸ばす' , how: '壁に手をつき、片脚を後ろへ引きます。かかとを床につけたままふくらはぎを伸ばします。' },
  s_quad:  { n: '太もも前ストレッチ',   amt: '各側', w: 20, r: 0, side: 1, light: 1, cue: '膝を揃えて、反りすぎない' , how: '立って片方の足首を持ち、かかとをお尻へ引き寄せます。膝は揃え、腰を反らしません。' },
  s_hip:   { n: 'お尻・股関節ストレッチ', amt: '各側', w: 20, r: 0, side: 1, light: 1, cue: '足首を膝にかけ、太ももを胸へ' , how: '仰向けで片方の足首を反対の膝にかけ、太ももを胸へ引き寄せます。お尻が伸びます。' },
  s_sh:    { n: '肩・胸ストレッチ',     amt: '30秒', w: 30, r: 0, light: 1, cue: '腕を後ろで組んで胸を開く' , how: '両手を背中で組み、胸を開いて肩甲骨を寄せます。肩はすくめません。' },
  // --- A 脚 ---
  rope:    { n: '縄跳び',               amt: '基本跳び+二重跳び', w: 30, r: 30, card: 6, cue: 'つま先で軽く・手首で回す' , gear: '縄' },
  pogo:    { n: 'ポゴジャンプ',         amt: '20回', w: 20, r: 45, card: 3, cue: '膝を伸ばしたまま足首で弾む' },
  jsquat:  { n: 'ジャンプスクワット',   amt: '5回', w: 25, r: 90, card: 1, cue: '1回ずつ止まって全力で真上へ' },
  box:     { n: 'ボックスジャンプ',     amt: '5回', w: 30, r: 90, card: 7, cue: '全力で跳び乗り、降りは歩く' , gear: 'ボックス(台)' },
  depth:   { n: 'デプスジャンプ',       amt: '5回', w: 35, r: 120, card: 8, cap: 3, cue: '着地したら即ジャンプ' , gear: 'ボックス(台)' },
  sprint:  { n: 'ダッシュ',             amt: '20m', w: 12, r: 90, card: 9, cue: '全力で地面を押す' , gear: '20mの直線' },
  bound:   { n: 'バウンディング',       amt: '10m', w: 12, r: 75, card: 10, cue: '大きく弾むように前へ' , gear: '10mの直線' },
  bulg:    { n: 'ブルガリアンスクワット', amt: '8回', w: 25, r: 60, side: 1, card: 2, cue: '前膝を内側に入れない' , gear: '椅子' },
  calf:    { n: '片脚カーフレイズ',     amt: '15回', w: 45, r: 45, side: 1, card: 4, cue: 'ゆっくり上げて、ゆっくり下ろす' , gear: '段差' },
  nordic:  { n: 'ノルディックカール',   amt: '5回', w: 30, r: 75, card: 5, cap: 3, cue: 'かかとを固定してゆっくり倒れる' , gear: '足を固定できるもの' },
  // --- B フットワーク ---
  split:   { n: 'スプリットステップ',   amt: '20回', w: 30, r: 30, card: 11, cue: '打たれる瞬間に軽く跳ぶ' },
  six:     { n: '6点フットワーク',      amt: '30秒', w: 30, r: 45, card: 12, cue: '毎回ベースに戻る' },
  lunge:   { n: 'ランジ&リカバリー',    amt: '10回', w: 30, r: 45, card: 13, cue: '踏み込んで素早く戻る' },
  cross:   { n: '十字タッチ',           amt: '20秒', w: 20, r: 30, card: 14, cue: '中央に戻って4方向にタッチ' },
  skater:  { n: 'スケーターバウンド', amt: '左右交互', w: 30, r: 45, cue: '片脚で着地して2秒止まる', how: '横へ大きく跳び、片脚で着地して2秒ピタッと止まります。膝が内側に入らないように。左右交互に行います。バドミントンの着地と切り返しの練習です。' },
  // --- C 体幹 ---
  plank:   { n: 'プランク',             amt: '30秒', w: 30, r: 30, card: 15, cue: 'お腹に力・腰を反らさない' },
  sideplank:{ n: 'サイドプランク',      amt: '25秒', w: 25, r: 30, side: 1, card: 16, cue: '頭からかかとまで一直線' },
  deadbug: { n: 'デッドバグ',           amt: '左右各8回', w: 40, r: 30, card: 17, cue: '腰を床に押しつけたまま' },
  birddog: { n: 'バードドッグ',         amt: '左右交互', w: 50, r: 30, card: 18, cue: '対角の手足をまっすぐ伸ばす' },
  pallof:  { n: 'パロフプレス',         amt: '10回', w: 30, r: 30, side: 1, card: 19, cue: '回されないように耐える' , gear: 'チューブ' },
  // --- D 肩・腕 ---
  medrot:  { n: 'メディシンボール回旋スロー', amt: '8回', w: 25, r: 60, side: 1, card: 20, cue: '足から腰、腰から腕の順に' , gear: 'メディシンボール・壁' },
  overhead:{ n: 'オーバーヘッドスロー', amt: '6〜8回', w: 30, r: 60, card: 21, cue: '全身をしならせて投げる' , gear: 'メディシンボール・壁' },
  tube:    { n: 'チューブ外旋',         amt: '15回', w: 30, r: 30, side: 1, card: 22, cue: '脇を締めて、ゆっくり外へ' , gear: 'チューブ' },
  pushup:  { n: 'プッシュアップ',       amt: '10回', w: 30, r: 45, card: 23, cue: '体を一直線に保つ' },
  wrist:   { n: 'リストカール',         amt: '各15回', w: 60, r: 30, card: 24, cue: '手首だけをゆっくり動かす' , gear: 'ペットボトル' },
  bridge:  { n: 'ヒップリフト',       amt: '10回', w: 40, r: 30, cue: 'お尻を締めて、ゆっくり', how: '仰向けで膝を立て、お尻を締めて腰を持ち上げます。肩から膝まで一直線にして2秒止め、ゆっくり下ろします。ノルディックカールの代わりになるハムストリングの入門種目です。' },
  ytw:     { n: 'Y・T・W(肩甲骨)',    amt: '各5回', w: 40, r: 30, cue: '肩をすくめず、軽く', how: 'うつ伏せ(またはおじぎ姿勢)で、腕をY・T・Wの形に順番に持ち上げます。肩甲骨を寄せ、肩をすくめないこと。重さは使わず、軽く行います。スマッシュで腕を支える肩まわりの筋肉を整えます。' },
  w_thor:  { n: '胸の回旋(胸椎)',    amt: '左右', w: 30, r: 0, light: 1, cue: '胸から大きくひねる', how: '四つ這いで片手を頭の後ろに置き、肘を天井へ向けて胸を大きくひねります。腰ではなく胸から回します。左右行います。' },
  // --- E 実戦 ---
  shadow:  { n: 'ジャンプスマッシュ・シャドー', amt: '5回', w: 30, r: 60, card: 25, cue: '最高点で打つイメージで' , gear: 'ラケット' },
  court:   { n: 'コート練習', amt: 'ジャンプスマッシュ 約 6〜8球', w: 30, r: 75, card: 25, cue: '質を優先。疲れたら止める' , gear: 'ラケット・シャトル' },
};

const mk = (key, label, ids) => ({ key, label, items: ids.map(id => ({ id, sets: [1, 1, 1] })) });
const G_WARM = mk('warm', 'ウォームアップ', ['w_jog', 'w_leg', 'w_hip', 'w_lunge', 'w_sh', 'w_thor', 'w_pogo']);
const G_WARM_X = mk('warm', 'ウォームアップ(爆発系の日)', ['w_jog', 'w_leg', 'w_hip', 'w_lunge', 'w_sh', 'w_thor', 'w_pogo', 'w_skip', 'w_shuf', 'w_ramp']);
const G_STRETCH = mk('cool', 'ストレッチ', ['s_calf', 's_quad', 's_hip', 's_sh']);
const grp = (key, label, items, pick) => ({ key, label, pick: !!pick, items: items.map(x => (typeof x === 'string' ? { id: x, sets: [1, 1, 1] } : { id: x[0], sets: x[1], min: x[2], max: x[3] })) });

// day index: 0=日 ... 6=土。color は曜日の小さな目印(局面色とは別系統)
const PLAN = {
  1: {
    theme: 'ジャンプ(爆発)デー', color: '#c0eb75', note: '爆発系は疲れていない最初に。1回ごとに全力で、質を優先。',
    home: [G_WARM_X, grp('main', 'ジャンプ', [['pogo', [2, 3, 4]], ['jsquat', [2, 3, 4]], ['rope', [2, 3, 3]]]), grp('core', '体幹', [['plank', [2, 3, 4]], ['sideplank', [2, 2, 3]]]), G_STRETCH],
    out:  [G_WARM_X, grp('main', 'ジャンプ', [['pogo', [2, 3, 4]], ['jsquat', [2, 3, 4]], ['box', [2, 3, 4]], ['rope', [2, 3, 3]]]), grp('core', '体幹', [['plank', [2, 3, 4]], ['sideplank', [2, 2, 3]]]), G_STRETCH],
  },
  2: {
    theme: 'フットワーク+上半身', color: '#f783ac', note: '動きの質を丁寧に。前日の脚の張りが強ければレベルは小で。肩に痛みが出たらその種目は止めます。',
    home: [G_WARM, grp('foot', 'フットワーク', [['split', [2, 3, 4]], ['cross', [4, 5, 6]], ['skater', [2, 3, 3]], ['lunge', [2, 3, 3]]]), grp('arm', '肩・腕', [['pushup', [2, 3, 4]], ['tube', [2, 3, 3]], ['wrist', [2, 2, 3]], ['ytw', [2, 2, 3]]]), G_STRETCH],
    out:  [G_WARM, grp('foot', 'フットワーク', [['six', [3, 4, 5]], ['split', [2, 3, 4]], ['skater', [2, 3, 3]], ['lunge', [2, 3, 3]]]), grp('arm', '肩・腕', [['pushup', [2, 3, 4]], ['tube', [2, 3, 3]], ['wrist', [2, 2, 3]], ['ytw', [2, 2, 3]]]), G_STRETCH],
  },
  3: {
    theme: '休養 / 軽い回復', color: '#94a3b8', rec: 1,
    home: [grp('rest', '回復', [['deadbug', [2, 2, 3]]]), G_STRETCH],
    out:  [grp('rest', '回復', [['s_jog', [1, 1, 1]], ['deadbug', [2, 2, 3]]]), G_STRETCH],
  },
  4: {
    theme: '脚の筋力+回旋', color: '#b197fc', note: 'ゆっくり丁寧に。反動を使わず、膝とハムストリングを守ります。',
    home: [G_WARM, grp('leg', '脚の筋力', [['bulg', [2, 3, 4]], ['calf', [2, 3, 3]], ['nordic', [2, 2, 2], 1], ['bridge', [2, 2, 2], 0, 0]]), grp('core', '体幹', [['birddog', [2, 3, 3]], ['pallof', [2, 3, 3]]]), G_STRETCH],
    out:  [G_WARM, grp('rot', '回旋(壁のある場所)', [['medrot', [2, 3, 3]], ['overhead', [2, 3, 3]]]), grp('leg', '脚の筋力', [['bulg', [2, 3, 4]], ['calf', [2, 3, 3]], ['nordic', [2, 2, 2], 1], ['bridge', [2, 2, 2], 0, 0]]), grp('core', '体幹', [['birddog', [2, 3, 3]], ['pallof', [2, 3, 3]]]), G_STRETCH],
  },
  5: { theme: '休養日', color: '#94a3b8', home: [G_STRETCH], out: [G_STRETCH] },
  6: {
    theme: '実戦+外トレ', color: '#e8b4a0', note: '爆発系は最初に。木曜のハムに張りがあればダッシュ・デプスは避け、バウンディングに。',
    home: [G_WARM, grp('main', '動作づくり', [['shadow', [3, 4, 6]], ['split', [2, 3, 4]], ['cross', [4, 5, 6]]]), grp('core', '体幹', [['plank', [2, 3, 3]]]), G_STRETCH],
    out:  [G_WARM_X, grp('run', '外トレ(疲れる前に・どれか選ぶ)', [['sprint', [4, 6, 8]], ['bound', [3, 4, 6]], ['depth', [1, 2, 3], 2]], true), grp('main', '実戦', [['court', [3, 4, 6]]]), G_STRETCH],
  },
  0: { theme: '完全休養', color: '#94a3b8', home: [G_STRETCH], out: [G_STRETCH] },
};
const REST_DAYS = [0, 3, 5];

/** menu: [{key,label,items:[{id,sets}],pick,pickAll}] filtered by level/opts */
function getMenu(day, place, level, opts = {}) {
  const inc = { warm: true, cool: true, ...opts };
  const src = PLAN[day][place] || PLAN[day].home;
  const out = [];
  for (const g of src) {
    if (g.key === 'warm' && !inc.warm) continue;
    if (g.key === 'cool' && !inc.cool) continue;
    let items = [];
    for (const it of g.items) {
      if (it.min != null && level < it.min) continue;
      if (it.max != null && level > it.max) continue;
      const ov = (inc.ov || {})[it.id] || 0;
      items.push({ id: it.id, cap: LIB[it.id].cap || 8, base: it.sets[level], sets: Math.max(1, Math.min(LIB[it.id].cap || 8, it.sets[level] + (it.sets[level] > 1 || ov > 0 ? ov : 0))) });
    }
    const pickAll = g.pick ? items.map(i => i.id) : null;
    if (g.pick) {
      let pk = (inc.pick || []).filter(id => pickAll.includes(id));
      if (!pk.length) pk = [pickAll[0]];
      items = items.filter(i => pk.includes(i.id));
    }
    if (items.length) out.push({ key: g.key, label: g.label, items, pick: !!g.pick, pickAll });
  }
  return out;
}

const PREP_FIRST = 10, PREP_MAIN = 15, PREP_LIGHT = 5, SWITCH = 5;
const GEAR_OF = ids => [...new Set(ids.map(id => LIB[id].gear).filter(Boolean))];

function buildTimeline(menu) {
  const flat = [];
  menu.forEach(g => g.items.forEach(it => flat.push({ ...it, group: g.label, gkey: g.key })));
  const lightN = {}, lightI = {}, mainN = flat.filter(f => !LIB[f.id].light).length; let mainI = 0;
  flat.forEach(f => { if (LIB[f.id].light) lightN[f.gkey] = (lightN[f.gkey] || 0) + 1; });
  flat.forEach(f => { if (LIB[f.id].light) { lightI[f.gkey] = (lightI[f.gkey] || 0) + 1; f.gi = lightI[f.gkey]; f.gn = lightN[f.gkey]; } else { mainI++; f.gi = mainI; f.gn = mainN; } });
  const segs = [];
  const push = s => segs.push(s);
  flat.forEach((it, xi) => {
    const L = LIB[it.id];
    const nextIt = flat[xi + 1];
    // prep
    const prevL = xi > 0 ? LIB[flat[xi - 1].id] : null;
    let prep = xi === 0 ? PREP_FIRST : (L.light ? PREP_LIGHT : PREP_MAIN);
    if (prevL && !prevL.light && !L.light) prep = Math.min(120, Math.max(PREP_MAIN, L.r > 0 ? Math.min(prevL.r, L.r * 2) : prevL.r));   // 種目間の回復
    if (prevL && !prevL.light && L.light) prep = 10;
    const base = { light: L.light ? 1 : 0, how: L.how || '', card: L.card || 0, gkey: it.gkey, ex: it.id, name: L.n, amt: L.amt, cue: L.cue, xi, xn: flat.length, gi: it.gi, gn: it.gn, group: it.group, sets: it.sets };
    push({ ...base, type: 'prep', dur: prep, set: 1, side: null, long: xi > 0 && prep >= 40 });
    for (let s = 1; s <= it.sets; s++) {
      if (L.side) {
        push({ ...base, type: 'work', dur: L.w, set: s, side: '左' });
        push({ ...base, type: 'switch', dur: SWITCH, set: s, side: '右へ' });
        push({ ...base, type: 'work', dur: L.w, set: s, side: '右' });
      } else {
        push({ ...base, type: 'work', dur: L.w, set: s, side: null });
      }
      if (s < it.sets && L.r > 0) push({ ...base, type: 'rest', dur: L.r, set: s, side: null });
    }
  });
  // fill "next" labels
  for (let i = 0; i < segs.length; i++) {
    const s = segs[i];
    let n = segs[i + 1];
    if (!n) { s.next = 'おつかれさま!'; continue; }
    s.next = nextLabel(n, s);
  }
  const total = segs.reduce((a, s) => a + s.dur, 0);
  return { segs, total, count: flat.length };
}

function nextLabel(n, cur) {
  if (n.type === 'prep') return `${n.name}`;
  if (n.type === 'work') {
    if (cur.type === 'prep') return `運動 ${n.dur}秒` + (n.sets > 1 ? ` ・ ${n.sets}セット` : '') + (n.side ? ' ・ 左右' : '');
    if (cur.type === 'switch') return `${n.name}(右) ${n.dur}秒`;
    return `${n.name} ${n.set}/${n.sets}セット`;
  }
  if (n.type === 'rest') return `休憩 ${n.dur}秒`;
  return `反対側へ ${n.dur}秒`;
}

function fmt(sec) {
  sec = Math.max(0, Math.round(sec));
  const m = Math.floor(sec / 60), s = sec % 60;
  return m + ':' + String(s).padStart(2, '0');
}
function estMinutes(day, place, level, opts) {
  return Math.round(buildTimeline(getMenu(day, place, level, opts)).total / 60);
}

/** Timer runner with injectable clock. events: {type:'seg'|'count'|'warn'|'done'} */
class Runner {
  constructor(segs, now) {
    this.segs = segs.map(s => ({ ...s }));
    this.base = this.segs.map(s => s.dur);
    this.now = now || (() => Date.now());
    this.i = 0; this.acc = 0; this.t0 = 0; this.running = false; this.done = false;
    this._beep = null; this._warn = false; this.started = false;
    this.keys = new Set(); this.actMs = 0; this.skipped = new Set(); this._last = 0;
  }
  get sets() { return this.keys.size; }
  get finished() { const c = {}; this.keys.forEach(k => { const x = +k.split(':')[0]; c[x] = (c[x] || 0) + 1; }); const f = new Set(); this.segs.forEach(s => { if (s.type === 'work' && c[s.xi] >= s.sets) f.add(s.xi); }); return f; }
  seg() { return this.segs[this.i]; }
  elapsed() { return this.acc + (this.running ? this.now() - this.t0 : 0); }
  remainingMs() { return Math.max(0, this.seg().dur * 1000 - this.elapsed()); }
  totalMs() { return this.segs.reduce((a, s) => a + s.dur * 1000, 0); }
  doneMs() { let a = 0; for (let k = 0; k < this.i; k++) a += this.segs[k].dur * 1000; return a + Math.min(this.elapsed(), this.seg().dur * 1000); }
  _tickAct() { const t = this.now(); if (this.running && this._last) this.actMs += Math.min(1500, t - this._last); this._last = this.running ? t : 0; }
  start() { if (!this.running && !this.done) { this.t0 = this.now(); this.running = true; this.started = true; this._last = this.t0; } }
  pause() { if (this.running) { this._tickAct(); this.acc += this.now() - this.t0; this.running = false; this._last = 0; } }
  toggle() { this.running ? this.pause() : this.start(); }
  _goto(j, over, natural) {
    const prev = this.segs[this.i];
    if (prev && prev.type === 'work' && !prev.light && (!prev.side || prev.side === '右') && (natural || this.elapsed() >= prev.dur * 500) && j > this.i) this.keys.add(prev.xi + ':' + prev.set);
    this._beep = null; this._warn = false;
    if (j >= this.segs.length) { this.done = true; this.running = false; this.i = this.segs.length - 1; this.acc = this.seg().dur * 1000; return; }
    this.i = Math.max(0, j); this.acc = over || 0; this.t0 = this.now();
  }
  skip() { this._goto(this.i + 1, 0, false); return [this.done ? { type: 'done' } : { type: 'seg', seg: this.seg() }]; }
  back() {
    if (this.elapsed() > 3000 || this.i === 0) this._goto(this.i, 0); else this._goto(this.i - 1, 0);
    this.skipped.delete(this.seg().xi);
    return [{ type: 'seg', seg: this.seg() }];
  }
  /** この種目を飛ばして次の種目の準備へ */
  skipExercise() {
    const xi = this.seg().xi;
    if (!this.finished.has(xi)) this.skipped.add(xi);
    let j = this.segs.findIndex((s, k) => k > this.i && s.xi > xi);
    if (j < 0) { this._goto(this.segs.length, 0); return [{ type: 'done' }]; }
    this._goto(j, 0, false); return [{ type: 'seg', seg: this.seg() }];
  }
  jumpTo(xi) {
    const j = this.segs.findIndex(s => s.xi === xi);
    if (j < 0) return [];
    const cur = this.seg().xi, fin = this.finished;
    for (let x = cur; x < xi; x++) if (!fin.has(x)) this.skipped.add(x);
    this.skipped.delete(xi);
    this._goto(j, 0, false); return [{ type: 'seg', seg: this.seg() }];
  }
  addTime(sec) { this.segs[this.i].dur += sec; this._warn = false; }
  plannedSets() { const m = {}; this.segs.forEach(s => { if (s.type === 'work' && !s.light && s.set === s.sets && (!s.side || s.side === '右')) m[s.xi] = s.sets; }); return Object.values(m).reduce((a, b) => a + b, 0); }
  exercises() {
    const out = [];
    this.segs.forEach(s => { if (!out[s.xi]) out[s.xi] = { xi: s.xi, ex: s.ex, name: s.name, sets: s.sets, group: s.group, gkey: s.gkey, card: s.card, light: s.light }; });
    return out;
  }
  snapshot() { return { i: this.i, el: Math.round(this.elapsed()), add: this.segs.map((s, k) => s.dur - this.base[k]), keys: [...this.keys], actMs: Math.round(this.actMs), skipped: [...this.skipped] }; }
  restore(sn) {
    this.i = Math.min(sn.i, this.segs.length - 1); this.acc = sn.el; this.running = false;
    (sn.add || []).forEach((d, k) => { if (this.segs[k]) this.segs[k].dur += d; });
    this.keys = new Set(sn.keys || []); this.actMs = sn.actMs || 0; this.skipped = new Set(sn.skipped || []);
  }
  tick() {
    const ev = [];
    if (this.done || !this.running) return ev;
    this._tickAct();
    let changed = false;
    while (!this.done && this.elapsed() >= this.seg().dur * 1000) {
      const over = this.elapsed() - this.seg().dur * 1000;
      this._goto(this.i + 1, over, true);
      changed = true;
    }
    if (this.done) { ev.push({ type: 'done' }); return ev; }
    if (changed) ev.push({ type: 'seg', seg: this.seg() });
    const s = this.seg();
    const sec = Math.ceil(this.remainingMs() / 1000);
    if (s.dur > 4 && sec >= 1 && sec <= 3 && this._beep !== sec) { this._beep = sec; ev.push({ type: 'count', n: sec }); }
    if ((s.type === 'rest' || s.type === 'prep') && s.dur >= 25 && sec <= 10 && sec > 3 && !this._warn) { this._warn = true; ev.push({ type: 'warn', n: 10 }); }
    return ev;
  }
}

if (typeof module !== 'undefined') module.exports = { GEAR_OF, LEVELS, DAYS, LIB, PLAN, REST_DAYS, getMenu, buildTimeline, fmt, estMinutes, Runner, PREP_FIRST };
