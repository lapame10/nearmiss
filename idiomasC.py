#!/usr/bin/env python3
"""PARTE C: el boton de idioma, la deteccion automatica, y que TODO el
contenido (no solo la interfaz) use el idioma elegido."""
RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0


def rep(v, n):
    global s, toc
    if v in s:
        s = s.replace(v, n); toc += 1
        return True
    print('  NO ENCUENTRO:', v[:72].replace('\n', ' | '))
    return False


# ---------- 1) el pie ----------
rep('<div>Reportes anónimos de incidentes y accidentes de parapente</div>',
    '<div data-i18n="pieTexto"></div>')

# ---------- 2) pintaOps: el nombre segun el idioma ----------
rep("""  div.innerHTML = lista.map(o =>
    '<button data-id="' + o.id + '">' +
    (o.e ? '<span class="mso">' + o.e + '</span>' : '') +
    '<span>' + o.n + '</span></button>').join('');""",
    """  div.innerHTML = lista.map(o =>
    '<button data-id="' + o.id + '">' +
    (o.e ? '<span class="mso">' + o.e + '</span>' : '') +
    '<span>' + nb(o) + '</span></button>').join('');""")

# ---------- 3) los demas sitios que usaban .n ----------
rep("""    const t = sevDe(i.sev);
    const sit = sitDe(i.sit);
    const titulo = (i.sit === 'otro' && i.otro) ? escapa(i.otro) : sit.n;""",
    """    const t = sevDe(i.sev);
    const sit = sitDe(i.sit);
    const titulo = (i.sit === 'otro' && i.otro) ? escapa(i.otro) : nb(sit);""")

rep("""      + '<span class="etq sevEtq">' + t.n + '</span>'""",
    """      + '<span class="etq sevEtq">' + nb(t) + '</span>'""")

rep("""      + (i.franja ? ' · ' + ((FRANJAS.find(f => f.id === i.franja) || {}).n || '') : '')
      + (i.aire ? ' · aire ' + ((AIRES.find(a => a.id === i.aire) || {}).n || '').toLowerCase() : '')""",
    """      + (i.franja ? ' · ' + nb(franjaDe(i.franja)) : '')
      + (i.aire ? ' · ' + nb(aireDe(i.aire)) : '')""")

rep("""        .bindPopup('<b>' + sitDe(i.sit).n + '</b> · ' + t.n + '<br>'
          + (i.mes ? nombreMes(i.mes) : '') + ' · '
          + ((FASES.find(f => f.id === i.fase) || {}).n || '')""",
    """        .bindPopup('<b>' + nb(sitDe(i.sit)) + '</b> · ' + nb(t) + '<br>'
          + (i.mes ? nombreMes(i.mes) : '') + ' · ' + nb(faseDe(i.fase))""")

rep("""      + '</b> son de <b>' + sitDe(tTop[0]).n.toLowerCase() + '</b>.</div>'""",
    """      + '</b> son de <b>' + nb(sitDe(tTop[0])) + '</b>.</div>'""")

rep("""      : [sitDe(t[0]).n, t[1]]));""", """      : [nb(sitDe(t[0])), t[1]]));""")

rep("""      .filter(k => porSev[k]).map(k => [sevDe(k).n, porSev[k]]));""",
    """      .filter(k => porSev[k]).map(k => [nb(sevDe(k)), porSev[k]]));""")

rep("""      .filter(k => porCons[k]).map(k => [consDe(k).n, porCons[k]]));""",
    """      .filter(k => porCons[k]).map(k => [nb(consDe(k)), porCons[k]]));""")

rep("""      .map(f => [(FASES.find(x => x.id === f[0]) || {}).n || f[0], f[1]]));""",
    """      .map(f => [nb(faseDe(f[0])) || f[0], f[1]]));""")

rep("""      .map(f => [(FRANJAS.find(x => x.id === f[0]) || {}).n || f[0], f[1]]));""",
    """      .map(f => [nb(franjaDe(f[0])) || f[0], f[1]]));""")

# ---------- 4) los textos de los titulos de los bloques de patrones ----------
for es, en in [
    ("bloque('Qué pasa más', 'pie_chart', total + ' eventos en total'",
     "bloque(t('quePasaMas'), 'pie_chart', total + ' ' + t('enTotal')"),
    ("bloque('Gravedad de los eventos', 'monitor_heart',\n    'del susto a lo peor: mirarlo sin morbo, para aprender'",
     "bloque(t('gravedadTitulo'), 'monitor_heart', t('gravedadSub')"),
    ("bloque('Consecuencias', 'healing',\n    'el resultado, en datos'",
     "bloque(t('consecTitulo'), 'healing', t('consecSub')"),
    ("bloque('En qué fase del vuelo', 'flight',\n    'dónde se complica'",
     "bloque(t('faseTitulo'), 'flight', t('faseSub')"),
    ("bloque('A qué hora del día', 'schedule',\n    'franja del día'",
     "bloque(t('horaTitulo'), 'schedule', t('horaSub')"),
    ("bloque('Dónde', 'place',\n    'por sitio, sin señalar puntos exactos'",
     "bloque(t('dondeTitulo'), 'place', t('dondeSub')"),
]:
    rep(es, en)

rep("""'<h3><span class="mso">lightbulb</span>El patrón más claro hasta ahora</h3>'""",
    """'<h3><span class="mso">lightbulb</span>' + t('masClaro') + '</h3>'""")
rep("""      + '<div class="cuantos" style="margin:10px 0 0">Con más datos esto dirá cosas como '
      + '«aquí, en esta época, pasa esto». Ese es el objetivo.</div></div>';""",
    """      + '<div class="cuantos" style="margin:10px 0 0">' + t('masDatos') + '</div></div>';""")

rep("""    caja.innerHTML = '<div class="patron" style="grid-column:1/-1">'
      + '<h3><span class="mso">hourglass_empty</span>Todavía no hay suficientes datos</h3>'
      + '<div class="cuantos">Los patrones salen cuando hay al menos 3 eventos. '
      + 'Ahora hay ' + incidentes.length + '.</div>'
      + '<div style="font-size:13px;line-height:1.65;color:var(--gris)">'
      + 'Por eso lo importante ahora es que la gente reporte: <b>cada susto cuenta</b>. '
      + 'Con 20 eventos esto ya dice cosas útiles.</div></div>';""",
    """    caja.innerHTML = '<div class="patron" style="grid-column:1/-1">'
      + '<h3><span class="mso">hourglass_empty</span>' + t('pocosDatos') + '</h3>'
      + '<div class="cuantos">' + t('pocosTexto') + incidentes.length + '.</div>'
      + '<div style="font-size:13px;line-height:1.65;color:var(--gris)">'
      + t('pocosFin') + '</div></div>';""")

# ---------- 5) los avisos y la lista vacia ----------
rep("""  }).join('') : '<div class="vacio">Todavía no hay eventos.<br>Sé el primero en contar uno.</div>';""",
    """  }).join('') : '<div class="vacio">' + t('nada') + '</div>';""")

rep("""    aviso('Falta algún dato', 'Necesito: <b>' + falta.join(', ') + '</b>.<br><br>'
      + 'Son 30 segundos y con eso ya sirve.');""",
    """    aviso(t('faltaTitulo'), t('faltaTexto') + '<b>' + falta.join(', ') + '</b>' + t('faltaFin'));""")

rep("""    aviso('Gracias. Ya está dentro.',
      'Lo que has contado puede evitar que otro pase por lo mismo.'
      + (viento ? '<br><br>Y he guardado el viento real de ese día: <b>'
          + textoViento(viento) + '</b>.' : '')
      + '<br><br>Puedes reportar todos los que quieras: <b>los sustos también cuentan</b>.');""",
    """    aviso(t('graciasTitulo'),
      t('graciasTexto')
      + (viento ? '<br><br>' + t('graciasViento') + '<b>' + textoViento(viento) + '</b>.' : '')
      + '<br><br>' + t('graciasFin'));""")

rep("""    aviso('No se pudo enviar', 'Revisa tu conexión e inténtalo otra vez.<br><br>'
      + '<span style="font-size:12px;color:#6b7f88">' + escapa(e.message) + '</span>');""",
    """    aviso(t('errorTitulo'), t('errorTexto') + '<br><br>'
      + '<span style="font-size:12px;color:#6b7f88">' + escapa(e.message) + '</span>');""")

rep("""  aviso('Ese evento no tiene punto',
      'Quien lo escribió no marcó dónde pasó. Es lo único que se pide y no se '
      + 'obligó, así que no hay sitio al que llevarte.');""",
    """  aviso(t('sinPuntoTitulo'), t('sinPuntoTexto'));""")

rep("""  aviso('Privacidad', 'No pedimos tu nombre, ni tu teléfono, ni tu correo.'
    + '<br><br>La ubicación se <b>redondea a unos 100 metros</b>, así que no señala un punto exacto.'
    + '<br><br>El <b>día</b> que pongas se usa solo para calcular el viento de esa jornada '
    + 'y <b>no se guarda</b>: solo queda el mes y el año.'
    + '<br><br>Y no hay cuentas ni usuarios: nadie puede ver quién reportó qué.'
    + '<br><br>El anonimato no es un extra. Es lo único que hace que esto sirva.');""",
    """  aviso(t('privTitulo'), t('privTexto'));""")

rep("""    $('txtEstado').textContent = 'Mirando el viento que hacía ese día…';""",
    """    $('txtEstado').textContent = t('mirandoViento');""")
rep("""  $('txtEstado').textContent = 'Enviando…';""", """  $('txtEstado').textContent = t('enviando');""")
rep("""          ? '<div class="verPunto"><span class="mso">my_location</span>Ver en el mapa</div>'""",
    """          ? '<div class="verPunto"><span class="mso">my_location</span>' + t('verEnMapa') + '</div>'""")
rep("""'<span class="etq pendEtq"><span class="mso">pending</span>pendiente de verificación</span>'""",
    """'<span class="etq pendEtq"><span class="mso">pending</span>' + t('pendVerif') + '</span>'""")

# ---------- 6) la validacion, con textos traducidos ----------
rep("""  if (!sel.sev) falta.push('qué ocurrió');
  if (!sel.sit) falta.push('qué pasó');
  if (!sel.cons) falta.push('las consecuencias');""",
    """  if (!sel.sev) falta.push(t('c1t').toLowerCase());
  if (!sel.sit) falta.push(t('c2t').toLowerCase());
  if (!sel.cons) falta.push(t('c3t').toLowerCase());""")
rep("""  if (!fase) falta.push('la fase del vuelo');""", """  if (!fase) falta.push(t('c4t').toLowerCase());""")
rep("""  if (sel.lat == null) falta.push('el sitio en el mapa');""", """  if (sel.lat == null) falta.push(t('c5t').toLowerCase());""")
rep("""  if (!sel.franja) falta.push('la franja del día');""", """  if (!sel.franja) falta.push(t('c7t').toLowerCase());""")
rep("""  if (sel.sit === 'otro' && !otro) falta.push('cuál era el «otro»');""",
    """  if (sel.sit === 'otro' && !otro) falta.push(t('otroTitulo').toLowerCase());""")

# ---------- 7) EL BOTON Y LA FUNCION ----------
rep("""/* ---------- arranque ---------- */""",
    """/* ==========================================================================
   CAMBIAR DE IDIOMA (idea de Pam)
   --------------------------------------------------------------------------
   El boton de la cabecera, la memoria en el movil, y la deteccion automatica:
   si el navegador viene en ingles, entra en ingles sin que nadie toque nada.
   ========================================================================== */
const IDIOMAS = { es: 'ES', en: 'EN' };

function ponIdioma(l, guardar){
  if (!TXT[l]) l = 'es';
  idioma = l;
  try { if (guardar !== false) localStorage.setItem('sr_idioma', l); } catch(e){}
  document.documentElement.lang = l;

  /* los textos marcados en el HTML */
  document.querySelectorAll('[data-i18n]').forEach(n => {
    const t2 = t(n.dataset.i18n);
    if (t2) n.innerHTML = t2;
  });
  document.querySelectorAll('[data-i18n-ph]').forEach(n => {
    const t2 = t(n.dataset.i18nPh);
    if (t2) n.placeholder = t2;
  });

  /* el boton */
  if ($('idTxt')) $('idTxt').textContent = IDIOMAS[l];

  /* las listas que se generan por codigo */
  $('selFase').innerHTML = '<option value="">' + t('eligeFase') + '</option>'
    + FASES.map(f => '<option value="' + f.id + '">' + nb(f) + '</option>').join('');
  /* conservo lo que el usuario ya habia elegido y marcado */
  const antesFase = $('selFase').dataset.v || '';
  if (antesFase) $('selFase').value = antesFase;
  pintaOps('opSev', SEVERIDAD, 'sev');
  pintaOps('opSit', SITUACION, 'sit');
  pintaOps('opCons', CONSEC, 'cons');
  pintaOps('opFranja', FRANJAS, 'franja');
  pintaOps('opAire', AIRES, 'aire');
  ['opSev','opSit','opCons','opFranja','opAire'].forEach((id, i2) => {
    const campo = ['sev','sit','cons','franja','aire'][i2];
    if (sel[campo]){
      const b = $(id).querySelector('button[data-id="' + sel[campo] + '"]');
      if (b) b.classList.add('on');
    }
  });
  $('cajaOtro').classList.toggle('on', sel.sit === 'otro');
  $('cajaFatalidad').classList.toggle('on', sel.cons === 'fatal' || sel.sev === 'fatal');
  $('bIGC').querySelector('[data-i18n]') && ($('bIGC').querySelector('[data-i18n]').innerHTML = t('igcBoton'));
  $('filtros').innerHTML = '<button class="on" data-f="todos">'
    + '<span class="mso">apps</span>' + t('todos') + '</button>'
    + SEVERIDAD.map(x => '<button data-f="' + x.id + '"><span class="mso">' + x.e
        + '</span>' + nb(x) + '</button>').join('');
  $('filtros').querySelectorAll('button').forEach(b => b.classList.toggle('on', b.dataset.f === filtro));

  /* y repinto lo que depende de los datos */
  if (mapaPrincipal) pintaIncidentes();
  if (typeof incidentes !== 'undefined' && incidentes.length) pintaPatrones();
}

$('bIdioma').onclick = () => ponIdioma(idioma === 'es' ? 'en' : 'es');

/* ---------- arranque ---------- */""")

rep("""pintaOps('opSev', SEVERIDAD, 'sev');""", """/* el idioma: primero lo que eligio antes, si no el del navegador */
ponIdioma((function(){
  try {
    const g = localStorage.getItem('sr_idioma');
    if (g && TXT[g]) return g;
  } catch(e){}
  return (navigator.language || 'es').toLowerCase().indexOf('en') === 0 ? 'en' : 'es';
})(), false);

pintaOps('opSev', SEVERIDAD, 'sev');""")

# el select de la fase lo rellena ponIdioma, asi que la linea vieja sobra
rep("""/* la fase, en desplegable como en el diseño de Pam */
$('selFase').innerHTML = '<option value="">Selecciona una fase…</option>'
  + FASES.map(f => '<option value="' + f.id + '">' + f.n + '</option>').join('');

""", "")

# y guardo la fase elegida, para que el cambio de idioma no la borre
rep("""  $('selFase').value = '';
    $('otroTexto').value = '';""",
    """  $('selFase').value = '';
    $('selFase').dataset.v = '';
    $('otroTexto').value = '';""")
rep("""  if (!fase) falta.push(t('c4t').toLowerCase());""",
    """  $('selFase').dataset.v = fase;
  if (!fase) falta.push(t('c4t').toLowerCase());""")

# ---------- 8) el CSS del boton de idioma ----------
rep("""  .nav button.on{opacity:1;background:rgba(255,255,255,.13)}""",
    """  .nav button.on{opacity:1;background:rgba(255,255,255,.13)}
  /* el boton de idioma: discreto, a la derecha del todo */
  .nav button.idioma{opacity:.85;border:1px solid rgba(255,255,255,.3);
    padding:7px 12px;font-size:12px;letter-spacing:.4px}
  .nav button.idioma:hover{opacity:1;background:rgba(255,255,255,.1)}""")

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
