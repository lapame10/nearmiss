#!/usr/bin/env python3
"""Limpia las referencias que quedaron a elementos que ya no existen.

Al quitar la pregunta del aire y el selector de mes, quedaron dos trozos de
JavaScript apuntando a cosas borradas. Eso reventaria al enviar el formulario.
"""

RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0

# 1) la limpieza del control del aire (ya no existe)
viejo = """    $('segAire').querySelectorAll('button').forEach(b => b.classList.remove('on'));
    $('chipsAire').querySelectorAll('button').forEach(b => b.classList.remove('on'));
"""
if viejo in s: s = s.replace(viejo, ''); toc += 1
else: print('  NO ENCUENTRO la limpieza del aire')

# 2) todo el bloque del selector de mes (ya no existe)
ini = s.find('/* ===== EL SELECTOR DE MES Y AÑO =====')
if ini >= 0:
    # acaba en el cierre del IIFE
    fin = s.find('  sm.classList.add(\'vacio\');\n})();', ini)
    if fin > 0:
        fin = s.find('\n', fin + len("  sm.classList.add('vacio');\n})();")) + 1
        s = s[:ini] + s[fin:]
        toc += 1
        print('  OK: fuera el bloque del selector de mes')
    else:
        print('  NO ENCUENTRO el final del bloque de mes')
else:
    print('  NO ENCUENTRO el inicio del bloque de mes')

# 3) la funcion mesElegido tampoco se usa
s = s.replace("""function mesElegido(){
  const m = $('selMes').value, a = $('selAnio').value;
  return (m && a) ? (a + '-' + m) : null;
}

""", '')

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')

# comprobacion final
import re
faltan = []
for ref in ['segAire', 'chipsAire', 'opViento', 'selMes', 'selAnio', 'mesElegido', 'sel.viento', 'sel.racheado']:
    if ref in s:
        faltan.append(ref)
print('  referencias huerfanas que quedan:', faltan if faltan else 'NINGUNA')
