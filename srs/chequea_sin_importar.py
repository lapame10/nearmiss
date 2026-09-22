#!/usr/bin/env python3
"""Comprobador: funciones que se usan y no se importan.

Este es el que me falto. Los otros comprobadores miraban los imports que HAY,
para ver si resuelven. Ninguno miraba los que FALTAN.

El fallo tipico: usar nombreFase() en report.js cuando esa funcion vive en
app.js y nunca se importo. El archivo compila (node --check no ve nada raro) y
revienta en tiempo de ejecucion con 'nombreFase is not defined'. Y solo pasa
cuando alguien entra en ese paso concreto del formulario, asi que una prueba
por encima no lo ve.

Es el mismo patron que ya me ha mordido varias veces: referencias a algo que
no existe en ese modulo. Aqui queda automatizado.
"""
import re, sys, os, glob

BASE = os.path.dirname(os.path.abspath(__file__)) + '/'
MODULOS = ['app', 'data', 'i18n', 'signals', 'config', 'supabase', 'igc', 'mapa']

afuera = {}
for f in MODULOS:
    ruta = BASE + f + '.js'
    if not os.path.exists(ruta): continue
    src = open(ruta, encoding='utf-8').read()
    n = set(re.findall(r'export\s+(?:async\s+)?(?:function|const|let|var|class)\s+([A-Za-z_$][\w$]*)', src))
    for b in re.findall(r'export\s*\{([^}]*)\}', src):
        for x in b.split(','):
            x = x.strip()
            if x: n.add(x.split(' as ')[-1].strip())
    afuera[f] = n
TODAS = set().union(*afuera.values()) if afuera else set()

total = 0
for ruta in sorted(glob.glob(BASE + '*.js')):
    nombre_arch = os.path.basename(ruta)
    if nombre_arch.startswith('chequea_') or nombre_arch.startswith('prepara_'): continue
    s = open(ruta, encoding='utf-8').read()
    tiene = set()
    for m in re.finditer(r"import\s*\{([^}]*)\}\s*from\s*'\./(\w+)\.js'", s):
        for x in m.group(1).split(','):
            x = x.strip().split(' as ')[-1].strip()
            if x: tiene.add(x)
    tiene |= set(re.findall(r'(?:function|const|let|var|class)\s+([A-Za-z_$][\w$]*)', s))
    for n in sorted(TODAS):
        if n in tiene: continue
        if re.search(r'[^\w.$]' + re.escape(n) + r'\s*\(', s):
            donde = [f for f, k in afuera.items() if n in k]
            print('  ✗ %s usa %s() y no la importa (esta en %s)' % (nombre_arch, n, ', '.join(donde)))
            total += 1

if total:
    print('  %d funciones sin importar' % total)
    sys.exit(1)
print('  ✓ ninguna funcion usada sin importar')
