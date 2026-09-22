/* ============================================================
   SkyReport — nucleo de la aplicacion
   Navegacion, componentes reutilizables y las vistas.
   ============================================================ */

import {
  SITES, EVENTOS, FASES, TIPOS_REPORTE, SEVERIDAD, RESULTADOS,
  DIRECCIONES, TIPOS_ZONA, DEMO, todosLosReportes, todosLosVuelos, igcDemo,
  hoyISO, haceDiasISO, diasEntre, FECHA_DEMO,
} from './data.js';
import {
  detectaSenales, similares, statsSite, patronesSite, completitud,
  distKm, FUERZA_TXT, contextoExposicion, nombreSitio,
} from './signals.js';
import { t, ponIdioma, idioma, detectaIdioma, idiomasDisponibles, traducePantalla } from './i18n.js';
import { haySupabase, red, AJUSTES } from './config.js';
import {
  conecta, enModoDemo, leeReportes, leeVuelos, leeSitios, leeZonas,
  deFilaReporte, deFilaVuelo, pendientes, sincroniza, vigilaConexion,
} from './supabase.js';

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
  capaMapa: 'terreno',
  sitioAbierto: null,
};

export function cargaDatos() {
  est.reps = todosLosReportes();
  est.vuelos = todosLosVuelos();
  est.senales = detectaSenales(est.reps);
}

/** Trae de Supabase y sustituye los datos locales.
 *
 *  IMPORTANTE: cuando Supabase está conectado, los datos de
 *  DEMOSTRACIÓN se apagan. Nunca se suman. Si se mezclaran, las
 *  estadísticas de un sitio inventado se leerían como si fueran de
 *  la comunidad, y eso es exactamente lo que no queremos. */
export async function cargaDesdeSupabase() {
  if (!haySupabase()) { red.modo = 'demo'; return { ok: false }; }
  const c = await conecta();
  if (!c.ok) return c;

  const [rs, vs] = await Promise.all([leeReportes(), leeVuelos()]);
  if (rs.ok) est.reps = rs.datos.map(deFilaReporte);
  if (vs.ok) est.vuelos = vs.datos.map(deFilaVuelo);
  if (!AJUSTES.permitirDemoConSupabase) {
    /* nada de demo junto a datos reales */
    est.reps = est.reps.filter(r => !r.demo);
    est.vuelos = est.vuelos.filter(v => !v.demo);
  }
  est.senales = detectaSenales(est.reps);
  return { ok: true, reportes: est.reps.length, vuelos: est.vuelos.length };
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
  /* la fecha de hoy sale del reloj, no de una constante */
  const hoy = hoyISO();
  const dd = Math.round((new Date(hoy + 'T12:00:00') - new Date(iso + 'T12:00:00')) / 86400000);
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
/* ============================================================
   TARJETA DE SEÑAL
   ============================================================
   Pam pidió quitar el aire de "score de riesgo" y poner delante
   los datos objetivos. Ahora lo primero que se lee son números
   comprobables: cuántos, en cuánta área, en cuántos días, con qué
   condiciones. La etiqueta de fuerza va al final y describe
   EVIDENCIA, no peligro. */
export function SignalCard({ sig }) {
  const s = sitio(sig.site);
  const ctx = contextoExposicion(sig, est.reps, est.vuelos, AJUSTES.minVuelosParaTasa);
  const fr = sig.fuerza || sig.nivel || 'limited';
  return `<article class="card clic" data-sig="${escapa(sig.id)}">
    <div class="entre">
      <span class="etq ${fr === 'strong' ? 'watch' : fr === 'repeated' ? 'info' : ''}">
        ${escapa(t('strength.' + fr))}</span>
      <span class="mini mono">${escapa(t('signals.rule'))} ${escapa(sig.regla)}</span>
    </div>
    <h3 class="mt">${escapa(sig.titulo)}</h3>
    <p class="sub">${escapa(s.n || '—')}${sig.zona ? ' · ' + escapa(sig.zona) : ''}</p>
    <dl class="dl mt">
      <dt>${escapa(t('signals.related', { n: sig.n }))}</dt>
      <dd>${escapa(fechaLarga(sig.desde))} – ${escapa(fechaLarga(sig.hasta))}</dd>
      ${sig.radioKm != null ? `<dt>${escapa(t('signals.area', { km: sig.radioKm }))}</dt>
        <dd>${escapa(t('signals.period', { n: sig.dias || '—' }))}</dd>` : ''}
      ${sig.condicion ? `<dt>${escapa(sig.condicion)}</dt>
        <dd>${(sig.franja && sig.franja.tramo)
          ? escapa(t('signals.between', {
              n: sig.franja.n,
              a: String(sig.franja.tramo).split('-')[0] + ':00',
              b: String(sig.franja.tramo).split('-')[1] + ':00' })) : ''}</dd>` : ''}
      ${ctx.suficiente
        ? `<dt>${escapa(t('signals.exposureTitle'))}</dt>
           <dd>${escapa(t('signals.exposure', { n: ctx.reportes, v: ctx.vuelos.toLocaleString(idioma()) }))}</dd>`
        : `<dt>${escapa(t('signals.exposureTitle'))}</dt>
           <dd class="mini">${escapa(t('signals.exposureLimited'))}</dd>`}
    </dl>
    <div class="mt2"><span class="btn gh">${escapa(t('signals.viewRelated'))} →</span></div>
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
  const sigs = est.senales.slice(0, 3);
  /* los reportes más recientes, por fecha de verdad */
  const recientes = reps.slice().sort((a, b) => String(b.fecha).localeCompare(String(a.fecha))).slice(0, 3);

  /* resumen: con la fecha REAL de hoy, no una constante */
  const hace30 = haceDiasISO(30);
  const ult30 = reps.filter(r => r.fecha >= hace30).length;
  const cuentaEv = {};
  reps.forEach(r => { cuentaEv[r.evento] = (cuentaEv[r.evento] || 0) + 1; });
  const [evMas, nEv] = Object.entries(cuentaEv).sort((a, b) => b[1] - a[1])[0] || ['', 0];
  const cuentaFa = {};
  reps.forEach(r => { cuentaFa[r.fase] = (cuentaFa[r.fase] || 0) + 1; });
  const [faMas] = Object.entries(cuentaFa).sort((a, b) => b[1] - a[1])[0] || [''];
  const cuentaVi = {};
  reps.filter(r => r.windDir).forEach(r => { cuentaVi[r.windDir] = (cuentaVi[r.windDir] || 0) + 1; });
  const [viMas] = Object.entries(cuentaVi).sort((a, b) => b[1] - a[1])[0] || [''];

  const demo = enModoDemo();

  return `
  <div class="hero">
    <h1>SkyReport</h1>
    <p class="lema">${escapa(t('brand.tagline'))}</p>
    ${demo ? `<div class="etq watch mt2" style="font-size:12px">
      ${escapa(t('common.demo'))}</div>` : ''}
  </div>

  <!-- ===== 1. BUSCAR UN SITIO — lo primero, para el que abre antes de volar ===== -->
  <section class="bloque" style="margin-top:20px">
    <h2>${escapa(t('home.searchTitle'))}</h2>
    <div class="buscador mt">
      <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor"
           stroke-width="2.2" stroke-linecap="round" aria-hidden="true">
        <circle cx="11" cy="11" r="7"/><path d="m20 20-3.6-3.6"/></svg>
      <input type="search" id="buscaSitio" autocomplete="off"
             placeholder="${escapa(t('home.searchPlaceholder'))}">
    </div>
    <div id="buscaResultados"></div>
  </section>

  <!-- ===== 2. LAS DOS ACCIONES ===== -->
  <section class="bloque">
    <div class="grid g2">
      <button class="card clic accion" data-ir="reportar">
        <span class="accion-ic">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor"
               stroke-width="2" stroke-linecap="round" aria-hidden="true">
            <path d="M12 9v4"/><path d="M12 17h.01"/>
            <path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/></svg>
        </span>
        <b>${escapa(t('home.reportEvent'))}</b>
        <span class="mini">${escapa(t('home.reportEventSub'))}</span>
      </button>
      <button class="card clic accion ok" data-ir="vuelo">
        <span class="accion-ic ok">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor"
               stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="m4.5 12.5 5 5L20 7"/></svg>
        </span>
        <b>${escapa(t('home.flewToday'))}</b>
        <span class="mini">${escapa(t('home.flewTodaySub'))}</span>
      </button>
    </div>
    ${red.pendientes ? `<div class="card mt" style="background:var(--amber-bg);border-color:#e8d7b0">
      <p class="sub">${escapa(t('status.pending', { n: red.pendientes }))}</p></div>` : ''}
  </section>

  <!-- ===== 3. ACTIVIDAD RECIENTE ===== -->
  <section class="bloque">
    <div class="cab">
      <h2>${escapa(t('home.recentActivity'))}</h2>
      <button class="btn gh" data-ir="mapa">${escapa(t('nav.map'))} →</button>
    </div>
    ${recientes.length
      ? `<div class="grid g2">${recientes.map(r => ReportCard({ rep: r, chico: true })).join('')}</div>`
      : `<p class="sub">${escapa(t('site.noReports'))}</p>`}
  </section>

  <!-- ===== 4. SEÑALES ===== -->
  <section class="bloque">
    <div class="cab">
      <div><h2>${escapa(t('home.recentSignals'))}</h2>
        <p class="mini">${escapa(t('signals.lede')).slice(0, 96)}…</p></div>
      <button class="btn gh" data-ir="senales">${escapa(t('nav.signals'))} →</button>
    </div>
    ${sigs.length
      ? `<div class="grid g2">${sigs.map(x => SignalCard({ sig: x })).join('')}</div>`
      : `<p class="sub">${escapa(t('signals.none'))}</p>`}
  </section>

  <!-- ===== 5. SITIOS ===== -->
  <section class="bloque">
    <div class="cab"><h2>${escapa(t('home.sitesActivity'))}</h2>
      <button class="btn gh" data-ir="sitios">${escapa(t('nav.sites'))} →</button></div>
    <div class="grid g2">${SITES.map(x => SiteCard({ s: x })).join('')}</div>
  </section>

  <!-- ===== 6. RESUMEN ===== -->
  <section class="bloque">
    <div class="cab"><h2>${escapa(t('home.patternSummary'))}</h2>
      <span class="mini">${escapa(t('strength.explain'))}</span></div>
    <div class="card">
      <div class="mets">
        <div class="met"><b>${nEv}</b><span>${escapa(nombreEv(evMas))}</span></div>
        <div class="met"><b>${ult30}</b><span>${escapa(t('common.reports'))} · 30 d</span></div>
        <div class="met"><b>${est.senales.length}</b><span>${escapa(t('nav.signals')).toLowerCase()}</span></div>
        <div class="met"><b style="font-size:16px">${escapa(nombreFase(faMas))}</b>
          <span>${escapa(t('site.mostPhase')).toLowerCase()}</span></div>
        <div class="met"><b style="font-size:16px">${escapa(viMas || '—')}</b>
          <span>${escapa(t('site.mostWind')).toLowerCase()}</span></div>
        <div class="met"><b>${est.vuelos.length.toLocaleString(idioma())}</b>
          <span>${escapa(t('common.flightsLogged'))}</span></div>
      </div>
    </div>
  </section>`;
}

/* ============================================================
   EL BUSCADOR DE SITIOS
   ============================================================
   Va aparte del resto de la pintura porque necesita escuchar
   mientras se escribe. Filtra por nombre, país y región, y admite
   tildes de menos (gente que escribe "penon" por "Peñón"). */
export function montaBuscador() {
  const inp = document.getElementById('buscaSitio');
  const caja = document.getElementById('buscaResultados');
  if (!inp || !caja) return;

  const sinTildes = (x) => (x || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');

  const pinta = (lista) => {
    if (!inp.value.trim()) { caja.innerHTML = ''; return; }
    if (!lista.length) {
      caja.innerHTML = `<p class="sub mt">${escapa(t('home.searchNoResults'))}</p>`;
      return;
    }
    caja.innerHTML = `<div class="grid g2 mt">${lista.slice(0, 6).map(s => SiteCard({ s })).join('')}</div>`;
    caja.querySelectorAll('[data-site]').forEach(c => {
      c.onclick = () => { est.tabSitio = 'overview'; ir('sitio', c.dataset.site); };
    });
  };

  const busca = () => {
    const q = sinTildes(inp.value.trim());
    if (!q) return pinta([]);
    const lista = SITES.filter(s =>
      sinTildes(s.n).includes(q) || sinTildes(s.pais).includes(q) || sinTildes(s.region).includes(q));
    pinta(lista);
  };
  inp.addEventListener('input', busca);
  inp.addEventListener('focus', busca);
  if (inp.value) busca();
}

/* ============================================================
   VISTA: SEÑALES
   ============================================================ */
function vistaSenales() {
  /* OJO: las claves son limited / repeated / strong. Antes eran
     elevated / watch / informational, que además sonaba a semáforo
     de peligro. Si se cambia aquí, hay que cambiarlo en signals.js. */
  const grupos = { strong: [], repeated: [], limited: [] };
  est.senales.forEach(s => {
    const f = s.fuerza || s.nivel || 'limited';
    (grupos[f] || grupos.limited).push(s);
  });
  const bloque = (clave, lista) => !lista.length ? '' : `
    <section class="bloque">
      <div class="cab">
        <div><h2>${escapa(t('strength.' + clave))}</h2>
          ${clave === 'strong' ? `<p class="mini">${escapa(t('strength.explain'))}</p>` : ''}</div>
        <span class="mini mono">${lista.length}</span>
      </div>
      <div class="grid g2">${lista.map(s => SignalCard({ sig: s })).join('')}</div>
    </section>`;
  return `
  <div class="hero" style="padding-top:20px">
    <h1>${escapa(t('signals.title'))}</h1>
    <p class="lema">${escapa(t('signals.lede'))}</p>
  </div>
  ${est.senales.length
    ? bloque('strong', grupos.strong) + bloque('repeated', grupos.repeated) + bloque('limited', grupos.limited)
    : `<div class="card centro" style="padding:36px"><p class="sub">${escapa(t('signals.none'))}</p>
       <p class="mini">${escapa(t('signals.noneHelp'))}</p></div>`}`;
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
      <span class="etq ${(sig.fuerza||sig.nivel) === 'strong' ? 'watch' : 'info'}">
        ${escapa(t('strength.' + (sig.fuerza || sig.nivel || 'limited')))}</span>
      <span class="mini mono">${escapa(t('signals.rule'))} ${escapa(sig.regla)}</span>
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
    <p class="mini">${escapa(t('signals.disclaimer'))}</p>
    <p class="mini mt">${escapa(t('strength.explain'))}</p>
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
  if (est.vista === 'inicio') montaBuscador();
}

export function ir(vista, arg) {
  if (arg && vista === 'sitio') est.sitioAbierto = arg;
  const hash = arg ? `#${vista}/${arg}` : `#${vista}`;
  if (location.hash !== hash) history.pushState(null, '', hash);
  est.vista = vista;
  if (vista === 'reportar') { import('./report.js').then(m => m.pintaReportar(arg)); return; }
  if (vista === 'vuelo')    { import('./report.js').then(m => m.pintaVueloRapido()); return; }
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

/** Pinta el estado de la red en la cabecera. Discreto: una línea
 *  pequeña que solo aparece cuando hay algo que contar. */
export function pintaEstadoRed() {
  const el = document.getElementById('estadoRed');
  if (!el) return;
  const demo = enModoDemo();
  const p = red.pendientes;
  let txt = '', clase = '';
  if (red.modo === 'sin-conexion') { txt = t('status.unavailable'); clase = 'aviso'; }
  else if (demo) { txt = t('status.demo'); clase = 'demo'; }
  else if (p) { txt = t('status.pending', { n: p }); clase = 'pend'; }

  el.className = 'estado-red' + (clase ? ' ' + clase : '');
  el.innerHTML = txt ? `<span>${escapa(txt)}</span>` : '';
  const b = document.getElementById('bSincroniza');
  if (b) b.classList.toggle('oculto', !(p && red.modo === 'comunidad'));
}

export function arranca() {
  ponIdioma(detectaIdioma(), false);
  cargaDatos();
  const [v, a] = desdeHash();
  ir(v, a);

  /* el idioma y el estado de la red, en la cabecera */
  const sel = document.getElementById('selIdioma');
  if (sel) {
    sel.innerHTML = idiomasDisponibles().map(x =>
      `<option value="${x.id}"${idioma() === x.id ? ' selected' : ''}>${escapa(x.n)}</option>`).join('');
    sel.onchange = () => {
      ponIdioma(sel.value);
      pinta(est.vista, est.sitioAbierto);
      pintaEstadoRed();
    };
  }
  const bs = document.getElementById('bSincroniza');
  if (bs) bs.onclick = async () => {
    bs.textContent = '…';
    const r = await sincroniza();
    red.pendientes = r.quedan;
    bs.textContent = '↻';
    pintaEstadoRed();
    aviso(r.enviados ? `Enviados ${r.enviados}.` : t('status.offlineSaved'));
  };

  pintaEstadoRed();
  /* si hay Supabase configurado, se traen los datos de la comunidad */
  if (haySupabase()) {
    cargaDesdeSupabase().then(r => { pintaEstadoRed(); if (r.ok) ir('inicio'); });
  }
  vigilaConexion(() => { pintaEstadoRed(); pinta(est.vista, est.sitioAbierto); });
  window.addEventListener('online', pintaEstadoRed);
  window.addEventListener('offline', pintaEstadoRed);
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
