"""
UNIVERSO AGENCIA — Face Swap Video Tool
mundo-multimedia | Reemplaza caras en video manteniendo audio original

Uso:
    python face_swap_video.py --video VIDEO.mp4 \
        --source1 FOTO_PERSONA1.jpg --source2 FOTO_PERSONA2.jpg \
        --output resultado.mp4 [--video2 resultado2.mp4 --source1b FOTO_P1B.jpg --source2b FOTO_P2B.jpg]

El script procesa en CPU. Para video de ~2 min espera 20-40 min.
"""

import os, sys, cv2, numpy as np, urllib.request, argparse, time, subprocess
from pathlib import Path

FFMPEG  = r"C:\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"
MODEL_DIR  = Path.home() / ".insightface" / "models"
INSWAPPER  = MODEL_DIR / "inswapper_128.onnx"
BUFFALO_L  = MODEL_DIR / "buffalo_l"

INSWAPPER_URL = "https://huggingface.co/ezioruan/inswapper_128.onnx/resolve/main/inswapper_128.onnx"


def download_model():
    """Download inswapper_128.onnx if not present (~554 MB)."""
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    if INSWAPPER.exists():
        print(f"[OK] inswapper model found: {INSWAPPER}")
        return
    print(f"Downloading inswapper_128.onnx (~554 MB) — esto tarda unos minutos...")

    def progress(block_num, block_size, total_size):
        pct = block_num * block_size * 100 / total_size
        if block_num % 200 == 0:
            mb = block_num * block_size / 1_000_000
            print(f"  {mb:.0f} MB / {total_size/1_000_000:.0f} MB  ({pct:.1f}%)", flush=True)

    urllib.request.urlretrieve(INSWAPPER_URL, INSWAPPER, reporthook=progress)
    print(f"[OK] Downloaded to {INSWAPPER}")


def load_models(det_size=640, use_dml=False):
    """Load FaceAnalysis app and inswapper model."""
    import insightface
    from insightface.app import FaceAnalysis
    from insightface.model_zoo import get_model

    # buffalo_l detection — siempre CPU (DML tiene ops Reshape incompatibles)
    print(f"Loading face analysis models (buffalo_l CPU, det_size={det_size})...")
    try:
        app = FaceAnalysis(name="buffalo_l", root=str(Path.home() / ".insightface"),
                           providers=['CPUExecutionProvider'])
    except TypeError:
        app = FaceAnalysis(name="buffalo_l", root=str(Path.home() / ".insightface"))
    app.prepare(ctx_id=-1, det_size=(det_size, det_size))
    print("[OK] buffalo_l loaded (CPU)")

    # inswapper — GPU via DirectML si disponible (este es el cuello de botella real)
    if use_dml:
        swap_providers = ['DmlExecutionProvider', 'CPUExecutionProvider']
        print("[GPU] DirectML habilitado para inswapper — AMD Radeon via DirectML")
    else:
        swap_providers = ['CPUExecutionProvider']

    print("Loading inswapper model...")
    try:
        swapper = get_model(str(INSWAPPER), download=False, providers=swap_providers)
    except TypeError:
        swapper = get_model(str(INSWAPPER), download=False)
    print("[OK] inswapper loaded")

    return app, swapper


def get_best_face(app, img):
    """Return the largest detected face (most prominent)."""
    faces = app.get(img)
    if not faces:
        return None
    return max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))


def match_face(detected_face, source_faces):
    """Match detected face to the most similar source face using cosine similarity.

    Uses normed_embedding (face identity vector) — works regardless of position in frame.
    Score range: -1 to 1 (1 = identical person).
    """
    emb = detected_face.normed_embedding
    scores = [np.dot(emb, src.normed_embedding) for src in source_faces]
    return source_faces[int(np.argmax(scores))]


def process_video(video_path, src_face_left, src_face_right, output_path, app, swapper, scale=1.0, skip=1, source_faces=None):
    """
    Swap faces in video.
    scale: resize frames before processing (0.5 = mitad de resolución, más rápido)
    skip:  procesar 1 de cada N frames (skip=2 = mitad de frames, 2x más rápido)
    """
    cap   = cv2.VideoCapture(video_path)
    fps   = cap.get(cv2.CAP_PROP_FPS)
    W_orig = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    H_orig = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total  = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    W_out = int(W_orig * scale)
    H_out = int(H_orig * scale)
    # Asegurar dimensiones pares (requerido por codecs)
    W_out = W_out if W_out % 2 == 0 else W_out - 1
    H_out = H_out if H_out % 2 == 0 else H_out - 1

    temp_path = str(output_path).replace(".mp4", "_noaudio.mp4")
    out = cv2.VideoWriter(temp_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (W_out, H_out))

    print(f"\nProcessing {total} frames @ {fps:.0f}fps — salida {W_out}x{H_out} (scale={scale}, skip={skip})")
    print(f"Frames a procesar: {total // skip} (ETA estimada: {(total // skip) * 4 / 60:.0f}-{(total // skip) * 6 / 60:.0f} min)\n")
    start = time.time()
    frame_idx = 0
    processed = 0
    last_swapped = None  # último frame procesado (para duplicar en frames saltados)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if scale != 1.0:
            frame = cv2.resize(frame, (W_out, H_out), interpolation=cv2.INTER_LINEAR)

        if frame_idx % skip == 0:
            faces = app.get(frame)
            if faces:
                srcs = source_faces if source_faces else [src_face_left, src_face_right]
                for face in faces:
                    src = match_face(face, srcs)
                    frame = swapper.get(frame, face, src, paste_back=True)
            last_swapped = frame
        else:
            # Frame saltado: reusar el último procesado
            if last_swapped is not None:
                frame = last_swapped

        out.write(frame)
        frame_idx += 1
        processed += 1

        if processed % 25 == 0:
            elapsed   = time.time() - start
            fps_proc  = processed / elapsed
            remaining = (total - processed) / max(fps_proc, 0.01)
            print(f"  frame {processed}/{total}  |  {fps_proc:.2f} fps  |  ETA {remaining/60:.1f} min", flush=True)

    cap.release()
    out.release()

    # Convertir a H.264 + audio original (compatible con todos los reproductores)
    print("\nConvirtiendo a H.264 y mezclando audio original...")
    cmd = [
        FFMPEG, "-y",
        "-i", temp_path,
        "-i", video_path,
        "-c:v", "libx264",   # H.264 — reproduce en WhatsApp, móvil, web, todo
        "-crf", "26",        # calidad (18=máx, 28=mínimo) — 26 es buen balance
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "128k",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-movflags", "+faststart",  # streaming-friendly
        str(output_path)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    os.remove(temp_path)
    size = os.path.getsize(output_path) / 1_000_000
    print(f"[DONE] {output_path} — {size:.1f} MB")


def main():
    parser = argparse.ArgumentParser(description="Face Swap Video — Universo Agencia")
    parser.add_argument("--video",   required=True, help="Video source path")
    parser.add_argument("--source1", required=True, help="Foto persona 1")
    parser.add_argument("--source2", required=True, help="Foto persona 2")
    parser.add_argument("--source3", help="Foto persona 3 (opcional)")
    parser.add_argument("--output",  required=True, help="Output video path")
    # Optional second video with different actors
    parser.add_argument("--source1b", help="Photo: left person video 2")
    parser.add_argument("--source2b", help="Photo: right person video 2")
    parser.add_argument("--output2",  help="Output path video 2")
    # Velocidad / calidad
    parser.add_argument("--scale", type=float, default=1.0,
                        help="Escala de resolución (0.5=mitad, más rápido). Default: 1.0")
    parser.add_argument("--skip",  type=int, default=1,
                        help="Procesar 1 de cada N frames (2=2x rápido). Default: 1")
    parser.add_argument("--det",   type=int, default=640,
                        help="Tamaño detección caras (320=más rápido, menos preciso). Default: 640")
    parser.add_argument("--fast", action="store_true",
                        help="Modo rápido: scale=0.5, skip=2, det=320 (~4x más rápido)")
    parser.add_argument("--gpu", action="store_true",
                        help="Usar AMD GPU via DirectML (onnxruntime-directml)")
    args = parser.parse_args()

    if args.fast:
        args.scale = 0.5
        args.skip  = 2
        args.det   = 320
        print("[FAST MODE] scale=0.5, skip=2, det=320 — estimado ~4x más rápido")

    # 1. Download model if needed
    download_model()

    # 2. Load models
    app, swapper = load_models(det_size=args.det, use_dml=args.gpu)

    # 3. Extract source faces from reference photos
    print("\nExtracting source faces from reference photos...")

    img1 = cv2.imread(args.source1)
    img2 = cv2.imread(args.source2)
    assert img1 is not None, f"Cannot read: {args.source1}"
    assert img2 is not None, f"Cannot read: {args.source2}"

    face_left  = get_best_face(app, img1)
    face_right = get_best_face(app, img2)

    assert face_left  is not None, f"No face detected in: {args.source1}"
    assert face_right is not None, f"No face detected in: {args.source2}"
    print(f"[OK] Persona 1 bbox: {face_left.bbox.astype(int)}")
    print(f"[OK] Persona 2 bbox: {face_right.bbox.astype(int)}")

    source_faces = [face_left, face_right]

    # Persona 3 opcional
    if args.source3:
        img3 = cv2.imread(args.source3)
        assert img3 is not None, f"Cannot read: {args.source3}"
        face3 = get_best_face(app, img3)
        assert face3 is not None, f"No face detected in: {args.source3}"
        source_faces.append(face3)
        print(f"[OK] Persona 3 bbox: {face3.bbox.astype(int)}")

    # 4. Process VIDEO 1
    print(f"\n{'='*55}")
    print(f"VIDEO 1: {args.output}  ({len(source_faces)} personas)")
    print(f"{'='*55}")
    process_video(args.video, source_faces[0], source_faces[-1], args.output, app, swapper,
                  scale=args.scale, skip=args.skip, source_faces=source_faces)

    # 5. Process VIDEO 2 (if provided)
    if args.source1b and args.source2b and args.output2:
        print(f"\n{'='*55}")
        print(f"VIDEO 2: {args.output2}")
        print(f"{'='*55}")

        img1b = cv2.imread(args.source1b)
        img2b = cv2.imread(args.source2b)
        assert img1b is not None, f"Cannot read: {args.source1b}"
        assert img2b is not None, f"Cannot read: {args.source2b}"

        face_left_b  = get_best_face(app, img1b)
        face_right_b = get_best_face(app, img2b)

        assert face_left_b  is not None, f"No face detected in: {args.source1b}"
        assert face_right_b is not None, f"No face detected in: {args.source2b}"
        print(f"[OK] Left face bbox: {face_left_b.bbox.astype(int)}")
        print(f"[OK] Right face bbox: {face_right_b.bbox.astype(int)}")

        process_video(args.video, face_left_b, face_right_b, args.output2, app, swapper,
                      scale=args.scale, skip=args.skip)

    print("\n[NEXIA] Face swap completado.")


if __name__ == "__main__":
    main()
