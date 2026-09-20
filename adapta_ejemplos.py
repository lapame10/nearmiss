#!/usr/bin/env python3
"""Adapta los reportes de ejemplo al vocabulario del diseno de Pam.

Tipos viejos: plegada, cable, arbol, colision, rotor, aterrizaje, despegue, bajo
Tipos nuevos (los del diseno): casi, perdida, colision, equipo, meteo, otro

Y la gravedad nueva: sin / leves / danos / graves
"""
import json
import urllib.request

FIRE = "https://plan-gym-8aff7-default-rtdb.firebaseio.com/nearmiss/incidentes"

TIPO = {
    'plegada': 'perdida', 'rotor': 'meteo', 'cable': 'casi', 'arbol': 'casi',
    'colision': 'colision', 'aterrizaje': 'casi', 'despegue': 'equipo',
    'bajo': 'casi',
}
GRAV = {'casi': 'sin', 'leve': 'leves', 'grave': 'graves'}

# lo que sintio cada piloto (la pregunta del aire del diseno de Pam)
AIRE = {
    'plegada': 'turbulento', 'rotor': 'variable', 'cable': 'tranquilo',
    'arbol': 'fuerte', 'colision': 'termico', 'aterrizaje': 'tranquilo',
    'despegue': 'variable', 'bajo': 'fuerte',
}

d = json.load(urllib.request.urlopen(FIRE + ".json", timeout=25)) or {}
print("  reportes:", len(d))
n = 0
for k, v in d.items():
    viejoT = v.get('tipo')
    v['tipo'] = TIPO.get(viejoT, viejoT)
    v['gravedad'] = GRAV.get(v.get('gravedad'), v.get('gravedad'))
    v['aire'] = AIRE.get(viejoT, None)
    v['v'] = 3
    req = urllib.request.Request(FIRE + '/' + k + '.json',
        data=json.dumps(v).encode('utf-8'), method='PUT',
        headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req, timeout=25).read()
    print("  %-11s -> %-10s %s" % (viejoT, v['tipo'], v['gravedad']))
    n += 1
print()
print("  actualizados:", n)
