"""
Generador de miniaturas para YouTube/LinkedIn/Instagram — mundo-multimedia
Usa Pillow (local, gratis). Genera miniaturas profesionales automáticamente.

Uso:
  python generador-miniaturas.py --imagen foto.jpg --titulo "5 Errores con IA" --plataforma youtube
"""
import argparse
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

TAMANIOS = {
    "youtube":   (1280, 720),
    "instagram": (1080, 1080),
    "linkedin":  (1200, 627),
    "reels":     (1080, 1920),
}

COLORES = {
    "naranja": "#FF6B35",
    "azul":    "#1E3A8A",
    "verde":   "#16A34A",
    "rojo":    "#DC2626",
    "morado":  "#7C3AED",
}

def cargar_fuente(tamanio):
    intentos = ["arialbd.ttf", "arial.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans.ttf"]
    for nombre in intentos:
        try:
            return ImageFont.truetype(nombre, tamanio)
        except:
            continue
    return ImageFont.load_default()

def generar_miniatura(imagen_path, titulo, subtitulo=None, plataforma="youtube",
                      color_acento="#FF6B35", salida=None):
    w, h = TAMANIOS.get(plataforma, (1280, 720))

    img = Image.open(imagen_path).convert("RGB")
    img = img.resize((w, h), Image.LANCZOS)

    oscurecer = Image.new("RGBA", (w, h), (0, 0, 0, 120))
    img = Image.alpha_composite(img.convert("RGBA"), oscurecer).convert("RGB")

    draw = ImageDraw.Draw(img)

    barra_h = h // 3
    barra = Image.new("RGBA", (w, barra_h), (*bytes.fromhex(color_acento.lstrip("#")), 200))
    img.paste(Image.alpha_composite(Image.new("RGBA", (w, barra_h), (0,0,0,0)), barra).convert("RGB"),
              (0, h - barra_h))

    font_titulo = cargar_fuente(int(h * 0.09))
    font_sub    = cargar_fuente(int(h * 0.05))

    lineas = []
    palabras = titulo.split()
    linea_actual = ""
    max_chars = 22
    for palabra in palabras:
        if len(linea_actual) + len(palabra) + 1 <= max_chars:
            linea_actual += (" " if linea_actual else "") + palabra
        else:
            if linea_actual:
                lineas.append(linea_actual)
            linea_actual = palabra
    if linea_actual:
        lineas.append(linea_actual)

    y_texto = h - barra_h + 20
    for linea in lineas:
        draw.text((30, y_texto), linea, font=font_titulo, fill="white",
                  stroke_width=2, stroke_fill="black")
        bbox = draw.textbbox((0, 0), linea, font=font_titulo)
        y_texto += bbox[3] - bbox[1] + 5

    if subtitulo:
        draw.text((30, y_texto + 5), subtitulo, font=font_sub,
                  fill=(220, 220, 220), stroke_width=1, stroke_fill="black")

    if not salida:
        nombre = os.path.splitext(os.path.basename(imagen_path))[0]
        salida = f"{nombre}_miniatura_{plataforma}.jpg"

    img.save(salida, "JPEG", quality=92)
    size_kb = os.path.getsize(salida) // 1024
    print(f"Miniatura generada: {salida} ({size_kb} KB, {w}x{h})")
    return salida

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador de miniaturas profesionales")
    parser.add_argument("--imagen", required=True, help="Foto de fondo")
    parser.add_argument("--titulo", required=True, help="Título principal")
    parser.add_argument("--subtitulo", help="Texto secundario (opcional)")
    parser.add_argument("--plataforma", default="youtube", choices=list(TAMANIOS.keys()))
    parser.add_argument("--color", default="naranja", choices=list(COLORES.keys()))
    parser.add_argument("--salida", help="Nombre archivo salida")
    args = parser.parse_args()

    generar_miniatura(
        args.imagen, args.titulo, args.subtitulo,
        args.plataforma, COLORES[args.color], args.salida
    )
