#!/usr/bin/env python3
"""Migra los datos al nodo nuevo y pone una fatalidad de ejemplo.

El nodo de Firebase se llamaba 'nearmiss'. Lo renombro a 'skyreport' para que
todo sea coherente, y de paso cambio uno de los ejemplos a fatalidad para que
se vea como queda en los patrones.
"""
import json
import urllib.request

BASE = "https://plan-gym-8aff7-default-rtdb.firebaseio.com"


def get(p):
    with urllib.request.urlopen(BASE + p + ".json", timeout=25) as r:
        return json.load(r)


def put(p, d):
    req = urllib.request.Request(BASE + p + ".json",
        data=json.dumps(d).encode('utf-8'), method='PUT',
        headers={'Content-Type': 'application/json'})
    return urllib.request.urlopen(req, timeout=25).read()


viejo = get("/nearmiss/incidentes") or {}
print("  reportes en el nodo viejo:", len(viejo))

# uno de los ejemplos pasa a fatalidad (inventado, para que se vea)
for k, v in viejo.items():
    if v.get('tipo') == 'meteo' and v.get('gravedad') == 'graves':
        v['gravedad'] = 'fatalidad'
        v['relato'] = ('Rotor en la zona baja del valle con viento fuerte. El piloto '
                       'perdió el control cerca del terreno. Se activaron los servicios '
                       'de emergencia. No lo cuento con más detalle porque no aporta: '
                       'lo que importa es la zona, la hora y las condiciones.')
        print("  -> un ejemplo cambiado a fatalidad")
        break

put("/skyreport/incidentes", viejo)
print("  copiado a /skyreport/incidentes:", len(viejo))

# comprobar
d = get("/skyreport/incidentes") or {}
print("  comprobado:", len(d), "reportes")
graves = {}
for v in d.values():
    graves[v.get('gravedad')] = graves.get(v.get('gravedad'), 0) + 1
print()
for k, n in graves.items():
    print("   %-12s %d" % (k, n))
