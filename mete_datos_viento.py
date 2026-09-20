#!/usr/bin/env python3
"""Muestra los DATOS del viento, no etiquetas.

Pam: 'me gusta mas que diga los datos del viento, no si era moderado, para
cuando alguien vea lo que paso'.

Tiene razon: 'moderado' cada uno lo entiende a su manera. '14 km/h con rachas
de 35 del Oeste' no se discute. Y sirve para que quien lo lea despues sepa
exactamente que habia ese dia.
"""

RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0

# ---------- 1) las funciones que traducen los numeros a algo legible ----------
viejo = """/* ---------- PINTAR LOS INCIDENTES ---------- */"""
nuevo = """/* ==========================================================================
   EL VIENTO, EN DATOS (idea de Pam)
   Nada de "estaba moderado": eso cada uno lo entiende a su manera.
   Mejor los numeros: 14 km/h con rachas de 35 del Oeste. Eso no se discute
   y sirve para que quien lo lea sepa exactamente que habia ese dia.
   ========================================================================== */
const CARDINALES = ['Norte','Noreste','Este','Sureste','Sur','Suroeste','Oeste','Noroeste'];

/* la direccion del viento: de donde VIENE (como se dice en meteorologia) */
function deDonde(grados){
  if (grados == null) return '';
  const i = Math.round(((grados % 360) + 360) % 360 / 45) % 8;
  return 'del ' + CARDINALES[i];
}

/* cuanto soplaba, en numeros. Y aviso cuando las rachas son muy superiores */
function textoViento(v){
  if (!v || v.kmh == null) return '';
  let t = v.kmh + ' km/h';
  if (v.racha != null && v.racha > v.kmh + 8)
    t += ' · rachas ' + v.racha + ' km/h';
  if (v.dir != null) t += ' · ' + deDonde(v.dir) + ' (' + v.dir + '°)';
  return t;
}

/* si las rachas pasan mucho del viento medio, es que estaba racheado */
function eraRacheado(v){
  return !!(v && v.kmh != null && v.racha != null && v.racha > v.kmh + 12);
}

/* ---------- PINTAR LOS INCIDENTES ---------- */"""

if viejo in s: s = s.replace(viejo, nuevo, 1); toc += 1
else: print('  NO ENCUENTRO donde meter las funciones')

# ---------- 2) en la lista: el viento en su propia linea, en datos ----------
viejo2 = """        ${(i.viento && i.viento.kmh != null) ? '· viento ' + i.viento.kmh + ' km/h' + (i.viento.racha && i.viento.racha > i.viento.kmh + 12 ? ' (rachas ' + i.viento.racha + ')' : '') : ''}
      </div>"""
nuevo2 = """      </div>
      ${textoViento(i.viento) ? '<div class="datoViento">💨 <b>' + textoViento(i.viento) + '</b>'
        + (eraRacheado(i.viento) ? ' <span class="marcoRacha">racheado</span>' : '') + '</div>' : ''}
      ${i.igcMin ? '<div class="datoVuelo">🛫 Vuelo de <b>' + i.igcMin + ' min</b>'
        + (i.igcAltMax ? ' · techo <b>' + i.igcAltMax + ' m</b>' : '') + '</div>' : ''}"""

if viejo2 in s: s = s.replace(viejo2, nuevo2); toc += 1
else: print('  NO ENCUENTRO la linea del viento en la lista')

# ---------- 3) en el popup del mapa ----------
viejo3 = """        ((FASES.find(f => f.id === i.fase) || {}).n || '') +
        (i.relato ? '<br><span style="font-size:12px">' + escapa(i.relato).slice(0, 180) + '</span>' : ''))"""
nuevo3 = """        ((FASES.find(f => f.id === i.fase) || {}).n || '') +
        (textoViento(i.viento) ? '<br><b>💨 ' + textoViento(i.viento) + '</b>' : '') +
        (i.igcMin ? '<br>🛫 ' + i.igcMin + ' min de vuelo' + (i.igcAltMax ? ', techo ' + i.igcAltMax + ' m' : '') : '') +
        (i.relato ? '<br><span style="font-size:12px">' + escapa(i.relato).slice(0, 180) + '</span>' : ''))"""

if viejo3 in s: s = s.replace(viejo3, nuevo3); toc += 1
else: print('  NO ENCUENTRO el popup del mapa')

# ---------- 4) en los patrones: un bloque con los datos del viento ----------
viejo4 = """  if (zonas.length) html += bloque('Dónde (por zona de ~2 km)',
    'sin señalar puntos exactos', zonas.map(z => [z[0], z[1].n]));"""
nuevo4 = """  if (zonas.length) html += bloque('Dónde (por zona de ~2 km)',
    'sin señalar puntos exactos', zonas.map(z => [z[0], z[1].n]));

  /* el viento: aqui estan los numeros, que es lo que pidio Pam */
  const conViento = incidentes.filter(i => i.viento && i.viento.kmh != null);
  if (conViento.length >= 3){
    const med = Math.round(conViento.reduce((a, i) => a + i.viento.kmh, 0) / conViento.length);
    const rach = conViento.filter(i => i.viento.racha != null);
    const medRach = rach.length ? Math.round(rach.reduce((a, i) => a + i.viento.racha, 0) / rach.length) : null;
    const nRach = conViento.filter(i => eraRacheado(i.viento)).length;
    const fuertes = conViento.filter(i => i.viento.kmh >= 25).length;

    /* reparto por direccion */
    const dirs = {};
    conViento.forEach(i => {
      if (i.viento.dir == null) return;
      const d = deDonde(i.viento.dir).replace('del ', '');
      dirs[d] = (dirs[d] || 0) + 1;
    });
    const listaDirs = Object.entries(dirs).sort((a, b) => b[1] - a[1]);

    let t = '<div class="patron"><h3>💨 El viento de esos días (datos reales)</h3>'
      + '<div class="cuantos">' + conViento.length + ' de ' + total
      + ' reportes traen el viento del clima de ese día</div>'
      + '<div style="font-size:13.5px;line-height:1.75">'
      + 'Viento medio: <b>' + med + ' km/h</b>'
      + (medRach != null ? ' · rachas medias: <b>' + medRach + ' km/h</b>' : '')
      + '<br>' + nRach + ' de ' + conViento.length + ' tenían <b>rachas muy por encima del viento medio</b>'
      + (nRach > conViento.length / 2 ? ' — o sea, la mayoría fueron con aire <b>racheado</b>' : '')
      + '<br>' + fuertes + ' fueron con viento sostenido de <b>25 km/h o más</b>'
      + '</div>';

    if (listaDirs.length){
      const maxD = listaDirs[0][1];
      t += '<div style="margin-top:12px">'
        + listaDirs.map(d => '<div class="barra"><span class="nom">del ' + d[0] + '</span>'
          + '<span class="pista"><i style="width:' + (d[1] / maxD * 100).toFixed(0) + '%"></i></span>'
          + '<span class="n">' + d[1] + '</span></div>').join('')
        + '</div>';
    }
    t += '</div>';
    html += t;
  }"""

if viejo4 in s: s = s.replace(viejo4, nuevo4); toc += 1
else: print('  NO ENCUENTRO el bloque de zonas')

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc, '/ 4')
print('  archivo:', len(s), 'bytes')
