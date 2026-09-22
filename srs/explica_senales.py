#!/usr/bin/env python3
"""Las explicaciones de las senales, al diccionario.

Estaban escritas en ingles dentro de signals.js, asi que los titulos salian
traducidos pero la explicacion de debajo seguia en ingles. Se veia raro.

Cada explicacion es un bloque de varias lineas que empieza en `explicacion:`
y acaba en `,`. Los sustituyo enteros, uno a uno, por su llamada a t().
"""
s = open('/Users/lapame10/.hermes/workspace/nearmiss/srs/signals.js', encoding='utf-8').read()

CAMBIOS = [
 ("""      explicacion: `${grupo.length} ${nombreEv(ev).toLowerCase()} reports within ` +
        `${radio(grupo)} km of each other, between ` +
        `${fechas[0]} and ${fechas[fechas.length - 1]}. ` +
        `${graves} involved injury or a reserve deployment.`,""",
  """      explicacion: t('signals.exp1', { n: grupo.length, e: nombreEv(ev).toLowerCase(),
        km: radio(grupo), a: fechas[0], b: fechas[fechas.length - 1], g: graves }),"""),

 ("""      explicacion: `${grupo.length} ${nombreEv(ev).toLowerCase()} reports at this site ` +
        `were logged with ${dir} wind.`,""",
  """      explicacion: t('signals.exp2', { n: grupo.length, e: nombreEv(ev).toLowerCase(),
        d: dir, o: otrasDirs }),"""),

 ("""      explicacion: `${grupo.length} reports have been logged in the ${z.n} zone. ` +
        `The same zone keeps appearing across different days.`,""",
  """      explicacion: t('signals.exp3', { n: grupo.length, z: z.n }),"""),

 ("""      explicacion: `${pct}% of the reports at this site were logged between ` +
        `${tramo.replace('-', ':00-')}:00. ` +
        `That pattern can simply mean that is when most people fly.`,""",
  """      explicacion: t('signals.exp4', { p: pct, a: tramo.split('-')[0] + ':00', b: tramo.split('-')[1] + ':00' }),"""),

 ("""      explicacion: `${grupo.length} reserve deployments have been reported at this site ` +
        `in the last ${dias} days.`,""",
  """      explicacion: t('signals.exp5', { n: grupo.length, d: dias }),"""),
]

toc = 0
for v, n in CAMBIOS:
    if v in s:
        s = s.replace(v, n, 1); toc += 1
    else:
        # pruebo con variantes de espaciado
        import re
        cab = v.strip().split('\n')[0].strip()
        m = re.search(re.escape(cab) + r'[\s\S]{0,400}?\n(\s*)(?=\S)', s)
        print('  ✗ no coincidio: %s' % cab[:64])

# la ultima: no coincide por el guion
if "`${tramo.replace('-', ':00-')}:00. `" in s:
    import re
    m = re.search(r"explicacion: `\$\{pct\}%[\s\S]{0,320}?most people fly\.`,", s)
    if m:
        s = s[:m.start()] + "explicacion: t('signals.exp4', { p: pct, a: tramo.split('-')[0] + ':00', b: tramo.split('-')[1] + ':00' })," + s[m.end():]
        toc += 1
        print('  ok: la de R4 (por regex)')

open('/Users/lapame10/.hermes/workspace/nearmiss/srs/signals.js','w',encoding='utf-8').write(s)
print('  cambios:', toc)
