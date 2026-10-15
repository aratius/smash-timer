const V = 'smash-timer-89542042fa';
const ASSETS = ['./', './index.html', './manifest.webmanifest', './icon-180.png', './icon-192.png', './icon-512.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(V).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  e.respondWith(caches.match(req, {ignoreSearch: true}).then(hit => {
    const net = fetch(req).then(r => {
      if (r && r.ok) { const copy = r.clone(); caches.open(V).then(c => c.put(req, copy)); }
      return r;
    }).catch(() => hit || (req.mode === 'navigate' ? caches.match('./index.html') : undefined));
    return hit || net;
  }));
});
