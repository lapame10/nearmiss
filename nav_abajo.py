#!/usr/bin/env python3
"""LA SOLUCION DE VERDAD al movil: la navegacion se va ABAJO.

Pam: 'ahora se ve peor'. Y tenia razon: llevaba tres parches intentando meter
4 cosas (nombre + nav de 3 + selector de idioma + lema) en 390 px, y en los
nombres largos de frances/aleman no cabe de ninguna manera. El texto se
solapaba.

En vez de seguir apretando, se hace lo que hacen TODAS las apps de verdad:
- La cabecera de arriba se queda con el nombre y el idioma.
- La navegacion (Mapa / Reportar / Patrones) se va a una barra FIJA ABAJO,
  con el icono y su texto debajo. Siempre cabe, en cualquier idioma.
- Es ademas mas comodo: en un movil se llega con el pulgar a lo de abajo,
  no a lo de arriba.
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


# ---------- 1) el selector de idioma SALE del nav, a la cabecera ----------
rep("""  <nav class="nav">
    <select id="bIdioma" class="idioma" aria-label="Language" title="Idioma / Language">""",
    """  <nav class="nav">
    <select id="bIdioma" class="idiomaSuelto" aria-label="Language" title="Idioma / Language">""")

# lo saco del nav y lo pongo en la cabecera, antes del nav
ini = s.find('    <select id="bIdioma" class="idiomaSuelto"')
fin = s.find('</select>', ini) + len('</select>\n')
sel_html = s[ini:fin]
s = s[:ini] + s[fin:]
# quito la indentacion de dentro del nav
sel_html = sel_html.replace('\n      ', '\n    ').replace('\n    </select>', '\n  </select>')

# y lo pongo entre la marca y el nav
rep("""  <nav class="nav">""", sel_html + """  <nav class="nav">""")
toc += 1

# ---------- 2) el CSS: en movil, el nav abajo ----------
rep("""  /* La cabecera es lo que peor se porta en pantallas estrechas: compiten el
     nombre, el nav de 3 botones y el selector de idioma. Y con los idiomas
     largos (Signaler, Tendances) no cabe: los textos se solapaban con los
     iconos. Solucion: en el nav, SOLO ICONOS, excepto el boton ACTIVO, que
     enseña su texto. Asi sabes donde estas y los tres caben siempre. */
  @media(max-width:820px){
    .nav{gap:1px}
    .nav button{padding:9px 10px;font-size:12.5px;gap:0}
    .nav button>span:not(.mso){display:none}
    .nav button.on{gap:6px;padding:9px 12px}
    .nav button.on>span:not(.mso){display:inline}
    .nav select.idioma{padding:6px 4px;padding-right:15px;font-size:11.5px;
      background-position:right 4px center}
    .nav button{padding:9px 8px}
    .marca{font-size:15.5px}
    .marca .pico{height:25px}
  }""",
    """  /* ==========================================================================
     EN MÓVIL LA NAVEGACIÓN SE VA ABAJO
     --------------------------------------------------------------------------
     Arriba competían cuatro cosas por 390 px (nombre, nav de 3 botones,
     selector de idioma y lema) y con los idiomas largos —Signaler, Tendances,
     Melden— el texto se solapaba. Se apretó tres veces y no hubo manera.
     Así que se hace como las apps de verdad: la navegación, en una barra fija
     abajo. Cabe siempre, en cualquier idioma, y además se llega con el pulgar.
     ========================================================================== */
  @media(max-width:820px){
    .cab{gap:10px}
    .marca{margin-right:auto}
    .nav{position:fixed;left:0;right:0;bottom:0;z-index:1800;
      background:var(--marino);border-top:1px solid rgba(255,255,255,.16);
      display:flex;justify-content:space-around;align-items:stretch;
      margin:0;gap:0;
      padding:6px 6px calc(6px + env(safe-area-inset-bottom))}
    .nav button{flex:1;flex-direction:column;gap:2px;padding:7px 4px;
      font-size:10.5px;font-weight:700;border-radius:10px;justify-content:center}
    .nav button .mso{font-size:22px}
    /* el texto vuelve: abajo hay sitio de sobra */
    .nav button>span:not(.mso){display:inline;white-space:nowrap}
    .nav button.on{background:rgba(255,255,255,.14)}
    /* y el cuerpo deja hueco para que la barra no tape el final de la pagina */
    body{padding-bottom:calc(72px + env(safe-area-inset-bottom))}
    /* el aviso no puede quedar debajo de la barra */
    .aviso{z-index:2600}
  }""")

# ---------- 3) el selector de idioma, ahora suelto en la cabecera ----------
rep("""  /* el selector de idioma: 5 idiomas, discreto, a la derecha del todo */
  .nav select.idioma{background:rgba(255,255,255,.1);color:#fff;border:1px solid rgba(255,255,255,.3);""",
    """  /* el selector de idioma: 5 idiomas, discreto, en la cabecera */
  select.idiomaSuelto{background:rgba(255,255,255,.1);color:#fff;border:1px solid rgba(255,255,255,.3);""")

rep("""  .nav select.idioma option{background:var(--marino);color:#fff}""",
    """  select.idiomaSuelto option{background:var(--marino);color:#fff}""")

# en pantallas estrechas, un poco mas pequeño pero sin desaparecer
rep("""  @media(max-width:640px){
    .cab{padding:0 12px;gap:9px;height:54px}""",
    """  @media(max-width:640px){
    .cab{padding:0 12px;gap:9px}
    select.idiomaSuelto{padding:6px 4px;padding-right:15px;font-size:11.5px;
      background-position:right 4px center}""")

# ---------- 4) el nav dejo de ser sticky dentro de la cabecera: quito el height fijo ----------
rep("""  .cab{background:var(--marino);color:#fff;padding:0 24px;
    display:flex;align-items:center;gap:26px;height:60px;position:sticky;top:0;z-index:1500}""",
    """  .cab{background:var(--marino);color:#fff;padding:0 24px;
    display:flex;align-items:center;gap:20px;height:60px;position:sticky;top:0;z-index:1500}""")

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
