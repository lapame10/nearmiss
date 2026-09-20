#!/usr/bin/env python3
"""Cambia los 18 botones de mes por dos desplegables (mes + año).

Pam: 'mejor que se pueda escoger mes y año de un carrilete'. En iPhone un
select se abre como la rueda nativa del calendario, que es mas comodo y mas
limpio que 18 botones apilados.
"""

RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()

# 1) el bloque que rellenaba los 18 botones
viejo1 = """/* los meses: los ultimos 18, del mas nuevo al mas viejo */
(function(){
  const hoy = new Date();
  const meses = [];
  for (let k = 0; k < 18; k++){
    const d = new Date(hoy.getFullYear(), hoy.getMonth() - k, 1);
    meses.push({ id: d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0'),
                 n: MESES[d.getMonth()] + ' ' + d.getFullYear() });
  }
  pintaOpciones('opMes', meses, 'mes');
})();"""

nuevo1 = """/* ===== EL SELECTOR DE MES Y AÑO =====
   Dos desplegables nativos: en el movil se abren como la rueda del calendario
   (lo que pidio Pam). Mas limpio y mas rapido que 18 botones apilados. */
function mesElegido(){
  const m = $('selMes').value, a = $('selAnio').value;
  return (m && a) ? (a + '-' + m) : null;
}

(function(){
  const hoy = new Date();
  const sm = $('selMes'), sa = $('selAnio');

  /* los meses, del mas nuevo al mas viejo, sin repetir */
  const vistos = {};
  for (let k = 0; k < 18; k++){
    const d = new Date(hoy.getFullYear(), hoy.getMonth() - k, 1);
    const num = String(d.getMonth() + 1).padStart(2, '0');
    if (vistos[num]) continue;
    vistos[num] = 1;
    const o = document.createElement('option');
    o.value = num;
    o.textContent = MESES[d.getMonth()].charAt(0).toUpperCase() + MESES[d.getMonth()].slice(1);
    sm.appendChild(o);
  }

  /* los años: este y los 4 anteriores */
  for (let k = 0; k < 5; k++){
    const a = hoy.getFullYear() - k;
    const o = document.createElement('option');
    o.value = a;
    o.textContent = a;
    if (k === 0) o.selected = true;      /* el año actual ya puesto */
    sa.appendChild(o);
  }

  const actualiza = () => {
    sel.mes = mesElegido();
    sm.classList.toggle('vacio', !sm.value);
  };
  sm.onchange = actualiza;
  sa.onchange = actualiza;
  sm.classList.add('vacio');
})();"""

# 2) al limpiar el formulario, resetear tambien los desplegables
viejo2 = """    ['opTipos','opGrav','opFase','opMes','opFranja','opViento'].forEach(id => {
      $(id).querySelectorAll('button').forEach(b => b.classList.remove('on'));
    });"""
nuevo2 = """    ['opTipos','opGrav','opFase','opFranja','opViento'].forEach(id => {
      $(id).querySelectorAll('button').forEach(b => b.classList.remove('on'));
    });
    $('selMes').value = '';
    $('selMes').classList.add('vacio');"""

# 3) la validacion del mes: que diga "mes y año"
viejo3 = "  if (!sel.mes) falta.push('el mes');"
nuevo3 = "  if (!sel.mes) falta.push('el mes y el año');"

for viejo, nuevo in [(viejo1, nuevo1), (viejo2, nuevo2), (viejo3, nuevo3)]:
    if viejo not in s:
        print('  NO ENCUENTRO:', viejo[:60].replace('\n', ' | '))
    else:
        s = s.replace(viejo, nuevo)
        print('  OK:', viejo[:56].replace('\n', ' | '))

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  archivo:', len(s), 'bytes')
