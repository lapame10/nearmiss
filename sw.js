/* ==========================================================================
   SERVICE WORKER de SkyReport
   --------------------------------------------------------------------------
   Sin esto, Android NO deja instalar la app de verdad (solo "añadir a
   pantalla de inicio", que abre el navegador con la barra). Y no funciona sin
   cobertura.

   La estrategia importa, y la elegí por un motivo concreto:

   - El HTML y el JavaScript van NETWORK-FIRST (primero la red, la copia solo
     si no hay red). Porque si se sirve la copia primero, Pam se queda con una
     version vieja y no ve los cambios. Eso ya nos pasó cuatro veces hoy.
   - Los iconos, las fuentes y Leaflet van CACHE-FIRST (la copia primero),
     porque no cambian nunca y así carga instantáneo.
   - Y los datos (Firebase, Open-Meteo) NUNCA se cachean: siempre a la red.
     Un reporte viejo o un viento viejo es peor que no tener nada.
   ========================================================================== */

const CACHE = 'skyreport-v1';

/* lo mínimo para que la app abra sin conexión */
const BASE = [
  './',
  './index.html',
  './manifest.json',
  './logo.png',
  './icono-192.png',
  './icono-512.png',
];

/* ---------- instalar: guardar lo mínimo ---------- */
self.addEventListener('install', ev => {
  ev.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(BASE).catch(() => {}))
      .then(() => self.skipWaiting())
  );
});

/* ---------- activar: borrar las copias viejas ---------- */
self.addEventListener('activate', ev => {
  ev.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

/* Las teselas del mapa son MUCHAS y pueden llenar el telefono. Se quedan con
   las 600 mas recientes y se tiran las viejas: sobra para los sitios de vuelo
   habituales y no se come el almacenamiento. */
const MAX_TESELAS = 600;
async function limpiaTeselas(){
  const c = await caches.open(CACHE);
  const ks = await c.keys();
  const teselas = ks.filter(r => /opentopomap|tile\.openstreetmap/.test(r.url));
  if (teselas.length <= MAX_TESELAS) return;
  for (const r of teselas.slice(0, teselas.length - MAX_TESELAS)) await c.delete(r);
}
self.addEventListener('message', ev => {
  if (ev.data === 'limpia-teselas') limpiaTeselas();
});

/* ---------- ¿es un dato que hay que pedir siempre a la red? ---------- */
function esDato(url){
  return url.hostname.indexOf('firebaseio') >= 0
      || url.hostname.indexOf('open-meteo') >= 0
      || url.hostname.indexOf('archive-api') >= 0;
}

/* ---------- ¿es algo que nunca cambia? ---------- */
function esFijo(url, req){
  return req.destination === 'image'
      || req.destination === 'font'
      || /\.(png|jpg|jpeg|svg|woff2?|ico)$/i.test(url.pathname)
      || url.hostname.indexOf('unpkg') >= 0
      || url.hostname.indexOf('gstatic') >= 0
      || url.hostname.indexOf('fonts.googleapis') >= 0
      /* las TESELAS del mapa (OpenTopoMap). Van cache-first para que el mapa
         se vea donde ya has estado, aunque no haya cobertura: es justo el caso
         de reportar desde un despegue sin señal. Antes no se cacheaban y el
         mapa se quedaba en blanco. */
      || url.hostname.indexOf('opentopomap') >= 0
      || url.hostname.indexOf('tile.openstreetmap') >= 0;
}

self.addEventListener('fetch', ev => {
  const req = ev.request;
  if (req.method !== 'GET') return;

  let url;
  try { url = new URL(req.url); } catch(e) { return; }
  if (url.protocol !== 'http:' && url.protocol !== 'https:') return;

  /* los datos, siempre a la red: nunca una copia */
  if (esDato(url)) return;

  /* lo fijo: la copia primero, y si no está, la red (y se guarda) */
  if (esFijo(url, req)){
    ev.respondWith(
      caches.match(req).then(copia => copia || fetch(req).then(r => {
        if (r && r.status === 200){
          const c = r.clone();
          caches.open(CACHE).then(x => x.put(req, c)).catch(() => {});
        }
        return r;
      }))
    );
    return;
  }

  /* el HTML y el JS: la red primero, la copia solo si no hay red.
     Así las actualizaciones llegan siempre. */
  ev.respondWith(
    fetch(req).then(r => {
      if (r && r.status === 200 && url.origin === location.origin){
        const c = r.clone();
        caches.open(CACHE).then(x => x.put(req, c)).catch(() => {});
      }
      return r;
    }).catch(() => caches.match(req).then(copia => copia || caches.match('./index.html')))
  );
});
