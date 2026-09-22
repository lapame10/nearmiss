#!/usr/bin/env python3
"""El IGC al principio del flujo de Reportar.

POR QUE

El IGC estaba en el paso 5, casi al final. Y ahi es donde peor esta: si el
piloto tiene el archivo, ese archivo ya sabe la fecha, la hora, el sitio, la
duracion, las altitudes, la velocidad y el rumbo. Pedir todo eso a mano y
despues decir 'ah, tambien puedes subir el IGC' es al reves.

Ahora el IGC es el atajo, no una tarea mas al final.

ANTES:  Tipo · Basico · Condiciones · Equipo · IGC · Narrativa
AHORA:  Tipo · IGC · Evento · Condiciones · Equipo · Narrativa

El paso 3 (Evento) se comporta distinto segun haya IGC o no:
  con IGC   -> marcar el momento del evento, y revisar lo que ya se saco
  sin IGC   -> el formulario manual de siempre, tal cual estaba

LO QUE NO SE TOCA
  - el parser (srs/igc.js): se usa el que hay, tal cual
  - el mapa del evento, el slider y las anomalias: se reutilizan moviendolos
  - el paso manual: es la misma funcion, sin cambios
  - la Black Box, el Event Snapshot, la privacidad del IGC
"""
BASE = '/Users/lapame10/.hermes/workspace/nearmiss/srs/'
toc = 0
s = open(BASE + 'report.js', encoding='utf-8').read()


def rep(v, n, q):
    global s, toc
    if v in s:
        s = s.replace(v, n, 1); toc += 1; print('  ok:', q)
    else:
        print('  ✗ NO COINCIDIO:', q)


# ============================================================
# 1 — el orden de los pasos
# ============================================================
rep("""const PASOS = ['report.step.type','report.step.basics','report.step.conditions','report.step.equipment','report.step.igc','report.step.narrative'];""",
    """/* EL IGC VA SEGUNDO, no quinto.
   El archivo ya sabe la fecha, la hora, la posicion, la duracion y lo que hizo
   la vela. Pedir todo eso a mano y luego ofrecer el IGC es el orden equivocado:
   con el archivo delante, la mitad del formulario sobra. */
const PASOS = ['report.step.type','report.step.igc','report.step.event','report.step.conditions','report.step.equipment','report.step.narrative'];""",
    'el orden de los pasos')

rep("""  html += rapido ? pasoVuelo() : [null, pasoTipo, pasoBasico, pasoCondiciones,
    pasoEquipo, pasoIGC, pasoNarrativa][paso]();""",
    """  html += rapido ? pasoVuelo() : [null, pasoTipo, pasoIGC, pasoEvento,
    pasoCondiciones, pasoEquipo, pasoNarrativa][paso]();""",
    'el orden al pintar')


# ============================================================
# 2 — pasoIGC: ahora es la PREGUNTA, al principio
# ============================================================
i = s.find('function pasoIGC() {')
j = s.find('/* ---------- PASO 6: NARRATIVA ---------- */')
if i < 0 or j < 0:
    raise SystemExit('  ✗ no encontre el bloque de pasoIGC')

NUEVO_IGC = '''/* ============================================================
   PASO 2: EL IGC
   ============================================================
   Una sola pregunta: tienes el archivo de este vuelo o no.

   Si lo tienes, se sube AQUI y SkyReport saca del archivo todo lo que puede
   sacar de forma fiable (fecha, hora, sitio aproximado, duracion, altitudes,
   velocidad, rumbo, y el viento si viene o se puede estimar). Eso se le ensena
   al piloto antes de seguir, para que vea que ha funcionado.

   Si no lo tienes, se sigue a mano exactamente igual que antes. El IGC nunca
   es obligatorio.
   ============================================================ */
function pasoIGC() {
  const hayTrack = track && track.puntos && track.puntos.length;
  const res = F.igcResumen;

  /* ---------- ya esta cargado: el resumen de lo que se saco ---------- */
  if (hayTrack && res) {
    return `<section class="bloque"><div class="cab"><h2>${escapa(t('igc.stepTitle'))}</h2></div>

  <div class="card" style="border-color:var(--green,#5b7c5a)">
    <div class="entre">
      <b>✓ ${escapa(t('igc.loaded'))}</b>
      <button class="btn gh" id="igcQuitar">✕</button>
    </div>
    <dl class="mets mt">
      <div class="fila"><dt>${escapa(t('igc.detected'))}</dt>
        <dd>${escapa(res.fecha)}${res.hora ? ' · ' + escapa(res.hora) + ' UTC' : ''}</dd></div>
      ${res.site ? `<div class="fila"><dt>${escapa(t('common.site'))}</dt>
        <dd>${escapa(res.site)}</dd></div>` : ''}
      ${res.duracion ? `<div class="fila"><dt>${escapa(t('igc.duration'))}</dt>
        <dd>${escapa(res.duracion)}</dd></div>` : ''}
      <div class="fila"><dt>${escapa(t('igc.points'))}</dt>
        <dd>${escapa(String(res.puntos))}</dd></div>
      ${res.altMax ? `<div class="fila"><dt>${escapa(t('igc.altMax'))}</dt>
        <dd>${escapa(res.altMax)}</dd></div>` : ''}
    </dl>
  </div>

  <div class="card mt" style="background:var(--bg-2)">
    <h4>${escapa(t('igc.privacyTitle'))}</h4>
    <p class="sub mt">${escapa(t('igc.privacy'))}</p>
  </div>
  </section>`;
  }

  /* ---------- la pregunta ---------- */
  return `<section class="bloque"><div class="cab"><h2>${escapa(t('igc.stepTitle'))}</h2></div>

  <div class="card">
    <p class="sub">${escapa(t('igc.stepHelp'))}</p>

    ${!F.igcSin ? `
    <div id="zonaDrop" class="drop mt2">
      <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor"
           stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M12 16V4"/><path d="m7 9 5-5 5 5"/><path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/></svg>
      <b>${escapa(t('igc.upload'))}</b>
      <p class="mini">${escapa(t('igc.orTap'))}</p>
      <input type="file" id="fIGC" accept=".igc" style="display:none">
    </div>

    <button class="btn gh bloque mt" id="igcSin">${escapa(t('igc.continueWithout'))}</button>

    <div id="igcError" class="oculto mt" style="background:var(--red-bg);border:1px solid #e8c8c4;
      border-radius:8px;padding:12px">
      <b>${escapa(t('igc.cantParse'))}</b>
      <p class="mini" id="igcMotivo"></p>
      <div class="row wrap mt" style="gap:8px">
        <button class="btn sec" id="igcOtro">${escapa(t('igc.tryAnother'))}</button>
        <button class="btn gh" id="igcSin2">${escapa(t('igc.continueWithout'))}</button>
      </div>
    </div>` : `
    <p class="mini mt2">${escapa(t('igc.withoutHint'))}</p>`}
  </div>
  </section>`;
}

'''

s = s[:i] + NUEVO_IGC + s[j:]
toc += 1
print('  ok: pasoIGC, reescrito como la pregunta del principio')

open(BASE + 'report.js', 'w', encoding='utf-8').write(s)
print('  cambios:', toc)
