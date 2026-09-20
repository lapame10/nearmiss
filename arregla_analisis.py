#!/usr/bin/env python3
"""Los arreglos del analisis de Pam sobre SkyReport.

GRAVES:
1) UTC vs hora local: el IGC da las horas en UTC, pero Open-Meteo con
   timezone=auto espera hora LOCAL. En Mexico eso son 6 horas de desfase: el
   viento que se guardaba era el de OTRA hora del dia. Se arregla usando
   timezone=UTC y buscando por la hora UTC cuando el dato viene del IGC.
2) Open-Meteo Archive tiene ~5 dias de retraso: si alguien reporta algo de esta
   semana, vientoReal() devolvia null EN SILENCIO. Se añade un fallback a la API
   de forecast con past_days, que SI tiene los ultimos dias.
3) Vuelos que cruzan medianoche: (t1 - t0) daba minutos NEGATIVOS.
4) El reset dejaba campos con claves que ya no se usan (tipo, gravedad): las
   reales son sev, sit, cons. Y el boton del IGC volvia a texto español fijo en
   vez de t('igcBoton'), asi que al cambiar de idioma se quedaba en español.

MENORES:
- ZONA_IDIOMA['Europe/Luxembourg '] tenia un espacio al final: nunca casaba
- const IDIOMAS = { es:'ES', en:'EN' } era codigo muerto
- 'from ' hardcodeado en la lista de direcciones del viento
- una linea vacia con un querySelectorAll que no hacia nada
"""
RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0


def rep(v, n, todas=False):
    global s, toc
    if v in s:
        s = s.replace(v, n) if todas else s.replace(v, n, 1)
        toc += 1
        return True
    print('  NO ENCUENTRO:', v[:70].replace('\n', ' | '))
    return False


# ==========================================================================
# GRAVE 1 + 2: el viento, con la zona horaria correcta y con respaldo
# ==========================================================================
rep("""async function vientoReal(lat, lon, dia, hora){
  try{
    const u = 'https://archive-api.open-meteo.com/v1/archive'
      + '?latitude=' + lat.toFixed(3) + '&longitude=' + lon.toFixed(3)
      + '&start_date=' + dia + '&end_date=' + dia
      + '&hourly=wind_speed_10m,wind_gusts_10m,wind_direction_10m&timezone=auto';
    const r = await fetch(u);
    if (!r.ok) throw new Error('http ' + r.status);
    const d = await r.json();
    if (!d.hourly || !d.hourly.time) return null;
    const i = Math.min(23, Math.max(0, Math.round(hora)));
    const v = d.hourly.wind_speed_10m ? d.hourly.wind_speed_10m[i] : null;
    if (v == null) return null;
    const g = d.hourly.wind_gusts_10m ? d.hourly.wind_gusts_10m[i] : null;
    const dr = d.hourly.wind_direction_10m ? d.hourly.wind_direction_10m[i] : null;
    return { kmh: Math.round(v), racha: g != null ? Math.round(g) : null,
             dir: dr != null ? Math.round(dr) : null };
  }catch(e){ return null; }
}""",
    """/* ==========================================================================
   EL VIENTO DE ESE DIA
   --------------------------------------------------------------------------
   OJO CON LAS HORAS. Aqui se cuela un error que nadie ve:

   - El IGC graba las horas en UTC (es el estandar del formato).
   - Open-Meteo, si le pides timezone=auto, te devuelve las horas en la hora
     LOCAL del sitio.
   - En Mexico (UTC-6) eso son SEIS HORAS de desfase: si el vuelo fue a las
     11:00 locales (17:00 UTC), se consultaba la hora 17 LOCAL, que son las
     23:00 UTC. Se guardaba el viento de otra hora del dia. Y como el numero
     sale igual de valido, nadie se entera.

   Solucion: si la hora viene de un IGC (enUTC) se pide timezone=UTC y se busca
   por la hora UTC. Si viene de la franja del dia (mañana/mediodia/tarde), que
   ya esta en hora local, se pide timezone=auto.

   Y el respaldo: el archivo historico de Open-Meteo lleva unos 5 dias de
   retraso. Si alguien reporta algo de esta semana, el archivo NO tiene ese dia
   y antes se quedaba sin viento en silencio. Ahora se prueba la API de
   prevision con past_days, que si tiene los ultimos dias.
   ========================================================================== */
function sacaViento(d, hora, dia){
  if (!d || !d.hourly || !d.hourly.time || !d.hourly.time.length) return null;
  let i = -1;
  if (dia){
    /* cuando la API devuelve varios dias (el forecast), busco la hora exacta */
    const clave = dia + 'T' + String(Math.floor(hora)).padStart(2, '0') + ':00';
    i = d.hourly.time.indexOf(clave);
    if (i < 0) return null;
  } else {
    i = Math.min(23, Math.max(0, Math.round(hora)));
  }
  const v = d.hourly.wind_speed_10m ? d.hourly.wind_speed_10m[i] : null;
  if (v == null) return null;
  const g = d.hourly.wind_gusts_10m ? d.hourly.wind_gusts_10m[i] : null;
  const dr = d.hourly.wind_direction_10m ? d.hourly.wind_direction_10m[i] : null;
  return { kmh: Math.round(v), racha: g != null ? Math.round(g) : null,
           dir: dr != null ? Math.round(dr) : null };
}

async function vientoReal(lat, lon, dia, hora, enUTC){
  const tz = enUTC ? 'UTC' : 'auto';
  const par = '&hourly=wind_speed_10m,wind_gusts_10m,wind_direction_10m&timezone=' + tz;
  const la = lat.toFixed(3), lo = lon.toFixed(3);

  /* 1) el archivo historico: tiene todo, pero con ~5 dias de retraso */
  try {
    const r = await fetch('https://archive-api.open-meteo.com/v1/archive'
      + '?latitude=' + la + '&longitude=' + lo
      + '&start_date=' + dia + '&end_date=' + dia + par);
    if (r.ok){
      const d = await r.json();
      const v = sacaViento(d, hora, null);   /* el archivo solo trae ese dia */
      if (v) return v;
    }
  } catch(e){}

  /* 2) el respaldo: si es de esta semana, el archivo todavia no lo tiene.
     La prevision con past_days=7 si. Aqui SI hay que buscar por fecha, porque
     vienen varios dias juntos. */
  try {
    const r = await fetch('https://api.open-meteo.com/v1/forecast'
      + '?latitude=' + la + '&longitude=' + lo
      + '&hourly=wind_speed_10m,wind_gusts_10m,wind_direction_10m'
      + '&past_days=7&forecast_days=1&timezone=' + tz);
    if (r.ok){
      const d = await r.json();
      return sacaViento(d, hora, dia);
    }
  } catch(e){}
  return null;
}""")

# ==========================================================================
# GRAVE 3: el vuelo que cruza medianoche
# ==========================================================================
rep("""  const medio = puntos[Math.floor(puntos.length / 2)];
  return { dia, horaInicio:t0, horaFin:t1, minutos:Math.round((t1 - t0) * 60),
           altMax, puntos:puntos.length, lat:medio.lat, lon:medio.lon };""",
    """  /* Si el vuelo cruza medianoche (despegue a las 23:40 y aterrizaje a las
     00:20), t1 seria MENOR que t0 y la duracion saldria NEGATIVA. Se suma un
     dia. Caso raro, pero un numero negativo en la ficha queda fatal. */
  if (t1 < t0) t1 += 24;
  const medio = puntos[Math.floor(puntos.length / 2)];
  return { dia, horaInicio:t0, horaFin:t1, minutos:Math.round((t1 - t0) * 60),
           altMax, puntos:puntos.length, lat:medio.lat, lon:medio.lon };""")

# ==========================================================================
# GRAVE 4a: el reset con las claves de verdad
# ==========================================================================
rep("""let sel = { tipo:null, gravedad:null, franja:null, aire:null, lat:null, lon:null };""",
    """/* OJO: las claves son sev / sit / cons. Antes ponia tipo y gravedad, que ya
   no existen. Funcionaba por accidente (se reemplaza el objeto entero), pero
   era una trampa para el proximo que lo lea. */
let sel = { sev:null, sit:null, cons:null, franja:null, aire:null, lat:null, lon:null };""")

rep("""    sel = { tipo:null, gravedad:null, franja:null, aire:null, lat:null, lon:null };""",
    """    sel = { sev:null, sit:null, cons:null, franja:null, aire:null, lat:null, lon:null };""")

# ==========================================================================
# GRAVE 4b: el boton del IGC, traducido
# ==========================================================================
rep("""    $('bIGC').innerHTML = '<span class="mso">upload_file</span> Subir mi archivo IGC';""",
    """    $('bIGC').innerHTML = '<span class="mso">upload_file</span> ' + t('igcBoton');""")

# ==========================================================================
# Y LA LLAMADA: hay que decirle si la hora es UTC o local
# ==========================================================================
rep("""    viento = await vientoReal(lat, lon, dia, hora);""",
    """    /* si la hora viene del IGC, esta en UTC (es el estandar del formato).
       Si viene de la franja del dia, esta en hora local. */
    viento = await vientoReal(lat, lon, dia, hora, !!igc);""")

# ==========================================================================
# MENORES
# ==========================================================================
# el espacio de Luxemburgo (y de paso: ya estaba como fr, esto era codigo muerto)
rep("""  'Europe/Luxembourg ':'de', Africa/Windhoek':'de',""",
    """  'Africa/Windhoek':'de',""", todas=True)
rep("""  'Europe/Luxembourg ':'de',""", """  'Africa/Windhoek':'de',""", todas=True)
rep("""Africa/Windhoek':'de',""", """'Africa/Windhoek':'de',""", todas=True)

# la constante IDIOMAS, que ya no se usa (el selector es un <select>)
rep("""const IDIOMAS = { es: 'ES', en: 'EN' };\n""", "")

# el 'from ' a pelo en la lista de direcciones
rep("""          + (idioma === 'es' ? 'del ' : 'from ') + d[0] + '</span>'""",
    """          + (DESDE[idioma] || 'de') + ' ' + d[0] + '</span>'""")

# la linea vacia
rep("""document.querySelectorAll('.ops button, .filtros button').forEach(b => {});\n""", "")

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
