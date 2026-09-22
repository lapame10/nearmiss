/* ============================================================
   SkyReport — motor de señales y análisis
   ============================================================

   Esto es lo que convierte reportes sueltos en algo útil.

   REGLA DE ORO: un Signal NUNCA es una verdad. Es una observacion
   de los datos que hay. Cada senal lleva escrito QUE regla la ha
   disparado, para que cualquiera pueda discutirla. Si una senal no
   se puede explicar, no se publica.

   De momento son reglas simples y transparentes, a proposito. No
   hay machine learning ni falta que hace: con pocos datos, una
   caja negra seria peor que no tener nada.
   ============================================================ */

import { EVENTOS, FASES, SITES, DIRECCIONES, diasEntre } from './data.js';
import { t } from './i18n.js';

/* ---------- utilidades ---------- */
const dias = (a, b) => Math.abs((new Date(a) - new Date(b)) / 86400000);

/** distancia en km entre dos puntos (haversine) */
export function distKm(la1, lo1, la2, lo2) {
  const R = 6371, r = Math.PI / 180;
  const dla = (la2 - la1) * r, dlo = (lo2 - lo1) * r;
  const x = Math.sin(dla / 2) ** 2 +
    Math.cos(la1 * r) * Math.cos(la2 * r) * Math.sin(dlo / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(x));
}

/* Los nombres de evento, fase y resultado salen del diccionario, para
   que la app entera cambie de idioma y no solo la mitad. */
const nombreEv = (id) => t('ev.' + id);
const nombreFase = (id) => t('fa.' + id);
export const nombreSitio = (id) => (SITES.find(s => s.id === id) || {}).n || id;
const zonaDe = (rep) => {
  const s = SITES.find(x => x.id === rep.site);
  return s ? (s.zonas || []).find(z => z.id === rep.zona) : null;
};

/* ============================================================
   FUERZA DEL PATRÓN — NO ES UN NIVEL DE PELIGRO
   ============================================================
   Antes esto se llamaba "elevated / watch / informational", que
   suena a semáforo y da a entender que la app está diciendo que
   un sitio es peligroso. No es eso y no puede serlo: SkyReport no
   tiene forma de saberlo.

   Lo único que puede describir es CUÁNTA EVIDENCIA RELACIONADA
   existe. Eso es todo. Estos tres nombres dicen exactamente eso y
   nada más:

     limited    pocos reportes: puede ser casualidad
     repeated   se repite: merece una mirada
     strong     se repite mucho y con condiciones en común

   Con MÁS reportes no se sabe si es más peligroso: también puede
   ser que simplemente haya más gente volando y más gente
   reportando. Por eso el nombre habla de evidencia, no de riesgo. */
export function fuerza(n, extra = 0) {
  const t = n + extra;
  if (t >= 6 || extra >= 2) return 'strong';
  if (t >= 4 || extra >= 1) return 'repeated';
  return 'limited';
}
export const FUERZA_TXT = {
  limited: 'Limited data',
  repeated: 'Repeated pattern',
  strong: 'Strong repeated pattern',
};
/* compatibilidad: el nombre viejo sigue funcionando */
export const NIVEL_TXT = FUERZA_TXT;
function nivel(n, extra = 0) { return fuerza(n, extra); }

/* ============================================================
   REGLAS
   Cada regla recibe todos los reportes y devuelve senales.
   Anadir una regla nueva = anadir una entrada a esta lista.
   ============================================================ */

/** R1 — Varios eventos del MISMO tipo, cerca y en poco tiempo. */
function r1_clusterLocal(reps) {
  const out = [];
  const porTipo = {};
  reps.forEach(r => { (porTipo[r.evento] = porTipo[r.evento] || []).push(r); });

  Object.entries(porTipo).forEach(([ev, lista]) => {
    const vistas = new Set();
    lista.forEach(a => {
      if (vistas.has(a.id)) return;
      /* todos los que estan a menos de 2 km y 30 dias de `a` */
      const grupo = lista.filter(b =>
        distKm(a.lat, a.lon, b.lat, b.lon) <= 2 &&
        dias(a.fecha, b.fecha) <= 30);
      if (grupo.length < 3) return;
      grupo.forEach(g => vistas.add(g.id));

      const fechas = grupo.map(g => g.fecha).sort();
      const vientos = cuenta(grupo.map(g => g.windDir).filter(Boolean));
      const [vMas, nV] = primero(vientos);
      const z = zonaDe(a);
      const graves = grupo.filter(g => g.reserve || g.injury === 'minor' ||
        g.injury === 'serious' || g.injury === 'fatal').length;

      out.push({
        id: 'SIG-' + ev + '-' + a.site + '-' + a.id,
        regla: 'R1',
        explicacion: t('signals.exp1', { n: grupo.length, e: nombreEv(ev).toLowerCase(),
          km: radio(grupo), a: fechas[0], b: fechas[fechas.length - 1], g: graves }),
        titulo: t('sg.r1') + ' · ' + nombreEv(ev),
        site: a.site,
        zona: z ? z.n : null,
        zonaTipo: z ? z.t : null,
        n: grupo.length,
        desde: fechas[0], hasta: fechas[fechas.length - 1],
        condicion: nV >= Math.ceil(grupo.length / 2) && vMas
          ? t('cond.windDir', { d: vMas }) : null,
        fuerza: fuerza(grupo.length, graves >= 1 && grupo.some(g => g.reserve) ? 2 : (graves >= 2 ? 1 : 0)),
        nivel: fuerza(grupo.length, 0),
        radioKm: radio(grupo),
        dias: diasEntre(fechas[0], fechas[fechas.length - 1]) + 1,
        franja: franjaComun(grupo),
        reps: grupo.map(g => g.id),
        lat: a.lat, lon: a.lon,
      });
    });
  });
  return out;
}

/** R2 — Mismo tipo de evento, mismo sitio, bajo la MISMA direccion de viento. */
function r2_mismoViento(reps) {
  const out = [];
  const grupos = {};
  reps.filter(r => r.windDir).forEach(r => {
    const k = r.site + '|' + r.evento + '|' + r.windDir;
    (grupos[k] = grupos[k] || []).push(r);
  });
  Object.entries(grupos).forEach(([k, grupo]) => {
    if (grupo.length < 3) return;
    const [site, ev, dir] = k.split('|');
    const fechas = grupo.map(g => g.fecha).sort();
    out.push({
      id: 'SIG-V-' + k,
      regla: 'R2',
      explicacion: t('signals.exp2', { n: grupo.length, e: nombreEv(ev).toLowerCase(),
        d: dir, o: otrasDirs }),
      titulo: t('sg.r2') + ' · ' + nombreEv(ev),
      site, zona: null, zonaTipo: null,
      n: grupo.length, desde: fechas[0], hasta: fechas[fechas.length - 1],
      condicion: t('cond.windDir', { d: dir }),
      fuerza: fuerza(grupo.length), nivel: fuerza(grupo.length),
      radioKm: radio(grupo), dias: diasEntre(fechas[0], fechas[fechas.length - 1]) + 1,
      reps: grupo.map(g => g.id),
      lat: grupo[0].lat, lon: grupo[0].lon,
    });
  });
  return out;
}

/** R3 — Misma zona concreta del sitio. Aqui esta el valor de las geozonas. */
function r3_mismaZona(reps) {
  const out = [];
  const grupos = {};
  reps.filter(r => r.zona).forEach(r => {
    (grupos[r.site + '|' + r.zona] = grupos[r.site + '|' + r.zona] || []).push(r);
  });
  Object.entries(grupos).forEach(([k, grupo]) => {
    if (grupo.length < 3) return;
    const [site, zonaId] = k.split('|');
    const s = SITES.find(x => x.id === site);
    const z = s && (s.zonas || []).find(x => x.id === zonaId);
    if (!z) return;
    const fechas = grupo.map(g => g.fecha).sort();
    const evs = cuenta(grupo.map(g => g.evento));
    const [evMas] = primero(evs);
    const dirs = cuenta(grupo.map(g => g.windDir).filter(Boolean));
    const [dir] = primero(dirs);
    out.push({
      id: 'SIG-Z-' + k,
      regla: 'R3',
      explicacion: t('signals.exp3', { n: grupo.length, z: z.n }),
      titulo: t('sg.r3') + ` · ${z.n}`,
      site, zona: z.n, zonaTipo: z.t,
      n: grupo.length, desde: fechas[0], hasta: fechas[fechas.length - 1],
      condicion: dir ? t('cond.windDir', { d: dir }) : null,
      fuerza: fuerza(grupo.length), nivel: fuerza(grupo.length),
      radioKm: radio(grupo), dias: diasEntre(fechas[0], fechas[fechas.length - 1]) + 1,
      reps: grupo.map(g => g.id),
      lat: z.lat, lon: z.lon,
    });
  });
  return out;
}

/** R4 — Concentracion por franja horaria. */
function r4_franja(reps) {
  const out = [];
  const porSite = {};
  reps.filter(r => r.hora).forEach(r => {
    (porSite[r.site] = porSite[r.site] || []).push(r);
  });
  Object.entries(porSite).forEach(([site, lista]) => {
    const franjas = { '06-10': 0, '10-13': 0, '13-16': 0, '16-19': 0, '19-22': 0 };
    lista.forEach(r => {
      const h = parseInt(r.hora.slice(0, 2), 10);
      if (h >= 13 && h < 16) franjas['13-16']++;
      else if (h >= 16 && h < 19) franjas['16-19']++;
      else if (h >= 10 && h < 13) franjas['10-13']++;
      else if (h >= 6 && h < 10) franjas['06-10']++;
      else franjas['19-22']++;
    });
    const [tramo, n] = primero(franjas);
    const pct = Math.round(n / lista.length * 100);
    if (n < 4 || pct < 40) return;
    const grupo = lista.filter(r => {
      const h = parseInt(r.hora.slice(0, 2), 10);
      return tramo === '13-16' ? (h >= 13 && h < 16) : tramo === '16-19' ? (h >= 16 && h < 19) :
        tramo === '10-13' ? (h >= 10 && h < 13) : tramo === '06-10' ? (h >= 6 && h < 10) : h >= 19;
    });
    const fechas = grupo.map(g => g.fecha).sort();
    out.push({
      id: 'SIG-H-' + site + '-' + tramo,
      regla: 'R4',
      explicacion: t('signals.exp4', { p: pct, a: tramo.split('-')[0] + ':00',
        b: tramo.split('-')[1] + ':00' }),
      titulo: t('sg.r4') + ` · ${tramo.replace('-', ':00–')}:00`,
      site, zona: null, zonaTipo: null,
      n: grupo.length, desde: fechas[0], hasta: fechas[fechas.length - 1],
      condicion: t('cond.timeOfDay'),
      fuerza: fuerza(grupo.length), nivel: fuerza(grupo.length),
      radioKm: radio(grupo), dias: diasEntre(fechas[0], fechas[fechas.length - 1]) + 1,
      /* OJO: la franja SIEMPRE va como objeto {tramo, n}, nunca como
         string suelto. Antes R4 la ponía como texto y R1 como objeto, y la
         tarjeta de señal reventaba al pintar. */
      franja: { tramo, n: grupo.length },
      reps: grupo.map(g => g.id),
      lat: lista[0].lat, lon: lista[0].lon,
    });
  });
  return out;
}

/** R5 — Despliegues de reserva recientes. Cuenta doble a proposito. */
function r5_reservas(reps) {
  const out = [];
  const porSite = {};
  reps.filter(r => r.reserve || r.evento === 'reserve').forEach(r => {
    (porSite[r.site] = porSite[r.site] || []).push(r);
  });
  Object.entries(porSite).forEach(([site, grupo]) => {
    if (grupo.length < 2) return;
    const fechas = grupo.map(g => g.fecha).sort();
    const dirs = cuenta(grupo.map(g => g.windDir).filter(Boolean));
    const [dir] = primero(dirs);
    out.push({
      id: 'SIG-R-' + site,
      regla: 'R5',
      explicacion: t('signals.exp5', { n: grupo.length, d: dias }),
      titulo: t('sg.r5'),
      site, zona: null, zonaTipo: null,
      n: grupo.length, desde: fechas[0], hasta: fechas[fechas.length - 1],
      condicion: dir ? t('cond.windDir', { d: dir }) : null,
      fuerza: 'strong', nivel: 'strong',
      radioKm: radio(grupo), dias: diasEntre(fechas[0], fechas[fechas.length - 1]) + 1,
      reps: grupo.map(g => g.id),
      lat: grupo[0].lat, lon: grupo[0].lon,
    });
  });
  return out;
}

/** R6 — Reportes con viento fuerte. */
function r6_vientoFuerte(reps) {
  const out = [];
  const fuertes = reps.filter(r => (r.windKmh || 0) >= 20);
  const porSite = {};
  fuertes.forEach(r => { (porSite[r.site] = porSite[r.site] || []).push(r); });
  Object.entries(porSite).forEach(([site, grupo]) => {
    if (grupo.length < 3) return;
    const fechas = grupo.map(g => g.fecha).sort();
    const media = Math.round(grupo.reduce((a, b) => a + (b.windKmh || 0), 0) / grupo.length);
    out.push({
      id: 'SIG-W-' + site,
      regla: 'R6',
      explicacion: t('signals.exp6', { n: grupo.length, m: media }),
      titulo: t('sg.r6'),
      site, zona: null, zonaTipo: null,
      n: grupo.length, desde: fechas[0], hasta: fechas[fechas.length - 1],
      condicion: t('cond.windAvg', { v: media }),
      fuerza: fuerza(grupo.length, 1), nivel: fuerza(grupo.length, 1),
      radioKm: radio(grupo), dias: diasEntre(fechas[0], fechas[fechas.length - 1]) + 1,
      reps: grupo.map(g => g.id),
      lat: grupo[0].lat, lon: grupo[0].lon,
    });
  });
  return out;
}

/* ---------- helpers de conteo ---------- */

/** Radio aproximado del grupo, en km: la distancia maxima entre dos
 *  de sus reportes. Sirve para poder decir "1.4 km area" en vez de
 *  una cifra que nadie sabe interpretar. */
function radio(grupo) {
  let max = 0;
  for (let i = 0; i < grupo.length; i++)
    for (let j = i + 1; j < grupo.length; j++) {
      const d = distKm(grupo[i].lat, grupo[i].lon, grupo[j].lat, grupo[j].lon);
      if (d > max) max = d;
    }
  return +max.toFixed(1);
}

/** La franja horaria en la que cayeron mas reportes del grupo. */
function franjaComun(grupo) {
  const c = {};
  grupo.forEach(r => {
    if (!r.hora) return;
    const h = parseInt(r.hora.slice(0, 2), 10);
    const t = h < 10 ? '06-10' : h < 13 ? '10-13' : h < 16 ? '13-16' : h < 19 ? '16-19' : '19-22';
    c[t] = (c[t] || 0) + 1;
  });
  const e = Object.entries(c).sort((a, b) => b[1] - a[1])[0];
  if (!e || e[1] < 2) return null;
  return { tramo: e[0], n: e[1] };
}

/* ============================================================
   CONTEXTO DE EXPOSICIÓN — EL DENOMINADOR
   ============================================================
   Esto es lo que evita el error más fácil y más grave de una
   plataforma así: decir que un sitio es peligroso porque tiene
   más reportes. Un sitio con 5.000 vuelos al año y 50 reportes
   puede estar mejor que uno con 200 vuelos y 10 reportes.

   Si hay vuelos registrados suficientes, se enseña la cifra. Si
   no los hay, se dice CLARAMENTE que el dato es limitado, en vez
   de callarse o de dejar que cada uno interprete lo que quiera.

   OJO con el sesgo que queda incluso teniendo denominador: los
   vuelos registrados son los que alguien se molestó en registrar.
   Por eso la interfaz siempre lleva la explicación al lado. */
export function contextoExposicion(sig, repes, vuelos, minVuelos = 30) {
  const ids = new Set(sig.reps);
  const rs = (repes || []).filter(r => ids.has(r.id));
  const dias = sig.dias || 30;

  /* los vuelos del MISMO sitio y en un periodo parecido */
  const delSitio = (vuelos || []).filter(v => v.site === sig.site);
  const fechaFin = sig.hasta || null;
  const comparables = fechaFin
    ? delSitio.filter(v => {
        const dd = Math.abs(diasEntre(v.fecha, fechaFin));
        return dd <= Math.max(dias, 45);
      })
    : delSitio;

  const hayDatos = comparables.length >= minVuelos;
  return {
    reportes: rs.length,
    vuelos: comparables.length,
    vuelosTotalesSitio: delSitio.length,
    suficiente: hayDatos,
    /* solo se calcula la tasa si hay muestra; si no, null */
    tasa: hayDatos ? +(rs.length / comparables.length * 1000).toFixed(1) : null,
  };
}
function cuenta(arr) {
  const c = {};
  arr.forEach(x => { if (x) c[x] = (c[x] || 0) + 1; });
  return c;
}
function primero(obj) {
  const e = Object.entries(obj).sort((a, b) => b[1] - a[1]);
  return e.length ? e[0] : [null, 0];
}

/* ============================================================
   MOTOR
   ============================================================ */
export function detectaSenales(reps) {
  const validos = reps.filter(r => r.tipo !== 'safe_flight');
  const todas = [
    ...r5_reservas(validos),
    ...r1_clusterLocal(validos),
    ...r3_mismaZona(validos),
    ...r2_mismoViento(validos),
    ...r4_franja(validos),
    ...r6_vientoFuerte(validos),
  ];
  /* quito duplicados: si dos reglas describen el mismo grupo, me quedo con la
     que tiene mas reportes (y si empatan, con la mas especifica) */
  const vistos = {};
  const fin = [];
  todas.forEach(s => {
    const firma = s.reps.slice().sort().join(',');
    if (vistos[firma]) {
      const otro = vistos[firma];
      if (s.n > otro.n) { fin[fin.indexOf(otro)] = s; vistos[firma] = s; }
      return;
    }
    vistos[firma] = s;
    fin.push(s);
  });
  /* orden: primero las graves, luego por numero de reportes */
  /* el orden usa los nombres NUEVOS (limited/repeated/strong) */
  const peso = { strong: 0, repeated: 1, limited: 2 };
  return fin.sort((a, b) => (peso[a.nivel] - peso[b.nivel]) || (b.n - a.n));
}

/* ============================================================
   REPORTES SIMILARES a uno dado
   ============================================================ */
export function similares(rep, reps, limite = 6) {
  return reps
    .filter(r => r.id !== rep.id)
    .map(r => {
      let p = 0;
      if (r.evento === rep.evento) p += 40;              /* el tipo pesa mas */
      if (r.site === rep.site) p += 15;
      if (r.zona && r.zona === rep.zona) p += 20;
      if (r.fase === rep.fase) p += 10;
      if (r.windDir && r.windDir === rep.windDir) p += 10;
      const km = distKm(rep.lat, rep.lon, r.lat, r.lon);
      if (km <= 2) p += 15; else if (km <= 8) p += 7;
      const dd = dias(rep.fecha, r.fecha);
      if (dd <= 30) p += 10; else if (dd <= 90) p += 4;
      return { r, p, km, dd };
    })
    .filter(x => x.p >= 35)
    .sort((a, b) => b.p - a.p)
    .slice(0, limite);
}

/* ============================================================
   ANÁLISIS POR EXCEPCIÓN
   La idea de telemetria: no ensenar mil datos, ensenar lo raro.
   Aqui se aplica a los tracks IGC.
   ============================================================ */
export function excepciones(track) {
  const out = [];
  if (!track || track.length < 4) return out;
  for (let i = 1; i < track.length; i++) {
    const a = track[i - 1], b = track[i];
    if (b.t > 0) break;                            /* solo antes del evento */
    /* caida fuerte */
    if (b.vs <= -5 && a.vs > -2.5) {
      out.push({ t: b.t, tipo: 'high_sink', txt: `Sudden sink, ${b.vs.toFixed(1)} m/s`,
                 lat: b.lat, lon: b.lon });
    }
    /* giro brusco */
    const dh = Math.abs(((b.heading - a.heading + 540) % 360) - 180);
    if (dh > 60) {
      out.push({ t: b.t, tipo: 'heading', txt: `Abrupt heading change, ${Math.round(dh)}°`,
                 lat: b.lat, lon: b.lon });
    }
    /* perdida de altura anormal en poco tiempo */
    if (a.baroAlt - b.baroAlt > 25) {
      out.push({ t: b.t, tipo: 'descent', txt: `Abnormal descent, ${a.baroAlt - b.baroAlt} m in 5 s`,
                 lat: b.lat, lon: b.lon });
    }
  }
  /* el track se corta de golpe */
  const ult = track[track.length - 1];
  const pen = track[track.length - 2];
  if (pen && ult.hs < 3 && pen.hs > 15) {
    out.push({ t: ult.t, tipo: 'stop', txt: 'Track terminates abruptly', lat: ult.lat, lon: ult.lon });
  }
  return out;
}

/* ============================================================
   COMPLETITUD DEL DATO
   OJO: esto mide la CALIDAD DEL DATO, no al piloto. No es una
   nota de nadie. Solo dice cuanto podemos aprender de un reporte.
   ============================================================ */
export function completitud(rep) {
  const partes = [
    ['ubicación',  r => r.lat != null && r.lon != null, 18],
    ['fecha',      r => !!r.fecha, 12],
    ['fase',       r => !!r.fase, 10],
    ['evento',     r => !!r.evento, 10],
    ['condiciones',r => !!(r.windDir && r.windKmh), 18],
    ['IGC',        r => !!r.igc, 16],
    ['descripción',r => !!(r.factores || r.lecciones), 10],
    ['equipo',     r => !!(r.ala || r.clase), 6],
  ];
  let pct = 0;
  const detalle = partes.map(([n, f, w]) => {
    const ok = !!f(rep);
    if (ok) pct += w;
    return { n, ok, w };
  });
  return { pct, detalle };
}

/* ============================================================
   ESTADÍSTICAS
   ============================================================ */
export function statsSite(site, reps, vuelos) {
  const R = reps.filter(r => r.site === site && r.tipo !== 'safe_flight');
  const V = vuelos.filter(v => v.site === site);
  const c = (xs) => Object.entries(cuenta(xs)).sort((a, b) => b[1] - a[1]);
  const masEvento = c(R.map(r => r.evento))[0];
  const masFase = c(R.map(r => r.fase))[0];
  const masViento = c(R.map(r => r.windDir).filter(Boolean))[0];
  const ultimo = R.slice().sort((a, b) => b.fecha.localeCompare(a.fecha))[0];
  const por1000 = V.length >= 30 ? Math.round(R.length / V.length * 1000) : null;
  return {
    total: R.length,
    nearMiss: R.filter(r => r.tipo === 'near_miss').length,
    reservas: R.filter(r => r.reserve || r.evento === 'reserve').length,
    duras: R.filter(r => r.evento === 'hardlanding').length,
    lesiones: R.filter(r => r.injury && r.injury !== 'none').length,
    vuelos: V.length,
    por1000,
    muestraPequena: V.length < 30,
    masEvento: masEvento ? { id: masEvento[0], n: nombreEv(masEvento[0]), c: masEvento[1] } : null,
    masFase: masFase ? { id: masFase[0], n: nombreFase(masFase[0]), c: masFase[1] } : null,
    masViento: masViento ? { id: masViento[0], c: masViento[1] } : null,
    ultimo,
    reps: R,
  };
}

export function patronesSite(site, reps) {
  const R = reps.filter(r => r.site === site && r.tipo !== 'safe_flight');
  const out = [];
  if (R.length < 3) return out;

  /* Las frases se construyen con t() y datos, para que salgan en el
     idioma que tenga puesto la persona. */
  const porFase = Object.entries(cuenta(R.map(r => r.fase))).sort((a, b) => b[1] - a[1]);
  if (porFase[0]) out.push({
    txt: t('site.patternPhase', {
      p: Math.round(porFase[0][1] / R.length * 100),
      f: nombreFase(porFase[0][0]).toLowerCase(),
    }),
  });

  const porDir = Object.entries(cuenta(R.map(r => r.windDir).filter(Boolean))).sort((a, b) => b[1] - a[1]);
  if (porDir[0] && porDir[0][1] >= 2) out.push({
    txt: t('site.patternWind', { n: porDir[0][1], t: R.length, d: porDir[0][0] }),
  });

  const tarde = R.filter(r => r.hora && parseInt(r.hora.slice(0, 2), 10) >= 13).length;
  if (tarde >= 3) out.push({
    txt: t('site.patternTime', { p: Math.round(tarde / R.length * 100) }),
  });

  const porZona = Object.entries(cuenta(R.map(r => r.zona).filter(Boolean))).sort((a, b) => b[1] - a[1]);
  if (porZona[0] && porZona[0][1] >= 3) {
    const s = SITES.find(x => x.id === site);
    const z = s && (s.zonas || []).find(x => x.id === porZona[0][0]);
    if (z) out.push({ txt: t('site.patternZone', { n: porZona[0][1], z: z.n }) });
  }

  const porEv = Object.entries(cuenta(R.map(r => r.evento))).sort((a, b) => b[1] - a[1]);
  if (porEv[0] && porEv[0][1] >= 2) out.push({
    txt: t('site.patternEvent', { e: nombreEv(porEv[0][0]), n: porEv[0][1] }),
  });

  return out;
}
