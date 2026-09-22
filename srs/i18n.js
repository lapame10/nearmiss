/* ============================================================
   SkyReport — idiomas
   ============================================================
   Todo el texto de la interfaz vive AQUÍ, no repartido por los
   archivos. Así traducir es añadir un bloque, y no hay que
   buscar cadenas sueltas por media aplicación.

   Uso:
       import { t, ponIdioma, idioma } from './i18n.js';
       t('nav.home')                    →  "Home"
       t('signal.related', { n: 5 })    →  "5 related reports"

   Si falta una clave, se devuelve la inglesa y, si tampoco está,
   la clave tal cual. Nunca se enseña un hueco en blanco.
   ============================================================ */

export const IDIOMAS = [
  { id: 'en', n: 'English',  bandera: 'EN' },
  { id: 'es', n: 'Español',  bandera: 'ES' },
  { id: 'fr', n: 'Français', bandera: 'FR' },
  { id: 'de', n: 'Deutsch',  bandera: 'DE' },
  { id: 'pt', n: 'Português',bandera: 'PT' },
];

const CLAVE = 'skyreport_idioma';

/* ============================================================
   DICCIONARIOS
   ============================================================ */
const EN = {
  'nav.home': 'Home', 'nav.map': 'Map', 'nav.report': 'Report',
  'nav.signals': 'Signals', 'nav.sites': 'Sites', 'nav.methodology': 'Methodology',

  'brand.tagline': 'Community safety intelligence for free flight',
  'common.of': 'of', 'common.reports': 'reports', 'common.report': 'report',
  'common.flightsLogged': 'flights logged', 'common.lastReport': 'Last report',
  'common.any': 'Any', 'common.apply': 'Apply', 'common.clear': 'Clear filters',
  'common.back': 'Back', 'common.continue': 'Continue', 'common.next': 'Next',
  'common.submit': 'Submit', 'common.loading': 'Loading…', 'common.na': 'N/A',
  'common.viewReport': 'View report', 'common.viewSignal': 'View signal',
  'common.viewSite': 'View site profile', 'common.optional': 'optional',
  'common.demo': 'Demo data', 'common.close': 'Close',

  'status.demo': 'Demonstration mode — this data is not a record of real accidents.',
  'status.community': 'Community data',
  'status.offline': 'No connection',
  'status.offlineSaved': 'Saved on this device. SkyReport will submit it when a connection is available.',
  'status.pending': '{n} waiting to be sent.',
  'status.synced': 'All submissions sent.',
  'status.connecting': 'Connecting…',
  'status.unavailable': 'SkyReport cannot reach the community data right now. Showing what is on this device.',

  'home.searchTitle': 'Search a flying site',
  'home.searchPlaceholder': 'Search a flying site…',
  'home.searchNoResults': 'No site matches that.',
  'home.reportEvent': 'Report an event',
  'home.reportEventSub': 'Structured, step by step',
  'home.flewToday': 'I flew today — no incident',
  'home.flewTodaySub': 'Three fields. Ten seconds.',
  'home.recentActivity': 'Recent reporting activity',
  'home.recentSignals': 'Recent signals',
  'home.sitesActivity': 'Sites with activity',
  'home.patternSummary': 'Pattern summary',
  'home.quickActions': 'Quick actions',

  'signals.title': 'Signals',
  'signals.lede': 'A signal is a pattern SkyReport has found across several reports. It is not an accident and it is not a safety assessment — it is what the available data shows, written so you can disagree with it.',
  'signals.none': 'No signals yet.',
  'signals.noneHelp': 'Signals appear when at least three similar reports cluster.',
  'signals.rule': 'Rule',
  'signals.related': '{n} related reports',
  'signals.viewRelated': 'View related reports',
  'signals.area': '{km} km area',
  'signals.period': '{n} days',
  'signals.conditions': '{x} conditions',
  'signals.between': '{n} occurred between {a} and {b}',
  'signals.exposureTitle': 'Exposure context',
  'signals.exposure': '{n} related reports · {v} logged flights in a comparable period',
  'signals.exposureLimited': 'Flight exposure data is currently limited.',
  'signals.exposureExplain': 'This does not mean the site is more or less dangerous. Sites with more pilots and more reporting activity naturally appear more often.',
  'signals.disclaimer': 'This is a data-derived signal based on available reports, not a definitive safety assessment.',

  'strength.limited': 'Limited data',
  'strength.repeated': 'Repeated pattern',
  'strength.strong': 'Strong repeated pattern',
  'strength.explain': 'These labels describe how much related evidence exists — not how dangerous it is to fly.',

  'safeFlight.title': 'I flew today — no incident',
  'safeFlight.lede': 'A flight where nothing happened. Three fields and you are done.',
  'safeFlight.site': 'Site',
  'safeFlight.date': 'Date',
  'safeFlight.type': 'Type of flight',
  'safeFlight.log': 'Log this flight',
  'safeFlight.logged': 'Flight logged — thank you',
  'safeFlight.why': 'Logging flights where nothing happened is what lets SkyReport put incident numbers in context.',
  'safeFlight.chooseSite': 'Choose a site…',
  'safeFlight.needSite': 'Pick a site and a type of flight',

  'report.title': 'Report',
  'report.lede': 'The form changes with the event. You only answer what is relevant.',
  'report.what': 'What are you reporting?',
  'report.step.type': 'Type', 'report.step.basics': 'Basics', 'report.step.conditions': 'Conditions',
  'report.step.equipment': 'Equipment', 'report.step.igc': 'IGC', 'report.step.narrative': 'Narrative',
  'report.step.quick': 'Quick log',
  'report.site': 'Site', 'report.zone': 'Zone within the site',
  'report.zoneHelp': 'Zones are what let SkyReport say "behind this ridge" instead of just naming the site.',
  'report.notSure': 'Not sure',
  'report.date': 'Date', 'report.time': 'Time',
  'report.location': 'Location on the map',
  'report.tapMap': 'Tap the map to place the event.',
  'report.phase': 'Flight phase', 'report.event': 'Event type',
  'report.outcome': 'Outcome', 'report.injury': 'Injury',
  'report.injuryNote': 'Injuries are recorded, never ranked.',
  'report.aboutEvent': 'About this event',
  'report.aboutEventHelp': 'Only the questions that matter for this type.',
  'report.altitude': 'Estimated altitude at the event (m AGL)',
  'report.conditionsTitle': 'Conditions you observed',
  'report.conditionsHelp': 'as you felt them, not from a model',
  'report.windDir': 'Wind direction', 'report.windSpeed': 'Wind speed (km/h)',
  'report.gusts': 'Gusts (km/h)', 'report.thermal': 'Thermal activity',
  'report.turbulence': 'Turbulence felt', 'report.cloud': 'Cloud',
  'report.weatherNotes': 'Anything else about the weather',
  'report.weatherFuture': 'If SkyReport can pull weather data for this location and time later, it will be shown next to what you reported — never instead of it.',
  'report.equipmentTitle': 'Equipment', 'report.equipmentHelp': 'all optional',
  'report.wingBrand': 'Wing brand', 'report.wingModel': 'Model',
  'report.wingClass': 'Class', 'report.wingSize': 'Size',
  'report.harness': 'Harness', 'report.reserve': 'Reserve',
  'report.experience': 'Approximate experience',
  'report.experienceNote': 'A wide range, on purpose. SkyReport does not identify pilots and does not rate their level.',
  'report.narrativeTitle': 'In your words',
  'report.narrativeHelp': 'plain description, no blame',
  'report.whatHappened': 'What happened',
  'report.contributing': 'Anything that may have contributed',
  'report.lessons': 'What you took from it',
  'report.advice': 'What you would tell another pilot',
  'report.submit': 'Submit report',
  'report.needFields': 'Still needed: {x}',
  'report.submitted': 'Report submitted',
  'report.submittedPending': 'Report submitted. It will appear once reviewed.',

  'igc.title': 'Flight track',
  'igc.drop': 'Drop an IGC file here',
  'igc.orTap': 'or tap to choose one',
  'igc.noFile': 'No file yet',
  'igc.privacyTitle': 'Privacy',
  'igc.privacy': 'Your IGC is used to extract what the wing was doing around the event. The original file is not published, the track is not published, and coordinates are rounded to about 100 m before anything appears publicly.',
  'igc.cantParse': 'Could not parse this IGC file.',
  'igc.tryAnother': 'Try another file',
  'igc.continueWithout': 'Continue without IGC',
  'igc.notIgc': 'That does not look like an .igc file.',
  'igc.loaded': 'IGC loaded: {n} points, {a} to {b} UTC.',
  'igc.demoTrack': 'Demonstration track — this is not from your file.',
  'igc.suggestTitle': 'Possible event point',
  'igc.suggestHelp': 'SkyReport can point at moments that stand out, but it cannot know which one is the event — a cravat or a near miss does not look like a steep descent. Move the marker to where it happened.',
  'igc.anomalies': 'Points that stand out',
  'igc.noAnomalies': 'Nothing stands out in this track.',
  'igc.confirm': 'Event occurred approximately here',
  'igc.confirmed': 'Event time confirmed: {h} UTC',
  'igc.needConfirm': 'Confirm where the event happened before continuing.',
  'igc.timeline': 'Event timeline',

  'method.title': 'How SkyReport works',
  'method.lede': 'What the data can and cannot tell you.',
  'method.reportVsSignal': 'Report vs Signal',
  'method.reportDef': 'Report — one event, sent by one person. It is testimony.',
  'method.signalDef': 'Signal — a pattern found across several reports. It is an observation, and it can be wrong. Every signal shows the rule that produced it, so you can judge it yourself.',
  'method.howBuilt': 'How signals are built',
  'method.limits': 'Limits of this data',
  'method.bias': 'Reporting bias',
  'method.biasText': 'People report what they think is worth reporting. Busy sites, competition sites and sites with an active local community are over-represented. A quiet site with no reports is not necessarily a safe site.',
  'method.denominator': 'The denominator problem',
  'method.denominatorText': '"100 incidents" means nothing on its own. 100 out of 500 flights is not the same as 100 out of 50,000. That is why SkyReport also records flights where nothing happened.',
  'method.correlation': 'Correlation is not causation',
  'method.correlationText': 'If most reports at a site mention NW wind, that may mean NW days are riskier — or simply that most people fly on NW days. Patterns here describe reports, not causes.',
  'method.wontDo': 'What SkyReport will not do',
  'method.wontDoText': 'It does not rank pilots, score risk, or tell you whether to fly. It gives you information. You make the decision.',
  'method.privacy': 'Privacy',

  'snapshot.title': 'Event snapshot', 'snapshot.event': 'Event', 'snapshot.phase': 'Phase',
  'snapshot.outcome': 'Outcome', 'snapshot.altitude': 'Altitude',
  'snapshot.wind': 'Wind', 'snapshot.site': 'Site',
  'snapshot.similar': 'Nearby similar reports', 'snapshot.igc': 'IGC',
  'snapshot.available': 'Available', 'snapshot.notAvailable': 'Not available',
  'snapshot.updates': 'updates as you type',

  'box.title': 'Event timeline', 'box.window': 'T-120 s → T+60 s',
  'box.altitude': 'Altitude', 'box.speed': 'Speed', 'box.climb': 'Climb / sink',
  'box.heading': 'Heading', 'box.note': 'Speed on the ground, barometric altitude and heading. A reconstruction from the IGC around the event, not a flight recorder.',
  'box.exceptions': 'Worth a look',
  'box.exceptionsHelp': 'Events flagged by simple thresholds, the way telemetry systems do: do not show everything, show what stands out.',
  'box.observation': 'These are observations from the track, not diagnoses.',

  'detail.whatHappened': 'What happened', 'detail.conditions': 'Conditions observed',
  'detail.equipment': 'Equipment', 'detail.location': 'Location',
  'detail.track': 'Flight track', 'detail.completeness': 'Data completeness',
  'detail.similar': 'Similar reports nearby', 'detail.noSimilar': 'No similar reports found nearby.',
  'detail.noDescription': 'No description was added to this report.',
  'detail.noIgc': 'No IGC for this report.',
  'detail.noIgcHelp': 'Adding a track lets SkyReport reconstruct what the wing was doing around the event.',
  'detail.coordNote': 'Coordinates are rounded to about 100 m. Exact tracks are not published.',
  'detail.completenessNote': 'How much we can learn from this report. Not an assessment of the pilot.',

  'site.overview': 'Overview', 'site.reports': 'Reports', 'site.signals': 'Signals',
  'site.map': 'Map', 'site.patterns': 'Patterns',
  'site.total': 'total reports', 'site.nearMiss': 'near misses',
  'site.reserve': 'reserve deployments', 'site.hard': 'hard landings',
  'site.injury': 'with injury', 'site.flights': 'flights logged',
  'site.mostEvent': 'Most common event', 'site.mostPhase': 'Most common phase',
  'site.mostWind': 'Most reported wind', 'site.rate': 'Reports per 1,000 logged flights',
  'site.rateLimited': '{n} flights logged at this site. That is still too small a sample to compare rates — a single busy week would move the number.',
  'site.rateValue': '{r} per 1,000 logged flights, from {n} logged flights.',
  'site.sampleSmall': 'The sample is still limited.',
  'site.zones': 'Zones', 'site.zonesHelp': 'Zones let us say "behind this ridge" instead of just naming the site.',
  'site.noReports': 'No reports at this site yet.',
  'site.noSignals': 'No signals at this site yet.',
  'site.notEnough': 'Not enough reports at this site yet to describe patterns.',
  'site.patternsNote': 'These are descriptions of the reports, not causes. Correlation here does not imply causation.',

  'map.title': 'Map', 'map.lede': 'Reports, heat concentration and signals. Filter it down to the conditions you care about.',
  'map.reports': 'Reports', 'map.heatmap': 'Heatmap', 'map.signals': 'Signals',
  'map.base': 'Base', 'map.filters': 'Filters', 'map.from': 'From', 'map.to': 'To',
  'map.country': 'Country', 'map.flyingSite': 'Site',
  'map.shown': '{n} reports shown', 'map.filtersActive': '{n} filters active',
  'map.rounded': 'Rounded to about 100 m.', 'map.injury': 'With injury',
  'map.noInjury': 'No injury', 'map.reserveOnly': 'Reserve deployment',
  'map.windDir': 'Wind direction', 'map.wingClass': 'Wing class',

  'lang.label': 'Language',
  'update.available': 'A new version of SkyReport is available.',
  'update.refresh': 'Refresh',

  'type.incident': 'Incident', 'type.near_miss': 'Near miss',
  'type.hazard': 'Hazard observation', 'type.safe_flight': 'Safe flight log',
  'type.incident.d': 'Something happened and it affected the flight or the pilot.',
  'type.near_miss.d': 'It nearly happened, but nothing came of it. Still valuable.',
  'type.hazard.d': 'A condition or feature worth flagging: cables, rotor, a gap in a fence.',
  'type.safe_flight.d': 'You flew here and nothing happened. Takes ten seconds.',

  'admin.title': 'Moderation', 'admin.pending': 'Pending',
  'admin.approve': 'Approve', 'admin.reject': 'Reject',
  'admin.duplicate': 'Mark duplicate', 'admin.review': 'Review',
};

const ES = {
  'nav.home': 'Inicio', 'nav.map': 'Mapa', 'nav.report': 'Reportar',
  'nav.signals': 'Señales', 'nav.sites': 'Sitios', 'nav.methodology': 'Metodología',

  'brand.tagline': 'Inteligencia de seguridad comunitaria para vuelo libre',
  'common.of': 'de', 'common.reports': 'reportes', 'common.report': 'reporte',
  'common.flightsLogged': 'vuelos registrados', 'common.lastReport': 'Último reporte',
  'common.any': 'Cualquiera', 'common.apply': 'Aplicar', 'common.clear': 'Quitar filtros',
  'common.back': 'Atrás', 'common.continue': 'Continuar', 'common.next': 'Siguiente',
  'common.submit': 'Enviar', 'common.loading': 'Cargando…', 'common.na': 'N/D',
  'common.viewReport': 'Ver reporte', 'common.viewSignal': 'Ver señal',
  'common.viewSite': 'Ver ficha del sitio', 'common.optional': 'opcional',
  'common.demo': 'Datos de demostración', 'common.close': 'Cerrar',

  'status.demo': 'Modo demostración — estos datos no son un registro de accidentes reales.',
  'status.community': 'Datos de la comunidad',
  'status.offline': 'Sin conexión',
  'status.offlineSaved': 'Guardado en este dispositivo. SkyReport lo enviará cuando haya conexión.',
  'status.pending': '{n} esperando a enviarse.',
  'status.synced': 'Todo enviado.',
  'status.connecting': 'Conectando…',
  'status.unavailable': 'SkyReport no puede alcanzar los datos de la comunidad ahora mismo. Se muestra lo que hay en este dispositivo.',

  'home.searchTitle': 'Buscar un sitio de vuelo',
  'home.searchPlaceholder': 'Busca un sitio de vuelo…',
  'home.searchNoResults': 'Ningún sitio coincide con eso.',
  'home.reportEvent': 'Reportar un evento',
  'home.reportEventSub': 'Estructurado, paso a paso',
  'home.flewToday': 'Hoy volé — sin incidentes',
  'home.flewTodaySub': 'Tres campos. Diez segundos.',
  'home.recentActivity': 'Actividad reciente',
  'home.recentSignals': 'Señales recientes',
  'home.sitesActivity': 'Sitios con actividad',
  'home.patternSummary': 'Resumen de patrones',
  'home.quickActions': 'Accesos rápidos',

  'signals.title': 'Señales',
  'signals.lede': 'Una señal es un patrón que SkyReport ha encontrado entre varios reportes. No es un accidente ni una evaluación de seguridad: es lo que muestran los datos disponibles, escrito para que puedas estar en desacuerdo.',
  'signals.none': 'Todavía no hay señales.',
  'signals.noneHelp': 'Las señales aparecen cuando se juntan al menos tres reportes parecidos.',
  'signals.rule': 'Regla',
  'signals.related': '{n} reportes relacionados',
  'signals.viewRelated': 'Ver reportes relacionados',
  'signals.area': 'área de {km} km',
  'signals.period': '{n} días',
  'signals.conditions': 'condiciones {x}',
  'signals.between': '{n} ocurrieron entre {a} y {b}',
  'signals.exposureTitle': 'Contexto de exposición',
  'signals.exposure': '{n} reportes relacionados · {v} vuelos registrados en un periodo comparable',
  'signals.exposureLimited': 'Los datos de exposición de vuelo son todavía limitados.',
  'signals.exposureExplain': 'Esto no significa que el sitio sea más o menos peligroso. Los sitios con más pilotos y más actividad de reporte aparecen más a menudo, naturalmente.',
  'signals.disclaimer': 'Esta es una señal derivada de los datos disponibles, no una evaluación definitiva de seguridad.',

  'strength.limited': 'Datos limitados',
  'strength.repeated': 'Patrón repetido',
  'strength.strong': 'Patrón repetido fuerte',
  'strength.explain': 'Estas etiquetas describen cuánta evidencia relacionada existe — no lo peligroso que es volar.',

  'safeFlight.title': 'Hoy volé — sin incidentes',
  'safeFlight.lede': 'Un vuelo donde no pasó nada. Tres campos y ya está.',
  'safeFlight.site': 'Sitio',
  'safeFlight.date': 'Fecha',
  'safeFlight.type': 'Tipo de vuelo',
  'safeFlight.log': 'Registrar este vuelo',
  'safeFlight.logged': 'Vuelo registrado — gracias',
  'safeFlight.why': 'Registrar los vuelos donde no pasó nada es lo que permite a SkyReport poner los reportes en contexto.',
  'safeFlight.chooseSite': 'Elige un sitio…',
  'safeFlight.needSite': 'Elige un sitio y un tipo de vuelo',

  'report.title': 'Reportar',
  'report.lede': 'El formulario cambia según el evento. Solo contestas lo que importa.',
  'report.what': '¿Qué estás reportando?',
  'report.step.type': 'Tipo', 'report.step.basics': 'Básico', 'report.step.conditions': 'Condiciones',
  'report.step.equipment': 'Equipo', 'report.step.igc': 'IGC', 'report.step.narrative': 'Narrativa',
  'report.step.quick': 'Registro rápido',
  'report.site': 'Sitio', 'report.zone': 'Zona dentro del sitio',
  'report.zoneHelp': 'Las zonas son lo que permite a SkyReport decir "detrás de esta cresta" en vez de solo nombrar el sitio.',
  'report.notSure': 'No estoy seguro',
  'report.date': 'Fecha', 'report.time': 'Hora',
  'report.location': 'Ubicación en el mapa',
  'report.tapMap': 'Toca el mapa para situar el evento.',
  'report.phase': 'Fase del vuelo', 'report.event': 'Tipo de evento',
  'report.outcome': 'Resultado', 'report.injury': 'Lesión',
  'report.injuryNote': 'Las lesiones se registran, nunca se clasifican.',
  'report.aboutEvent': 'Sobre este evento',
  'report.aboutEventHelp': 'Solo las preguntas que importan para este tipo.',
  'report.altitude': 'Altitud estimada en el evento (m AGL)',
  'report.conditionsTitle': 'Condiciones que observaste',
  'report.conditionsHelp': 'como las sentiste, no de un modelo',
  'report.windDir': 'Dirección del viento', 'report.windSpeed': 'Velocidad del viento (km/h)',
  'report.gusts': 'Rachas (km/h)', 'report.thermal': 'Actividad térmica',
  'report.turbulence': 'Turbulencia percibida', 'report.cloud': 'Nubosidad',
  'report.weatherNotes': 'Algo más sobre el tiempo',
  'report.weatherFuture': 'Si más adelante SkyReport puede obtener datos meteorológicos de este lugar y hora, se mostrarán junto a lo que reportaste — nunca en su lugar.',
  'report.equipmentTitle': 'Equipo', 'report.equipmentHelp': 'todo opcional',
  'report.wingBrand': 'Marca del ala', 'report.wingModel': 'Modelo',
  'report.wingClass': 'Clasificación', 'report.wingSize': 'Talla',
  'report.harness': 'Arnés', 'report.reserve': 'Reserva',
  'report.experience': 'Experiencia aproximada',
  'report.experienceNote': 'Un rango amplio, a propósito. SkyReport no identifica pilotos ni juzga su nivel.',
  'report.narrativeTitle': 'En tus palabras',
  'report.narrativeHelp': 'descripción llana, sin culpar a nadie',
  'report.whatHappened': 'Qué pasó',
  'report.contributing': 'Qué pudo contribuir',
  'report.lessons': 'Qué sacaste de ello',
  'report.advice': 'Qué le dirías a otro piloto',
  'report.submit': 'Enviar reporte',
  'report.needFields': 'Falta: {x}',
  'report.submitted': 'Reporte enviado',
  'report.submittedPending': 'Reporte enviado. Aparecerá cuando se revise.',

  'igc.title': 'Track del vuelo',
  'igc.drop': 'Arrastra aquí un archivo IGC',
  'igc.orTap': 'o toca para elegir uno',
  'igc.noFile': 'Ningún archivo todavía',
  'igc.privacyTitle': 'Privacidad',
  'igc.privacy': 'Tu IGC se usa para extraer qué hacía el ala alrededor del evento. El archivo original no se publica, el track no se publica, y las coordenadas se redondean a unos 100 m antes de que nada aparezca públicamente.',
  'igc.cantParse': 'No se ha podido interpretar este archivo IGC.',
  'igc.tryAnother': 'Probar otro archivo',
  'igc.continueWithout': 'Continuar sin IGC',
  'igc.notIgc': 'Eso no parece un archivo .igc.',
  'igc.loaded': 'IGC cargado: {n} puntos, de {a} a {b} UTC.',
  'igc.demoTrack': 'Track de demostración — no sale de tu archivo.',
  'igc.suggestTitle': 'Posible momento del evento',
  'igc.suggestHelp': 'SkyReport puede señalar momentos que destacan, pero no puede saber cuál es el evento — un cravat o un roce no se parecen a una caída fuerte. Mueve el marcador a donde ocurrió.',
  'igc.anomalies': 'Momentos que destacan',
  'igc.noAnomalies': 'Nada destaca en este track.',
  'igc.confirm': 'El evento ocurrió aproximadamente aquí',
  'igc.confirmed': 'Hora del evento confirmada: {h} UTC',
  'igc.needConfirm': 'Confirma dónde ocurrió el evento antes de continuar.',
  'igc.timeline': 'Cronología del evento',

  'method.title': 'Cómo funciona SkyReport',
  'method.lede': 'Qué pueden y qué no pueden decirte los datos.',
  'method.reportVsSignal': 'Reporte y señal',
  'method.reportDef': 'Reporte — un evento, enviado por una persona. Es un testimonio.',
  'method.signalDef': 'Señal — un patrón encontrado entre varios reportes. Es una observación, y puede estar equivocada. Cada señal muestra la regla que la produjo, para que la juzgues tú.',
  'method.howBuilt': 'Cómo se construyen las señales',
  'method.limits': 'Límites de estos datos',
  'method.bias': 'Sesgo de reporte',
  'method.biasText': 'La gente reporta lo que cree que merece la pena reportar. Los sitios concurridos, los de competición y los que tienen comunidad local activa salen sobrerrepresentados. Un sitio tranquilo sin reportes no es necesariamente un sitio seguro.',
  'method.denominator': 'El problema del denominador',
  'method.denominatorText': '"100 incidentes" no dice nada por sí solo. 100 de 500 vuelos no es lo mismo que 100 de 50.000. Por eso SkyReport registra también los vuelos donde no pasó nada.',
  'method.correlation': 'Correlación no es causalidad',
  'method.correlationText': 'Si la mayoría de reportes de un sitio mencionan viento NW, eso puede significar que los días de NW son más duros — o simplemente que la gente vuela sobre todo en días de NW. Los patrones describen reportes, no causas.',
  'method.wontDo': 'Lo que SkyReport no hace',
  'method.wontDoText': 'No clasifica pilotos, no puntúa riesgos y no te dice si volar. Te da información. La decisión es tuya.',
  'method.privacy': 'Privacidad',

  'snapshot.title': 'Ficha del evento', 'snapshot.event': 'Evento', 'snapshot.phase': 'Fase',
  'snapshot.outcome': 'Resultado', 'snapshot.altitude': 'Altitud',
  'snapshot.wind': 'Viento', 'snapshot.site': 'Sitio',
  'snapshot.similar': 'Reportes similares cerca', 'snapshot.igc': 'IGC',
  'snapshot.available': 'Disponible', 'snapshot.notAvailable': 'No disponible',
  'snapshot.updates': 'se actualiza mientras escribes',

  'box.title': 'Cronología del evento', 'box.window': 'T-120 s → T+60 s',
  'box.altitude': 'Altitud', 'box.speed': 'Velocidad', 'box.climb': 'Ascenso / caída',
  'box.heading': 'Rumbo', 'box.note': 'Velocidad sobre el suelo, altitud barométrica y rumbo. Una reconstrucción del IGC alrededor del evento, no una caja negra de verdad.',
  'box.exceptions': 'Merece la pena mirar',
  'box.exceptionsHelp': 'Momentos señalados por umbrales simples, como hacen los sistemas de telemetría: no enseñar todo, enseñar lo que destaca.',
  'box.observation': 'Estas son observaciones del track, no diagnósticos.',

  'detail.whatHappened': 'Qué pasó', 'detail.conditions': 'Condiciones observadas',
  'detail.equipment': 'Equipo', 'detail.location': 'Ubicación',
  'detail.track': 'Track del vuelo', 'detail.completeness': 'Completitud del dato',
  'detail.similar': 'Reportes similares cerca', 'detail.noSimilar': 'No se han encontrado reportes similares cerca.',
  'detail.noDescription': 'Este reporte no tiene descripción.',
  'detail.noIgc': 'Este reporte no tiene IGC.',
  'detail.noIgcHelp': 'Añadir un track permite a SkyReport reconstruir qué hacía el ala alrededor del evento.',
  'detail.coordNote': 'Las coordenadas se redondean a unos 100 m. Los tracks exactos no se publican.',
  'detail.completenessNote': 'Cuánto podemos aprender de este reporte. No es una valoración del piloto.',

  'site.overview': 'Resumen', 'site.reports': 'Reportes', 'site.signals': 'Señales',
  'site.map': 'Mapa', 'site.patterns': 'Patrones',
  'site.total': 'reportes totales', 'site.nearMiss': 'casi accidentes',
  'site.reserve': 'despliegues de reserva', 'site.hard': 'aterrizajes duros',
  'site.injury': 'con lesión', 'site.flights': 'vuelos registrados',
  'site.mostEvent': 'Evento más común', 'site.mostPhase': 'Fase más común',
  'site.mostWind': 'Viento más reportado', 'site.rate': 'Reportes por 1.000 vuelos registrados',
  'site.rateLimited': '{n} vuelos registrados en este sitio. Sigue siendo una muestra demasiado pequeña para comparar tasas — una sola semana buena movería el número.',
  'site.rateValue': '{r} por 1.000 vuelos registrados, sobre {n} vuelos.',
  'site.sampleSmall': 'La muestra sigue siendo limitada.',
  'site.zones': 'Zonas', 'site.zonesHelp': 'Las zonas permiten decir "detrás de esta cresta" en vez de solo nombrar el sitio.',
  'site.noReports': 'Todavía no hay reportes en este sitio.',
  'site.noSignals': 'Todavía no hay señales en este sitio.',
  'site.notEnough': 'Todavía no hay reportes suficientes en este sitio para describir patrones.',
  'site.patternsNote': 'Estas son descripciones de los reportes, no causas. Aquí correlación no implica causalidad.',

  'map.title': 'Mapa', 'map.lede': 'Reportes, concentración y señales. Filtra hasta las condiciones que te interesan.',
  'map.reports': 'Reportes', 'map.heatmap': 'Mapa de calor', 'map.signals': 'Señales',
  'map.base': 'Base', 'map.filters': 'Filtros', 'map.from': 'Desde', 'map.to': 'Hasta',
  'map.country': 'País', 'map.flyingSite': 'Sitio',
  'map.shown': '{n} reportes mostrados', 'map.filtersActive': '{n} filtros activos',
  'map.rounded': 'Redondeado a unos 100 m.', 'map.injury': 'Con lesión',
  'map.noInjury': 'Sin lesión', 'map.reserveOnly': 'Despliegue de reserva',
  'map.windDir': 'Dirección del viento', 'map.wingClass': 'Clase de ala',

  'lang.label': 'Idioma',
  'update.available': 'Hay una versión nueva de SkyReport.',
  'update.refresh': 'Actualizar',

  'type.incident': 'Incidente', 'type.near_miss': 'Casi accidente',
  'type.hazard': 'Observación de peligro', 'type.safe_flight': 'Vuelo sin incidentes',
  'type.incident.d': 'Pasó algo y afectó al vuelo o al piloto.',
  'type.near_miss.d': 'Casi pasó, pero no llegó a más. Sigue siendo valioso.',
  'type.hazard.d': 'Una condición o un elemento que merece señalarse: cables, rotor, un hueco en una valla.',
  'type.safe_flight.d': 'Volaste aquí y no pasó nada. Son diez segundos.',

  'admin.title': 'Moderación', 'admin.pending': 'Pendiente',
  'admin.approve': 'Aprobar', 'admin.reject': 'Rechazar',
  'admin.duplicate': 'Marcar duplicado', 'admin.review': 'Revisar',
};

const FR = {
  'nav.home': 'Accueil', 'nav.map': 'Carte', 'nav.report': 'Signaler',
  'nav.signals': 'Signaux', 'nav.sites': 'Sites', 'nav.methodology': 'Méthode',
  'brand.tagline': 'Renseignement de sécurité communautaire pour le vol libre',
  'common.reports': 'signalements', 'common.flightsLogged': 'vols enregistrés',
  'common.back': 'Retour', 'common.continue': 'Continuer', 'common.next': 'Suivant',
  'common.submit': 'Envoyer', 'common.loading': 'Chargement…', 'common.na': 'N/D',
  'common.optional': 'facultatif', 'common.demo': 'Données de démonstration',

  'status.demo': 'Mode démonstration — ces données ne sont pas un registre d’accidents réels.',
  'status.offline': 'Hors ligne',
  'status.offlineSaved': 'Enregistré sur cet appareil. SkyReport l’enverra dès qu’une connexion sera disponible.',
  'home.searchTitle': 'Chercher un site de vol',
  'home.searchPlaceholder': 'Chercher un site de vol…',
  'home.reportEvent': 'Signaler un événement',
  'home.flewToday': "J'ai volé aujourd'hui — aucun incident",
  'home.flewTodaySub': 'Trois champs. Dix secondes.',
  'home.recentSignals': 'Signaux récents',
  'home.sitesActivity': 'Sites avec activité',
  'home.patternSummary': 'Résumé des tendances',

  'signals.title': 'Signaux',
  'signals.lede': "Un signal est une tendance que SkyReport a trouvée dans plusieurs signalements. Ce n'est pas un accident et ce n'est pas une évaluation de sécurité.",
  'signals.related': '{n} signalements liés', 'signals.viewRelated': 'Voir les signalements liés',
  'signals.rule': 'Règle', 'signals.disclaimer': "Signal dérivé des données disponibles, pas une évaluation de sécurité définitive.",
  'strength.limited': 'Données limitées', 'strength.repeated': 'Tendance répétée',
  'strength.strong': 'Tendance répétée forte',

  'safeFlight.title': "J'ai volé aujourd'hui — aucun incident",
  'safeFlight.lede': "Un vol où rien ne s'est passé. Trois champs et c'est fini.",
  'safeFlight.site': 'Site', 'safeFlight.date': 'Date', 'safeFlight.type': 'Type de vol',
  'safeFlight.log': 'Enregistrer ce vol', 'safeFlight.logged': 'Vol enregistré — merci',
  'safeFlight.chooseSite': 'Choisir un site…',
  'report.title': 'Signaler', 'report.step.type': 'Type', 'report.step.basics': 'Base',
  'report.step.conditions': 'Conditions', 'report.step.equipment': 'Équipement',
  'report.step.igc': 'IGC', 'report.step.narrative': 'Récit',
  'report.submit': 'Envoyer le signalement',
  'igc.drop': 'Déposez un fichier IGC ici', 'igc.cantParse': "Impossible d'interpréter ce fichier IGC.",
  'igc.tryAnother': 'Essayer un autre fichier', 'igc.continueWithout': 'Continuer sans IGC',
  'method.title': 'Comment fonctionne SkyReport',
  'lang.label': 'Langue',
  'update.available': 'Une nouvelle version de SkyReport est disponible.',
  'update.refresh': 'Actualiser',
};

const DE = {
  'nav.home': 'Start', 'nav.map': 'Karte', 'nav.report': 'Melden',
  'nav.signals': 'Signale', 'nav.sites': 'Gebiete', 'nav.methodology': 'Methode',
  'brand.tagline': 'Sicherheitsinformationen aus der Community für Gleitschirmflieger',
  'common.reports': 'Meldungen', 'common.flightsLogged': 'erfasste Flüge',
  'common.back': 'Zurück', 'common.continue': 'Weiter', 'common.next': 'Weiter',
  'common.submit': 'Senden', 'common.loading': 'Lädt…', 'common.na': 'k. A.',
  'common.optional': 'optional', 'common.demo': 'Demodaten',

  'status.demo': 'Demomodus — diese Daten sind kein Verzeichnis echter Unfälle.',
  'status.offline': 'Keine Verbindung',
  'status.offlineSaved': 'Auf diesem Gerät gespeichert. SkyReport sendet es, sobald eine Verbindung besteht.',
  'home.searchTitle': 'Fluggebiet suchen',
  'home.searchPlaceholder': 'Fluggebiet suchen…',
  'home.reportEvent': 'Ereignis melden',
  'home.flewToday': 'Heute geflogen — kein Zwischenfall',
  'home.flewTodaySub': 'Drei Felder. Zehn Sekunden.',
  'home.recentSignals': 'Aktuelle Signale',
  'home.sitesActivity': 'Gebiete mit Aktivität',
  'home.patternSummary': 'Musterübersicht',

  'signals.title': 'Signale',
  'signals.lede': 'Ein Signal ist ein Muster, das SkyReport in mehreren Meldungen gefunden hat. Es ist kein Unfall und keine Sicherheitsbewertung.',
  'signals.related': '{n} zugehörige Meldungen', 'signals.viewRelated': 'Zugehörige Meldungen ansehen',
  'signals.rule': 'Regel', 'signals.disclaimer': 'Aus den verfügbaren Daten abgeleitetes Signal, keine abschließende Sicherheitsbewertung.',
  'strength.limited': 'Begrenzte Daten', 'strength.repeated': 'Wiederkehrendes Muster',
  'strength.strong': 'Stark wiederkehrendes Muster',

  'safeFlight.title': 'Heute geflogen — kein Zwischenfall',
  'safeFlight.lede': 'Ein Flug, bei dem nichts passiert ist. Drei Felder und fertig.',
  'safeFlight.site': 'Gebiet', 'safeFlight.date': 'Datum', 'safeFlight.type': 'Flugart',
  'safeFlight.log': 'Diesen Flug erfassen', 'safeFlight.logged': 'Flug erfasst — danke',
  'safeFlight.chooseSite': 'Gebiet wählen…',
  'report.title': 'Melden', 'report.step.type': 'Art', 'report.step.basics': 'Basis',
  'report.step.conditions': 'Bedingungen', 'report.step.equipment': 'Ausrüstung',
  'report.step.igc': 'IGC', 'report.step.narrative': 'Schilderung',
  'report.submit': 'Meldung senden',
  'igc.drop': 'IGC-Datei hier ablegen', 'igc.cantParse': 'Diese IGC-Datei konnte nicht gelesen werden.',
  'igc.tryAnother': 'Andere Datei versuchen', 'igc.continueWithout': 'Ohne IGC fortfahren',
  'method.title': 'Wie SkyReport funktioniert',
  'lang.label': 'Sprache',
  'update.available': 'Eine neue Version von SkyReport ist verfügbar.',
  'update.refresh': 'Aktualisieren',
};

const PT = {
  'nav.home': 'Início', 'nav.map': 'Mapa', 'nav.report': 'Reportar',
  'nav.signals': 'Sinais', 'nav.sites': 'Locais', 'nav.methodology': 'Método',
  'brand.tagline': 'Inteligência de segurança comunitária para voo livre',
  'common.reports': 'relatos', 'common.flightsLogged': 'voos registados',
  'common.back': 'Voltar', 'common.continue': 'Continuar', 'common.next': 'Seguinte',
  'common.submit': 'Enviar', 'common.loading': 'A carregar…', 'common.na': 'N/D',
  'common.optional': 'opcional', 'common.demo': 'Dados de demonstração',

  'status.demo': 'Modo de demonstração — estes dados não são um registo de acidentes reais.',
  'status.offline': 'Sem ligação',
  'status.offlineSaved': 'Guardado neste dispositivo. O SkyReport enviará quando houver ligação.',
  'home.searchTitle': 'Procurar um local de voo',
  'home.searchPlaceholder': 'Procurar um local de voo…',
  'home.reportEvent': 'Reportar um evento',
  'home.flewToday': 'Hoje voei — sem incidentes',
  'home.flewTodaySub': 'Três campos. Dez segundos.',
  'home.recentSignals': 'Sinais recentes',
  'home.sitesActivity': 'Locais com atividade',
  'home.patternSummary': 'Resumo de padrões',

  'signals.title': 'Sinais',
  'signals.lede': 'Um sinal é um padrão que o SkyReport encontrou em vários relatos. Não é um acidente nem uma avaliação de segurança.',
  'signals.related': '{n} relatos relacionados', 'signals.viewRelated': 'Ver relatos relacionados',
  'signals.rule': 'Regra', 'signals.disclaimer': 'Sinal derivado dos dados disponíveis, não uma avaliação de segurança definitiva.',
  'strength.limited': 'Dados limitados', 'strength.repeated': 'Padrão repetido',
  'strength.strong': 'Padrão repetido forte',

  'safeFlight.title': 'Hoje voei — sem incidentes',
  'safeFlight.lede': 'Um voo onde nada aconteceu. Três campos e está feito.',
  'safeFlight.site': 'Local', 'safeFlight.date': 'Data', 'safeFlight.type': 'Tipo de voo',
  'safeFlight.log': 'Registar este voo', 'safeFlight.logged': 'Voo registado — obrigado',
  'safeFlight.chooseSite': 'Escolher um local…',
  'report.title': 'Reportar', 'report.step.type': 'Tipo', 'report.step.basics': 'Básico',
  'report.step.conditions': 'Condições', 'report.step.equipment': 'Equipamento',
  'report.step.igc': 'IGC', 'report.step.narrative': 'Narrativa',
  'report.submit': 'Enviar relato',
  'igc.drop': 'Arraste um ficheiro IGC para aqui', 'igc.cantParse': 'Não foi possível ler este ficheiro IGC.',
  'igc.tryAnother': 'Tentar outro ficheiro', 'igc.continueWithout': 'Continuar sem IGC',
  'method.title': 'Como funciona o SkyReport',
  'lang.label': 'Idioma',
  'update.available': 'Está disponível uma nova versão do SkyReport.',
  'update.refresh': 'Atualizar',
};

/* ============================================================
   MOTOR
   ============================================================ */
const DIC = { en: EN, es: ES, fr: FR, de: DE, pt: PT };

const idDePais = {
  ES:'es', MX:'es', AR:'es', CL:'es', CO:'es', PE:'es', UY:'es', EC:'es', VE:'es', BO:'es', PY:'es', CR:'es', GT:'es', CU:'es', DO:'es', HN:'es', NI:'es', PA:'es', PR:'es', SV:'es',
  FR:'fr', BE:'fr', CH:'fr', CA:'fr', LU:'fr', MC:'fr', SN:'fr', CI:'fr', ML:'fr', BF:'fr',
  DE:'de', AT:'de', LI:'de',
  PT:'pt', BR:'pt', AO:'pt', MZ:'pt', CV:'pt', GW:'pt', ST:'pt', TL:'pt',
  GB:'en', US:'en', AU:'en', NZ:'en', IE:'en', ZA:'en', IN:'en', SG:'en', PH:'en', NG:'en', KE:'en',
};

/** Idioma por la zona horaria, que es más fiable que el navegador. */
function porZonaHoraria() {
  try {
    const z = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
    if (/^America\/(Mexico|Monterrey|Tijuana|Cancun|Merida)/.test(z)) return 'es';
    if (/^Europe\/(Madrid|Lisbon)/.test(z)) return z.includes('Lisbon') ? 'pt' : 'es';
    if (/^America\/(Sao_Paulo|Bahia|Fortaleza|Recife|Belem|Manaus|Cuiaba|Campo_Grande|Maceio|Salvador|Santarem|Porto_Velho|Rio_Branco|Boa_Vista|Noronha)/.test(z)) return 'pt';
    if (/^Europe\/(Paris|Brussels|Zurich|Luxembourg|Monaco)/.test(z)) return 'fr';
    if (/^Europe\/(Berlin|Vienna|Vaduz)/.test(z)) return 'de';
    if (/^Atlantic\/(Canary|Azores|Madeira)/.test(z)) return 'es';
    if (/^America\//.test(z)) return 'es';
  } catch (e) { /* da igual: se cae al navegador */ }
  return null;
}

function delNavegador() {
  const l = (navigator.languages && navigator.languages[0]) || navigator.language || '';
  const dos = l.slice(0, 2).toLowerCase();
  return DIC[dos] ? dos : null;
}

export function idiomaGuardado() {
  try {
    const g = localStorage.getItem(CLAVE);
    if (g && DIC[g]) return g;
  } catch (e) {}
  return null;
}

export function detectaIdioma() {
  const guardado = idiomaGuardado();
  if (guardado) return guardado;
  return delNavegador() || porZonaHoraria() || 'en';
}

let ACTUAL = 'en';

export function idioma() { return ACTUAL; }

export function ponIdioma(id, guardar = true) {
  ACTUAL = DIC[id] ? id : 'en';
  if (guardar) { try { localStorage.setItem(CLAVE, ACTUAL); } catch (e) {} }
  try { document.documentElement.lang = ACTUAL; } catch (e) {}
  return ACTUAL;
}

/** Traduce una clave. Los {x} se sustituyen por el objeto de datos. */
export function t(clave, datos) {
  const d = DIC[ACTUAL] || EN;
  let txt = d[clave];
  if (txt === undefined) txt = EN[clave];       /* respaldo al inglés */
  if (txt === undefined) return clave;          /* nunca un hueco vacío */
  if (datos) {
    txt = txt.replace(/\{(\w+)\}/g, (m, k) =>
      datos[k] === undefined || datos[k] === null ? m : String(datos[k]));
  }
  return txt;
}

/** Igual que t(), pero para textos que llevan HTML dentro. */
export function th(clave, datos) { return t(clave, datos); }

export function idiomasDisponibles() { return IDIOMAS; }

/* Traduce de una vez todos los elementos que lleven data-i18n.
   Así el HTML no tiene texto escrito a mano. */
export function traducePantalla(raiz = document) {
  raiz.querySelectorAll('[data-i18n]').forEach(el => {
    const k = el.dataset.i18n;
    if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
      if (el.dataset.i18nAtr === 'placeholder') el.placeholder = t(k);
      else el.value = t(k);
    } else {
      el.textContent = t(k);
    }
  });
  raiz.querySelectorAll('[data-i18n-ph]').forEach(el => { el.placeholder = t(el.dataset.i18nPh); });
  raiz.querySelectorAll('[data-i18n-title]').forEach(el => { el.title = t(el.dataset.i18nTitle); });
}
