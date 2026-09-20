#!/usr/bin/env python3
"""Prepara el logo de Pam para SkyReport.

El logo que mando Pam (un pin de mapa con un parapente dentro, en azules) es
muchisimo mejor que el triangulito que habia. Le preparo:
- logo.png: para la cabecera (fondo blanco, recortado, cuadrado)
- icono-192.png y icono-512.png: para el manifest y el favicon
"""
import os
from PIL import Image

ORIGEN = '/Users/lapame10/.hermes/cache/images/img_ab205535963b.jpg'
DESTINO = '/Users/lapame10/.hermes/workspace/nearmiss'

im = Image.open(ORIGEN).convert('RGB')
print('  original:', im.size)

# --- 1) recorto el blanco de alrededor ---
# busco el recuadro de todo lo que no sea casi blanco
gris = im.convert('L')
mascara = gris.point(lambda v: 255 if v < 244 else 0)
caja = mascara.getbbox()
print('  recuadro del dibujo:', caja)
log = im.crop(caja)

# --- 2) lo cuadro con un poco de aire ---
lado = max(log.size)
aire = int(lado * 0.06)
cuadro = lado + aire * 2
lienzo = Image.new('RGB', (cuadro, cuadro), (255, 255, 255))
lienzo.paste(log, ((cuadro - log.size[0]) // 2, (cuadro - log.size[1]) // 2))
print('  cuadrado:', lienzo.size)

# --- 3) los tres tamanos ---
tamanos = [('logo.png', 256), ('icono-192.png', 192), ('icono-512.png', 512)]
for nombre, n in tamanos:
    r = lienzo.resize((n, n), Image.LANCZOS)
    r.save(os.path.join(DESTINO, nombre), 'PNG', optimize=True)
    print('  %-16s %d x %d  (%d KB)' % (nombre, n, n, os.path.getsize(os.path.join(DESTINO, nombre)) // 1024))

# --- 4) y una version para ver como queda en la cabecera azul ---
# sobre azul marino, para comprobar que se ve
fondo = Image.new('RGB', (420, 90), (22, 50, 59))
mini = lienzo.resize((54, 54), Image.LANCZOS)
# le pongo las esquinas redondeadas, como en la web
from PIL import ImageDraw
redondo = Image.new('RGBA', (54, 54), (0, 0, 0, 0))
d = ImageDraw.Draw(redondo)
d.rounded_rectangle([0, 0, 53, 53], radius=13, fill=(255, 255, 255, 255))
redondo.paste(mini, (0, 0), redondo.split()[3])
fondo.paste(redondo.convert('RGB'), (20, 18))
d2 = ImageDraw.Draw(fondo)
try:
    from PIL import ImageFont
    f = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 27)
except Exception:
    f = ImageFont.load_default()
d2.text((88, 30), 'SkyReport', font=f, fill=(255, 255, 255))
fondo.save('/tmp/logo_cabecera.png')
print()
print('  /tmp/logo_cabecera.png  (como se vera en la cabecera azul)')
