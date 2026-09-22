/* ============================================================
   SkyReport — modelo de datos y datos de demostración
   ============================================================

   ⚠️ IMPORTANTE: TODO lo de este archivo son DATOS DE DEMOSTRACIÓN
   (DEMO DATA). No son accidentes reales. Están inventados para
   poder construir y probar la interfaz. Cuando se conecte el
   backend real, este archivo se sustituye por las llamadas a la
   API y no hace falta tocar ni una vista.

   Dos cosas que NO hay que mezclar nunca:

   REPORT  = un evento individual que envía una persona.
   SIGNAL  = un patrón que calcula SkyReport a partir de VARIOS
             reportes. Nunca es una verdad: es una observación
             basada en los datos disponibles.

   Los SIGNALS de abajo están CALCULADOS por el motor de reglas
   (srs/signals.js) a partir de los REPORTES, no escritos a mano.
   ============================================================ */

export const DEMO = true;

/* ---------- FASES DE VUELO ---------- */
export const FASES = [
  { id:'launch',      n:'Launch' },
  { id:'initial',     n:'Initial climb' },
  { id:'thermalling', n:'Thermalling' },
  { id:'ridge',       n:'Ridge soaring' },
  { id:'transition',  n:'Transition' },
  { id:'gaggle',      n:'Competition gaggle' },
  { id:'glide',       n:'Final glide' },
  { id:'approach',    n:'Approach' },
  { id:'landing',     n:'Landing' },
  { id:'ground',      n:'Ground handling' },
  { id:'other',       n:'Other' },
];

/* ---------- TIPOS DE EVENTO ----------
   Es una lista, no un enum cerrado: añadir uno nuevo es añadir una
   linea aqui y nada mas. */
export const EVENTOS = [
  { id:'asymmetric',   n:'Asymmetric collapse' },
  { id:'frontal',      n:'Frontal collapse' },
  { id:'fullstall',    n:'Full stall' },
  { id:'spin',         n:'Spin' },
  { id:'cravat',       n:'Cravat' },
  { id:'autorotation', n:'Autorotation' },
  { id:'twist',        n:'Twist' },
  { id:'losscontrol',  n:'Loss of control' },
  { id:'reserve',      n:'Reserve deployment' },
  { id:'tree',         n:'Tree landing' },
  { id:'water',        n:'Water landing' },
  { id:'hardlanding',  n:'Hard landing' },
  { id:'collision',    n:'Collision' },
  { id:'midair',       n:'Mid-air collision' },
  { id:'launchinc',    n:'Launch incident' },
  { id:'landinginc',   n:'Landing incident' },
  { id:'turbulence',   n:'Turbulence' },
  { id:'equipment',    n:'Equipment failure' },
  { id:'line',         n:'Line issue' },
  { id:'unknown',      n:'Unknown' },
];

/* ---------- TIPOS DE REPORTE ---------- */
export const TIPOS_REPORTE = [
  { id:'incident',   n:'Incident',
    d:'Something happened and it affected the flight or the pilot.' },
  { id:'near_miss',  n:'Near miss',
    d:'It nearly happened, but nothing came of it. Still valuable.' },
  { id:'hazard',     n:'Hazard observation',
    d:'A condition or feature worth flagging: cables, rotor, a gap in a fence.' },
  { id:'safe_flight',n:'Safe flight log',
    d:'You flew here and nothing happened. Takes ten seconds.' },
];

/* ---------- RESULTADOS ---------- */
export const RESULTADOS = [
  { id:'recovered',  n:'Recovered in flight' },
  { id:'deployed',   n:'Reserve deployed' },
  { id:'landed_safe',n:'Landed safely' },
  { id:'injury',     n:'Injury' },
  { id:'material',   n:'Material damage' },
  { id:'unknown',    n:'Unknown' },
];

/* ---------- SEVERIDAD ---------- */
export const SEVERIDAD = [
  { id:'none',  n:'No injury' },
  { id:'minor', n:'Minor injury' },
  { id:'serious',n:'Serious injury' },
  { id:'fatal', n:'Fatality' },
];

/* ---------- VIENTO ---------- */
export const DIRECCIONES = ['N','NE','E','SE','S','SW','W','NW'];

/* ---------- TIPOS DE ZONA DENTRO DE UN SITIO ----------
   Aqui esta la clave para dejar de hablar solo de "Valle de Bravo":
   un reporte puede apuntar a una microzona concreta. */
export const TIPOS_ZONA = [
  { id:'launch',      n:'Launch' },
  { id:'landing',     n:'Landing' },
  { id:'ridge',       n:'Ridge' },
  { id:'lee',         n:'Lee side' },
  { id:'venturi',     n:'Venturi' },
  { id:'rotor',       n:'Rotor area' },
  { id:'convergence', n:'Convergence area' },
  { id:'cables',      n:'Cables' },
  { id:'hazard',      n:'Terrain hazard' },
  { id:'transition',  n:'Common transition' },
];

/* ============================================================
   SITIOS
   ============================================================ */
export const SITES = [
  {
    id:'valle', n:'Valle de Bravo', pais:'Mexico', region:'Estado de Mexico',
    lat:19.1070, lon:-100.1260, alt:2100,
    desc:'Classic thermal site above a lake. Big air, strong cycles, busy in season.',
    zonas:[
      { id:'v-launch',  n:'Launch (El Peñón)', t:'launch',    lat:19.1120, lon:-100.1220 },
      { id:'v-ridge',   n:'Main ridge',         t:'ridge',     lat:19.1180, lon:-100.1320 },
      { id:'v-lee',     n:'Lee side of main ridge', t:'lee',   lat:19.1215, lon:-100.1400 },
      { id:'v-venturi', n:'Venturi at the gap', t:'venturi',   lat:19.1250, lon:-100.1360 },
      { id:'v-trans',   n:'Lake crossing transition', t:'transition', lat:19.1180, lon:-100.1500 },
      { id:'v-landing', n:'Landing (La Candelaria)', t:'landing', lat:19.1030, lon:-100.1180 },
    ],
  },
  {
    id:'krushevo', n:'Krushevo', pais:'North Macedonia', region:'Pelagonia',
    lat:41.3680, lon:21.2480, alt:1350,
    desc:'High plateau, reliable convergence, competition venue. Long transitions.',
    zonas:[
      { id:'k-launch',  n:'Launch (Mečkin Kamen)', t:'launch', lat:41.3720, lon:21.2420 },
      { id:'k-ridge',   n:'North ridge',     t:'ridge',   lat:41.3760, lon:21.2540 },
      { id:'k-lee',     n:'Lee of north ridge', t:'lee', lat:41.3800, lon:21.2620 },
      { id:'k-conv',    n:'Convergence line', t:'convergence', lat:41.3600, lon:21.2600 },
      { id:'k-landing', n:'Main landing field', t:'landing', lat:41.3640, lon:21.2450 },
    ],
  },
  {
    id:'castelo', n:'Castelo', pais:'Brazil', region:'Espírito Santo',
    lat:-20.6040, lon:-41.1910, alt:850,
    desc:'Inland ridge flying, humid air, strong thermals late in the day.',
    zonas:[
      { id:'c-launch',  n:'Launch (Pedra do Castelo)', t:'launch', lat:-20.6010, lon:-41.1880 },
      { id:'c-ridge',   n:'Main ridge line', t:'ridge', lat:-20.6080, lon:-41.1960 },
      { id:'c-rotor',   n:'Rotor behind the col', t:'rotor', lat:-20.6120, lon:-41.2030 },
      { id:'c-cables',  n:'Cables on the road crossing', t:'cables', lat:-20.6070, lon:-41.1880 },
      { id:'c-landing', n:'Landing field', t:'landing', lat:-20.6060, lon:-41.1900 },
    ],
  },
  {
    id:'pegalajar', n:'Pegalajar', pais:'Spain', region:'Sierra Mágina',
    lat:37.7400, lon:-3.6470, alt:1100,
    desc:'Inland Andalusia. Dry, dusty, sharp thermals and a small landing area.',
    zonas:[
      { id:'p-launch',  n:'Launch (Sierra Mágina)', t:'launch', lat:37.7440, lon:-3.6430 },
      { id:'p-ridge',   n:'East ridge', t:'ridge', lat:37.7460, lon:-3.6520 },
      { id:'p-venturi', n:'Venturi between the two spurs', t:'venturi', lat:37.7480, lon:-3.6580 },
      { id:'p-landing', n:'Village landing', t:'landing', lat:37.7380, lon:-3.6450 },
      { id:'p-hazard',  n:'Rock band on approach', t:'hazard', lat:37.7410, lon:-3.6440 },
    ],
  },
];

/* ============================================================
   REPORTES DE DEMOSTRACIÓN
   Atajos para no repetir: se construyen con una funcion para que
   el archivo siga siendo legible.
   ============================================================ */

/* ============================================================
   FECHAS: NUNCA HARDCODEADAS EN LA LÓGICA REAL
   ============================================================
   La fecha de HOY sale del reloj del dispositivo, en su zona
   horaria local. Ojo con el detalle de siempre:

       new Date().toISOString().slice(0,10)   ← MAL

   Eso convierte a UTC primero. En México (UTC-6), a las 19:00 del
   día 5 eso ya devuelve el día 6. Un formulario que se rellena
   por la tarde aparecería con la fecha de mañana.

   La forma buena es leer los componentes locales uno a uno. */
export function hoyISO(f = new Date()) {
  const p = (n) => String(n).padStart(2, '0');
  return `${f.getFullYear()}-${p(f.getMonth() + 1)}-${p(f.getDate())}`;
}

/** Fecha de hoy menos n días, también en local. */
export function haceDiasISO(n) {
  const f = new Date();
  f.setDate(f.getDate() - n);
  return hoyISO(f);
}

/** Días entre dos fechas ISO (b - a). Sin líos de zonas. */
export function diasEntre(a, b) {
  const pa = new Date(a + 'T00:00:00'), pb = new Date(b + 'T00:00:00');
  return Math.round((pb - pa) / 86400000);
}

/* Los datos de DEMOSTRACIÓN sí llevan fechas fijas relativas a una
   fecha de referencia, para que la demo se vea igual siempre y no
   se vaya desplazando. Están separados a propósito de lo de arriba:
   lo productivo usa el reloj, la demo usa esta constante. */
export const FECHA_DEMO = '2026-09-20';
const d = (dias) => {
  const x = new Date(FECHA_DEMO + 'T12:00:00');
  x.setDate(x.getDate() - dias);
  return hoyISO(x);
};

let _n = 0;
const R = (o) => ({
  id: 'DEMO-' + String(++_n).padStart(3, '0'),
  demo: true,                    /* ← marcados como demostración, uno a uno */
  tipo: 'incident',
  pais: null,
  zona: null,
  windDir: null, windKmh: null, gustKmh: null,
  thermal: null, turb: null, cloud: null,
  injury: 'none', reserve: false,
  ala: null, modelo: null, clase: null, harness: null, reserva: null, exp: null,
  igc: false,
  factores: '', lecciones: '',
  completo: null,
  ...o,
});

export const REPORTS = [
  /* ---------- VALLE DE BRAVO ---------- */
  R({ site:'valle', n:'v1', fecha:d(2), hora:'14:20', lat:19.1216, lon:-100.1402,
      zona:'v-lee', fase:'thermalling', evento:'asymmetric', resultado:'recovered',
      windDir:'NW', windKmh:24, gustKmh:33, thermal:'strong', turb:'moderate', cloud:'few',
      ala:'Ozone', modelo:'Enzo 3', clase:'EN D', exp:'5-10',
      factores:'Lee side of the ridge, wind crossed the spur.',
      lecciones:'The wind was stronger than the valley forecast. Climb on the sunny side, not behind.' }),

  R({ site:'valle', n:'v2', fecha:d(6), hora:'14:50', lat:19.1210, lon:-100.1395,
      zona:'v-lee', fase:'thermalling', evento:'asymmetric', resultado:'recovered',
      windDir:'NW', windKmh:26, gustKmh:35, thermal:'strong', turb:'strong',
      ala:'Gin', modelo:'Leopard', clase:'EN D', exp:'3-5',
      factores:'Same spur, NW wind. Rotor off the ridge behind.',
      lecciones:'If the drift is faster than the climb, move out.' }),

  R({ site:'valle', n:'v3', fecha:d(9), hora:'15:10', lat:19.1225, lon:-100.1415,
      zona:'v-lee', fase:'ridge', evento:'frontal', resultado:'recovered',
      windDir:'NW', windKmh:22, gustKmh:31, thermal:'moderate', turb:'moderate',
      ala:'Niviuk', modelo:'Artik 6', clase:'EN C', exp:'1-3',
      factores:'NW component behind the spur.',
      lecciones:'Ask locally which side of the ridge is working before you commit.' }),

  R({ site:'valle', n:'v4', fecha:d(4), hora:'16:35', lat:19.1035, lon:-100.1185,
      zona:'v-landing', fase:'landing', evento:'hardlanding', resultado:'material',
      windDir:'S', windKmh:14, gustKmh:24, thermal:'moderate', turb:'moderate',
      ala:'Advance', modelo:'Epsilon', clase:'EN B', exp:'1-3',
      factores:'Downwind leg after the lake crossing, late flare.',
      lecciones:'The field gets a wind shadow after 16:00. Come in with margin.' }),

  R({ site:'valle', n:'v5', fecha:d(11), hora:'16:20', lat:19.1040, lon:-100.1190,
      zona:'v-landing', fase:'landing', evento:'hardlanding', resultado:'minor',
      injury:'minor',
      windDir:'S', windKmh:16, gustKmh:26, thermal:'moderate', turb:'moderate',
      ala:'BGD', modelo:'Base', clase:'EN B', exp:'1-3',
      factores:'Thermal off the field at the moment of flare.',
      lecciones:'The last 50 m in this field are bumpy in the afternoon.' }),

  R({ site:'valle', n:'v6', fecha:d(3), hora:'13:40', lat:19.1178, lon:-100.1318,
      zona:'v-ridge', fase:'thermalling', evento:'turbulence', resultado:'landed_safe',
      windDir:'NW', windKmh:28, gustKmh:38, thermal:'strong', turb:'strong',
      ala:'Ozone', modelo:'Delta 4', clase:'EN C', exp:'5-10',
      factores:'Strong cycle at the ridge, gusty.',
      lecciones:'Gusts 38 km/h on the ridge. Not the day to be low.' }),

  R({ site:'valle', n:'v7', fecha:d(15), hora:'12:10', lat:19.1125, lon:-100.1228,
      zona:'v-launch', fase:'ground', evento:'launchinc', resultado:'landed_safe',
      windDir:'NW', windKmh:12, gustKmh:18, thermal:'weak', turb:'light',
      ala:'Skywalk', modelo:'Mesc', clase:'EN B', exp:'<1',
      factores:'Riser twist during inflation in a gusty cycle.',
      lecciones:'Launch was cross by 12:00. The high launch is calmer.' }),

  R({ site:'valle', n:'v8', fecha:d(1), hora:'11:30', lat:19.1180, lon:-100.1500,
      zona:'v-trans', fase:'transition', evento:'asymmetric', resultado:'recovered',
      windDir:'W', windKmh:18, gustKmh:27, thermal:'moderate', turb:'moderate',
      ala:'Gin', modelo:'Bonanza 3', clase:'EN C', exp:'3-5',
      tipos:'near_miss',
      factores:'Mid-lake transition with a collapsing cycle.',
      lecciones:'Cross the lake with altitude, not at the limit.' }),

  /* ---------- KRUSHEVO ---------- */
  R({ site:'krushevo', n:'k1', fecha:d(5), hora:'13:15', lat:41.3795, lon:21.2612,
      zona:'k-lee', fase:'thermalling', evento:'asymmetric', resultado:'recovered',
      windDir:'NW', windKmh:20, gustKmh:29, thermal:'strong', turb:'moderate',
      ala:'Ozone', modelo:'Zeno 2', clase:'EN D', exp:'10+',
      factores:'Lee of the north ridge, crossed by the NW wind.',
      lecciones:'The ridge works on the sunny face. Behind it is a different day.' }),

  R({ site:'krushevo', n:'k2', fecha:d(8), hora:'13:50', lat:41.3810, lon:21.2630,
      zona:'k-lee', fase:'ridge', evento:'frontal', resultado:'recovered',
      windDir:'NW', windKmh:23, gustKmh:32, thermal:'strong', turb:'strong',
      ala:'Niviuk', modelo:'Peak 5', clase:'EN D', exp:'5-10',
      factores:'NW on the lee side.', lecciones:'Stay on the sunny side.' }),

  R({ site:'krushevo', n:'k3', fecha:d(12), hora:'14:05', lat:41.3830, lon:21.2650,
      zona:'k-lee', fase:'thermalling', evento:'reserve', resultado:'deployed',
      injury:'minor', reserve:true,
      windDir:'NW', windKmh:25, gustKmh:36, thermal:'strong', turb:'strong',
      ala:'Ozone', modelo:'Enzo 3', clase:'EN D', exp:'10+',
      igc:true,
      factores:'Cascade of collapses behind the ridge in NW.',
      lecciones:'Behind the ridge on a NW day the air is not the same air.' }),

  R({ site:'krushevo', n:'k4', fecha:d(7), hora:'15:40', lat:41.3650, lon:21.2455,
      zona:'k-landing', fase:'approach', evento:'landinginc', resultado:'landed_safe',
      windDir:'SW', windKmh:19, gustKmh:30, thermal:'moderate', turb:'moderate',
      ala:'Gin', modelo:'Leopard', clase:'EN D', exp:'5-10',
      factores:'Crosswind on final after a late return.', lecciones:'Plan the return with margin.' }),

  R({ site:'krushevo', n:'k5', fecha:d(2), hora:'12:30', lat:41.3590, lon:21.2610,
      zona:'k-conv', fase:'transition', evento:'fullstall', resultado:'recovered',
      windDir:'S', windKmh:8, gustKmh:15, thermal:'weak', turb:'light',
      ala:'Advance', modelo:'Sigma 11', clase:'EN C', exp:'3-5',
      ala2:null,
      lecciones:'Practising in calm air is not the same as recovering when it counts.' }),

  R({ site:'krushevo', n:'k6', fecha:d(16), hora:'11:05', lat:41.3735, lon:21.2430,
      zona:'k-launch', fase:'ground', evento:'launchinc', resultado:'landed_safe',
      windDir:'N', windKmh:10, gustKmh:16, thermal:'weak', turb:'light',
      factores:'Riser caught on the ground.', lecciones:'Check risers before every inflation.' }),

  /* ---------- CASTELO ---------- */
  R({ site:'castelo', n:'c1', fecha:d(3), hora:'15:25', lat:-20.6125, lon:-41.2038,
      zona:'c-rotor', fase:'ridge', evento:'asymmetric', resultado:'recovered',
      windDir:'E', windKmh:17, gustKmh:26, thermal:'strong', turb:'strong',
      ala:'Skywalk', modelo:'Cumeo', clase:'EN C', exp:'3-5',
      factores:'Rotor behind the col.', lecciones:'The col is not a place to be low.' }),

  R({ site:'castelo', n:'c2', fecha:d(10), hora:'15:50', lat:-20.6130, lon:-41.2045,
      zona:'c-rotor', fase:'thermalling', evento:'turbulence', resultado:'landed_safe',
      windDir:'E', windKmh:20, gustKmh:30, thermal:'strong', turb:'strong',
      factores:'Same col, same hour.', lecciones:'After 15:00 the col turns ugly.' }),

  R({ site:'castelo', n:'c3', fecha:d(5), hora:'16:10', lat:-20.6065, lon:-41.1892,
      zona:'c-landing', fase:'landing', evento:'hardlanding', resultado:'material',
      windDir:'E', windKmh:12, gustKmh:20, thermal:'moderate', turb:'moderate',
      factores:'Dust devil crossing the field.', lecciones:'Wait for the dust to settle before final.' }),

  R({ site:'castelo', n:'c4', fecha:d(13), hora:'14:30', lat:-20.6072, lon:-41.1885,
      zona:'c-cables', fase:'approach', evento:'line', resultado:'landed_safe',
      tipo:'hazard', igc:false,
      factores:'Cables on the road crossing are hard to see against the hill.',
      lecciones:'They are there. Look for the poles, not the wires.' }),

  R({ site:'castelo', n:'c5', fecha:d(1), hora:'17:20', lat:-20.6090, lon:-41.1975,
      zona:'c-ridge', fase:'glide', evento:'asymmetric', resultado:'recovered',
      windDir:'E', windKmh:15, gustKmh:24, thermal:'weak', turb:'moderate',
      ala:'Ozone', modelo:'Rush 6', clase:'EN B', exp:'1-3',
      factores:'Late cycle at low altitude.', lecciones:'Late cycles are small and sharp.' }),

  /* ---------- PEGALAJAR ---------- */
  R({ site:'pegalajar', n:'p1', fecha:d(4), hora:'14:45', lat:37.7485, lon:-3.6585,
      zona:'p-venturi', fase:'ridge', evento:'asymmetric', resultado:'recovered',
      windDir:'E', windKmh:21, gustKmh:32, thermal:'strong', turb:'strong',
      ala:'Niviuk', modelo:'Hook 6', clase:'EN B', exp:'1-3',
      factores:'Air accelerating between the two spurs.', lecciones:'The gap is a venturi. Cross high.' }),

  R({ site:'pegalajar', n:'p2', fecha:d(8), hora:'15:00', lat:37.7490, lon:-3.6590,
      zona:'p-venturi', fase:'thermalling', evento:'turbulence', resultado:'landed_safe',
      windDir:'E', windKmh:23, gustKmh:34, thermal:'strong', turb:'strong',
      ala:'Advance', modelo:'Iota 2', clase:'EN C', exp:'3-5',
      factores:'Venturi effect, E wind.', lecciones:'Same place, same wind, same result.' }),

  R({ site:'pegalajar', n:'p3', fecha:d(9), hora:'15:20', lat:37.7415, lon:-3.6445,
      zona:'p-hazard', fase:'approach', evento:'landinginc', resultado:'landed_safe',
      windDir:'S', windKmh:13, gustKmh:22, thermal:'moderate', turb:'moderate',
      factores:'Rock band on approach, needed to stay right.', lecciones:'Keep right of the rocks on the way in.' }),

  R({ site:'pegalajar', n:'p4', fecha:d(14), hora:'13:30', lat:37.7385, lon:-3.6455,
      zona:'p-landing', fase:'landing', evento:'hardlanding', resultado:'minor',
      injury:'minor',
      windDir:'SE', windKmh:17, gustKmh:28, thermal:'strong', turb:'strong',
      factores:'Crosswind and a dry, hard field.', lecciones:'The field is small and it is cross more often than not.' }),

  R({ site:'pegalajar', n:'p5', fecha:d(6), hora:'12:00', lat:37.7465, lon:-3.6525,
      zona:'p-ridge', fase:'transition', evento:'turbulence', resultado:'landed_safe',
      windDir:'E', windKmh:19, gustKmh:29, thermal:'moderate', turb:'moderate',
      tipos:'near_miss',
      factores:'Shear where the ridge ends.', lecciones:'Where the ridge ends, expect the air to change.' }),
];

/* ============================================================
   REGISTROS DE VUELO SIN INCIDENTES (Safe Flight Logs)
   Este es el DENOMINADOR. Sin el, "100 incidentes" no dice nada.
   ============================================================ */
const VUELOS = [
  /* [id, site, diasAtras, tipoVuelo] — se generan varios por sitio */
];
{
  const tipos = ['XC','local','soaring','training','competition'];
  let i = 0;
  const plan = {
    valle: [60, 18, 9], krushevo: [40, 14, 7], castelo: [28, 12, 5], pegalajar: [22, 9, 4],
  };
  Object.entries(plan).forEach(([site, [total, dias, porDia]]) => {
    for (let k = 0; k < total; k++) {
      const dia = Math.floor(k / porDia) * Math.round(dias / (total / porDia));
      VUELOS.push([site, Math.max(0, dia + (k % 3)), tipos[(i + k) % tipos.length]]);
      i++;
    }
  });
}

export const SAFE_LOGS = VUELOS.map(([site, dias, tipo], n) => ({
  id: 'SF-DEMO-' + String(n + 1).padStart(3, '0'),
  site, fecha: d(dias), tipo, anon: true, demo: true,
}));

/* ============================================================
   IGC DE DEMOSTRACIÓN
   Genera un track sintetico alrededor de un punto, con un evento
   en el medio. Es MOCK: cuando exista el parser real, esta
   funcion se sustituye por la lectura del archivo .igc.
   ============================================================ */
export function igcDemo(lat, lon, segundosAntes = 120, segundosDespues = 60) {
  const pts = [];
  const total = segundosAntes + segundosDespues;
  let la = lat + 0.0035, lo = lon - 0.0060, alt = 1980, heading = 55;
  for (let s = -segundosAntes; s <= segundosDespues; s += 5) {
    const t = s <= 0 ? s : s;
    /* giro progresivo para simular una deriva y una correccion brusca */
    heading += 0.5 + (s > -20 && s < 5 ? 4.5 : 0);
    const rad = heading * Math.PI / 180;
    la += Math.cos(rad) * 0.00030;
    lo += Math.sin(rad) * 0.00030;
    /* perfil vertical: ascendente hasta T-10 y caida fuerte en el evento */
    let vs;
    if (s < -10)      { vs = 1.6; }
    else if (s < 0)   { vs = -5.8; }   /* sudden high sink */
    else if (s < 12)  { vs = -3.1; }
    else              { vs = 1.2; }
    alt += vs * 5;
    const viento = s < -10 ? 9.5 : (s < 12 ? 4.2 : 8.0);
    pts.push({
      t: s,                                  /* segundos relativos al EVENTO */
      lat: +la.toFixed(6), lon: +lo.toFixed(6),
      gpsAlt: Math.round(alt), baroAlt: Math.round(alt - 12 + (s % 7)),
      hs: +viento.toFixed(1),                 /* ground speed km/h */
      vs: +vs.toFixed(2),                     /* climb/sink m/s */
      heading: Math.round(heading % 360),
    });
  }
  return pts;
}

/* ============================================================
   ESTADO LOCAL (preferencias y modo backend)
   ============================================================
   Cuando exista backend real, aqui se cambia LOCAL por REMOTO y
   las vistas no se enteran: todas hablan con `db`. */
export const CLAVE_LOCAL = 'skyreport_v2_reportes';
export const CLAVE_VUELOS = 'skyreport_v2_vuelos';

export function guardaLocal(clave, datos) {
  try { localStorage.setItem(clave, JSON.stringify(datos)); return true; }
  catch (e) { return false; }
}
export function leeLocal(clave, po = null) {
  try { const x = localStorage.getItem(clave); return x ? JSON.parse(x) : po; }
  catch (e) { return po; }
}

/* Los reportes que ve la app = los de demostracion + los que haya
   enviado la persona (guardados en el navegador). */
export function todosLosReportes() {
  const mios = leeLocal(CLAVE_LOCAL, []);
  return [...(Array.isArray(mios) ? mios : []), ...REPORTS];
}
export function todosLosVuelos() {
  const mios = leeLocal(CLAVE_VUELOS, []);
  return [...(Array.isArray(mios) ? mios : []), ...SAFE_LOGS];
}
