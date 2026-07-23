const BASE = self.location.pathname.replace(/\/sw\.js$/, '');
const CACHE = 'darshan-corpus-v2';
const PRECACHE = [
  `${BASE}/`,
  `${BASE}/index.html`,
  `${BASE}/manifest.webmanifest`,
  `${BASE}/static/css/fonts.css`,
  `${BASE}/static/css/colors.css`,
  `${BASE}/static/css/typography.css`,
  `${BASE}/static/css/spacing.css`,
  `${BASE}/static/css/motion.css`,
  `${BASE}/static/css/app.css`,
  `${BASE}/static/js/base.js`,
  `${BASE}/static/js/app.js`,
  `${BASE}/static/js/strings.js`,
  `${BASE}/static/js/theme.js`,
  `${BASE}/static/js/ephemeris.js`,
  `${BASE}/static/js/path-store.js`,
  `${BASE}/static/js/diary-crypto.js`,
  `${BASE}/static/js/diary-store.js`,
  `${BASE}/static/js/presence-metrics.js`,
  `${BASE}/static/js/bells.js`,
  `${BASE}/static/js/corpus-store.js`,
  `${BASE}/static/js/inquiry-quota.js`,
  `${BASE}/static/data/daily-words.json`,
  `${BASE}/static/data/library/catalog.json`,
  `${BASE}/static/data/library/gita-ii-47.json`,
  `${BASE}/static/data/living-maps/aspiration-path.json`,
  `${BASE}/static/data/nature/house.json`,
  `${BASE}/static/data/nature/fire-agni.json`,
  `${BASE}/static/data/sangha/exploration.json`,
  `${BASE}/static/icons/icon-192.svg`,
  `${BASE}/static/icons/icon-512.svg`,
];

const API_PREFIXES = ['/ask', '/inquire', '/witness', '/retrieve', '/inquiry'];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(PRECACHE)).then(() => self.skipWaiting()),
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))),
    ).then(() => self.clients.claim()),
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);
  const path = url.pathname;
  const relative = BASE && path.startsWith(BASE) ? path.slice(BASE.length) || '/' : path;
  if (API_PREFIXES.some((p) => relative.startsWith(p) || path.startsWith(p))) return;

  event.respondWith(
    caches.match(request).then((cached) => {
      const network = fetch(request)
        .then((response) => {
          if (response.ok && url.origin === self.location.origin) {
            const clone = response.clone();
            caches.open(CACHE).then((cache) => cache.put(request, clone));
          }
          return response;
        })
        .catch(() => cached);
      return cached || network;
    }),
  );
});
