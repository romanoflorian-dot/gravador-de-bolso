/* Gravador de Bolso — funciona sem internet depois da primeira visita */
const CACHE = 'gravador-de-bolso-v3';
const SHELL = ['./', './index.html', './manifest.webmanifest', './lame.min.js',
  './icon-192.png', './icon-512.png', './icon-maskable-512.png', './apple-touch-icon.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const r = e.request;
  if (r.method !== 'GET') return;
  if (r.mode === 'navigate') {
    // página: tenta a rede (para receber atualizações) e cai no que está guardado
    e.respondWith(fetch(r).then(res => {
      const cp = res.clone(); caches.open(CACHE).then(c => c.put('./index.html', cp)); return res;
    }).catch(() => caches.match('./index.html')));
    return;
  }
  // demais arquivos (ícones, MP3, fontes): o que está guardado primeiro
  e.respondWith(caches.match(r).then(hit => hit || fetch(r).then(res => {
    if (res.ok || res.type === 'opaque') { const cp = res.clone(); caches.open(CACHE).then(c => c.put(r, cp)); }
    return res;
  })));
});
