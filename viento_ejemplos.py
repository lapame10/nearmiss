#!/usr/bin/env python3
"""Pone el viento REAL a los reportes de ejemplo, consultando el clima.

Es lo mismo que hara la app cuando alguien reporte: coge el dia y el sitio,
pregunta a Open-Meteo el viento de esa hora, y guarda los numeros.
"""
import json
import time
import urllib.request

FIRE = "https://plan-gym-8aff7-default-rtdb.firebaseio.com/nearmiss/incidentes"

# a cada ejemplo le doy un dia, para poder sacar el viento real
DIAS = {
    '2026-05': '2026-05-15', '2026-04': '2026-04-12', '2026-07': '2026-07-19',
    '2026-06': '2026-06-14', '2026-02': '2026-02-08', '2026-09': '2026-09-06',
    '2026-03': '2026-03-22', '2026-01': '2026-01-11', '2026-08': '2026-08-16',
}
HORA = {'manana': 9, 'mediodia': 13, 'tarde': 16}


def viento(lat, lon, dia, hora):
    u = ("https://archive-api.open-meteo.com/v1/archive"
         "?latitude=%.3f&longitude=%.3f&start_date=%s&end_date=%s"
         "&hourly=wind_speed_10m,wind_gusts_10m,wind_direction_10m&timezone=auto"
         % (lat, lon, dia, dia))
    try:
        d = json.load(urllib.request.urlopen(u, timeout=25))
        h = d.get('hourly', {})
        i = min(23, max(0, hora))
        v = h.get('wind_speed_10m', [None] * 24)[i]
        g = h.get('wind_gusts_10m', [None] * 24)[i]
        dr = h.get('wind_direction_10m', [None] * 24)[i]
        if v is None:
            return None
        return {'kmh': round(v), 'racha': round(g) if g is not None else None,
                'dir': round(dr) if dr is not None else None}
    except Exception as e:
        print('    fallo:', e)
        return None


d = json.load(urllib.request.urlopen(FIRE + ".json", timeout=25)) or {}
print("  reportes:", len(d))
print()

for k, v in d.items():
    dia = DIAS.get(v.get('mes'))
    if not dia:
        continue
    hora = HORA.get(v.get('franja'), 13)
    w = viento(v['lat'], v['lon'], dia, hora)
    if not w:
        print('  %-12s sin datos de viento' % v.get('tipo'))
        continue
    v['viento'] = w
    v['igcMin'] = v.get('igcMin') or None
    v['igcAltMax'] = v.get('igcAltMax') or None
    req = urllib.request.Request(FIRE + '/' + k + '.json',
        data=json.dumps(v).encode('utf-8'), method='PUT',
        headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req, timeout=25).read()
    rach = ' rachas %d' % w['racha'] if w['racha'] else ''
    print('  %-12s %s  ->  %d km/h%s, %d°' % (v.get('tipo'), dia, w['kmh'], rach, w['dir'] or 0))
    time.sleep(0.4)

print()
print("  listo: los ejemplos ya traen el viento REAL de su dia")
