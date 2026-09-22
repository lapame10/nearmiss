#!/usr/bin/env python3
"""El paso 3: Evento.

Se comporta distinto segun haya IGC o no:

  CON IGC  -> primero marcar el momento del evento (el slider, el mapa y las
              anomalias que ya existian, movidos aqui desde el paso 5), y
              despues confirmar tipo de evento, fase y resultado. Los datos que
              ya salieron del archivo no se vuelven a preguntar.

  SIN IGC  -> el formulario manual de siempre, entero, sin recortar nada.

El paso manual NO se toca: se renombra pasoBasico -> pasoManual y se llama tal
cual desde aqui. Si el cambio del IGC no funciona como se esperaba, el camino
sin IGC queda exactamente como estaba.
"""
BASE = '/Users/lapame10/.hermes/workspace/nearmiss/srs/'
import re
toc = 0
s = open(BASE + 'report.js', encoding='utf-8').read()

# ---------- 1) el formulario manual, renombrado pero sin tocar ----------
if 'function pasoManual() {' not in s:
    s = s.replace('function pasoBasico() {',
                  """/* El formulario manual de siempre. Con IGC casi no se usa, sin IGC es el
   camino principal. No se le ha cambiado nada. */
function pasoManual() {""", 1)
    toc += 1
    print('  ok: pasoBasico -> pasoManual (sin tocar nada dentro)')

# ---------- 2) el paso Evento ----------
NUEVO = '''/* ============================================================
   PASO 3: EL EVENTO
   ============================================================
   Es el paso que mas cambia segun el camino.

   SIN IGC: el formulario manual entero. Sitio, fecha, hora, ubicacion, fase,
   tipo de evento y resultado. Es lo que habia antes, sin recortes.

   CON IGC: el archivo ya dijo donde, cuando y como fue el vuelo, asi que este
   paso empieza por lo unico que el archivo NO puede saber: DONDE estuvo el
   evento. Se propone el track, se marcan posibles anomalias como sitios donde
   mirar, y la persona confirma.

   Lo de 'posibles anomalias' es importante: el sistema NO decide cual fue el
   evento. Una caida fuerte, un giro brusco o un corte del track son motivos
   para mirar ahi, no diagnosticos. Un cravat, un roce o un problema de lineas
   no se parecen en nada a una caida fuerte, y solo el piloto sabe que paso.

   Hasta que no confirma, no hay Black Box y el reporte no tiene hora de evento.
   ============================================================ */
function pasoEvento() {
  const hayTrack = track && track.puntos && track.puntos.length;
  if (!hayTrack) return pasoManual();

  const p = track.puntos[F.igcPunto || 0] || {};
  const res = F.igcResumen || {};

  return `<section class="bloque">
  <div class="cab"><h2>${escapa(t('igc.markTitle'))}</h2>
    <span class="mini">${escapa(t('igc.markHelp'))}</span></div>

  <!-- ===== lo que se saco del archivo ===== -->
  <div class="card" style="border-color:var(--blue-2)">
    <div class="entre">
      <b>✓ ${escapa(t('igc.loaded'))}</b>
      <span class="mini">${escapa(res.fecha || '')}${res.hora ? ' · ' + escapa(res.hora) + ' UTC' : ''}</span>
    </div>
    ${res.site ? `<p class="mini mt">${escapa(t('common.site'))}: <b>${escapa(res.site)}</b></p>` : ''}
  </div>

  <!-- ===== el track y el slider ===== -->
  <div class="card mt">
    <div id="mapaEvento" style="height:250px;border-radius:10px;overflow:hidden;border:1px solid var(--line)"></div>

    <div class="campo mt">
      <label>${escapa(t('igc.confirm'))}</label>
      <input type="range" id="sliderEvento" min="0" max="${track.puntos.length - 1}"
             value="${F.igcPunto || 0}" step="1" class="slider">
      <div class="entre mini mono mt">
        <span id="horaDesde">${escapa(track.meta.desde)}</span>
        <b id="horaElegida">${escapa(horaBonita(p.hora))} UTC</b>
        <span id="horaHasta">${escapa(track.meta.hasta)}</span>
      </div>
    </div>

    <!-- lo que se sabe de ese punto concreto -->
    <dl class="mets mt" id="datosPunto">
      ${p.altGps != null ? `<div class="fila"><dt>${escapa(t('igc.altGps'))}</dt>
        <dd>${escapa(String(p.altGps))} m</dd></div>` : ''}
      ${p.altBaro != null ? `<div class="fila"><dt>${escapa(t('igc.altBaro'))}</dt>
        <dd>${escapa(String(p.altBaro))} m</dd></div>` : ''}
      ${p.vel != null ? `<div class="fila"><dt>${escapa(t('igc.speed'))}</dt>
        <dd>${escapa(String(p.vel))} km/h</dd></div>` : ''}
      ${p.velVert != null ? `<div class="fila"><dt>${escapa(t('igc.vertical'))}</dt>
        <dd>${escapa(String(p.velVert))} m/s</dd></div>` : ''}
      ${p.rumbo != null ? `<div class="fila"><dt>${escapa(t('igc.heading'))}</dt>
        <dd>${escapa(String(p.rumbo))}°</dd></div>` : ''}
    </dl>

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
  </div>

  <!-- ===== la black box, solo despues de confirmar ===== -->
  ${F.igcConfirmado ? `
  <div class="card mt">
    <div class="cab"><h3>${escapa(t('box.title'))}</h3>
      <span class="mini">${escapa(t('box.window'))}</span></div>
    <div id="timeline"></div>
    <div id="excepciones" class="mt"></div>
  </div>` : ''}

  <!-- ===== lo que el archivo NO puede saber ===== -->
  <div class="card mt">
    <div class="cab"><h3>${escapa(t('igc.whatHappened'))}</h3>
      <span class="mini">${escapa(t('igc.whatHappenedHelp'))}</span></div>

    <div class="campo"><label>${escapa(t('report.eventType'))}</label>
      <div class="opciones col">
        ${EVENTOS.slice(0, 12).map(e => `<button class="op${F.evento === e.id ? ' on' : ''}"
          data-evento="${e.id}">${escapa(nombreEv(e.id))}</button>`).join('')}
        <button class="op${F.evento && !EVENTOS.slice(0, 12).some(e => e.id === F.evento) ? ' on' : ''}"
          data-evento="unknown">${escapa(t('ev.unknown'))}</button>
      </div>
    </div>

    <div class="campo mt2"><label>${escapa(t('report.phase'))}</label>
      <div class="opciones">
        ${FASES.map(f => `<button class="op${F.fase === f.id ? ' on' : ''}"
          data-fase="${f.id}">${escapa(nombreFase(f.id))}</button>`).join('')}
      </div>
    </div>

    <div class="campo mt2"><label>${escapa(t('report.outcome'))}</label>
      <div class="opciones">
        ${RESULTADOS.map(r => `<button class="op${F.resultado === r.id ? ' on' : ''}"
          data-resultado="${r.id}">${escapa(nombreRes(r.id))}</button>`).join('')}
      </div>
    </div>

    ${['deployed', 'injury', 'material'].includes(F.resultado) ? `
    <div class="campo mt2"><label>${escapa(t('report.serious'))}</label>
      <div class="opciones">
        ${SEVERIDAD.map(s => `<button class="op${F.cons === s.id ? ' on' : ''}"
          data-cons="${s.id}">${escapa(t('cons.' + s.id))}</button>`).join('')}
      </div>
    </div>` : ''}
  </div>
  </section>`;
}

'''

# lo inserto antes del paso de condiciones
marca = '/* ---------- PASO 3: CONDICIONES'
if marca not in s:
    marca = 'function pasoCondiciones() {'
    m = re.search(r'/\* -+ PASO \d+[^\n]*\n', s[:s.find('function pasoCondiciones')][::-1])
    # busco hacia atras el comentario del paso de condiciones
    i = s.rfind('/*', 0, s.find('function pasoCondiciones'))
    marca = s[i:i+60] if i > 0 else 'function pasoCondiciones() {'
if marca in s:
    s = s.replace(marca, NUEVO + marca, 1)
    toc += 1
    print('  ok: pasoEvento, insertado')
else:
    print('  ✗ no encontre donde insertar pasoEvento')

open(BASE + 'report.js', 'w', encoding='utf-8').write(s)
print('  cambios:', toc)
