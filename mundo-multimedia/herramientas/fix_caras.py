"""
Fix cara extraction — analyzes all faces in each photo and re-extracts correctly.
"""
import cv2, os
from pathlib import Path
import insightface
from insightface.app import FaceAnalysis

WORK = Path(r"D:\Proyectos claude\mundo-multimedia\proyectos\face-swap")
WORK.mkdir(parents=True, exist_ok=True)

DOWNLOADS = r"C:\Users\Romer\Downloads"
foto1 = os.path.join(DOWNLOADS, "WhatsApp Image 2026-06-20 at 3.52.11 PM.jpeg")  # anciano gafas azul
foto2 = os.path.join(DOWNLOADS, "WhatsApp Image 2026-06-20 at 3.55.39 PM.jpeg")  # gorra roja
foto3 = os.path.join(DOWNLOADS, "WhatsApp Image 2026-06-20 at 3.56.19 PM.jpeg")  # grupo

app = FaceAnalysis(name="buffalo_l", root=str(Path.home() / ".insightface"))
app.prepare(ctx_id=0, det_size=(640, 640))


def analizar_foto(path, label):
    img = cv2.imread(path)
    faces = app.get(img)
    faces_sorted = sorted(faces, key=lambda f: (f.bbox[0]+f.bbox[2])/2)
    print(f"\n=== {label} ===  {img.shape[1]}x{img.shape[0]}  Caras: {len(faces_sorted)}")
    for i, f in enumerate(faces_sorted):
        cx = int((f.bbox[0]+f.bbox[2])/2)
        cy = int((f.bbox[1]+f.bbox[3])/2)
        w = int(f.bbox[2]-f.bbox[0])
        h = int(f.bbox[3]-f.bbox[1])
        pos = "IZQ" if cx < img.shape[1]/2 else "DER"
        print(f"  [{i}] cx={cx} cy={cy} tamanio={w}x{h} [{pos}] score={f.det_score:.2f}")
        # Save each detected face
        pad = 0.4
        x1 = max(0, int(f.bbox[0] - (f.bbox[2]-f.bbox[0])*pad))
        y1 = max(0, int(f.bbox[1] - (f.bbox[3]-f.bbox[1])*pad))
        x2 = min(img.shape[1], int(f.bbox[2] + (f.bbox[2]-f.bbox[0])*pad))
        y2 = min(img.shape[0], int(f.bbox[3] + (f.bbox[3]-f.bbox[1])*pad))
        crop = img[y1:y2, x1:x2]
        out = str(WORK / f"debug_{label}_cara{i}.jpg")
        cv2.imwrite(out, crop)
        print(f"         -> guardada: debug_{label}_cara{i}.jpg")
    return img, faces_sorted


# Analyze all
img1, f1 = analizar_foto(foto1, "foto1_anciano")
img2, f2 = analizar_foto(foto2, "foto2_gorraroja")
img3, f3 = analizar_foto(foto3, "foto3_grupo")

# === Determine correct indices based on output ===
# FOTO 1: man in blue shirt is typically on the RIGHT (higher x) = last in sorted list
# FOTO 3:
#   - Woman in military jacket is far LEFT (index 0)
#   - Man in ORANGE shirt is next LEFT (index 1)
#   - Man in gray shirt with glasses is CENTER (index 2 or 3)

print("\n\n=== EXTRACTING FINAL FACES ===")

def extract_face(img, faces_sorted, idx, output_name, padding=0.5):
    if idx >= len(faces_sorted):
        print(f"ERROR: solo {len(faces_sorted)} caras, se pidio indice {idx}")
        return
    f = faces_sorted[idx]
    pw = int((f.bbox[2]-f.bbox[0]) * padding)
    ph = int((f.bbox[3]-f.bbox[1]) * padding)
    x1 = max(0, int(f.bbox[0]) - pw)
    y1 = max(0, int(f.bbox[1]) - ph)
    x2 = min(img.shape[1], int(f.bbox[2]) + pw)
    y2 = min(img.shape[0], int(f.bbox[3]) + ph)
    crop = img[y1:y2, x1:x2]
    out = str(WORK / output_name)
    cv2.imwrite(out, crop)
    size = os.path.getsize(out)
    print(f"[OK] {output_name}  ({size//1024}KB)  cara_idx={idx}  bbox={int(f.bbox[0])},{int(f.bbox[1])},{int(f.bbox[2])},{int(f.bbox[3])}")

# VIDEO 1: anciano (rightmost in foto1) + trigueño gafas gris (foto3)
# Foto1: man is on the RIGHT = last index
extract_face(img1, f1, len(f1)-1, "v1_anciano.jpg")
# Foto3: trigueño gafas gris — likely index 2 (after woman idx0, orange idx1)
# We'll extract index 2 (center person with glasses in dark gray shirt)
extract_face(img3, f3, 2, "v1_joven_gris.jpg")

# VIDEO 2: gorra roja (foto2, single dominant face) + hijo naranja (foto3, index 1)
extract_face(img2, f2, 0, "v2_gorra_roja.jpg")
# Foto3: hijo naranja — index 1 (after woman in military)
extract_face(img3, f3, 1, "v2_hijo_naranja.jpg")

print("\nDone. Check debug images to verify correctness.")
print(f"Files in {WORK}:")
for f in sorted(WORK.glob("*.jpg")):
    sz = f.stat().st_size // 1024
    print(f"  {f.name}  ({sz}KB)")
