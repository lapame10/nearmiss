#!/usr/bin/env python3
"""El logo, SOLO la gota, sin el fondo blanco (version corregida).

Pam: 'pero que quede solo la gota, sin el fondo blanco'.

El logo tiene dos zonas blancas:
  - la de FUERA de la gota  -> esa hay que hacerla TRANSPARENTE
  - la de DENTRO del pin    -> esa es parte del dibujo y se queda

La forma de separarlas: rellenar (flood fill) desde las 4 esquinas. Ese relleno
solo alcanza el blanco CONECTADO al exterior; el de dentro del pin queda
aislado por el contorno azul y no se toca.
"""
import os
from PIL import Image, ImageDraw

ORIGEN = '/Users/lapame10/.hermes/cache/images/img_ab205535963b.jpg'
DESTINO = '/Users/lapame10/.hermes/workspace/nearmiss'
MAGENTA = (255, 0, 255)

im = Image.open(ORIGEN).convert('RGB')
print('  original:', im.size)

# 1) relleno desde las cuatro esquinas con un color que no existe en el dibujo
marca = im.copy()
an, al = marca.size
esquinas = [(0, 0), (an - 1, 0), (0, al - 1), (an - 1, al - 1), (an // 2, 0), (an // 2, al - 1)]
for e in esquinas:
    if marca.getpixel(e) != MAGENTA:
        ImageDraw.floodfill(marca, e, MAGENTA, thresh=42)

# 2) todo lo que quedo magenta es fondo -> transparente
rgba = im.convert('RGBA')
px = rgba.load()
fondo = 0
for y in range(al):
    for x in range(an):
        if marca.getpixel((x, y)) == MAGENTA:
            px[x, y] = (255, 255, 255, 0)
            fondo += 1
print('  pixeles de fondo quitados: %.1f%%' % (100.0 * fondo / (an * al)))

# 3) recorto a lo que queda (la gota)
caja = rgba.split()[3].getbbox()
print('  recuadro de la gota:', caja)
log = rgba.crop(caja)

# 4) lo cuadro con un pelin de aire
lado = max(log.size)
aire = int(lado * 0.05)
cuadro = lado + aire * 2
lienzo = Image.new('RGBA', (cuadro, cuadro), (255, 255, 255, 0))
lienzo.paste(log, ((cuadro - log.size[0]) // 2, (cuadro - log.size[1]) // 2), log)

# 5) los tamanos
for nombre, n in [('logo.png', 256), ('icono-192.png', 192), ('icono-512.png', 512)]:
    r = lienzo.resize((n, n), Image.LANCZOS)
    r.save(os.path.join(DESTINO, nombre), 'PNG', optimize=True)
    print('  %-16s %d x %d  (%d KB)' % (nombre, n, n,
          os.path.getsize(os.path.join(DESTINO, nombre)) // 1024))

# 6) y una muestra sobre los dos fondos, para verlo
fondo = Image.new('RGB', (520, 100), (22, 50, 59))
mini = lienzo.resize((62, 62), Image.LANCZOS)
# sobre azul marino (la cabecera)
fondo.paste(mini, (18, 19), mini)
# y sobre blanco (el resto de la app)
blanco = Image.new('RGB', (110, 100), (255, 255, 255))
blanco.paste(mini, (24, 19), mini)
fondo.paste(blanco, (250, 0))
d = ImageDraw.Draw(fondo)
try:
    from PIL import ImageFont
    f = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 28)
except Exception:
    f = ImageFont.load_default()
d.text((96, 34), 'SkyReport', font=f, fill=(255, 255, 255))
fondo.save('/tmp/logo_sin_fondo.png')
print()
print('  /tmp/logo_sin_fondo.png  (sobre azul marino y sobre blanco)')
