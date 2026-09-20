#!/usr/bin/env python3
"""Arregla el nav de la cabecera, que se aplasta.

Pam dijo 'en el celular se ve mal' y al probar el frances vi la causa exacta:
con 3 botones (Carte / Signaler / Tendances), el selector de idioma, el nombre y
el subtitulo, la cabecera no cabe. Los textos se solapan con los iconos.

Solucion:
- El subtitulo se oculta antes (era lo que mas pesaba)
- Y en movil, los botones del nav ensenan SOLO EL ICONO, menos el activo, que
  ensena su texto: asi sabes donde estas y los otros tres caben siempre.
"""
RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0


def rep(v, n):
    global s, toc
    if v in s:
        s = s.replace(v, n); toc += 1
        return True
    print('  NO ENCUENTRO:', v[:70].replace('\n', ' | '))
    return False


# ---------- 1) el corte del subtitulo, antes ----------
rep("""  /* por debajo de 1180 el subtítulo de la cabecera ya no cabe con el nav:
     se quita el subtítulo (el hero ya explica lo mismo) antes que cortar
     los botones del nav. */
  @media(max-width:1179px){
    .marcaTxt{display:none}
  }""",
    """  /* El subtítulo de la cabecera es lo primero que sobra: el hero ya dice lo
     mismo. Y con los idiomas largos (Signaler, Tendances) hace falta el sitio
     antes. Por eso se quita ya a los 1400px. */
  @media(max-width:1400px){
    .marcaTxt{display:none}
  }
  @media(max-width:1150px){
    .cabDer{display:none}
  }""")

# ---------- 2) el nav no se aplasta nunca ----------
rep("""  .nav button .mso{font-size:19px}""",
    """  .nav button .mso{font-size:19px}
  /* el nav NUNCA se encoge: si no cabe, se quitan los textos (abajo), no se
     aplastan los botones uno contra otro */
  .nav button>span:not(.mso){white-space:nowrap}""")

# ---------- 3) en movil: solo iconos, menos el activo ----------
rep("""  /* ===================== MOVIL ===================== */
  @media(max-width:640px){""",
    """  /* ===================== MOVIL ===================== */
  /* La cabecera es lo que peor se porta en un movil: 5 cosas compitiendo por
     390 px (nombre, subtitulo, nav de 3, selector de idioma, lema). Solucion:
     en el nav solo ICONOS, y el boton ACTIVO enseña su texto. Asi sabes donde
     estas y los otros dos caben siempre, en cualquier idioma. */
  @media(max-width:820px){
    .nav{gap:1px}
    .nav button{padding:9px 10px;font-size:12.5px;gap:0}
    .nav button>span:not(.mso){display:none}
    .nav button.on{gap:6px;padding:9px 12px}
    .nav button.on>span:not(.mso){display:inline}
    .nav select.idioma{padding:7px 6px;padding-right:19px;font-size:11.5px}
  }

  @media(max-width:640px){""")

# ---------- 4) en movil muy pequeño, el nombre tambien se acorta ----------
rep("""    .marca{font-size:17px}
    .marca .pico{height:29px}""",
    """    .marca{font-size:16.5px;gap:7px}
    .marca .pico{height:27px}""")

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
