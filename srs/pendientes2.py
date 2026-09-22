#!/usr/bin/env python3
"""Punto 4 (accesibilidad de las tarjetas) y las claves que faltan.

LAS TARJETAS

Antes eran <article class="card clic" data-rep="ID"> con un onclick puesto por
JavaScript. Eso funciona con el dedo y con el raton, y con nada mas:

  - no se puede llegar a ellas con el tabulador
  - Enter no hace nada
  - un lector de pantalla no sabe que llevan a algun sitio
  - si el JavaScript falla, no navegan

Ahora son enlaces de verdad:

  <a class="card clic" href="#reporte/ID" data-rep="ID">

El href funciona solo, aunque el JavaScript no cargue. Y se sigue
interceptando el click para que la navegacion sea instantanea, sin recargar.
"""
BASE = '/Users/lapame10/.hermes/workspace/nearmiss/srs/'
toc = 0
s = open(BASE + 'app.js', encoding='utf-8').read()

# ---------- ReportCard ----------
v = """  return `<article class="card clic" data-rep="${escapa(rep.id)}">"""
n = """  return `<a class="card clic" href="#reporte/${escapa(rep.id)}" data-rep="${escapa(rep.id)}">"""
if v in s: s = s.replace(v, n, 1); toc += 1; print('  ReportCard → enlace')

# ---------- SignalCard ----------
v = """  return `<article class="card clic" data-sig="${escapa(sig.id)}">"""
n = """  return `<a class="card clic" href="#senal/${escapa(sig.id)}" data-sig="${escapa(sig.id)}">"""
if v in s: s = s.replace(v, n, 1); toc += 1; print('  SignalCard → enlace')

# ---------- SiteCard ----------
v = """  return `<article class="card clic" data-site="${escapa(s.id)}">"""
n = """  return `<a class="card clic" href="#sitio/${escapa(s.id)}" data-site="${escapa(s.id)}">"""
if v in s: s = s.replace(v, n, 1); toc += 1; print('  SiteCard → enlace')

# ---------- y sus cierres </article> → </a> ----------
# van uno a uno: busco los </article> que cierran cada tarjeta
for marca, q in [("""<div class="mt2"><span class="btn gh">${escapa(t('common.viewReport'))} →</span></div>
  </article>`;""",
                  'el cierre de ReportCard'),
                 ("""    <div class="mt2"><span class="btn gh">${escapa(t('signals.viewRelated'))} →</span></div>
  </article>`;""",
                  'el cierre de SignalCard'),
                 ("""    <p class="mini mt">${escapa(t('common.lastReport'))}: ${st.ultimo ? escapa(hace(st.ultimo.fecha)) : '—'}</p>
  </article>`;""",
                  'el cierre de SiteCard')]:
    v = marca
    n = marca.replace('</article>`;', '</a>`;')
    if v in s:
        s = s.replace(v, n, 1); toc += 1; print('  %s' % q)

open(BASE + 'app.js', 'w', encoding='utf-8').write(s)

# ============================================================
# LAS CLAVES QUE FALTAN
# ============================================================
s = open(BASE + 'i18n.js', encoding='utf-8').read()
T = [
 # clave, es, fr, de, pt, en
 ('signals.relatedShort', '{n} reportes', '{n} signalements', '{n} Meldungen', '{n} relatos', '{n} reports'),
 ('igc.noTrackStored', 'IGC disponible — la reconstrucción del track no está guardada para este reporte.',
  'IGC disponible — la reconstitution du tracé n’est pas enregistrée pour ce signalement.',
  'IGC verfügbar — die Track-Rekonstruktion ist für diese Meldung nicht gespeichert.',
  'IGC disponível — a reconstrução do percurso não está guardada para este relato.',
  'IGC available — track reconstruction is not stored for this report.'),
 ('igc.noTrackStoredHelp', 'No se muestra ninguna reconstrucción para no inventar datos. Si el piloto adjuntó el archivo, el sistema puede recalcularla a partir de él.',
  'Aucune reconstitution n’est affichée pour ne pas inventer de données. Si le pilote a joint le fichier, le système peut la recalculer à partir de celui-ci.',
  'Es wird keine Rekonstruktion angezeigt, um keine Daten zu erfinden. Wenn der Pilot die Datei angehängt hat, kann das System sie daraus neu berechnen.',
  'Não é mostrada nenhuma reconstrução para não inventar dados. Se o piloto anexou o ficheiro, o sistema pode recalculá-la a partir dele.',
  'No reconstruction is shown rather than inventing data. If the pilot attached the file, the system can recalculate it from there.'),
]
n_claves = 0
for claves in T:
    k = claves[0]
    for idioma, valor in [('EN',claves[5]),('ES',claves[1]),('FR',claves[2]),('DE',claves[3]),('PT',claves[4])]:
        i = s.find('const %s = {' % idioma); j = s.find('\n};', i)
        if ("'%s':" % k) in s[i:j]: continue
        comilla = '"' if "'" in valor else "'"
        s = s[:j] + "\n  '%s': %s%s%s," % (k, comilla, valor, comilla) + s[j:]
        n_claves += 1
open(BASE + 'i18n.js', 'w', encoding='utf-8').write(s)
print('  claves nuevas: %d' % n_claves)
