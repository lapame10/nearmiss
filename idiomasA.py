#!/usr/bin/env python3
"""PARTE A: el motor de idiomas de SkyReport (Pam: 'un boton para cambiar
idioma, por que si queremos que sea para todo el mundo eso es super importante').

Que hace:
- Un objeto con todos los textos en cada idioma
- Los elementos del HTML llevan data-i18n="clave" y se rellenan solos
- Los arrays de opciones (gravedad, situacion...) llevan el nombre en cada idioma
- Boton en la cabecera, deteccion automatica del navegador y memoria en el movil
"""
RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0


def rep(v, n):
    global s, toc
    if v in s:
        s = s.replace(v, n); toc += 1
        return True
    print('  NO ENCUENTRO:', v[:75].replace('\n', ' | '))
    return False


# ==========================================================================
# 1) EL MOTOR: textos en cada idioma
# ==========================================================================
rep("""const FIRE = 'https://plan-gym-8aff7-default-rtdb.firebaseio.com';
const $ = id => document.getElementById(id);""",
    """const FIRE = 'https://plan-gym-8aff7-default-rtdb.firebaseio.com';
const $ = id => document.getElementById(id);

/* ==========================================================================
   LOS IDIOMAS (idea de Pam)
   --------------------------------------------------------------------------
   'Si queremos que sea para todo el mundo eso es super importante'.
   El español va primero porque es el idioma en que se piensa esto, pero el
   inglés es el que hace que un piloto de Suiza o de Brasil lo pueda usar.
   Añadir otro idioma = copiar un bloque y traducirlo. Nada mas.
   ========================================================================== */
const TXT = {
  es: {
    /* cabecera */
    lema: 'Una comunidad<br>por vuelos más seguros',
    navMapa: 'Mapa', navReportar: 'Reportar', navPatrones: 'Patrones',
    /* portada */
    heroTitulo: 'Seguridad compartida. Aprendizaje colectivo.',
    heroTexto: 'Aquí puedes reportar de forma anónima eventos de parapente.<br>'
             + 'No buscamos culpables, buscamos aprender para que todos volvamos a volar.',
    heroCita: '<b>“Cada experiencia cuenta.</b> Un vuelo más seguro empieza con '
            + 'compartir lo que ocurrió.”',
    /* el formulario */
    formTitulo: 'Reportar un evento',
    formAviso: 'Todo es anónimo. Los campos marcados son obligatorios.',
    c1t: '¿Qué ocurrió?', c1a: 'De un susto a lo peor. Esto clasifica el evento.',
    c2t: '¿Qué pasó?', c2a: 'La situación concreta. Es lo que permite ver patrones después.',
    c3t: 'Consecuencias', c3a: 'El resultado concreto.',
    c4t: 'Fase del vuelo', c4a: '¿En qué momento del vuelo?',
    c5t: 'Dónde', c5a: 'Toca la zona en el mapa. Se guarda redondeado a ~100 m: '
                     + 'suficiente para ver patrones, poco para señalar a nadie.',
    c6t: 'Cuándo', c6a: 'Con el día saco el viento real que hacía ahí. '
                      + '<b>El día no se publica</b>: se guarda el mes y el año.',
    c7t: 'Franja del día', c7a: 'Se publica la franja, nunca la hora.',
    c8t: 'Cómo estaba el aire', c8a: 'Lo que tú sentiste. El dato real del viento lo saco yo.',
    c9t: 'Tu archivo de vuelo', c9a: 'Un IGC identifica un vuelo concreto. Lee esto antes.',
    c10t: 'Cuéntalo', c10a: 'Sin nombres. El detalle que identifica a alguien, fuera; '
                          + 'el que explica lo que pasó, dentro.',
    obligatorio: 'obligatorio', opcional: 'opcional',
    otroTitulo: '¿Cuál? Cuéntalo en una línea',
    otroEjemplo: 'Ej: enganche con el arnés · objetivo en el aire · nudo en el freno',
    fatalTexto: '<b>Gracias por contarlo.</b> Es el dato que más ayuda a que no vuelva '
              + 'a pasar.<br><br>Cuéntalo <b>sin nombres</b> y sin detalles que no '
              + 'aporten aprendizaje. Lo que importa es qué pasó y en qué condiciones, '
              + 'no quién.<br><br><b>Las fatalidades no se publican al momento:</b> '
              + 'quedan pendientes de verificación para que un error o un rumor no se '
              + 'convierta en un dato.',
    igcBoton: 'Subir mi archivo IGC',
    igcBorrar: 'Borrar el track después de procesarlo',
    relatoEjemplo: 'Escribe aquí tu relato (opcional)...',
    privacidad: '<b>Qué se publica y qué no.</b><br><b>Se publica:</b> el mes y el año, '
              + 'la zona redondeada, la franja del día, la situación y las consecuencias.'
              + '<br><b>No se publica nunca:</b> tu nombre, el día exacto, la hora exacta, '
              + 'tu posición precisa, ni el archivo IGC. El archivo se usa solo para leer '
              + 'las condiciones del vuelo y no se queda.',
    enviar: 'Enviar evento anónimo',
    /* los contadores y la columna derecha */
    evEventos: 'eventos', evEvento: 'evento',
    evSitios: 'sitios', evPatrones: 'patrones', evPatron: 'patrón',
    principios: 'Principios',
    p1: 'Seguridad antes que todo', p1s: 'Aprendemos de la experiencia real.',
    p2: 'Sin juicios, sin culpables', p2s: 'Esto no trata de señalar, sino de mejorar.',
    p3: 'Comunidad global', p3s: 'El conocimiento compartido hace nuestros vuelos más seguros.',
    anonTitulo: 'Anónimo por diseño',
    anonTexto: 'No pedimos tu nombre, ni datos personales, ni información que pueda '
             + 'identificarte. La ubicación es aproximada y los detalles se tratan con cuidado.',
    anonMas: 'Saber más sobre tu privacidad',
    aprendeTitulo: 'Qué aprendemos',
    aprendeTexto: 'Los eventos nos permiten identificar patrones, zonas de riesgo y '
                + 'situaciones recurrentes para compartir aprendizajes con toda la comunidad.',
    aprendeVer: 'Ver patrones y análisis',
    reciente: 'Actividad reciente en el mapa',
    verMapaCompleto: 'Ver mapa completo',
    emergencia: '<b>Importante</b><br>SkyReport no es un canal de emergencia. Si '
              + 'necesitas ayuda inmediata, contacta con los servicios de rescate locales.',
    /* las vistas */
    mapaTitulo: 'Mapa de eventos',
    mapaSub: 'Cada punto es un evento. El calor muestra dónde se acumulan.',
    patronesTitulo: 'Patrones',
    patronesSub: 'Los eventos aislados cuentan historias. Juntos revelan patrones.',
    todos: 'Todos',
    /* avisos */
    faltaTitulo: 'Falta algún dato', faltaTexto: 'Necesito: ',
    faltaFin: '.<br><br>Son 30 segundos y con eso ya sirve.',
    graciasTitulo: 'Gracias. Ya está dentro.',
    graciasTexto: 'Lo que has contado puede evitar que otro pase por lo mismo.',
    graciasViento: 'Y he guardado el viento real de ese día: ',
    graciasFin: 'Puedes reportar todos los que quieras: <b>los sustos también cuentan</b>.',
    errorTitulo: 'No se pudo enviar',
    errorTexto: 'Revisa tu conexión e inténtalo otra vez.',
    privTitulo: 'Privacidad',
    privTexto: 'No pedimos tu nombre, ni tu teléfono, ni tu correo.<br><br>La ubicación '
             + 'se <b>redondea a unos 100 metros</b>, así que no señala un punto exacto.'
             + '<br><br>El <b>día</b> que pongas se usa solo para calcular el viento de '
             + 'esa jornada y <b>no se guarda</b>: solo queda el mes y el año.'
             + '<br><br>Y no hay cuentas ni usuarios: nadie puede ver quién reportó qué.'
             + '<br><br>El anonimato no es un extra. Es lo único que hace que esto sirva.',
    sinPuntoTitulo: 'Ese evento no tiene punto',
    sinPuntoTexto: 'Quien lo escribió no marcó dónde pasó. Es lo único que se pide y no '
                 + 'se obligó, así que no hay sitio al que llevarte.',
    mirandoViento: 'Mirando el viento que hacía ese día…',
    enviando: 'Enviando…',
    verEnMapa: 'Ver en el mapa',
    pendVerif: 'pendiente de verificación',
    entender: 'Entendido',
    nada: 'Todavía no hay eventos.<br>Sé el primero en contar uno.',
    /* los patrones */
    masClaro: 'El patrón más claro hasta ahora', en: 'En', hayEventos: 'hay',
    eventos2: 'eventos', yDeEllos: 'y de ellos', sonDe: 'son de',
    masDatos: 'Con más datos esto dirá cosas como «aquí, en esta época, pasa esto». Ese es el objetivo.',
    quePasaMas: 'Qué pasa más', enTotal: 'eventos en total',
    faseTitulo: 'En qué fase del vuelo', faseSub: 'dónde se complica',
    vientoTitulo: 'El viento de esos días', vientoSub: 'traen el viento real del clima de ese día',
    vientoMedio: 'Viento medio', rachasMedias: 'rachas medias',
    tenianRachas: 'tenían <b>rachas muy por encima del viento medio</b>',
    mayoriaRachado: ' — la mayoría fueron con aire <b>racheado</b>',
    conSostenido: 'fueron con viento sostenido de <b>25 km/h o más</b>',
    gravedadTitulo: 'Gravedad de los eventos', gravedadSub: 'del susto a lo peor: mirarlo sin morbo, para aprender',
    consecTitulo: 'Consecuencias', consecSub: 'el resultado, en datos',
    horaTitulo: 'A qué hora del día', horaSub: 'franja del día',
    dondeTitulo: 'Dónde', dondeSub: 'por sitio, sin señalar puntos exactos',
    pocosDatos: 'Todavía no hay suficientes datos',
    pocosTexto: 'Los patrones salen cuando hay al menos 3 eventos. Ahora hay ',
    pocosFin: 'Por eso lo importante ahora es que la gente reporte: <b>cada susto cuenta</b>. '
            + 'Con 20 eventos esto ya dice cosas útiles.',
  },

  en: {
    lema: 'A community<br>for safer flights',
    navMapa: 'Map', navReportar: 'Report', navPatrones: 'Patterns',
    heroTitulo: 'Shared safety. Collective learning.',
    heroTexto: 'Here you can anonymously report paragliding events.<br>'
             + 'We are not looking for someone to blame — we are looking to learn, '
             + 'so we all land safely.',
    heroCita: '<b>“Every experience counts.</b> A safer flight starts by sharing '
            + 'what happened.”',
    formTitulo: 'Report an event',
    formAviso: 'Everything is anonymous. The marked fields are required.',
    c1t: 'What happened?', c1a: 'From a close call to the worst. This classifies the event.',
    c2t: 'What was it?', c2a: 'The specific situation. This is what makes patterns possible.',
    c3t: 'Consequences', c3a: 'The actual outcome.',
    c4t: 'Phase of flight', c4a: 'At what point in the flight?',
    c5t: 'Where', c5a: 'Tap the area on the map. It is stored rounded to ~100 m: '
                     + 'enough to see patterns, too little to point at anyone.',
    c6t: 'When', c6a: 'With the day I work out the real wind that day. '
                    + '<b>The day is never published</b>: only the month and year are kept.',
    c7t: 'Time of day', c7a: 'The time of day is published, never the exact hour.',
    c8t: 'How was the air', c8a: 'What you felt. I work out the real wind myself.',
    c9t: 'Your flight file', c9a: 'An IGC identifies one specific flight. Read this first.',
    c10t: 'Tell the story', c10a: 'No names. Leave out anything that identifies someone; '
                                + 'keep what explains what happened.',
    obligatorio: 'required', opcional: 'optional',
    otroTitulo: 'Which one? Describe it in one line',
    otroEjemplo: 'E.g. harness snag · someone in the air · brake knot',
    fatalTexto: '<b>Thank you for telling it.</b> This is the data that helps most to '
              + 'keep it from happening again.<br><br>Please tell it <b>without names</b> '
              + 'and without details that do not add to what we learn. What matters is '
              + 'what happened and in what conditions, not who.<br><br>'
              + '<b>Fatalities are not published immediately:</b> they stay pending '
              + 'verification so a mistake or a rumour does not become data.',
    igcBoton: 'Upload my IGC file',
    igcBorrar: 'Delete the track after processing it',
    relatoEjemplo: 'Write your story here (optional)...',
    privacidad: '<b>What is published and what is not.</b><br><b>Published:</b> the month '
              + 'and year, the rounded area, the time of day, the situation and the '
              + 'consequences.<br><b>Never published:</b> your name, the exact day, the '
              + 'exact hour, your precise position, or the IGC file. The file is only '
              + 'read for the flight conditions and is not kept.',
    enviar: 'Send anonymous event',
    evEventos: 'events', evEvento: 'event',
    evSitios: 'sites', evPatrones: 'patterns', evPatron: 'pattern',
    principios: 'Principles',
    p1: 'Safety above all', p1s: 'We learn from real experience.',
    p2: 'No judgement, no blame', p2s: 'This is not about pointing fingers, it is about improving.',
    p3: 'A global community', p3s: 'Shared knowledge makes our flights safer.',
    anonTitulo: 'Anonymous by design',
    anonTexto: 'We do not ask for your name, personal data, or anything that could '
             + 'identify you. The location is approximate and details are handled with care.',
    anonMas: 'Learn more about your privacy',
    aprendeTitulo: 'What we learn',
    aprendeTexto: 'Events let us spot patterns, risk areas and recurring situations so '
                + 'we can share what we learn with the whole community.',
    aprendeVer: 'See patterns and analysis',
    reciente: 'Recent activity on the map',
    verMapaCompleto: 'See the full map',
    emergencia: '<b>Important</b><br>SkyReport is not an emergency channel. If you need '
              + 'immediate help, contact your local rescue services.',
    mapaTitulo: 'Event map',
    mapaSub: 'Each dot is one event. The heat shows where they pile up.',
    patronesTitulo: 'Patterns',
    patronesSub: 'Single events tell stories. Together they reveal patterns.',
    todos: 'All',
    faltaTitulo: 'Something is missing', faltaTexto: 'I need: ',
    faltaFin: '.<br><br>It takes 30 seconds and that is all it needs.',
    graciasTitulo: 'Thank you. It is in.',
    graciasTexto: 'What you told us may keep someone else from going through the same.',
    graciasViento: 'And I saved the real wind from that day: ',
    graciasFin: 'You can report as many as you like: <b>close calls count too</b>.',
    errorTitulo: 'Could not send it',
    errorTexto: 'Check your connection and try again.',
    privTitulo: 'Privacy',
    privTexto: 'We do not ask for your name, phone or email.<br><br>The location is '
             + '<b>rounded to about 100 metres</b>, so it does not point at an exact spot.'
             + '<br><br>The <b>day</b> you enter is used only to work out the wind that '
             + 'day and is <b>not saved</b>: only the month and year remain.'
             + '<br><br>There are no accounts and no users: nobody can see who reported what.'
             + '<br><br>Anonymity is not a feature. It is the only thing that makes this work.',
    sinPuntoTitulo: 'That event has no location',
    sinPuntoTexto: 'Whoever wrote it did not mark where it happened. It is the one thing '
                 + 'we ask for and it is not required, so there is nowhere to take you.',
    mirandoViento: 'Checking the wind that day…',
    enviando: 'Sending…',
    verEnMapa: 'See on the map',
    pendVerif: 'pending verification',
    entender: 'Got it',
    nada: 'No events yet.<br>Be the first to tell one.',
    masClaro: 'The clearest pattern so far', en: 'At', hayEventos: 'there are',
    eventos2: 'events', yDeEllos: 'and of those', sonDe: 'are',
    masDatos: 'With more data this will say things like “here, in this season, this is '
            + 'what happens”. That is the goal.',
    quePasaMas: 'What happens most', enTotal: 'events in total',
    faseTitulo: 'Phase of flight', faseSub: 'where it gets complicated',
    vientoTitulo: 'The wind on those days', vientoSub: 'carry the real wind from the weather of that day',
    vientoMedio: 'Average wind', rachasMedias: 'average gusts',
    tenianRachas: 'had <b>gusts well above the average wind</b>',
    mayoriaRachado: ' — most of them were in <b>gusty</b> air',
    conSostenido: 'had sustained wind of <b>25 km/h or more</b>',
    gravedadTitulo: 'Severity of the events', gravedadSub: 'from a scare to the worst: read it without morbid curiosity, to learn',
    consecTitulo: 'Consequences', consecSub: 'the outcome, in numbers',
    horaTitulo: 'Time of day', horaSub: 'time of day',
    dondeTitulo: 'Where', dondeSub: 'by site, without pointing at exact spots',
    pocosDatos: 'Not enough data yet',
    pocosTexto: 'Patterns appear once there are at least 3 events. Right now there are ',
    pocosFin: 'That is why the important thing now is that people report: <b>every close '
            + 'call counts</b>. With 20 events this already tells you useful things.',
  },
};

let idioma = 'es';""")

# ==========================================================================
# 2) LOS ARRAYS, con el nombre en cada idioma
# ==========================================================================
rep("""const SEVERIDAD = [
  { id:'near',      e:'warning',         n:'Near miss / casi accidente' },
  { id:'incidente', e:'error_outline',   n:'Incidente' },
  { id:'accidente', e:'report_problem',  n:'Accidente' },
  { id:'grave',     e:'personal_injury', n:'Accidente grave' },
  { id:'fatal',     e:'emergency',       n:'Fatalidad' },
];""",
    """const SEVERIDAD = [
  { id:'near',      e:'warning',         es:'Near miss / casi accidente', en:'Near miss' },
  { id:'incidente', e:'error_outline',   es:'Incidente',      en:'Incident' },
  { id:'accidente', e:'report_problem',  es:'Accidente',      en:'Accident' },
  { id:'grave',     e:'personal_injury', es:'Accidente grave', en:'Serious accident' },
  { id:'fatal',     e:'emergency',       es:'Fatalidad',      en:'Fatality' },
];""")

rep("""const SITUACION = [
  { id:'plegada',    e:'air',            n:'Plegada o cierre' },
  { id:'proximidad', e:'groups',         n:'Proximidad entre pilotos' },
  { id:'sotavento',  e:'landscape',      n:'Sotavento' },
  { id:'rotor',      e:'storm',          n:'Rotor o turbulencia' },
  { id:'cable',      e:'cable',          n:'Cable o tendido' },
  { id:'arbol',      e:'forest',         n:'Árbol o zona arbolada' },
  { id:'despegue',   e:'flight_takeoff', n:'Despegue' },
  { id:'aterrizaje', e:'flight_land',    n:'Aterrizaje' },
  { id:'bajo',       e:'trending_down',  n:'Quedarse bajo' },
  { id:'otro',       e:'more_horiz',     n:'Otro' },
];""",
    """const SITUACION = [
  { id:'plegada',    e:'air',            es:'Plegada o cierre',           en:'Collapse or closure' },
  { id:'proximidad', e:'groups',         es:'Proximidad entre pilotos',   en:'Close to another pilot' },
  { id:'sotavento',  e:'landscape',      es:'Sotavento',                  en:'Lee side' },
  { id:'rotor',      e:'storm',          es:'Rotor o turbulencia',        en:'Rotor or turbulence' },
  { id:'cable',      e:'cable',          es:'Cable o tendido',            en:'Cable or power line' },
  { id:'arbol',      e:'forest',         es:'Árbol o zona arbolada',      en:'Tree or wooded area' },
  { id:'despegue',   e:'flight_takeoff', es:'Despegue',                   en:'Launch' },
  { id:'aterrizaje', e:'flight_land',    es:'Aterrizaje',                 en:'Landing' },
  { id:'bajo',       e:'trending_down',  es:'Quedarse bajo',              en:'Getting low' },
  { id:'otro',       e:'more_horiz',     es:'Otro',                       en:'Other' },
];""")

rep("""const CONSEC = [
  { id:'sin',    e:'check_circle',    n:'Sin lesiones' },
  { id:'leves',  e:'healing',         n:'Lesiones leves' },
  { id:'graves', e:'personal_injury', n:'Lesiones graves' },
  { id:'danos',  e:'car_crash',       n:'Daños materiales' },
  { id:'fatal',  e:'emergency',       n:'Fatalidad' },
];""",
    """const CONSEC = [
  { id:'sin',    e:'check_circle',    es:'Sin lesiones',      en:'No injuries' },
  { id:'leves',  e:'healing',         es:'Lesiones leves',    en:'Minor injuries' },
  { id:'graves', e:'personal_injury', es:'Lesiones graves',   en:'Serious injuries' },
  { id:'danos',  e:'car_crash',       es:'Daños materiales',  en:'Material damage' },
  { id:'fatal',  e:'emergency',       es:'Fatalidad',         en:'Fatality' },
];""")

rep("""const FASES = [
  { id:'despegue',     n:'Despegue' },
  { id:'termica',      n:'Térmica / ascenso' },
  { id:'transito',     n:'Tránsito' },
  { id:'aproximacion', n:'Aproximación' },
  { id:'aterrizaje',   n:'Aterrizaje' },
];""",
    """const FASES = [
  { id:'despegue',     es:'Despegue',            en:'Launch' },
  { id:'termica',      es:'Térmica / ascenso',   en:'Thermal / climb' },
  { id:'transito',     es:'Tránsito',            en:'Transition' },
  { id:'aproximacion', es:'Aproximación',        en:'Approach' },
  { id:'aterrizaje',   es:'Aterrizaje',          en:'Landing' },
];""")

rep("""const FRANJAS = [
  { id:'manana',   e:'wb_twilight',   n:'Mañana' },
  { id:'mediodia', e:'light_mode',    n:'Mediodía' },
  { id:'tarde',    e:'wb_sunny',      n:'Tarde' },
  { id:'noche',    e:'dark_mode',     n:'Noche' },
];""",
    """const FRANJAS = [
  { id:'manana',   e:'wb_twilight',   es:'Mañana',   en:'Morning' },
  { id:'mediodia', e:'light_mode',    es:'Mediodía', en:'Midday' },
  { id:'tarde',    e:'wb_sunny',      es:'Tarde',    en:'Afternoon' },
  { id:'noche',    e:'dark_mode',     es:'Noche',    en:'Evening' },
];""")

rep("""const AIRES = [
  { id:'tranquilo',  e:'air',              n:'Tranquilo' },
  { id:'turbulento', e:'waves',            n:'Turbulento' },
  { id:'termico',    e:'local_fire_department', n:'Térmico' },
  { id:'fuerte',     e:'storm',            n:'Con viento fuerte' },
  { id:'variable',   e:'swap_horiz',       n:'Variable' },
  { id:'nose',       e:'help',             n:'No lo sé' },
];""",
    """const AIRES = [
  { id:'tranquilo',  e:'air',                   es:'Tranquilo',         en:'Calm' },
  { id:'turbulento', e:'waves',                 es:'Turbulento',        en:'Turbulent' },
  { id:'termico',    e:'local_fire_department', es:'Térmico',           en:'Thermal' },
  { id:'fuerte',     e:'storm',                 es:'Con viento fuerte', en:'Strong wind' },
  { id:'variable',   e:'swap_horiz',            es:'Variable',          en:'Variable' },
  { id:'nose',       e:'help',                  es:'No lo sé',          en:'Not sure' },
];""")

# ==========================================================================
# 3) las funciones que leen el nombre segun el idioma
# ==========================================================================
rep("""function sevDe(id){ return SEVERIDAD.find(t => t.id === id) || SEVERIDAD[0]; }
function sitDe(id){ return SITUACION.find(t => t.id === id) || SITUACION[SITUACION.length - 1]; }
function consDe(id){ return CONSEC.find(t => t.id === id) || { n: id || '', e:'help' }; }""",
    """/* el nombre de una opcion, en el idioma que toque */
function nb(o){ return o ? (o[idioma] || o.es || '') : ''; }
function sevDe(id){ return SEVERIDAD.find(t => t.id === id) || SEVERIDAD[0]; }
function sitDe(id){ return SITUACION.find(t => t.id === id) || SITUACION[SITUACION.length - 1]; }
function consDe(id){ return CONSEC.find(t => t.id === id) || { es: id || '', en: id || '', e:'help' }; }
function faseDe(id){ return FASES.find(f => f.id === id) || { es:'', en:'' }; }
function franjaDe(id){ return FRANJAS.find(f => f.id === id) || { es:'', en:'' }; }
function aireDe(id){ return AIRES.find(a => a.id === id) || { es:'', en:'' }; }
/* y el texto de la interfaz */
function t(k){ return (TXT[idioma] && TXT[idioma][k]) || (TXT.es[k] || ''); }""")

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
