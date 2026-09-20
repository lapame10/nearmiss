#!/usr/bin/env python3
"""LA PÁGINA DE ADMINISTRACIÓN de SkyReport (petición de Pam).

Pam: 'me falta una opcion de administrador, que yo pueda darle ese perfil a
diferentes personas que sean los encargados por zona, para que puedan activar o
no las fatalidades, o administrar la pagina, incidentes y todo por si vemos que
hay fallos, algo que borrar o modificar'.

LAS DECISIONES DE DISEÑO (y por qué):

1) SIN CONTRASEÑAS NI CUENTAS, con CLAVES. La app no tiene usuarios y montar
   login+correo+recuperación sería otro producto. Una clave larga se le da a
   quien se quiera, y se puede revocar borrándola. Coherente con el resto.

2) DOS ROLES, no cinco:
   - SUPER  -> todo: verificar, editar, borrar, y crear/revocar admins
   - ZONA   -> solo lo de SU zona: verificar fatalidades, editar y borrar
   Menos roles = menos confusión. Se pueden añadir después.

3) LO QUE DE VERDAD HACE FALTA, en orden de importancia:
   a) VERIFICAR FATALIDADES (publicar o rechazar). Es lo que pedía Pam y lo
      que hace que la etiqueta 'pendiente de verificación' signifique algo.
   b) BORRAR un evento (spam, duplicado, ofensivo, broma).
   c) EDITAR un dato mal puesto (la ubicación, la fecha, la gravedad).
   d) REGISTRO DE ACCIONES: quién hizo qué y cuándo. Sin esto, un admin puede
      abusar y no queda rastro. En una app de seguridad, el rastro ES el
      producto.

4) LO QUE UN ADMIN **NO** PUEDE HACER NUNCA:
   - Ver datos personales (no los hay, y no se van a pedir).
   - Ver la ubicación exacta (solo ve lo mismo que todos: aproximado).
   Porque si el admin pudiera desanonimizar, el anonimato ya no valdría nada.

5) BORRAR NO ES BORRAR: el evento se copia a 'papelera' antes. Así una
   equivocación se puede deshacer y queda el rastro.
"""
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
# 1) EL BOTON DE ADMIN EN EL NAV (solo sale si has entrado con una clave)
# ==========================================================================
rep("""    <button id="tPatrones"><span class="mso">bar_chart</span><span data-i18n="navPatrones">Patrones</span></button>""",
    """    <button id="tPatrones"><span class="mso">bar_chart</span><span data-i18n="navPatrones">Patrones</span></button>
    <button id="tAdmin" style="display:none"><span class="mso">admin_panel_settings</span><span data-i18n="navAdmin">Admin</span></button>""")

# ==========================================================================
# 2) LA VISTA DE ADMIN
# ==========================================================================
rep("""  <div class="vista" id="vMapa">""",
    """  <!-- ===================== ADMIN ===================== -->
  <div class="vista" id="vAdmin">
    <div class="cuerpo" style="grid-template-columns:1fr">

      <div class="cabAdmin">
        <div>
          <h2><span class="mso">admin_panel_settings</span> <span data-i18n="admTitulo"></span></h2>
          <div class="adQuien" id="adQuien"></div>
        </div>
        <button class="btn claro" id="adSalir" data-i18n="admSalir"></button>
      </div>

      <!-- lo primero: lo que está pendiente de verificar -->
      <div class="bloqueAdmin" id="adPendientes">
        <h3><span class="mso">pending_actions</span>
          <span data-i18n="admPendientes"></span>
          <span class="cuenta rojo" id="adNPend">0</span></h3>
        <p class="adAyuda" data-i18n="admPendientesAyuda"></p>
        <div id="adListaPend"></div>
      </div>

      <!-- todos los eventos, para corregir o borrar -->
      <div class="bloqueAdmin">
        <h3><span class="mso">list_alt</span> <span data-i18n="admTodos"></span>
          <span class="cuenta" id="adNTotal">0</span></h3>
        <p class="adAyuda" data-i18n="admTodosAyuda"></p>
        <input type="text" id="adBusca" data-i18n-ph="admBuscar" placeholder="Buscar…">
        <div id="adListaTodos"></div>
      </div>

      <!-- solo para el super admin: gestionar quién más puede -->
      <div class="bloqueAdmin" id="adAdmins" style="display:none">
        <h3><span class="mso">group</span> <span data-i18n="admEquipo"></span></h3>
        <p class="adAyuda" data-i18n="admEquipoAyuda"></p>
        <div class="adNuevo">
          <input type="text" id="adNuevoNombre" data-i18n-ph="admNombre" placeholder="Nombre">
          <input type="text" id="adNuevoZona" data-i18n-ph="admZona" placeholder="Zona (ej: Valle de Bravo)">
          <select id="adNuevoRol">
            <option value="zona">Zona</option>
            <option value="super">Super admin</option>
          </select>
          <button class="btn" id="adCrear" data-i18n="admCrear"></button>
        </div>
        <div id="adListaAdmins"></div>
      </div>

      <!-- el rastro: quién hizo qué -->
      <div class="bloqueAdmin">
        <h3><span class="mso">history</span> <span data-i18n="admRegistro"></span></h3>
        <p class="adAyuda" data-i18n="admRegistroAyuda"></p>
        <div id="adListaLog"></div>
      </div>

    </div>
  </div>

  <div class="vista" id="vMapa">""")

# ==========================================================================
# 3) EL CSS
# ==========================================================================
rep("""  /* ===== EL PUNTO QUE HAS TOCADO =====""",
    """  /* ==========================================================================
     LA PÁGINA DE ADMINISTRACIÓN
     Discreta y sobria: quien entra aquí no viene a mirar, viene a resolver algo.
     ========================================================================== */
  .cabAdmin{display:flex;justify-content:space-between;align-items:flex-start;
    gap:16px;flex-wrap:wrap;margin-bottom:18px}
  .cabAdmin h2{margin:0;font-size:23px;letter-spacing:-.6px;display:flex;
    align-items:center;gap:9px}
  .cabAdmin h2 .mso{font-size:26px;color:var(--mar)}
  .adQuien{font-size:12.5px;color:var(--gris);margin-top:6px;line-height:1.5}
  .adQuien b{color:var(--tinta)}
  .bloqueAdmin{background:var(--papel);border-radius:13px;padding:18px;
    box-shadow:0 1px 3px rgba(22,50,59,.08);margin-bottom:16px}
  .bloqueAdmin h3{margin:0 0 4px;font-size:15px;display:flex;align-items:center;gap:8px}
  .bloqueAdmin h3 .mso{font-size:20px;color:var(--mar)}
  .cuenta{background:#eef3f6;color:var(--mar);font-size:12px;font-weight:800;
    border-radius:20px;padding:2px 9px;margin-left:auto}
  .cuenta.rojo{background:#fbeeec;color:#8f3f36}
  .adAyuda{font-size:12.5px;color:var(--gris);line-height:1.55;margin:0 0 14px}
  .adFila{display:flex;justify-content:space-between;align-items:flex-start;gap:14px;
    padding:13px 0;border-top:1px solid var(--linea);flex-wrap:wrap}
  .adFila:first-child{border-top:none}
  .adFila .adInfo{flex:1;min-width:220px}
  .adFila .adTit{font-weight:800;font-size:13.5px;display:flex;align-items:center;gap:7px}
  .adFila .adMeta{font-size:12px;color:var(--gris);margin-top:4px;line-height:1.5}
  .adFila .adRelato{font-size:12.5px;color:#4a6470;margin-top:7px;line-height:1.55;
    font-style:italic}
  .adBtns{display:flex;gap:7px;flex-wrap:wrap;align-items:flex-start}
  .adBtns button{border:none;border-radius:9px;padding:9px 14px;font-family:inherit;
    font-size:12.5px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:5px}
  .adBtns button .mso{font-size:17px}
  .adOk{background:#e8f5ec;color:#1f6b40}
  .adOk:hover{background:#d5ecdd}
  .adNo{background:#fbeeec;color:#8f3f36}
  .adNo:hover{background:#f6ddd9}
  .adEd{background:#eef2f4;color:#3b5560}
  .adEd:hover{background:#e0e7ea}
  .adDel{background:#fdf1e8;color:#96500f}
  .adDel:hover{background:#fae3d0}
  .adNuevo{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px}
  .adNuevo input,.adNuevo select{flex:1;min-width:130px;font-family:inherit;font-size:13.5px;
    padding:11px 12px;border:2px solid var(--linea);border-radius:10px;background:#fbfdfd;
    color:var(--tinta);-webkit-appearance:none;appearance:none}
  .adNuevo input:focus,.adNuevo select:focus{outline:none;border-color:var(--mar)}
  .adNuevo button{flex:0 0 auto;margin:0}
  .adClave{font-family:ui-monospace,Menlo,monospace;font-size:13px;font-weight:700;
    background:#eef3f6;border-radius:7px;padding:5px 9px;color:var(--mar);
    letter-spacing:1px;user-select:all}
  .adLogFila{display:flex;gap:11px;padding:9px 0;border-top:1px solid var(--linea);
    font-size:12.5px;align-items:baseline}
  .adLogFila:first-child{border-top:none}
  .adLogFila .mso{font-size:17px;color:var(--gris);flex-shrink:0}
  .adLogFila .cuando{color:var(--gris);font-size:11.5px;white-space:nowrap;margin-left:auto}
  .vacioAdmin{font-size:13px;color:var(--gris);line-height:1.6;padding:14px 0}

  /* la pantalla de entrada con la clave */
  .puerta{background:var(--papel);border-radius:13px;padding:26px;max-width:430px;
    box-shadow:0 2px 10px rgba(22,50,59,.1);margin:0 auto}
  .puerta h2{margin:0 0 6px;font-size:20px;display:flex;align-items:center;gap:9px}
  .puerta p{font-size:13px;color:var(--gris);line-height:1.55;margin:0 0 16px}
  .puerta input{width:100%;font-family:ui-monospace,Menlo,monospace;font-size:16px;
    letter-spacing:3px;text-align:center;padding:14px;border:2px solid var(--linea);
    border-radius:11px;background:#fbfdfd;text-transform:uppercase}
  .puerta input:focus{outline:none;border-color:var(--mar)}
  .puerta .err{color:var(--rojo);font-size:12.5px;margin-top:10px;display:none}
  .puerta .err.on{display:block}

  /* ===== EL PUNTO QUE HAS TOCADO =====""")

# ==========================================================================
# 4) LOS TEXTOS (español e inglés; los otros tres caen al inglés si falta)
# ==========================================================================
rep("""    todos: 'Todos',
    subTitulo: 'Reportes anónimos de eventos de parapente',""",
    """    todos: 'Todos',
    /* --- admin --- */
    navAdmin: 'Admin',
    admTitulo: 'Administración',
    admSalir: 'Salir',
    admPendientes: 'Pendientes de verificar',
    admPendientesAyuda: 'Las fatalidades no se publican hasta que alguien las '
      + 'confirma. Aquí decides. Si dudas, no la publiques: un dato falso hace '
      + 'más daño que un dato que falta.',
    admTodos: 'Todos los eventos',
    admTodosAyuda: 'Puedes corregir un dato mal puesto o borrar un evento. Borrar '
      + 'no borra: se guarda una copia por si hay que deshacerlo.',
    admBuscar: 'Buscar por sitio, tipo o texto…',
    admEquipo: 'Quién puede administrar',
    admEquipoAyuda: 'Dale una clave a cada persona de confianza. Puedes revocarla '
      + 'cuando quieras. Los de zona solo ven y tocan lo de su zona.',
    admNombre: 'Nombre',
    admZona: 'Zona (ej: Valle de Bravo)',
    admCrear: 'Dar clave',
    admRegistro: 'Registro de acciones',
    admRegistroAyuda: 'Quién hizo qué y cuándo. Esto no se puede borrar.',
    admPub: 'Publicar', admRech: 'Rechazar', admEditar: 'Editar',
    admBorrar: 'Borrar', admRevocar: 'Revocar',
    admTuClave: 'Tu clave',
    admPuerta: 'Entrar como administrador',
    admPuertaAyuda: 'Pega aquí la clave que te dieron. Se queda guardada en este '
      + 'dispositivo y no se envía a ningún sitio.',
    admClaveMal: 'Esa clave no vale. Mírala bien, o pídele otra a quien te la dio.',
    admEres: 'Eres <b>{n}</b> · {r}',
    admRolSuper: 'super admin (puedes todo)',
    admRolZona: 'encargado de <b>{z}</b>',
    admRolVer: 'verificador',
    admSinPermiso: 'Ese evento no es de tu zona.',
    admPublicado: 'Publicado. Ya se ve en el mapa.',
    admRechazado: 'Rechazado. No se publicará, pero queda el registro.',
    admBorrado: 'Borrado. Se puede deshacer: hay copia.',
    admNadaPend: 'No hay nada pendiente. Todo verificado.',
    admNadaLog: 'Todavía no se ha hecho nada.',
    admConfirmBorrar: '¿Seguro que quieres borrar este evento? Se puede deshacer.',
    admOk: 'Hecho',
    subTitulo: 'Reportes anónimos de eventos de parapente',""")

rep("""    todos: 'All',
    subTitulo: 'Anonymous paragliding event reports',""",
    """    todos: 'All',
    navAdmin: 'Admin',
    admTitulo: 'Administration',
    admSalir: 'Sign out',
    admPendientes: 'Pending verification',
    admPendientesAyuda: 'Fatalities are not published until somebody confirms '
      + 'them. That is your call. If in doubt, do not publish: a false entry '
      + 'does more damage than a missing one.',
    admTodos: 'All events',
    admTodosAyuda: 'You can fix a wrong detail or delete an event. Deleting does '
      + 'not destroy: a copy is kept in case it needs undoing.',
    admBuscar: 'Search by site, type or text…',
    admEquipo: 'Who can administer',
    admEquipoAyuda: 'Give a key to each trusted person. You can revoke it any '
      + 'time. Zone admins only see and touch their own zone.',
    admNombre: 'Name',
    admZona: 'Zone (e.g. Valle de Bravo)',
    admCrear: 'Issue key',
    admRegistro: 'Action log',
    admRegistroAyuda: 'Who did what and when. This cannot be deleted.',
    admPub: 'Publish', admRech: 'Reject', admEditar: 'Edit',
    admBorrar: 'Delete', admRevocar: 'Revoke',
    admTuClave: 'Your key',
    admPuerta: 'Sign in as administrator',
    admPuertaAyuda: 'Paste the key you were given. It stays on this device and is '
      + 'never sent anywhere.',
    admClaveMal: 'That key is not valid. Check it, or ask for another one.',
    admEres: 'You are <b>{n}</b> · {r}',
    admRolSuper: 'super admin (you can do everything)',
    admRolZona: 'zone admin for <b>{z}</b>',
    admRolVer: 'verifier',
    admSinPermiso: 'That event is not in your zone.',
    admPublicado: 'Published. It is on the map now.',
    admRechazado: 'Rejected. It will not be published, but the record stays.',
    admBorrado: 'Deleted. It can be undone: a copy is kept.',
    admNadaPend: 'Nothing pending. All verified.',
    admNadaLog: 'Nothing has been done yet.',
    admConfirmBorrar: 'Delete this event? It can be undone.',
    admOk: 'Done',
    subTitulo: 'Anonymous paragliding event reports',""")

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
