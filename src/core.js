/* ===== core: menu data + timeline + runner (pure logic, testable in node) ===== */
const LEVELS = ['小', '中', '大'];
const DAYS = ['日', '月', '火', '水', '木', '金', '土'];

// w=運動秒, r=セット間休憩秒, side=左右それぞれ行う, card=やり方カード番号
const LIB = {
  // --- ウォームアップ ---
  w_jog:   { n: '足踏みジョグ',     amt: '軽く', w: 60, r: 0, light: 1, cue: '呼吸を整えながら体を温める' },
  w_leg:   { n: 'レッグスイング',   amt: '前後・左右', w: 30, r: 0, light: 1, cue: '脚を大きく振る(壁や椅子につかまってOK)' },
  w_hip:   { n: '股関節まわし',     amt: '大きく', w: 30, r: 0, light: 1, cue: '膝で大きな円を描く' },
  w_lunge: { n: 'ランジ歩行',       amt: '10m', w: 30, r: 0, light: 1, cue: '一歩ずつ深く踏み込む' },
  w_sh:    { n: '肩まわし',         amt: '大きく', w: 20, r: 0, light: 1, cue: '肩甲骨から大きくまわす' },
  w_pogo:  { n: '軽いポゴジャンプ', amt: '10回', w: 20, r: 0, light: 1, cue: '足首だけで軽く弾む' },
  // --- ストレッチ・クールダウン ---
  s_jog:   { n: 'ジョグ(ゆっくり)', amt: '5分', w: 300, r: 0, light: 1, cue: '会話できるペースで' },
  s_calf:  { n: 'ふくらはぎストレッチ', amt: '各側', w: 20, r: 0, side: 1, light: 1, cue: 'かかとを床につけたまま伸ばす' },
  s_quad:  { n: '太もも前ストレッチ',   amt: '各側', w: 20, r: 0, side: 1, light: 1, cue: '膝を揃えて、反りすぎない' },
  s_hip:   { n: 'お尻・股関節ストレッチ', amt: '各側', w: 20, r: 0, side: 1, light: 1, cue: '背すじを伸ばして体を前へ' },
  s_sh:    { n: '肩・胸ストレッチ',     amt: '30秒', w: 30, r: 0, light: 1, cue: '腕を後ろで組んで胸を開く' },
  // --- A 脚 ---
  rope:    { n: '縄跳び',               amt: '基本跳び+二重跳び', w: 30, r: 30, card: 6, cue: 'つま先で軽く・手首で回す' },
  pogo:    { n: 'ポゴジャンプ',         amt: '20回', w: 20, r: 45, card: 3, cue: '膝を伸ばしたまま足首で弾む' },
  jsquat:  { n: 'ジャンプスクワット',   amt: '5回', w: 25, r: 90, card: 1, cue: '1回ずつ止まって全力で真上へ' },
  box:     { n: 'ボックスジャンプ',     amt: '5回', w: 30, r: 90, card: 7, cue: '全力で跳び乗り、降りは歩く' },
  depth:   { n: 'デプスジャンプ',       amt: '5回', w: 35, r: 120, card: 8, cue: '着地したら即ジャンプ' },
  sprint:  { n: 'ダッシュ',             amt: '20m', w: 12, r: 90, card: 9, cue: '全力で地面を押す' },
  bound:   { n: 'バウンディング',       amt: '10m', w: 12, r: 75, card: 10, cue: '大きく弾むように前へ' },
  bulg:    { n: 'ブルガリアンスクワット', amt: '8回', w: 25, r: 60, side: 1, card: 2, cue: '前膝を内側に入れない' },
  calf:    { n: '片脚カーフレイズ',     amt: '15回', w: 45, r: 45, side: 1, card: 4, cue: 'ゆっくり上げて、ゆっくり下ろす' },
  nordic:  { n: 'ノルディックカール',   amt: '5回', w: 30, r: 75, card: 5, cue: 'かかとを固定してゆっくり倒れる' },
  // --- B フットワーク ---
  split:   { n: 'スプリットステップ',   amt: '20回', w: 30, r: 30, card: 11, cue: '打たれる瞬間に軽く跳ぶ' },
  six:     { n: '6点フットワーク',      amt: '30秒', w: 30, r: 45, card: 12, cue: '毎回ベースに戻る' },
  lunge:   { n: 'ランジ&リカバリー',    amt: '10回', w: 30, r: 45, card: 13, cue: '踏み込んで素早く戻る' },
  cross:   { n: '十字タッチ',           amt: '20秒', w: 20, r: 30, card: 14, cue: '中央に戻って4方向にタッチ' },
  // --- C 体幹 ---
  plank:   { n: 'プランク',             amt: '30秒', w: 30, r: 30, card: 15, cue: 'お腹に力・腰を反らさない' },
  sideplank:{ n: 'サイドプランク',      amt: '25秒', w: 25, r: 30, side: 1, card: 16, cue: '頭からかかとまで一直線' },
  deadbug: { n: 'デッドバグ',           amt: '左右各8回', w: 40, r: 30, card: 17, cue: '腰を床に押しつけたまま' },
  birddog: { n: 'バードドッグ',         amt: '左右交互', w: 50, r: 30, card: 18, cue: '対角の手足をまっすぐ伸ばす' },
  pallof:  { n: 'パロフプレス',         amt: '10回', w: 30, r: 30, side: 1, card: 19, cue: '回されないように耐える' },
  // --- D 肩・腕 ---
  medrot:  { n: 'メディシンボール回旋スロー', amt: '8回', w: 25, r: 60, side: 1, card: 20, cue: '足から腰、腰から腕の順に' },
  overhead:{ n: 'オーバーヘッドスロー', amt: '6〜8回', w: 30, r: 60, card: 21, cue: '全身をしならせて投げる' },
  tube:    { n: 'チューブ外旋',         amt: '15回', w: 30, r: 30, side: 1, card: 22, cue: '脇を締めて、ゆっくり外へ' },
  pushup:  { n: 'プッシュアップ',       amt: '10回', w: 30, r: 45, card: 23, cue: '体を一直線に保つ' },
  wrist:   { n: 'リストカール',         amt: '15回', w: 40, r: 30, card: 24, cue: '手首だけをゆっくり動かす' },
  // --- E 実戦 ---
  shadow:  { n: 'ジャンプスマッシュ・シャドー', amt: '5回', w: 30, r: 60, card: 25, cue: '最高点で打つイメージで' },
  court:   { n: 'コート練習(ジャンプスマッシュ)', amt: '1ラウンド', w: 60, r: 30, card: 25, cue: '質を優先。疲れたら止める' },
};

const G_WARM = { key: 'warm', label: 'ウォームアップ', items: ['w_jog', 'w_leg', 'w_hip', 'w_lunge', 'w_sh', 'w_pogo'].map(id => ({ id, sets: [1, 1, 1] })) };
const G_STRETCH = { key: 'cool', label: 'ストレッチ', items: ['s_calf', 's_quad', 's_hip', 's_sh'].map(id => ({ id, sets: [1, 1, 1] })) };
const grp = (key, label, items) => ({ key, label, items: items.map(x => (typeof x === 'string' ? { id: x, sets: [1, 1, 1] } : { id: x[0], sets: x[1], min: x[2] })) });

// day index: 0=日 ... 6=土
const PLAN = {
  1: {
    theme: 'ジャンプ(爆発)デー', color: '#ff6a2b',
    home: [G_WARM, grp('main', 'ジャンプ', [['rope', [3, 4, 5]], ['pogo', [2, 3, 4]], ['jsquat', [2, 3, 4]]]), grp('core', '体幹', [['plank', [2, 3, 4]], ['sideplank', [2, 2, 3]]]), G_STRETCH],
    out:  [G_WARM, grp('main', 'ジャンプ', [['rope', [3, 4, 5]], ['pogo', [2, 3, 4]], ['jsquat', [2, 3, 4]], ['box', [2, 3, 4]]]), grp('core', '体幹', [['plank', [2, 3, 4]], ['sideplank', [2, 2, 3]]]), G_STRETCH],
  },
  2: {
    theme: 'フットワーク+上半身', color: '#26d0b0',
    home: [G_WARM, grp('foot', 'フットワーク', [['split', [2, 3, 4]], ['cross', [4, 5, 6]], ['lunge', [2, 3, 3]]]), grp('arm', '肩・腕', [['pushup', [2, 3, 4]], ['tube', [2, 3, 3]], ['wrist', [2, 2, 3]]]), G_STRETCH],
    out:  [G_WARM, grp('foot', 'フットワーク', [['six', [3, 4, 5]], ['split', [2, 3, 4]], ['lunge', [2, 3, 3]]]), grp('arm', '肩・腕', [['pushup', [2, 3, 4]], ['tube', [2, 3, 3]], ['wrist', [2, 2, 3]]]), G_STRETCH],
  },
  3: {
    theme: '休養 / 軽い回復', color: '#5aa2ff',
    home: [grp('rest', '回復', [['deadbug', [2, 2, 3]]]), G_STRETCH],
    out:  [grp('rest', '回復', [['s_jog', [1, 1, 1]], ['deadbug', [2, 2, 3]]]), G_STRETCH],
  },
  4: {
    theme: '脚の筋力+回旋', color: '#b197fc',
    home: [G_WARM, grp('leg', '脚の筋力', [['bulg', [2, 3, 4]], ['calf', [2, 3, 3]], ['nordic', [2, 3, 3]]]), grp('core', '体幹', [['birddog', [2, 3, 3]], ['pallof', [2, 3, 3]]]), G_STRETCH],
    out:  [G_WARM, grp('leg', '脚の筋力', [['bulg', [2, 3, 4]], ['calf', [2, 3, 3]], ['nordic', [2, 3, 3]]]), grp('rot', '回旋(壁のある場所)', [['medrot', [2, 3, 3]], ['overhead', [2, 3, 3]]]), grp('core', '体幹', [['birddog', [2, 3, 3]], ['pallof', [2, 3, 3]]]), G_STRETCH],
  },
  5: {
    theme: '休養日', color: '#5aa2ff',
    home: [G_STRETCH], out: [G_STRETCH],
  },
  6: {
    theme: '実戦+外トレ', color: '#ffc83d',
    home: [G_WARM, grp('main', '動作づくり', [['shadow', [3, 4, 6]], ['split', [2, 3, 4]], ['cross', [4, 5, 6]]]), grp('core', '体幹', [['plank', [2, 3, 3]]]), G_STRETCH],
    out:  [G_WARM, grp('main', '実戦', [['court', [3, 5, 8]]]), grp('run', '外トレ(どれか選んで)', [['sprint', [4, 6, 8]], ['bound', [3, 4, 6]], ['depth', [1, 2, 3], 2]]), G_STRETCH],
  },
  0: {
    theme: '完全休養', color: '#5aa2ff',
    home: [G_STRETCH], out: [G_STRETCH],
  },
};
const REST_DAYS = [0, 3, 5];

/** menu: [{group,label,items:[{id,sets}]}] filtered by level/opts */
function getMenu(day, place, level, opts = {}) {
  const inc = { warm: true, cool: true, ...opts };
  const src = PLAN[day][place] || PLAN[day].home;
  const out = [];
  for (const g of src) {
    if (g.key === 'warm' && !inc.warm) continue;
    if (g.key === 'cool' && !inc.cool) continue;
    const items = [];
    for (const it of g.items) {
      if (it.min != null && level < it.min) continue;
      items.push({ id: it.id, sets: it.sets[level] });
    }
    if (items.length) out.push({ key: g.key, label: g.label, items });
  }
  return out;
}

const PREP_FIRST = 10, PREP_MAIN = 15, PREP_LIGHT = 5, SWITCH = 5;

function buildTimeline(menu) {
  const flat = [];
  menu.forEach(g => g.items.forEach(it => flat.push({ ...it, group: g.label, gkey: g.key })));
  const segs = [];
  const push = s => segs.push(s);
  flat.forEach((it, xi) => {
    const L = LIB[it.id];
    const nextIt = flat[xi + 1];
    // prep
    const prep = xi === 0 ? PREP_FIRST : (L.light ? PREP_LIGHT : PREP_MAIN);
    const base = { gkey: it.gkey, ex: it.id, name: L.n, amt: L.amt, cue: L.cue, xi, xn: flat.length, group: it.group, sets: it.sets };
    push({ ...base, type: 'prep', dur: prep, set: 1, side: null });
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
    if (n.type === 'switch') n = segs[i + 2] || n;
    s.next = nextLabel(n);
  }
  const total = segs.reduce((a, s) => a + s.dur, 0);
  return { segs, total, count: flat.length };
}

function nextLabel(n) {
  const sd = n.side ? `(${n.side})` : '';
  if (n.type === 'prep') return `${n.name}`;
  if (n.type === 'work') return `${n.name}${sd} ${n.sets > 1 ? n.set + '/' + n.sets + 'セット' : ''}`.trim();
  if (n.type === 'rest') return '休憩';
  return n.name;
}

function fmt(sec) {
  sec = Math.max(0, Math.round(sec));
  const m = Math.floor(sec / 60), s = sec % 60;
  return m + ':' + String(s).padStart(2, '0');
}
function estMinutes(day, place, level, opts) {
  return Math.round(buildTimeline(getMenu(day, place, level, opts)).total / 60);
}

/** Timer runner with injectable clock. events: {type:'seg'|'count'|'done'} */
class Runner {
  constructor(segs, now) {
    this.segs = segs.map(s => ({ ...s }));
    this.now = now || (() => Date.now());
    this.i = 0; this.acc = 0; this.t0 = 0; this.running = false; this.done = false; this._beep = null; this.started = false;
  }
  seg() { return this.segs[this.i]; }
  elapsed() { return this.acc + (this.running ? this.now() - this.t0 : 0); }
  remainingMs() { return Math.max(0, this.seg().dur * 1000 - this.elapsed()); }
  totalMs() { return this.segs.reduce((a, s) => a + s.dur * 1000, 0); }
  doneMs() { let a = 0; for (let k = 0; k < this.i; k++) a += this.segs[k].dur * 1000; return a + Math.min(this.elapsed(), this.seg().dur * 1000); }
  start() { if (!this.running && !this.done) { this.t0 = this.now(); this.running = true; this.started = true; } }
  pause() { if (this.running) { this.acc += this.now() - this.t0; this.running = false; } }
  toggle() { this.running ? this.pause() : this.start(); }
  _goto(j, over) {
    this._beep = null;
    if (j >= this.segs.length) { this.done = true; this.running = false; this.i = this.segs.length - 1; this.acc = this.seg().dur * 1000; return; }
    this.i = Math.max(0, j); this.acc = over || 0; this.t0 = this.now();
  }
  skip() { this._goto(this.i + 1, 0); return [this.done ? { type: 'done' } : { type: 'seg', seg: this.seg() }]; }
  back() {
    if (this.elapsed() > 3000 || this.i === 0) this._goto(this.i, 0); else this._goto(this.i - 1, 0);
    return [{ type: 'seg', seg: this.seg() }];
  }
  addTime(sec) { this.segs[this.i].dur += sec; }
  tick() {
    const ev = [];
    if (this.done || !this.running) return ev;
    let changed = false;
    while (!this.done && this.elapsed() >= this.seg().dur * 1000) {
      const over = this.elapsed() - this.seg().dur * 1000;
      this._goto(this.i + 1, over);
      changed = true;
    }
    if (this.done) { ev.push({ type: 'done' }); return ev; }
    if (changed) ev.push({ type: 'seg', seg: this.seg() });
    const s = this.seg();
    const sec = Math.ceil(this.remainingMs() / 1000);
    if (s.dur > 4 && sec >= 1 && sec <= 3 && this._beep !== sec) { this._beep = sec; ev.push({ type: 'count', n: sec }); }
    return ev;
  }
}

if (typeof module !== 'undefined') module.exports = { LEVELS, DAYS, LIB, PLAN, REST_DAYS, getMenu, buildTimeline, fmt, estMinutes, Runner, PREP_FIRST };
