#!/usr/bin/env python3
"""Las claves del flujo nuevo, en los cinco idiomas.

Traducciones naturales, no literales. 'Como funciona SkyReport' no es
'How SkyReport works' palabra por palabra en frances: ahi suena mejor
'Comment fonctionne SkyReport'. Y 'Continuar sin IGC' en aleman es
'Ohne IGC fortfahren', no 'Weiter ohne IGC', que se entiende pero suena a
traduccion de maquina.
"""
BASE = '/Users/lapame10/.hermes/workspace/nearmiss/srs/'
s = open(BASE + 'i18n.js', encoding='utf-8').read()

# clave: (es, fr, de, pt, en)
T = [
 ('report.step.event', 'Evento', 'Événement', 'Ereignis', 'Evento', 'Event'),

 # --- el paso del IGC, al principio ---
 ('igc.stepTitle', '¿Tienes el IGC de este vuelo?',
  'As-tu le tracé IGC de ce vol ?',
  'Hast du das IGC dieses Flugs?',
  'Tens o IGC deste voo?',
  'Do you have the IGC for this flight?'),
 ('igc.stepHelp', 'Súbelo y SkyReport completará automáticamente los datos que pueda obtener del vuelo.',
  'Ajoute-le et SkyReport remplira automatiquement les données qu’il peut tirer du vol.',
  'Lade es hoch und SkyReport füllt automatisch aus, was sich aus dem Flug ablesen lässt.',
  'Carrega-o e o SkyReport preencherá automaticamente os dados que conseguir tirar do voo.',
  'Upload it and SkyReport will fill in whatever it can read from the flight.'),
 ('igc.upload', 'Subir IGC', 'Ajouter un IGC', 'IGC hochladen', 'Carregar IGC', 'Upload IGC'),
 ('igc.continueWithout', 'Continuar sin IGC', 'Continuer sans IGC', 'Ohne IGC fortfahren',
  'Continuar sem IGC', 'Continue without IGC'),
 ('igc.withoutHint', 'Puedes rellenarlo a mano. El IGC nunca es obligatorio.',
  'Tu peux le remplir à la main. Le IGC n’est jamais obligatoire.',
  'Du kannst es von Hand ausfüllen. Das IGC ist nie Pflicht.',
  'Podes preenchê-lo à mão. O IGC nunca é obrigatório.',
  'You can fill it in by hand. The IGC is never required.'),

 # --- el resumen de lo detectado ---
 ('igc.detected', 'Vuelo detectado', 'Vol détecté', 'Flug erkannt', 'Voo detetado', 'Flight detected'),
 ('igc.duration', 'Duración', 'Durée', 'Dauer', 'Duração', 'Duration'),
 ('igc.points', 'Puntos', 'Points', 'Punkte', 'Pontos', 'Points'),
 ('igc.altMax', 'Altitud máxima', 'Altitude maximale', 'Höchste Höhe', 'Altitude máxima', 'Max altitude'),
 ('igc.noTrackStoredShort', 'Track no guardado', 'Tracé non enregistré', 'Track nicht gespeichert',
  'Percurso não guardado', 'Track not stored'),

 # --- marcar el momento del evento ---
 ('igc.markTitle', 'Marca el momento del evento',
  'Marque le moment de l’événement',
  'Markiere den Moment des Ereignisses',
  'Marca o momento do evento',
  'Mark when the event happened'),
 ('igc.markHelp', 'SkyReport propone dónde mirar. Tú confirmas dónde fue.',
  'SkyReport propose où regarder. Toi, tu confirmes où c’était.',
  'SkyReport schlägt vor, wo man hinschaut. Du bestätigst, wo es war.',
  'O SkyReport sugere onde olhar. Tu confirmas onde foi.',
  'SkyReport suggests where to look. You confirm where it was.'),
 ('igc.whatHappened', 'Lo que el archivo no puede saber',
  'Ce que le fichier ne peut pas savoir',
  'Was die Datei nicht wissen kann',
  'O que o ficheiro não pode saber',
  'What the file cannot know'),
 ('igc.whatHappenedHelp', 'El track sabe dónde y cuándo. Esto solo lo sabes tú.',
  'Le tracé sait où et quand. Ça, il n’y a que toi qui le sais.',
  'Der Track weiß wo und wann. Das hier weißt nur du.',
  'O percurso sabe onde e quando. Isto só tu sabes.',
  'The track knows where and when. This part only you know.'),

 # --- los datos del punto ---
 ('igc.altGps', 'Altitud GPS', 'Altitude GPS', 'GPS-Höhe', 'Altitude GPS', 'GPS altitude'),
 ('igc.altBaro', 'Altitud barométrica', 'Altitude barométrique', 'Barometrische Höhe',
  'Altitude barométrica', 'Barometric altitude'),
 ('igc.speed', 'Velocidad sobre el suelo', 'Vitesse sol', 'Geschwindigkeit über Grund',
  'Velocidade em relação ao solo', 'Ground speed'),
 ('igc.vertical', 'Velocidad vertical', 'Vitesse verticale', 'Vertikalgeschwindigkeit',
  'Velocidade vertical', 'Vertical speed'),
 ('igc.heading', 'Rumbo', 'Cap', 'Kurs', 'Rumo', 'Heading'),

 # --- de donde sale cada dato ---
 ('igc.fromFile', 'IGC', 'IGC', 'IGC', 'IGC', 'IGC'),
 ('igc.estimated', 'Estimado', 'Estimé', 'Geschätzt', 'Estimado', 'Estimated'),
 ('igc.fromPilot', 'Tú', 'Toi', 'Du', 'Tu', 'You'),

 # --- el acceso desde inicio ---
 ('home.howItWorks', 'Cómo funciona SkyReport', 'Comment fonctionne SkyReport',
  'Wie SkyReport funktioniert', 'Como funciona o SkyReport', 'How SkyReport works'),
]

toc = 0
for claves in T:
    k = claves[0]
    for idioma, valor in [('EN', claves[5]), ('ES', claves[1]), ('FR', claves[2]),
                          ('DE', claves[3]), ('PT', claves[4])]:
        i = s.find('const %s = {' % idioma); j = s.find('\n};', i)
        if ("'%s':" % k) in s[i:j]:
            continue
        comilla = '"' if "'" in valor else "'"
        s = s[:j] + "\n  '%s': %s%s%s," % (k, comilla, valor, comilla) + s[j:]
        toc += 1
open(BASE + 'i18n.js', 'w', encoding='utf-8').write(s)
print('  entradas nuevas: %d' % toc)

# ---------- y comprobar que 'common.site' existe ----------
import re
i = s.find('const ES = {'); j = s.find('\n};', i)
print('  common.site existe: %s' % ('si' if "'common.site'" in s[i:j] else 'NO — hay que anadirla'))
