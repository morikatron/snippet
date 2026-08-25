/* π — Service Worker
   目的: ホーム画面から起動したときにオフラインでも動くようにする。
   方針:
     - インストール時に配信ファイル一式を事前キャッシュ
     - HTML / JS / CSS / manifest はネットワーク優先（オンラインなら常に最新、落ちていればキャッシュ）
     - pi_bcd.bin とアイコンは不変なのでキャッシュ優先
     - ページ遷移（navigate）がオフラインで失敗したらキャッシュ済みの "./" を返す
     - 別オリジン（Google Fonts 等）と GET 以外はそのまま素通し */

const CACHE_NAME = "pi-game-v1";

const PRECACHE = [
	"./",
	"index.html",
	"style.css",
	"app.js",
	"manifest.json",
	"pi_bcd.bin",
	"icon-192.png",
	"icon-512.png",
	"icon-maskable-512.png",
	"apple-touch-icon.png",
];

// 変更されないファイル（キャッシュ優先で返す）
const IMMUTABLE = new Set([
	"pi_bcd.bin",
	"icon-192.png",
	"icon-512.png",
	"icon-maskable-512.png",
	"apple-touch-icon.png",
]);

const scopeUrl = new URL(self.registration.scope);

function relativePath(url) {
	// scope 配下の相対パス（"" なら "./" 相当）
	return url.pathname.startsWith(scopeUrl.pathname)
		? url.pathname.slice(scopeUrl.pathname.length)
		: null;
}

self.addEventListener("install", (event) => {
	event.waitUntil(
		caches
			.open(CACHE_NAME)
			.then((cache) => cache.addAll(PRECACHE))
			.then(() => self.skipWaiting()),
	);
});

self.addEventListener("activate", (event) => {
	event.waitUntil(
		caches
			.keys()
			.then((keys) =>
				Promise.all(
					keys
						.filter((k) => k !== CACHE_NAME)
						.map((k) => caches.delete(k)),
				),
			)
			.then(() => self.clients.claim()),
	);
});

async function cacheFirst(request) {
	const cached = await caches.match(request);
	if (cached) return cached;
	const res = await fetch(request);
	if (res.ok) {
		const cache = await caches.open(CACHE_NAME);
		cache.put(request, res.clone());
	}
	return res;
}

async function networkFirst(request, fallbackKey) {
	try {
		const res = await fetch(request);
		if (res.ok) {
			const cache = await caches.open(CACHE_NAME);
			cache.put(request, res.clone());
		}
		return res;
	} catch (e) {
		const cached =
			(await caches.match(request)) ||
			(fallbackKey ? await caches.match(fallbackKey) : undefined);
		if (cached) return cached;
		throw e;
	}
}

self.addEventListener("fetch", (event) => {
	const { request } = event;
	if (request.method !== "GET") return;
	const url = new URL(request.url);
	if (url.origin !== self.location.origin) return;
	const rel = relativePath(url);
	if (rel === null) return;

	if (request.mode === "navigate") {
		event.respondWith(networkFirst(request, "./"));
		return;
	}
	if (IMMUTABLE.has(rel)) {
		event.respondWith(cacheFirst(request));
		return;
	}
	event.respondWith(networkFirst(request));
});
