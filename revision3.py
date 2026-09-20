#!/usr/bin/env python3
"""CSS de las etiquetas nuevas, la frase de patrones de Pam, y los datos."""
import json
import urllib.request

RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0


def rep(v, n):
    global s, toc
    if v in s:
        s = s.replace(v, n); toc += 1
    else:
        print('  NO ENCUENTRO:', v[:70].replace('\n', ' | '))


# ---------- 1) el CSS de las etiquetas de gravedad y el check del IGC ----------
rep("""  .inc.pendiente{opacity:.82}""", """  placeholder""")   # por si ya existe

rep("""  .marcaRacha{background:var(--casiBg);color:#8a5a10;font-size:10px;font-weight:800;
    padding:2px 7px;border-radius:20px;margin-left:5px}""",
    """  .marcaRacha{background:var(--casiBg);color:#8a5a10;font-size:10px;font-weight:800;
    padding:2px 7px;border-radius:20px;margin-left:5px}

  /* ===== LA GRAVEDAD EN LA TARJETA =====
     Pam: 'naranja solo para advertencias importantes, rojo solo para accidente
     grave o fatalidad'. Asi que el color sube con la gravedad, sin gritar. */
  .etq.sevEtq{background:#eef3f6;color:#5f7a86;text-transform:none;
    letter-spacing:0;font-size:10.5px;margin-left:auto;white-space:nowrap}
  .inc.sevincidente .etq.sevEtq{background:#eef2f4;color:#4a6470}
  .inc.sevaccidente .etq.sevEtq{background:#fdf1e0;color:#8a5a10}
  .inc.sevgrave .etq.sevEtq{background:#fbeeec;color:#8f3f36}
  .inc.sevfatal .etq.sevEtq{background:#e4e9eb;color:#26343b}
  .inc.sevnear{border-left-color:#8ba3ad}
  .inc.sevincidente{border-left-color:#5f7a86}
  .inc.sevaccidente{border-left-color:#d9782f}
  .inc.sevgrave{border-left-color:#b5544a}
  .inc.sevfatal{border-left-color:#33424a}

  /* pendiente de verificacion: se ve, pero se nota que no esta confirmado */
  .etq.pendEtq{background:#fdf6e8;color:#8a6420;display:inline-flex;
    align-items:center;gap:3px;text-transform:none;letter-spacing:0;font-size:10px}
  .etq.pendEtq .mso{font-size:13px}
  .inc.pendiente{background:#fcfcfa}

  /* el check del IGC */
  .marcaCheck{display:flex;align-items:center;gap:9px;margin-top:11px;
    font-size:12.5px;color:#2b4750;cursor:pointer;line-height:1.4}
  .marcaCheck input{width:18px;height:18px;accent-color:var(--mar);flex-shrink:0}
  .marcaCheck span{font-weight:600}""")

# ---------- 2) la frase de patrones (la de Pam) ----------
rep("""      <div class="cabSeccion"><h2>Patrones y análisis</h2>
        <span class="sub">Lo que sale cuando muchos pilotos reportan.</span></div>""",
    """      <div class="cabSeccion"><h2>Patrones</h2>
        <span class="sub">Los eventos aislados cuentan historias. Juntos revelan patrones.</span></div>""")

# ---------- 3) la cabecera de la derecha: eventos, no reportes ----------
rep("""<div class="cabDer">Una comunidad<br>por vuelos más seguros</div>""",
    """<div class="cabDer">Una comunidad<br>por vuelos más seguros</div>""")

# ---------- 4) terminos sueltos que quedaban ----------
for v, n in [
    ('reportes de la comunidad', 'eventos reportados'),
    ('<div class="t">reportes</div>', '<div class="t">eventos</div>'),
    ('total + \' reportes en total\'', 'total + \' eventos en total\''),
    ('\' reportes en total\'', '\' eventos en total\''),
    ('Los patrones salen cuando hay al menos 3 reportes. ', 'Los patrones salen cuando hay al menos 3 eventos. '),
    ('Ahora hay ', 'Ahora hay '),
    ('Sé el primero en contar uno.', 'Sé el primero en contar uno.'),
    ('de la comunidad</div>', 'eventos</div>'),
    ('reportes traen el viento real', 'eventos traen el viento real'),
    ('En la zona de <b>', 'En <b>'),
    (' reportes</b>, y de ellos', ' eventos</b>, y de ellos'),
]:
    if v in s and v != n:
        s = s.replace(v, n); toc += 1

open(RUTA, 'w', encoding='utf-8').write(s)
print('  cambios en el HTML:', toc)

# ==========================================================================
# 5) MIGRAR LOS DATOS DE EJEMPLO al modelo nuevo (sev / sit / cons)
# ==========================================================================
BASE = "https://plan-gym-8aff7-default-rtdb.firebaseio.com/skyreport/incidentes"

# el tipo viejo -> la situacion nueva
SIT = {'perdida': 'plegada', 'cable': 'cable', 'arbol': 'arbol',
       'colision': 'proximidad', 'rotor': 'rotor', 'meteo': 'rotor',
       'aterrizaje': 'aterrizaje', 'despegue': 'despegue', 'bajo': 'bajo'}

# a cada ejemplo le pongo su gravedad definitiva, para que se vea la escala
SEV = {
    0: ('near',      'sin'),
    1: ('near',      'sin'),
    2: ('incidente', 'leves'),
    3: ('near',      'sin'),
    4: ('incidente', 'sin'),
    5: ('accidente', 'leves'),
    6: ('incidente', 'leves'),
    7: ('near',      'sin'),
    8: ('near',      'sin'),
    9: ('fatal',     'fatal'),
}

d = json.load(urllib.request.urlopen(BASE + ".json", timeout=25)) or {}
print()
print('  migrando', len(d), 'ejemplos...')
for k in sorted(d.keys()):
    v = d[k]
    if 'sev' in v:
        continue
    tipo_viejo = v.get('tipo')
    sit = SIT.get(tipo_viejo, 'otro')
    idx = list(sorted(d.keys())).index(k)
    sev, cons = SEV.get(idx, ('near', 'sin'))
    v['sit'] = sit
    v['sev'] = sev
    v['cons'] = cons
    v['verif'] = 'pendiente' if sev == 'fatal' else 'ok'
    v.pop('tipo', None)
    v.pop('gravedad', None)
    v['v'] = 4
    req = urllib.request.Request(BASE + '/' + k + '.json',
        data=json.dumps(v).encode('utf-8'), method='PUT',
        headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req, timeout=25).read()
    print('   %-10s -> %-10s %-10s %s' % (tipo_viejo, sev, sit, cons))
