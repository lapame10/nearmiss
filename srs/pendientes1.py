#!/usr/bin/env python3
"""Los pendientes tecnicos: 1, 2, 3 y 5 de la lista de Pam.

1. CRITICO — igcDemo() ya no se usa en reportes reales
   Estaba en app.js:805. Al abrir la ficha de cualquier reporte con igc:true,
   se generaba un track SINTETICO y se pintaba como si fuera la reconstruccion
   del IGC de esa persona. Es lo mas grave que puede hacer esta app: alguien
   creeria estar viendo lo que hizo su ala.

   Regla nueva:
     - si el reporte es demo Y la app esta en modo demo  -> track de demo,
       avisado en pantalla
     - si hay puntos reales guardados                    -> se usan
     - si solo hay metadata del IGC, sin puntos          -> NO hay Black Box,
       se dice que no esta guardada

2. La fecha hardcodeada '2026-09-20' en report.js

3. Fugas de i18n: 'Still needed: ', 'Apply', 'N reports ·'

5. aviso() con textContent en vez de innerHTML
"""
BASE = '/Users/lapame10/.hermes/workspace/nearmiss/srs/'
toc = 0

# ============================================================
# 1 — EL IGC DE VERDAD O NINGUNO
# ============================================================
s = open(BASE + 'app.js', encoding='utf-8').read()

viejo = """    if (vista === 'reporte' && arg) {
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
    }"""

nuevo = """    if (vista === 'reporte' && arg) {
      const rep = est.reps.find(r => r.id === arg);
      /* ============================================================
         LA BLACK BOX — SOLO CON DATOS DEL REPORTE
         ============================================================
         Aqui habia esto:

             if (rep && rep.igc) {
               const tr = igcDemo(rep.lat, rep.lon);   // <-- INVENTADO
               m.mapaTrack(tr, 'mapaTrack');
               m.pintaTimeline(tr, 'timeline', 'excepciones');
             }

         Es decir: bastaba con que el reporte dijera 'tengo IGC' para que la
         app pintara un track SINTETICO y lo presentara como la reconstruccion
         del vuelo de esa persona. Sin decirlo en ningun sitio.

         Eso no puede pasar, por dos razones. La primera es que es mentira, y
         una app de seguridad no puede permitirse mentir ni un poco: si alguien
         cree estar viendo lo que hizo su ala cuando ve numeros inventados,
         puede sacar conclusiones equivocadas sobre su propio vuelo. La
         segunda es que los datos inventados son verosimiles: tienen la forma
         de un track real, asi que no hay forma de que el lector lo note.

         La regla ahora:
           - Demo Mode + reporte demo  -> track de demostracion, y se avisa
           - puntos reales guardados   -> se usan esos
           - solo metadata, sin puntos -> NO hay Black Box, y se dice por que
         ============================================================ */
      if (rep && rep.igc) {
        const esDemo = rep.demo === true && enModoDemo();
        const puntos = Array.isArray(rep.igcTrack) && rep.igcTrack.length
          ? rep.igcTrack : null;

        if (puntos) {
          /* datos de verdad del reporte */
          m.mapaTrack(puntos, 'mapaTrack');
          m.pintaTimeline(puntos, 'timeline', 'excepciones', rep.igcEventoTs);
        } else if (esDemo) {
          /* solo aqui se permite inventar, y se dice en pantalla */
          const tr = igcDemo(rep.lat, rep.lon);
          const av = document.getElementById('avisoTrack');
          if (av) av.textContent = t('igc.demoTrack');
          m.mapaTrack(tr, 'mapaTrack');
          m.pintaTimeline(tr, 'timeline', 'excepciones');
        } else {
          /* hay IGC, pero no se guardo el track: NO se inventa nada */
          const caja = document.getElementById('trackNoGuardado');
          if (caja) caja.classList.remove('oculto');
        }
      }
    }"""
if viejo in s:
    s = s.replace(viejo, nuevo, 1); toc += 1
    print('  1. app.js: la Black Box ya no inventa datos')

# ============================================================
# 5 — aviso() con textContent
# ============================================================
v5a = """export function aviso(txt, ms = 3200) {
  const a = $('#aviso');
  if (!a) return;
  a.innerHTML = txt;"""
n5a = """export function aviso(txt, ms = 3200) {
  const a = $('#aviso');
  if (!a) return;
  /* textContent, no innerHTML: los avisos solo llevan texto. Con innerHTML
     cualquier cosa que acabe dentro de un mensaje se interpreta como HTML, y
     eso es una via de inyeccion que no hace falta tener abierta. */
  a.textContent = txt;"""
if v5a in s:
    s = s.replace(v5a, n5a, 1); toc += 1
    print('  5. app.js: aviso() con textContent')

v5b = """    setTimeout(() => { a.innerHTML = ''; }, 260);"""
n5b = """    setTimeout(() => { a.textContent = ''; }, 260);"""
if v5b in s:
    s = s.replace(v5b, n5b, 1); toc += 1
    print('  5. app.js: y al vaciar, igual')

open(BASE + 'app.js', 'w', encoding='utf-8').write(s)

# ============================================================
# 2 — la ultima fecha hardcodeada
# ============================================================
s = open(BASE + 'report.js', encoding='utf-8').read()
v2 = """    fecha: F.fecha || '2026-09-20',"""
n2 = """    /* hoyISO(), no una constante: la fecha de un reporte real sale del reloj
       del dispositivo. Las fechas fijas solo viven en los datos de demo. */
    fecha: F.fecha || hoyISO(),"""
if v2 in s:
    s = s.replace(v2, n2, 1); toc += 1
    print('  2. report.js: la fecha hardcodeada')

# ============================================================
# 3 — las tres fugas de i18n
# ============================================================
v3a = """  if (falta.length) { aviso('Still needed: ' + falta.join(', ')); return; }"""
n3a = """  if (falta.length) { aviso(t('report.needFields', { x: falta.join(', ') })); return; }"""
if v3a in s:
    s = s.replace(v3a, n3a, 1); toc += 1
    print('  3. report.js: "Still needed"')

open(BASE + 'report.js', 'w', encoding='utf-8').write(s)

# ============================================================
# 3 — las fugas de mapa.js
# ============================================================
s = open(BASE + 'mapa.js', encoding='utf-8').read()
v3b = """    <button class="btn pri" id="fAplicar">Apply</button></div>`;"""
n3b = """    <button class="btn pri" id="fAplicar">${escapa(t('common.apply'))}</button></div>`;"""
if v3b in s:
    s = s.replace(v3b, n3b, 1); toc += 1
    print('  3. mapa.js: el boton "Apply"')

v3c = """        <span style="color:#8c939b;font-size:12px">${s.n} reports ·
        ${escapa(fechaLarga(s.desde))} – ${escapa(fechaLarga(s.hasta))}</span><br>"""
n3c = """        <span style="color:#8c939b;font-size:12px">${escapa(t('signals.relatedShort', { n: s.n }))} ·
        ${escapa(fechaLarga(s.desde))} – ${escapa(fechaLarga(s.hasta))}</span><br>"""
if v3c in s:
    s = s.replace(v3c, n3c, 1); toc += 1
    print('  3. mapa.js: el popup de senales')

open(BASE + 'mapa.js', 'w', encoding='utf-8').write(s)

print('\n  cambios:', toc)
