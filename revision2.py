#!/usr/bin/env python3
"""Actualiza todo el JS a la clasificacion nueva (revision de Pam).

tipo -> sev (gravedad del evento) + sit (situacion)
gravedad -> cons (consecuencias)
"""
RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0


def rep(viejo, nuevo, veces=1):
    global s, toc
    if viejo in s:
        s = s.replace(viejo, nuevo, veces)
        toc += 1
        return True
    print('  NO ENCUENTRO:', viejo[:70].replace('\n', ' | '))
    return False


# ---------- 1) las funciones que buscan en las listas ----------
rep("""function tipoDe(id){ return TIPOS.find(t => t.id === id) || TIPOS[TIPOS.length - 1]; }""",
    """function sevDe(id){ return SEVERIDAD.find(t => t.id === id) || SEVERIDAD[0]; }
function sitDe(id){ return SITUACION.find(t => t.id === id) || SITUACION[SITUACION.length - 1]; }
function consDe(id){ return CONSEC.find(t => t.id === id) || { n: id || '', e:'help' }; }
/* el color, segun Pam: gris para lo leve, naranja para lo que avisa,
   y rojo SOLO para accidente grave o fatalidad */
function colorDe(id){
  return id === 'fatal' ? '#33424a'
       : id === 'grave' ? '#b5544a'
       : id === 'accidente' ? '#d9782f'
       : id === 'incidente' ? '#5f7a86'
       : '#8ba3ad';
}""")

# ---------- 2) el selector de tipos: ahora son tres ----------
rep("""    if (campo === 'tipo'){
      $('cajaOtro').classList.toggle('on', sel.tipo === 'otro');
      if (sel.tipo === 'otro') setTimeout(() => $('otroTexto').focus(), 120);
    }
    /* si marca una fatalidad, sale el texto de respeto */
    if (campo === 'gravedad' && $('cajaFatalidad')){
      $('cajaFatalidad').classList.toggle('on', sel.gravedad === 'fatalidad');
    }""",
    """    /* si la situación es "otro", le pido que diga cuál */
    if (campo === 'sit'){
      $('cajaOtro').classList.toggle('on', sel.sit === 'otro');
      if (sel.sit === 'otro') setTimeout(() => $('otroTexto').focus(), 120);
    }
    /* si hay una fatalidad (en la gravedad o en las consecuencias), sale el
       texto de respeto y el aviso de que queda pendiente de verificación */
    if (campo === 'cons' || campo === 'sev'){
      const hayFatal = (sel.cons === 'fatal' || sel.sev === 'fatal');
      if ($('cajaFatalidad')) $('cajaFatalidad').classList.toggle('on', hayFatal);
    }""")

# ---------- 3) el mini mapa: color por severidad ----------
rep("""    const col = i.gravedad === 'fatalidad' ? '#33424a'
              : (i.gravedad === 'graves' ? '#b5544a'
              : (i.gravedad === 'sin' ? '#2f7d4f' : '#c98a24'));
    L.circleMarker([i.lat, i.lon], { radius:6, color:'#fff', weight:2,""",
    """    const col = colorDe(i.sev);
    L.circleMarker([i.lat, i.lon], { radius:6, color:'#fff', weight:2,""")

# ---------- 4) la lista ----------
rep("""  const vis = incidentes.filter(i => filtro === 'todos' || i.tipo === filtro);""",
    """  const vis = incidentes.filter(i => filtro === 'todos' || i.sev === filtro);""")

rep("""    const t = tipoDe(i.tipo);
    const titulo = (i.tipo === 'otro' && i.otro) ? escapa(i.otro) : t.n;
    return '<div class="inc ' + (i.gravedad || '') + '" data-id="' + i.id
      + '" onclick="irAlPunto(\\'' + i.id + '\\')">'
      + '<div class="tipo"><span class="mso">' + t.e + '</span>' + titulo + '</div>'""",
    """    const t = sevDe(i.sev);
    const sit = sitDe(i.sit);
    const titulo = (i.sit === 'otro' && i.otro) ? escapa(i.otro) : sit.n;
    const pend = (i.verif === 'pendiente');
    return '<div class="inc ' + (i.cons || '') + ' sev' + (i.sev || 'near')
      + (pend ? ' pendiente' : '') + '" data-id="' + i.id
      + '" onclick="irAlPunto(\\'' + i.id + '\\')">'
      + '<div class="tipo"><span class="mso">' + sit.e + '</span>' + titulo
      + '<span class="etq sevEtq">' + t.n + '</span>'
      + (pend ? '<span class="etq pendEtq"><span class="mso">pending</span>pendiente de verificación</span>' : '')
      + '</div>'""")

# ---------- 5) el color del punto en el mapa principal ----------
rep("""      const t = tipoDe(i.tipo);
      const col = i.gravedad === 'fatalidad' ? '#33424a'
                : (i.gravedad === 'graves' ? '#b5544a'
                : (i.gravedad === 'sin' ? '#2f7d4f' : '#c98a24'));""",
    """      const t = sevDe(i.sev);
      const col = colorDe(i.sev);""")

rep("""        .bindPopup('<b>' + t.n + '</b><br>'""",
    """        .bindPopup('<b>' + sitDe(i.sit).n + '</b> · ' + t.n + '<br>'""")

# ---------- 6) los patrones: por situacion, y por severidad ----------
rep("""    const clave = (i.tipo === 'otro' && i.otro)
      ? 'otro::' + i.otro.trim().toLowerCase() : i.tipo;
    porTipo[clave] = (porTipo[clave] || 0) + 1;""",
    """    const clave = (i.sit === 'otro' && i.otro)
      ? 'otro::' + i.otro.trim().toLowerCase() : (i.sit || 'otro');
    porTipo[clave] = (porTipo[clave] || 0) + 1;""")

rep("""    porZona[clave].tipos[i.tipo] = (porZona[clave].tipos[i.tipo] || 0) + 1;""",
    """    porZona[clave].tipos[i.sit] = (porZona[clave].tipos[i.sit] || 0) + 1;""")

rep("""      + '</b> son de tipo <b>' + tipoDe(tTop[0]).n.toLowerCase() + '</b>.</div>'""",
    """      + '</b> son de <b>' + sitDe(tTop[0]).n.toLowerCase() + '</b>.</div>'""")

rep("""    tipos.map(t => t[0].indexOf('otro::') === 0
      ? ['Otro: ' + t[0].slice(6), t[1]]
      : [tipoDe(t[0]).n, t[1]]));""",
    """    tipos.map(t => t[0].indexOf('otro::') === 0
      ? ['Otro: ' + t[0].slice(6), t[1]]
      : [sitDe(t[0]).n, t[1]]));""")

rep("""  if (tipos.length) html += bloque('Qué pasa más', 'pie_chart', total + ' reportes en total',""",
    """  if (tipos.length) html += bloque('Qué pasa más', 'pie_chart', total + ' eventos en total',""")

# ---------- 7) el bloque de severidad y el de consecuencias ----------
rep("""  const porGrav = {};
  incidentes.forEach(i => { if (i.gravedad) porGrav[i.gravedad] = (porGrav[i.gravedad] || 0) + 1; });
  if (Object.keys(porGrav).length) html += bloque('Cómo acabaron', 'monitor_heart',
    'del susto a lo peor: mirarlo sin morbo, para aprender',
    ['sin','leves','danos','graves','fatalidad']
      .filter(k => porGrav[k])
      .map(k => [(GRAV.find(g => g.id === k) || {}).n || k, porGrav[k]]));""",
    """  /* la gravedad y las consecuencias: de menos a mas, sin morbo */
  const porSev = {};
  incidentes.forEach(i => { if (i.sev) porSev[i.sev] = (porSev[i.sev] || 0) + 1; });
  if (Object.keys(porSev).length) html += bloque('Gravedad de los eventos', 'monitor_heart',
    'del susto a lo peor: mirarlo sin morbo, para aprender',
    ['near','incidente','accidente','grave','fatal']
      .filter(k => porSev[k]).map(k => [sevDe(k).n, porSev[k]]));

  const porCons = {};
  incidentes.forEach(i => { if (i.cons) porCons[i.cons] = (porCons[i.cons] || 0) + 1; });
  if (Object.keys(porCons).length) html += bloque('Consecuencias', 'healing',
    'el resultado, en datos',
    ['sin','leves','graves','danos','fatal']
      .filter(k => porCons[k]).map(k => [consDe(k).n, porCons[k]]));""")

# ---------- 8) los contadores de la derecha ----------
rep("""    incidentes.forEach(i => { cuenta[i.tipo] = (cuenta[i.tipo] || 0) + 1; });
    $('nPatrones').textContent = Object.values(cuenta).filter(n => n >= 3).length;""",
    """    incidentes.forEach(i => { cuenta[i.sit] = (cuenta[i.sit] || 0) + 1; });
    $('nPatrones').textContent = Object.values(cuenta).filter(n => n >= 3).length;""")

# ---------- 9) la validacion ----------
rep("""  if (!sel.tipo) falta.push('el tipo de incidente');
  if (!sel.gravedad) falta.push('cómo acabó');""",
    """  if (!sel.sev) falta.push('qué ocurrió');
  if (!sel.sit) falta.push('qué pasó');
  if (!sel.cons) falta.push('las consecuencias');""")

rep("""  if (sel.tipo === 'otro' && !otro) falta.push('cuál era el «otro»');""",
    """  if (sel.sit === 'otro' && !otro) falta.push('cuál era el «otro»');""")

# ---------- 10) el guardado ----------
rep("""    tipo: sel.tipo, gravedad: sel.gravedad, fase: fase,""",
    """    sev: sel.sev, sit: sel.sit, cons: sel.cons, fase: fase,""")

rep("""    otro: (sel.tipo === 'otro') ? otro : null,""",
    """    otro: (sel.sit === 'otro') ? otro : null,
    /* una fatalidad NO se publica al momento: queda pendiente de verificacion
       (idea de Pam: alguien puede equivocarse de fecha, sitio o incluso
       reportar un rumor). Los near miss entran directos. */
    verif: (sel.sev === 'fatal' || sel.cons === 'fatal') ? 'pendiente' : 'ok',""")

# ---------- 11) limpiar el formulario ----------
rep("""    ['opTipos','opGrav','opFranja','opAire'].forEach(id => {""",
    """    ['opSev','opSit','opCons','opFranja','opAire'].forEach(id => {""")

# ---------- 12) el arranque ----------
rep("""pintaOps('opTipos', TIPOS, 'tipo');
pintaOps('opGrav', GRAV, 'gravedad');""",
    """pintaOps('opSev', SEVERIDAD, 'sev');
pintaOps('opSit', SITUACION, 'sit');
pintaOps('opCons', CONSEC, 'cons');""")

# ---------- 13) los filtros: por gravedad ----------
rep("""  + TIPOS.map(t => '<button data-f="' + t.id + '"><span class="mso">' + t.e + '</span>'
      + t.n + '</button>').join('');""",
    """  + SEVERIDAD.map(t => '<button data-f="' + t.id + '"><span class="mso">' + t.e + '</span>'
      + t.n + '</button>').join('');""")

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios aplicados:', toc)
print('  archivo:', len(s), 'bytes')
print()
for viejo in ['TIPOS', 'GRAV[', 'tipoDe(', 'sel.tipo', 'sel.gravedad', 'i.gravedad', 'i.tipo']:
    n = s.count(viejo)
    if n: print('  ⚠ quedan referencias a', viejo, ':', n)
