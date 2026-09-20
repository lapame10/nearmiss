#!/usr/bin/env python3
"""Agrupa las zonas POR NOMBRE de sitio, no por cuadricula.

Con la cuadricula salia 'Valle de Bravo 5' y 'Valle de Bravo 1' como dos
lineas distintas, y es el mismo sitio. Ahora se suman.
"""

RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0

# 1) el ranking de la derecha
viejo = """    const zonas = {};
    incidentes.forEach(i => {
      if (i.lat == null) return;
      const k = i.lat.toFixed(1) + ',' + i.lon.toFixed(1);
      zonas[k] = (zonas[k] || 0) + 1;
    });
    const top = Object.entries(zonas).sort((a, b) => b[1] - a[1]).slice(0, 5);
    $('zonasTop').innerHTML = top.length ? top.map((z, k) => {
      const p = z[0].split(',');
      return '<div class="zf"><span>' + (k + 1) + '. '
        + escapa(nombreSitio(parseFloat(p[0]), parseFloat(p[1])))
        + '</span><b>' + z[1] + '</b></div>';
    }).join('')"""
nuevo = """    const zonas = {};
    incidentes.forEach(i => {
      if (i.lat == null) return;
      const k = nombreSitio(i.lat, i.lon);   /* por NOMBRE, asi no se repite */
      zonas[k] = (zonas[k] || 0) + 1;
    });
    const top = Object.entries(zonas).sort((a, b) => b[1] - a[1]).slice(0, 5);
    $('zonasTop').innerHTML = top.length ? top.map((z, k) =>
      '<div class="zf"><span>' + (k + 1) + '. ' + escapa(z[0])
      + '</span><b>' + z[1] + '</b></div>').join('')"""
if viejo in s: s = s.replace(viejo, nuevo); toc += 1
else: print('  NO ENCUENTRO el ranking')

# 2) los patrones por zona: igual, por nombre
viejo2 = """  const porZona = {};
  incidentes.forEach(i => {
    if (i.lat == null) return;
    const clave = i.lat.toFixed(1) + ', ' + i.lon.toFixed(1);
    porZona[clave] = porZona[clave] || { n:0, tipos:{} };
    porZona[clave].n++;
    porZona[clave].tipos[i.tipo] = (porZona[clave].tipos[i.tipo] || 0) + 1;
  });"""
nuevo2 = """  const porZona = {};
  incidentes.forEach(i => {
    if (i.lat == null) return;
    const clave = nombreSitio(i.lat, i.lon);   /* por nombre, no por cuadricula */
    porZona[clave] = porZona[clave] || { n:0, tipos:{} };
    porZona[clave].n++;
    porZona[clave].tipos[i.tipo] = (porZona[clave].tipos[i.tipo] || 0) + 1;
  });"""
if viejo2 in s: s = s.replace(viejo2, nuevo2); toc += 1
else: print('  NO ENCUENTRO los patrones por zona')

# 3) el bloque de patrones: ya no hay que convertir coordenadas
viejo3 = """  if (zonas.length) html += bloque('Dónde', 'place',
    'por zona, sin señalar puntos exactos',
    zonas.map(z => {
      const p = z[0].split(',');
      return [escapa(nombreSitio(parseFloat(p[0]), parseFloat(p[1]))), z[1].n];
    }));"""
nuevo3 = """  if (zonas.length) html += bloque('Dónde', 'place',
    'por sitio, sin señalar puntos exactos', zonas.map(z => [escapa(z[0]), z[1].n]));"""
if viejo3 in s: s = s.replace(viejo3, nuevo3); toc += 1
else: print('  NO ENCUENTRO el bloque de zonas')

# 4) y el "patron mas claro"
viejo4 = """      + '<div style="font-size:14.5px;line-height:1.7">En <b>'
      + escapa(nombreSitio(parseFloat(zTop[0].split(',')[0]), parseFloat(zTop[0].split(',')[1])))
      + '</b> hay <b>' + zTop[1].n + ' reportes</b>, y de ellos <b>' + tTop[1]"""
nuevo4 = """      + '<div style="font-size:14.5px;line-height:1.7">En <b>' + escapa(zTop[0])
      + '</b> hay <b>' + zTop[1].n + ' reportes</b>, y de ellos <b>' + tTop[1]"""
if viejo4 in s: s = s.replace(viejo4, nuevo4); toc += 1
else: print('  NO ENCUENTRO el patron mas claro')

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc, '/ 4')
print('  archivo:', len(s), 'bytes')
