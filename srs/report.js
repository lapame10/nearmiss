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
let track = null;

function nuevoForm() {
  return {
    tipo: 'incident', site: '', fecha: '2026-09-20', hora: '',
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

const PASOS = ['Type', 'Basics', 'Conditions', 'Equipment', 'IGC', 'Narrative'];
const PASOS_VUELO = ['Type', 'Quick log'];

/* ============================================================
   PINTAR
   ============================================================ */
export function pintaReportar(arg) {
  if (arg === 'igc') paso = 5;
  const cont = document.getElementById('app');
  cont.classList.add('on');
  document.querySelectorAll('.vista').forEach(x => x.classList.remove('on'));
  cont.innerHTML = `<div class="cont" style="padding-top:10px;padding-bottom:40px">
    <button class="btn gh mb" id="rVolver">← Back</button>
    <div id="rCuerpo"></div>
  </div>`;
  document.getElementById('rVolver').onclick = () => ir('inicio');
  pintaPaso();
}

function pintaPaso() {
  const rapido = F.tipo === 'safe_flight';
  const listaPasos = rapido ? PASOS_VUELO : PASOS;
  const c = document.getElementById('rCuerpo');
  if (!c) return;
  if (paso > listaPasos.length) paso = listaPasos.length;

  let html = `<div class="hero" style="padding:6px 0 0">
    <h1>Report</h1>
    <p class="lema">${rapido
      ? 'A flight where nothing happened. Three fields and you are done.'
      : 'The form changes with the event. You only answer what is relevant.'}</p>
  </div>`;

  html += `<div class="pasos mt2">${listaPasos.map((n, i) =>
    `<span class="paso-n${paso === i + 1 ? ' on' : paso > i + 1 ? ' hecho' : ''}">${
      paso > i + 1 ? '✓ ' : (i + 1) + '. '}${escapa(n)}</span>`).join('')}</div>`;

  html += rapido ? pasoVuelo() : [null, pasoTipo, pasoBasico, pasoCondiciones,
    pasoEquipo, pasoIGC, pasoNarrativa][paso]();

  /* navegacion */
  if (rapido) {
    html += `<div class="row mt2"><button class="btn pri grande" id="rEnviar" style="flex:1">
      Log this flight</button></div>`;
  } else {
    html += `<div class="row mt2">
      ${paso > 1 ? '<button class="btn sec" id="rAtras">← Back</button>' : ''}
      ${paso < listaPasos.length
        ? '<button class="btn pri" id="rSig" style="flex:1">Continue →</button>'
        : '<button class="btn pri grande" id="rEnviar" style="flex:1">Submit report</button>'}
    </div>`;
  }

  /* el snapshot en vivo, segun vas escribiendo */
  if (!rapido && (F.evento || F.fase)) {
    html += `<section class="bloque"><div class="cab"><h2>Event snapshot</h2>
      <span class="mini">updates as you type</span></div><div id="snapVivo"></div></section>`;
  }

  c.innerHTML = html;
  enganchaPaso();
  if (document.getElementById('snapVivo')) pintaSnapshotVivo();
}

/* ---------- PASO 1: TIPO ---------- */
function pasoTipo() {
  return `<section class="bloque"><div class="cab"><h2>What are you reporting?</h2></div>
    <div class="opciones col">
      ${TIPOS_REPORTE.map(t => `<button class="op${F.tipo === t.id ? ' on' : ''}"
        data-tipo="${t.id}"><b>${escapa(t.n)}</b><small>${escapa(t.d)}</small></button>`).join('')}
    </div></section>`;
}

/* ---------- SAFE FLIGHT LOG ---------- */
function pasoVuelo() {
  return `<section class="bloque"><div class="cab"><h2>Safe flight log</h2></div>
    <div class="card">
      <div class="campo"><label>Site</label>
        <select id="fSite"><option value="">Choose a site…</option>
          ${SITES.map(s => `<option value="${s.id}"${F.site === s.id ? ' selected' : ''}>${escapa(s.n)}</option>`).join('')}
        </select></div>
      <div class="campo"><label>Date</label>
        <input type="date" id="fFecha" value="${escapa(F.fecha)}"></div>
      <div class="campo"><label>Type of flight</label>
        <div class="opciones">
          ${[['local','Local'],['soaring','Soaring'],['XC','Cross country'],
             ['training','Training'],['competition','Competition'],['ground','Ground handling']]
            .map(([v, n]) => `<button class="op${F.tipoVuelo === v ? ' on' : ''}" data-vuelo="${v}">${n}</button>`).join('')}
        </div></div>
      <p class="mini">That is all. Logging flights where nothing happened is what lets
      SkyReport put incident numbers in context.</p>
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
  return `<section class="bloque"><div class="cab"><h2>Where and when</h2></div>
  <div class="card">
    <div class="campo"><label>Site</label>
      <select id="fSite"><option value="">Choose a site…</option>
        ${SITES.map(s => `<option value="${s.id}"${F.site === s.id ? ' selected' : ''}>${escapa(s.n)} — ${escapa(s.pais)}</option>`).join('')}
      </select></div>

    ${sz.length ? `<div class="campo"><label>Zone within the site <span class="mini">(optional)</span></label>
      <div class="opciones">
        <button class="op${!F.zona ? ' on' : ''}" data-zona="">Not sure</button>
        ${sz.map(z => {
          const t = (TIPOS_ZONA.find(x => x.id === z.t) || {}).n || z.t;
          return `<button class="op${F.zona === z.id ? ' on' : ''}" data-zona="${z.id}">
            ${escapa(z.n)}<small>${escapa(t)}</small></button>`;
        }).join('')}
      </div>
      <p class="pista">Zones are what let SkyReport say "behind this ridge" instead of
      just naming the site.</p></div>` : ''}

    <div class="row wrap" style="gap:12px">
      <div class="campo" style="flex:1;min-width:150px"><label>Date</label>
        <input type="date" id="fFecha" value="${escapa(F.fecha)}"></div>
      <div class="campo" style="flex:1;min-width:120px"><label>Time</label>
        <input type="text" id="fHora" placeholder="14:30" value="${escapa(F.hora)}"></div>
    </div>

    <div class="campo"><label>Location on the map</label>
      <div id="mapaElegir" style="height:230px;border-radius:8px;overflow:hidden;border:1px solid var(--line-2)"></div>
      <p class="pista" id="pistaCoord">Tap the map to place the event.
        ${F.lat ? `Chosen: ${F.lat.toFixed(4)}, ${F.lon.toFixed(4)}` : 'You can also leave it and set the site only.'}</p>
    </div>
  </div>

  <div class="card mt">
    <div class="campo"><label>Flight phase</label>
      <div class="opciones">${FASES.map(f =>
        `<button class="op${F.fase === f.id ? ' on' : ''}" data-fase="${f.id}">${escapa(f.n)}</button>`).join('')}</div></div>

    <div class="campo"><label>Event type</label>
      <div class="opciones">${EVENTOS.map(e =>
        `<button class="op${F.evento === e.id ? ' on' : ''}" data-ev="${e.id}">${escapa(e.n)}</button>`).join('')}</div></div>

    <div class="campo"><label>Outcome</label>
      <div class="opciones">${RESULTADOS.map(r =>
        `<button class="op${F.resultado === r.id ? ' on' : ''}" data-res="${r.id}">${escapa(r.n)}</button>`).join('')}</div></div>

    <div class="campo"><label>Injury</label>
      <div class="opciones">${SEVERIDAD.map(s =>
        `<button class="op${F.injury === s.id ? ' on' : ''}" data-inj="${s.id}">${escapa(s.n)}</button>`).join('')}</div>
      <p class="pista">Injuries are recorded, never ranked.</p></div>
  </div>

  ${F.evento && EXTRA[F.evento] ? `
  <div class="card mt" style="border-color:var(--blue-2)">
    <h3>About this event</h3>
    <p class="mini mb">Only the questions that matter for this type.</p>
    ${EXTRA[F.evento].map(q => campoExtra(q)).join('')}
  </div>` : ''}
  <div class="card mt">
    <div class="campo"><label>Estimated altitude at the event (m AGL)
      <span class="mini">(optional)</span></label>
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
  return `<section class="bloque"><div class="cab"><h2>Conditions you observed</h2>
    <span class="mini">as you felt them, not from a model</span></div>
  <div class="card">
    <div class="campo"><label>Wind direction</label>
      <div class="opciones">${DIRECCIONES.map(d =>
        `<button class="op${F.windDir === d ? ' on' : ''}" data-dir="${d}">${d}</button>`).join('')}</div></div>
    <div class="row wrap" style="gap:12px">
      <div class="campo" style="flex:1;min-width:130px"><label>Wind speed (km/h)</label>
        <input type="number" id="fKmh" placeholder="18" value="${escapa(F.windKmh)}"></div>
      <div class="campo" style="flex:1;min-width:130px"><label>Gusts (km/h)</label>
        <input type="number" id="fGust" placeholder="27" value="${escapa(F.gustKmh)}"></div>
    </div>
    <div class="campo"><label>Thermal activity</label>
      <div class="opciones">${[['weak','Weak'],['moderate','Moderate'],['strong','Strong'],['none','None']]
        .map(([v, n]) => `<button class="op${F.thermal === v ? ' on' : ''}" data-th="${v}">${n}</button>`).join('')}</div></div>
    <div class="campo"><label>Turbulence felt</label>
      <div class="opciones">${[['light','Light'],['moderate','Moderate'],['strong','Strong'],['violent','Violent']]
        .map(([v, n]) => `<button class="op${F.turb === v ? ' on' : ''}" data-tb="${v}">${n}</button>`).join('')}</div></div>
    <div class="campo"><label>Cloud</label>
      <div class="opciones">${[['clear','Clear'],['few','Few'],['scattered','Scattered'],['overcast','Overcast']]
        .map(([v, n]) => `<button class="op${F.cloud === v ? ' on' : ''}" data-cl="${v}">${n}</button>`).join('')}</div></div>
    <div class="campo"><label>Anything else about the weather
      <span class="mini">(optional)</span></label>
      <textarea id="fMeteo" placeholder="Dust devils at the field after 16:00…">${escapa(F.meteo)}</textarea></div>
    <p class="mini">If SkyReport can pull weather data for this location and time later, it will
    be shown next to what you reported — never instead of it.</p>
  </div></section>`;
}

/* ---------- PASO 4: EQUIPO ---------- */
function pasoEquipo() {
  return `<section class="bloque"><div class="cab"><h2>Equipment</h2>
    <span class="mini">all optional</span></div>
  <div class="card">
    <div class="row wrap" style="gap:12px">
      <div class="campo" style="flex:1;min-width:140px"><label>Wing brand</label>
        <input type="text" id="fAla" placeholder="Ozone" value="${escapa(F.ala)}"></div>
      <div class="campo" style="flex:1;min-width:140px"><label>Model</label>
        <input type="text" id="fModelo" placeholder="Delta 4" value="${escapa(F.modelo)}"></div>
    </div>
    <div class="campo"><label>Class</label>
      <div class="opciones">${['A','B','C','D','CCC','Competition'].map(c =>
        `<button class="op${F.clase === c ? ' on' : ''}" data-cls="${c}">${c}</button>`).join('')}</div></div>
    <div class="row wrap" style="gap:12px">
      <div class="campo" style="flex:1;min-width:120px"><label>Size</label>
        <input type="text" id="fTalla" placeholder="MS" value="${escapa(F.talla)}"></div>
      <div class="campo" style="flex:1;min-width:140px"><label>Harness</label>
        <input type="text" id="fHarness" placeholder="Pod" value="${escapa(F.harness)}"></div>
    </div>
    <div class="campo"><label>Reserve</label>
      <input type="text" id="fReserva" placeholder="Brand / model" value="${escapa(F.reserva)}"></div>
    <div class="campo"><label>Approximate experience</label>
      <div class="opciones">${[['<1','<1 year'],['1-3','1–3 years'],['3-5','3–5 years'],
        ['5-10','5–10 years'],['10+','10+ years']]
        .map(([v, n]) => `<button class="op${F.exp === v ? ' on' : ''}" data-exp="${v}">${n}</button>`).join('')}</div>
      <p class="pista">A wide range, on purpose. SkyReport does not identify pilots and does not
      rate their level.</p></div>
  </div></section>`;
}

/* ---------- PASO 5: IGC ---------- */
function pasoIGC() {
  return `<section class="bloque"><div class="cab"><h2>Flight track</h2>
    <span class="mini">optional</span></div>
  <div class="card">
    <div id="zonaDrop" style="border:2px dashed var(--line-2);border-radius:12px;padding:28px 16px;
      text-align:center;background:var(--bg-2)">
      <b>Drop an IGC file here</b>
      <p class="mini mt">or tap to choose one</p>
      <input type="file" id="fIGC" accept=".igc" style="display:none">
      <p class="mini mt2" id="igcEstado">${F.igc
        ? `✓ ${escapa(F.igcNombre || 'track loaded')}` : 'No file yet'}</p>
    </div>
    <div class="mt2">
      <p class="sub">With a track, SkyReport can show what the wing was doing around the event:</p>
      <div class="fila-etq mt">
        <span class="etq">position</span><span class="etq">ground speed</span>
        <span class="etq">climb / sink</span><span class="etq">heading</span>
        <span class="etq">GPS altitude</span>
      </div>
    </div>
  </div>
  <div class="card mt" style="background:var(--bg-2)">
    <h4>Privacy</h4>
    <p class="sub mt">Your IGC is used to extract the conditions around the event. The original
    file is not published, the track is not published, and coordinates are rounded to about
    100 m before anything appears publicly.</p>
  </div>
  ${F.igc ? `<div class="card mt"><div class="cab"><h3>Track preview</h3>
    <span class="mini">T-120 s → T+60 s</span></div>
    <div id="mapaIGC" style="height:260px;border-radius:10px;overflow:hidden;
      border:1px solid var(--line)"></div></div>` : ''}
  </section>`;
}

/* ---------- PASO 6: NARRATIVA ---------- */
function pasoNarrativa() {
  return `<section class="bloque"><div class="cab"><h2>In your words</h2>
    <span class="mini">plain description, no blame</span></div>
  <div class="card">
    <div class="campo"><label>What happened</label>
      <textarea id="fFactores" placeholder="On the lee side of the ridge, on a NW day…">${escapa(F.factores)}</textarea></div>
    <div class="campo"><label>Anything that may have contributed
      <span class="mini">(optional)</span></label>
      <textarea id="fContrib" placeholder="The wind was stronger than forecast…">${escapa(F.contrib || '')}</textarea></div>
    <div class="campo"><label>What you took from it
      <span class="mini">(optional)</span></label>
      <textarea id="fLecciones" placeholder="If the drift is faster than the climb, move out…">${escapa(F.lecciones)}</textarea></div>
    <div class="campo"><label>What you would tell another pilot
      <span class="mini">(optional)</span></label>
      <textarea id="fRecomendar" placeholder="Ask locally which side of the ridge is working…">${escapa(F.recomendar)}</textarea></div>
  </div>
  <div class="card mt"><div class="cab"><h3>Data completeness</h3></div>
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

  /* el mapa de elegir punto y el de la pista */
  import('./mapa.js').then(m => {
    if (document.getElementById('mapaElegir')) m.mapaElegir(F, (la, lo) => {
      F.lat = la; F.lon = lo;
      const p = document.getElementById('pistaCoord');
      if (p) p.textContent = `Chosen: ${la.toFixed(4)}, ${lo.toFixed(4)}`;
    });
    if (document.getElementById('mapaIGC')) m.mapaTrack(track || igcDemo(20.5, -100.1), 'mapaIGC');
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

async function cargaIGC(f) {
  if (!/\.igc$/i.test(f.name)) { aviso('That does not look like an .igc file'); return; }
  const texto = await f.text();
  const lineas = texto.split('\n').filter(l => l.startsWith('B'));
  const pts = [];
  lineas.forEach(l => {
    if (l.length < 35) return;
    const hh = +l.slice(1, 3), mm = +l.slice(3, 5), ss = +l.slice(5, 7);
    const la = +l.slice(7, 15) / 100000, lo = +l.slice(15, 24) / 100000;
    const alt = +l.slice(30, 35);
    if (!isFinite(la) || !isFinite(lo)) return;
    pts.push({ t: hh * 3600 + mm * 60 + ss, lat: la, lon: lo, baroAlt: alt,
      gpsAlt: alt, hs: 0, vs: 0, heading: 0 });
  });
  if (!pts.length) {
    /* sin parser real: se usa un track de demostracion, pero se dice */
    track = igcDemo(20.5, -100.1);
    aviso('Track loaded as demonstration data');
  } else {
    /* velocidades y rumbos a partir de los puntos */
    for (let i = 1; i < pts.length; i++) {
      const a = pts[i - 1], b = pts[i];
      const dt = Math.max(1, b.t - a.t);
      const x = (b.lon - a.lon) * 111320 * Math.cos(b.lat * Math.PI / 180);
      const y = (b.lat - a.lat) * 110540;
      b.hs = Math.sqrt(x * x + y * y) / dt * 3.6;
      b.vs = (b.baroAlt - a.baroAlt) / dt;
      b.heading = (Math.atan2(x, y) * 180 / Math.PI + 360) % 360;
    }
    /* reetiqueto los tiempos como relativos al punto de mayor caida = EVENTO */
    let peor = 0;
    for (let i = 1; i < pts.length; i++) if (pts[i].vs < pts[peor].vs) peor = i;
    const t0 = pts[peor].t;
    track = pts.map(p => ({ ...p, t: p.t - t0 })).filter(p => p.t >= -120 && p.t <= 60);
    aviso('IGC loaded: ' + pts.length + ' points');
  }
  F.igc = true; F.igcNombre = f.name;
  pintaPaso();
}

/* ============================================================
   ENVIAR
   ============================================================ */
function envia() {
  guardaCampos();

  /* --- registro de vuelo sin incidentes: rapidisimo --- */
  if (F.tipo === 'safe_flight') {
    if (!F.site || !F.tipoVuelo) { aviso('Pick a site and a type of flight'); return; }
    const v = { id: 'SF-' + Date.now(), site: F.site, fecha: F.fecha,
      tipo: F.tipoVuelo, anon: true };
    const previos = JSON.parse(localStorage.getItem(CLAVE_VUELOS) || '[]');
    guardaLocal(CLAVE_VUELOS, [v, ...previos]);
    est.vuelos = [v, ...est.vuelos];
    F = nuevoForm(); paso = 1;
    aviso('Flight logged — thank you');
    ir('inicio');
    return;
  }

  /* --- reporte normal --- */
  const falta = [];
  if (!F.site) falta.push('site');
  if (!F.fase) falta.push('flight phase');
  if (!F.evento) falta.push('event type');
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
  const previos = JSON.parse(localStorage.getItem(CLAVE_LOCAL) || '[]');
  guardaLocal(CLAVE_LOCAL, [rep, ...previos]);
  cargaDatos();

  const { pct } = { pct: 0 };
  F = nuevoForm(); paso = 1; track = null;
  aviso('Report submitted' + (rep.igc ? ' — track attached' : ''));
  ir('inicio');
}
