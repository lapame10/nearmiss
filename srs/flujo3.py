#!/usr/bin/env python3
"""El resumen de lo que se saco del IGC, y los enganches del paso nuevo.

Al cargar el archivo, se guarda F.igcResumen con lo que se puede ensenar:
fecha, hora, sitio aproximado, duracion, puntos y altitud maxima. Eso es lo
que se le muestra al piloto justo despues de subirlo, para que vea que ha
funcionado antes de seguir.

El sitio NO viene en el archivo: se deduce mirando a que sitio conocido esta
mas cerca el primer punto del track. Si no hay ninguno a menos de 30 km, se
deja vacio y lo pone el piloto a mano. Deducir no es inventar: si no hay
ninguno cerca, no se dice nada.
"""
BASE = '/Users/lapame10/.hermes/workspace/nearmiss/srs/'
toc = 0
s = open(BASE + 'report.js', encoding='utf-8').read()


def rep(v, n, q):
    global s, toc
    if v in s:
        s = s.replace(v, n, 1); toc += 1; print('  ok:', q)
    else:
        print('  ✗ NO COINCIDIO:', q)


# ============================================================
# 1 — el resumen, al terminar de parsear
# ============================================================
rep("""  track = { puntos: r.puntos, meta: r.meta, nombre: f.name };
  anomalias = posiblesAnomalias(r.puntos);""",
    """  track = { puntos: r.puntos, meta: r.meta, nombre: f.name };
  anomalias = posiblesAnomalias(r.puntos);

  /* ===== LO QUE SE SACO DEL ARCHIVO =====
     Se guarda ya montado, para poder ensenarlo justo despues de subirlo. El
     sitio no viene en un IGC: se deduce del punto de despegue, mirando cual de
     los sitios conocidos esta mas cerca. Si no hay ninguno a menos de 30 km se
     deja vacio y lo pone el piloto. */
  const p0 = r.puntos[0] || {};
  const cerca = SITES.map(x => ({ x, km: distKm(p0.lat, p0.lon, x.lat, x.lon) }))
    .filter(o => o.km < 30).sort((a, b) => a.km - b.km)[0];
  const dur = r.meta.duracionS || 0;
  F.igcResumen = {
    fecha: r.meta.desde || '',
    hora: (p0.hora || '').slice(0, 5),
    site: cerca ? cerca.x.n : '',
    siteId: cerca ? cerca.x.id : '',
    duracion: dur ? `${Math.floor(dur / 3600)} h ${Math.round((dur % 3600) / 60)} min` : '',
    puntos: r.meta.puntos,
    altMax: r.meta.altMax != null ? String(r.meta.altMax) + ' m' : '',
  };
  /* si el sitio se deduce bien, se rellena solo: no se le pregunta lo que ya sabemos */
  if (cerca && !F.site) { F.site = cerca.x.id; F.siteDeducido = true; }
  if (r.meta.desde) { F.fecha = r.meta.desde; F.fechaDeducida = true; }
  if (p0.hora) { F.hora = p0.hora.slice(0, 5); F.horaDeducida = true; }
  if (p0.lat != null) { F.lat = p0.lat; F.lon = p0.lon; F.ubiDeducida = true; }""",
    'el resumen del IGC')

# ============================================================
# 2 — al fallar: 'continuar sin IGC' lleva al paso 3, no al 5
# ============================================================
rep("""    const c = document.getElementById('igcSin');
    if (c) c.onclick = () => { F.igc = false; paso = 5; pintaPaso(); };""",
    """    const c = document.getElementById('igcSin');
    if (c) c.onclick = () => { F.igc = false; F.igcSin = true; paso = 3; pintaPaso(); };""",
    'el "continuar sin IGC" del error → paso 3')

# ============================================================
# 3 — distKm hace falta aqui
# ============================================================
if 'function distKm' not in s:
    # ¿lo exporta app.js?
    ap = open(BASE + 'app.js', encoding='utf-8').read()
    if 'export function distKm' in ap or 'export const distKm' in ap:
        rep("""  DIRECCIONES, TIPOS_ZONA, CLAVE_LOCAL, CLAVE_VUELOS, guardaLocal, igcDemo,""",
            """  DIRECCIONES, TIPOS_ZONA, CLAVE_LOCAL, CLAVE_VUELOS, guardaLocal, igcDemo,
  distKm,""", 'distKm importado de app.js')
    else:
        print('  ⚠ distKm no esta en app.js, hay que mirarlo')

open(BASE + 'report.js', 'w', encoding='utf-8').write(s)
print('  cambios:', toc)
