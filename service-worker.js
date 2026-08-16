/* 花光首富的十个亿 - PWA Service Worker
 * 策略：同源 GET 走「网络优先 + 缓存兜底」，保证游戏更新能及时生效，
 *      离线时也能打开壳页面。Supabase 等跨域请求直接放行到网络。
 */
const CACHE = 'spendbillion-v1';
const SHELL = [
  '/',
  '/index.html',
  '/manifest.webmanifest',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
  '/icons/maskable-512.png',
  '/icons/icon.svg'
];

self.addEventListener('install', function (e) {
  e.waitUntil((async function () {
    const c = await caches.open(CACHE);
    await Promise.allSettled(SHELL.map(function (u) {
      return c.add(u).catch(function () {});
    }));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', function (e) {
  e.waitUntil((async function () {
    const ks = await caches.keys();
    await Promise.all(ks.filter(function (k) { return k !== CACHE; }).map(function (k) {
      return caches.delete(k);
    }));
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', function (e) {
  const req = e.request;
  if (req.method !== 'GET') return;
  const u = new URL(req.url);
  if (u.origin !== self.location.origin) return; // 跨域（Supabase 等）直接走网络
  e.respondWith((async function () {
    try {
      const r = await fetch(req);
      const cp = r.clone();
      caches.open(CACHE).then(function (c) { c.put(req, cp); });
      return r;
    } catch (err) {
      const hit = await caches.match(req);
      if (hit) return hit;
      if (req.mode === 'navigate') return caches.match('/index.html');
      return new Response('', { status: 504, statusText: 'offline' });
    }
  })());
});
