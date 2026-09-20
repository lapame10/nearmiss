#!/usr/bin/env python3
"""Mete incidentes de EJEMPLO para que se vean los patrones.

OJO: son inventados, para la demo. Antes de que la app se use de verdad hay
que borrarlos (o dejarlos marcados como ejemplo).
"""
import json
import urllib.request

FIRE = "https://plan-gym-8aff7-default-rtdb.firebaseio.com/nearmiss/incidentes"

# Ejemplos realistas de la zona de Valle de Bravo (redondeados a ~100 m,
# que es como los guarda la app de verdad)
EJEMPLOS = [
    dict(tipo='plegada', gravedad='casi', fase='termica', lat=19.107, lon=-100.126,
         mes='2026-05', franja='mediodia', viento='fuerte',
         relato='Térmica fuerte entrando al valle. Se me cerró el lado derecho de golpe, '
                'un 50%. Tres giros para recuperar. Iba cargado y con las manos altas.'),
    dict(tipo='cable', gravedad='casi', fase='aproximacion', lat=19.13, lon=-100.15,
         mes='2026-04', franja='tarde', viento='normal',
         relato='En la aproximación a un campo vi el tendido tarde, ya bajo. Pasé por '
                'debajo por poco. Desde arriba el cable casi no se ve.'),
    dict(tipo='arbol', gravedad='leve', fase='aproximacion', lat=19.11, lon=-100.16,
         mes='2026-07', franja='tarde', viento='fuerte',
         relato='Me quedé bajo en el sotavento y no me dio para cruzar. Acabé en los pinos. '
                'Sin daño personal, la vela se enganchó. Tardé 40 min en sacarla.'),
    dict(tipo='colision', gravedad='casi', fase='termica', lat=19.108, lon=-100.124,
         mes='2026-06', franja='mediodia', viento='normal',
         relato='Subiendo en espiral con 4 más en la misma térmica, cada uno a su altura. '
                'Uno entró por el otro lado sin mirar. Nos vimos a 5 metros. Ni un grito.'),
    dict(tipo='rotor', gravedad='casi', fase='transito', lat=19.15, lon=-100.18,
         mes='2026-02', franja='manana', viento='cambiante',
         relato='Cruzando hacia la cresta me cogió un rotor fuerte. La vela se metió para '
                'delante y me tiró del arnés. Susto serio. El viento había rolado.'),
    dict(tipo='plegada', gravedad='leve', fase='termica', lat=19.106, lon=-100.127,
         mes='2026-09', franja='mediodia', viento='fuerte',
         relato='Cierre asimétrico grande con la vela acelerada. Más de la mitad del ala. '
                'Con la mano derecha conseguí pararla pero perdí bastante altura.'),
    dict(tipo='aterrizaje', gravedad='leve', fase='aterrizaje', lat=19.19, lon=-100.13,
         mes='2026-03', franja='tarde', viento='normal',
         relato='Campo de aterrizaje con piedras grandes. No las vi hasta el último momento. '
                'Aterrizé encima de una y me doblé el tobillo.'),
    dict(tipo='despegue', gravedad='casi', fase='despegue', lat=19.1075, lon=-100.1255,
         mes='2026-01', franja='manana', viento='cambiante',
         relato='En el despegue viento racheado. La vela se me infló torcida y me arrastró '
                'un metro hacia el lado. Un compañero me agarró.'),
    dict(tipo='bajo', gravedad='casi', fase='aproximacion', lat=19.12, lon=-100.14,
         mes='2026-08', franja='tarde', viento='fuerte',
         relato='Me confié y me quedé sin altura en el valle. El viento en contra me comió '
                'todo. Acabé en un campo lejos, sin problema, pero el coche tardó una hora.'),
    dict(tipo='rotor', gravedad='grave', fase='transito', lat=19.148, lon=-100.182,
         mes='2026-05', franja='tarde', viento='fuerte',
         relato='Rotor en la zona baja del valle. La vela colapsó entera y entré en giro. '
                'Tiré de reserva. Sin lesiones, pero la vela quedó destrozada.'),
]

for e in EJEMPLOS:
    e['creado'] = 1789000000000 + len(e) * 1000
    e['v'] = 1
    e['ejemplo'] = True          # marcados, para poder borrarlos de golpe
    req = urllib.request.Request(FIRE + '.json',
        data=json.dumps(e).encode('utf-8'), method='POST',
        headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=20) as r:
        print('  metido:', e['tipo'], e['gravedad'], e['mes'])

print()
print('  total de ejemplo:', len(EJEMPLOS))
