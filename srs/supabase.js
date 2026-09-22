/* ============================================================
   SkyReport — conexión con Supabase + cola offline
   ============================================================
   Dos trabajos:

   1) Hablar con Supabase (leer reportes aprobados, leer vuelos,
      insertar reportes y vuelos).

   2) NO PERDER NADA SI NO HAY COBERTURA. Esto es crítico: la
      gente reporta desde el sitio de vuelo, donde justo no hay
      señal. Si alguien envía un reporte sin conexión:
        · se guarda en el teléfono
        · se le dice claramente
        · y se envía solo cuando vuelva la cobertura
      Para que no se duplique al reintentar, el id (UUID) lo
      genera el cliente ANTES de enviar. Si el envío se corta a
      medias, el segundo intento lleva el mismo id y la base de
      datos lo rechaza por clave duplicada: eso es exactamente lo
      que queremos.

   Si Supabase no está configurado, todo esto se queda en modo
   demo y no se llama a la red ni una vez.
   ============================================================ */

import { SUPABASE_URL, SUPABASE_ANON_KEY, haySupabase, red, AJUSTES } from './config.js';

const CLAVE_COLA = 'skyreport_cola';
const CLAVE_VOLADAS = 'skyreport_cola_vuelos';

let cliente = null;

/* ============================================================
   ARRANQUE
   ============================================================ */
export async function conecta() {
  if (!haySupabase()) {
    red.modo = 'demo';
    return { ok: false, modo: 'demo' };
  }
  try {
    /* el cliente se carga desde el CDN: así GitHub Pages sigue
       sirviendo la app sin ningún paso de compilación */
    if (!cliente) {
      const { createClient } = await import(
        'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm'
      );
      cliente = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
        auth: { persistSession: false },
        global: { headers: { 'x-application-name': 'skyreport' } },
      });
    }
    /* una consulta mínima para saber si de verdad responde */
    const { error } = await cliente.from('sites').select('id').limit(1);
    if (error) throw error;
    red.modo = 'comunidad';
    red.ultimoError = null;
    return { ok: true, modo: 'comunidad' };
  } catch (e) {
    red.modo = 'sin-conexion';
    red.ultimoError = (e && e.message) || 'unknown error';
    return { ok: false, modo: 'sin-conexion', error: red.ultimoError };
  }
}

export function enModoDemo() { return red.modo !== 'comunidad'; }
export function hayCliente() { return !!cliente; }

/* ============================================================
   UUID EN EL CLIENTE
   ============================================================
   Se genera antes de enviar. Es lo que permite reintentar sin
   duplicar: si el primer envío llegó a medias, el id ya existe
   y el segundo intento se rechaza solo. */
export function uuid() {
  if (crypto && crypto.randomUUID) return crypto.randomUUID();
  /* por si el navegador es viejo: versión 4 hecha a mano */
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
    const r = Math.random() * 16 | 0;
    return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
  });
}

/* ============================================================
   REDONDEO DE COORDENADAS
   ============================================================
   El punto exacto nunca se publica. Se redondea a unos 100 m
   antes de salir del dispositivo. */
export function redondea(v) {
  if (v == null || !isFinite(v)) return null;
  const f = AJUSTES.redondeoGrados;
  return Math.round(v / f) * f;
}

/* ============================================================
   LECTURAS
   ============================================================ */
export async function leeReportes(siteId = null) {
  if (!cliente) return { ok: false, datos: [], motivo: 'sin conexion' };
  try {
    let q = cliente.from('reports')
      .select('*')
      .eq('status', 'approved')
      .order('date', { ascending: false })
      .limit(1000);
    if (siteId) q = q.eq('site_id', siteId);
    const { data, error } = await q;
    if (error) throw error;
    return { ok: true, datos: data || [] };
  } catch (e) {
    red.ultimoError = e.message;
    return { ok: false, datos: [], motivo: e.message };
  }
}

export async function leeVuelos(siteId = null) {
  if (!cliente) return { ok: false, datos: [], motivo: 'sin conexion' };
  try {
    let q = cliente.from('safe_flight_logs').select('*').limit(20000);
    if (siteId) q = q.eq('site_id', siteId);
    const { data, error } = await q;
    if (error) throw error;
    return { ok: true, datos: data || [] };
  } catch (e) {
    return { ok: false, datos: [], motivo: e.message };
  }
}

export async function leeSitios() {
  if (!cliente) return { ok: false, datos: [] };
  try {
    const { data, error } = await cliente.from('sites').select('*').eq('active', true);
    if (error) throw error;
    return { ok: true, datos: data || [] };
  } catch (e) {
    return { ok: false, datos: [], motivo: e.message };
  }
}

export async function leeZonas() {
  if (!cliente) return { ok: false, datos: [] };
  try {
    const { data, error } = await cliente.from('site_zones').select('*');
    if (error) throw error;
    return { ok: true, datos: data || [] };
  } catch (e) {
    return { ok: false, datos: [], motivo: e.message };
  }
}

/* ============================================================
   ESCRITURAS CON COLA
   ============================================================
   Si no hay conexión (o falla), se guarda en el teléfono y se
   dice. Nunca se pierde. */
function encola(clave, item) {
  try {
    const c = JSON.parse(localStorage.getItem(clave) || '[]');
    c.push(item);
    localStorage.setItem(clave, JSON.stringify(c));
    return true;
  } catch (e) { return false; }
}
function desencola(clave) {
  try { return JSON.parse(localStorage.getItem(clave) || '[]'); }
  catch (e) { return []; }
}
function quitaDeCola(clave, id) {
  try {
    const c = desencola(clave).filter(x => x.id !== id);
    localStorage.setItem(clave, JSON.stringify(c));
    return c.length;
  } catch (e) { return 0; }
}

export function pendientes() {
  return desencola(CLAVE_COLA).length + desencola(CLAVE_VOLADAS).length;
}
export function colaReportes() { return desencola(CLAVE_COLA); }
export function colaVuelos() { return desencola(CLAVE_VOLADAS); }

/** Prepara un reporte para la base de datos.
 *  Redondea coordenadas, calcula la completitud y traduce los
 *  nombres de los campos del formulario a los de la tabla. */
export function aFilaReporte(f, completo) {
  return {
    id: f.id || uuid(),
    report_type: f.tipo || 'incident',
    site_id: f.site || null,
    date: f.fecha || null,
    time: f.hora || null,
    latitude: redondea(f.lat),
    longitude: redondea(f.lon),
    zone_id: f.zona || null,
    flight_phase: f.fase || null,
    event_type: f.evento || null,
    outcome: f.resultado || null,
    injury_severity: f.injury || 'none',
    wind_direction: f.windDir || null,
    wind_kmh: f.windKmh ? parseInt(f.windKmh, 10) : null,
    gust_kmh: f.gustKmh ? parseInt(f.gustKmh, 10) : null,
    thermal_activity: f.thermal || null,
    turbulence: f.turb || null,
    cloud_conditions: f.cloud || null,
    weather_notes: f.meteo || null,
    wing_brand: f.ala || null,
    wing_model: f.modelo || null,
    wing_class: f.clase || null,
    wing_size: f.talla || null,
    harness: f.harness || null,
    reserve: f.reserva || null,
    experience_range: f.exp || null,
    description: f.factores || null,
    contributing_factors: f.contrib || null,
    lessons_learned: f.lecciones || null,
    advice: f.recomendar || null,
    has_igc: !!f.igc,
    igc_metadata: f.igcMeta || null,
    additional_event_data: (f.extra && Object.keys(f.extra).length) ? f.extra : null,
    data_completeness: typeof completo === 'number' ? completo : null,
    /* IMPORTANTE: nunca 'approved' desde el navegador. La policy de
       Supabase rechaza el insert si se intenta. */
    status: AJUSTES.autoAprobar ? 'pending' : 'pending',
  };
}

/** Envía un reporte. Si no puede, lo deja en la cola y avisa. */
export async function enviaReporte(f, completo) {
  const fila = aFilaReporte(f, completo);
  if (!cliente || red.modo !== 'comunidad') {
    encola(CLAVE_COLA, fila);
    red.pendientes = pendientes();
    return { ok: false, encolado: true, id: fila.id,
      motivo: 'Saved on this device. SkyReport will submit it when a connection is available.' };
  }
  try {
    const { error } = await cliente.from('reports').insert(fila);
    if (error) throw error;
    return { ok: true, id: fila.id, estado: fila.status };
  } catch (e) {
    encola(CLAVE_COLA, fila);
    red.pendientes = pendientes();
    red.ultimoError = e.message;
    return { ok: false, encolado: true, id: fila.id, motivo: e.message };
  }
}

/** Registra un vuelo sin incidentes. Es el que más se usa, así
 *  que tiene que ser el más ligero. */
export async function enviaVuelo(v) {
  const fila = {
    id: v.id || uuid(),
    site_id: v.site || null,
    date: v.fecha || null,
    flight_type: v.tipo || null,
  };
  if (!cliente || red.modo !== 'comunidad') {
    encola(CLAVE_VOLADAS, fila);
    red.pendientes = pendientes();
    return { ok: false, encolado: true, id: fila.id };
  }
  try {
    const { error } = await cliente.from('safe_flight_logs').insert(fila);
    if (error) throw error;
    return { ok: true, id: fila.id };
  } catch (e) {
    encola(CLAVE_VOLADAS, fila);
    red.pendientes = pendientes();
    return { ok: false, encolado: true, id: fila.id, motivo: e.message };
  }
}

/** Reintenta lo que quedó en la cola. Se llama al arrancar y
 *  cuando el navegador dice que ha vuelto la conexión. */
export async function sincroniza() {
  if (!cliente || red.modo !== 'comunidad') return { enviados: 0, quedan: pendientes() };
  let enviados = 0;

  for (const fila of colaReportes()) {
    try {
      const { error } = await cliente.from('reports').insert(fila);
      /* el 23505 es "clave duplicada": ya había llegado antes,
         así que se quita de la cola y se da por bueno */
      if (error && error.code !== '23505') throw error;
      quitaDeCola(CLAVE_COLA, fila.id);
      enviados++;
    } catch (e) { break; }
  }

  for (const fila of colaVuelos()) {
    try {
      const { error } = await cliente.from('safe_flight_logs').insert(fila);
      if (error && error.code !== '23505') throw error;
      quitaDeCola(CLAVE_VOLADAS, fila.id);
      enviados++;
    } catch (e) { break; }
  }

  red.pendientes = pendientes();
  return { enviados, quedan: red.pendientes };
}

/* ============================================================
   VIGILANTE DE CONEXIÓN
   ============================================================ */
export function vigilaConexion(alCambiar) {
  const avisa = async () => {
    const antes = red.modo;
    if (navigator.onLine) {
      await conecta();
      if (red.modo === 'comunidad') await sincroniza();
    } else {
      red.modo = 'sin-conexion';
    }
    if (alCambiar && red.modo !== antes) alCambiar(red.modo);
  };
  window.addEventListener('online', avisa);
  window.addEventListener('offline', () => {
    red.modo = 'sin-conexion';
    if (alCambiar) alCambiar(red.modo);
  });
  if (navigator.onLine) sincroniza();
}

/* ============================================================
   TRADUCCIÓN DE FILAS
   ============================================================
   La base de datos habla en nombres largos (flight_phase) y la
   interfaz en cortos (fase). Aquí se traduce, en un solo sitio,
   para que las vistas no tengan que saber nada de la tabla. */
export function deFilaReporte(r) {
  return {
    id: r.id,
    tipo: r.report_type,
    site: r.site_id,
    fecha: r.date,
    hora: r.time,
    lat: r.latitude,
    lon: r.longitude,
    zona: r.zone_id,
    fase: r.flight_phase,
    evento: r.event_type,
    resultado: r.outcome,
    injury: r.injury_severity || 'none',
    windDir: r.wind_direction,
    windKmh: r.wind_kmh,
    gustKmh: r.gust_kmh,
    thermal: r.thermal_activity,
    turb: r.turbulence,
    cloud: r.cloud_conditions,
    meteo: r.weather_notes,
    ala: r.wing_brand,
    modelo: r.wing_model,
    clase: r.wing_class,
    talla: r.wing_size,
    harness: r.harness,
    reserva: r.reserve,
    exp: r.experience_range,
    factores: r.description,
    contrib: r.contributing_factors,
    lecciones: r.lessons_learned,
    recomendar: r.advice,
    igc: r.has_igc,
    igcMeta: r.igc_metadata,
    extra: r.additional_event_data || {},
    completo: r.data_completeness,
    demo: false,
    status: r.status,
  };
}

export function deFilaVuelo(v) {
  return {
    id: v.id, site: v.site_id, fecha: v.date, tipo: v.flight_type,
    anon: true, demo: false,
  };
}
