#!/usr/bin/env python3
"""Los ultimos textos visibles: los ejemplos de los campos y el boton Refresh.

Que se traduce y que no:

  SI — los EJEMPLOS de texto que ve el usuario al escribir:
       'Dust devils at the field after 16:00…'
       'On the lee side of the ridge, on a NW day…'
       'Brand / model'
       y el boton 'Refresh' de la version nueva.

  NO — los nombres de marcas y modelos reales: Ozone, Delta 4, MS, Pod.
       Son nombres propios, se escriben igual en los cinco idiomas. Un piloto
       aleman tambien vuela un 'Delta 4'.

  NO — las unidades y siglas: km, km/h, AGL, IGC, UTC, m, s.

  NO — 'SkyReport' ni 'OpenStreetMap': son nombres propios.
"""
BASE = '/Users/lapame10/.hermes/workspace/nearmiss/'
import re
toc = 0

# ---------- 1) el HTML: el boton de actualizar ----------
h = open(BASE + 'index.html', encoding='utf-8').read()
v = """<button class="btn pri" id="bActualiza">Refresh</button>"""
n = """<button class="btn pri" id="bActualiza" data-i18n="update.refresh">Refresh</button>"""
if v in h:
    h = h.replace(v, n, 1); toc += 1
    print('  index.html: el boton Refresh')
v2 = """<span id="actualizaTxt">A new version of SkyReport is available.</span>"""
n2 = """<span id="actualizaTxt" data-i18n="update.available">A new version of SkyReport is available.</span>"""
if v2 in h:
    h = h.replace(v2, n2, 1); toc += 1
    print('  index.html: el texto de la version nueva')
open(BASE + 'index.html', 'w', encoding='utf-8').write(h)

# ---------- 2) los placeholders de ejemplo ----------
s = open(BASE + 'srs/report.js', encoding='utf-8').read()
CAMBIOS = [
 ('placeholder="Dust devils at the field after 16:00…"',
  'placeholder="${escapa(t(\'ph.meteo\'))}"'),
 ('placeholder="Brand / model"',
  'placeholder="${escapa(t(\'ph.reserva\'))}"'),
 ('placeholder="On the lee side of the ridge, on a NW day…"',
  'placeholder="${escapa(t(\'ph.factores\'))}"'),
 ('placeholder="The wind was stronger than forecast…"',
  'placeholder="${escapa(t(\'ph.contrib\'))}"'),
 ('placeholder="If the drift is faster than the climb, move out…"',
  'placeholder="${escapa(t(\'ph.lecciones\'))}"'),
 ('placeholder="Ask locally which side of the ridge is working…"',
  'placeholder="${escapa(t(\'ph.recomendar\'))}"'),
]
for v, n in CAMBIOS:
    if v in s:
        s = s.replace(v, n, 1); toc += 1
        print('  report.js: %s' % v[:46])
    else:
        print('  ⚠ no coincidio: %s' % v[:46])
open(BASE + 'srs/report.js', 'w', encoding='utf-8').write(s)

# ---------- 3) el tooltip EVENT ----------
s = open(BASE + 'srs/mapa.js', encoding='utf-8').read()
if "bindTooltip('EVENT'" in s:
    s = s.replace("bindTooltip('EVENT'", "bindTooltip(t('box.eventMark')", 1)
    toc += 1
    print('  mapa.js: el tooltip del evento')
open(BASE + 'srs/mapa.js', 'w', encoding='utf-8').write(s)

# ---------- 4) las claves ----------
s = open(BASE + 'srs/i18n.js', encoding='utf-8').read()
T = [
 ('ph.meteo', 'Remolinos de polvo en el campo después de las 16:00…',
  'Des tourbillons de poussière au terrain après 16h00…',
  'Staubteufel am Startplatz nach 16:00…',
  'Redemoinhos de pó no campo depois das 16:00…',
  'Dust devils at the field after 16:00…'),
 ('ph.reserva', 'Marca / modelo', 'Marque / modèle', 'Marke / Modell', 'Marca / modelo', 'Brand / model'),
 ('ph.factores', 'En el lado de socavón de la cresta, un día de NW…',
  'Du côté sous le vent de la crête, un jour de NW…',
  'Auf der Leeseite des Grats, an einem NW-Tag…',
  'No lado de sotavento da crista, num dia de NW…',
  'On the lee side of the ridge, on a NW day…'),
 ('ph.contrib', 'El viento era más fuerte de lo previsto…',
  'Le vent était plus fort que prévu…',
  'Der Wind war stärker als vorhergesagt…',
  'O vento estava mais forte do que o previsto…',
  'The wind was stronger than forecast…'),
 ('ph.lecciones', 'Si la deriva es más rápida que el ascenso, sal de ahí…',
  'Si la dérive est plus rapide que la montée, dégagez…',
  'Wenn die Abdrift schneller ist als das Steigen, raus dort…',
  'Se a deriva é mais rápida que a subida, sai de lá…',
  'If the drift is faster than the climb, move out…'),
 ('ph.recomendar', 'Pregunta en el sitio qué lado de la cresta está funcionando…',
  'Demandez sur place quel côté de la crête fonctionne…',
  'Frag vor Ort, welche Seite des Grats gerade geht…',
  'Pergunta no local que lado da crista está a funcionar…',
  'Ask locally which side of the ridge is working…'),
 ('box.eventMark', 'EVENTO', 'ÉVÉNEMENT', 'EREIGNIS', 'EVENTO', 'EVENT'),
]
n_c = 0
for claves in T:
    k = claves[0]
    for idioma, valor in [('EN',claves[5]),('ES',claves[1]),('FR',claves[2]),('DE',claves[3]),('PT',claves[4])]:
        i = s.find('const %s = {' % idioma); j = s.find('\n};', i)
        if ("'%s':" % k) in s[i:j]: continue
        comilla = '"' if "'" in valor else "'"
        s = s[:j] + "\n  '%s': %s%s%s," % (k, comilla, valor, comilla) + s[j:]
        n_c += 1
open(BASE + 'srs/i18n.js', 'w', encoding='utf-8').write(s)
print('  claves nuevas: %d' % n_c)
print('\n  cambios:', toc)
