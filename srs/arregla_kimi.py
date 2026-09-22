#!/usr/bin/env python3
"""Los seis que encontro Kimi, arreglados.

Su diagnostico de fondo era el correcto: mi comprobador numero 4 solo mira
texto plano dentro del template. Todo lo que se construye con variables
—st.masEvento.n, las fechas, frases armadas en el codigo— se le escapa.

1. La tabbar: solo Report llevaba data-i18n. Los otros cuatro no, porque mi
   reemplazo buscaba '>Home</a>' y en la tabbar el enlace tiene atributos
   distintos. Verificado: inicio/mapa/senales/sitios lo tenian a NO.

2. fechaLarga() tenia los meses en ingles en un array. La fecha salia
   '22 Sep 2026' en cualquier idioma. Ahora usa Intl, que ademas pone el orden
   correcto de cada pais (en aleman es '22. Sep 2026').

3. En la ficha de sitio se usaban st.masEvento.n y st.masFase.n, que son los
   nombres crudos de data.js en ingles. En SiteCard ya se hacia bien con
   nombreEv(st.masEvento.id). Copiado ese patron.

4. ReportCard tenia 'Reserve' e 'IGC' escritos, y el resumen del home '· 30 d'.

5. El toast de sincronizacion decia 'Enviados N.' en español fijo, aunque la
   app estuviera en ingles.

6. Los enlaces de la cabecera llevaban data-i18n dos veces: en el <a> y en el
   <span> de dentro. Funcionaba, pero traducia lo mismo dos veces. Quitado el
   del <a>, que se queda el del <span>.
"""
import re

BASE = '/Users/lapame10/.hermes/workspace/nearmiss/'
toc = 0

# ============================================================
# 1 y 6 — EL HTML: la tabbar y el duplicado de la cabecera
# ============================================================
h = open(BASE + 'index.html', encoding='utf-8').read()

# 1) la tabbar: los cuatro que faltaban
for en, clave in [('>Home</a>', 'nav.home'), ('>Map</a>', 'nav.map'),
                  ('>Signals</a>', 'nav.signals'), ('>Sites</a>', 'nav.sites')]:
    if en in h:
        # puede estar partido por saltos de linea; pruebo tambien sin salto
        texto = en[1:-4]
        for forma in [en, '>' + texto + '\n  </a>', '>' + texto + '</a>']:
            if forma in h:
                nuevo = forma.replace('>' + texto, '><span data-i18n="%s">%s</span>' % (clave, texto))
                h = h.replace(forma, nuevo, 1)
                print('  tabbar: %s → data-i18n' % texto)
                toc += 1
                break
        else:
            print('  ⚠ tabbar: no encontre el enlace de %s' % texto)

# 6) el duplicado: quito el data-i18n de los <a> de la cabecera (el span lo tiene)
h = re.sub(r'<a([^>]*?) data-i18n="(nav\.\w+)"([^>]*?)>(<span data-i18n=)',
           r'<a\1\3>\4', h)
h = re.sub(r'(<a[^>]*?) data-i18n="nav\.(\w+)"([^>]*?)>([A-Za-z]+)</a>',
           r'\1\3><span data-i18n="nav.\2">\4</span></a>', h)
open(BASE + 'index.html', 'w', encoding='utf-8').write(h)

# ============================================================
# 2 — fechaLarga(): con Intl, que sabe los meses de cada idioma
# ============================================================
s = open(BASE + 'srs/app.js', encoding='utf-8').read()

viejo = """export function fechaLarga(iso) {
  if (!iso) return '—';
  const [a, m, d] = iso.split('-').map(Number);
  const M = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  return `${d} ${M[m-1]} ${a}`;
}"""
nuevo = """/* ============================================================
   FECHAS LARGAS, EN EL IDIOMA QUE TOQUE
   ============================================================
   Antes esto tenia los meses en un array en ingles, asi que la
   fecha salia '22 Sep 2026' en cualquier idioma: en español, en
   frances o en aleman. Se le escapo a mis comprobadores porque no
   es texto dentro de un template, es un array de datos.

   Ahora usa Intl, que ademas acierta con el orden de cada pais
   (en aleman es '22. Sept. 2026', en ingles '22 Sep 2026'). */
export function fechaLarga(iso) {
  if (!iso) return '—';
  try {
    const [a, m, d] = iso.split('-').map(Number);
    return new Intl.DateTimeFormat(idioma() + '-u-nu-latn', {
      day: 'numeric', month: 'short', year: 'numeric',
    }).format(new Date(a, m - 1, d));
  } catch (e) {
    /* si el navegador no puede, al menos que no salga vacio */
    return iso;
  }
}"""
if viejo in s:
    s = s.replace(viejo, nuevo, 1); toc += 1
    print('  fechaLarga(): ahora con Intl')
else:
    print('  ⚠ no encontre fechaLarga')

# ============================================================
# 3 — la ficha de sitio: los nombres por nombreEv/nombreFase
# ============================================================
v3a = """<dt>${escapa(t('site.mostEvent'))}</dt><dd>${st.masEvento ? escapa(st.masEvento.n) + ` (${st.masEvento.c})` : '—'}</dd>"""
n3a = """<dt>${escapa(t('site.mostEvent'))}</dt><dd>${st.masEvento ? escapa(nombreEv(st.masEvento.id)) + ` (${st.masEvento.c})` : '—'}</dd>"""
v3b = """<dt>${escapa(t('site.mostPhase'))}</dt><dd>${st.masFase ? escapa(st.masFase.n) + ` (${st.masFase.c})` : '—'}</dd>"""
n3b = """<dt>${escapa(t('site.mostPhase'))}</dt><dd>${st.masFase ? escapa(nombreFase(st.masFase.id)) + ` (${st.masFase.c})` : '—'}</dd>"""
for v, n, q in [(v3a, n3a, 'masEvento'), (v3b, n3b, 'masFase')]:
    if v in s:
        s = s.replace(v, n, 1); toc += 1
        print('  ficha de sitio: %s por nombreEv/nombreFase' % q)
    else:
        print('  ⚠ no encontre %s' % q)

# ============================================================
# 4 — ReportCard y el resumen del home
# ============================================================
v4a = """      ${rep.reserve ? '<span class="etq sev">Reserve</span>' : ''}
      ${rep.igc ? '<span class="etq ok">IGC</span>' : ''}"""
n4a = """      ${rep.reserve ? `<span class="etq sev">${escapa(t('common.reserve'))}</span>` : ''}
      ${rep.igc ? `<span class="etq ok">${escapa(t('snapshot.igc'))}</span>` : ''}"""
if v4a in s:
    s = s.replace(v4a, n4a, 1); toc += 1
    print('  ReportCard: Reserve e IGC por t()')
else:
    print('  ⚠ no encontre el ReportCard')

v4b = """<div class="met"><b>${ult30}</b><span>${escapa(t('common.reports'))} · 30 d</span></div>"""
n4b = """<div class="met"><b>${ult30}</b><span>${escapa(t('common.reports'))} · ${escapa(t('home.days30'))}</span></div>"""
if v4b in s:
    s = s.replace(v4b, n4b, 1); toc += 1
    print('  resumen del home: el "30 d"')
else:
    print('  ⚠ no encontre el "30 d"')

# ============================================================
# 5 — el toast de sincronizacion
# ============================================================
v5 = """    aviso(r.enviados ? `Enviados ${r.enviados}.` : t('status.offlineSaved'));"""
n5 = """    aviso(r.enviados ? t('status.sent', { n: r.enviados }) : t('status.offlineSaved'));"""
if v5 in s:
    s = s.replace(v5, n5, 1); toc += 1
    print('  el toast de sincronizacion')
else:
    print('  ⚠ no encontre el toast')

open(BASE + 'srs/app.js', 'w', encoding='utf-8').write(s)
print('\n  cambios totales:', toc)
