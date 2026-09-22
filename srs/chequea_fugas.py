#!/usr/bin/env python3
"""Comprobador 7: fugas de idioma que NO son texto plano.

El numero 4 mira el HTML de las plantillas y solo ve texto escrito a mano. Todo
lo que se construye con variables se le escapa. Esto busca lo otro:

  a) arrays de nombres de meses/dias dentro del codigo
  b) nombres crudos de data.js usados en pantalla (.n sin nombreEv/nombreFase)
  c) texto entre comillas que parece interfaz y no pasa por t()

No es perfecto: avisa para que alguien lo mire, no decide.
"""
import re, sys, os

BASE = '/Users/lapame10/.hermes/workspace/nearmiss/srs/'
fallos = []

for f in ['app.js', 'report.js', 'mapa.js', 'signals.js']:
    src = open(BASE + f, encoding='utf-8').read()

    # a) meses o dias en un array
    for m in re.finditer(r"\[\s*'(Jan|Feb|Mar|Ene|Lun|Mon|Sun)'", src):
        linea = src[:m.start()].count('\n') + 1
        fallos.append('%s:%d  array de meses o dias (usa Intl)' % (f, linea))

    # b) nombres de data.js pintados en crudo
    for m in re.finditer(r'mas(Evento|Fase|Zona|Viento)\??\.\s*(n|nombre)\b', src):
        linea = src[:m.start()].count('\n') + 1
        fallos.append('%s:%d  nombre crudo en pantalla (%s)' % (f, linea, m.group(0)[:20]))

    # c) texto que parece interfaz y va suelto en un span o entre > <
    for m in re.finditer(r'>\s*([A-Z][a-z][A-Za-z \u00c0-\u017f]{5,40}?)\s*<', src):
        s = m.group(1).strip()
        if re.fullmatch(r'[A-Z][a-zA-Z \u00c0-\u017f]+', s) and ' ' in s:
            linea = src[:m.start()].count('\n') + 1
            fallos.append('%s:%d  posible texto suelto: "%s"' % (f, linea, s[:34]))

if fallos:
    print('  fugas que mirar: %d' % len(fallos))
    for x in fallos[:14]:
        print('   · ' + x)
else:
    print('  ✓ ninguna fuga de las que este comprobador sabe ver')
