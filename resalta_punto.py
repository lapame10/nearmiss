#!/usr/bin/env python3
"""El punto que tocas tiene que RESALTAR entre muchos (idea de Pam).

Pam: 'si hay muchos no hay algo que lo haga resaltar para saber que ese es el
que pique'.

Con 10 puntos se ve cual es. Con 200, no. Asi que ahora:
- El punto elegido se agranda y se le pone un pin oscuro ENCIMA
- Y los DEMAS puntos se atenuan, para que salte a la vista
"""

RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0

# ---------- 1) la variable de cual esta señalado ----------
viejo = """let marcasInc = {};      /* id del reporte -> su marca en el mapa */"""
nuevo = """let marcasInc = {};      /* id del reporte -> su marca en el mapa */
let idSenalado = null;   /* el reporte que has tocado: ese se resalta */"""
if viejo in s: s = s.replace(viejo, nuevo); toc += 1
else: print('  NO ENCUENTRO las variables')

# ---------- 2) marcarlo al tocar ----------
viejo2 = """  ponPestana('tMapa');
  pintaIncidentes();          /* por si acaso, me aseguro de que las marcas existen */"""
nuevo2 = """  idSenalado = id;            /* <- esto hace que SU punto se resalte */
  ponPestana('tMapa');
  pintaIncidentes();          /* repinto para que se vea el resalte */"""
if viejo2 in s: s = s.replace(viejo2, nuevo2); toc += 1
else: print('  NO ENCUENTRO el irAlPunto')

# ---------- 3) el punto elegido: mas grande, con pin encima, y los demas atenuados ----------
viejo3 = """      marcasInc[i.id] = L.circleMarker([i.lat, i.lon],
        { radius:8, color:'#fff', weight:2.5, fillColor:col, fillOpacity:.92 })"""
nuevo3 = """      /* el elegido se agranda y se pone oscuro; los demas se atenuan */
      const elegido = (i.id === idSenalado);
      marcasInc[i.id] = L.circleMarker([i.lat, i.lon],
        { radius: elegido ? 14 : 8,
          color:'#fff',
          weight: elegido ? 5 : 2.5,
          fillColor: elegido ? '#16323b' : col,
          fillOpacity: elegido ? 1 : (idSenalado ? 0.38 : 0.92) })"""
if viejo3 in s: s = s.replace(viejo3, nuevo3); toc += 1
else: print('  NO ENCUENTRO el circleMarker')

# ---------- 4) el pin que no se puede confundir ----------
viejo4 = """        .addTo(capaPuntos);
    });"""
nuevo4 = """        .addTo(capaPuntos);
      /* y encima un pin grande: con muchos puntos, esto no se puede confundir */
      if (elegido){
        L.marker([i.lat, i.lon], {
          icon: L.divIcon({ className:'',
            html:'<div class="pinAqui"><span class="mso">my_location</span></div>',
            iconSize:[38,38], iconAnchor:[19,19] }),
          zIndexOffset: 3000, interactive:false
        }).addTo(capaPuntos);
      }
    });"""
if viejo4 in s: s = s.replace(viejo4, nuevo4); toc += 1
else: print('  NO ENCUENTRO el addTo(capaPuntos)')

# ---------- 5) quitar el resalte al cambiar de filtro ----------
viejo5 = """  $('filtros').onclick = ev => {
  const b = ev.target.closest('button');
  if (!b) return;
  $('filtros').querySelectorAll('button').forEach(x => x.classList.remove('on'));
  b.classList.add('on');
  filtro = b.dataset.f;
  pintaIncidentes();
};"""
nuevo5 = """  $('filtros').onclick = ev => {
  const b = ev.target.closest('button');
  if (!b) return;
  $('filtros').querySelectorAll('button').forEach(x => x.classList.remove('on'));
  b.classList.add('on');
  filtro = b.dataset.f;
  idSenalado = null;          /* al cambiar de filtro, quito el resalte */
  pintaIncidentes();
};"""
if viejo5 in s: s = s.replace(viejo5, nuevo5); toc += 1
else: print('  NO ENCUENTRO los filtros')

# ---------- 6) el CSS del pin y del pulso ----------
viejo6 = """  .marcaRacha{background:var(--casiBg);color:#8a5a10;font-size:10px;font-weight:800;
    padding:2px 7px;border-radius:20px;margin-left:5px}"""
nuevo6 = """  .marcaRacha{background:var(--casiBg);color:#8a5a10;font-size:10px;font-weight:800;
    padding:2px 7px;border-radius:20px;margin-left:5px}

  /* ===== EL PUNTO QUE HAS TOCADO =====
     Con muchos puntos en el mapa no sabes cual es el tuyo. Este pin oscuro con
     el aro que late no se puede confundir. */
  .pinAqui{width:38px;height:38px;border-radius:50%;background:#16323b;
    display:flex;align-items:center;justify-content:center;color:#fff;
    box-shadow:0 0 0 5px rgba(22,50,59,.22),0 3px 12px rgba(0,0,0,.35);
    animation:latePin 1.5s ease-in-out infinite;pointer-events:none}
  .pinAqui .mso{font-size:21px}
  @keyframes latePin{
    0%,100%{transform:scale(1);box-shadow:0 0 0 5px rgba(22,50,59,.22),0 3px 12px rgba(0,0,0,.35)}
    50%{transform:scale(1.1);box-shadow:0 0 0 12px rgba(22,50,59,.07),0 3px 12px rgba(0,0,0,.35)}
  }"""
if viejo6 in s: s = s.replace(viejo6, nuevo6); toc += 1
else: print('  NO ENCUENTRO el CSS de marcaRacha')

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc, '/ 6')
print('  archivo:', len(s), 'bytes')
