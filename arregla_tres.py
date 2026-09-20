#!/usr/bin/env python3
"""Tres arreglos sobre el diseno de Pam.

1) El icono 'collision' NO existe en Material Symbols -> salia como texto
   literal "COLLISION" en el boton. Lo cambio por 'merge'.
2) La columna derecha se salia por el borde de la pantalla (el formulario
   imponia un ancho minimo grande). Se arregla con minmax(0,1fr) + min-width:0.
3) Las zonas salian como coordenadas (19.1,-100.1) en vez de con el NOMBRE del
   sitio, como en el diseno de Pam (Valle de Bravo, Castejon...). Anyado una
   lista de sitios de parapente conocidos y asigno el mas cercano.
"""

RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0

# ---------- 1) el icono que no existe ----------
viejo = "  { id:'colision', e:'collision',          n:'Colisión' },"
nuevo = "  { id:'colision', e:'merge',              n:'Colisión' },"
if viejo in s: s = s.replace(viejo, nuevo); toc += 1
print('  1) icono de colision:', 'OK' if toc else 'NO ENCONTRADO')

# ---------- 2) el desbordamiento de la columna derecha ----------
viejo2 = """  .cuerpo{display:grid;grid-template-columns:1fr;gap:18px;padding:18px 24px 40px;
    max-width:1500px;margin:0 auto}
  @media(min-width:1000px){
    .cuerpo{grid-template-columns:1fr 370px}"""
nuevo2 = """  /* OJO: minmax(0,1fr) y min-width:0 son necesarios. Sin eso, el formulario
     impone un ancho minimo grande y la columna derecha se sale de la pantalla. */
  .cuerpo{display:grid;grid-template-columns:minmax(0,1fr);gap:18px;
    padding:18px 24px 40px;max-width:1500px;margin:0 auto}
  .cuerpo>*{min-width:0}
  @media(min-width:1000px){
    .cuerpo{grid-template-columns:minmax(0,1fr) 360px}"""
if viejo2 in s: s = s.replace(viejo2, nuevo2); toc += 1
print('  2) el layout:', 'OK' if toc == 2 else 'NO ENCONTRADO')

# ---------- 3) los nombres de los sitios ----------
viejo3 = """/* ---------- el viento: datos, no etiquetas ---------- */"""
nuevo3 = """/* ==========================================================================
   LOS NOMBRES DE LOS SITIOS
   Las coordenadas no dicen nada. Mejor "Valle de Bravo" que "19.1, -100.1".
   Si el punto no esta cerca de ningun sitio conocido, se muestran los numeros.
   ========================================================================== */
const SITIOS = [
  /* Mexico */
  { n:'Valle de Bravo',   lat:19.107, lon:-100.126 },
  { n:'La Torre (Valle)', lat:19.093, lon:-100.150 },
  { n:'Sacacorchos',      lat:19.110, lon:-100.162 },
  { n:'Malinalco',        lat:18.949, lon: -99.496 },
  { n:'Tapalpa',          lat:19.945, lon:-103.766 },
  { n:'La Huasteca',      lat:25.636, lon:-100.440 },
  { n:'San Miguel de Allende', lat:20.914, lon:-100.744 },
  { n:'Taxco',            lat:18.556, lon: -99.605 },
  { n:'Huasca',           lat:20.203, lon: -98.570 },
  { n:'Mineral del Chico',lat:20.216, lon: -98.729 },
  { n:'Pico de Orizaba',  lat:18.853, lon: -97.107 },
  { n:'Chapala',          lat:20.296, lon:-103.191 },
  { n:'Tequesquitengo',   lat:18.617, lon: -99.260 },
  { n:'Amecameca',        lat:19.126, lon: -98.766 },
  { n:'Cuetzalan',        lat:20.018, lon: -97.523 },
  { n:'Real de Catorce',  lat:23.690, lon:-100.887 },
  /* los clasicos internacionales */
  { n:'Roldanillo (Colombia)', lat:4.415, lon:-76.153 },
  { n:'Castejón de Sos (España)', lat:42.512, lon:0.487 },
  { n:'Algodonales (España)',   lat:36.877, lon:-5.404 },
  { n:'Piedrahíta (España)',    lat:40.464, lon:-5.327 },
  { n:'Organyà (España)',       lat:42.211, lon:1.325 },
  { n:'Áger (España)',          lat:42.000, lon:0.760 },
];

/* el sitio conocido mas cercano, si esta a menos de 35 km */
function nombreSitio(lat, lon){
  let mejor = null, dMin = 1e9;
  const cos = Math.cos(lat * Math.PI / 180);
  SITIOS.forEach(s => {
    const dLat = (lat - s.lat) * 111;
    const dLon = (lon - s.lon) * 111 * cos;
    const d = Math.sqrt(dLat * dLat + dLon * dLon);
    if (d < dMin){ dMin = d; mejor = s.n; }
  });
  if (dMin <= 35) return mejor;
  return lat.toFixed(2) + ', ' + lon.toFixed(2);
}

/* ---------- el viento: datos, no etiquetas ---------- */"""
if viejo3 in s: s = s.replace(viejo3, nuevo3, 1); toc += 1
print('  3) la tabla de sitios:', 'OK' if toc == 3 else 'NO ENCONTRADO')

# ---------- 4) usar el nombre en el ranking de zonas ----------
viejo4 = """    $('zonasTop').innerHTML = top.length ? top.map((z, k) =>
      '<div class="zf"><span>' + (k + 1) + '. ' + z[0] + '</span><b>' + z[1] + '</b></div>').join('')"""
nuevo4 = """    $('zonasTop').innerHTML = top.length ? top.map((z, k) => {
      const p = z[0].split(',');
      return '<div class="zf"><span>' + (k + 1) + '. '
        + escapa(nombreSitio(parseFloat(p[0]), parseFloat(p[1])))
        + '</span><b>' + z[1] + '</b></div>';
    }).join('')"""
if viejo4 in s: s = s.replace(viejo4, nuevo4); toc += 1
print('  4) el ranking de zonas:', 'OK' if toc == 4 else 'NO ENCONTRADO')

# ---------- 5) y en la lista de incidentes ----------
viejo5 = """      + (i.lat != null ? i.lat.toFixed(2) + ', ' + i.lon.toFixed(2) + ' · ' : '')"""
nuevo5 = """      + (i.lat != null ? '<b>' + escapa(nombreSitio(i.lat, i.lon)) + '</b> · ' : '')"""
if viejo5 in s: s = s.replace(viejo5, nuevo5); toc += 1
print('  5) la lista de incidentes:', 'OK' if toc == 5 else 'NO ENCONTRADO')

# ---------- 6) y en el bloque de patrones por zona ----------
viejo6 = """  if (zonas.length) html += bloque('Dónde (por zona de ~2 km)', 'place',
    'sin señalar puntos exactos', zonas.map(z => [z[0], z[1].n]));"""
nuevo6 = """  if (zonas.length) html += bloque('Dónde', 'place',
    'por zona, sin señalar puntos exactos',
    zonas.map(z => {
      const p = z[0].split(',');
      return [escapa(nombreSitio(parseFloat(p[0]), parseFloat(p[1]))), z[1].n];
    }));"""
if viejo6 in s: s = s.replace(viejo6, nuevo6); toc += 1
print('  6) los patrones por zona:', 'OK' if toc == 6 else 'NO ENCONTRADO')

# ---------- 7) y en el "patron mas claro" ----------
viejo7 = """      + '<div style="font-size:14.5px;line-height:1.7">En la zona de <b>' + zTop[0]
      + '</b> hay <b>' + zTop[1].n + ' reportes</b>, y de ellos <b>' + tTop[1]"""
nuevo7 = """      + '<div style="font-size:14.5px;line-height:1.7">En <b>'
      + escapa(nombreSitio(parseFloat(zTop[0].split(',')[0]), parseFloat(zTop[0].split(',')[1])))
      + '</b> hay <b>' + zTop[1].n + ' reportes</b>, y de ellos <b>' + tTop[1]"""
if viejo7 in s: s = s.replace(viejo7, nuevo7); toc += 1
print('  7) el patron mas claro:', 'OK' if toc == 7 else 'NO ENCONTRADO')

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc, '/ 7')
print('  archivo:', len(s), 'bytes')
