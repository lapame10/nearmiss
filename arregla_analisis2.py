#!/usr/bin/env python3
"""Lo que quedaba del analisis:

- El CSS muerto (.ops.gravedad -> .ops.cons, y fatalidad -> fatal)
- Traducir el bloque del ADMIN y el boton de instalar a fr, de y pt
- El string suelto 'Aun no hay zonas con reportes.'
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
# 1) EL CSS MUERTO
# La clase real es 'cons' (el div es <div class="ops cons" id="opCons">) y el id
# real de la fatalidad es 'fatal', no 'fatalidad'. Asi que estas 8 reglas no
# casaban NUNCA: los botones de consecuencias no cambiaban de color al marcarlos.
# ==========================================================================
rep('.ops.gravedad', '.ops.cons', todas=True)
rep("[data-id=fatalidad]", "[data-id=fatal]", todas=True)

# ==========================================================================
# 2) EL STRING SUELTO
# ==========================================================================
rep("""      : '<div style="font-size:12px;color:var(--gris)">Aún no hay zonas con reportes.</div>';""",
    """      : '<div style="font-size:12px;color:var(--gris)">' + t('zonasNada') + '</div>';""")

rep("    empezando: 'La base de conocimiento está empezando.<br>Cada reporte ayuda a construirla.',",
    "    empezando: 'La base de conocimiento está empezando.<br>Cada reporte ayuda a construirla.',\n"
    "    zonasNada: 'Aún no hay zonas con reportes.',")
rep("    empezando: 'The knowledge base is just starting.<br>Every report helps build it.',",
    "    empezando: 'The knowledge base is just starting.<br>Every report helps build it.',\n"
    "    zonasNada: 'No areas with reports yet.',")

# ==========================================================================
# 3) LAS TRADUCCIONES QUE FALTABAN (fr, de, pt)
# ==========================================================================
FR = """
    /* --- admin (francés) --- */
    instBoton: 'Installer l’application',
    instTitulo: 'Ajoute-le à ton écran d’accueil',
    instTexto: 'Sur iPhone il n’y a pas de bouton d’installation. Voici comment :<br><br>'
      + '<b>1.</b> Touche le bouton <b>Partager</b> (le carré avec la flèche).<br>'
      + '<b>2.</b> Fais défiler et touche <b>« Sur l’écran d’accueil »</b>.<br>'
      + '<b>3.</b> Donne-lui un nom et touche <b>Ajouter</b>.<br><br>'
      + 'Et voilà : sa propre icône, comme une app. <b>Et ça marche sans réseau.</b>',
    zonasNada: 'Pas encore de zones avec des signalements.',
    admTitulo: 'Administration',
    admSalir: 'Quitter',
    admPendientes: 'En attente de vérification',
    admPendientesAyuda: 'Les accidents mortels ne sont pas publiés tant que quelqu’un '
      + 'ne les a pas confirmés. C’est ton rôle. En cas de doute, ne publie pas : '
      + 'une donnée fausse fait plus de dégâts qu’une donnée manquante.',
    admTodos: 'Tous les événements',
    admTodosAyuda: 'Tu peux corriger une donnée mal saisie ou supprimer un événement. '
      + 'Supprimer ne détruit pas : une copie est conservée au cas où.',
    admBuscar: 'Chercher par site, type ou texte…',
    admEquipo: 'Qui peut administrer',
    admEquipoAyuda: 'Donne une clé à chaque personne de confiance. Tu peux la révoquer '
      + 'quand tu veux. Les admins de zone ne voient et ne touchent que leur zone.',
    admNombre: 'Nom',
    admZona: 'Zone (ex : Valle de Bravo)',
    admCrear: 'Créer une clé',
    admRegistro: 'Journal des actions',
    admRegistroAyuda: 'Qui a fait quoi et quand. Cela ne peut pas être supprimé.',
    admPub: 'Publier', admRech: 'Refuser', admEditar: 'Modifier',
    admBorrar: 'Supprimer', admRevocar: 'Révoquer',
    admTuClave: 'Ta clé',
    admPuerta: 'Entrer comme administrateur',
    admPuertaAyuda: 'Colle ici la clé qu’on t’a donnée. Elle reste sur cet appareil et '
      + 'n’est envoyée nulle part.',
    admClaveMal: 'Cette clé n’est pas valable. Vérifie-la, ou demande-en une autre.',
    admEres: 'Tu es <b>{n}</b> · {r}',
    admRolSuper: 'super admin (tu peux tout)',
    admRolZona: 'responsable de <b>{z}</b>',
    admRolVer: 'vérificateur',
    admSinPermiso: 'Cet événement n’est pas dans ta zone.',
    admPublicado: 'Publié. Il est sur la carte.',
    admRechazado: 'Refusé. Il ne sera pas publié, mais la trace reste.',
    admBorrado: 'Supprimé. C’est réversible : une copie est conservée.',
    admNadaPend: 'Rien en attente. Tout est vérifié.',
    admNadaLog: 'Rien n’a encore été fait.',
    admConfirmBorrar: 'Supprimer cet événement ? C’est réversible.',
    admOk: 'C’est fait',"""

DE = """
    /* --- admin (alemán) --- */
    instBoton: 'App installieren',
    instTitulo: 'Zum Home-Bildschirm hinzufügen',
    instTexto: 'Auf dem iPhone gibt es keinen Installationsknopf. So geht es:<br><br>'
      + '<b>1.</b> Tippe auf <b>Teilen</b> (das Quadrat mit dem Pfeil).<br>'
      + '<b>2.</b> Scrolle und tippe auf <b>„Zum Home-Bildschirm“</b>.<br>'
      + '<b>3.</b> Gib einen Namen und tippe auf <b>Hinzufügen</b>.<br><br>'
      + 'Fertig — mit eigenem Symbol, wie eine App. <b>Und sie funktioniert ohne Netz.</b>',
    zonasNada: 'Noch keine Gebiete mit Meldungen.',
    admTitulo: 'Verwaltung',
    admSalir: 'Abmelden',
    admPendientes: 'Prüfung ausstehend',
    admPendientesAyuda: 'Tödliche Unfälle werden erst veröffentlicht, wenn jemand sie '
      + 'bestätigt hat. Das ist deine Aufgabe. Im Zweifel nicht veröffentlichen: eine '
      + 'falsche Angabe schadet mehr als eine fehlende.',
    admTodos: 'Alle Ereignisse',
    admTodosAyuda: 'Du kannst eine falsche Angabe korrigieren oder ein Ereignis löschen. '
      + 'Löschen zerstört nichts: eine Kopie bleibt erhalten.',
    admBuscar: 'Nach Ort, Art oder Text suchen…',
    admEquipo: 'Wer verwalten darf',
    admEquipoAyuda: 'Gib jeder Vertrauensperson einen Schlüssel. Du kannst ihn jederzeit '
      + 'entziehen. Gebiets-Admins sehen und bearbeiten nur ihr Gebiet.',
    admNombre: 'Name',
    admZona: 'Gebiet (z. B. Valle de Bravo)',
    admCrear: 'Schlüssel erstellen',
    admRegistro: 'Aktionsprotokoll',
    admRegistroAyuda: 'Wer was getan hat und wann. Das lässt sich nicht löschen.',
    admPub: 'Veröffentlichen', admRech: 'Ablehnen', admEditar: 'Bearbeiten',
    admBorrar: 'Löschen', admRevocar: 'Entziehen',
    admTuClave: 'Dein Schlüssel',
    admPuerta: 'Als Administrator anmelden',
    admPuertaAyuda: 'Füge hier den Schlüssel ein, den du bekommen hast. Er bleibt auf '
      + 'diesem Gerät und wird nirgendwohin gesendet.',
    admClaveMal: 'Dieser Schlüssel ist ungültig. Prüfe ihn, oder bitte um einen neuen.',
    admEres: 'Du bist <b>{n}</b> · {r}',
    admRolSuper: 'Super-Admin (du darfst alles)',
    admRolZona: 'verantwortlich für <b>{z}</b>',
    admRolVer: 'Prüfer',
    admSinPermiso: 'Dieses Ereignis liegt nicht in deinem Gebiet.',
    admPublicado: 'Veröffentlicht. Es ist auf der Karte.',
    admRechazado: 'Abgelehnt. Es wird nicht veröffentlicht, bleibt aber protokolliert.',
    admBorrado: 'Gelöscht. Rückgängig möglich: eine Kopie bleibt erhalten.',
    admNadaPend: 'Nichts offen. Alles geprüft.',
    admNadaLog: 'Bisher wurde nichts getan.',
    admConfirmBorrar: 'Dieses Ereignis löschen? Es ist rückgängig zu machen.',
    admOk: 'Erledigt',"""

PT = """
    /* --- admin (português) --- */
    instBoton: 'Instalar a aplicação',
    instTitulo: 'Adiciona ao ecrã principal',
    instTexto: 'No iPhone não há botão de instalação. É assim:<br><br>'
      + '<b>1.</b> Toca em <b>Partilhar</b> (o quadrado com a seta).<br>'
      + '<b>2.</b> Desce e toca em <b>«Adicionar ao ecrã principal»</b>.<br>'
      + '<b>3.</b> Dá-lhe um nome e toca em <b>Adicionar</b>.<br><br>'
      + 'E fica com o seu ícone, como uma app. <b>E funciona sem rede.</b>',
    zonasNada: 'Ainda não há zonas com relatos.',
    admTitulo: 'Administração',
    admSalir: 'Sair',
    admPendientes: 'Pendentes de verificação',
    admPendientesAyuda: 'As fatalidades não são publicadas até alguém as confirmar. '
      + 'É a tua decisão. Em caso de dúvida, não publiques: um dado falso faz mais '
      + 'dano do que um dado em falta.',
    admTodos: 'Todos os eventos',
    admTodosAyuda: 'Podes corrigir um dado mal introduzido ou apagar um evento. Apagar '
      + 'não destrói: fica uma cópia para o caso de ser preciso.',
    admBuscar: 'Procurar por local, tipo ou texto…',
    admEquipo: 'Quem pode administrar',
    admEquipoAyuda: 'Dá uma chave a cada pessoa de confiança. Podes revogá-la quando '
      + 'quiseres. Os admins de zona só veem e mexem na sua zona.',
    admNombre: 'Nome',
    admZona: 'Zona (ex: Valle de Bravo)',
    admCrear: 'Criar chave',
    admRegistro: 'Registo de ações',
    admRegistroAyuda: 'Quem fez o quê e quando. Isto não se pode apagar.',
    admPub: 'Publicar', admRech: 'Rejeitar', admEditar: 'Editar',
    admBorrar: 'Apagar', admRevocar: 'Revogar',
    admTuClave: 'A tua chave',
    admPuerta: 'Entrar como administrador',
    admPuertaAyuda: 'Cola aqui a chave que te deram. Fica neste dispositivo e não é '
      + 'enviada para lado nenhum.',
    admClaveMal: 'Essa chave não é válida. Confirma-a, ou pede outra.',
    admEres: 'És <b>{n}</b> · {r}',
    admRolSuper: 'super admin (podes tudo)',
    admRolZona: 'responsável por <b>{z}</b>',
    admRolVer: 'verificador',
    admSinPermiso: 'Esse evento não é da tua zona.',
    admPublicado: 'Publicado. Já está no mapa.',
    admRechazado: 'Rejeitado. Não será publicado, mas fica o registo.',
    admBorrado: 'Apagado. Dá para desfazer: fica uma cópia.',
    admNadaPend: 'Nada pendente. Tudo verificado.',
    admNadaLog: 'Ainda não se fez nada.',
    admConfirmBorrar: 'Apagar este evento? Dá para desfazer.',
    admOk: 'Feito',"""


def añade_al_bloque(idioma, texto):
    """Mete el texto antes del cierre del bloque de ese idioma."""
    global s
    ini = s.find('\n  ' + idioma + ': {')
    if ini < 0:
        print('  NO encuentro el bloque', idioma)
        return False
    # busco el cierre: la primera linea que sea exactamente '  },'  despues
    j = s.find('\n  },', ini)
    if j < 0:
        print('  NO encuentro el cierre de', idioma)
        return False
    # el cierre real del bloque: busco '  },' DESPUES del ultimo '  },' del idioma
    # mas simple: cuento llaves desde el inicio del bloque
    i = s.find('{', ini)
    n, k = 0, i
    while k < len(s):
        if s[k] == '{': n += 1
        elif s[k] == '}':
            n -= 1
            if n == 0: break
        k += 1
    s = s[:k] + texto + '\n  ' + s[k:]
    return True


for idioma, txt in [('fr', FR), ('de', DE), ('pt', PT)]:
    if añade_al_bloque(idioma, txt):
        toc += 1
        print('  bloque', idioma, 'ampliado')

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
