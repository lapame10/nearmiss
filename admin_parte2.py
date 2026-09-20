#!/usr/bin/env python3
"""Inserta la vista de admin con el ancla correcta (sin indentacion)."""
RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()

VISTA = '''<!-- ===================== ADMIN ===================== -->
<div class="vista" id="vAdmin">
  <div class="cuerpo" style="grid-template-columns:1fr">

    <div class="cabAdmin">
      <div>
        <h2><span class="mso">admin_panel_settings</span> <span data-i18n="admTitulo"></span></h2>
        <div class="adQuien" id="adQuien"></div>
      </div>
      <button class="btn claro" id="adSalir" data-i18n="admSalir"></button>
    </div>

    <!-- 1: lo pendiente de verificar -->
    <div class="bloqueAdmin">
      <h3><span class="mso">pending_actions</span>
        <span data-i18n="admPendientes"></span>
        <span class="cuenta rojo" id="adNPend">0</span></h3>
      <p class="adAyuda" data-i18n="admPendientesAyuda"></p>
      <div id="adListaPend"></div>
    </div>

    <!-- 2: todos los eventos, para corregir o borrar -->
    <div class="bloqueAdmin">
      <h3><span class="mso">list_alt</span> <span data-i18n="admTodos"></span>
        <span class="cuenta" id="adNTotal">0</span></h3>
      <p class="adAyuda" data-i18n="admTodosAyuda"></p>
      <input type="text" id="adBusca" data-i18n-ph="admBuscar" placeholder="Buscar…">
      <div id="adListaTodos"></div>
    </div>

    <!-- 3: solo para el super admin -->
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

    <!-- 4: el rastro -->
    <div class="bloqueAdmin">
      <h3><span class="mso">history</span> <span data-i18n="admRegistro"></span></h3>
      <p class="adAyuda" data-i18n="admRegistroAyuda"></p>
      <div id="adListaLog"></div>
    </div>

  </div>
</div>

'''

ANCLA = '<div class="vista" id="vMapa">'
if ANCLA in s:
    s = s.replace(ANCLA, VISTA + ANCLA, 1)
    print('  vista de admin insertada')
else:
    print('  NO ENCUENTRO el ancla')

open(RUTA, 'w', encoding='utf-8').write(s)
print('  archivo:', len(s), 'bytes')
