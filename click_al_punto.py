#!/usr/bin/env python3
"""Click en un reporte -> te lleva a su punto en el mapa (idea de Pam).

Igual que en Find Whale: tocas el reporte y el mapa va a ese sitio.
"""

RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0

# ---------- 1) guardar las marcas del mapa por id, y la funcion que va al punto ----------
viejo = """let incidentes = [];
let mapaPrincipal = null, mapaMarca = null, mapaCalorMini = null;"""
nuevo = """let incidentes = [];
let marcasInc = {};      /* id del reporte -> su marca en el mapa */
let mapaPrincipal = null, mapaMarca = null, mapaCalorMini = null;"""
if viejo in s: s = s.replace(viejo, nuevo); toc += 1
else: print('  NO ENCUENTRO las variables')

# ---------- 2) la funcion ----------
viejo2 = """/* ---------- la lista ---------- */"""
nuevo2 = """/* ==========================================================================
   TOCAR UN REPORTE Y QUE EL MAPA VAYA A SU PUNTO (idea de Pam)
   ========================================================================== */
function irAlPunto(id){
  const i = incidentes.find(x => x.id === id);
  if (!i) return;
  if (i.lat == null){
    aviso('Ese reporte no tiene punto',
      'Quien lo escribió no marcó dónde pasó. Es lo único que se pide y no se '
      + 'obligó, así que no hay sitio al que llevarte.');
    return;
  }
  ponPestana('tMapa');
  pintaIncidentes();          /* por si acaso, me aseguro de que las marcas existen */
  setTimeout(() => {
    if (!mapaPrincipal) return;
    mapaPrincipal.setView([i.lat, i.lon], 14, { animate:true });
    const m = marcasInc[id];
    if (m && m.openPopup) m.openPopup();
    /* subo al mapa, que es donde esta el punto */
    const mm = document.getElementById('mapa');
    if (mm) mm.scrollIntoView({ behavior:'smooth', block:'start' });
    /* y dejo la tarjeta marcada con un aro, para saber cual es */
    document.querySelectorAll('.inc').forEach(n => n.classList.remove('senala'));
    const nodo = document.querySelector('.inc[data-id="' + id + '"]');
    if (nodo) nodo.classList.add('senala');
  }, 220);
}

/* ---------- la lista ---------- */"""
if viejo2 in s: s = s.replace(viejo2, nuevo2, 1); toc += 1
else: print('  NO ENCUENTRO el sitio de la lista')

# ---------- 3) la tarjeta: clickable, con data-id y con el aviso de "ver en el mapa" ----------
viejo3 = """    return '<div class="inc ' + (i.gravedad || '') + '">'
      + '<div class="tipo"><span class="mso">' + t.e + '</span>' + titulo + '</div>'"""
nuevo3 = """    return '<div class="inc ' + (i.gravedad || '') + '" data-id="' + i.id
      + '" onclick="irAlPunto(\\'' + i.id + '\\')">'
      + '<div class="tipo"><span class="mso">' + t.e + '</span>' + titulo + '</div>'"""
if viejo3 in s: s = s.replace(viejo3, nuevo3); toc += 1
else: print('  NO ENCUENTRO la tarjeta')

# ---------- 4) el pie de la tarjeta con "ver en el mapa" ----------
viejo4 = """      + (i.relato ? '<div class="relato">' + escapa(i.relato) + '</div>' : '')
      + '</div>';"""
nuevo4 = """      + (i.relato ? '<div class="relato">' + escapa(i.relato) + '</div>' : '')
      + (i.lat != null
          ? '<div class="verPunto"><span class="mso">my_location</span>Ver en el mapa</div>'
          : '')
      + '</div>';"""
if viejo4 in s: s = s.replace(viejo4, nuevo4); toc += 1
else: print('  NO ENCUENTRO el relato')

# ---------- 5) guardar la marca al pintarla ----------
viejo5 = """      L.circleMarker([i.lat, i.lon], { radius:8, color:'#fff', weight:2.5,
        fillColor:col, fillOpacity:.92 })
        .bindPopup('<b>' + t.n + '</b><br>'"""
nuevo5 = """      marcasInc[i.id] = L.circleMarker([i.lat, i.lon],
        { radius:8, color:'#fff', weight:2.5, fillColor:col, fillOpacity:.92 })
        .bindPopup('<b>' + t.n + '</b><br>'"""
if viejo5 in s: s = s.replace(viejo5, nuevo5); toc += 1
else: print('  NO ENCUENTRO el circleMarker')

# ---------- 6) limpiar las marcas viejas al repintar ----------
viejo6 = """    capaPuntos.clearLayers();
    if (capaCalor){ mapaPrincipal.removeLayer(capaCalor); capaCalor = null; }"""
nuevo6 = """    capaPuntos.clearLayers();
    marcasInc = {};
    if (capaCalor){ mapaPrincipal.removeLayer(capaCalor); capaCalor = null; }"""
if viejo6 in s: s = s.replace(viejo6, nuevo6); toc += 1
else: print('  NO ENCUENTRO el clearLayers')

# ---------- 7) el CSS ----------
viejo7 = """  .inc{background:var(--papel);border-radius:12px;padding:16px;
    box-shadow:0 1px 3px rgba(22,50,59,.08);border-left:4px solid var(--casi)}"""
nuevo7 = """  .inc{background:var(--papel);border-radius:12px;padding:16px;
    box-shadow:0 1px 3px rgba(22,50,59,.08);border-left:4px solid var(--casi);
    cursor:pointer;transition:box-shadow .15s}
  .inc:hover{box-shadow:0 3px 14px rgba(22,50,59,.17)}
  .inc.senala{box-shadow:0 0 0 3px var(--mar)}
  /* el aviso de que se puede tocar */
  .inc .verPunto{display:flex;align-items:center;gap:6px;margin-top:11px;
    font-size:12px;font-weight:800;color:var(--mar);letter-spacing:-.1px}
  .inc .verPunto .mso{font-size:17px}"""
if viejo7 in s: s = s.replace(viejo7, nuevo7); toc += 1
else: print('  NO ENCUENTRO el CSS de .inc')

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc, '/ 7')
print('  archivo:', len(s), 'bytes')
