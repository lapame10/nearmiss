#!/usr/bin/env python3
"""El 'Otro' tiene que decir cual.

Pam: 'que te digan que otro, no solo que puchen ese boton'. Tiene razon: si
todos ponen 'otro' no hay dato, y encima los 'otro' son los que mas enseñan.
"""

RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()

cambios = [
    # 1) al elegir un tipo, si es "otro" saco la caja para que lo escriba
    ("""    div.querySelectorAll('button').forEach(x => x.classList.remove('on'));
    b.classList.add('on');
    sel[campo] = b.dataset.id;
  };
}""",
     """    div.querySelectorAll('button').forEach(x => x.classList.remove('on'));
    b.classList.add('on');
    sel[campo] = b.dataset.id;
    /* si elige "otro", le pido que diga cual: si no, ese reporte no enseña nada */
    if (campo === 'tipo'){
      $('cajaOtro').classList.toggle('on', sel.tipo === 'otro');
      if (sel.tipo === 'otro') setTimeout(() => $('otroTexto').focus(), 120);
    }
  };
}"""),

    # 2) validar: el "otro" hay que decirlo
    ("""  if (!sel.mes) falta.push('el mes');
  if (falta.length){""",
     """  if (!sel.mes) falta.push('el mes');
  const otro = $('otroTexto').value.trim();
  if (sel.tipo === 'otro' && !otro) falta.push('qué tipo era (el «otro» hay que decir cuál)');
  if (falta.length){"""),

    # 3) guardarlo
    ("""    viento: sel.viento, relato: relato.slice(0, 900),
    creado: Date.now(),""",
     """    viento: sel.viento, relato: relato.slice(0, 900),
    otro: (sel.tipo === 'otro') ? otro : null,
    creado: Date.now(),"""),

    # 4) limpiarlo al enviar y esconder la caja
    ("""    $('txtSitio').textContent = 'Toca el sitio aproximado. No hace falta que sea exacto: solo queremos saber la zona.';""",
     """    $('otroTexto').value = '';
    $('cajaOtro').classList.remove('on');
    $('txtSitio').textContent = 'Toca el sitio aproximado. No hace falta que sea exacto: solo queremos saber la zona.';"""),

    # 5) en la lista: si es "otro", que se vea cual
    ("""  $('listaInc').innerHTML = vis.length ? vis.map(i => {
    const t = tipoDe(i.tipo);
    return `<div class="inc ${i.gravedad || ''}">
      <div class="tit">${t.e} ${t.n}</div>""",
     """  $('listaInc').innerHTML = vis.length ? vis.map(i => {
    const t = tipoDe(i.tipo);
    const titulo = (i.tipo === 'otro' && i.otro)
      ? t.e + ' ' + escapa(i.otro)
      : t.e + ' ' + t.n;
    return `<div class="inc ${i.gravedad || ''}">
      <div class="tit">${titulo}</div>"""),

    # 6) en los patrones: los "otro" se agrupan por lo que la gente escribio,
    #    asi si 4 personas dicen "objetivo en el aire" sale como un tipo propio
    ("""  const porTipo = {};
  incidentes.forEach(i => { porTipo[i.tipo] = (porTipo[i.tipo] || 0) + 1; });
  const tipos = Object.entries(porTipo).sort((a, b) => b[1] - a[1]);""",
     """  const porTipo = {};
  incidentes.forEach(i => {
    /* los "otro" no se juntan todos en una bolsa: se agrupan por lo que
       escribio la gente, para que un tipo raro repetido salga a la luz */
    const clave = (i.tipo === 'otro' && i.otro)
      ? 'otro::' + i.otro.trim().toLowerCase()
      : i.tipo;
    porTipo[clave] = (porTipo[clave] || 0) + 1;
  });
  const tipos = Object.entries(porTipo).sort((a, b) => b[1] - a[1]);"""),

    # y la etiqueta de esos grupos
    ("""  if (tipos.length) html += bloque('Qué pasa más', total + ' reportes en total',
    tipos.map(t => [tipoDe(t[0]).e + ' ' + tipoDe(t[0]).n, t[1]]));""",
     """  if (tipos.length) html += bloque('Qué pasa más', total + ' reportes en total',
    tipos.map(t => {
      if (t[0].indexOf('otro::') === 0) return ['❓ ' + t[0].slice(6), t[1]];
      return [tipoDe(t[0]).e + ' ' + tipoDe(t[0]).n, t[1]];
    }));"""),
]

for viejo, nuevo in cambios:
    if viejo not in s:
        print('  NO ENCUENTRO:', viejo[:64].replace('\n', ' | '))
    else:
        s = s.replace(viejo, nuevo)
        print('  OK:', viejo[:58].replace('\n', ' | '))

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  archivo:', len(s), 'bytes')
