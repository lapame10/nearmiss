#!/usr/bin/env python3
"""El JavaScript de la administración."""
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


JS = r"""
/* ==========================================================================
   LA ADMINISTRACIÓN
   --------------------------------------------------------------------------
   Ver más arriba las decisiones de diseño. Resumen:
   - Sin cuentas: una CLAVE larga que se da a quien se quiera y se revoca
     borrándola. Coherente con una app que no tiene usuarios.
   - Dos roles: SUPER (todo) y ZONA (solo lo de su zona).
   - Todo lo que se hace queda en un REGISTRO que no se puede borrar.
   - Borrar NO borra: se copia a la papelera antes.
   - Y un admin NUNCA puede ver datos personales (no los hay) ni la ubicación
     exacta (solo ve lo mismo que todo el mundo). Si pudiera, el anonimato no
     valdría nada.
   ========================================================================== */
let yoAdmin = null;
let admins = {};
let logAcciones = [];

/* una clave que se pueda leer por teléfono sin equivocarse: sin I, O, 0, 1 */
function claveNueva(){
  const abc = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  let c = '';
  for (let i = 0; i < 12; i++) c += abc[Math.floor(Math.random() * abc.length)];
  return c.slice(0, 4) + '-' + c.slice(4, 8) + '-' + c.slice(8, 12);
}

/* ---------- quién soy y qué puedo ---------- */
function esSuper(){ return yoAdmin && yoAdmin.rol === 'super'; }

function puedeTocar(i){
  if (!yoAdmin) return false;
  if (esSuper()) return true;
  if (yoAdmin.rol === 'zona' && i.lat != null){
    /* solo lo de SU zona. La zona se compara con el nombre del sitio, así que
       hay que escribirla igual que sale en el mapa (ej: 'Valle de Bravo'). */
    return nombreSitio(i.lat, i.lon) === (yoAdmin.zona || '');
  }
  return false;
}

/* ---------- el registro: quién hizo qué ---------- */
function anota(que, idEvento, detalle){
  if (!yoAdmin) return;
  firebase.database().ref('skyreport/log').push({
    quien: yoAdmin.nombre || '?',
    clave: yoAdmin.clave,
    rol: yoAdmin.rol,
    zona: yoAdmin.zona || null,
    que: que,
    evento: idEvento || null,
    detalle: detalle || null,
    cuando: firebase.database.ServerValue.TIMESTAMP,
  });
}

/* ---------- entrar y salir ---------- */
function entraAdmin(clave, callar){
  clave = String(clave || '').trim().toUpperCase();
  const a = admins[clave];
  if (!a || a.activo === false){
    const e = $('adErr');
    if (e && !callar){ e.textContent = t('admClaveMal'); e.classList.add('on'); }
    return false;
  }
  yoAdmin = Object.assign({ clave: clave }, a);
  try { localStorage.setItem('sr_admin', clave); } catch(e){}
  if ($('tAdmin')) $('tAdmin').style.display = '';
  pintaAdmin();
  return true;
}

function salirAdmin(){
  yoAdmin = null;
  try { localStorage.removeItem('sr_admin'); } catch(e){}
  if ($('tAdmin')) $('tAdmin').style.display = 'none';
  ponPestana('tReportar');
}

/* ---------- las acciones ---------- */
async function admVerificar(id){
  const i = incidentes.find(x => x.id === id);
  if (!i) return;
  if (!puedeTocar(i)) return aviso(t('admTitulo'), t('admSinPermiso'));
  await firebase.database().ref('skyreport/incidentes/' + id).update({
    verif: 'ok', verifPor: yoAdmin.nombre || '?', verifTs: Date.now(),
  });
  anota('verificar', id);
  aviso(t('admOk'), t('admPublicado'));
}

async function admRechazar(id){
  const i = incidentes.find(x => x.id === id);
  if (!i) return;
  if (!puedeTocar(i)) return aviso(t('admTitulo'), t('admSinPermiso'));
  await firebase.database().ref('skyreport/incidentes/' + id).update({
    verif: 'rechazado', verifPor: yoAdmin.nombre || '?', verifTs: Date.now(),
  });
  anota('rechazar', id);
  aviso(t('admOk'), t('admRechazado'));
}

async function admBorrar(id){
  const i = incidentes.find(x => x.id === id);
  if (!i) return;
  if (!puedeTocar(i)) return aviso(t('admTitulo'), t('admSinPermiso'));
  if (!confirm(t('admConfirmBorrar'))) return;
  /* copia antes: borrar no es borrar */
  await firebase.database().ref('skyreport/papelera/' + id).set(Object.assign({}, i, {
    borradoPor: yoAdmin.nombre || '?', borradoTs: Date.now(),
  }));
  await firebase.database().ref('skyreport/incidentes/' + id).remove();
  anota('borrar', id, (sitDe(i.sit).es || '') + ' · ' + (i.mes || ''));
  aviso(t('admOk'), t('admBorrado'));
}

async function admCrear(){
  if (!esSuper()) return;
  const nombre = ($('adNuevoNombre').value || '').trim();
  const zona = ($('adNuevoZona').value || '').trim();
  const rol = $('adNuevoRol').value;
  if (!nombre) return aviso(t('admTitulo'), t('admNombre'));
  if (rol === 'zona' && !zona) return aviso(t('admTitulo'), t('admZona'));
  const clave = claveNueva();
  await firebase.database().ref('skyreport/admins/' + clave).set({
    nombre: nombre, rol: rol, zona: (rol === 'zona' ? zona : null),
    activo: true, creado: Date.now(), creadoPor: yoAdmin.nombre || '?',
  });
  anota('crear-admin', null, nombre + (zona ? ' (' + zona + ')' : '') + ' · ' + clave);
  $('adNuevoNombre').value = ''; $('adNuevoZona').value = '';
  aviso(t('admOk'), '🔑 <b>' + nombre + '</b><br><br>' + t('admTuClave') + ':<br>'
    + '<span class="adClave">' + clave + '</span><br><br>'
    + 'Dásela y que entre en <b>skyreport/?admin=' + clave + '</b>');
}

async function admRevocar(clave){
  if (!esSuper()) return;
  const a = admins[clave];
  if (!a) return;
  if (!confirm('¿Revocar la clave de ' + (a.nombre || clave) + '?')) return;
  await firebase.database().ref('skyreport/admins/' + clave).update({ activo: false });
  anota('revocar-admin', null, a.nombre || clave);
}

/* ---------- pintar ---------- */
function pintaAdmin(){
  if (!yoAdmin){
    /* sin clave: la puerta */
    $('vAdmin').innerHTML = '<div class="cuerpo" style="grid-template-columns:1fr">'
      + '<div class="puerta">'
      + '<h2><span class="mso">lock</span>' + t('admPuerta') + '</h2>'
      + '<p>' + t('admPuertaAyuda') + '</p>'
      + '<input type="text" id="adClave" placeholder="XXXX-XXXX-XXXX" autocomplete="off">'
      + '<div class="err" id="adErr"></div>'
      + '<button class="btn" id="adEntrar" style="width:100%;margin-top:14px;'
      + 'justify-content:center">' + t('admPuerta') + '</button>'
      + '</div></div>';
    $('adEntrar').onclick = () => entraAdmin($('adClave').value);
    $('adClave').onkeydown = ev => { if (ev.key === 'Enter') entraAdmin($('adClave').value); };
    return;
  }
  /* con clave: la página entera */
  const rol = esSuper() ? t('admRolSuper')
            : (yoAdmin.rol === 'zona' ? t('admRolZona').replace('{z}', yoAdmin.zona || '')
            : t('admRolVer'));
  $('adQuien').innerHTML = t('admEres').replace('{n}', yoAdmin.nombre || '?')
    .replace('{r}', rol) + ' · <span class="adClave">' + yoAdmin.clave + '</span>';
  $('adAdmins').style.display = esSuper() ? '' : 'none';
  pintaPendientes();
  pintaTodos();
  pintaAdmins();
}

function filaEvento(i, conVerificar){
  const sit = sitDe(i.sit), sv = sevDe(i.sev);
  const sitio = i.lat != null ? nombreSitio(i.lat, i.lon) : '—';
  const puede = puedeTocar(i);
  let btns = '';
  if (conVerificar && puede){
    btns += '<button class="adOk" onclick="admVerificar(\'' + i.id + '\')">'
          + '<span class="mso">check_circle</span>' + t('admPub') + '</button>'
          + '<button class="adNo" onclick="admRechazar(\'' + i.id + '\')">'
          + '<span class="mso">cancel</span>' + t('admRech') + '</button>';
  }
  if (puede){
    btns += '<button class="adDel" onclick="admBorrar(\'' + i.id + '\')">'
          + '<span class="mso">delete</span>' + t('admBorrar') + '</button>';
  }
  return '<div class="adFila">'
    + '<div class="adInfo">'
    + '<div class="adTit"><span class="mso">' + sit.e + '</span>'
    + ((i.sit === 'otro' && i.otro) ? escapa(i.otro) : nb(sit))
    + ' <span class="etq sevEtq">' + nb(sv) + '</span></div>'
    + '<div class="adMeta">' + sitio + ' · ' + (i.mes ? nombreMes(i.mes) : '—')
    + ' · ' + nb(franjaDe(i.franja))
    + (i.verif && i.verif !== 'ok' ? ' · <b>' + i.verif + '</b>' : '')
    + (i.verifPor ? ' · por ' + escapa(i.verifPor) : '') + '</div>'
    + (i.relato ? '<div class="adRelato">' + escapa(i.relato) + '</div>' : '')
    + '</div>'
    + '<div class="adBtns">' + btns + '</div>'
    + '</div>';
}

function pintaPendientes(){
  const pend = incidentes.filter(i => i.verif === 'pendiente');
  $('adNPend').textContent = pend.length;
  $('adListaPend').innerHTML = pend.length
    ? pend.map(i => filaEvento(i, true)).join('')
    : '<div class="vacioAdmin">' + t('admNadaPend') + '</div>';
}

function pintaTodos(){
  const q = ($('adBusca') && $('adBusca').value || '').toLowerCase().trim();
  let lista = incidentes.slice().reverse();
  if (q){
    lista = lista.filter(i => {
      const txt = [(i.otro || ''), (i.relato || ''), nb(sitDe(i.sit)),
                   nb(sevDe(i.sev)), (i.lat != null ? nombreSitio(i.lat, i.lon) : '')]
                  .join(' ').toLowerCase();
      return txt.indexOf(q) >= 0;
    });
  }
  $('adNTotal').textContent = lista.length;
  $('adListaTodos').innerHTML = lista.length
    ? lista.map(i => filaEvento(i, i.verif === 'pendiente')).join('')
    : '<div class="vacioAdmin">' + t('nada') + '</div>';
}

function pintaAdmins(){
  if (!esSuper()) return;
  const ks = Object.keys(admins);
  $('adListaAdmins').innerHTML = ks.length
    ? ks.map(k => {
        const a = admins[k] || {};
        return '<div class="adFila"><div class="adInfo">'
          + '<div class="adTit">' + escapa(a.nombre || '?')
          + (a.activo === false ? ' <span class="etq">' + t('admRevocar') + 'ado</span>' : '')
          + '</div>'
          + '<div class="adMeta">' + (a.rol === 'super' ? t('admRolSuper') : (a.zona || ''))
          + ' · <span class="adClave">' + k + '</span></div></div>'
          + '<div class="adBtns">'
          + (a.activo === false ? ''
              : '<button class="adNo" onclick="admRevocar(\'' + k + '\')">'
                + '<span class="mso">block</span>' + t('admRevocar') + '</button>')
          + '</div></div>';
      }).join('')
    : '<div class="vacioAdmin">—</div>';
}

function pintaLog(){
  $('adListaLog').innerHTML = logAcciones.length
    ? logAcciones.map(l => {
        const cuando = l.cuando ? new Date(l.cuando).toLocaleString(idioma) : '';
        const ic = l.que === 'verificar' ? 'check_circle'
                 : l.que === 'rechazar' ? 'cancel'
                 : l.que === 'borrar' ? 'delete'
                 : l.que === 'crear-admin' ? 'person_add' : 'block';
        return '<div class="adLogFila"><span class="mso">' + ic + '</span>'
          + '<div><b>' + escapa(l.quien || '?') + '</b> · ' + escapa(l.que || '')
          + (l.detalle ? ' · ' + escapa(l.detalle) : '') + '</div>'
          + '<span class="cuando">' + cuando + '</span></div>';
      }).join('')
    : '<div class="vacioAdmin">' + t('admNadaLog') + '</div>';
}

/* ---------- enganchar ---------- */
$('tAdmin').onclick = () => { ponPestana('tAdmin'); pintaAdmin(); };
$('adSalir').onclick = salirAdmin;
$('adCrear').onclick = admCrear;
$('adBusca').oninput = pintaTodos;
"""

rep("""/* ---------- arranque ---------- */""", JS + """
/* ---------- arranque ---------- */""")

# ---------- escuchar admins y log al arrancar ----------
rep("""firebase.initializeApp({ databaseURL: FIRE + '/' });""",
    """firebase.initializeApp({ databaseURL: FIRE + '/' });

/* los admins y el registro se escuchan siempre (son pocos datos) */
firebase.database().ref('skyreport/admins').on('value', s2 => {
  admins = s2.val() || {};
  if (yoAdmin){
    const a = admins[yoAdmin.clave];
    if (!a || a.activo === false){ salirAdmin(); }     /* si me revocaron, fuera */
    else { yoAdmin = Object.assign({ clave: yoAdmin.clave }, a); pintaAdmin(); }
  } else {
    /* ¿hay una clave guardada de antes, o viene en la dirección? */
    let k = null;
    try { k = new URLSearchParams(location.search).get('admin'); } catch(e){}
    if (!k){ try { k = localStorage.getItem('sr_admin'); } catch(e){} }
    if (k) entraAdmin(k, true);
  }
});
firebase.database().ref('skyreport/log').limitToLast(80).on('value', s2 => {
  logAcciones = [];
  s2.forEach(h => logAcciones.push(Object.assign({ _k: h.key }, h.val())));
  logAcciones.reverse();
  if ($('adListaLog') && yoAdmin) pintaLog();
});""")

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
