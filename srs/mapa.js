/* ============================================================
   SkyReport — el mapa
   ============================================================
   Tres modos: reportes individuales, mapa de calor y senales.
   Leaflet + teselas de OpenStreetMap. Sin clave de API, gratis,
   y funciona en GitHub Pages.
   ============================================================ */

import { SITES, EVENTOS, FASES, DIRECCIONES, TIPOS_ZONA } from './data.js';
import { est, ir, aviso, escapa, nombreEv, nombreFase, fechaLarga, hace, sitio } from './app.js';
import { distKm, excepciones, similares } from './signals.js';

/* ===== LAS CAPAS DEL MAPA =====
   OJO: CARTO ya NO es libre. Su tesela antigua contesta "API KEY REQUIRED" y
   el mapa sale con el fondo vacio (Pam lo vio en su movil). Estas tres no
   piden clave y son las que mejor le van al parapente:

     Map      OpenStreetMap estandar: limpio, se lee todo
     Terrain  OpenTopoMap: topografico, se ven crestas, valles y pendientes
              — para leer el relieve de un sitio es la mejor
     Satellite Esri World Imagery: foto real, para ver el terreno de verdad

   Todas son de uso libre con atribucion. Si algun dia hiciera falta mas
   trafico, se cambia aqui y ya. */
const CAPAS = {
  mapa: {
    n: 'Map',
    url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
    atrib: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    max: 19,
  },
  terreno: {
    n: 'Terrain',
    url: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
    atrib: '&copy; OpenTopoMap (CC-BY-SA) · &copy; OpenStreetMap',
    max: 17,
  },
  satelite: {
    n: 'Satellite',
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    atrib: 'Imagery &copy; Esri, Maxar, Earthstar Geographics',
    max: 18,
  },
};

let mapa = null, capa = null, marcadores = [];

function cargaLeaflet() {
  return new Promise((res, rej) => {
    if (window.L) return res(window.L);
    if (!document.querySelector('#leafletCss')) {
      const l = document.createElement('link');
      l.id = 'leafletCss'; l.rel = 'stylesheet';
      l.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
      document.head.appendChild(l);
    }
    const s = document.createElement('script');
    s.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
    s.onload = () => res(window.L);
    s.onerror = rej;
    document.head.appendChild(s);
  });
}

/** Crea un mapa con la capa elegida.
    OJO con el invalidateSize: Leaflet mide el contenedor UNA vez, cuando se
    crea. Si el div acaba de entrar en el DOM, o si el movil cambia de alto al
    aparecer la barra del navegador, la medida se queda vieja y el mapa sale
    gris o descuadrado. Por eso se repite la medida un momento despues y
    tambien cuando cambia el tamano de la ventana. */
function base(id, centro = [20, 0], zoom = 3, capa = 'mapa') {
  const L = window.L;
  const c = CAPAS[capa] || CAPAS.mapa;
  const m = L.map(id, { zoomControl: true, attributionControl: true }).setView(centro, zoom);
  L.tileLayer(c.url, { attribution: c.atrib, maxZoom: c.max, crossOrigin: true }).addTo(m);
  setTimeout(() => { try { m.invalidateSize(); } catch (e) {} }, 240);
  return m;
}

/* ============================================================
   FILTROS
   ============================================================ */
export function filtra(reps) {
  const f = est.filtros;
  return reps.filter(r => {
    if (r.tipo === 'safe_flight') return false;
    if (f.site && r.site !== f.site) return false;
    if (f.pais && (sitio(r.site).pais || '') !== f.pais) return false;
    if (f.ev && r.evento !== f.ev) return false;
    if (f.fase && r.fase !== f.fase) return false;
    if (f.viento && r.windDir !== f.viento) return false;
    if (f.clase && r.clase !== f.clase) return false;
    if (f.sev === 'lesion' && (!r.injury || r.injury === 'none')) return false;
    if (f.sev === 'sinlesion' && r.injury && r.injury !== 'none') return false;
    if (f.sev === 'reserva' && !r.reserve) return false;
    if (f.desde && r.fecha < f.desde) return false;
    if (f.hasta && r.fecha > f.hasta) return false;
    return true;
  });
}

/* ============================================================
   MAPA PRINCIPAL
   ============================================================ */
export async function pintaMapa() {
  /* #app lleva la clase .vista: hay que excluirla o se apaga a si misma
     y la vista sale en blanco (Pam: "no me deja hacer reporte"). */
  document.querySelectorAll('.vista').forEach(x => {
    if (x.id !== 'app') x.classList.remove('on');
  });
  document.getElementById('app').classList.add('on');
  cont.innerHTML = `<div class="cont" style="padding-top:10px;padding-bottom:40px">
    <div class="hero" style="padding:4px 0 0">
      <h1>Map</h1>
      <p class="lema">Reports, heat concentration and signals. Filter it down to the conditions you care about.</p>
    </div>

    <div class="row wrap mt2" style="gap:6px">
      ${[['reports','Reports'],['heatmap','Heatmap'],['signals','Signals']].map(([v, n]) =>
        `<button class="paso-n${est.modoMapa === v ? ' on' : ''}" data-modo="${v}">${n}</button>`).join('')}
      <button class="btn gh" id="mFiltros">Filters <span class="mono" id="nFiltros"></span></button>
    </div>

    <div class="row wrap mt" style="gap:6px">
      <span class="mini" style="align-self:center">Base</span>
      ${Object.entries(CAPAS).map(([k, c]) =>
        `<button class="paso-n${est.capaMapa === k ? ' on' : ''}" data-capa="${k}">${escapa(c.n)}</button>`).join('')}
    </div>

    <div id="panelFiltros" class="card mt oculto"></div>
    <div class="mt"><div id="mapa"></div></div>
    <p class="mini mt" id="resumen"></p>
  </div>`;

  document.querySelectorAll('[data-modo]').forEach(b => b.onclick = () => {
    est.modoMapa = b.dataset.modo; pintaMapa();
  });
  document.querySelectorAll('[data-capa]').forEach(b => b.onclick = () => {
    est.capaMapa = b.dataset.capa; pintaMapa();
  });
  document.getElementById('mFiltros').onclick = () => {
    const p = document.getElementById('panelFiltros');
    p.classList.toggle('oculto');
    if (!p.classList.contains('oculto') && !p.dataset.montado) { pintaFiltros(); p.dataset.montado = '1'; }
  };

  const L = await cargaLeaflet();
  if (mapa) { mapa.remove(); mapa = null; }
  /* 'mapa' es el id del div; la variable del modulo se llama igual, asi que
     aqui hay que ir con cuidado de no pisarlas */
  mapa = base('mapa', [30, -20], 2, est.capaMapa || 'mapa');

  const lista = filtra(est.reps);
  const capaDatos = L.layerGroup().addTo(mapa);
  capa = capaDatos;

  if (est.modoMapa === 'reports') pintaReportes(L, capaDatos, lista);
  else if (est.modoMapa === 'heatmap') pintaCalor(L, capaDatos, lista);
  else pintaSenales(L, capaDatos);

  /* filtros activos */
  const nf = Object.values(est.filtros).filter(Boolean).length;
  document.getElementById('nFiltros').textContent = nf ? `(${nf})` : '';
  documentoResumen(lista, nf);
}

function documentoResumen(lista, nf) {
  const r = document.getElementById('resumen');
  if (!r) return;
  r.innerHTML = `<b>${lista.length}</b> reports shown${nf ? ` · ${nf} filter${nf > 1 ? 's' : ''} active` : ''}.
    Rounded to about 100 m.`;
}

function pintaFiltros() {
  const p = document.getElementById('panelFiltros');
  const f = est.filtros;
  const sel = (id, etq, ops, val) => `<div class="campo" style="min-width:150px;flex:1">
    <label>${etq}</label>
    <select data-f="${id}"><option value="">Any</option>
      ${ops.map(([v, n]) => `<option value="${escapa(v)}"${val === v ? ' selected' : ''}>${escapa(n)}</option>`).join('')}
    </select></div>`;
  const paises = [...new Set(SITES.map(s => s.pais))];
  p.innerHTML = `<div class="row wrap" style="gap:12px;align-items:flex-end">
    ${sel('site', 'Site', SITES.map(s => [s.id, s.n]), f.site)}
    ${sel('pais', 'Country', paises.map(x => [x, x]), f.pais)}
    ${sel('ev', 'Event type', EVENTOS.map(e => [e.id, e.n]), f.ev)}
    ${sel('fase', 'Flight phase', FASES.map(x => [x.id, x.n]), f.fase)}
    ${sel('sev', 'Outcome', [['lesion','With injury'],['sinlesion','No injury'],['reserva','Reserve deployment']], f.sev)}
    ${sel('viento', 'Wind direction', DIRECCIONES.map(d => [d, d]), f.viento)}
    ${sel('clase', 'Wing class', ['A','B','C','D','CCC','Competition'].map(c => [c, c]), f.clase)}
    <div class="campo" style="min-width:140px;flex:1"><label>From</label>
      <input type="date" data-f="desde" value="${escapa(f.desde)}"></div>
    <div class="campo" style="min-width:140px;flex:1"><label>To</label>
      <input type="date" data-f="hasta" value="${escapa(f.hasta)}"></div>
  </div>
  <div class="row mt"><button class="btn sec" id="fLimpiar">Clear filters</button>
    <button class="btn pri" id="fAplicar">Apply</button></div>`;

  p.querySelectorAll('[data-f]').forEach(e => e.addEventListener('change', () => {
    est.filtros[e.dataset.f] = e.value;
  }));
  document.getElementById('fLimpiar').onclick = () => {
    est.filtros = { site:'', pais:'', ev:'', fase:'', sev:'', viento:'', clase:'', desde:'', hasta:'' };
    pintaMapa();
  };
  document.getElementById('fAplicar').onclick = () => pintaMapa();
}

/** Marcador circular con color segun lo que paso */
function colorDe(rep) {
  if (rep.reserve || rep.evento === 'reserve') return '#98372f';
  if (rep.evento === 'hardlanding' || rep.injury && rep.injury !== 'none') return '#a8742c';
  if (rep.tipo === 'near_miss') return '#2c4a6e';
  if (rep.tipo === 'hazard') return '#5a6169';
  return '#3d6390';
}

function pintaReportes(L, capa, lista) {
  /* si hay muchos puntos juntos, agrupo: un circulo con el numero, y al
     acercar salen los individuales. Leaflet.markercluster no esta cargado,
     asi que se hace a mano: agrupo por celda de una rejilla que depende del
     zoom y pinto el centro con el recuento. */
  const zoom = mapa.getZoom();
  const celda = zoom >= 11 ? 0 : zoom >= 8 ? 0.15 : zoom >= 5 ? 0.6 : 2;
  const grupos = {};
  lista.forEach(r => {
    const k = celda ? `${Math.round(r.lat / celda)}|${Math.round(r.lon / celda)}` : r.id;
    (grupos[k] = grupos[k] || []).push(r);
  });

  Object.values(grupos).forEach(g => {
    if (g.length > 6 && celda) {
      const la = g.reduce((a, b) => a + b.lat, 0) / g.length;
      const lo = g.reduce((a, b) => a + b.lon, 0) / g.length;
      const grave = g.filter(x => x.reserve).length;
      L.circleMarker([la, lo], {
        radius: Math.min(30, 13 + g.length / 6),
        fillColor: grave ? '#98372f' : '#2c4a6e', fillOpacity: .82,
        color: '#fff', weight: 2,
      }).addTo(capa).bindTooltip(`${g.length} reports`, { permanent: true, direction: 'center', className: 'etqCl' })
        .on('click', () => mapa.setView([la, lo], Math.min(13, mapa.getZoom() + 3)));
      return;
    }
    g.forEach(r => marcador(L, capa, r));
  });

  /* el sitio como referencia */
  SITES.forEach(s => {
    if (!lista.some(r => r.site === s.id)) return;
    L.marker([s.lat, s.lon], { opacity: 0,
      icon: L.divIcon({ className: '', html: `<div style="font:11px/1.2 var(--f);color:#5a6169;
        white-space:nowrap;font-weight:650;text-shadow:0 1px 3px #fff,0 0 8px #fff">${escapa(s.n)}</div>`,
        iconSize: [0, 0] }) }).addTo(capa);
  });
}

function marcador(L, capa, rep) {
  const m = L.circleMarker([rep.lat, rep.lon], {
    radius: 7, fillColor: colorDe(rep), fillOpacity: .9, color: '#fff', weight: 1.6,
  }).addTo(capa);
  const z = (SITES.find(s => s.id === rep.site) || {}).zonas?.find(x => x.id === rep.zona);
  m.bindPopup(`<div style="font:13px/1.5 var(--f);min-width:210px">
    <b>${escapa(nombreEv(rep.evento))}</b><br>
    <span style="color:#8c939b;font-size:12px">${escapa(fechaLarga(rep.fecha))} · ${escapa(hace(rep.fecha))}</span><br>
    ${escapa((sitio(rep.site) || {}).n || '')}${z ? ' · ' + escapa(z.n) : ''}<br>
    <span style="color:#5a6169;font-size:12px">${escapa(nombreFase(rep.fase))} ·
    ${rep.windDir ? rep.windDir + ' ' + rep.windKmh + ' km/h' : 'no wind recorded'}</span><br>
    <a href="#reporte/${escapa(rep.id)}" style="font-weight:650">View report →</a>
  </div>`);
  marcadores.push(m);
}

/** Mapa de calor: se pinta con circulos de radio progresivo. */
function pintaCalor(L, capa, lista) {
  const max = {};
  lista.forEach(r => {
    const k = `${Math.round(r.lat * 20)}|${Math.round(r.lon * 20)}`;
    max[k] = (max[k] || 0) + 1;
  });
  const tope = Math.max(1, ...Object.values(max));
  lista.forEach(r => {
    const k = `${Math.round(r.lat * 20)}|${Math.round(r.lon * 20)}`;
    const n = max[k] / tope;
    L.circle([r.lat, r.lon], {
      radius: 900 + 3400 * n,
      fillColor: n > .66 ? '#98372f' : n > .33 ? '#a8742c' : '#2c4a6e',
      fillOpacity: .16 + .26 * n, stroke: false,
    }).addTo(capa);
  });
  if (lista.length) {
    const la = lista.reduce((a, b) => a + b.lat, 0) / lista.length;
    const lo = lista.reduce((a, b) => a + b.lon, 0) / lista.length;
    mapa.setView([la, lo], 4);
  }
}

function pintaSenales(L, capa) {
  const sigs = (est.filtros.site ? est.senales.filter(s => s.site === est.filtros.site) : est.senales);
  sigs.forEach(s => {
    /* el color describe la EVIDENCIA, no el peligro: azul para lo
       repetido, ámbar para lo fuerte. Nunca rojo, que asusta. */
    const fr = s.fuerza || s.nivel;
    const col = fr === 'strong' ? '#a8742c' : fr === 'repeated' ? '#3d6390' : '#8c939b';
    L.circle([s.lat, s.lon], { radius: 2200, color: col, weight: 1.5,
      fillColor: col, fillOpacity: .1, dashArray: '5 5' }).addTo(capa);
    L.circleMarker([s.lat, s.lon], { radius: 9, fillColor: col, fillOpacity: .9,
      color: '#fff', weight: 2 }).addTo(capa)
      .bindPopup(`<div style="font:13px/1.5 var(--f);min-width:220px">
        <b>${escapa(s.titulo)}</b><br>
        <span style="color:#8c939b;font-size:12px">${s.n} reports ·
        ${escapa(fechaLarga(s.desde))} – ${escapa(fechaLarga(s.hasta))}</span><br>
        ${escapa(s.explicacion)}<br>
        <a href="#senal/${escapa(s.id)}" style="font-weight:650">View signal →</a>
      </div>`);
  });
  if (sigs.length) {
    const la = sigs.reduce((a, b) => a + b.lat, 0) / sigs.length;
    const lo = sigs.reduce((a, b) => a + b.lon, 0) / sigs.length;
    mapa.setView([la, lo], 3);
  }
}

/* ============================================================
   MAPA PARA ELEGIR UN PUNTO
   ============================================================ */
export async function mapaElegir(F, cb) {
  const L = await cargaLeaflet();
  const s = SITES.find(x => x.id === F.site) || SITES[0];
  const m = base('mapaElegir', [F.lat || s.lat, F.lon || s.lon], F.lat ? 13 : 9);
  let mk = null;
  if (F.lat) mk = L.marker([F.lat, F.lon]).addTo(m);
  m.on('click', e => {
    const { lat, lng } = e.latlng;
    if (mk) mk.setLatLng([lat, lng]); else mk = L.marker([lat, lng]).addTo(m);
    cb(lat, lng);
  });
  (s.zonas || []).forEach(z => {
    const t = (TIPOS_ZONA.find(x => x.id === z.t) || {}).n || z.t;
    L.circleMarker([z.lat, z.lon], { radius: 6, fillColor: '#5a6169', fillOpacity: .5,
      color: '#fff', weight: 1.5 }).addTo(m)
      .bindTooltip(`${z.n} · ${t}`, { direction: 'top' });
  });
}

/* ============================================================
   MAPA PARA ELEGIR EL MOMENTO DEL EVENTO
   ============================================================
   Devuelve una función para mover el marcador desde fuera (el
   deslizador). El usuario toca el track o mueve el deslizador, y
   aquí se mueve la marca. Importante: esto NO decide el evento,
   solo deja señalarlo. */
export async function mapaEvento(puntos, idCont, alElegir) {
  const el = document.getElementById(idCont);
  if (!el || !puntos || !puntos.length) return null;
  const L = await cargaLeaflet();
  const m = base(idCont, [puntos[0].lat, puntos[0].lon], 14);

  L.polyline(puntos.map(p => [p.lat, p.lon]), { color: '#5a6169', weight: 3, opacity: .9 }).addTo(m);

  const marca = L.circleMarker([puntos[0].lat, puntos[0].lon], {
    radius: 8, fillColor: '#2c4a6e', fillOpacity: .95, color: '#fff', weight: 2.5,
  }).addTo(m);

  /* tocar el track elige el punto más cercano */
  m.on('click', (e) => {
    let mejor = 0, d = Infinity;
    puntos.forEach((p, i) => {
      const dd = Math.hypot(p.lat - e.latlng.lat, (p.lon - e.latlng.lng) * .95);
      if (dd < d) { d = dd; mejor = i; }
    });
    marca.setLatLng([puntos[mejor].lat, puntos[mejor].lon]);
    if (alElegir) alElegir(mejor);
  });

  m.fitBounds(L.latLngBounds(puntos.map(p => [p.lat, p.lon])).pad(.25));
  return (i) => { const p = puntos[i]; if (p) marca.setLatLng([p.lat, p.lon]); };
}

/* ============================================================
   MAPA DEL TRACK + BLACK BOX
   ============================================================ */
export async function mapaTrack(track, idCont) {
  const L = await cargaLeaflet();
  const m = base(idCont, [track[0].lat, track[0].lon], 14);
  const antes = track.filter(p => p.t <= 0);
  const desp = track.filter(p => p.t >= 0);
  const linea = (pts, col, dash) => L.polyline(pts.map(p => [p.lat, p.lon]),
    { color: col, weight: 3, dashArray: dash, opacity: .95 }).addTo(m);
  if (antes.length) linea(antes, '#5a6169', null);
  if (desp.length) linea(desp, '#2c4a6e', null);
  /* el evento */
  const ev = track.find(p => p.t === 0) || track[0];
  L.circleMarker([ev.lat, ev.lon], { radius: 9, fillColor: '#98372f', fillOpacity: .95,
    color: '#fff', weight: 2.5 }).addTo(m).bindTooltip('Event', { permanent: true, direction: 'top' });
  /* las marcas de tiempo */
  [-120, -60, -30, 30, 60].forEach(t => {
    const p = track.find(x => x.t === t) || track.reduce((a, b) => Math.abs(b.t - t) < Math.abs(a.t - t) ? b : a);
    if (p) L.circleMarker([p.lat, p.lon], { radius: 4, fillColor: '#fff', fillOpacity: 1,
      color: '#5a6169', weight: 1.5 }).addTo(m).bindTooltip(`T${t > 0 ? '+' : ''}${t} s`, { direction: 'top' });
  });
  m.fitBounds(L.latLngBounds(track.map(p => [p.lat, p.lon])).pad(.2));
  return m;
}

export function pintaTimeline(track, idTimeline, idExcep, tEvento) {
  const cont = document.getElementById(idTimeline);
  if (!cont || !track || track.length < 3) return;

  /* ===== LA VENTANA SE MONTA ALREDEDOR DEL MOMENTO CONFIRMADO =====
     Antes se usaba el punto de mayor caída, que es una suposición
     mala: un cravat, un roce o un problema de líneas no tienen por
     qué coincidir con una caída fuerte. Ahora el cero es el momento
     que ha confirmado la persona. */
  const cero = (tEvento != null) ? tEvento : track[Math.floor(track.length / 2)].t;
  const marcas = [-120, -60, -30, 0, 30, 60].map(off => {
    const objetivo = cero + off;
    let mejor = null, d = Infinity;
    for (const p of track) { const dd = Math.abs(p.t - objetivo); if (dd < d) { d = dd; mejor = p; } }
    return (mejor && d <= 60) ? { ...mejor, off } : { off, vacio: true };
  });
  const maxSpeed = Math.max(...track.map(p => p.hs), 1);
  const altMin = Math.min(...track.map(p => p.baroAlt));
  const altMax = Math.max(...track.map(p => p.baroAlt));

  cont.innerHTML = `<div class="tabla-scroll" style="overflow-x:auto">
    <table class="tabla">
      <tr><th>T</th><th>Altitude</th><th>Speed</th><th>Climb / sink</th><th>Heading</th></tr>
      ${marcas.map(p => p.vacio ? `<tr>
        <td class="mono"><b>${p.off === 0 ? 'EVENT' : `T${p.off > 0 ? '+' : ''}${p.off} s`}</b></td>
        <td class="mono" colspan="4" style="color:var(--ink-3)">${escapa(nombreFase ? t('common.na') : 'N/A')}</td>
      </tr>` : `<tr${p.off === 0 ? ' style="background:var(--blue-bg)"' : ''}>
        <td class="mono"><b>${p.off === 0 ? 'EVENT' : `T${p.off > 0 ? '+' : ''}${p.off} s`}</b></td>
        <td class="mono">${p.altPresion != null ? p.altPresion + ' m' : 'N/A'}</td>
        <td class="mono">${p.hs != null ? p.hs.toFixed(0) + ' km/h' : 'N/A'}</td>
        <td class="mono" style="color:${p.vs != null && p.vs < -3 ? 'var(--red)' : p.vs > 0 ? 'var(--green)' : 'inherit'}">
          ${p.vs != null ? (p.vs > 0 ? '+' : '') + p.vs.toFixed(1) + ' m/s' : 'N/A'}</td>
        <td class="mono">${p.heading != null ? Math.round(p.heading) + '°' : 'N/A'}</td>
      </tr>`).join('')}
    </table></div>
    <p class="mini mt">Speed on the ground, barometric altitude and heading. Not a flight
    recorder — a reconstruction from the IGC around the event.</p>`;

  const ex = document.getElementById(idExcep);
  if (ex) {
    /* las anomalías también se calculan sobre el momento confirmado */
    const lista = excepciones(track.map(p => ({ ...p, t: p.t - cero })));
    ex.innerHTML = lista.length ? `
      <h4>Worth a look</h4>
      <p class="mini mb">Events flagged by simple thresholds, the way telemetry systems do it:
      do not show everything, show what stands out.</p>
      ${lista.map(e => `<div class="row" style="gap:8px;margin:6px 0">
        <span class="etq mono">T${e.t > 0 ? '+' : ''}${e.t} s</span>
        <span class="sub">${escapa(e.txt)}</span></div>`).join('')}`
      : `<p class="mini">No anomalies flagged in this track.</p>`;
  }
}

/* ============================================================
   MAPAS PEQUEÑOS (señal y sitio)
   ============================================================ */
export async function mapaSenal(sig, id) {
  const el = document.getElementById(id);
  if (!el) return;
  const L = await cargaLeaflet();
  const m = base(id, [sig.lat, sig.lon], 13);
  const fr = sig.fuerza || sig.nivel;
  const col = fr === 'strong' ? '#a8742c' : fr === 'repeated' ? '#3d6390' : '#8c939b';
  L.circle([sig.lat, sig.lon], { radius: 2000, color: col, weight: 1.5,
    fillColor: col, fillOpacity: .08, dashArray: '5 5' }).addTo(m);
  est.reps.filter(r => sig.reps.includes(r.id)).forEach(r => {
    L.circleMarker([r.lat, r.lon], { radius: 7, fillColor: colorDe(r), fillOpacity: .9,
      color: '#fff', weight: 1.6 }).addTo(m).bindTooltip(`${nombreEv(r.evento)} · ${r.fecha}`);
  });
}

export async function mapaSitio(siteId, id) {
  const el = document.getElementById(id);
  if (!el) return;
  const s = SITES.find(x => x.id === siteId);
  if (!s) return;
  const L = await cargaLeaflet();
  const m = base(id, [s.lat, s.lon], 12);
  (s.zonas || []).forEach(z => {
    const t = (TIPOS_ZONA.find(x => x.id === z.t) || {}).n || z.t;
    const n = est.reps.filter(r => r.zona === z.id).length;
    L.circleMarker([z.lat, z.lon], { radius: 9, fillColor: n ? '#2c4a6e' : '#8c939b',
      fillOpacity: .55, color: '#fff', weight: 2 }).addTo(m)
      .bindTooltip(`${z.n} · ${t}${n ? ' · ' + n + ' reports' : ''}`, { direction: 'top' });
  });
  est.reps.filter(r => r.site === siteId).forEach(r => {
    L.circleMarker([r.lat, r.lon], { radius: 6, fillColor: colorDe(r), fillOpacity: .9,
      color: '#fff', weight: 1.5 }).addTo(m)
      .bindPopup(`<b>${escapa(nombreEv(r.evento))}</b><br>
        <a href="#reporte/${escapa(r.id)}">View report →</a>`);
  });
}
