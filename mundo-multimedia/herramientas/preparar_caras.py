"""
UNIVERSO — Preparador de Caras de Referencia
Extrae caras individuales de fotos grupales y las guarda como imágenes limpias.
"""

import cv2, sys, os
import numpy as np
from pathlib import Path

WORK_DIR = Path(r"D:\Proyectos claude\mundo-multimedia\proyectos\face-swap")


def detectar_caras(img_path):
    import insightface
    from insightface.app import FaceAnalysis
    app = FaceAnalysis(name="buffalo_l", root=str(Path.home() / ".insightface"))
    app.prepare(ctx_id=0, det_size=(640, 640))

    img = cv2.imread(img_path)
    assert img is not None, f"No se puede leer: {img_path}"
    faces = app.get(img)
    return img, faces


def mostrar_caras(img_path):
    """Muestra todas las caras detectadas con su índice y posición."""
    img, faces = detectar_caras(img_path)
    print(f"\nFoto: {img_path}")
    print(f"Dimensiones: {img.shape[1]}x{img.shape[0]}")
    print(f"Caras detectadas: {len(faces)}")
    for i, f in enumerate(sorted(faces, key=lambda x: (x.bbox[0]+x.bbox[2])/2)):
        cx = int((f.bbox[0]+f.bbox[2])/2)
        cy = int((f.bbox[1]+f.bbox[3])/2)
        w  = int(f.bbox[2]-f.bbox[0])
        h  = int(f.bbox[3]-f.bbox[1])
        pos = "IZQUIERDA" if cx < img.shape[1]/2 else "DERECHA"
        print(f"  Cara {i}: centro ({cx},{cy})  tamaño {w}x{h}  [{pos}]  score={f.det_score:.2f}")
    return img, faces


def extraer_cara(img_path, cara_index_por_x, salida_path, padding=0.3):
    """
    Extrae la cara en posición cara_index_por_x (0=más izquierda, 1=siguiente...).
    padding=0.3 añade margen alrededor de la cara para mejor resultado.
    """
    img, faces = detectar_caras(img_path)
    faces_sorted = sorted(faces, key=lambda x: (x.bbox[0]+x.bbox[2])/2)

    if cara_index_por_x >= len(faces_sorted):
        print(f"ERROR: Solo hay {len(faces_sorted)} caras. Pide índice 0..{len(faces_sorted)-1}")
        return

    face = faces_sorted[cara_index_por_x]
    x1, y1, x2, y2 = [int(v) for v in face.bbox]

    # Añadir margen
    pw = int((x2-x1) * padding)
    ph = int((y2-y1) * padding)
    x1m = max(0, x1-pw)
    y1m = max(0, y1-ph)
    x2m = min(img.shape[1], x2+pw)
    y2m = min(img.shape[0], y2+ph)

    crop = img[y1m:y2m, x1m:x2m]
    cv2.imwrite(salida_path, crop)
    print(f"[OK] Cara {cara_index_por_x} guardada en: {salida_path}")
    return salida_path


if __name__ == "__main__":
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    DOWNLOADS = r"C:\Users\Romer\Downloads"

    foto1 = os.path.join(DOWNLOADS, "WhatsApp Image 2026-06-20 at 3.52.11 PM.jpeg")  # anciano gafas azul
    foto2 = os.path.join(DOWNLOADS, "WhatsApp Image 2026-06-20 at 3.55.39 PM.jpeg")  # gorra roja
    foto3 = os.path.join(DOWNLOADS, "WhatsApp Image 2026-06-20 at 3.56.19 PM.jpeg")  # grupo (naranja + gris)

    print("=" * 60)
    print("ANALIZANDO FOTOS DE REFERENCIA")
    print("=" * 60)

    img1, faces1 = mostrar_caras(foto1)
    img2, faces2 = mostrar_caras(foto2)
    img3, faces3 = mostrar_caras(foto3)

    print("\n" + "=" * 60)
    print("EXTRAYENDO CARAS PARA LOS DOS VIDEOS")
    print("=" * 60)

    # VIDEO 1:
    # - Joven (izquierda video) = trigueño gafas gris (DERECHA en foto3 = índice 1 por x)
    # - Anciano (derecha video) = anciano gafas azul (foto1 = única cara principal)
    print("\n[VIDEO 1]")
    extraer_cara(foto3, cara_index_por_x=1,
                 salida_path=str(WORK_DIR / "v1_joven_trigueño.jpg"))
    extraer_cara(foto1, cara_index_por_x=0,
                 salida_path=str(WORK_DIR / "v1_anciano.jpg"))

    # VIDEO 2:
    # - Joven (izquierda video) = hijo naranja (IZQUIERDA en foto3 = índice 0 por x)
    # - Anciano (derecha video) = gorra roja (foto2)
    print("\n[VIDEO 2]")
    extraer_cara(foto3, cara_index_por_x=0,
                 salida_path=str(WORK_DIR / "v2_hijo_naranja.jpg"))
    extraer_cara(foto2, cara_index_por_x=0,
                 salida_path=str(WORK_DIR / "v2_gorra_roja.jpg"))

    print("\n[OK] Todas las caras preparadas en:")
    print(f"  {WORK_DIR}")
    for f in WORK_DIR.glob("*.jpg"):
        print(f"    {f.name}")
