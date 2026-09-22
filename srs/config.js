/* ============================================================
   SkyReport — configuración
   ============================================================

   ⚠️ AQUÍ SE PONEN TUS DOS CREDENCIALES DE SUPABASE.
   Mientras estén vacías, SkyReport funciona en MODO DEMO:
   todo vive en el navegador y se ve un aviso claro.

   ─────────────────────────────────────────────────────────
   DÓNDE SACAR LAS DOS CREDENCIALES
   ─────────────────────────────────────────────────────────
   1. Entra en https://supabase.com y crea un proyecto (gratis).
   2. En el menú, Settings → API.
   3. Copia estos dos valores y pégalos aquí abajo:

      Project URL        →  SUPABASE_URL
      anon public key    →  SUPABASE_ANON_KEY

   La anon key PUEDE estar en el frontend: está pensada para eso.
   Lo que protege los datos de verdad NO es esconder esta clave,
   son las policies de Row Level Security de supabase/schema.sql.
   Sin RLS, esa clave daría acceso a todo. Con RLS, solo deja
   leer lo aprobado y añadir cosas nuevas — nada más.

   4. Ejecuta supabase/schema.sql en el SQL Editor de Supabase.
      Ese archivo crea las tablas, los índices y las policies.
      Sin ese paso, la app NO debe conectarse: mejor modo demo
      que una base de datos abierta.

   ⚠️ NO pongas aquí la service_role key. Esa salta todas las
   reglas y no debe estar nunca en el navegador.
   ============================================================ */

export const SUPABASE_URL = '';        // ← pega aquí tu Project URL
export const SUPABASE_ANON_KEY = '';   // ← pega aquí tu anon public key

/* ============================================================
   ¿Está configurado?
   ============================================================
   Se comprueba que las dos existen Y que no son los placeholders
   de ejemplo. Así, si alguien pega el archivo tal cual, la app
   sigue en modo demo en vez de intentar conectar y fallar. */
export function haySupabase() {
  const ok = (x) => typeof x === 'string' && x.length > 20 &&
    !x.includes('TU_') && !x.includes('PEGA') && !x.includes('xxxx');
  return ok(SUPABASE_URL) && ok(SUPABASE_ANON_KEY) &&
    SUPABASE_URL.startsWith('https://');
}

/* ============================================================
   Ajustes de la plataforma
   ============================================================ */
export const AJUSTES = {
  /* Radio al que se redondean las coordenadas públicas.
     ~0,001 grados ≈ 100 m. La política de privacidad de SkyReport:
     el punto exacto nunca se publica. */
  redondeoGrados: 0.001,

  /* ¿Los reportes nuevos entran directamente como aprobados?
     En desarrollo sí, para poder probar el circuito entero.
     En producción debería ser false: entran como 'pending' y pasan
     por moderación antes de ser públicos. */
  autoAprobar: true,

  /* ¿Se mezclan los datos de demostración con los reales?
     Nunca. Con Supabase conectado, los demo se apagan solos. */
  permitirDemoConSupabase: false,

  /* Cuántos reportes hacen falta para describir un patrón */
  minReportesSenal: 3,

  /* A partir de cuántos vuelos registrados un dato de exposición
     (reports per 1.000 flights) ya se puede mostrar sin engañar */
  minVuelosParaTasa: 30,
};

/* ============================================================
   Estado global de la conexión
   ============================================================
   Las vistas leen esto para saber qué enseñar. Es la única
   fuente de verdad sobre si estamos en demo o en comunidad. */
export const red = {
  modo: haySupabase() ? 'conectando' : 'demo',
  ultimoError: null,
  pendientes: 0,      /* reportes esperando conexión */
};
