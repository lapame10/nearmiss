#!/usr/bin/env python3
"""Arregla el choque de nombres y traduce el bloque del viento.

PROBLEMA: la funcion de traduccion se llama t(), y dentro de pintaIncidentes
habia una variable local 'const t = sevDe(...)'. Eso SOMBREA la funcion: cuando
el codigo de dentro llamaba a t('verEnMapa'), estaba llamando a un objeto en
vez de a la funcion -> TypeError.

Mismo caso con 'let t =' del bloque del viento.

Es el tipo de fallo que no canta al cargar, solo al pintar. Se arregla
renombrando las variables locales.
"""
RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0


def rep(v, n):
    global s, toc
    if v in s:
        s = s.replace(v, n); toc += 1
        return True
    print('  NO ENCUENTRO:', v[:72].replace('\n', ' | '))
    return False


# ---------- 1) en pintaIncidentes: t -> sv ----------
rep("""    const t = sevDe(i.sev);
    const sit = sitDe(i.sit);
    const titulo = (i.sit === 'otro' && i.otro) ? escapa(i.otro) : nb(sit);""",
    """    const sv = sevDe(i.sev);          /* NO llamarlo 't': t() es la traduccion */
    const sit = sitDe(i.sit);
    const titulo = (i.sit === 'otro' && i.otro) ? escapa(i.otro) : nb(sit);""")

rep("""      + '<span class="etq sevEtq">' + nb(t) + '</span>'""",
    """      + '<span class="etq sevEtq">' + nb(sv) + '</span>'""")

# ---------- 2) en el mapa: t -> sv ----------
rep("""      const t = sevDe(i.sev);
      const col = colorDe(i.sev);""",
    """      const sv = sevDe(i.sev);
      const col = colorDe(i.sev);""")

rep("""        .bindPopup('<b>' + nb(sitDe(i.sit)) + '</b> · ' + nb(t) + '<br>'""",
    """        .bindPopup('<b>' + nb(sitDe(i.sit)) + '</b> · ' + nb(sv) + '<br>'""")

# ---------- 3) el bloque del viento: 'let t' -> 'let blk', y traducido ----------
rep("""    let t = '<div class="patron"><h3><span class="mso">air</span>El viento de esos días</h3>'
      + '<div class="cuantos">' + conViento.length + ' de ' + total
      + ' eventos traen el viento real del clima de ese día</div>'
      + '<div style="font-size:13.5px;line-height:1.8">'
      + 'Viento medio: <b>' + med + ' km/h</b>'
      + (medRach != null ? ' · rachas medias: <b>' + medRach + ' km/h</b>' : '')
      + '<br>' + nRach + ' de ' + conViento.length
      + ' tenían <b>rachas muy por encima del viento medio</b>'
      + (nRach > conViento.length / 2 ? ' — la mayoría fueron con aire <b>racheado</b>' : '')
      + '<br>' + fuertes + ' fueron con viento sostenido de <b>25 km/h o más</b></div>';""",
    """    /* OJO: la variable NO puede llamarse 't', que es la funcion de traduccion */
    let blk = '<div class="patron"><h3><span class="mso">air</span>' + t('vientoTitulo') + '</h3>'
      + '<div class="cuantos">' + conViento.length + ' / ' + total + ' '
      + t('vientoSub') + '</div>'
      + '<div style="font-size:13.5px;line-height:1.8">'
      + t('vientoMedio') + ': <b>' + med + ' km/h</b>'
      + (medRach != null ? ' · ' + t('rachasMedias') + ': <b>' + medRach + ' km/h</b>' : '')
      + '<br>' + nRach + ' / ' + conViento.length + ' ' + t('tenianRachas')
      + (nRach > conViento.length / 2 ? t('mayoriaRachado') : '')
      + '<br>' + fuertes + ' ' + t('conSostenido') + '</div>';""")

rep("""      t += '<div style="margin-top:13px">'""", """      blk += '<div style="margin-top:13px">'""")
rep("""        + listaDirs.map(d => '<div class="fila"><span class="nom">del ' + d[0] + '</span>'
          + '<span class="pista"><i style="width:' + (d[1] / maxD * 100).toFixed(0) + '%"></i></span>'
          + '<span class="n">' + d[1] + '</span></div>').join('') + '</div>';
    }
    html += t + '</div>';""",
    """        + listaDirs.map(d => '<div class="fila"><span class="nom">'
          + (idioma === 'es' ? 'del ' : 'from ') + d[0] + '</span>'
          + '<span class="pista"><i style="width:' + (d[1] / maxD * 100).toFixed(0) + '%"></i></span>'
          + '<span class="n">' + d[1] + '</span></div>').join('') + '</div>';
    }
    html += blk + '</div>';""")

# ---------- 4) los cardinales del viento, en ingles ----------
rep("""const CARDINALES = ['Norte','Noreste','Este','Sureste','Sur','Suroeste','Oeste','Noroeste'];
/* la direccion del viento: de donde VIENE (como se dice en meteorologia) */
function deDonde(grados){
  if (grados == null) return '';
  const i = Math.round(((grados % 360) + 360) % 360 / 45) % 8;
  return 'del ' + CARDINALES[i];
}""",
    """const CARDINALES = {
  es: ['Norte','Noreste','Este','Sureste','Sur','Suroeste','Oeste','Noroeste'],
  en: ['North','North-east','East','South-east','South','South-west','West','North-west'],
};
/* la direccion del viento: de donde VIENE (como se dice en meteorologia) */
function deDonde(grados){
  if (grados == null) return '';
  const i = Math.round(((grados % 360) + 360) % 360 / 45) % 8;
  return (idioma === 'es' ? 'del ' : 'from ') + CARDINALES[idioma][i];
}""")

# y los sitios donde se usaba deDonde quitando 'del '
rep("""      const d = deDonde(i.viento.dir).replace('del ', '');""",
    """      const d = deDonde(i.viento.dir).replace(/^(del |from )/, '');""")

# ---------- 5) el nombre del mes, en ingles ----------
rep("""const MESES = ['enero','febrero','marzo','abril','mayo','junio',
               'julio','agosto','septiembre','octubre','noviembre','diciembre'];""",
    """const MESES = {
  es: ['enero','febrero','marzo','abril','mayo','junio',
       'julio','agosto','septiembre','octubre','noviembre','diciembre'],
  en: ['January','February','March','April','May','June',
       'July','August','September','October','November','December'],
};""")

rep("""function nombreMes(m){
  const p = String(m).split('-');
  return MESES[parseInt(p[1], 10) - 1] + ' ' + p[0];
}""",
    """function nombreMes(m){
  const p = String(m).split('-');
  const mm = MESES[idioma][parseInt(p[1], 10) - 1] || '';
  return idioma === 'es' ? (mm + ' ' + p[0]) : (mm + ' ' + p[0]);
}""")

# ---------- 6) el sitio: 'de' en los sitios ----------
rep("""function nombreSitio(lat, lon){""",
    """function nombreSitio(lat, lon){""")

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
