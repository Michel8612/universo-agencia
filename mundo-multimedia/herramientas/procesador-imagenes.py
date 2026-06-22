"""
Procesador de imágenes — mundo-multimedia
Uso: python procesador-imagenes.py --input foto.jpg --modo miniatura --plataforma youtube
"""
import argparse
import os
from PIL import Image, ImageDraw, ImageFont

TAMANIOS = {
    "youtube":    (1280, 720),
    "instagram":  (1080, 1080),
    "reels":      (1080, 1920),
    "linkedin":   (1200, 627),
    "twitter":    (1200, 675),
    "facebook":   (1200, 630),
}

def redimensionar(img, plataforma):
    w, h = TAMANIOS.get(plataforma, (1080, 1080))
    return img.resize((w, h), Image.LANCZOS)

def anadir_marca_agua(img, texto="Universo IA", opacidad=80):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), texto, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = img.width - tw - 20
    y = img.height - th - 20
    draw.text((x, y), texto, font=font, fill=(255, 255, 255, opacidad))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

def comprimir(img, calidad=85):
    return img  # se aplica al guardar con quality=calidad

def procesar(input_path, modo, plataforma, salida=None, marca=None):
    img = Image.open(input_path)
    nombre_base = os.path.splitext(os.path.basename(input_path))[0]

    if modo == "miniatura" or modo == "redimensionar":
        img = redimensionar(img, plataforma)
        print(f"  Redimensionado a {TAMANIOS.get(plataforma)} para {plataforma}")

    if marca:
        img = anadir_marca_agua(img, marca)
        print(f"  Marca de agua añadida: {marca}")

    if not salida:
        salida = f"{nombre_base}_{plataforma}.jpg"

    img.save(salida, "JPEG", quality=85, optimize=True)
    size_kb = os.path.getsize(salida) // 1024
    print(f"  Guardado: {salida} ({size_kb} KB)")
    return salida

def batch(carpeta, plataforma, marca=None):
    extensiones = (".jpg", ".jpeg", ".png", ".webp")
    archivos = [f for f in os.listdir(carpeta) if f.lower().endswith(extensiones)]
    print(f"\nProcesando {len(archivos)} imágenes para {plataforma}...\n")
    salidas = []
    for archivo in archivos:
        ruta = os.path.join(carpeta, archivo)
        salida = os.path.join(carpeta, f"editado_{archivo}")
        print(f"→ {archivo}")
        salidas.append(procesar(ruta, "redimensionar", plataforma, salida, marca))
    print(f"\nListo. {len(salidas)} imágenes procesadas.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Procesador de imágenes para redes sociales")
    parser.add_argument("--input", help="Imagen o carpeta de imágenes")
    parser.add_argument("--modo", default="miniatura", choices=["miniatura", "redimensionar", "marca"])
    parser.add_argument("--plataforma", default="instagram", choices=list(TAMANIOS.keys()))
    parser.add_argument("--salida", help="Nombre del archivo de salida")
    parser.add_argument("--marca", help="Texto de marca de agua")
    parser.add_argument("--batch", action="store_true", help="Procesar carpeta entera")
    args = parser.parse_args()

    if not args.input:
        print("Uso: python procesador-imagenes.py --input foto.jpg --plataforma youtube")
        print(f"Plataformas: {', '.join(TAMANIOS.keys())}")
    elif args.batch or os.path.isdir(args.input):
        batch(args.input, args.plataforma, args.marca)
    else:
        procesar(args.input, args.modo, args.plataforma, args.salida, args.marca)
