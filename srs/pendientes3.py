#!/usr/bin/env python3
"""Punto 6: los filtros del mapa cuando estas en modo Senales.

EL PROBLEMA

El panel de filtros ofrece nueve cosas: sitio, pais, tipo de evento, fase,
resultado, viento, clase de ala, desde, hasta. Cuando estas en modo Reportes,
todas se aplican de verdad.

Pero en modo Senales, `pintaSenales()` solo miraba UNA:

    const sigs = est.filtros.site ? est.senales.filter(s => s.site === ...) : est.senales;

O sea: podias poner 'viento NW' y 'solo con lesion', y las senales no
cambiaban. La interfaz daba a entender que estaba filtrando cuando no filtraba
nada. Eso es peor que no tener el filtro: la persona cree que ha acotado y no
ha acotado.

LA SOLUCION (estrategia A, la que pidio Pam)

Una senal aparece solo si alguno de SUS reportes relacionados pasa los filtros.
Asi el filtro hace lo que dice: si pides viento NW, solo ves senales que tengan
al menos un reporte con viento NW.

Y como una senal puede tener diez reportes y que solo dos pasen el filtro, el
popup dice cuantos pasan: '2 de 10 reportes'. Asi no se queda uno pensando que
los diez cumplen lo que ha pedido.
"""
BASE = '/Users/lapame10/.hermes/workspace/nearmiss/srs/'
toc = 0

s = open(BASE + 'mapa.js', encoding='utf-8').read()

viejo = """function pintaSenales(L, capa) {
  const sigs = (est.filtros.site ? est.senales.filter(s => s.site === est.filtros.site) : est.senales);
  sigs.forEach(s => {"""

nuevo = """/* ============================================================
   LAS SENALES QUE PASAN EL FILTRO
   ============================================================
   Una senal se construyo a partir de unos reportes (s.reps guarda sus id).
   Aqui se mira si ALGUNO de esos reportes pasa los filtros que hay puestos.

   Por que 'alguno' y no 'todos': porque lo util es encontrar senales donde
   haya al menos un caso de lo que buscas. Si pidieras que TODOS los reportes
   de la senal cumplieran el filtro, casi nunca saldria nada, y menos cuanto
   mas filtros pongas.

   Devuelve la senal junto con cuantos de sus reportes pasan, para poder
   decirlo en el popup. */
function senalesFiltradas() {
  const pasan = new Set(filtra(est.reps).map(r => r.id));
  const salida = [];
  est.senales.forEach(s => {
    const suyos = (s.reps || []).filter(id => pasan.has(id));
    if (!suyos.length) return;
    /* si no hay filtros puestos, se cuentan todos */
    const hayFiltro = numeroDeFiltros() > 0;
    salida.push({
      s,
      dentro: hayFiltro ? suyos.length : (s.reps || []).length,
      total: (s.reps || []).length,
      filtrada: hayFiltro && suyos.length < (s.reps || []).length,
    });
  });
  return salida;
}

function pintaSenales(L, capa) {
  const lista = senalesFiltradas();
  const sigs = lista.map(x => x.s);
  lista.forEach(({ s, dentro, total, filtrada }) => {"""

if viejo in s:
    s = s.replace(viejo, nuevo, 1); toc += 1
    print('  mapa.js: las senales pasan por los filtros')

# ---------- el popup: decir cuantos pasan ----------
v2 = """        <span style="color:#8c939b;font-size:12px">${escapa(t('signals.relatedShort', { n: s.n }))} ·
        ${escapa(fechaLarga(s.desde))} – ${escapa(fechaLarga(s.hasta))}</span><br>"""
n2 = """        <span style="color:#8c939b;font-size:12px">${escapa(
          filtrada ? t('signals.relatedFiltered', { n: dentro, t: total })
                   : t('signals.relatedShort', { n: total }))} ·
        ${escapa(fechaLarga(s.desde))} – ${escapa(fechaLarga(s.hasta))}</span><br>"""
if v2 in s:
    s = s.replace(v2, n2, 1); toc += 1
    print('  mapa.js: el popup dice cuantos pasan el filtro')

open(BASE + 'mapa.js', 'w', encoding='utf-8').write(s)

# ============================================================
# numeroDeFiltros() — para saber si hay alguno puesto
# ============================================================
s = open(BASE + 'mapa.js', encoding='utf-8').read()
if 'function numeroDeFiltros' not in s:
    # la añado justo antes de senalesFiltradas
    s = s.replace("""/* ============================================================
   LAS SENALES QUE PASAN EL FILTRO""",
"""/* Cuantos filtros hay puestos ahora mismo. Sirve para no decir '2 de 10' cuando
   en realidad no hay ningun filtro y simplemente la senal tiene 2 reportes. */
function numeroDeFiltros() {
  const f = est.filtros || {};
  return Object.keys(f).filter(k => f[k] !== '' && f[k] != null).length;
}

/* ============================================================
   LAS SENALES QUE PASAN EL FILTRO""", 1)
    open(BASE + 'mapa.js', 'w', encoding='utf-8').write(s)
    print('  mapa.js: numeroDeFiltros()')

# ============================================================
# la clave nueva
# ============================================================
s = open(BASE + 'i18n.js', encoding='utf-8').read()
VAL = [
 ('signals.relatedFiltered', '{n} de {t} reportes pasan el filtro',
  '{n} sur {t} signalements correspondent au filtre',
  '{n} von {t} Meldungen passen zum Filter',
  '{n} de {t} relatos correspondem ao filtro',
  '{n} of {t} reports match the filter'),
]
n_c = 0
for claves in VAL:
    k = claves[0]
    for idioma, valor in [('EN',claves[5]),('ES',claves[1]),('FR',claves[2]),('DE',claves[3]),('PT',claves[4])]:
        i = s.find('const %s = {' % idioma); j = s.find('\n};', i)
        if ("'%s':" % k) in s[i:j]: continue
        s = s[:j] + "\n  '%s': '%s'," % (k, valor.replace("'", "\\'")) + s[j:]
        n_c += 1
open(BASE + 'i18n.js', 'w', encoding='utf-8').write(s)
print('  claves nuevas: %d' % n_c)
print('\n  cambios:', toc)
