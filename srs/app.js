/* ============================================================
   SkyReport — nucleo de la aplicacion
   Navegacion, componentes reutilizables y las vistas.
   ============================================================ */

import {
  SITES, EVENTOS, FASES, TIPOS_REPORTE, SEVERIDAD, RESULTADOS,
  DIRECCIONES, TIPOS_ZONA, DEMO, todosLosReportes, todosLosVuelos, igcDemo,
} from './data.js';
import {
  detectaSenales, similares, statsSite, patronesSite, completitud,
  distKm, NIVEL_TXT, nombreSitio,
} from './signals.js';

/* ============================================================
   ESTADO
   ============================================================ */
export const est = {
  reps: [],
  vuelos: [],
  senales: [],
  vista: 'inicio',
  filtros: { site:'', pais:'', ev:'', fase:'', sev:'', viento:'', clase:'', desde:'', hasta:'' },
  modoMapa: 'reports',
  sitioAbierto: null,
};

export function cargaDatos() {
  est.reps = todosLosReportes();
  est.vuelos = todosLosVuelos();
  est.senales = detectaSenales(est.reps);
}

/* ============================================================
   UTILIDADES
   ============================================================ */
export const $ = (s) => document.querySelector(s);
export const $$ = (s) => [...document.querySelectorAll(s)];

export function escapa(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

let _avisoT = null;
export function aviso(txt, ms = 3200) {
  const a = $('#aviso');
  if (!a) return;
  a.innerHTML = txt;
  a.classList.add('on');
  clearTimeout(_avisoT);
  _avisoT = setTimeout(() => a.classList.remove('on'), ms);
}

export function fechaLarga(iso) {
  if (!iso) return '—';
  const [a, m, d] = iso.split('-').map(Number);
  const M = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  return `${d} ${M[m - 1]} ${a}`;
}

export function hace(iso) {
  const dd = Math.round((new Date('2026-09-20') - new Date(iso)) / 86400000);
  if (dd <= 0) return 'today';
  if (dd === 1) return 'yesterday';
  if (dd < 30) return `${dd} days ago`;
  if (dd < 60) return 'last month';
  return `${Math.round(dd / 30)} months ago`;
}

export const nombreEv = (id) => (EVENTOS.find(e => e.id === id) || {}).n || id || '—';
export const nombreFase = (id) => (FASES.find(e => e.id === id) || {}).n || id || '—';
export const nombreRes = (id) => (RESULTADOS.find(e => e.id === id) || {}).n || id || '—';
export const nombreTipo = (id) => (TIPOS_REPORTE.find(e => e.id === id) || {}).n || id;
export const sitio = (id) => SITES.find(s => s.id === id) || {};
export const zonaDe = (rep) => {
  const s = SITES.find(x => x.id === rep.site) || {};
  return (s.zonas || []).find(z => z.id === rep.zona) || null;
};

/* ============================================================
   COMPONENTES
   ============================================================ */

/** Etiqueta de severidad. El rojo SOLO para lesiones graves o fatales. */
export function Severidad({ id }) {
  if (!id || id === 'none') return `<span class="etq ok">No injury</span>`;
  if (id === 'minor')  return `<span class="etq">Minor injury</span>`;
  if (id === 'serious') return `<span class="etq sev">Serious injury</span>`;
  if (id === 'fatal')   return `<span class="etq sev">Fatality · pending verification</span>`;
  return `<span class="etq">${escapa(id)}</span>`;
}

/** Barra de completitud del DATO (no del piloto). */
export function DataCompleteness({ rep, corto = false }) {
  const { pct, detalle } = completitud(rep);
  if (corto) {
    return `<div class="row" style="gap:7px">
      <div class="barra" style="flex:1"><i style="width:${pct}%"></i></div>
      <span class="mini mono">${pct}%</span>
    </div>`;
  }
  return `<div>
    <div class="entre mb"><span class="mini">Data completeness</span>
      <b class="mono">${pct}%</b></div>
    <div class="barra"><i style="width:${pct}%"></i></div>
    <div class="fila-etq">${detalle.map(d =>
      `<span class="etq${d.ok ? ' ok' : ''}">${d.ok ? '✓' : '·'} ${escapa(d.n)}</span>`).join('')}</div>
    <p class="mini mt">How much we can learn from this report. Not an assessment of the pilot.</p>
  </div>`;
}

/** Tarjeta de reporte. */
export function ReportCard({ rep, chico = false }) {
  const s = sitio(rep.site), z = zonaDe(rep);
  return `<article class="card clic" data-rep="${escapa(rep.id)}">
    <div class="entre">
      <span class="eyebrow">${escapa(fechaLarga(rep.fecha))}${rep.hora ? ' · ' + escapa(rep.hora) : ''}</span>
      <span class="etq${rep.tipo === 'near_miss' ? ' info' : ''}">${escapa(nombreTipo(rep.tipo))}</span>
    </div>
    <h3 class="mt">${escapa(nombreEv(rep.evento))}</h3>
    <p class="sub">${escapa(s.n || '—')}${z ? ' · ' + escapa(z.n) : ''}</p>
    <div class="fila-etq">
      <span class="etq">${escapa(nombreFase(rep.fase))}</span>
      <span class="etq">${escapa(nombreRes(rep.resultado))}</span>
      ${rep.windDir ? `<span class="etq">${rep.windDir} ${rep.windKmh || '?'} km/h</span>` : ''}
      ${rep.reserve ? '<span class="etq sev">Reserve</span>' : ''}
      ${rep.igc ? '<span class="etq ok">IGC</span>' : ''}
    </div>
    ${chico ? '' : `<div class="mt">${DataCompleteness({ rep, corto: true })}</div>`}
  </article>`;
}

/** Tarjeta de senal. NUNCA dice que algo sea peligroso. */
export function SignalCard({ sig }) {
  const s = sitio(sig.site);
  return `<article class="card clic" data-sig="${escapa(sig.id)}">
    <div class="entre">
      <span class="etq ${sig.nivel === 'elevated' ? 'elev' : sig.nivel === 'watch' ? 'watch' : 'info'}">
        ${escapa(NIVEL_TXT[sig.nivel])}</span>
      <span class="mini mono">${escapa(sig.regla)}</span>
    </div>
    <h3 class="mt">${escapa(sig.titulo)}</h3>
    <p class="sub">${escapa(s.n || '—')}${sig.zona ? ' · ' + escapa(sig.zona) : ''}</p>
    <dl class="dl mt">
      <dt>Reports</dt><dd>${sig.n}</dd>
      <dt>Period</dt><dd>${escapa(fechaLarga(sig.desde))} – ${escapa(fechaLarga(sig.hasta))}</dd>
      ${sig.condicion ? `<dt>Main condition</dt><dd>${escapa(sig.condicion)}</dd>` : ''}
    </dl>
    <div class="mt2"><span class="btn gh">View signal →</span></div>
  </article>`;
}

/** Tarjeta de sitio. */
export function SiteCard({ s }) {
  const st = statsSite(s.id, est.reps, est.vuelos);
  const sigs = est.senales.filter(x => x.site === s.id).length;
  return `<article class="card clic" data-site="${escapa(s.id)}">
    <div class="entre">
      <div>
        <h3>${escapa(s.n)}</h3>
        <p class="mini">${escapa(s.pais)} · ${escapa(s.region)}</p>
      </div>
      ${sigs ? `<span class="etq watch">${sigs} signal${sigs > 1 ? 's' : ''}</span>` : ''}
    </div>
    <div class="mets mt">
      <div class="met"><b>${st.total}</b><span>reports</span></div>
      <div class="met"><b>${st.vuelos}</b><span>flights logged</span></div>
      <div class="met"><b>${st.masEvento ? escapa(st.masEvento.n) : '—'}</b><span>most reported</span></div>
    </div>
    <p class="mini mt">Last report: ${st.ultimo ? escapa(hace(st.ultimo.fecha)) : '—'}</p>
  </article>`;
}

/** Event Snapshot. Aparece en el formulario y en la ficha del evento. */
export function EventSnapshot({ rep, nSimilares = 0 }) {
  const z = zonaDe(rep);
  const alt = rep.altAgl ? `${rep.altAgl} m AGL` : '—';
  const viento = rep.windDir ? `${rep.windDir} ${rep.windKmh || '?'}` +
    (rep.gustKmh ? `–${rep.gustKmh}` : '') + ' km/h' : '—';
  return `<div class="snap">
    <div class="cabeza">
      <b>Event snapshot</b>
      <span class="mini mono">${escapa(rep.id)}</span>
    </div>
    <div class="cuerpo">
      <div class="linea"><span>Event</span><span>${escapa(nombreEv(rep.evento))}</span></div>
      <div class="linea"><span>Phase</span><span>${escapa(nombreFase(rep.fase))}</span></div>
      <div class="linea"><span>Outcome</span><span>${escapa(nombreRes(rep.resultado))}</span></div>
      <div class="linea"><span>Altitude</span><span>${escapa(alt)}</span></div>
      <div class="linea"><span>Wind</span><span>${escapa(viento)}</span></div>
      <div class="linea"><span>Site</span><span>${escapa(sitio(rep.site).n || '—')}${
        z ? ' · ' + escapa(z.n) : ''}</span></div>
      <div class="linea"><span>Nearby similar reports</span><span>${nSimilares}</span></div>
      <div class="linea"><span>IGC</span><span>${rep.igc ? 'Available' : 'Not available'}</span></div>
    </div>
  </div>`;
}

/* ============================================================
   VISTA: INICIO
   ============================================================ */
function vistaInicio() {
  const reps = est.reps.filter(r => r.tipo !== 'safe_flight');
  const sigs = est.senales.slice(0, 4);
  const recientes = reps.slice().sort((a, b) => b.fecha.localeCompare(a.fecha)).slice(0, 4);

  const cuentaEv = {};
  reps.forEach(r => { cuentaEv[r.evento] = (cuentaEv[r.evento] || 0) + 1; });
  const [evMas, nEv] = Object.entries(cuentaEv).sort((a, b) => b[1] - a[1])[0] || ['—', 0];
  const cuentaFa = {};
  reps.forEach(r => { cuentaFa[r.fase] = (cuentaFa[r.fase] || 0) + 1; });
  const [faMas] = Object.entries(cuentaFa).sort((a, b) => b[1] - a[1])[0] || ['—'];
  const cuentaVi = {};
  reps.filter(r => r.windDir).forEach(r => { cuentaVi[r.windDir] = (cuentaVi[r.windDir] || 0) + 1; });
  const [viMas] = Object.entries(cuentaVi).sort((a, b) => b[1] - a[1])[0] || ['—'];
  const ult30 = reps.filter(r => (new Date('2026-09-20') - new Date(r.fecha)) / 86400000 <= 30).length;

  return `
  <div class="hero">
    <h1>SkyReport</h1>
    <p class="lema">Community safety intelligence for free flight.</p>
    <div class="cta">
      <button class="btn pri grande" data-ir="reportar">Report incident</button>
      <button class="btn sec grande" data-ir="mapa">Explore map</button>
    </div>
    ${DEMO ? `<p class="mini mt2">This build shows demonstration data. It is not a record of real accidents.</p>` : ''}
  </div>

  <section class="bloque">
    <div class="cab">
      <div><h2>Recent signals</h2>
        <p class="mini">Patterns found across several reports. An observation, not a verdict.</p></div>
      <button class="btn gh" data-ir="senales">All signals →</button>
    </div>
    <div class="grid g2">${sigs.map(s => SignalCard({ sig: s })).join('')}</div>
  </section>

  <section class="bloque">
    <div class="cab">
      <div><h2>Sites with activity</h2></div>
      <button class="btn gh" data-ir="sitios">All sites →</button>
    </div>
    <div class="grid g2">${SITES.map(s => SiteCard({ s })).join('')}</div>
  </section>

  <section class="bloque">
    <div class="cab"><h2>Pattern summary</h2></div>
    <div class="card">
      <div class="mets">
        <div class="met"><b>${nEv}</b><span>${escapa(nombreEv(evMas))} most reported</span></div>
        <div class="met"><b>${ult30}</b><span>reports in last 30 days</span></div>
        <div class="met"><b>${est.senales.length}</b><span>signals detected</span></div>
        <div class="met"><b style="font-size:17px">${escapa(nombreFase(faMas))}</b><span>most common phase</span></div>
        <div class="met"><b style="font-size:17px">${escapa(viMas)}</b><span>most reported wind</span></div>
        <div class="met"><b>${est.vuelos.length}</b><span>flights logged</span></div>
      </div>
    </div>
  </section>

  <section class="bloque">
    <div class="cab"><h2>Recently reported</h2>
      <button class="btn gh" data-ir="mapa">Explore map →</button></div>
    <div class="grid g2">${recientes.map(r => ReportCard({ rep: r })).join('')}</div>
  </section>

  <section class="bloque">
    <div class="cab"><h2>Quick actions</h2></div>
    <div class="grid g4">
      <button class="card clic centro" data-ir="reportar" style="padding:18px">
        <b>New report</b><p class="mini">Structured, step by step</p></button>
      <button class="card clic centro" data-ir="reportar" data-paso="igc" style="padding:18px">
        <b>Upload IGC</b><p class="mini">Add a track to a report</p></button>
      <button class="card clic centro" data-ir="mapa" style="padding:18px">
        <b>Explore map</b><p class="mini">Reports, heatmap, signals</p></button>
      <button class="card clic centro" data-ir="senales" style="padding:18px">
        <b>View signals</b><p class="mini">${est.senales.length} active</p></button>
    </div>
  </section>`;
}

/* ============================================================
   VISTA: SEÑALES
   ============================================================ */
function vistaSenales() {
  const porNivel = { elevated: [], watch: [], informational: [] };
  est.senales.forEach(s => porNivel[s.nivel].push(s));
  const grupo = (t, lista) => !lista.length ? '' : `
    <section class="bloque">
      <div class="cab"><h2>${t}</h2><span class="mini mono">${lista.length}</span></div>
      <div class="grid g2">${lista.map(s => SignalCard({ sig: s })).join('')}</div>
    </section>`;
  return `
  <div class="hero" style="padding-top:20px">
    <h1>Signals</h1>
    <p class="lema">A signal is a pattern SkyReport has found across several reports.
    It is not an accident and it is not a safety assessment — it is what the available
    data shows, written so you can disagree with it.</p>
  </div>
  ${est.senales.length ? `
    ${grupo('Elevated', porNivel.elevated)}
    ${grupo('Watch', porNivel.watch)}
    ${grupo('Informational', porNivel.informational)}`
    : `<div class="card centro" style="padding:36px"><p class="sub">No signals yet.</p>
       <p class="mini">Signals appear when at least three similar reports cluster.</p></div>`}`;
}

function vistaSenal(id) {
  const sig = est.senales.find(s => s.id === id);
  if (!sig) return `<p class="sub">Signal not found.</p>`;
  const reps = est.reps.filter(r => sig.reps.includes(r.id));
  const z = sig.zona;
  return `
  <button class="btn gh mb" data-ir="senales">← Signals</button>
  <div class="hero" style="padding:8px 0">
    <div class="entre">
      <span class="etq ${sig.nivel === 'elevated' ? 'elev' : sig.nivel === 'watch' ? 'watch' : 'info'}">
        ${escapa(NIVEL_TXT[sig.nivel])}</span>
      <span class="mini mono">Rule ${escapa(sig.regla)}</span>
    </div>
    <h1 style="font-size:26px;margin-top:10px">${escapa(sig.titulo)}</h1>
    <p class="lema">${escapa(sig.explicacion)}</p>
  </div>

  <section class="bloque">
    <div class="card">
      <div class="mets">
        <div class="met"><b>${sig.n}</b><span>related reports</span></div>
        <div class="met"><b style="font-size:16px">${escapa(fechaLarga(sig.desde))}</b><span>first</span></div>
        <div class="met"><b style="font-size:16px">${escapa(fechaLarga(sig.hasta))}</b><span>last</span></div>
        ${sig.condicion ? `<div class="met"><b style="font-size:16px">${escapa(sig.condicion)}</b>
          <span>main condition</span></div>` : ''}
      </div>
      ${z ? `<p class="mt"><b>Zone:</b> ${escapa(z)}</p>` : ''}
    </div>
  </section>

  <section class="bloque">
    <div class="cab"><h2>Where</h2></div>
    <div id="mapaSenal" style="height:300px;border-radius:12px;overflow:hidden;border:1px solid var(--line)"></div>
  </section>

  <section class="bloque">
    <div class="cab"><h2>Related reports</h2><span class="mini mono">${reps.length}</span></div>
    <div class="grid g2">${reps.map(r => ReportCard({ rep: r, chico: true })).join('')}</div>
  </section>

  <div class="card" style="background:var(--bg-2);border-style:dashed">
    <p class="mini">This is a data-derived signal based on available reports, not a
    definitive safety assessment.</p>
  </div>`;
}

/* ============================================================
   VISTA: SITIOS
   ============================================================ */
function vistaSitios() {
  return `
  <div class="hero" style="padding-top:20px">
    <h1>Sites</h1>
    <p class="lema">What has been reported at each place, and where within it.</p>
  </div>
  <div class="grid g2">${SITES.map(s => SiteCard({ s })).join('')}</div>`;
}

function vistaSitio(id, tab = 'overview') {
  const s = SITES.find(x => x.id === id);
  if (!s) return `<p class="sub">Site not found.</p>`;
  const st = statsSite(id, est.reps, est.vuelos);
  const sigs = est.senales.filter(x => x.site === id);
  const tabs = [['overview', 'Overview'], ['reports', 'Reports'], ['signals', 'Signals'],
    ['map', 'Map'], ['patterns', 'Patterns']];
  const T = (t) => `<button class="paso-n${tab === t ? ' on' : ''}" data-sitetab="${t}">${
    escapa(tabs.find(x => x[0] === t)[1])}</button>`;

  let cuerpo = '';

  if (tab === 'overview') {
    cuerpo = `
    <div class="card">
      <div class="mets">
        <div class="met"><b>${st.total}</b><span>total reports</span></div>
        <div class="met"><b>${st.nearMiss}</b><span>near misses</span></div>
        <div class="met"><b>${st.reservas}</b><span>reserve deployments</span></div>
        <div class="met"><b>${st.duras}</b><span>hard landings</span></div>
        <div class="met"><b>${st.lesiones}</b><span>with injury</span></div>
        <div class="met"><b>${st.vuelos}</b><span>flights logged</span></div>
      </div>
      <div class="mt2">
        <dl class="dl">
          <dt>Most common event</dt><dd>${st.masEvento ? escapa(st.masEvento.n) + ` (${st.masEvento.c})` : '—'}</dd>
          <dt>Most common phase</dt><dd>${st.masFase ? escapa(st.masFase.n) + ` (${st.masFase.c})` : '—'}</dd>
          <dt>Most reported wind</dt><dd>${st.masViento ? escapa(st.masViento.id) + ` (${st.masViento.c})` : '—'}</dd>
          <dt>Last report</dt><dd>${st.ultimo ? escapa(fechaLarga(st.ultimo.fecha)) : '—'}</dd>
        </dl>
      </div>
    </div>
    <div class="card mt">
      <h3>Reports per 1,000 logged flights</h3>
      ${st.por1000 == null
        ? `<p class="sub mt">${st.vuelos} flights logged at this site. That is still too small a
           sample to compare rates — a single busy week would move the number.</p>
           <p class="mini mt">This is exactly why safe flight logs matter: without a denominator,
           "100 incidents" says nothing.</p>`
        : `<p class="sub mt"><b style="font-size:24px">${st.por1000}</b> per 1,000 logged flights,
           from ${st.vuelos} logged flights.${st.muestraPequena ? ' The sample is still limited.' : ''}</p>`}
    </div>`;
  }

  if (tab === 'reports') {
    const lista = st.reps.slice().sort((a, b) => b.fecha.localeCompare(a.fecha));
    cuerpo = lista.length
      ? `<div class="grid g2">${lista.map(r => ReportCard({ rep: r })).join('')}</div>`
      : `<p class="sub">No reports at this site yet.</p>`;
  }

  if (tab === 'signals') {
    cuerpo = sigs.length
      ? `<div class="grid g2">${sigs.map(x => SignalCard({ sig: x })).join('')}</div>`
      : `<p class="sub">No signals at this site yet.</p>`;
  }

  if (tab === 'map') {
    cuerpo = `<div id="mapaSitio" style="height:380px;border-radius:12px;overflow:hidden;border:1px solid var(--line)"></div>
      <div class="card mt"><b>Zones</b>
        <div class="fila-etq mt">${(s.zonas || []).map(z => {
          const n = st.reps.filter(r => r.zona === z.id).length;
          const t = (TIPOS_ZONA.find(x => x.id === z.t) || {}).n || z.t;
          return `<span class="etq${n ? ' info' : ''}">${escapa(z.n)} · ${escapa(t)}${n ? ' · ' + n : ''}</span>`;
        }).join('')}</div>
        <p class="mini mt">Zones let us say "behind this ridge" instead of just naming the site.</p>
      </div>`;
  }

  if (tab === 'patterns') {
    const p = patronesSite(id, est.reps);
    cuerpo = p.length
      ? `<div class="grid g2">${p.map(x => `<div class="card"><p>${escapa(x.txt)}</p></div>`).join('')}</div>
         <p class="mini mt">These are descriptions of the reports, not causes. Correlation here does
         not imply causation.</p>`
      : `<p class="sub">Not enough reports at this site yet to describe patterns.</p>`;
  }

  return `
  <button class="btn gh mb" data-ir="sitios">← Sites</button>
  <div class="hero" style="padding:6px 0 2px">
    <h1>${escapa(s.n)}</h1>
    <p class="lema">${escapa(s.pais)} · ${escapa(s.region)} · ${s.alt} m</p>
    <p class="sub mt">${escapa(s.desc)}</p>
  </div>
  <div class="row wrap mt2" style="gap:6px">${tabs.map(t => T(t[0])).join('')}</div>
  <section class="bloque">${cuerpo}</section>`;
}

/* ============================================================
   VISTA: DETALLE DEL REPORTE
   ============================================================ */
function vistaReporte(id) {
  const rep = est.reps.find(r => r.id === id);
  if (!rep) return `<p class="sub">Report not found.</p>`;
  const s = sitio(rep.site), z = zonaDe(rep);
  const sims = similares(rep, est.reps);

  return `
  <button class="btn gh mb" id="volver">← Back</button>
  <div class="hero" style="padding:6px 0 2px">
    <span class="eyebrow">${escapa(fechaLarga(rep.fecha))}${rep.hora ? ' · ' + escapa(rep.hora) : ''}</span>
    <h1>${escapa(nombreEv(rep.evento))}</h1>
    <p class="lema">${escapa(s.n || '—')}${z ? ' · ' + escapa(z.n) : ''}</p>
  </div>

  <section class="bloque">
    ${EventSnapshot({ rep, nSimilares: sims.length })}
  </section>

  ${rep.igc ? `
  <section class="bloque">
    <div class="cab"><h2>Flight track</h2>
      <span class="mini">IGC available</span></div>
    <div id="mapaTrack" style="height:320px;border-radius:12px;overflow:hidden;border:1px solid var(--line)"></div>
    <div class="card mt">
      <div class="cab"><h3>Event timeline</h3>
        <span class="mini">T-120 s → T+60 s</span></div>
      <div id="timeline"></div>
      <div id="excepciones" class="mt"></div>
    </div>
  </section>` : `
  <section class="bloque">
    <div class="card"><p class="sub">No IGC for this report.</p>
      <p class="mini mt">Adding a track lets SkyReport reconstruct what the wing was doing
      around the event — speed, sink rate, heading.</p></div>
  </section>`}

  <section class="bloque">
    <div class="cab"><h2>What happened</h2></div>
    <div class="card">
      <p>${escapa(rep.factores || 'No description was added to this report.')}</p>
      ${rep.lecciones ? `<h4 class="mt2">Lessons learned</h4><p class="sub">${escapa(rep.lecciones)}</p>` : ''}
    </div>
  </section>

  <section class="bloque">
    <div class="cab"><h2>Conditions observed</h2></div>
    <div class="card"><dl class="dl">
      <dt>Wind</dt><dd>${rep.windDir ? escapa(rep.windDir) + ' ' + rep.windKmh + ' km/h' +
        (rep.gustKmh ? ' · gusts ' + rep.gustKmh : '') : '—'}</dd>
      <dt>Thermal activity</dt><dd>${escapa(rep.thermal || '—')}</dd>
      <dt>Turbulence felt</dt><dd>${escapa(rep.turb || '—')}</dd>
      <dt>Cloud</dt><dd>${escapa(rep.cloud || '—')}</dd>
    </dl></div>
  </section>

  <section class="bloque">
    <div class="cab"><h2>Equipment</h2></div>
    <div class="card"><dl class="dl">
      <dt>Wing</dt><dd>${escapa([rep.ala, rep.modelo].filter(Boolean).join(' ') || '—')}</dd>
      <dt>Class</dt><dd>${escapa(rep.clase || '—')}</dd>
      <dt>Harness</dt><dd>${escapa(rep.harness || '—')}</dd>
      <dt>Reserve</dt><dd>${escapa(rep.reserva || '—')}</dd>
      <dt>Experience</dt><dd>${escapa(rep.exp || '—')}</dd>
    </dl><p class="mini mt">Experience is collected as a range, on purpose. SkyReport does not
    identify pilots and does not rate them.</p></div>
  </section>

  <section class="bloque">
    <div class="cab"><h2>Location</h2></div>
    <div class="card"><dl class="dl">
      <dt>Site</dt><dd>${escapa(s.n || '—')}</dd>
      <dt>Zone</dt><dd>${escapa(z ? z.n : '—')}</dd>
      <dt>Coordinates</dt><dd class="mono">${rep.lat.toFixed(4)}, ${rep.lon.toFixed(4)}</dd>
    </dl><p class="mini mt">Coordinates are rounded to about 100 m. Exact tracks are not published.</p></div>
  </section>

  <section class="bloque">
    <div class="cab"><h2>Data completeness</h2></div>
    <div class="card">${DataCompleteness({ rep })}</div>
  </section>

  <section class="bloque">
    <div class="cab"><h2>Similar reports nearby</h2><span class="mini mono">${sims.length}</span></div>
    ${sims.length ? `<div class="grid g2">${sims.map(x => ReportCard({ rep: x.r, chico: true })).join('')}</div>`
      : `<p class="sub">No similar reports found nearby.</p>`}
  </section>`;
}

/* ============================================================
   VISTA: METODOLOGÍA
   ============================================================ */
function vistaMetodo() {
  return `
  <div class="hero" style="padding-top:20px">
    <h1>How SkyReport works</h1>
    <p class="lema">What the data can and cannot tell you.</p>
  </div>

  <section class="bloque">
    <div class="card">
      <h3>Report vs Signal</h3>
      <p class="sub mt"><b>Report</b> — one event, sent by one person. It is testimony.</p>
      <p class="sub"><b>Signal</b> — a pattern found across several reports. It is an
      observation, and it can be wrong. Every signal shows the rule that produced it, so you
      can judge it yourself.</p>
    </div>
  </section>

  <section class="bloque">
    <div class="cab"><h2>How signals are built</h2></div>
    <div class="grid g2">
      <div class="card"><h4>R1 · Cluster</h4><p class="sub">Three or more reports of the same
      event within 2 km and 30 days.</p></div>
      <div class="card"><h4>R2 · Same wind</h4><p class="sub">Three or more reports of the same
      event logged with the same wind direction.</p></div>
      <div class="card"><h4>R3 · Same zone</h4><p class="sub">Three or more reports inside the
      same zone of a site — a ridge, a venturi, a lee side.</p></div>
      <div class="card"><h4>R4 · Time of day</h4><p class="sub">40% or more of a site's reports
      falling in the same four-hour window.</p></div>
      <div class="card"><h4>R5 · Reserve deployments</h4><p class="sub">Two or more reserve
      deployments reported at the same site.</p></div>
      <div class="card"><h4>R6 · Strong wind</h4><p class="sub">Three or more reports logged
      with wind at or above 20 km/h.</p></div>
    </div>
    <p class="mini mt">The rules are deliberately simple and written out. With few reports, a
    more complicated model would be less honest, not more.</p>
  </section>

  <section class="bloque">
    <div class="cab"><h2>Limits of this data</h2></div>
    <div class="card">
      <h4>Reporting bias</h4>
      <p class="sub">People report what they think is worth reporting. Busy sites, competition
      sites and sites with an active local community are over-represented. A quiet site with no
      reports is not necessarily a safe site.</p>
      <h4 class="mt2">The denominator problem</h4>
      <p class="sub">"100 incidents" means nothing on its own. 100 out of 500 flights is not the
      same as 100 out of 50,000. That is why SkyReport also records flights where nothing
      happened.</p>
      <h4 class="mt2">Correlation is not causation</h4>
      <p class="sub">If most reports at a site mention NW wind, that may mean NW days are
      riskier — or simply that most people fly on NW days. Patterns here describe reports, not
      causes.</p>
      <h4 class="mt2">What SkyReport will not do</h4>
      <p class="sub">It does not rank pilots, score risk, or tell you whether to fly. It gives you
      information. You make the decision.</p>
    </div>
  </section>

  <section class="bloque">
    <div class="cab"><h2>Privacy</h2></div>
    <div class="card"><p class="sub">Reports can be submitted anonymously. Names, emails and
    phone numbers are never published. Coordinates are rounded to about 100 m and the original
    IGC file is not published.</p></div>
  </section>`;
}

/* ============================================================
   ROUTER
   ============================================================ */
const VISTAS = {
  inicio: vistaInicio,
  senales: vistaSenales,
  sitios: vistaSitios,
  metodo: vistaMetodo,
};

export function pinta(vista, arg) {
  if (vista === 'reportar' || vista === 'mapa') return;   /* los pinta su modulo */
  est.vista = vista;
  const cont = $('#app');
  if (!cont) return;
  let html = '';
  if (vista === 'senal') html = vistaSenal(arg);
  else if (vista === 'sitio') html = vistaSitio(arg, est.tabSitio || 'overview');
  else if (vista === 'reporte') html = vistaReporte(arg);
  else html = (VISTAS[vista] || vistaInicio)();
  cont.innerHTML = `<div class="cont" style="padding-top:8px;padding-bottom:34px">${html}</div>`;
  pintaNav(vista);
  engancha();
  /* ===== LOS MAPAS Y GRAFICOS VAN DESPUES =====
     Necesitan el div ya dentro del DOM. Si se pintan antes, Leaflet no
     encuentra su contenedor y el mapa sale en blanco. */
  import('./mapa.js').then(m => {
    if (vista === 'senal' && arg) m.mapaSenal(est.senales.find(x => x.id === arg), 'mapaSenal');
    if (vista === 'sitio' && est.tabSitio === 'map' && arg) m.mapaSitio(arg, 'mapaSitio');
    if (vista === 'reporte' && arg) {
      const rep = est.reps.find(r => r.id === arg);
      /* ===== EL "BLACK BOX" =====
         Con el IGC, reconstruyo que hacia el ala alrededor del evento:
         posicion, velocidad, ascenso/caida y rumbo. No es solo pintar un
         track: es una reconstruccion con marcas de tiempo T-120 ... T+60. */
      if (rep && rep.igc) {
        const tr = igcDemo(rep.lat, rep.lon);
        m.mapaTrack(tr, 'mapaTrack');
        m.pintaTimeline(tr, 'timeline', 'excepciones');
      }
    }
  });
}

function pintaNav(vista) {
  const base = { senal: 'senales', sitio: 'sitios', reporte: 'sitios' }[vista] || vista;
  $$('.top nav a, .tabbar a').forEach(a => {
    a.classList.toggle('on', a.dataset.ir === base);
  });
}

function engancha() {
  $$('[data-ir]').forEach(b => b.onclick = () => ir(b.dataset.ir, b.dataset.paso));
  $$('[data-rep]').forEach(c => c.onclick = () => ir('reporte', c.dataset.rep));
  $$('[data-sig]').forEach(c => c.onclick = () => ir('senal', c.dataset.sig));
  $$('[data-site]').forEach(c => c.onclick = () => { est.tabSitio = 'overview'; ir('sitio', c.dataset.site); });
  $$('[data-sitetab]').forEach(b => b.onclick = () => {
    est.tabSitio = b.dataset.sitetab;
    ir('sitio', est.sitioAbierto);
  });
  const v = $('#volver');
  if (v) v.onclick = () => history.back();
}

export function ir(vista, arg) {
  if (arg && vista === 'sitio') est.sitioAbierto = arg;
  const hash = arg ? `#${vista}/${arg}` : `#${vista}`;
  if (location.hash !== hash) history.pushState(null, '', hash);
  est.vista = vista;
  if (vista === 'reportar') { import('./report.js').then(m => m.pintaReportar(arg)); return; }
  if (vista === 'mapa')     { import('./mapa.js').then(m => m.pintaMapa()); return; }
  $$('.vista').forEach(x => x.classList.remove('on'));
  $('#app').classList.add('on');
  pinta(vista, arg);
  window.scrollTo({ top: 0 });
}

export function desdeHash() {
  const h = (location.hash || '#inicio').slice(1);
  const [v, a] = h.split('/');
  return [v || 'inicio', a || null];
}

export function arranca() {
  cargaDatos();
  const [v, a] = desdeHash();
  ir(v, a);
  window.addEventListener('popstate', () => {
    const [v2, a2] = desdeHash();
    est.tabSitio = 'overview';
    ir(v2, a2);
  });
  /* el mapa y los graficos se pintan despues de insertar el HTML */
  document.addEventListener('sky:repinta', () => pinta(est.vista, est.sitioAbierto));
}

if (typeof window !== 'undefined') {
  window.SkyReport = { est, ir, pinta, arranca, cargaDatos, aviso, escapa, nombreEv,
    nombreFase, nombreRes, nombreTipo, fechaLarga, hace, sitio, zonaDe, Severidad,
    DataCompleteness, ReportCard, SignalCard, SiteCard, EventSnapshot };
}
