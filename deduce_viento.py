#!/usr/bin/env python3
"""EL VIENTO NO SE PREGUNTA: SE DEDUCE (idea de Pam)

Pam: 'mas bien pondria algo como... que no pongan nada, pero si tienen el IGC
de ahi sacamos mas informacion, y si no lo tienen con poner el dia (opcional)
sacamos el viento del clima... asi no dejamos que hagan tanto'.

Tiene razon y es buen diseño de producto: no preguntes lo que puedes deducir.
- Menos campos = mas gente reporta
- Y el viento del clima real es mas fiable que la percepcion de nadie

Como:
1. El dia que ponga -> Open-Meteo (gratis, sin llave) da el viento de esa hora
2. Si ademas sube su IGC -> saco la hora exacta y los datos del vuelo
3. El dia NO se guarda (privacidad); solo el mes y el año
"""

RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()

# ---------- 1) fuera el control deslizante del aire ----------
viejo = """/* ===== EL AIRE: control deslizante + etiqueta de racheado ===== */
(function(){
  const seg = $('segAire');
  seg.onclick = ev => {
    const b = ev.target.closest('button');
    if (!b) return;
    seg.querySelectorAll('button').forEach(x => x.classList.remove('on'));
    b.classList.add('on');
    sel.viento = b.dataset.id;
  };
  const chips = $('chipsAire');
  chips.onclick = ev => {
    const b = ev.target.closest('button');
    if (!b) return;
    b.classList.toggle('on');
    sel.racheado = b.classList.contains('on');
  };
})();"""

nuevo = """/* ==========================================================================
   EL VIENTO NO SE PREGUNTA: SE DEDUCE (idea de Pam)
   --------------------------------------------------------------------------
   Antes le pediamos al piloto que dijera si el aire estaba flojo o fuerte.
   Eso es preguntar lo que ya sabemos: con el dia que puso, los datos del
   clima nos dicen el viento REAL que hacia a esa hora en ese sitio.
   Y es mejor dato: no es lo que uno recuerda, es lo que habia.
   Si ademas sube su IGC, la hora es exacta y el dato mejora todavia.
   ========================================================================== */

/* el dia que eligio, en formato AAAA-MM-DD (o null) */
function diaElegido(){
  const v = $('fecha').value;
  return v || null;
}

/* la hora aproximada, segun la franja */
function horaDeFranja(f){
  if (f === 'manana') return 9;
  if (f === 'mediodia') return 13;
  if (f === 'tarde') return 16;
  return 13;
}

/* le pido el viento a Open-Meteo: gratis, sin llave, y con datos desde 1940 */
async function vientoReal(lat, lon, dia, hora){
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
    const g = d.hourly.wind_gusts_10m ? d.hourly.wind_gusts_10m[i] : null;
    const dir = d.hourly.wind_direction_10m ? d.hourly.wind_direction_10m[i] : null;
    if (v == null) return null;
    return { kmh: Math.round(v), racha: g != null ? Math.round(g) : null,
             dir: dir != null ? Math.round(dir) : null };
  }catch(e){ return null; }
}

/* ===== EL ARCHIVO IGC =====
   Es el registro estandar que graba el vario. De aqui saco la hora exacta,
   la duracion y la altura maxima. NO guardo el archivo ni el recorrido. */
function leeIGC(texto){
  const lineas = texto.split(/\\r?\\n/);
  const puntos = [];
  let dia = null;
  lineas.forEach(l => {
    if (l.indexOf('HFDTE') === 0){
      const m = l.match(/HFDTE(?:DATE:)?(\\d{2})(\\d{2})(\\d{2})/);
      if (m) dia = '20' + m[3] + '-' + m[2] + '-' + m[1];
    }
    if (l.charAt(0) === 'B' && l.length > 34){
      const hh = parseInt(l.substr(1,2), 10);
      const mi = parseInt(l.substr(3,2), 10);
      const la = parseInt(l.substr(7,2), 10) + parseFloat(l.substr(9,5)) / 1000 / 60;
      const lo = parseInt(l.substr(15,3), 10) + parseFloat(l.substr(18,5)) / 1000 / 60;
      const alt = parseInt(l.substr(30,5), 10);
      if (!isNaN(hh) && !isNaN(la) && !isNaN(lo))
        puntos.push({ h: hh + mi / 60, lat: la, lon: lo, alt: isNaN(alt) ? null : alt });
    }
  });
  if (!puntos.length) return null;
  let altMax = null, t0 = puntos[0].h, t1 = puntos[0].h;
  puntos.forEach(p => {
    if (p.alt != null && (altMax == null || p.alt > altMax)) altMax = p.alt;
    if (p.h < t0) t0 = p.h;
    if (p.h > t1) t1 = p.h;
  });
  return { dia: dia, horaInicio: t0, horaFin: t1,
           minutos: Math.round((t1 - t0) * 60),
           altMax: altMax, puntos: puntos.length,
           lat: puntos[Math.floor(puntos.length / 2)].lat,
           lon: puntos[Math.floor(puntos.length / 2)].lon };
}

let igc = null;
$('bIGC').onclick = () => $('ficheroIGC').click();
$('ficheroIGC').onchange = ev => {
  const f = ev.target.files && ev.target.files[0];
  if (!f) return;
  const lector = new FileReader();
  lector.onload = () => {
    const d = leeIGC(String(lector.result));
    if (!d){
      $('igcInfo').innerHTML = '⚠️ No he podido leer el archivo. ¿Seguro que es un IGC?';
      $('igcInfo').classList.add('on');
      return;
    }
    igc = d;
    $('bIGC').classList.add('on');
    $('bIGC').textContent = '✅ ' + f.name;
    const h = Math.floor(d.horaInicio) + ':' + String(Math.round((d.horaInicio % 1) * 60)).padStart(2,'0');
    $('igcInfo').innerHTML = '🛫 Volaste <b>' + d.minutos + ' minutos</b>, '
      + 'despegando sobre las <b>' + h + '</b>'
      + (d.altMax ? ', hasta <b>' + d.altMax + ' m</b>' : '') + '.'
      + '<br>Con esto el viento sale de la hora exacta, no de una estimación.';
    $('igcInfo').classList.add('on');
    /* si el IGC trae el dia y el piloto no lo puso, lo relleno */
    if (d.dia && !$('fecha').value) $('fecha').value = d.dia;
  };
  lector.readAsText(f);
};

/* ===== EL BOTON DE ENVIAR: calcula el viento y guarda ===== */
$('bEnviar').onclick = envia;"""

if viejo in s:
    s = s.replace(viejo, nuevo); print('  OK: fuera el control del aire, dentro el calculo')
else:
    print('  NO ENCUENTRO el bloque del aire')

# ---------- 2) la validacion: el mes ya no es obligatorio --------------
viejo2 = """  const otro = $('otroTexto').value.trim();
  if (sel.tipo === 'otro' && !otro) falta.push('qué tipo era (el «otro» hay que decir cuál)');"""
nuevo2 = """  const otro = $('otroTexto').value.trim();
  if (sel.tipo === 'otro' && !otro) falta.push('qué tipo era (el «otro» hay que decir cuál)');
  const dia = diaElegido();"""
if viejo2 in s: s = s.replace(viejo2, nuevo2); print('  OK: validacion actualizada')
else: print('  NO ENCUENTRO la validacion')

# ---------- 3) quitar la obligacion del mes --------------------------
viejo3 = "  if (!sel.mes) falta.push('el mes y el año');\n"
if viejo3 in s: s = s.replace(viejo3, ''); print('  OK: el mes ya no es obligatorio')
else: print('  NO ENCUENTRO la linea del mes obligatorio')

# ---------- 4) al enviar: calculo el viento y guardo -----------------
viejo4 = """  const dato = {
    tipo: sel.tipo, gravedad: sel.gravedad, fase: sel.fase,
    lat: sel.lat, lon: sel.lon, mes: sel.mes, franja: sel.franja,
    viento: sel.viento, racheado: !!sel.racheado, relato: relato.slice(0, 900),
    otro: (sel.tipo === 'otro') ? otro : null,
    creado: Date.now(),
    v: 1
  };

  $('bEnviar').disabled = true;
  $('txtEstado').textContent = 'Enviando…';"""

nuevo4 = """  /* el mes y el año salen del dia; el DIA no se guarda (privacidad) */
  const mes = dia ? dia.slice(0, 7) : null;

  /* el viento: lo saco del clima real, no lo pregunto */
  $('bEnviar').disabled = true;
  let viento = null;
  if (dia){
    $('txtEstado').textContent = 'Mirando el viento que hacía ese día…';
    const hora = igc ? igc.horaInicio : horaDeFranja(sel.franja);
    viento = await vientoReal(sel.lat, sel.lon, dia, hora);
  }

  const dato = {
    tipo: sel.tipo, gravedad: sel.gravedad, fase: sel.fase,
    lat: sel.lat, lon: sel.lon, mes: mes, franja: sel.franja,
    viento: viento,                       /* {kmh, racha, dir} del clima real */
    igcMin: igc ? igc.minutos : null,     /* solo numeros del vuelo */
    igcAltMax: igc ? igc.altMax : null,
    relato: relato.slice(0, 900),
    otro: (sel.tipo === 'otro') ? otro : null,
    creado: Date.now(),
    v: 2
  };

  $('txtEstado').textContent = 'Enviando…';"""
if viejo4 in s: s = s.replace(viejo4, nuevo4); print('  OK: al enviar calcula el viento')
else: print('  NO ENCUENTRO el bloque de datos')

# ---------- 5) limpiar tambien la fecha y el IGC --------------------
viejo5 = """    $('selMes').value = '';
    $('selMes').classList.add('vacio');"""
nuevo5 = """    $('fecha').value = '';
    $('ficheroIGC').value = '';
    igc = null;
    $('bIGC').classList.remove('on');
    $('bIGC').textContent = '📁 Subir mi archivo IGC';
    $('igcInfo').classList.remove('on');"""
if viejo5 in s: s = s.replace(viejo5, nuevo5); print('  OK: limpieza actualizada')
else: print('  NO ENCUENTRO la limpieza del mes')

# ---------- 6) la lista: el viento viene calculado -------------------
viejo6 = """        ${i.viento ? '· aire ' + ((VIENTOS.find(v => v.id === i.viento) || {}).n || i.viento).toLowerCase() : ''}${i.racheado ? ' y racheado' : ''}"""
nuevo6 = """        ${(i.viento && i.viento.kmh != null) ? '· viento ' + i.viento.kmh + ' km/h' + (i.viento.racha && i.viento.racha > i.viento.kmh + 12 ? ' (rachas ' + i.viento.racha + ')' : '') : ''}"""
if viejo6 in s: s = s.replace(viejo6, nuevo6); print('  OK: la lista muestra el viento calculado')
else: print('  NO ENCUENTRO el texto del viento')

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  archivo:', len(s), 'bytes')
