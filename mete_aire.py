#!/usr/bin/env python3
"""El aire, con control deslizante en vez de botones sueltos.

Pam: 'en como estaba el aire, eso es como de niño'.
Ahora es un segmented control estilo iOS (4 niveles) + una etiqueta aparte
para "racheado o cambiante", que es otra cosa distinta (no es intensidad).
"""

RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0

# 1) las opciones del viento: 4 niveles de intensidad
viejo = """const VIENTOS = [
  { id:'flojo',     n:'Flojo' },
  { id:'normal',    n:'Normal' },
  { id:'fuerte',    n:'Fuerte' },
  { id:'cambiante', n:'Cambiante / racheado' },
  { id:'nose',      n:'No sé' },
];"""
nuevo = """/* la intensidad del aire, de menos a mas. El "racheado" va aparte porque no
   es intensidad: puedes tener aire flojo y racheado a la vez. */
const VIENTOS = [
  { id:'calmo',  n:'Calmo' },
  { id:'flojo',  n:'Flojo' },
  { id:'normal', n:'Normal' },
  { id:'fuerte', n:'Fuerte' },
];"""
if viejo in s: s = s.replace(viejo, nuevo); toc += 1
else: print('  NO ENCUENTRO las opciones del viento')

# 2) el manejador del control y de la etiqueta
viejo2 = "pintaOpciones('opViento', VIENTOS, 'viento');"
nuevo2 = """/* ===== EL AIRE: control deslizante + etiqueta de racheado ===== */
(function(){
  const seg = $('segAire');
  seg.onclick = ev => {
    const b = ev.target.closest('button');
    if (!b) return;
    seg.querySelectorAll('button').forEach(x => x.classList.remove('on'));
    b.classList.add('on');
    sel.viento = b.dataset.id;
  };
  const chips = $('chipsAire');
  chips.onclick = ev => {
    const b = ev.target.closest('button');
    if (!b) return;
    b.classList.toggle('on');
    sel.racheado = b.classList.contains('on');
  };
})();"""
if viejo2 in s: s = s.replace(viejo2, nuevo2); toc += 1
else: print('  NO ENCUENTRO pintaOpciones del viento')

# 3) guardar el racheado
viejo3 = "    viento: sel.viento, relato: relato.slice(0, 900),"
nuevo3 = "    viento: sel.viento, racheado: !!sel.racheado, relato: relato.slice(0, 900),"
if viejo3 in s: s = s.replace(viejo3, nuevo3); toc += 1
else: print('  NO ENCUENTRO donde se guarda el viento')

# 4) limpiar al enviar
viejo4 = """    ['opTipos','opGrav','opFase','opFranja','opViento'].forEach(id => {
      $(id).querySelectorAll('button').forEach(b => b.classList.remove('on'));
    });"""
nuevo4 = """    ['opTipos','opGrav','opFase','opFranja'].forEach(id => {
      $(id).querySelectorAll('button').forEach(b => b.classList.remove('on'));
    });
    $('segAire').querySelectorAll('button').forEach(b => b.classList.remove('on'));
    $('chipsAire').querySelectorAll('button').forEach(b => b.classList.remove('on'));"""
if viejo4 in s: s = s.replace(viejo4, nuevo4); toc += 1
else: print('  NO ENCUENTRO el bloque de limpiar')

# 5) en la lista, que se vea el racheado aparte
viejo5 = """        ${i.viento ? '· viento ' + ((VIENTOS.find(v => v.id === i.viento) || {}).n || '').toLowerCase() : ''}"""
nuevo5 = """        ${i.viento ? '· aire ' + ((VIENTOS.find(v => v.id === i.viento) || {}).n || i.viento).toLowerCase() : ''}${i.racheado ? ' y racheado' : ''}"""
if viejo5 in s: s = s.replace(viejo5, nuevo5); toc += 1
else: print('  NO ENCUENTRO el texto del viento en la lista')

# 6) y en los filtros: sin cambios (los filtros son por tipo)

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios aplicados:', toc, '/ 5')
print('  archivo:', len(s), 'bytes')
