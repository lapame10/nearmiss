#!/usr/bin/env python3
"""La revision de producto de Pam: clasificacion, terminos y privacidad.

Pam:
 1) 'Dejar de llamar a todo incidente'. 'Reportar un evento'.
    'Que ocurrio?' con la escala: near miss / incidente / accidente /
    accidente grave / fatalidad. 'Eso hace que SkyReport sea el paraguas'.
 2) 'Como acabo?' -> 'Consecuencias' (mas sobrio para una muerte).
 3) El IGC tiene un problema de privacidad: dia + hora + ruta + sitio
    identifica al piloto aunque borres su nombre. Hay que decir la verdad.
"""
import re

RUTA = '/Users/lapame10/.hermes/workspace/nearmiss/index.html'
s = open(RUTA, encoding='utf-8').read()
toc = 0

# ==========================================================================
# 1) EL FORMULARIO: terminos nuevos y la clasificacion de Pam
# ==========================================================================
ini = s.find('        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:14px;flex-wrap:wrap">\n          <h2>Reportar un incidente o accidente</h2>')
fin = s.find('        <div class="enviarFila">')

if ini < 0 or fin < 0:
    print('  NO ENCUENTRO el bloque del formulario')
else:
    nuevo = '''        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:14px;flex-wrap:wrap">
          <h2>Reportar un evento</h2>
          <span class="avisoTop">Todo es anónimo. Los campos marcados son obligatorios.</span>
        </div>

        <div class="rejilla dos" style="margin-top:22px">

          <div class="campo">
            <div class="campoTit"><span class="num">1</span><h3>¿Qué ocurrió?</h3>
              <span class="etq req">obligatorio</span></div>
            <p class="campoAyuda">De un susto a lo peor. Esto clasifica el evento.</p>
            <div class="ops sev" id="opSev"></div>
          </div>

          <div class="campo">
            <div class="campoTit"><span class="num">2</span><h3>¿Qué pasó?</h3>
              <span class="etq req">obligatorio</span></div>
            <p class="campoAyuda">La situación concreta. Es lo que permite ver patrones después.</p>
            <div class="ops" id="opSit"></div>
            <div class="cajaOtro" id="cajaOtro">
              <label>¿Cuál? Cuéntalo en una línea</label>
              <input type="text" id="otroTexto" maxlength="70"
                placeholder="Ej: enganche con el arnés · objetivo en el aire · nudo en el freno">
            </div>
          </div>

          <div class="campo">
            <div class="campoTit"><span class="num">3</span><h3>Consecuencias</h3>
              <span class="etq req">obligatorio</span></div>
            <p class="campoAyuda">El resultado concreto.</p>
            <div class="ops cons" id="opCons"></div>
            <div class="cajaFatalidad" id="cajaFatalidad">
              <span class="mso">volunteer_activism</span>
              <div>Gracias por contarlo. <b>Es el dato que más ayuda</b> a que no
              vuelva a pasar.<br><br>
              Cuéntalo <b>sin nombres</b> y sin detalles que no aporten aprendizaje.
              Lo que importa es qué pasó y en qué condiciones, no quién.
              <br><br>
              <b>Las fatalidades no se publican al momento:</b> quedan pendientes de
              verificación para que un error o un rumor no se convierta en un dato.</div>
            </div>
          </div>

          <div class="campo">
            <div class="campoTit"><span class="num">4</span><h3>Fase del vuelo</h3>
              <span class="etq req">obligatorio</span></div>
            <p class="campoAyuda">¿En qué momento del vuelo?</p>
            <select id="selFase"><option value="">Selecciona una fase…</option></select>
          </div>

          <div class="campo">
            <div class="campoTit"><span class="num">5</span><h3>Dónde</h3>
              <span class="etq req">obligatorio</span></div>
            <p class="campoAyuda">Toca la zona en el mapa. Se guarda redondeado a ~100 m:
            suficiente para ver patrones, poco para señalar a nadie.</p>
            <div class="mapaMarcar" id="mapaMarca"></div>
          </div>

          <div class="campo">
            <div class="campoTit"><span class="num">6</span><h3>Cuándo</h3>
              <span class="etq opc">opcional</span></div>
            <p class="campoAyuda">Con el día saco el viento real que hacía ahí.
            <b>El día no se publica</b>: se guarda el mes y el año.</p>
            <input type="date" id="fecha">
          </div>

          <div class="campo">
            <div class="campoTit"><span class="num">7</span><h3>Franja del día</h3>
              <span class="etq req">obligatorio</span></div>
            <p class="campoAyuda">Se publica la franja, nunca la hora.</p>
            <div class="ops" id="opFranja" style="grid-template-columns:repeat(2,1fr)"></div>
          </div>

          <div class="campo">
            <div class="campoTit"><span class="num">8</span><h3>Cómo estaba el aire</h3>
              <span class="etq opc">opcional</span></div>
            <p class="campoAyuda">Lo que tú sentiste. El dato real del viento lo saco yo.</p>
            <div class="ops" id="opAire"></div>
          </div>

          <div class="campo">
            <div class="campoTit"><span class="num">9</span><h3>Tu archivo de vuelo</h3>
              <span class="etq opc">opcional</span></div>
            <p class="campoAyuda">Un IGC identifica un vuelo concreto. Lee esto antes.</p>
            <div class="igcBox">
              <button class="btnIgc" id="bIGC"><span class="mso">upload_file</span> Subir mi archivo IGC</button>
              <input type="file" id="ficheroIGC" accept=".igc,text/plain" style="display:none">
              <div class="igcInfo" id="igcInfo"></div>
              <label class="marcaCheck">
                <input type="checkbox" id="borrarTrack" checked>
                <span>Borrar el track después de procesarlo</span>
              </label>
            </div>
          </div>

        </div>

        <div style="margin-top:22px">
          <div class="campoTit"><span class="num">10</span><h3>Cuéntalo</h3>
            <span class="etq opc">opcional</span></div>
          <p class="campoAyuda">Sin nombres. El detalle que identifica a alguien, fuera;
          el que explica lo que pasó, dentro.</p>
          <textarea id="relato" maxlength="1000"
            placeholder="Escribe aquí tu relato (opcional)..."></textarea>
          <div class="contador"><span id="cuentaTxt">0</span> / 1000</div>
        </div>

        <div class="privacidad">
          <span class="mso">lock</span>
          <div><b>Qué se publica y qué no.</b><br>
          <b>Se publica:</b> el mes y el año, la zona redondeada, la franja del día,
          la situación y las consecuencias.<br>
          <b>No se publica nunca:</b> tu nombre, el día exacto, la hora exacta, tu
          posición precisa, ni el archivo IGC. El archivo se usa solo para leer las
          condiciones del vuelo y no se queda.</div>
        </div>

'''
    s = s[:ini] + nuevo + s[fin:]
    toc += 1
    print('  OK: formulario reescrito con la clasificacion de Pam')

# ==========================================================================
# 2) LAS DEFINICIONES EN EL JS
# ==========================================================================
viejo2 = s[s.find('const TIPOS = ['):s.find('const FASES = [')]
nuevo2 = '''/* ==========================================================================
   LA CLASIFICACIÓN (revisión de Pam)
   --------------------------------------------------------------------------
   Pam: 'dejar de llamar a todo incidente'. SkyReport tiene que ser el PARABUAS
   de todo lo que pasa volando, de un susto a una fatalidad. Así que ahora hay
   TRES preguntas distintas que antes estaban mezcladas en una:

     1. ¿Qué ocurrió?   -> la GRAVEDAD del evento (near miss ... fatalidad)
     2. ¿Qué pasó?      -> la SITUACIÓN concreta (plegada, sotavento...) que es
                           lo que luego genera los patrones
     3. Consecuencias   -> el RESULTADO (sin lesiones ... fatalidad)
   ========================================================================== */

/* 1 · la gravedad. Esto es lo que hace que SkyReport sea el paraguas */
const SEVERIDAD = [
  { id:'near',      e:'warning',         n:'Near miss / casi accidente' },
  { id:'incidente', e:'error_outline',   n:'Incidente' },
  { id:'accidente', e:'report_problem',  n:'Accidente' },
  { id:'grave',     e:'personal_injury', n:'Accidente grave' },
  { id:'fatal',     e:'emergency',       n:'Fatalidad' },
];

/* 2 · la situación. Aquí está el valor: es lo que permite decir
   '17 eventos con sotavento' o '8 proximidades entre pilotos' */
const SITUACION = [
  { id:'plegada',    e:'air',            n:'Plegada o cierre' },
  { id:'proximidad', e:'groups',         n:'Proximidad entre pilotos' },
  { id:'sotavento',  e:'landscape',      n:'Sotavento' },
  { id:'rotor',      e:'storm',          n:'Rotor o turbulencia' },
  { id:'cable',      e:'cable',          n:'Cable o tendido' },
  { id:'arbol',      e:'forest',         n:'Árbol o zona arbolada' },
  { id:'despegue',   e:'flight_takeoff', n:'Despegue' },
  { id:'aterrizaje', e:'flight_land',    n:'Aterrizaje' },
  { id:'bajo',       e:'trending_down',  n:'Quedarse bajo' },
  { id:'otro',       e:'more_horiz',     n:'Otro' },
];

/* 3 · las consecuencias. '¿Cómo acabó?' sonaba feo para una muerte. */
const CONSEC = [
  { id:'sin',    e:'check_circle',    n:'Sin lesiones' },
  { id:'leves',  e:'healing',         n:'Lesiones leves' },
  { id:'graves', e:'personal_injury', n:'Lesiones graves' },
  { id:'danos',  e:'car_crash',       n:'Daños materiales' },
  { id:'fatal',  e:'emergency',       n:'Fatalidad' },
];

'''
if viejo2:
    s = s.replace(viejo2, nuevo2, 1); toc += 1
    print('  OK: definiciones nuevas (SEVERIDAD / SITUACION / CONSEC)')
else:
    print('  NO ENCUENTRO las definiciones viejas')

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
