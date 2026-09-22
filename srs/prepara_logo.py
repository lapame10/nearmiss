#!/usr/bin/env python3
"""El logo nuevo de SkyReport: prepararlo bien.

Lo que manda Pam es una captura de 107x118 con el fondo beige del chat
(245,244,240) pegado alrededor del hexagono. Si se usa tal cual como icono,
sale un cuadrado beige con un hexagono pequeno dentro y un borde que no pega
con nada. Y en el iPhone, iOS redondea las esquinas: si el dibujo llega al
borde, se come parte del logo.

Lo que se hace aqui:

  1. recortar el fondo: me quedo con los pixeles que NO son beige
  2. recortar al contenido y dejarlo CUADRADO, centrado
  3. dejar un margen del 8%, que es lo que iOS necesita para redondear sin
     comerse el dibujo
  4. sacar los tamaños que hacen falta: 512, 192, 180 (apple-touch) y 32
     (favicon), y un maskable con fondo azul lleno

Sobre el maskable: Android recorta el icono con la forma que le da la gana
(circulo, gota, cuadrado redondeado). Para que no corte el hexagono, el dibujo
tiene que caber en el 80% central y el fondo tiene que llegar hasta los bordes.
Por eso el maskable lleva fondo azul lleno y el hexagono mas pequeño dentro.
"""
from PIL import Image
import os

ORIGEN = '/Users/lapame10/.hermes/cache/images/img_a703df16d0d0.jpg'
DESTINO = '/Users/lapame10/.hermes/workspace/nearmiss/'
AZUL = (43, 71, 118)          # el azul del hexagono, sacado de la propia imagen

im = Image.open(ORIGEN).convert('RGB')
ancho, alto = im.size
print('  origen: %dx%d' % (ancho, alto))

# ---------- 1) recorto el fondo beige ----------
# el fondo del chat es un beige muy claro y plano. Todo lo que se aleje de ese
# color es dibujo.
fondo = im.getpixel((1, 1))
print('  fondo a quitar: %s' % (fondo,))
px = im.load()
minx, miny, maxx, maxy = ancho, alto, 0, 0
for y in range(alto):
    for x in range(ancho):
        r, g, b = px[x, y]
        # distancia al color de fondo; el antialias deja pixeles intermedios,
        # asi que soy generoso y solo descarto lo que esta claramente cerca
        if abs(r - fondo[0]) + abs(g - fondo[1]) + abs(b - fondo[2]) > 40:
            if x < minx: minx = x
            if x > maxx: maxx = x
            if y < miny: miny = y
            if y > maxy: maxy = y

print('  dibujo encontrado: x %d..%d  y %d..%d' % (minx, maxx, miny, maxy))
if maxx <= minx or maxy <= miny:
    raise SystemExit('  ✗ no encontre el dibujo')

recorte = im.crop((minx, miny, maxx + 1, maxy + 1))
lado = max(recorte.size)
print('  recorte: %dx%d' % recorte.size)

# ---------- 2) cuadrado, centrado, con margen ----------
MARGEN = 0.08                       # 8% para que iOS pueda redondear
lado_final = int(lado / (1 - MARGEN * 2))
lienzo = Image.new('RGBA', (lado_final, lado_final), (0, 0, 0, 0))

# ---------- 3) el fondo beige, transparente ----------
rgba = recorte.convert('RGBA')
datos = rgba.load()
for y in range(rgba.size[1]):
    for x in range(rgba.size[0]):
        r, g, b, a = datos[x, y]
        if abs(r - fondo[0]) + abs(g - fondo[1]) + abs(b - fondo[2]) < 40:
            datos[x, y] = (r, g, b, 0)

lienzo.paste(rgba, ((lado_final - recorte.size[0]) // 2,
                    (lado_final - recorte.size[1]) // 2), rgba)

# ---------- 4) los tamaños ----------
TAMANOS = {
    'icono-512.png': 512,
    'icono-192.png': 192,
    'apple-touch-icon.png': 180,
    'favicon-32.png': 32,
}
for nombre, tam in TAMANOS.items():
    # para los pequeños, un poco mas de margen se ve mejor
    m = 0.14 if tam <= 192 else 0.08
    n = int(lado / (1 - m * 2))
    base = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    base.paste(rgba, ((n - recorte.size[0]) // 2, (n - recorte.size[1]) // 2), rgba)
    base.resize((tam, tam), Image.LANCZOS).save(DESTINO + nombre, 'PNG')
    print('  %-22s %dx%d' % (nombre, tam, tam))

# ---------- 5) el maskable, con fondo lleno ----------
for nombre, tam in [('icono-maskable-512.png', 512), ('icono-maskable-192.png', 192)]:
    base = Image.new('RGB', (tam, tam), AZUL)
    # el dibujo cabe en el 72% central, que es lo que Android garantiza que
    # no recorta
    dentro = int(tam * 0.72)
    # el hexagono en blanco sobre el azul: invierto los colores del dibujo
    d = rgba.resize((dentro, dentro), Image.LANCZOS)
    px2 = d.load()
    for y in range(d.size[1]):
        for x in range(d.size[0]):
            r, g, b, a = px2[x, y]
            if a > 40:
                # el trazo y el punto son blancos en el original; el hexagono
                # azul pasa a ser del mismo azul que el fondo
                claro = (r > 170 and g > 170 and b > 170)
                px2[x, y] = (255, 255, 255, 255) if claro else AZUL + (255,)
    base.paste(d, ((tam - dentro) // 2, (tam - dentro) // 2), d)
    base.save(DESTINO + nombre, 'PNG')
    print('  %-22s %dx%d' % (nombre, tam, tam))

# ---------- 6) y una copia en grande para la cabecera ----------
rgba.resize((128, 128), Image.LANCZOS).save(DESTINO + 'logo.png', 'PNG')
print('  %-22s %dx%d' % ('logo.png', 128, 128))
print('\n  ✓ listo')
