#!/usr/bin/env python3
"""PARTE B: marcar los textos del HTML, el boton y la deteccion automatica."""
RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0


def rep(v, n, critico=True):
    global s, toc
    if v in s:
        s = s.replace(v, n); toc += 1
        return True
    if critico:
        print('  NO ENCUENTRO:', v[:72].replace('\n', ' | '))
    return False


# ==========================================================================
# 1) LOS TEXTOS DEL HTML, marcados con data-i18n
# ==========================================================================
textos = [
    # cabecera: el boton de idioma va aqui
    ('<nav class="nav">',
     '<nav class="nav">\n'
     '    <button id="bIdioma" class="idioma" aria-label="Language">🌐 <span id="idTxt">ES</span></button>'),

    ('<div class="cabDer">Una comunidad<br>por vuelos más seguros</div>',
     '<div class="cabDer" data-i18n="lema"></div>'),

    ('<button id="tMapa"><span class="mso">map</span>Mapa</button>',
     '<button id="tMapa"><span class="mso">map</span><span data-i18n="navMapa">Mapa</span></button>'),
    ('<button id="tReportar" class="on"><span class="mso">edit_note</span>Reportar</button>',
     '<button id="tReportar" class="on"><span class="mso">edit_note</span><span data-i18n="navReportar">Reportar</span></button>'),
    ('<button id="tPatrones"><span class="mso">bar_chart</span>Patrones</button>',
     '<button id="tPatrones"><span class="mso">bar_chart</span><span data-i18n="navPatrones">Patrones</span></button>'),

    # portada
    ('<h1>Seguridad compartida. Aprendizaje colectivo.</h1>',
     '<h1 data-i18n="heroTitulo">Seguridad compartida. Aprendizaje colectivo.</h1>'),
    ('<p>Aquí puedes reportar de forma anónima eventos de parapente.<br>\n    No buscamos culpables, buscamos aprender para que todos volvamos a volar.</p>',
     '<p data-i18n="heroTexto"></p>'),
    ('<div class="cita">\n      <b>“Cada experiencia cuenta.</b>\n      Un vuelo más seguro empieza con compartir lo que ocurrió.”\n    </div>',
     '<div class="cita" data-i18n="heroCita"></div>'),

    # formulario
    ('<h2>Reportar un evento</h2>', '<h2 data-i18n="formTitulo">Reportar un evento</h2>'),
    ('<span class="avisoTop">Todo es anónimo. Los campos marcados son obligatorios.</span>',
     '<span class="avisoTop" data-i18n="formAviso"></span>'),

    ('<h3>¿Qué ocurrió?</h3>', '<h3 data-i18n="c1t">¿Qué ocurrió?</h3>'),
    ('<p class="campoAyuda">De un susto a lo peor. Esto clasifica el evento.</p>',
     '<p class="campoAyuda" data-i18n="c1a"></p>'),
    ('<h3>¿Qué pasó?</h3>', '<h3 data-i18n="c2t">¿Qué pasó?</h3>'),
    ('<p class="campoAyuda">La situación concreta. Es lo que permite ver patrones después.</p>',
     '<p class="campoAyuda" data-i18n="c2a"></p>'),
    ('<h3>Consecuencias</h3>', '<h3 data-i18n="c3t">Consecuencias</h3>'),
    ('<p class="campoAyuda">El resultado concreto.</p>',
     '<p class="campoAyuda" data-i18n="c3a"></p>'),
    ('<h3>Fase del vuelo</h3>', '<h3 data-i18n="c4t">Fase del vuelo</h3>'),
    ('<p class="campoAyuda">¿En qué momento del vuelo?</p>',
     '<p class="campoAyuda" data-i18n="c4a"></p>'),
    ('<h3>Dónde</h3>', '<h3 data-i18n="c5t">Dónde</h3>'),
    ('<p class="campoAyuda">Toca la zona en el mapa. Se guarda redondeado a ~100 m:\n            suficiente para ver patrones, poco para señalar a nadie.</p>',
     '<p class="campoAyuda" data-i18n="c5a"></p>'),
    ('<h3>Cuándo</h3>', '<h3 data-i18n="c6t">Cuándo</h3>'),
    ('<p class="campoAyuda">Con el día saco el viento real que hacía ahí.\n            <b>El día no se publica</b>: se guarda el mes y el año.</p>',
     '<p class="campoAyuda" data-i18n="c6a"></p>'),
    ('<h3>Franja del día</h3>', '<h3 data-i18n="c7t">Franja del día</h3>'),
    ('<p class="campoAyuda">Se publica la franja, nunca la hora.</p>',
     '<p class="campoAyuda" data-i18n="c7a"></p>'),
    ('<h3>Cómo estaba el aire</h3>', '<h3 data-i18n="c8t">Cómo estaba el aire</h3>'),
    ('<p class="campoAyuda">Lo que tú sentiste. El dato real del viento lo saco yo.</p>',
     '<p class="campoAyuda" data-i18n="c8a"></p>'),
    ('<h3>Tu archivo de vuelo</h3>', '<h3 data-i18n="c9t">Tu archivo de vuelo</h3>'),
    ('<p class="campoAyuda">Un IGC identifica un vuelo concreto. Lee esto antes.</p>',
     '<p class="campoAyuda" data-i18n="c9a"></p>'),
    ('<h3>Cuéntalo</h3>', '<h3 data-i18n="c10t">Cuéntalo</h3>'),
    ('<p class="campoAyuda">Sin nombres. El detalle que identifica a alguien, fuera;\n          el que explica lo que pasó, dentro.</p>',
     '<p class="campoAyuda" data-i18n="c10a"></p>'),

    ('<span class="etq req">obligatorio</span>', '<span class="etq req" data-i18n="obligatorio"></span>'),
    ('<span class="etq opc">opcional</span>', '<span class="etq opc" data-i18n="opcional"></span>'),

    ('<label>¿Cuál? Cuéntalo en una línea</label>',
     '<label data-i18n="otroTitulo"></label>'),
    ('placeholder="Ej: enganche con el arnés · objetivo en el aire · nudo en el freno">',
     'data-i18n-ph="otroEjemplo">'),

    ('<div>Gracias por contarlo. <b>Es el dato que más ayuda</b> a que no\n              vuelva a pasar.<br><br>\n              Cuéntalo <b>sin nombres</b> y sin detalles que no aporten aprendizaje.\n              Lo que importa es qué pasó y en qué condiciones, no quién.\n              <br><br>\n              <b>Las fatalidades no se publican al momento:</b> quedan pendientes de\n              verificación para que un error o un rumor no se convierta en un dato.</div>',
     '<div data-i18n="fatalTexto"></div>'),

    ('<button class="btnIgc" id="bIGC"><span class="mso">upload_file</span> Subir mi archivo IGC</button>',
     '<button class="btnIgc" id="bIGC"><span class="mso">upload_file</span> <span data-i18n="igcBoton">Subir mi archivo IGC</span></button>'),
    ('<span>Borrar el track después de procesarlo</span>',
     '<span data-i18n="igcBorrar"></span>'),
    ('placeholder="Escribe aquí tu relato (opcional)...">',
     'data-i18n-ph="relatoEjemplo">'),

    ('<div><b>Qué se publica y qué no.</b><br>\n          <b>Se publica:</b> el mes y el año, la zona redondeada, la franja del día,\n          la situación y las consecuencias.<br>\n          <b>No se publica nunca:</b> tu nombre, el día exacto, la hora exacta, tu\n          posición precisa, ni el archivo IGC. El archivo se usa solo para leer las\n          condiciones del vuelo y no se queda.</div>',
     '<div data-i18n="privacidad"></div>'),

    ('<span class="mso">send</span> Enviar evento anónimo',
     '<span class="mso">send</span> <span data-i18n="enviar">Enviar evento anónimo</span>'),

    # columna derecha
    ('<h3><span class="mso">verified_user</span> Principios</h3>',
     '<h3><span class="mso">verified_user</span> <span data-i18n="principios"></span></h3>'),
    ('<b>Seguridad antes que todo</b><span>Aprendemos de la experiencia real.</span>',
     '<b data-i18n="p1"></b><span data-i18n="p1s"></span>'),
    ('<b>Sin juicios, sin culpables</b><span>Esto no trata de señalar, sino de mejorar.</span>',
     '<b data-i18n="p2"></b><span data-i18n="p2s"></span>'),
    ('<b>Comunidad global</b><span>El conocimiento compartido hace nuestros vuelos más seguros.</span>',
     '<b data-i18n="p3"></b><span data-i18n="p3s"></span>'),
    ('<h3><span class="mso">lock</span> Anónimo por diseño</h3>',
     '<h3><span class="mso">lock</span> <span data-i18n="anonTitulo"></span></h3>'),
    ('<div style="font-size:12.5px;color:var(--gris);line-height:1.6">\n          No pedimos tu nombre, ni datos personales, ni información que pueda\n          identificarte. La ubicación es aproximada y los detalles se tratan con cuidado.\n        </div>',
     '<div style="font-size:12.5px;color:var(--gris);line-height:1.6" data-i18n="anonTexto"></div>'),
    ('<a class="enlace" href="#" id="masPrivacidad">Saber más sobre tu privacidad →</a>',
     '<a class="enlace" href="#" id="masPrivacidad"><span data-i18n="anonMas"></span> →</a>'),
    ('<h3><span class="mso">school</span> Qué aprendemos</h3>',
     '<h3><span class="mso">school</span> <span data-i18n="aprendeTitulo"></span></h3>'),
    ('<div style="font-size:12.5px;color:var(--gris);line-height:1.6">\n          Los eventos nos permiten identificar patrones, zonas de riesgo y\n          situaciones recurrentes para compartir aprendizajes con toda la comunidad.\n        </div>',
     '<div style="font-size:12.5px;color:var(--gris);line-height:1.6" data-i18n="aprendeTexto"></div>'),
    ('<a class="enlace" href="#" id="verPatrones">Ver patrones y análisis →</a>',
     '<a class="enlace" href="#" id="verPatrones"><span data-i18n="aprendeVer"></span> →</a>'),
    ('<h3><span class="mso">map</span> Actividad reciente en el mapa</h3>',
     '<h3><span class="mso">map</span> <span data-i18n="reciente"></span></h3>'),
    ('<a class="enlace" href="#" id="verMapa">Ver mapa completo →</a>',
     '<a class="enlace" href="#" id="verMapa"><span data-i18n="verMapaCompleto"></span> →</a>'),
    ('<div><b>Importante</b><br>SkyReport no es un canal de emergencia. Si necesitas\n        ayuda inmediata, contacta con los servicios de rescate locales.</div>',
     '<div data-i18n="emergencia"></div>'),

    # vistas
    ('<h2>Mapa de eventos</h2>', '<h2 data-i18n="mapaTitulo"></h2>'),
    ('<span class="sub">Cada punto es un evento. El calor muestra dónde se acumulan.</span>',
     '<span class="sub" data-i18n="mapaSub"></span>'),
    ('<h2>Patrones</h2>', '<h2 data-i18n="patronesTitulo"></h2>'),
    ('<span class="sub">Los eventos aislados cuentan historias. Juntos revelan patrones.</span>',
     '<span class="sub" data-i18n="patronesSub"></span>'),

    # pie
    ('<div>Reportes anónimos de incidentes y accidentes de parapente</div>',
     '<div data-i18n="pieTexto">Reportes anónimos de eventos de parapente</div>'),
    ('<button class="btn" id="avX">Entendido</button>',
     '<button class="btn" id="avX" data-i18n="entender">Entendido</button>'),
]

for v, n in textos:
    rep(v, n)

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios en el HTML:', toc)
print('  archivo:', len(s), 'bytes')
