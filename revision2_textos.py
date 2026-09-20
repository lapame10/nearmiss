#!/usr/bin/env python3
"""Las correcciones de texto de Pam (revision 2).

1) 'De un susto a lo peor' -> demasiado coloquial para el tono del sitio
2) 'El dato real del viento lo saco yo' -> promete mas de lo que se puede saber
3) CONTRADICCION DEL IGC: habia una casilla 'borrar el track' Y se decia que el
   archivo 'no se queda'. Si siempre se borra, la casilla sobra. Se quita.
4) Los tres ceros parecen plataforma abandonada: se esconden
5) Los 10 pasos: agruparlos en 3 bloques (Evento / Contexto / Informacion)
6) Los ~100 m: no prometer 'poco para senalar a nadie'
"""
RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0


def rep(v, n):
    global s, toc
    if v in s:
        s = s.replace(v, n); toc += 1
        return True
    print('  NO ENCUENTRO:', v[:72].replace('\n', ' | '))
    return False


# ---------- 1) "De un susto a lo peor" ----------
rep("c1a: 'De un susto a lo peor. Esto clasifica el evento.',",
    "c1a: 'Clasifica el nivel del evento, desde un casi accidente hasta una fatalidad.',")
rep("c1a: 'From a close call to the worst. This classifies the event.',",
    "c1a: 'Sets the level of the event, from a near miss to a fatality.',")

# ---------- 2) el viento ----------
rep("c8a: 'Lo que tú sentiste. El dato real del viento lo saco yo.',",
    "c8a: 'Lo que tú sentiste. Si indicas fecha y ubicación, SkyReport puede '\n"
    "       + 'complementar el reporte con datos meteorológicos registrados de esa zona.',")
rep("c8a: 'What you felt. I work out the real wind myself.',",
    "c8a: 'What you felt. If you give the date and location, SkyReport can add '\n"
    "       + 'recorded weather data for that area.',")

# ---------- 3) LA CONTRADICCION DEL IGC ----------
# fuera la casilla: si el archivo se elimina siempre, no hay nada que elegir
rep("""              <label class="marcaCheck">
                <input type="checkbox" id="borrarTrack" checked>
                <span data-i18n="igcBorrar"></span>
              </label>
""", """              <div class="igcNota"><span class="mso">delete_sweep</span>
                <span data-i18n="igcNota"></span></div>
""")
rep("    igcBorrar: 'Borrar el track después de procesarlo',",
    "    igcNota: 'El archivo se elimina automáticamente después de extraer los datos '\n"
    "           + 'necesarios: la hora del vuelo y la altura máxima. No se guarda ni se '\n"
    "           + 'publica en ningún caso.',")
rep("    igcBorrar: 'Delete the track after processing it',",
    "    igcNota: 'The file is deleted automatically after extracting the data we need: '\n"
    "           + 'the flight time and the maximum altitude. It is never stored or '\n"
    "           + 'published.',")

# y el texto de la pregunta 9, mas claro
rep("c9a: 'Un IGC identifica un vuelo concreto. Lee esto antes.',",
    "c9a: 'Un IGC identifica un vuelo concreto. Lee cómo se trata antes de subirlo.',")
rep("c9a: 'An IGC identifies one specific flight. Read this first.',",
    "c9a: 'An IGC identifies one specific flight. Read how it is handled before uploading.',")

# el CSS de la nota
rep("""  /* el check del IGC */
  .marcaCheck{display:flex;align-items:center;gap:9px;margin-top:11px;
    font-size:12.5px;color:#2b4750;cursor:pointer;line-height:1.4}
  .marcaCheck input{width:18px;height:18px;accent-color:var(--mar);flex-shrink:0}
  .marcaCheck span{font-weight:600}""",
    """  /* la nota del IGC: dice que el archivo se borra solo, sin casilla que marcar */
  .igcNota{display:flex;gap:9px;align-items:flex-start;margin-top:11px;
    font-size:12.5px;color:#2b4750;line-height:1.5}
  .igcNota .mso{font-size:19px;color:var(--mar);flex-shrink:0;margin-top:1px}
  .igcNota span:last-child{flex:1}""")

# ---------- 4) QUITAR LA PROMESA DE LOS 100 m ----------
rep("c5a: 'Toca la zona en el mapa. Se guarda redondeado a ~100 m: '\n"
    "                     + 'suficiente para ver patrones, poco para señalar a nadie.',",
    "c5a: 'Toca la zona en el mapa. La ubicación pública se muestra de forma '\n"
    "                     + 'aproximada, para reducir la posibilidad de identificar al piloto.',")
rep("c5a: 'Tap the area on the map. It is stored rounded to ~100 m: '\n"
    "                     + 'enough to see patterns, too little to point at anyone.',",
    "c5a: 'Tap the area on the map. The public location is shown only approximately, '\n"
    "                     + 'to reduce the chance of identifying the pilot.',")

rep("""    privacidad: '<b>Qué se publica y qué no.</b><br><b>Se publica:</b> el mes y el año, '
              + 'la zona redondeada, la franja del día, la situación y las consecuencias.'
              + '<br><b>No se publica nunca:</b> tu nombre, el día exacto, la hora exacta, '
              + 'tu posición precisa, ni el archivo IGC. El archivo se usa solo para leer '
              + 'las condiciones del vuelo y no se queda.',""",
    """    privacidad: '<b>Qué se publica y qué no.</b><br><b>Se publica:</b> el mes y el año, '
              + 'la ubicación aproximada, la franja del día, la situación y las consecuencias.'
              + '<br><b>No se publica nunca:</b> tu nombre, el día exacto, la hora exacta, '
              + 'tu posición precisa, ni el archivo IGC. El archivo se usa solo para leer '
              + 'las condiciones del vuelo y se elimina en el momento.',""")

rep("""    privTexto: 'No pedimos tu nombre, ni tu teléfono, ni tu correo.<br><br>La ubicación '
             + 'se <b>redondea a unos 100 metros</b>, así que no señala un punto exacto.'
             + '<br><br>El <b>día</b> que pongas se usa solo para calcular el viento de '""",
    """    privTexto: 'No pedimos tu nombre, ni tu teléfono, ni tu correo.<br><br>La ubicación '
             + 'que se publica es <b>aproximada</b>. En un despegue remoto, con la fecha y '
             + 'las circunstancias, eso todavía podría ser identificable — por eso pedimos '
             + 'también que no pongas detalles que señalen a una persona.'
             + '<br><br>El <b>día</b> que pongas se usa solo para calcular el viento de '""")

# ---------- 5) LOS TRES CONTADORES: fuera los ceros ----------
rep("""        <div class="stat"><span class="mso">description</span>
          <div class="n" id="nReportes">0</div><div class="t" id="tReportes">eventos</div></div>
        <div class="stat"><span class="mso">place</span>
          <div class="n" id="nSitios">0</div><div class="t" id="tSitios">sitios</div></div>
        <div class="stat"><span class="mso">insights</span>
          <div class="n" id="nPatrones">0</div><div class="t" id="tPatronesTxt">patrones</div></div>""",
    """        <div class="stat" id="stEventos"><span class="mso">description</span>
          <div class="n" id="nReportes">0</div><div class="t" id="tReportes">eventos</div></div>
        <div class="stat" id="stSitios"><span class="mso">place</span>
          <div class="n" id="nSitios">0</div><div class="t" id="tSitios">sitios</div></div>
        <div class="stat" id="stPatrones"><span class="mso">insights</span>
          <div class="n" id="nPatrones">0</div><div class="t" id="tPatronesTxt">patrones</div></div>""")

rep("""          <div class="stats">
        <div class="stat" id="stEventos">""",
    """          <div class="stats" id="filaStats">
        <div class="stat" id="stEventos">""")

# el mensaje de "esto acaba de empezar", para cuando no hay nada
rep("""          <div class="stats" id="filaStats">""",
    """          <div class="empezando" id="empezando">
            <span class="mso">eco</span>
            <div data-i18n="empezando"></div>
          </div>
          <div class="stats" id="filaStats">""")

rep("""        <div class="stat" id="stEventos"><span class="mso">description</span>
          <div class="n" id="nReportes">0</div><div class="t" id="tReportes">eventos</div></div>
        <div class="stat" id="stSitios"><span class="mso">place</span>
          <div class="n" id="nSitios">0</div><div class="t" id="tSitios">sitios</div></div>
        <div class="stat" id="stPatrones"><span class="mso">insights</span>
          <div class="n" id="nPatrones">0</div><div class="t" id="tPatronesTxt">patrones</div></div>
      </div>""",
    """        <div class="stat" id="stEventos"><span class="mso">description</span>
          <div class="n" id="nReportes">0</div><div class="t" id="tReportes">eventos</div></div>
        <div class="stat" id="stSitios"><span class="mso">place</span>
          <div class="n" id="nSitios">0</div><div class="t" id="tSitios">sitios</div></div>
        <div class="stat" id="stPatrones"><span class="mso">insights</span>
          <div class="n" id="nPatrones">0</div><div class="t" id="tPatronesTxt">patrones</div></div>
      </div>
      <div class="empezando" id="empezando" style="display:none">
        <span class="mso">eco</span>
        <div data-i18n="empezando"></div>
      </div>""")

# fuera el bloque duplicado que puse arriba
rep("""          <div class="empezando" id="empezando">
            <span class="mso">eco</span>
            <div data-i18n="empezando"></div>
          </div>
          <div class="stats" id="filaStats">""", """          <div class="stats" id="filaStats">""")

# ---------- 6) la logica de esconder los ceros ----------
rep("""    /* singular o plural, que '1 patrones' se ve muy mal */
    const uno = n => n === 1;""",
    """    /* singular o plural, que '1 patrones' se ve muy mal */
    const uno = n => n === 1;
    /* Pam: los ceros parecen una plataforma abandonada. Un contador a 0 no se
       enseña, y si no hay NADA se dice que esto acaba de empezar. */
    const verStat = (id, v) => {
      const n = $(id);
      if (n) n.style.display = v > 0 ? '' : 'none';
    };""")

rep("""    $('tPatronesTxt').textContent = uno(nPat) ? t('evPatron') : t('evPatrones');""",
    """    $('tPatronesTxt').textContent = uno(nPat) ? t('evPatron') : t('evPatrones');

    /* escondo los contadores que estan a cero, y si no hay nada lo digo */
    verStat('stEventos', incidentes.length);
    verStat('stSitios', sitios.size);
    verStat('stPatrones', nPat);
    const vacio = (incidentes.length === 0);
    if ($('empezando')) $('empezando').style.display = vacio ? 'flex' : 'none';
    if ($('filaStats')) $('filaStats').style.display = vacio ? 'none' : '';""")

# las dos claves nuevas
rep("    evSitios: 'sitios', evSitio: 'sitio',",
    "    evSitios: 'sitios', evSitio: 'sitio',\n"
    "    empezando: 'La base de conocimiento está empezando.<br>Cada reporte ayuda a construirla.',")
rep("    evSitios: 'sites', evSitio: 'site',",
    "    evSitios: 'sites', evSitio: 'site',\n"
    "    empezando: 'The knowledge base is just starting.<br>Every report helps build it.',")

# el CSS del aviso
rep("""  /* el check del IGC */""", """  /* cuando todavia no hay nada: no ensenar tres ceros, decir que empieza */
  .empezando{display:none;gap:11px;align-items:flex-start;background:#f2f6f8;
    border-radius:11px;padding:14px;font-size:12.5px;line-height:1.55;color:#3b5560}
  .empezando .mso{color:var(--mar);font-size:20px;flex-shrink:0;margin-top:1px}

  /* el check del IGC */""")

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
print('  ¿queda la casilla de borrar?', 'borrarTrack' in s)
