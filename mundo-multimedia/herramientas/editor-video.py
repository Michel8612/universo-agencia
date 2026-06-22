"""
Editor de vídeo — mundo-multimedia (usa FFmpeg, sin coste)
Requiere FFmpeg instalado: winget install ffmpeg

Uso:
  python editor-video.py --input video.mp4 --modo cortar --inicio 0:10 --fin 0:45
  python editor-video.py --input video.mp4 --modo subtitulos
  python editor-video.py --input video.mp4 --modo convertir --formato mp4
  python editor-video.py --input video.mp4 --modo gif --inicio 0:05 --fin 0:10
"""
import argparse
import subprocess
import os
import sys

def ffmpeg(args_list):
    cmd = ["ffmpeg", "-y"] + args_list
    print(f"  Ejecutando: {' '.join(cmd[:6])}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  Error FFmpeg: {result.stderr[-300:]}")
        return False
    return True

def verificar_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True)
        return True
    except FileNotFoundError:
        print("FFmpeg no está instalado.")
        print("Instala con: winget install ffmpeg")
        print("O descarga desde: https://ffmpeg.org/download.html")
        return False

def tiempo_a_segundos(t):
    partes = t.split(":")
    if len(partes) == 2:
        return int(partes[0]) * 60 + float(partes[1])
    elif len(partes) == 3:
        return int(partes[0]) * 3600 + int(partes[1]) * 60 + float(partes[2])
    return float(t)

def cortar(input_path, inicio, fin, salida=None):
    nombre = os.path.splitext(input_path)[0]
    ext = os.path.splitext(input_path)[1]
    if not salida:
        salida = f"{nombre}_corte{ext}"
    dur = tiempo_a_segundos(fin) - tiempo_a_segundos(inicio)
    ok = ffmpeg(["-i", input_path, "-ss", str(inicio), "-t", str(dur),
                 "-c", "copy", salida])
    if ok:
        print(f"  Clip guardado: {salida}")

def convertir(input_path, formato, salida=None):
    nombre = os.path.splitext(input_path)[0]
    if not salida:
        salida = f"{nombre}_convertido.{formato}"
    args = ["-i", input_path]
    if formato == "gif":
        args += ["-vf", "fps=10,scale=480:-1:flags=lanczos", "-loop", "0"]
    elif formato == "mp4":
        args += ["-c:v", "libx264", "-crf", "23", "-c:a", "aac"]
    args.append(salida)
    ok = ffmpeg(args)
    if ok:
        size_mb = os.path.getsize(salida) / (1024*1024)
        print(f"  Convertido: {salida} ({size_mb:.1f} MB)")

def extraer_audio(input_path, salida=None):
    nombre = os.path.splitext(input_path)[0]
    if not salida:
        salida = f"{nombre}.mp3"
    ok = ffmpeg(["-i", input_path, "-q:a", "0", "-map", "a", salida])
    if ok:
        print(f"  Audio extraído: {salida}")

def hacer_gif(input_path, inicio, fin, salida=None):
    nombre = os.path.splitext(input_path)[0]
    if not salida:
        salida = f"{nombre}.gif"
    dur = tiempo_a_segundos(fin) - tiempo_a_segundos(inicio)
    ok = ffmpeg(["-i", input_path, "-ss", str(inicio), "-t", str(dur),
                 "-vf", "fps=12,scale=480:-1:flags=lanczos", "-loop", "0", salida])
    if ok:
        size_mb = os.path.getsize(salida) / (1024*1024)
        print(f"  GIF creado: {salida} ({size_mb:.1f} MB)")

def info(input_path):
    result = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json",
                             "-show_format", "-show_streams", input_path],
                            capture_output=True, text=True)
    print(result.stdout[:1000] if result.stdout else "No se pudo obtener info")

if __name__ == "__main__":
    if not verificar_ffmpeg():
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Editor de vídeo con FFmpeg")
    parser.add_argument("--input", required=True, help="Archivo de vídeo")
    parser.add_argument("--modo", default="info",
                        choices=["cortar", "convertir", "audio", "gif", "info"])
    parser.add_argument("--inicio", default="0:00", help="Tiempo inicio (mm:ss)")
    parser.add_argument("--fin", default="0:30", help="Tiempo fin (mm:ss)")
    parser.add_argument("--formato", default="mp4", help="Formato destino")
    parser.add_argument("--salida", help="Nombre archivo salida")
    args = parser.parse_args()

    print(f"\n→ Modo: {args.modo} | Archivo: {args.input}\n")

    if args.modo == "cortar":
        cortar(args.input, args.inicio, args.fin, args.salida)
    elif args.modo == "convertir":
        convertir(args.input, args.formato, args.salida)
    elif args.modo == "audio":
        extraer_audio(args.input, args.salida)
    elif args.modo == "gif":
        hacer_gif(args.input, args.inicio, args.fin, args.salida)
    elif args.modo == "info":
        info(args.input)
