#!/usr/bin/env python3
"""NearMiss -> SkyReport, y se pueden registrar fatalidades.

Pam: 'me gustaria mas que se llamara SkyReport y que se puedan poner
fatalidades, por que es importante tener todos los datos'.

Tiene razon y es un argumento tecnico: sin las fatalidades los datos estan
SESGADOS (sesgo de supervivencia). Solo estarias analizando a los que tuvieron
suerte. En aviacion comercial los accidentes mortales son los que mas han
cambiado los procedimientos.

Pero se pide con respeto: sin nombres, y con un texto que lo diga claro.
"""

RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0

# ---------- 1) el nombre, en todas partes ----------
cambios_nombre = [
    ('<title>NearMiss — reportes anónimos de incidentes de parapente</title>',
     '<title>SkyReport — reportes anónimos de incidentes de parapente</title>'),
    ('    NearMiss\n    <span class="marcaTxt">Reportes anónimos de incidentes y casi accidentes de parapente</span>',
     '    SkyReport\n    <span class="marcaTxt">Reportes anónimos de incidentes y accidentes de parapente</span>'),
    ('<div><b>NearMiss</b></div>', '<div><b>SkyReport</b></div>'),
    ('<div>Reportes anónimos de incidentes y casi accidentes de parapente</div>',
     '<div>Reportes anónimos de incidentes y accidentes de parapente</div>'),
    ('<div><b>Importante</b><br>NearMiss no es un canal de emergencia.',
     '<div><b>Importante</b><br>SkyReport no es un canal de emergencia.'),
    ('<h2>Reportar un incidente o casi accidente</h2>',
     '<h2>Reportar un incidente o accidente</h2>'),
    ('Aquí puedes reportar de forma anónima incidentes y casi accidentes de parapente.',
     'Aquí puedes reportar de forma anónima incidentes y accidentes de parapente.'),
]
for v, n in cambios_nombre:
    if v in s: s = s.replace(v, n); toc += 1
    else: print('  NO ENCUENTRO:', v[:55])

# ---------- 2) la gravedad: se añade la fatalidad ----------
viejo = """const GRAV = [
  { id:'sin',    e:'check_circle',    n:'Sin lesiones' },
  { id:'leves',  e:'healing',         n:'Lesiones leves' },
  { id:'danos',  e:'car_crash',       n:'Daños materiales' },
  { id:'graves', e:'personal_injury', n:'Lesiones graves' },
];"""
nuevo = """/* La gravedad, de menos a mas. La fatalidad esta aqui a proposito: sin ella
   los datos estarian SESGADOS (solo analizarias a los que tuvieron suerte).
   En aviacion comercial los accidentes mortales son los que mas cambiaron los
   procedimientos. Pero se pide con respeto: sin nombres y sin detalles morbosos. */
const GRAV = [
  { id:'sin',       e:'check_circle',    n:'Sin lesiones' },
  { id:'leves',     e:'healing',         n:'Lesiones leves' },
  { id:'danos',     e:'car_crash',       n:'Daños materiales' },
  { id:'graves',    e:'personal_injury', n:'Lesiones graves' },
  { id:'fatalidad', e:'emergency',       n:'Fatalidad' },
];"""
if viejo in s: s = s.replace(viejo, nuevo); toc += 1
else: print('  NO ENCUENTRO la gravedad')

# ---------- 3) el estilo de la fatalidad (sobrio, sin rojo chillón) ----------
viejo2 = """  .ops.gravedad button.on[data-id=graves]{border-color:var(--grave);background:var(--graveBg);
    box-shadow:0 0 0 1px var(--grave) inset}
  .ops.gravedad button.on[data-id=graves] .mso{color:var(--grave)}"""
nuevo2 = """  .ops.gravedad button.on[data-id=graves]{border-color:var(--grave);background:var(--graveBg);
    box-shadow:0 0 0 1px var(--grave) inset}
  .ops.gravedad button.on[data-id=graves] .mso{color:var(--grave)}
  /* la fatalidad: gris muy oscuro, SOBRIO. Nada de rojo chillón: esto se trata
     con respeto, no como una alarma mas. */
  .ops.gravedad button.on[data-id=fatalidad]{border-color:#33424a;background:#eef1f3;
    box-shadow:0 0 0 1px #33424a inset}
  .ops.gravedad button.on[data-id=fatalidad] .mso{color:#33424a}"""
if viejo2 in s: s = s.replace(viejo2, nuevo2); toc += 1
else: print('  NO ENCUENTRO el estilo de gravedad')

# ---------- 4) la caja de respeto al elegir fatalidad ----------
viejo3 = """            <div class="ops gravedad" id="opGrav"></div>
          </div>"""
nuevo3 = """            <div class="ops gravedad" id="opGrav"></div>
            <div class="cajaFatalidad" id="cajaFatalidad">
              <span class="mso">volunteer_activism</span>
              <div>Gracias por contarlo. <b>Es el dato que más ayuda</b> a que no
              vuelva a pasar.<br><br>
              Cuéntalo <b>sin nombres</b> y sin detalles que no aporten aprendizaje.
              Lo que importa es qué pasó y en qué condiciones, no quién.</div>
            </div>
          </div>"""
if viejo3 in s: s = s.replace(viejo3, nuevo3); toc += 1
else: print('  NO ENCUENTRO donde la caja de fatalidad')

# ---------- 5) mostrarla al elegir fatalidad ----------
viejo4 = """    if (campo === 'tipo'){
      $('cajaOtro').classList.toggle('on', sel.tipo === 'otro');
      if (sel.tipo === 'otro') setTimeout(() => $('otroTexto').focus(), 120);
    }"""
nuevo4 = """    if (campo === 'tipo'){
      $('cajaOtro').classList.toggle('on', sel.tipo === 'otro');
      if (sel.tipo === 'otro') setTimeout(() => $('otroTexto').focus(), 120);
    }
    /* si marca una fatalidad, sale el texto de respeto */
    if (campo === 'gravedad' && $('cajaFatalidad')){
      $('cajaFatalidad').classList.toggle('on', sel.gravedad === 'fatalidad');
    }"""
if viejo4 in s: s = s.replace(viejo4, nuevo4); toc += 1
else: print('  NO ENCUENTRO el pintaOps')

# ---------- 6) el CSS de la caja ----------
viejo5 = """  /* cuando eliges "otro", te pido que digas cual: si no, no hay dato */"""
nuevo5 = """  /* al marcar una fatalidad: un texto de respeto, sin dramatismo */
  .cajaFatalidad{display:none;margin-top:10px;background:#eef1f3;border-radius:10px;
    padding:13px;border-left:3px solid #33424a;gap:11px;align-items:flex-start}
  .cajaFatalidad.on{display:flex}
  .cajaFatalidad .mso{color:#33424a;font-size:20px;flex-shrink:0;margin-top:1px}
  .cajaFatalidad div{font-size:12.5px;line-height:1.6;color:#2c3d45}

  /* cuando eliges "otro", te pido que digas cual: si no, no hay dato */"""
if viejo5 in s: s = s.replace(viejo5, nuevo5); toc += 1
else: print('  NO ENCUENTRO el CSS de cajaOtro')

# ---------- 7) limpiar la caja al enviar ----------
viejo6 = """    $('cajaOtro').classList.remove('on');"""
nuevo6 = """    $('cajaOtro').classList.remove('on');
    $('cajaFatalidad').classList.remove('on');"""
if viejo6 in s: s = s.replace(viejo6, nuevo6); toc += 1
else: print('  NO ENCUENTRO la limpieza')

# ---------- 8) en los patrones: un bloque de gravedad ----------
viejo7 = """  if (Object.keys(porFranja).length) html += bloque('A qué hora del día', 'schedule',"""
nuevo7 = """  /* la gravedad: aqui se ve si los incidentes son sustos o algo peor.
     Es el dato que mas enseña, y el que hay que mirar sin morbo. */
  const porGrav = {};
  incidentes.forEach(i => { if (i.gravedad) porGrav[i.gravedad] = (porGrav[i.gravedad] || 0) + 1; });
  if (Object.keys(porGrav).length) html += bloque('Cómo acabaron', 'monitor_heart',
    'del susto a lo peor: mirarlo sin morbo, para aprender',
    ['sin','leves','danos','graves','fatalidad']
      .filter(k => porGrav[k])
      .map(k => [(GRAV.find(g => g.id === k) || {}).n || k, porGrav[k]]));

  if (Object.keys(porFranja).length) html += bloque('A qué hora del día', 'schedule',"""
if viejo7 in s: s = s.replace(viejo7, nuevo7); toc += 1
else: print('  NO ENCUENTRO los patrones de franja')

# ---------- 9) el color del punto en el mapa, para la fatalidad ----------
viejo8 = """      const col = i.gravedad === 'graves' ? '#b5544a'
                : (i.gravedad === 'sin' ? '#2f7d4f' : '#c98a24');"""
nuevo8 = """      const col = i.gravedad === 'fatalidad' ? '#33424a'
                : (i.gravedad === 'graves' ? '#b5544a'
                : (i.gravedad === 'sin' ? '#2f7d4f' : '#c98a24'));"""
if viejo8 in s: s = s.replace(viejo8, nuevo8); toc += 1
else: print('  NO ENCUENTRO el color del punto (mapa principal)')

viejo9 = """      const col = i.gravedad === 'graves' ? '#b5544a'
              : (i.gravedad === 'sin' ? '#2f7d4f' : '#c98a24');"""
nuevo9 = """      const col = i.gravedad === 'fatalidad' ? '#33424a'
              : (i.gravedad === 'graves' ? '#b5544a'
              : (i.gravedad === 'sin' ? '#2f7d4f' : '#c98a24'));"""
if viejo9 in s: s = s.replace(viejo9, nuevo9); toc += 1
else: print('  NO ENCUENTRO el color del punto (mini mapa)')

# ---------- 10) el borde de la tarjeta ----------
viejo10 = """  .inc.graves{border-left-color:var(--grave)}"""
nuevo10 = """  .inc.graves{border-left-color:var(--grave)}
  .inc.fatalidad{border-left-color:#33424a}"""
if viejo10 in s: s = s.replace(viejo10, nuevo10); toc += 1
else: print('  NO ENCUENTRO el borde de la tarjeta')

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc, '/ 10')
print('  archivo:', len(s), 'bytes')
print()
print('  quedan menciones a NearMiss:', s.count('NearMiss'))
