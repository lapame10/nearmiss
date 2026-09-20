#!/usr/bin/env python3
"""Arregla la situacion de los ejemplos que quedaron en 'otro'.

Vienen de una migracion anterior donde el tipo decia 'casi', y ese tipo no
existe en las categorias nuevas. Miro el relato para deducir la situacion
correcta.
"""
import json
import urllib.request

BASE = "https://plan-gym-8aff7-default-rtdb.firebaseio.com/skyreport/incidentes"

# palabras del relato -> la situacion
PISTAS = [
    ('cable',       'cable'),
    ('tendido',     'cable'),
    ('pinos',       'arbol'),
    ('árbol',       'arbol'),
    ('arbol',       'arbol'),
    ('aterrizaje',  'aterrizaje'),
    ('campo',       'aterrizaje'),
    ('despegue',    'despegue'),
    ('rotor',       'rotor'),
    ('sotavento',   'sotavento'),
    ('espiral',     'plegada'),
    ('pleg',        'plegada'),
    ('cierre',      'plegada'),
]

d = json.load(urllib.request.urlopen(BASE + ".json", timeout=25)) or {}
n = 0
for k in sorted(d.keys()):
    v = d[k]
    if v.get('sit') != 'otro':
        continue
    rel = (v.get('relato') or '').lower()
    nueva = None
    for palabra, sit in PISTAS:
        if palabra in rel:
            nueva = sit
            break
    if not nueva:
        continue
    v['sit'] = nueva
    v.pop('otro', None)
    req = urllib.request.Request(BASE + '/' + k + '.json',
        data=json.dumps(v).encode('utf-8'), method='PUT',
        headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req, timeout=25).read()
    print('   corregido a: %-12s (%s)' % (nueva, v.get('sev')))
    n += 1

# y la fatalidad, que habla de sotavento y de rotor bajo
for k in sorted(d.keys()):
    v = d[k]
    if v.get('sev') == 'fatal' and v.get('sit') == 'rotor':
        v['sit'] = 'sotavento'
        req = urllib.request.Request(BASE + '/' + k + '.json',
            data=json.dumps(v).encode('utf-8'), method='PUT',
            headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=25).read()
        print('   la fatalidad pasa a: sotavento')
        n += 1

print()
print('  corregidos:', n)
print()
d = json.load(urllib.request.urlopen(BASE + ".json", timeout=25)) or {}
sev, sit = {}, {}
for v in d.values():
    sev[v.get('sev')] = sev.get(v.get('sev'), 0) + 1
    sit[v.get('sit')] = sit.get(v.get('sit'), 0) + 1
print('  === GRAVEDAD ===')
for k in ['near','incidente','accidente','grave','fatal']:
    if sev.get(k): print('   %-12s %d' % (k, sev[k]))
print()
print('  === SITUACION ===')
for k, v in sorted(sit.items(), key=lambda x: -x[1]):
    print('   %-12s %d' % (k, v))
