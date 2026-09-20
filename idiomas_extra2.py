#!/usr/bin/env python3
"""Parte 2: los nombres de las opciones, el selector de 5 idiomas y la
deteccion por zona horaria (el pais, sin pedir GPS ni llamar a ninguna API)."""
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


# ==========================================================================
# 1) LOS NOMBRES DE LAS OPCIONES, en los 5 idiomas
# ==========================================================================
rep("""const SEVERIDAD = [
  { id:'near',      e:'warning',         es:'Near miss / casi accidente', en:'Near miss' },
  { id:'incidente', e:'error_outline',   es:'Incidente',      en:'Incident' },
  { id:'accidente', e:'report_problem',  es:'Accidente',      en:'Accident' },
  { id:'grave',     e:'personal_injury', es:'Accidente grave', en:'Serious accident' },
  { id:'fatal',     e:'emergency',       es:'Fatalidad',      en:'Fatality' },
];""",
    """const SEVERIDAD = [
  { id:'near',      e:'warning',         es:'Near miss / casi accidente', en:'Near miss',
    fr:'Presque-accident', de:'Beinaheunfall', pt:'Quase-acidente' },
  { id:'incidente', e:'error_outline',   es:'Incidente',        en:'Incident',
    fr:'Incident', de:'Zwischenfall', pt:'Incidente' },
  { id:'accidente', e:'report_problem',  es:'Accidente',        en:'Accident',
    fr:'Accident', de:'Unfall', pt:'Acidente' },
  { id:'grave',     e:'personal_injury', es:'Accidente grave',  en:'Serious accident',
    fr:'Accident grave', de:'Schwerer Unfall', pt:'Acidente grave' },
  { id:'fatal',     e:'emergency',       es:'Fatalidad',        en:'Fatality',
    fr:'Accident mortel', de:'Tödlicher Unfall', pt:'Fatalidade' },
];""")

rep("""const SITUACION = [
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
];""",
    """const SITUACION = [
  { id:'plegada',    e:'air',            es:'Plegada o cierre',         en:'Collapse or closure',
    fr:'Fermeture', de:'Einklapper', pt:'Fechamento' },
  { id:'proximidad', e:'groups',         es:'Proximidad entre pilotos', en:'Close to another pilot',
    fr:'Proximité entre pilotes', de:'Nähe zu anderen Piloten', pt:'Proximidade entre pilotos' },
  { id:'sotavento',  e:'landscape',      es:'Sotavento',                en:'Lee side',
    fr:'Sous le vent', de:'Lee-Seite', pt:'Sotavento' },
  { id:'rotor',      e:'storm',          es:'Rotor o turbulencia',      en:'Rotor or turbulence',
    fr:'Rotor ou turbulence', de:'Rotor oder Turbulenz', pt:'Rotor ou turbulência' },
  { id:'cable',      e:'cable',          es:'Cable o tendido',          en:'Cable or power line',
    fr:'Câble ou ligne électrique', de:'Kabel oder Stromleitung', pt:'Cabo ou linha elétrica' },
  { id:'arbol',      e:'forest',         es:'Árbol o zona arbolada',    en:'Tree or wooded area',
    fr:'Arbre ou zone boisée', de:'Baum oder Waldgebiet', pt:'Árvore ou zona arborizada' },
  { id:'despegue',   e:'flight_takeoff', es:'Despegue',                 en:'Launch',
    fr:'Décollage', de:'Start', pt:'Descolagem' },
  { id:'aterrizaje', e:'flight_land',    es:'Aterrizaje',               en:'Landing',
    fr:'Atterrissage', de:'Landung', pt:'Aterragem' },
  { id:'bajo',       e:'trending_down',  es:'Quedarse bajo',            en:'Getting low',
    fr:'Rester trop bas', de:'Zu tief geraten', pt:'Ficar baixo' },
  { id:'otro',       e:'more_horiz',     es:'Otro',                     en:'Other',
    fr:'Autre', de:'Sonstiges', pt:'Outro' },
];""")

rep("""const CONSEC = [
  { id:'sin',    e:'check_circle',    es:'Sin lesiones',      en:'No injuries' },
  { id:'leves',  e:'healing',         es:'Lesiones leves',    en:'Minor injuries' },
  { id:'graves', e:'personal_injury', es:'Lesiones graves',   en:'Serious injuries' },
  { id:'danos',  e:'car_crash',       es:'Daños materiales',  en:'Material damage' },
  { id:'fatal',  e:'emergency',       es:'Fatalidad',         en:'Fatality' },
];""",
    """const CONSEC = [
  { id:'sin',    e:'check_circle',    es:'Sin lesiones',     en:'No injuries',
    fr:'Aucune blessure', de:'Keine Verletzungen', pt:'Sem lesões' },
  { id:'leves',  e:'healing',         es:'Lesiones leves',   en:'Minor injuries',
    fr:'Blessures légères', de:'Leichte Verletzungen', pt:'Lesões leves' },
  { id:'graves', e:'personal_injury', es:'Lesiones graves',  en:'Serious injuries',
    fr:'Blessures graves', de:'Schwere Verletzungen', pt:'Lesões graves' },
  { id:'danos',  e:'car_crash',       es:'Daños materiales', en:'Material damage',
    fr:'Dégâts matériels', de:'Sachschaden', pt:'Danos materiais' },
  { id:'fatal',  e:'emergency',       es:'Fatalidad',        en:'Fatality',
    fr:'Accident mortel', de:'Tödlicher Unfall', pt:'Fatalidade' },
];""")

rep("""const FASES = [
  { id:'despegue',     es:'Despegue',            en:'Launch' },
  { id:'termica',      es:'Térmica / ascenso',   en:'Thermal / climb' },
  { id:'transito',     es:'Tránsito',            en:'Transition' },
  { id:'aproximacion', es:'Aproximación',        en:'Approach' },
  { id:'aterrizaje',   es:'Aterrizaje',          en:'Landing' },
];""",
    """const FASES = [
  { id:'despegue',     es:'Despegue',          en:'Launch',
    fr:'Décollage', de:'Start', pt:'Descolagem' },
  { id:'termica',      es:'Térmica / ascenso', en:'Thermal / climb',
    fr:'Thermique / montée', de:'Thermik / Steigen', pt:'Térmica / subida' },
  { id:'transito',     es:'Tránsito',          en:'Transition',
    fr:'Transit', de:'Übergang', pt:'Trânsito' },
  { id:'aproximacion', es:'Aproximación',      en:'Approach',
    fr:'Approche', de:'Anflug', pt:'Aproximação' },
  { id:'aterrizaje',   es:'Aterrizaje',        en:'Landing',
    fr:'Atterrissage', de:'Landung', pt:'Aterragem' },
];""")

rep("""const FRANJAS = [
  { id:'manana',   e:'wb_twilight',   es:'Mañana',   en:'Morning' },
  { id:'mediodia', e:'light_mode',    es:'Mediodía', en:'Midday' },
  { id:'tarde',    e:'wb_sunny',      es:'Tarde',    en:'Afternoon' },
  { id:'noche',    e:'dark_mode',     es:'Noche',    en:'Evening' },
];""",
    """const FRANJAS = [
  { id:'manana',   e:'wb_twilight', es:'Mañana',   en:'Morning',
    fr:'Matin', de:'Morgen', pt:'Manhã' },
  { id:'mediodia', e:'light_mode',  es:'Mediodía', en:'Midday',
    fr:'Midi', de:'Mittag', pt:'Meio-dia' },
  { id:'tarde',    e:'wb_sunny',    es:'Tarde',    en:'Afternoon',
    fr:'Après-midi', de:'Nachmittag', pt:'Tarde' },
  { id:'noche',    e:'dark_mode',   es:'Noche',    en:'Evening',
    fr:'Soir', de:'Abend', pt:'Noite' },
];""")

rep("""const AIRES = [
  { id:'tranquilo',  e:'air',                   es:'Tranquilo',         en:'Calm' },
  { id:'turbulento', e:'waves',                 es:'Turbulento',        en:'Turbulent' },
  { id:'termico',    e:'local_fire_department', es:'Térmico',           en:'Thermal' },
  { id:'fuerte',     e:'storm',                 es:'Con viento fuerte', en:'Strong wind' },
  { id:'variable',   e:'swap_horiz',            es:'Variable',          en:'Variable' },
  { id:'nose',       e:'help',                  es:'No lo sé',          en:'Not sure' },
];""",
    """const AIRES = [
  { id:'tranquilo',  e:'air',                   es:'Tranquilo',   en:'Calm',
    fr:'Calme', de:'Ruhig', pt:'Calmo' },
  { id:'turbulento', e:'waves',                 es:'Turbulento',  en:'Turbulent',
    fr:'Turbulent', de:'Turbulent', pt:'Turbulento' },
  { id:'termico',    e:'local_fire_department', es:'Térmico',     en:'Thermal',
    fr:'Thermique', de:'Thermisch', pt:'Térmico' },
  { id:'fuerte',     e:'storm',                 es:'Con viento fuerte', en:'Strong wind',
    fr:'Vent fort', de:'Starker Wind', pt:'Vento forte' },
  { id:'variable',   e:'swap_horiz',            es:'Variable',    en:'Variable',
    fr:'Variable', de:'Wechselhaft', pt:'Variável' },
  { id:'nose',       e:'help',                  es:'No lo sé',    en:'Not sure',
    fr:'Je ne sais pas', de:'Weiß nicht', pt:'Não sei' },
];""")

# los meses y los puntos cardinales
rep("""const MESES = {
  es: ['enero','febrero','marzo','abril','mayo','junio',
       'julio','agosto','septiembre','octubre','noviembre','diciembre'],
  en: ['January','February','March','April','May','June',
       'July','August','September','October','November','December'],
};""",
    """const MESES = {
  es: ['enero','febrero','marzo','abril','mayo','junio',
       'julio','agosto','septiembre','octubre','noviembre','diciembre'],
  en: ['January','February','March','April','May','June',
       'July','August','September','October','November','December'],
  fr: ['janvier','février','mars','avril','mai','juin',
       'juillet','août','septembre','octobre','novembre','décembre'],
  de: ['Januar','Februar','März','April','Mai','Juni',
       'Juli','August','September','Oktober','November','Dezember'],
  pt: ['janeiro','fevereiro','março','abril','maio','junho',
       'julho','agosto','setembro','outubro','novembro','dezembro'],
};""")

rep("""const CARDINALES = {
  es: ['Norte','Noreste','Este','Sureste','Sur','Suroeste','Oeste','Noroeste'],
  en: ['North','North-east','East','South-east','South','South-west','West','North-west'],
};""",
    """const CARDINALES = {
  es: ['Norte','Noreste','Este','Sureste','Sur','Suroeste','Oeste','Noroeste'],
  en: ['North','North-east','East','South-east','South','South-west','West','North-west'],
  fr: ['Nord','Nord-est','Est','Sud-est','Sud','Sud-ouest','Ouest','Nord-ouest'],
  de: ['Norden','Nordosten','Osten','Südosten','Süden','Südwesten','Westen','Nordwesten'],
  pt: ['Norte','Nordeste','Este','Sudeste','Sul','Sudoeste','Oeste','Noroeste'],
};
const DESDE = { es:'del', en:'from', fr:'du', de:'aus', pt:'de' };""")

rep("""  return (idioma === 'es' ? 'del ' : 'from ') + CARDINALES[idioma][i];""",
    """  return (DESDE[idioma] || 'de') + ' ' + CARDINALES[idioma][i];""")

rep("""  const mm = MESES[idioma][parseInt(p[1], 10) - 1] || '';
  return idioma === 'es' ? (mm + ' ' + p[0]) : (mm + ' ' + p[0]);""",
    """  const mm = MESES[idioma][parseInt(p[1], 10) - 1] || '';
  return mm + ' ' + p[0];""")

# ==========================================================================
# 2) EL SELECTOR: ya no son 2 idiomas, son 5
# ==========================================================================
rep("""    <button id="bIdioma" class="idioma" aria-label="Language">🌐 <span id="idTxt">ES</span></button>""",
    """    <select id="bIdioma" class="idioma" aria-label="Language" title="Idioma / Language">
      <option value="es">🌐 ES</option>
      <option value="en">🌐 EN</option>
      <option value="fr">🌐 FR</option>
      <option value="de">🌐 DE</option>
      <option value="pt">🌐 PT</option>
    </select>""")

rep("""  .nav button.idioma{opacity:.85;border:1px solid rgba(255,255,255,.3);
    padding:7px 12px;font-size:12px;letter-spacing:.4px}
  .nav button.idioma:hover{opacity:1;background:rgba(255,255,255,.1)}""",
    """  /* el selector de idioma: 5 idiomas, discreto, a la derecha del todo */
  .nav select.idioma{background:rgba(255,255,255,.1);color:#fff;border:1px solid rgba(255,255,255,.3);
    border-radius:9px;padding:7px 9px;font-family:inherit;font-size:12px;font-weight:700;
    letter-spacing:.4px;cursor:pointer;-webkit-appearance:none;appearance:none;
    padding-right:22px;
    background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='6'><path d='M0 0h10L5 6z' fill='white' opacity='.7'/></svg>");
    background-repeat:no-repeat;background-position:right 7px center}
  .nav select.idioma option{background:var(--marino);color:#fff}""")

rep("""$('bIdioma').onclick = () => ponIdioma(idioma === 'es' ? 'en' : 'es');""",
    """$('bIdioma').onchange = ev => ponIdioma(ev.target.value);""")

rep("""  /* el boton */
  if ($('idTxt')) $('idTxt').textContent = IDIOMAS[l];""",
    """  /* el selector */
  if ($('bIdioma')) $('bIdioma').value = l;""")

# ==========================================================================
# 3) EL IDIOMA POR PAIS, por la zona horaria (sin GPS y sin APIs)
# ==========================================================================
rep("""/* el idioma, por orden: 1) el de la direccion (?lang=en)  2) el que ya
   eligio antes  3) el del navegador. Asi se puede compartir un enlace en
   ingles con un piloto de otro pais. */
ponIdioma((function(){
  try {
    const q = new URLSearchParams(location.search).get('lang');
    if (q && TXT[q.toLowerCase()]) return q.toLowerCase();
  } catch(e){}
  try {
    const g = localStorage.getItem('sr_idioma');
    if (g && TXT[g]) return g;
  } catch(e){}
  return (navigator.language || 'es').toLowerCase().indexOf('en') === 0 ? 'en' : 'es';
})(), false);""",
    """/* ==========================================================================
   ¿EN QUÉ IDIOMA ABRIR? (idea de Pam: 'que dependa de donde te encuentres')
   --------------------------------------------------------------------------
   Por orden:
     1) ?lang=fr en la direccion (para compartir un enlace ya en un idioma)
     2) lo que la persona eligio la ultima vez
     3) el idioma del NAVEGADOR (navigator.language)
     4) el PAIS, deducido de la ZONA HORARIA del sistema
   El punto 4 no pide GPS, no llama a ninguna API y es instantaneo: la zona
   horaria ya dice en qué pais está el dispositivo (Europe/Paris -> francés).
   Ningún permiso, ningún aviso al usuario.
   ========================================================================== */
const ZONA_IDIOMA = {
  /* español */
  'America/Mexico_City':'es', 'America/Monterrey':'es', 'America/Tijuana':'es',
  'America/Bogota':'es', 'America/Lima':'es', 'America/Santiago':'es',
  'America/Argentina':'es', 'America/Havana':'es', 'America/Caracas':'es',
  'America/Guayaquil':'es', 'America/Asuncion':'es', 'America/Montevideo':'es',
  'America/Guatemala':'es', 'America/El_Salvador':'es', 'America/Tegucigalpa':'es',
  'America/Managua':'es', 'America/Costa_Rica':'es', 'America/Panama':'es',
  'America/Santo_Domingo':'es', 'America/Puerto_Rico':'es', 'America/La_Paz':'es',
  'Europe/Madrid':'es', 'Atlantic/Canary':'es', 'Africa/Equatorial_Guinea':'es',
  /* francés */
  'Europe/Paris':'fr', 'Europe/Brussels':'fr', 'Europe/Monaco':'fr', 'Europe/Luxembourg':'fr',
  'Africa/Dakar':'fr', 'Africa/Abidjan':'fr', 'Africa/Casablanca':'fr', 'Africa/Algiers':'fr',
  'Africa/Tunis':'fr', 'Africa/Bamako':'fr', 'Africa/Ouagadougou':'fr', 'Africa/Niamey':'fr',
  'Africa/Libreville':'fr', 'Africa/Kinshasa':'fr', 'Indian/Reunion':'fr',
  'America/Montreal':'fr', 'America/Toronto':'fr', 'America/Guadeloupe':'fr',
  'America/Martinique':'fr', 'America/Cayenne':'fr',
  /* alemán */
  'Europe/Berlin':'de', 'Europe/Vienna':'de', 'Europe/Zurich':'de',
  'Europe/Luxembourg ':'de', 'Africa/Windhoek':'de',
  /* portugués */
  'Europe/Lisbon':'pt', 'Atlantic/Azores':'pt', 'Atlantic/Madeira':'pt',
  'America/Sao_Paulo':'pt', 'America/Manaus':'pt', 'America/Fortaleza':'pt',
  'America/Belem':'pt', 'America/Recife':'pt', 'America/Bahia':'pt',
  'America/Cuiaba':'pt', 'America/Porto_Velho':'pt', 'America/Rio_Branco':'pt',
  'Africa/Luanda':'pt', 'Africa/Maputo':'pt', 'Africa/Bissau':'pt',
  'Africa/Praia':'pt', 'Asia/Macau':'pt', 'Asia/Dili':'pt',
};
function idiomaPorPais(){
  let tz = '';
  try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch(e){ return null; }
  if (!tz) return null;
  if (ZONA_IDIOMA[tz]) return ZONA_IDIOMA[tz];
  /* si no está exacto, pruebo por la parte de la ciudad o por el prefijo */
  const partes = tz.split('/');
  const zona = partes[0] + '/' + (partes[1] || '');
  if (ZONA_IDIOMA[zona]) return ZONA_IDIOMA[zona];
  for (const k in ZONA_IDIOMA){
    if (tz.indexOf(k) === 0) return ZONA_IDIOMA[k];
  }
  return null;
}

/* el idioma del navegador, si lo reconozco */
function idiomaDelNavegador(){
  const l = (navigator.language || navigator.userLanguage || '').toLowerCase().slice(0, 2);
  return TXT[l] ? l : null;
}

ponIdioma((function(){
  try {                                        /* 1) ?lang= en la dirección */
    const q = new URLSearchParams(location.search).get('lang');
    if (q && TXT[q.toLowerCase()]) return q.toLowerCase();
  } catch(e){}
  try {                                        /* 2) lo que ya eligió */
    const g = localStorage.getItem('sr_idioma');
    if (g && TXT[g]) return g;
  } catch(e){}
  return idiomaDelNavegador()                  /* 3) el del navegador */
      || idiomaPorPais()                       /* 4) el del país (por zona horaria) */
      || 'en';                                 /* 5) inglés por defecto: es el idioma
                                                    franco del parapente */
})(), false);""")

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
