#!/usr/bin/env python3
"""Los dos que fallaron en el intento anterior, bien hechos.

fechaLarga: no coincidio porque el array tenia 'M[m - 1]' con espacios y yo
escribi 'M[m-1]'. Cuidado con eso.

La tabbar: el texto de cada enlace va DESPUES del </svg>, y mi busqueda
'>Home</a>' no lo encontraba porque entre el texto y el </a> hay un salto de
linea y espacios. Aqui voy con expresion regular sobre el contenido del <a>,
que es lo robusto.
"""
import re

BASE = '/Users/lapame10/.hermes/workspace/nearmiss/'
toc = 0

# ============================================================
# fechaLarga, con Intl
# ============================================================
s = open(BASE + 'srs/app.js', encoding='utf-8').read()
m = re.search(r'export function fechaLarga\(iso\)\s*\{[\s\S]*?\n\}', s)
nuevo = """/* ============================================================
   FECHAS LARGAS, EN EL IDIOMA QUE TOQUE
   ============================================================
   Antes los meses estaban en un array en ingles, asi que la fecha salia
   '22 Sep 2026' en cualquier idioma: en espanol, en frances o en aleman.

   Se les escapo a mis comprobadores porque no es texto dentro de una
   plantilla, es un array de datos: el comprobador mira el HTML de las vistas
   y ahi solo ve la llamada a fechaLarga(), no lo que devuelve.

   Ahora usa Intl, que ademas acierta con el orden de cada pais (en aleman es
   '22. Sept. 2026', en ingles '22 Sep 2026'). */
export function fechaLarga(iso) {
  if (!iso) return '—';
  try {
    const [a, mes, d] = iso.split('-').map(Number);
    return new Intl.DateTimeFormat(idioma() + '-u-nu-latn', {
      day: 'numeric', month: 'short', year: 'numeric',
    }).format(new Date(a, mes - 1, d));
  } catch (e) {
    /* si el navegador no puede, al menos que no salga vacio */
    return iso;
  }
}"""
if m:
    s = s[:m.start()] + nuevo + s[m.end():]
    open(BASE + 'srs/app.js', 'w', encoding='utf-8').write(s)
    toc += 1
    print('  fechaLarga(): ahora con Intl')
else:
    print('  ⚠ no encontre fechaLarga')

# ============================================================
# La tabbar: el texto de cada enlace, a un span con data-i18n
# ============================================================
h = open(BASE + 'index.html', encoding='utf-8').read()
CLAVES = {'inicio': 'nav.home', 'mapa': 'nav.map', 'reportar': 'nav.report',
          'senales': 'nav.signals', 'sitios': 'nav.sites'}

def arregla(m):
    global toc
    entero = m.group(0)
    destino = m.group(1)
    cuerpo = m.group(2)
    if 'data-i18n' in cuerpo:
        return entero                     # ya lo tiene
    # el texto suelto es lo ultimo, despues del </svg>
    mm = re.search(r'(</svg>)\s*([A-Za-z][A-Za-z\s]*?)\s*$', cuerpo, re.S)
    if not mm:
        return entero
    nuevo_cuerpo = cuerpo[:mm.start(2)] + '<span data-i18n="%s">%s</span>' % (
        CLAVES.get(destino, 'nav.home'), mm.group(2).strip())
    return entero.replace(cuerpo, nuevo_cuerpo)

h2 = re.sub(r'<a [^>]*data-ir="(\w+)"[^>]*>(.*?)</a>', arregla, h, flags=re.S)
if h2 != h:
    open(BASE + 'index.html', 'w', encoding='utf-8').write(h2)
    print('  tabbar: los cinco enlaces con data-i18n')
else:
    print('  ⚠ la tabbar no cambio')
