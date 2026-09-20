#!/usr/bin/env python3
"""Añade francés, alemán y portugués, y el idioma automático por país.

Pam: 'me gustaria agregar frances, aleman, portugues.... tambien quiero que
depende donde te encuentres en el mundo la pagina se abra en ese idioma por
default, o si podemos saber el idioma del usuario por default'.

COMO SE SABE EL PAIS SIN PEDIR EL GPS NI LLAMAR A NINGUNA API:
por la ZONA HORARIA del navegador (Intl.DateTimeFormat timeZone). 'Europe/Paris'
-> frances, 'America/Sao_Paulo' -> portugues. Es gratis, instantaneo y no
molesta a nadie con un permiso.
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
# LOS TRES BLOQUES NUEVOS, justo antes del cierre del diccionario
# ==========================================================================
NUEVOS = r"""
  /* ==================== FRANCÉS ==================== */
  fr: {
    lema: 'Une communauté<br>pour des vols plus sûrs',
    navMapa: 'Carte', navReportar: 'Signaler', navPatrones: 'Tendances',
    heroTitulo: 'Sécurité partagée. Apprentissage collectif.',
    heroTexto: 'Ici, tu peux signaler un événement de parapente de façon anonyme.<br>'
             + 'On ne cherche pas de coupable : on cherche à apprendre pour que '
             + 'tout le monde rentre à la maison.',
    heroCita: '<b>« Chaque expérience compte.</b> Un vol plus sûr commence par '
            + 'raconter ce qui s’est passé. »',
    formTitulo: 'Signaler un événement',
    formAviso: 'Tout est anonyme. Les champs marqués sont obligatoires.',
    c1t: 'Que s’est-il passé ?', c1a: 'Classe le niveau de l’événement, du presque-accident à l’accident mortel.',
    c2t: 'De quoi s’agissait-il ?', c2a: 'La situation concrète. C’est ce qui permet de voir des tendances ensuite.',
    c3t: 'Conséquences', c3a: 'Le résultat concret.',
    c4t: 'Phase du vol', c4a: 'À quel moment du vol ?',
    c5t: 'Où', c5a: 'Touche la zone sur la carte. La localisation publique est donnée de façon '
                  + 'approximative, pour réduire la possibilité d’identifier le pilote.',
    c6t: 'Quand', c6a: 'Avec le jour, j’obtiens le vent qu’il faisait là-bas. '
                    + '<b>Le jour n’est jamais publié</b> : seul le mois et l’année sont conservés.',
    c7t: 'Moment de la journée', c7a: 'C’est le moment qui est publié, jamais l’heure.',
    c8t: 'Comment était l’air', c8a: 'Ce que tu as ressenti. Si tu indiques la date et le lieu, SkyReport '
                                  + 'peut compléter le rapport avec les données météo enregistrées de cette zone.',
    c9t: 'Ton fichier de vol', c9a: 'Un IGC identifie un vol précis. Lis comment il est traité avant de l’envoyer.',
    c10t: 'Raconte', c10a: 'Pas de noms. Ce qui identifie quelqu’un, dehors ; ce qui explique ce qui s’est passé, dedans.',
    obligatorio: 'obligatoire', opcional: 'facultatif',
    otroTitulo: 'Lequel ? Décris-le en une ligne',
    otroEjemplo: 'Ex : accrochage du harnais · quelqu’un en l’air · nœud dans le frein',
    fatalTexto: '<b>Merci de le raconter.</b> C’est la donnée qui aide le plus à éviter que cela se reproduise.'
              + '<br><br>Raconte-le <b>sans noms</b> et sans détails qui n’apportent rien. Ce qui compte, '
              + 'c’est ce qui s’est passé et dans quelles conditions, pas qui.<br><br>'
              + '<b>Les accidents mortels ne sont pas publiés tout de suite :</b> ils restent en attente de '
              + 'vérification, pour qu’une erreur ou une rumeur ne devienne pas une donnée.',
    igcBoton: 'Envoyer mon fichier IGC',
    igcNota: 'Le fichier est supprimé automatiquement après l’extraction des données nécessaires : '
           + 'l’heure du vol et l’altitude maximale. Il n’est jamais conservé ni publié.',
    relatoEjemplo: 'Écris ton récit ici (facultatif)...',
    privacidad: '<b>Ce qui est publié et ce qui ne l’est pas.</b><br><b>Publié :</b> le mois et l’année, '
              + 'la localisation approximative, le moment de la journée, la situation et les conséquences.'
              + '<br><b>Jamais publié :</b> ton nom, le jour exact, l’heure exacte, ta position précise, '
              + 'ni le fichier IGC. Le fichier sert uniquement à lire les conditions du vol et il est supprimé aussitôt.',
    enviar: 'Envoyer l’événement anonyme',
    evEventos: 'événements', evEvento: 'événement',
    evSitios: 'sites', evSitio: 'site',
    empezando: 'La base de connaissances commence.<br>Chaque signalement aide à la construire.',
    evPatrones: 'tendances', evPatron: 'tendance',
    principios: 'Principes',
    p1: 'La sécurité avant tout', p1s: 'On apprend de l’expérience réelle.',
    p2: 'Sans jugement, sans coupable', p2s: 'Il ne s’agit pas de pointer quelqu’un, mais d’améliorer.',
    p3: 'Communauté internationale', p3s: 'Le savoir partagé rend nos vols plus sûrs.',
    anonTitulo: 'Anonyme par conception',
    anonTexto: 'Nous ne demandons ni ton nom, ni de données personnelles, ni rien qui puisse t’identifier. '
             + 'La localisation est approximative et les détails sont traités avec soin.',
    anonMas: 'En savoir plus sur ta vie privée',
    aprendeTitulo: 'Ce qu’on apprend',
    aprendeTexto: 'Les signalements permettent d’identifier des tendances, des zones à risque et des '
                + 'situations récurrentes, pour partager ce savoir avec toute la communauté.',
    aprendeVer: 'Voir les tendances et l’analyse',
    reciente: 'Activité récente sur la carte',
    verMapaCompleto: 'Voir la carte complète',
    emergencia: '<b>Important</b><br>SkyReport n’est pas un canal d’urgence. Si tu as besoin d’aide '
              + 'immédiate, contacte les secours locaux.',
    mapaTitulo: 'Carte des événements',
    mapaSub: 'Chaque point est un événement. La chaleur montre où ils s’accumulent.',
    patronesTitulo: 'Tendances',
    patronesSub: 'Les événements isolés racontent des histoires. Ensemble, ils révèlent des tendances.',
    todos: 'Tous',
    subTitulo: 'Signalements anonymes d’événements de parapente',
    pieTexto: 'Signalements anonymes d’événements de parapente',
    pieLema: 'Voler. Apprendre. Revenir.',
    eligeFase: 'Choisis une phase…',
    faltaTitulo: 'Il manque une donnée', faltaTexto: 'Il me faut : ',
    faltaFin: '.<br><br>C’est l’affaire de 30 secondes et ça suffit.',
    graciasTitulo: 'Merci. C’est enregistré.',
    graciasTexto: 'Ce que tu as raconté peut éviter à quelqu’un d’autre de vivre la même chose.',
    graciasViento: 'Et j’ai gardé le vent qu’il faisait ce jour-là : ',
    graciasFin: 'Tu peux en signaler autant que tu veux : <b>les frayeurs comptent aussi</b>.',
    errorTitulo: 'Envoi impossible',
    errorTexto: 'Vérifie ta connexion et réessaie.',
    privTitulo: 'Vie privée',
    privTexto: 'Nous ne demandons ni ton nom, ni ton téléphone, ni ton e-mail.<br><br>La localisation '
             + 'publiée est <b>approximative</b>. Sur un décollage isolé, avec la date et les '
             + 'circonstances, cela pourrait encore être identifiable — c’est pourquoi nous demandons '
             + 'aussi de ne pas écrire de détails qui désignent une personne.'
             + '<br><br>Le <b>jour</b> que tu indiques sert uniquement à calculer le vent de cette '
             + 'journée et <b>n’est pas conservé</b> : il ne reste que le mois et l’année.'
             + '<br><br>Il n’y a ni compte ni utilisateur : personne ne peut voir qui a signalé quoi.'
             + '<br><br>L’anonymat n’est pas une option. C’est la seule chose qui fait que ça marche.',
    sinPuntoTitulo: 'Cet événement n’a pas de point',
    sinPuntoTexto: 'Celui qui l’a écrit n’a pas marqué où c’est arrivé. C’est la seule chose qu’on '
                 + 'demande et elle n’est pas obligatoire, donc il n’y a nulle part où t’emmener.',
    mirandoViento: 'Je regarde le vent qu’il faisait ce jour-là…',
    enviando: 'Envoi…',
    verEnMapa: 'Voir sur la carte',
    pendVerif: 'en attente de vérification',
    entender: 'Compris',
    nada: 'Pas encore d’événement.<br>Sois le premier à en raconter un.',
    masClaro: 'La tendance la plus claire jusqu’ici', en: 'À', hayEventos: 'il y a',
    eventos2: 'événements', yDeEllos: 'et parmi eux', sonDe: 'sont de',
    masDatos: 'Avec plus de données, ceci dira des choses comme « ici, à cette saison, voilà ce qui '
            + 'se passe ». C’est l’objectif.',
    quePasaMas: 'Ce qui arrive le plus', enTotal: 'événements au total',
    faseTitulo: 'À quelle phase du vol', faseSub: 'où ça se complique',
    vientoTitulo: 'Le vent de ces jours-là', vientoSub: 'apportent le vent réel de la météo de ce jour',
    vientoMedio: 'Vent moyen', rachasMedias: 'rafales moyennes',
    tenianRachas: 'avaient des <b>rafales bien au-dessus du vent moyen</b>',
    mayoriaRachado: ' — la plupart étaient par air <b>rafaleux</b>',
    conSostenido: 'avaient un vent soutenu de <b>25 km/h ou plus</b>',
    gravedadTitulo: 'Gravité des événements',
    gravedadSub: 'de la frayeur au pire : à regarder sans morbidité, pour apprendre',
    consecTitulo: 'Conséquences', consecSub: 'le résultat, en chiffres',
    horaTitulo: 'À quel moment de la journée', horaSub: 'moment de la journée',
    dondeTitulo: 'Où', dondeSub: 'par site, sans pointer de lieu exact',
    pocosDatos: 'Pas encore assez de données',
    pocosTexto: 'Les tendances apparaissent à partir de 3 événements. Il y en a ',
    pocosFin: 'C’est pourquoi le plus important maintenant, c’est que les gens signalent : '
            + '<b>chaque frayeur compte</b>. Avec 20 événements, ceci dit déjà des choses utiles.',
  },

  /* ==================== ALEMÁN ==================== */
  de: {
    lema: 'Eine Gemeinschaft<br>für sicherere Flüge',
    navMapa: 'Karte', navReportar: 'Melden', navPatrones: 'Muster',
    heroTitulo: 'Geteilte Sicherheit. Gemeinsames Lernen.',
    heroTexto: 'Hier kannst du Gleitschirm-Ereignisse anonym melden.<br>'
             + 'Wir suchen keinen Schuldigen — wir wollen lernen, damit alle wieder '
             + 'sicher landen.',
    heroCita: '<b>„Jede Erfahrung zählt.</b> Ein sicherer Flug beginnt damit, zu '
            + 'erzählen, was passiert ist.“',
    formTitulo: 'Ein Ereignis melden',
    formAviso: 'Alles ist anonym. Die markierten Felder sind Pflicht.',
    c1t: 'Was ist passiert?', c1a: 'Ordnet die Schwere des Ereignisses ein — vom Beinaheunfall bis zum tödlichen Unfall.',
    c2t: 'Worum handelte es sich?', c2a: 'Die konkrete Situation. Sie ermöglicht später die Muster.',
    c3t: 'Folgen', c3a: 'Das konkrete Ergebnis.',
    c4t: 'Flugphase', c4a: 'Zu welchem Zeitpunkt des Fluges?',
    c5t: 'Wo', c5a: 'Tippe die Gegend auf der Karte an. Der öffentliche Standort wird nur '
                  + 'ungenau dargestellt, um die Möglichkeit zu verringern, den Piloten zu erkennen.',
    c6t: 'Wann', c6a: 'Mit dem Tag ermittle ich den tatsächlichen Wind dort. '
                    + '<b>Der Tag wird nie veröffentlicht</b>: nur Monat und Jahr bleiben erhalten.',
    c7t: 'Tageszeit', c7a: 'Veröffentlicht wird die Tageszeit, nie die genaue Uhrzeit.',
    c8t: 'Wie war die Luft', c8a: 'Was du gespürt hast. Wenn du Datum und Ort angibst, kann SkyReport '
                                + 'den Bericht mit aufgezeichneten Wetterdaten für diese Gegend ergänzen.',
    c9t: 'Deine Flugdatei', c9a: 'Ein IGC identifiziert einen bestimmten Flug. Lies vorher, wie damit umgegangen wird.',
    c10t: 'Erzähl es', c10a: 'Keine Namen. Was jemanden identifiziert, raus; was erklärt, was passiert ist, rein.',
    obligatorio: 'Pflicht', opcional: 'optional',
    otroTitulo: 'Welches? Beschreib es in einer Zeile',
    otroEjemplo: 'Z. B. Hängen im Gurtzeug · jemand in der Luft · Knoten in der Bremse',
    fatalTexto: '<b>Danke, dass du es erzählst.</b> Das ist die Angabe, die am meisten hilft, '
              + 'damit es nicht wieder passiert.<br><br>Erzähl es <b>ohne Namen</b> und ohne '
              + 'Details, die nichts beitragen. Wichtig ist, was passiert ist und unter welchen '
              + 'Bedingungen — nicht, wer.<br><br><b>Tödliche Unfälle werden nicht sofort '
              + 'veröffentlicht:</b> sie bleiben bis zur Prüfung offen, damit ein Fehler oder '
              + 'ein Gerücht nicht zu einer Angabe wird.',
    igcBoton: 'Meine IGC-Datei hochladen',
    igcNota: 'Die Datei wird nach dem Auslesen der nötigen Daten automatisch gelöscht: Flugzeit '
           + 'und maximale Höhe. Sie wird nie gespeichert oder veröffentlicht.',
    relatoEjemplo: 'Schreib hier deinen Bericht (optional)...',
    privacidad: '<b>Was veröffentlicht wird und was nicht.</b><br><b>Veröffentlicht:</b> Monat und '
              + 'Jahr, der ungefähre Ort, die Tageszeit, die Situation und die Folgen.'
              + '<br><b>Nie veröffentlicht:</b> dein Name, der genaue Tag, die genaue Uhrzeit, '
              + 'deine genaue Position oder die IGC-Datei. Die Datei dient nur dem Auslesen der '
              + 'Flugbedingungen und wird sofort gelöscht.',
    enviar: 'Anonymes Ereignis senden',
    evEventos: 'Ereignisse', evEvento: 'Ereignis',
    evSitios: 'Orte', evSitio: 'Ort',
    empezando: 'Die Wissensbasis beginnt gerade.<br>Jede Meldung hilft, sie aufzubauen.',
    evPatrones: 'Muster', evPatron: 'Muster',
    principios: 'Grundsätze',
    p1: 'Sicherheit über alles', p1s: 'Wir lernen aus echter Erfahrung.',
    p2: 'Ohne Urteil, ohne Schuld', p2s: 'Es geht nicht darum, zu zeigen, sondern besser zu werden.',
    p3: 'Weltweite Gemeinschaft', p3s: 'Geteiltes Wissen macht unsere Flüge sicherer.',
    anonTitulo: 'Anonym von Grund auf',
    anonTexto: 'Wir fragen weder nach deinem Namen noch nach persönlichen Daten noch nach '
             + 'irgendetwas, das dich identifizieren könnte. Der Ort ist ungefähr und Details '
             + 'werden sorgfältig behandelt.',
    anonMas: 'Mehr über deinen Datenschutz',
    aprendeTitulo: 'Was wir lernen',
    aprendeTexto: 'Meldungen zeigen Muster, Risikogebiete und wiederkehrende Situationen — '
                + 'damit wir das Gelernte mit der ganzen Gemeinschaft teilen können.',
    aprendeVer: 'Muster und Analyse ansehen',
    reciente: 'Letzte Aktivität auf der Karte',
    verMapaCompleto: 'Ganze Karte ansehen',
    emergencia: '<b>Wichtig</b><br>SkyReport ist kein Notfallkanal. Wenn du sofort Hilfe '
              + 'brauchst, wende dich an die örtlichen Rettungsdienste.',
    mapaTitulo: 'Karte der Ereignisse',
    mapaSub: 'Jeder Punkt ist ein Ereignis. Die Wärme zeigt, wo sie sich häufen.',
    patronesTitulo: 'Muster',
    patronesSub: 'Einzelne Ereignisse erzählen Geschichten. Zusammen zeigen sie Muster.',
    todos: 'Alle',
    subTitulo: 'Anonyme Meldungen von Gleitschirm-Ereignissen',
    pieTexto: 'Anonyme Meldungen von Gleitschirm-Ereignissen',
    pieLema: 'Fliegen. Lernen. Zurückkommen.',
    eligeFase: 'Wähle eine Phase…',
    faltaTitulo: 'Eine Angabe fehlt', faltaTexto: 'Ich brauche: ',
    faltaFin: '.<br><br>Das dauert 30 Sekunden und reicht schon.',
    graciasTitulo: 'Danke. Es ist drin.',
    graciasTexto: 'Was du erzählt hast, kann verhindern, dass es jemand anderem genauso geht.',
    graciasViento: 'Und ich habe den echten Wind jenes Tages gespeichert: ',
    graciasFin: 'Du kannst so viele melden, wie du willst: <b>Schreckmomente zählen auch</b>.',
    errorTitulo: 'Senden fehlgeschlagen',
    errorTexto: 'Prüfe deine Verbindung und versuch es noch einmal.',
    privTitulo: 'Datenschutz',
    privTexto: 'Wir fragen weder nach deinem Namen noch nach Telefon oder E-Mail.<br><br>Der '
             + 'veröffentlichte Ort ist <b>ungefähr</b>. An einem abgelegenen Startplatz könnte '
             + 'er zusammen mit Datum und Umständen noch erkennbar sein — deshalb bitten wir '
             + 'auch darum, keine Details zu schreiben, die auf eine Person hinweisen.'
             + '<br><br>Der <b>Tag</b>, den du angibst, dient nur der Windberechnung und wird '
             + '<b>nicht gespeichert</b>: es bleiben nur Monat und Jahr.'
             + '<br><br>Es gibt keine Konten und keine Nutzer: niemand kann sehen, wer was gemeldet hat.'
             + '<br><br>Anonymität ist keine Option. Sie ist das Einzige, was das hier funktionieren lässt.',
    sinPuntoTitulo: 'Dieses Ereignis hat keinen Punkt',
    sinPuntoTexto: 'Wer es geschrieben hat, hat nicht markiert, wo es passiert ist. Das ist das '
                 + 'Einzige, wonach wir fragen, und es ist nicht Pflicht — also gibt es kein Ziel.',
    mirandoViento: 'Ich schaue den Wind jenes Tages nach…',
    enviando: 'Wird gesendet…',
    verEnMapa: 'Auf der Karte sehen',
    pendVerif: 'Prüfung ausstehend',
    entender: 'Verstanden',
    nada: 'Noch keine Ereignisse.<br>Sei der Erste, der eines erzählt.',
    masClaro: 'Das klarste Muster bisher', en: 'In', hayEventos: 'gibt es',
    eventos2: 'Ereignisse', yDeEllos: 'und davon', sonDe: 'sind',
    masDatos: 'Mit mehr Daten steht hier so etwas wie „hier, in dieser Jahreszeit, passiert das“. '
            + 'Das ist das Ziel.',
    quePasaMas: 'Was am häufigsten passiert', enTotal: 'Ereignisse insgesamt',
    faseTitulo: 'In welcher Flugphase', faseSub: 'wo es kompliziert wird',
    vientoTitulo: 'Der Wind jener Tage', vientoSub: 'bringen den echten Wind des Wetters jenes Tages',
    vientoMedio: 'Mittlerer Wind', rachasMedias: 'mittlere Böen',
    tenianRachas: 'hatten <b>Böen weit über dem mittleren Wind</b>',
    mayoriaRachado: ' — die meisten bei <b>böigem</b> Wind',
    conSostenido: 'hatten beständigen Wind von <b>25 km/h oder mehr</b>',
    gravedadTitulo: 'Schwere der Ereignisse',
    gravedadSub: 'vom Schreck bis zum Schlimmsten: ohne Sensationslust ansehen, um zu lernen',
    consecTitulo: 'Folgen', consecSub: 'das Ergebnis, in Zahlen',
    horaTitulo: 'Zu welcher Tageszeit', horaSub: 'Tageszeit',
    dondeTitulo: 'Wo', dondeSub: 'nach Ort, ohne genaue Punkte zu zeigen',
    pocosDatos: 'Noch nicht genug Daten',
    pocosTexto: 'Muster entstehen ab 3 Ereignissen. Aktuell gibt es ',
    pocosFin: 'Deshalb ist jetzt das Wichtigste, dass Leute melden: <b>jeder Schreck zählt</b>. '
            + 'Mit 20 Ereignissen sagt das hier schon Nützliches.',
  },

  /* ==================== PORTUGUÉS ==================== */
  pt: {
    lema: 'Uma comunidade<br>por voos mais seguros',
    navMapa: 'Mapa', navReportar: 'Relatar', navPatrones: 'Padrões',
    heroTitulo: 'Segurança compartilhada. Aprendizagem coletiva.',
    heroTexto: 'Aqui podes relatar eventos de parapente de forma anónima.<br>'
             + 'Não procuramos culpados — procuramos aprender para que todos voltem a voar.',
    heroCita: '<b>“Cada experiência conta.</b> Um voo mais seguro começa por partilhar '
            + 'o que aconteceu.”',
    formTitulo: 'Relatar um evento',
    formAviso: 'Tudo é anónimo. Os campos marcados são obrigatórios.',
    c1t: 'O que aconteceu?', c1a: 'Classifica o nível do evento, desde um quase-acidente até uma fatalidade.',
    c2t: 'O que foi?', c2a: 'A situação concreta. É o que permite ver padrões depois.',
    c3t: 'Consequências', c3a: 'O resultado concreto.',
    c4t: 'Fase do voo', c4a: 'Em que momento do voo?',
    c5t: 'Onde', c5a: 'Toca na zona do mapa. A localização pública é mostrada de forma '
                    + 'aproximada, para reduzir a possibilidade de identificar o piloto.',
    c6t: 'Quando', c6a: 'Com o dia descubro o vento real que fazia ali. '
                    + '<b>O dia nunca é publicado</b>: só ficam o mês e o ano.',
    c7t: 'Altura do dia', c7a: 'Publica-se a altura do dia, nunca a hora.',
    c8t: 'Como estava o ar', c8a: 'O que sentiste. Se indicares data e localização, o SkyReport pode '
                                + 'complementar o relato com dados meteorológicos registados dessa zona.',
    c9t: 'O teu ficheiro de voo', c9a: 'Um IGC identifica um voo concreto. Lê como é tratado antes de o enviar.',
    c10t: 'Conta-o', c10a: 'Sem nomes. O que identifica alguém, fora; o que explica o que aconteceu, dentro.',
    obligatorio: 'obrigatório', opcional: 'opcional',
    otroTitulo: 'Qual? Descreve-o numa linha',
    otroEjemplo: 'Ex: prender no arnês · alguém no ar · nó no travão',
    fatalTexto: '<b>Obrigado por contá-lo.</b> É o dado que mais ajuda a evitar que volte a acontecer.'
              + '<br><br>Conta-o <b>sem nomes</b> e sem detalhes que não acrescentem nada. O que '
              + 'importa é o que aconteceu e em que condições, não quem.<br><br>'
              + '<b>As fatalidades não são publicadas de imediato:</b> ficam pendentes de '
              + 'verificação, para que um erro ou um rumor não se torne num dado.',
    igcBoton: 'Enviar o meu ficheiro IGC',
    igcNota: 'O ficheiro é eliminado automaticamente depois de extrair os dados necessários: '
           + 'a hora do voo e a altitude máxima. Nunca é guardado nem publicado.',
    relatoEjemplo: 'Escreve aqui o teu relato (opcional)...',
    privacidad: '<b>O que se publica e o que não.</b><br><b>Publica-se:</b> o mês e o ano, a '
              + 'localização aproximada, a altura do dia, a situação e as consequências.'
              + '<br><b>Nunca se publica:</b> o teu nome, o dia exato, a hora exata, a tua posição '
              + 'precisa, nem o ficheiro IGC. O ficheiro serve só para ler as condições do voo e é '
              + 'eliminado de imediato.',
    enviar: 'Enviar evento anónimo',
    evEventos: 'eventos', evEvento: 'evento',
    evSitios: 'locais', evSitio: 'local',
    empezando: 'A base de conhecimento está a começar.<br>Cada relato ajuda a construí-la.',
    evPatrones: 'padrões', evPatron: 'padrão',
    principios: 'Princípios',
    p1: 'Segurança acima de tudo', p1s: 'Aprendemos com a experiência real.',
    p2: 'Sem julgamentos, sem culpados', p2s: 'Não se trata de apontar, mas de melhorar.',
    p3: 'Comunidade global', p3s: 'O conhecimento partilhado torna os nossos voos mais seguros.',
    anonTitulo: 'Anónimo por conceção',
    anonTexto: 'Não pedimos o teu nome, nem dados pessoais, nem nada que te possa identificar. '
             + 'A localização é aproximada e os detalhes são tratados com cuidado.',
    anonMas: 'Saber mais sobre a tua privacidade',
    aprendeTitulo: 'O que aprendemos',
    aprendeTexto: 'Os relatos permitem identificar padrões, zonas de risco e situações recorrentes, '
                + 'para partilhar o que aprendemos com toda a comunidade.',
    aprendeVer: 'Ver padrões e análise',
    reciente: 'Atividade recente no mapa',
    verMapaCompleto: 'Ver mapa completo',
    emergencia: '<b>Importante</b><br>O SkyReport não é um canal de emergência. Se precisares de '
              + 'ajuda imediata, contacta os serviços de socorro locais.',
    mapaTitulo: 'Mapa de eventos',
    mapaSub: 'Cada ponto é um evento. O calor mostra onde se acumulam.',
    patronesTitulo: 'Padrões',
    patronesSub: 'Os eventos isolados contam histórias. Juntos revelam padrões.',
    todos: 'Todos',
    subTitulo: 'Relatos anónimos de eventos de parapente',
    pieTexto: 'Relatos anónimos de eventos de parapente',
    pieLema: 'Volar. Aprender. Voltar.',
    eligeFase: 'Escolhe uma fase…',
    faltaTitulo: 'Falta um dado', faltaTexto: 'Preciso de: ',
    faltaFin: '.<br><br>São 30 segundos e com isso já serve.',
    graciasTitulo: 'Obrigado. Já está dentro.',
    graciasTexto: 'O que contaste pode evitar que outro passe pelo mesmo.',
    graciasViento: 'E guardei o vento real desse dia: ',
    graciasFin: 'Podes relatar todos os que quiseres: <b>os sustos também contam</b>.',
    errorTitulo: 'Não foi possível enviar',
    errorTexto: 'Verifica a tua ligação e tenta outra vez.',
    privTitulo: 'Privacidade',
    privTexto: 'Não pedimos o teu nome, nem o telemóvel, nem o e-mail.<br><br>A localização '
             + 'publicada é <b>aproximada</b>. Num descolamento remoto, com a data e as '
             + 'circunstâncias, ainda poderia ser identificável — por isso pedimos também que '
             + 'não escrevas detalhes que apontem para uma pessoa.'
             + '<br><br>O <b>dia</b> que indicares serve só para calcular o vento dessa jornada e '
             + '<b>não é guardado</b>: fica apenas o mês e o ano.'
             + '<br><br>Não há contas nem utilizadores: ninguém pode ver quem relatou o quê.'
             + '<br><br>O anonimato não é um extra. É a única coisa que faz isto funcionar.',
    sinPuntoTitulo: 'Esse evento não tem ponto',
    sinPuntoTexto: 'Quem o escreveu não marcou onde aconteceu. É a única coisa que pedimos e não é '
                 + 'obrigatória, por isso não há sítio para onde te levar.',
    mirandoViento: 'A ver o vento que fazia nesse dia…',
    enviando: 'A enviar…',
    verEnMapa: 'Ver no mapa',
    pendVerif: 'pendente de verificação',
    entender: 'Entendido',
    nada: 'Ainda não há eventos.<br>Sê o primeiro a contar um.',
    masClaro: 'O padrão mais claro até agora', en: 'Em', hayEventos: 'há',
    eventos2: 'eventos', yDeEllos: 'e desses', sonDe: 'são de',
    masDatos: 'Com mais dados isto dirá coisas como «aqui, nesta época, acontece isto». É o objetivo.',
    quePasaMas: 'O que acontece mais', enTotal: 'eventos no total',
    faseTitulo: 'Em que fase do voo', faseSub: 'onde se complica',
    vientoTitulo: 'O vento desses dias', vientoSub: 'trazem o vento real do clima desse dia',
    vientoMedio: 'Vento médio', rachasMedias: 'rajadas médias',
    tenianRachas: 'tinham <b>rajadas muito acima do vento médio</b>',
    mayoriaRachado: ' — a maioria foi com ar <b>rajado</b>',
    conSostenido: 'foram com vento sustentado de <b>25 km/h ou mais</b>',
    gravedadTitulo: 'Gravidade dos eventos',
    gravedadSub: 'do susto ao pior: olhar sem morbidez, para aprender',
    consecTitulo: 'Consequências', consecSub: 'o resultado, em números',
    horaTitulo: 'A que hora do dia', horaSub: 'altura do dia',
    dondeTitulo: 'Onde', dondeSub: 'por local, sem apontar pontos exatos',
    pocosDatos: 'Ainda não há dados suficientes',
    pocosTexto: 'Os padrões aparecem a partir de 3 eventos. Neste momento há ',
    pocosFin: 'Por isso o importante agora é que as pessoas relatem: <b>cada susto conta</b>. '
            + 'Com 20 eventos isto já diz coisas úteis.',
  },
};

let idioma = 'es';
const IDIOMAS_NOMBRE = { es:'Español', en:'English', fr:'Français', de:'Deutsch', pt:'Português' };"""

rep("""};

let idioma = 'es';""", NUEVOS)

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  cambios:', toc)
print('  archivo:', len(s), 'bytes')
