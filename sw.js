/* ============================================================
   SkyReport — Service Worker
   ============================================================
   EL PROBLEMA QUE RESUELVE ESTE ARCHIVO
   -------------------------------------
   La app ya lleva varias versiones. Si el service worker guarda el
   index.html y los módulos y los sirve siempre desde la copia, la
   gente se queda con una versión vieja y no hay forma de que la
   nueva llegue: hay que decirle "borra la caché" a mano. Eso es
   inaceptable para una app que va a cambiar.

   LA ESTRATEGIA
   -------------
     HTML y JS de la app  → RED PRIMERO. Se pide a GitHub Pages; si
                            responde, se usa y se guarda una copia.
                            Si no hay red, se tira de la copia.
                            Así una versión nueva aparece en cuanto
                            se publica.
     Iconos, fuentes      → COPIA PRIMERO. No cambian casi nunca y
     y las teselas del        son lo que hace que la app abra rápido
     mapa                     y funcione sin cobertura en el sitio
                              de vuelo.
     Supabase             → NUNCA se guarda. Los datos de la
                            comunidad tienen que ser siempre los de
                            ahora, nunca una copia de ayer.

   Al cambiar VERSION se borran todas las cachés viejas solas.
   ============================================================ */

const VERSION = 'skyreport-cache-v6';

/* Qué se guarda al instalar, para que la app abra sin conexión */
const BASE = [
  './',
  './index.html',
  './srs/styles.css',
  './srs/app.js',
  './srs/data.js',
  './srs/signals.js',
  './srs/report.js',
  './srs/mapa.js',
  './srs/igc.js',
  './srs/i18n.js',
  './srs/config.js',
  './srs/supabase.js',
  './icono-192.png',
  './icono-512.png',
  './manifest.json',
];

/* ============================================================
   INSTALAR
   ============================================================ */
self.addEventListener('install', ev => {
  ev.waitUntil(
    caches.open(VERSION)
      /* addAll falla entero si UNA falla, así que van una a una */
      .then(c => Promise.all(BASE.map(u => c.add(u).catch(() => null))))
      .then(() => self.skipWaiting())
  );
});

/* ============================================================
   ACTIVAR — borra las cachés viejas
   ============================================================ */
self.addEventListener('activate', ev => {
  ev.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k !== VERSION).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

/* ============================================================
   MENSAJE DESDE LA PÁGINA
   ============================================================ */
self.addEventListener('message', ev => {
  if (ev.data && ev.data.tipo === 'SALTA_YA') {
    self.skipWaiting();
  }
});

/* ============================================================
   INTERCEPTAR PETICIONES
   ============================================================ */
self.addEventListener('fetch', ev => {
  const req = ev.request;
  if (req.method !== 'GET') return;

  let url;
  try { url = new URL(req.url); } catch (e) { return; }

  /* --- Supabase y cualquier API: siempre a la red, sin copia --- */
  if (/supabase\.co|supabase\.in/.test(url.hostname)) return;

  /* --- teselas del mapa: copia primero, y se limitan --- */
  if (/tile\.opentopomap\.org|tile\.openstreetmap\.org|arcgisonline\.com/.test(url.hostname)) {
    ev.respondWith(copiaPrimero(req));
    return;
  }

  /* --- Leaflet desde el CDN: copia primero --- */
  if (/unpkg\.com|jsdelivr\.net/.test(url.hostname)) {
    ev.respondWith(copiaPrimero(req));
    return;
  }

  /* --- el resto: si es de la propia app, red primero --- */
  if (url.origin === location.origin) {
    const esApp = /\.(html|js|css|json)$/i.test(url.pathname) || url.pathname.endsWith('/');
    ev.respondWith(esApp ? redPrimero(req) : copiaPrimero(req));
    return;
  }

  /* --- cualquier otra cosa: que siga su curso --- */
});

/* ============================================================
   ESTRATEGIAS
   ============================================================ */

/** Red primero: pide, y si contesta usa eso. Si falla, la copia.
 *  Es lo que hace que una versión nueva llegue sola. */
async function redPrimero(req) {
  try {
    const r = await fetch(req, { cache: 'no-store' });
    if (r && r.ok) {
      const c = await caches.open(VERSION);
      c.put(req, r.clone());
      return r;
    }
    throw new Error('bad response');
  } catch (e) {
    const c = await caches.match(req);
    if (c) return c;
    /* sin red y sin copia: al menos que se vea algo */
    if (req.mode === 'navigate') {
      const idx = await caches.match('./index.html');
      if (idx) return idx;
    }
    return new Response('Offline', { status: 503, statusText: 'Offline' });
  }
}

/** Copia primero: rápido y sirve sin cobertura. */
async function copiaPrimero(req) {
  const c = await caches.match(req);
  if (c) {
    /* se refresca por detrás, sin hacer esperar a nadie */
    fetch(req).then(r => {
      if (r && r.ok) caches.open(VERSION).then(cc => cc.put(req, r));
    }).catch(() => {});
    return c;
  }
  try {
    const r = await fetch(req);
    if (r && r.ok) {
      const cc = await caches.open(VERSION);
      cc.put(req, r.clone());
      limitarTeselas();
    }
    return r;
  } catch (e) {
    return new Response('', { status: 503 });
  }
}

/* ============================================================
   LÍMITE DE TESELAS
   ============================================================
   Los mapas llenan la caché enseguida. Se guardan las últimas y
   el resto se van borrando, para que la app no acabe ocupando
   cientos de megas en el teléfono de nadie. */
const MAX_TESELAS = 500;
let ultimaLimpieza = 0;

async function limitarTeselas() {
  const ahora = Date.now();
  if (ahora - ultimaLimpieza < 60000) return;      /* como mucho, una vez por minuto */
  ultimaLimpieza = ahora;
  try {
    const c = await caches.open(VERSION);
    const ks = await c.keys();
    const teselas = ks.filter(r =>
      /opentopomap|tile\.openstreetmap|arcgisonline/.test(r.url));
    if (teselas.length > MAX_TESELAS) {
      for (const r of teselas.slice(0, teselas.length - MAX_TESELAS)) await c.delete(r);
    }
  } catch (e) { /* da igual */ }
}
