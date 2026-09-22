/* ============================================================
   SkyReport — el flujo de reportar
   ============================================================

   Tres decisiones importantes:

   1) SAFE FLIGHT LOG tarda menos de 10 segundos. Es el
      DENOMINADOR. Sin vuelos sin incidentes, "100 incidentes"
      no dice nada: 100 de 500 no es lo mismo que 100 de 50.000.
      Por eso va aparte y pide tres cosas y nada mas.

   2) EL FORMULARIO CAMBIA SEGUN EL EVENTO. Nadie deberia
      contestar cien preguntas. Si eliges "reserve deployment"
      salen las preguntas de la reserva; si eliges "hard landing",
      las del aterrizaje. Las preguntas extra son un objeto:
      anadir un bloque nuevo es anadir una entrada.

   3) EL SNAPSHOT SE ACTUALIZA MIENTRAS ESCRIBES. Ves la ficha
      del evento tomar forma, que es lo que quedara publicado.
   ============================================================ */

import {
  SITES, EVENTOS, FASES, TIPOS_REPORTE, SEVERIDAD, RESULTADOS,
  DIRECCIONES, TIPOS_ZONA, CLAVE_LOCAL, CLAVE_VUELOS, guardaLocal, igcDemo,
} from './data.js';
import { est, cargaDatos, ir, aviso, escapa } from './app.js';
import { EventSnapshot, DataCompleteness } from './app.js';
import { t } from './i18n.js';
import { parseIGC, posiblesAnomalias, ventanaEvento, horaBonita } from './igc.js';
import { enviaReporte, enviaVuelo, enModoDemo } from './supabase.js';
import { AJUSTES, red } from './config.js';
/* hoyISO vive en data.js, que es donde están las fechas */
import { hoyISO } from './data.js';

/* ============================================================
   PREGUNTAS DINÁMICAS
   Anadir un bloque = anadir una entrada aqui. Nada mas.
   ============================================================ */
const EXTRA = {
  reserve: [
    { id:'reserva_desplego', t:'op', n:'Did the reserve fully deploy?',
      o:[['yes','Yes'],['partial','Partially'],['no','No']] },
    { id:'reserva_altura', t:'num', n:'Estimated deployment altitude (m AGL)',
      p:'A rough figure is fine' },
    { id:'reserva_enredo', t:'op', n:'Was there entanglement with the main wing?',
      o:[['no','No'],['yes','Yes']] },
    { id:'reserva_principal', t:'op', n:'Was the main wing disabled?',
      o:[['no','No'],['yes','Yes']] },
    { id:'reserva_final', t:'op', n:'Landing outcome',
      o:[['standing','Stood up'],['ground','Ground contact'],['obstacle','Obstacle']] },
  ],
  hardlanding: [
    { id:'ater_viento', t:'op', n:'Wind direction relative to landing',
      o:[['into','Into wind'],['cross','Crosswind'],['down','Downwind']] },
    { id:'ater_flare', t:'op', n:'Flare timing',
      o:[['ok','Fine'],['early','Too early'],['late','Too late'],['none','No flare']] },
    { id:'ater_obstaculo', t:'op', n:'Obstacle involved?',
      o:[['no','No'],['yes','Yes']] },
    { id:'ater_terreno', t:'op', n:'Terrain type',
      o:[['grass','Grass'],['dirt','Dry dirt'],['rock','Rock'],['asphalt','Asphalt'],['other','Other']] },
  ],
  asymmetric: [
    { id:'col_tipo', t:'op', n:'Asymmetric or frontal?',
      o:[['asym','Asymmetric'],['frontal','Frontal']] },
    { id:'col_pct', t:'op', n:'Estimated size of the collapse',
      o:[['lt25','Less than 25%'],['25-50','25–50%'],['gt50','More than 50%']] },
    { id:'col_cravat', t:'op', n:'Cravat?', o:[['no','No'],['yes','Yes']] },
    { id:'col_rot', t:'op', n:'Rotation?', o:[['no','No'],['yes','Yes']] },
    { id:'col_recupero', t:'op', n:'How did it recover?',
      o:[['solo','On its own'],['input','With pilot input'],['reserve','Reserve']] },
  ],
  frontal: [
    { id:'fro_tipo', t:'op', n:'Did it stay frontal or fold?',
      o:[['frontal','Stayed frontal'],['fold','Folded']] },
    { id:'fro_recupero', t:'op', n:'Recovery',
      o:[['solo','On its own'],['input','With pilot input'],['reserve','Reserve']] },
  ],
  turbulence: [
    { id:'turb_donde', t:'op', n:'Where was it strongest?',
      o:[['ridge','On the ridge'],['lee','Behind a feature'],['thermal','In a thermal'],
         ['transition','On transition'],['landing','On approach']] },
    { id:'turb_aviso', t:'op', n:'Any warning before it?',
      o:[['none','Nothing obvious'],['dust','Dust or debris'],['cloud','Cloud build-up'],['gust','Sudden gust']] },
  ],
  cravat: [
    { id:'cra_linea', t:'op', n:'Which lines were caught?',
      o:[['stab','Stabilo'],['tip','Tip lines'],['other','Other']] },
    { id:'cra_salio', t:'op', n:'Did it come out?',
      o:[['yes','Yes, in flight'],['no','No']] },
  ],
  midair: [
    { id:'aire_donde', t:'op', n:'Where were you relative to the other wing?',
      o:[['below','Below'],['level','Level'],['above','Above']] },
    { id:'aire_gaggle', t:'op', n:'Was it in a gaggle?', o:[['no','No'],['yes','Yes']] },
  ],
  spin: [
    { id:'spin_entrada', t:'op', n:'How did it start?',
      o:[['slow','Flying too slow'],['turn','Sharp turn'],['input','Pilot input']] },
    { id:'spin_salida', t:'op', n:'Exit', o:[['solo','On its own'],['input','With input'],['reserve','Reserve']] },
  ],
};

/* ============================================================
   ESTADO DEL FORMULARIO
   ============================================================ */
let F = nuevoForm();
let paso = 1;

/* El track parseado. Ya NO es un array suelto: lleva los puntos y
   los metadatos (fecha, altitudes, duración) que saca el parser. */
let track = null;
/* Posibles anomalías: sitios donde MIRAR, no el evento. */
let anomalias = [];

function nuevoForm() {
  return {
    tipo: 'incident', site: '',
    /* la fecha inicial es HOY, del reloj del dispositivo, en su
       zona horaria local. Nada de constantes. */
    fecha: hoyISO(), hora: '',
    lat: null, lon: null, zona: '',
    fase: '', evento: '', resultado: '', injury: 'none',
    windDir: '', windKmh: '', gustKmh: '',
    thermal: '', turb: '', cloud: '', meteo: '', comentarios: '',
    ala: '', modelo: '', clase: '', talla: '', harness: '', reserva: '', exp: '',
    igc: false, igcNombre: '', altAgl: '',
    factores: '', lecciones: '', recomendar: '',
    extra: {},
  };
}

const PASOS = ['report.step.type','report.step.basics','report.step.conditions','report.step.equipment','report.step.igc','report.step.narrative'];
const PASOS_VUELO = ['report.step.quick'];

/* ============================================================
   PINTAR
   ============================================================ */
/* ============================================================
   VUELO SIN INCIDENTES — ENTRADA PROPIA
   ============================================================
   Pam pidió que esto no estuviera escondido dentro del flujo de
   reportar. Es el DENOMINADOR: sin vuelos registrados, los
   reportes no se pueden poner en contexto. Si cuesta rellenarlo,
   nadie lo rellena, así que son tres campos y ya.

   Se guarda aparte, con su propia función, para que no pueda
   fallar por culpa del formulario grande. */
export function pintaVueloRapido() {
  /* ===== OJO CON ESTO =====
     #app TIENE la clase .vista. Si primero se enciende y luego se
     recorren todas las .vista apagandolas, se apaga a si mismo y la
     vista sale EN BLANCO. Pam: "no me deja hacer reporte". El
     contenedor se excluye de la lista. */
  document.querySelectorAll('.vista').forEach(x => {
    if (x.id !== 'app') x.classList.remove('on');
  });
  const cont = document.getElementById('app');
  cont.classList.add('on');
  const hoy = hoyISO();

  cont.innerHTML = `<div class="cont" style="padding-top:10px;padding-bottom:40px">
    <button class="btn gh mb" id="vVolver">← ${escapa(t('common.back'))}</button>

    <div class="hero" style="padding:6px 0 0">
      <h1>${escapa(t('safeFlight.title'))}</h1>
      <p class="lema">${escapa(t('safeFlight.lede'))}</p>
    </div>

    <section class="bloque">
      <div class="card">
        <div class="campo"><label>${escapa(t('safeFlight.site'))}</label>
          <select id="vSite" class="${F.vSite ? '' : ''}">
            <option value="">${escapa(t('safeFlight.chooseSite'))}</option>
            ${SITES.map(s => `<option value="${s.id}"${F.vSite === s.id ? ' selected' : ''}>${escapa(s.n)} — ${escapa(s.pais)}</option>`).join('')}
          </select></div>

        <div class="campo"><label>${escapa(t('safeFlight.date'))}</label>
          <input type="date" id="vFecha" value="${escapa(F.vFecha || hoy)}"></div>

        <div class="campo"><label>${escapa(t('safeFlight.type'))}</label>
          <div class="opciones">
            ${['local','soaring','XC','training','competition','ground']
              .map(v => `<button class="op${F.vTipo === v ? ' on' : ''}" data-vtipo="${v}">${
                escapa(t('flight.' + v))}</button>`).join('')}
          </div></div>

        <button class="btn pri grande bloque mt2" id="vEnviar">✓ ${escapa(t('safeFlight.log'))}</button>
      </div>

      <div class="card mt" style="background:var(--bg-2);border-style:dashed">
        <p class="sub">${escapa(t('safeFlight.why'))}</p>
        <p class="mini mt" id="vCuenta"></p>
      </div>
    </section>
  </div>`;

  const cuenta = () => {
    const n = est.vuelos.filter(v => v.site === F.vSite).length;
    const el = document.getElementById('vCuenta');
    if (!el) return;
    el.textContent = F.vSite
      ? `${n} ${t('common.flightsLogged')} · ${sitioNombre(F.vSite)}` +
        (n < AJUSTES.minVuelosParaTasa ? ` · ${t('site.sampleSmall')}` : '')
      : '';
  };

  document.getElementById('vVolver').onclick = () => ir('inicio');
  document.querySelectorAll('[data-vtipo]').forEach(b => b.onclick = () => {
    F.vTipo = b.dataset.vtipo;
    document.querySelectorAll('[data-vtipo]').forEach(x => x.classList.toggle('on', x.dataset.vtipo === F.vTipo));
  });
  const sel = document.getElementById('vSite');
  sel.onchange = () => { F.vSite = sel.value; cuenta(); };
  const fe = document.getElementById('vFecha');
  fe.onchange = () => { F.vFecha = fe.value; };
  cuenta();

  document.getElementById('vEnviar').onclick = async () => {
    if (!F.vSite || !F.vTipo) { aviso(t('safeFlight.needSite')); return; }
    const b = document.getElementById('vEnviar');
    b.disabled = true; b.textContent = '…';
    /* el vuelo va a Supabase si está conectado; si no, se queda en
       el teléfono y se dice. Nunca se pierde. */
    const r = await enviaVuelo({ id: null, site: F.vSite, fecha: F.vFecha || hoy, tipo: F.vTipo });
    const local = { id: r.id, site: F.vSite, fecha: F.vFecha || hoy, tipo: F.vTipo, anon: true,
                    demo: enModoDemo() };
    est.vuelos = [local, ...est.vuelos];
    F.vSite = ''; F.vTipo = '';
    aviso(r.ok ? t('safeFlight.logged') : t('status.offlineSaved'), 4200);
    ir('inicio');
  };
}

function sitioNombre(id) {
  const s = SITES.find(x => x.id === id);
  return s ? s.n : id;
}

export function pintaReportar(arg) {
  if (arg === 'igc') paso = 5;
  const cont = document.getElementById('app');
  cont.classList.add('on');
  /* #app lleva la clase .vista: excluirla, o se apaga a si misma */
  document.querySelectorAll('.vista').forEach(x => {
    if (x.id !== 'app') x.classList.remove('on');
  });
  cont.innerHTML = `<div class="cont" style="padding-top:10px;padding-bottom:40px">
    <button class="btn gh mb" id="rVolver">← ${escapa(t('common.back'))}</button>
    <div id="rCuerpo"></div>
  </div>`;
  document.getElementById('rVolver').onclick = () => ir('inicio');
  pintaPaso();
}

function pintaPaso() {
  const rapido = F.tipo === 'safe_flight';
  /* OJO: esto son CLAVES del diccionario, no texto. Antes eran cadenas en
     ingles ('Type', 'Basics'...) y por eso los pasos se quedaban sin traducir
     aunque el resto del formulario cambiara de idioma. */
  const listaPasos = rapido ? PASOS_VUELO : PASOS;
  const c = document.getElementById('rCuerpo');
  if (!c) return;
  if (paso > listaPasos.length) paso = listaPasos.length;

  let html = `<div class="hero" style="padding:6px 0 0">
    <h1>${escapa(t('report.title'))}</h1>
    <p class="lema">${rapido
      ? escapa(t('safeFlight.lede'))
      : escapa(t('report.lede'))}</p>
  </div>`;

  html += `<div class="pasos mt2">${listaPasos.map((n, i) =>
    `<span class="paso-n${paso === i + 1 ? ' on' : paso > i + 1 ? ' hecho' : ''}">${
      paso > i + 1 ? '✓ ' : (i + 1) + '. '}${escapa(t(n))}</span>`).join('')}</div>`;

  html += rapido ? pasoVuelo() : [null, pasoTipo, pasoBasico, pasoCondiciones,
    pasoEquipo, pasoIGC, pasoNarrativa][paso]();

  /* navegacion */
  if (rapido) {
    html += `<div class="row mt2"><button class="btn pri grande" id="rEnviar" style="flex:1">
      ${escapa(t('safeFlight.log'))}</button></div>`;
  } else {
    html += `<div class="row mt2">
      ${paso > 1 ? `<button class="btn sec" id="rAtras">← ${escapa(t('common.back'))}</button>` : ''}
      ${paso < listaPasos.length
        ? `<button class="btn pri" id="rSig" style="flex:1">${escapa(t('common.continue'))} →</button>`
        : `<button class="btn pri grande" id="rEnviar" style="flex:1">${escapa(t('report.submit'))}</button>`}
    </div>`;
  }

  /* el snapshot en vivo, segun vas escribiendo */
  if (!rapido && (F.evento || F.fase)) {
    html += `<section class="bloque"><div class="cab"><h2>${escapa(t('snapshot.title'))}</h2>
      <span class="mini">${escapa(t('snapshot.updates'))}</span></div><div id="snapVivo"></div></section>`;
  }

  c.innerHTML = html;
  enganchaPaso();
  if (document.getElementById('snapVivo')) pintaSnapshotVivo();
}

/* ---------- PASO 1: TIPO ---------- */
function pasoTipo() {
  return `<section class="bloque"><div class="cab"><h2>${escapa(t('report.what'))}</h2></div>
    <div class="opciones col">
      ${TIPOS_REPORTE.map(x => `<button class="op${F.tipo === x.id ? ' on' : ''}"
        data-tipo="${x.id}"><b>${escapa(t('tp.' + x.id))}</b>
        <small>${escapa(t('type.' + x.id + '.d'))}</small></button>`).join('')}
    </div></section>`;
}

/* ---------- SAFE FLIGHT LOG ---------- */
function pasoVuelo() {
  return `<section class="bloque"><div class="cab"><h2>${escapa(t('safeFlight.title'))}</h2></div>
    <div class="card">
      <div class="campo"><label>${escapa(t('report.site'))}</label>
        <select id="fSite"><option value="">${escapa(t('safeFlight.chooseSite'))}</option>
          ${SITES.map(s => `<option value="${s.id}"${F.site === s.id ? ' selected' : ''}>${escapa(s.n)}</option>`).join('')}
        </select></div>
      <div class="campo"><label>${escapa(t('report.date'))}</label>
        <input type="date" id="fFecha" value="${escapa(F.fecha)}"></div>
      <div class="campo"><label>${escapa(t('safeFlight.type'))}</label>
        <div class="opciones">
          ${['local','soaring','XC','training','competition','ground']
            .map(v => `<button class="op${F.tipoVuelo === v ? ' on' : ''}" data-vuelo="${v}">${
              escapa(t('flight.' + v))}</button>`).join('')}
        </div></div>
      <p class="mini">${escapa(t('safeFlight.why'))}</p>
    </div>
    <div class="card mt" style="background:var(--bg-2);border-style:dashed">
      <p class="sub"><b>${est.vuelos.length} flights logged</b> across ${SITES.length} sites so far.</p>
      <p class="mini mt">Indicators built on fewer than 30 logged flights are shown with a
      clear warning. The sample is still small.</p>
    </div></section>`;
}

/* ---------- PASO 2: BÁSICO ---------- */
function pasoBasico() {
  const sz = (SITES.find(s => s.id === F.site) || {}).zonas || [];
  return `<section class="bloque"><div class="cab"><h2>${escapa(t('igc.whereTitle'))}</h2></div>
  <div class="card">
    <div class="campo"><label>${escapa(t('report.site'))}</label>
      <select id="fSite"><option value="">${escapa(t('safeFlight.chooseSite'))}</option>
        ${SITES.map(s => `<option value="${s.id}"${F.site === s.id ? ' selected' : ''}>${escapa(s.n)} — ${escapa(s.pais)}</option>`).join('')}
      </select></div>

    ${sz.length ? `<div class="campo"><label>${escapa(t('report.zone'))} <span class="mini">(${escapa(t('common.optional'))})</span></label>
      <div class="opciones">
        <button class="op${!F.zona ? ' on' : ''}" data-zona="">${escapa(t('report.notSure'))}</button>
        ${sz.map(z => {
          const t = (TIPOS_ZONA.find(x => x.id === z.t) || {}).n || z.t;
          return `<button class="op${F.zona === z.id ? ' on' : ''}" data-zona="${z.id}">
            ${escapa(z.n)}<small>${escapa(t)}</small></button>`;
        }).join('')}
      </div>
      <p class="pista">${escapa(t('report.zoneHelp'))}</p></div>` : ''}

    <div class="row wrap" style="gap:12px">
      <div class="campo" style="flex:1;min-width:150px"><label>${escapa(t('report.date'))}</label>
        <input type="date" id="fFecha" value="${escapa(F.fecha)}"></div>
      <div class="campo" style="flex:1;min-width:120px"><label>${escapa(t('report.time'))}</label>
        <input type="text" id="fHora" placeholder="14:30" value="${escapa(F.hora)}"></div>
    </div>

    <div class="campo"><label>${escapa(t('report.location'))}</label>
      <div id="mapaElegir" style="height:230px;border-radius:8px;overflow:hidden;border:1px solid var(--line-2)"></div>
      <p class="pista" id="pistaCoord">${escapa(t('report.tapMap'))} ${
        F.lat ? `${F.lat.toFixed(4)}, ${F.lon.toFixed(4)}` : escapa(t('igc.setSiteOnly'))}</p>
    </div>
  </div>

  <div class="card mt">
    <div class="campo"><label>${escapa(t('report.phase'))}</label>
      <div class="opciones">${FASES.map(f =>
        `<button class="op${F.fase === f.id ? ' on' : ''}" data-fase="${f.id}">${escapa(f.n)}</button>`).join('')}</div></div>

    <div class="campo"><label>${escapa(t('report.event'))}</label>
      <div class="opciones">${EVENTOS.map(e =>
        `<button class="op${F.evento === e.id ? ' on' : ''}" data-ev="${e.id}">${escapa(e.n)}</button>`).join('')}</div></div>

    <div class="campo"><label>${escapa(t('common.outcome'))}</label>
      <div class="opciones">${RESULTADOS.map(r =>
        `<button class="op${F.resultado === r.id ? ' on' : ''}" data-res="${r.id}">${escapa(r.n)}</button>`).join('')}</div></div>

    <div class="campo"><label>${escapa(t('common.injury'))}</label>
      <div class="opciones">${SEVERIDAD.map(s =>
        `<button class="op${F.injury === s.id ? ' on' : ''}" data-inj="${s.id}">${escapa(s.n)}</button>`).join('')}</div>
      <p class="pista">${escapa(t('report.injuryNote'))}</p></div>
  </div>

  ${F.evento && EXTRA[F.evento] ? `
  <div class="card mt" style="border-color:var(--blue-2)">
    <h3>${escapa(t('report.aboutEvent'))}</h3>
    <p class="mini mb">${escapa(t('report.aboutEventHelp'))}</p>
    ${EXTRA[F.evento].map(q => campoExtra(q)).join('')}
  </div>` : ''}
  <div class="card mt">
    <div class="campo"><label>${escapa(t('report.altitude'))}
      <span class="mini">(${escapa(t('common.optional'))})</span></label>
      <input type="number" id="fAlt" placeholder="120" value="${escapa(F.altAgl)}"></div>
  </div></section>`;
}

function campoExtra(q) {
  const v = F.extra[q.id] || '';
  if (q.t === 'op') {
    return `<div class="campo"><label>${escapa(q.n)}</label>
      <div class="opciones">${q.o.map(([id, n]) =>
        `<button class="op${v === id ? ' on' : ''}" data-extra="${q.id}" data-val="${id}">${escapa(n)}</button>`).join('')}</div></div>`;
  }
  return `<div class="campo"><label>${escapa(q.n)}</label>
    <input type="text" data-extra-txt="${q.id}" placeholder="${escapa(q.p || '')}" value="${escapa(v)}">
    ${q.p ? `<p class="pista">${escapa(q.p)}</p>` : ''}</div>`;
}

/* ---------- PASO 3: CONDICIONES ---------- */
function pasoCondiciones() {
  return `<section class="bloque"><div class="cab"><h2>${escapa(t('report.conditionsTitle'))}</h2>
    <span class="mini">as you felt them, not from a model</span></div>
  <div class="card">
    <div class="campo"><label>${escapa(t('report.windDir'))}</label>
      <div class="opciones">${DIRECCIONES.map(d =>
        `<button class="op${F.windDir === d ? ' on' : ''}" data-dir="${d}">${d}</button>`).join('')}</div></div>
    <div class="row wrap" style="gap:12px">
      <div class="campo" style="flex:1;min-width:130px"><label>${escapa(t('common.windSpeed'))}</label>
        <input type="number" id="fKmh" placeholder="18" value="${escapa(F.windKmh)}"></div>
      <div class="campo" style="flex:1;min-width:130px"><label>${escapa(t('common.gusts'))}</label>
        <input type="number" id="fGust" placeholder="27" value="${escapa(F.gustKmh)}"></div>
    </div>
    <div class="campo"><label>${escapa(t('common.thermal'))}</label>
      <div class="opciones">${['weak','moderate','strong','none']
        .map(v => `<button class="op${F.thermal === v ? ' on' : ''}" data-th="${v}">${
          escapa(t('cond.' + v))}</button>`).join('')}</div></div>
    <div class="campo"><label>${escapa(t('common.turbulence'))}</label>
      <div class="opciones">${['light','moderate','strong','violent']
        .map(v => `<button class="op${F.turb === v ? ' on' : ''}" data-tb="${v}">${
          escapa(t('cond.' + v))}</button>`).join('')}</div></div>
    <div class="campo"><label>${escapa(t('common.cloud'))}</label>
      <div class="opciones">${['clear','few','scattered','overcast']
        .map(v => `<button class="op${F.cloud === v ? ' on' : ''}" data-cl="${v}">${
          escapa(t('cond.' + v))}</button>`).join('')}</div></div>
    <div class="campo"><label>${escapa(t('report.weatherNotes'))}
      <span class="mini">(${escapa(t('common.optional'))})</span></label>
      <textarea id="fMeteo" placeholder="Dust devils at the field after 16:00…">${escapa(F.meteo)}</textarea></div>
    <p class="mini">${escapa(t('report.weatherFuture'))}</p>
  </div></section>`;
}

/* ---------- PASO 4: EQUIPO ---------- */
function pasoEquipo() {
  return `<section class="bloque"><div class="cab"><h2>Equipment</h2>
    <span class="mini">${escapa(t('report.equipmentHelp'))}</span></div>
  <div class="card">
    <div class="row wrap" style="gap:12px">
      <div class="campo" style="flex:1;min-width:140px"><label>${escapa(t('report.wingBrand'))}</label>
        <input type="text" id="fAla" placeholder="Ozone" value="${escapa(F.ala)}"></div>
      <div class="campo" style="flex:1;min-width:140px"><label>${escapa(t('report.wingModel'))}</label>
        <input type="text" id="fModelo" placeholder="Delta 4" value="${escapa(F.modelo)}"></div>
    </div>
    <div class="campo"><label>${escapa(t('common.class'))}</label>
      <div class="opciones">${['A','B','C','D','CCC','Competition'].map(c =>
        `<button class="op${F.clase === c ? ' on' : ''}" data-cls="${c}">${c}</button>`).join('')}</div></div>
    <div class="row wrap" style="gap:12px">
      <div class="campo" style="flex:1;min-width:120px"><label>${escapa(t('report.wingSize'))}</label>
        <input type="text" id="fTalla" placeholder="MS" value="${escapa(F.talla)}"></div>
      <div class="campo" style="flex:1;min-width:140px"><label>${escapa(t('common.harness'))}</label>
        <input type="text" id="fHarness" placeholder="Pod" value="${escapa(F.harness)}"></div>
    </div>
    <div class="campo"><label>${escapa(t('common.reserve'))}</label>
      <input type="text" id="fReserva" placeholder="Brand / model" value="${escapa(F.reserva)}"></div>
    <div class="campo"><label>${escapa(t('report.experience'))}</label>
      <div class="opciones">${['less1','1-3','3-5','5-10','10+']
        .map(v => `<button class="op${F.exp === v ? ' on' : ''}" data-exp="${v}">${
          escapa(t('exp.' + v))}</button>`).join('')}</div>
      <p class="pista">${escapa(t('report.experienceNote'))}</p></div>
  </div></section>`;
}

/* ---------- PASO 5: IGC ---------- */
function pasoIGC() {
  const hayTrack = track && track.puntos && track.puntos.length;
  return `<section class="bloque"><div class="cab"><h2>${escapa(t('igc.title'))}</h2>
    <span class="mini">${escapa(t('common.optional'))}</span></div>

  ${!hayTrack ? `
  <div class="card">
    <div id="zonaDrop" class="drop">
      <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor"
           stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M12 16V4"/><path d="m7 9 5-5 5 5"/><path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/></svg>
      <b>${escapa(t('igc.drop'))}</b>
      <p class="mini">${escapa(t('igc.orTap'))}</p>
      <input type="file" id="fIGC" accept=".igc" style="display:none">
    </div>
    <div id="igcError" class="oculto mt" style="background:var(--red-bg);border:1px solid #e8c8c4;
      border-radius:8px;padding:12px">
      <b>${escapa(t('igc.cantParse'))}</b>
      <p class="mini" id="igcMotivo"></p>
      <div class="row wrap mt" style="gap:8px">
        <button class="btn sec" id="igcOtro">${escapa(t('igc.tryAnother'))}</button>
        <button class="btn gh" id="igcSin">${escapa(t('igc.continueWithout'))}</button>
      </div>
    </div>
  </div>` : `
  <div class="card">
    <div class="entre">
      <b>${escapa(t('igc.loaded', { n: track.meta.puntos, a: track.meta.desde, b: track.meta.hasta }))}</b>
      <button class="btn gh" id="igcQuitar">✕</button>
    </div>
  </div>`}

  ${F.igcVentana ? `
  <!-- ===== CONFIRMAR EL MOMENTO DEL EVENTO =====
       Esto es lo que hacía mal antes: se daba por hecho que el evento era el
       punto de mayor caída. No tiene por qué: un cravat, un roce con otro ala,
       un enganche en el despegue o un problema de líneas no se parecen en nada
       a una caída fuerte. Así que SkyReport PROPONE sitios donde mirar y la
       persona confirma dónde fue. Hasta que no confirma, no hay Black Box. -->
  <div class="card mt" style="border-color:var(--blue-2)">
    <h3>${escapa(t('igc.suggestTitle'))}</h3>
    <p class="mini mb">${escapa(t('igc.suggestHelp'))}</p>

    <div id="mapaEvento" style="height:250px;border-radius:10px;overflow:hidden;border:1px solid var(--line)"></div>

    <div class="campo mt">
      <label>${escapa(t('igc.confirm'))}</label>
      <input type="range" id="sliderEvento" min="0" max="${track.puntos.length - 1}"
             value="${F.igcPunto || 0}" step="1" class="slider">
      <div class="entre mini mono mt">
        <span id="horaDesde">${escapa(track.meta.desde)}</span>
        <b id="horaElegida">${escapa(horaBonita((track.puntos[F.igcPunto || 0] || {}).hora))} UTC</b>
        <span id="horaHasta">${escapa(track.meta.hasta)}</span>
      </div>
    </div>

    ${anomalias.length ? `
    <div class="mt2">
      <h4>${escapa(t('igc.anomalies'))}</h4>
      <p class="mini mb">${escapa(t('box.observation'))}</p>
      ${anomalias.map(a => `<button class="op anom" data-irA="${a.t}">${escapa(a.txt)}</button>`).join('')}
    </div>` : `<p class="mini mt">${escapa(t('igc.noAnomalies'))}</p>`}

    <button class="btn pri grande bloque mt2" id="igcConfirma">
      ✓ ${escapa(t('igc.confirm'))}</button>
    ${F.igcConfirmado ? `<p class="mini mt centro" id="igcOk">
      ${escapa(t('igc.confirmed', { h: horaBonita(F.igcHora) }))}</p>` : ''}
  </div>` : ''}

  ${F.igcConfirmado ? `
  <div class="card mt">
    <div class="cab"><h3>${escapa(t('box.title'))}</h3>
      <span class="mini">${escapa(t('box.window'))}</span></div>
    <div id="timeline"></div>
    <div id="excepciones" class="mt"></div>
  </div>` : ''}

  <div class="card mt" style="background:var(--bg-2)">
    <h4>${escapa(t('igc.privacyTitle'))}</h4>
    <p class="sub mt">${escapa(t('igc.privacy'))}</p>
  </div>
  </section>`;
}

/* ---------- PASO 6: NARRATIVA ---------- */
function pasoNarrativa() {
  return `<section class="bloque"><div class="cab"><h2>${escapa(t('report.narrativeTitle'))}</h2>
    <span class="mini">${escapa(t('report.narrativeHelp'))}</span></div>
  <div class="card">
    <div class="campo"><label>${escapa(t('report.whatHappened'))}</label>
      <textarea id="fFactores" placeholder="On the lee side of the ridge, on a NW day…">${escapa(F.factores)}</textarea></div>
    <div class="campo"><label>${escapa(t('report.contributing'))}
      <span class="mini">(${escapa(t('common.optional'))})</span></label>
      <textarea id="fContrib" placeholder="The wind was stronger than forecast…">${escapa(F.contrib || '')}</textarea></div>
    <div class="campo"><label>${escapa(t('report.lessons'))}
      <span class="mini">(${escapa(t('common.optional'))})</span></label>
      <textarea id="fLecciones" placeholder="If the drift is faster than the climb, move out…">${escapa(F.lecciones)}</textarea></div>
    <div class="campo"><label>${escapa(t('report.advice'))}
      <span class="mini">(${escapa(t('common.optional'))})</span></label>
      <textarea id="fRecomendar" placeholder="Ask locally which side of the ridge is working…">${escapa(F.recomendar)}</textarea></div>
  </div>
  <div class="card mt"><div class="cab"><h3>${escapa(t('common.dataCompleteness'))}</h3></div>
    <div id="completitud"></div></div>
  </section>`;
}

function pintaSnapshotVivo() {
  const el = document.getElementById('snapVivo');
  if (!el) return;
  el.innerHTML = EventSnapshot({ rep: { ...F, id: 'DRAFT' }, nSimilares: 0 });
  const c = document.getElementById('completitud');
  if (c) c.innerHTML = DataCompleteness({ rep: F });
}

/* ============================================================
   ENGANCHAR
   ============================================================ */
function guardaCampos() {
  const g = (id) => { const e = document.getElementById(id); return e ? e.value : null; };
  ['fFecha','fHora','fKmh','fGust','fMeteo','fAla','fModelo','fTalla','fHarness',
   'fReserva','fFactores','fContrib','fLecciones','fRecomendar','fAlt']
    .forEach(id => {
      const v = g(id);
      if (v == null) return;
      const mapa = { fFecha:'fecha', fHora:'hora', fKmh:'windKmh', fGust:'gustKmh',
        fMeteo:'meteo', fAla:'ala', fModelo:'modelo', fTalla:'talla', fHarness:'harness',
        fReserva:'reserva', fFactores:'factores', fContrib:'contrib', fLecciones:'lecciones',
        fRecomendar:'recomendar', fAlt:'altAgl' };
      F[mapa[id]] = v;
    });
  const sel = g('fSite');
  if (sel != null) F.site = sel;
  document.querySelectorAll('[data-extra-txt]').forEach(i => { F.extra[i.dataset.extraTxt] = i.value; });
}

function enganchaPaso() {
  const on = (sel, ev, fn) => document.querySelectorAll(sel).forEach(e => e.addEventListener(ev, fn));

  on('[data-tipo]', 'click', e => {
    guardaCampos();
    F.tipo = e.currentTarget.dataset.tipo;
    paso = 1; pintaPaso();
  });
  on('[data-vuelo]', 'click', e => { F.tipoVuelo = e.currentTarget.dataset.vuelo; guardaCampos(); pintaPaso(); });

  const uno = (attr, campo) => on(`[data-${attr}]`, 'click', e => {
    guardaCampos();
    F[campo] = e.currentTarget.dataset[attr];
    if (campo === 'evento') F.extra = {};
    pintaPaso();
  });
  uno('zona', 'zona'); uno('fase', 'fase'); uno('ev', 'evento');
  uno('res', 'resultado'); uno('inj', 'injury'); uno('dir', 'windDir');
  uno('th', 'thermal'); uno('tb', 'turb'); uno('cl', 'cloud');
  uno('cls', 'clase'); uno('exp', 'exp');

  on('[data-extra]', 'click', e => {
    guardaCampos();
    F.extra[e.currentTarget.dataset.extra] = e.currentTarget.dataset.val;
    pintaPaso();
  });

  const sig = document.getElementById('rSig');
  if (sig) sig.onclick = () => { guardaCampos(); paso++; pintaPaso(); window.scrollTo({ top: 0 }); };
  const atr = document.getElementById('rAtras');
  if (atr) atr.onclick = () => { guardaCampos(); paso--; pintaPaso(); window.scrollTo({ top: 0 }); };
  const env = document.getElementById('rEnviar');
  if (env) env.onclick = envia;

  /* el mapa de elegir punto */
  import('./mapa.js').then(m => {
    if (document.getElementById('mapaElegir')) m.mapaElegir(F, (la, lo) => {
      F.lat = la; F.lon = lo;
      const p = document.getElementById('pistaCoord');
      if (p) p.textContent = `${la.toFixed(4)}, ${lo.toFixed(4)}`;
    });

    /* ===== EL SELECTOR DEL MOMENTO DEL EVENTO =====
       Con el track ya parseado, se pinta el mapa y un deslizador para
       elegir el punto. Se puede mover el deslizador o tocar una de las
       anomalías detectadas, que salta el marcador a ese momento — pero
       ese momento no es "el evento": es un sitio donde mirar. */
    const sl = document.getElementById('sliderEvento');
    if (sl && track) {
      const marca = m.mapaEvento(track.puntos, 'mapaEvento', (i) => {
        F.igcPunto = i;
        if (sl) sl.value = i;
        pintaHora();
      });
      const pintaHora = () => {
        const p = track.puntos[F.igcPunto || 0] || {};
        const h = document.getElementById('horaElegida');
        if (h) h.textContent = horaBonita(p.hora) + ' UTC';
      };
      sl.oninput = () => { F.igcPunto = +sl.value; pintaHora(); if (mueveMarca) mueveMarca(+sl.value); };
      var mueveMarca = marca;

      document.querySelectorAll('[data-irA]').forEach(b => b.onclick = () => {
        const t = +b.dataset.irA;
        let mejor = 0, d = Infinity;
        track.puntos.forEach((p, i) => { const dd = Math.abs(p.t - t); if (dd < d) { d = dd; mejor = i; } });
        F.igcPunto = mejor;
        sl.value = mejor;
        pintaHora();
        if (mueveMarca) mueveMarca(mejor);
      });

      const conf = document.getElementById('igcConfirma');
      if (conf) conf.onclick = () => {
        const p = track.puntos[F.igcPunto || 0];
        if (!p) { aviso(t('igc.needConfirm')); return; }
        F.igcConfirmado = true;
        F.igcHora = p.hora;
        F.igcTs = p.t;
        F.igcLat = p.lat;
        F.igcLon = p.lon;
        F.lat = F.lat == null ? p.lat : F.lat;
        F.lon = F.lon == null ? p.lon : F.lon;
        F.igcMeta = Object.assign({}, F.igcMeta, {
          event_timestamp: p.hora, event_lat: p.lat, event_lon: p.lon,
        });
        aviso(t('igc.confirmed', { h: horaBonita(p.hora) }));
        pintaPaso();
        /* y la Black Box, montada alrededor de ESTE momento */
        const v = ventanaEvento(track.puntos, p.t);
        import('./mapa.js').then(mm => {
          if (document.getElementById('timeline')) mm.pintaTimeline(track.puntos, 'timeline', 'excepciones', p.t);
        });
      };
    }
  });

  /* IGC: arrastrar o elegir */
  const drop = document.getElementById('zonaDrop');
  const file = document.getElementById('fIGC');
  if (drop && file) {
    drop.onclick = () => file.click();
    file.onchange = () => { if (file.files[0]) cargaIGC(file.files[0]); };
    ['dragenter','dragover'].forEach(ev => drop.addEventListener(ev, e => {
      e.preventDefault(); drop.style.borderColor = 'var(--blue)';
    }));
    ['dragleave','drop'].forEach(ev => drop.addEventListener(ev, e => {
      e.preventDefault(); drop.style.borderColor = 'var(--line-2)';
    }));
    drop.addEventListener('drop', e => {
      const f = e.dataTransfer.files[0];
      if (f) cargaIGC(f);
    });
  }
}

/* ============================================================
   CARGAR UN IGC
   ============================================================
   Regla que no se rompe: si el archivo no se entiende, se dice.
   NUNCA se mete un track de mentira y se hace pasar por el del
   usuario. La versión anterior hacía justo eso, y es la peor
   clase de error que puede tener esta app: alguien creería estar
   viendo lo que hizo su ala cuando ve unos datos inventados.

   Un track de demostración solo aparece si la app está en modo
   demo, y entonces se avisa en pantalla. */
async function cargaIGC(f) {
  const fallo = (motivo) => {
    track = null; anomalias = [];
    F.igc = false; F.igcVentana = false; F.igcConfirmado = false;
    pintaPaso();
    const e = document.getElementById('igcError');
    const m = document.getElementById('igcMotivo');
    if (e) e.classList.remove('oculto');
    if (m) m.textContent = motivo;
    const b = document.getElementById('igcOtro');
    if (b) b.onclick = () => pintaPaso();
    const c = document.getElementById('igcSin');
    if (c) c.onclick = () => { F.igc = false; paso = 5; pintaPaso(); };
  };

  if (!/\.igc$/i.test(f.name)) { fallo(t('igc.notIgc')); return; }

  let texto = '';
  try { texto = await f.text(); }
  catch (e) { fallo(t('igc.readError')); return; }

  const r = parseIGC(texto);
  if (!r.ok) { fallo(r.motivo || t('igc.cantParse')); return; }

  track = { puntos: r.puntos, meta: r.meta, nombre: f.name };
  anomalias = posiblesAnomalias(r.puntos);
  F.igc = true;
  F.igcNombre = f.name;
  F.igcVentana = true;
  F.igcConfirmado = false;
  F.igcPunto = 0;
  F.igcMeta = {
    puntos: r.meta.puntos, desde: r.meta.desde, hasta: r.meta.hasta,
    duracion_s: r.meta.duracionS, alt_max: r.meta.altMax, alt_min: r.meta.altMin,
    tiene_barometrica: r.meta.tieneBarometrica, tiene_gps: r.meta.tieneGPS,
    anomalias: anomalias.map(a => ({ tipo: a.tipo, hora: a.hora })),
  };
  aviso(t('igc.loaded', { n: r.meta.puntos, a: r.meta.desde, b: r.meta.hasta }), 5200);
  pintaPaso();
}

/* ============================================================
   ENVIAR
   ============================================================ */
async function envia() {
  guardaCampos();

  /* --- registro de vuelo sin incidentes: rapidisimo --- */
  if (F.tipo === 'safe_flight') {
    if (!F.site || !F.tipoVuelo) { aviso(t('safeFlight.needSite')); return; }
    const v = { id: null, site: F.site, fecha: F.fecha, tipo: F.tipoVuelo };
    const r = await enviaVuelo(v);
    est.vuelos = [{ ...v, id: r.id || 'local', anon: true, demo: enModoDemo() }, ...est.vuelos];
    F = nuevoForm(); paso = 1;
    aviso(r.ok ? t('safeFlight.logged') : t('status.offlineSaved'), 4400);
    ir('inicio');
    return;
  }

  /* --- reporte normal --- */
  if (F.igcVentana && !F.igcConfirmado) { aviso(t('igc.needConfirm'), 4200); return; }

  const falta = [];
  if (!F.site) falta.push(t('report.site'));
  if (!F.fase) falta.push(t('report.phase'));
  if (!F.evento) falta.push(t('report.event'));
  if (falta.length) { aviso('Still needed: ' + falta.join(', ')); return; }

  const s = SITES.find(x => x.id === F.site) || {};
  const rep = {
    ...F,
    id: 'R-' + Date.now(),
    demo: false,
    lat: F.lat != null ? F.lat : (s.lat || 0),
    lon: F.lon != null ? F.lon : (s.lon || 0),
    windKmh: F.windKmh ? +F.windKmh : null,
    gustKmh: F.gustKmh ? +F.gustKmh : null,
    altAgl: F.altAgl ? +F.altAgl : '',
    fecha: F.fecha || '2026-09-20',
  };
  /* se guarda en el teléfono SIEMPRE (por si acaso) y además se
     intenta enviar. Si no hay conexión, queda en la cola y se dice. */
  const previos = JSON.parse(localStorage.getItem(CLAVE_LOCAL) || '[]');
  guardaLocal(CLAVE_LOCAL, [rep, ...previos]);

  const envio = await enviaReporte(rep, rep.completo);
  cargaDatos();

  F = nuevoForm(); paso = 1; track = null; anomalias = [];
  aviso(envio.ok ? t('report.submittedPending') : t('status.offlineSaved'), 5200);
  ir('inicio');
}
