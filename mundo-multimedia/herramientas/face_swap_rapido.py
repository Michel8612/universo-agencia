"""
NEXIA — Face Swap Rapido (Paralelo + GPU)
Divide el video en N chunks, los procesa en paralelo y los une.
Con DirectML + 4 workers = ~15 min para video de 2 min
"""
import os, sys, subprocess, argparse, time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

FFMPEG  = r"C:\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"
SCRIPT  = str(Path(__file__).parent / "face_swap_video.py")


def get_video_duration(video_path):
    """Get video duration in seconds using FFprobe."""
    ffprobe = FFMPEG.replace("ffmpeg.exe", "ffprobe.exe")
    cmd = [ffprobe, "-v", "error", "-show_entries", "format=duration",
           "-of", "default=noprint_wrappers=1:nokey=1", video_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())


def split_video(video_path, chunk_dir, n_chunks):
    """Split video into N chunks using FFmpeg stream copy (fast, no re-encode)."""
    duration = get_video_duration(video_path)
    chunk_duration = duration / n_chunks
    chunks = []

    for i in range(n_chunks):
        start = i * chunk_duration
        out_path = str(chunk_dir / f"chunk_{i:02d}.mp4")
        cmd = [
            FFMPEG, "-y",
            "-ss", str(start),
            "-i", video_path,
            "-t", str(chunk_duration),
            "-c", "copy",
            "-avoid_negative_ts", "make_zero",
            out_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        chunks.append(out_path)
        print(f"  [split] Chunk {i+1}/{n_chunks} — {start:.1f}s → {start+chunk_duration:.1f}s")

    return chunks, duration


def process_chunk(args_tuple):
    """Worker function: process a single chunk with face_swap_video.py"""
    chunk_path, source1, source2, source3, out_path, use_gpu, chunk_idx = args_tuple

    cmd = [
        sys.executable, SCRIPT,
        "--video",   chunk_path,
        "--source1", source1,
        "--source2", source2,
        "--output",  out_path,
        "--fast",
    ]
    if source3:
        cmd += ["--source3", source3]
    if use_gpu:
        cmd.append("--gpu")

    print(f"  [worker {chunk_idx}] Iniciando → {Path(out_path).name}")
    start = time.time()
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8:replace"  # evita crash por mensajes en español de onnxruntime
    result = subprocess.run(cmd, capture_output=True, env=env)
    elapsed = time.time() - start

    stderr_text = result.stderr.decode("utf-8", errors="replace") if result.stderr else ""
    if result.returncode != 0:
        print(f"  [worker {chunk_idx}] ERROR:\n{stderr_text[-500:]}")
        return False, chunk_idx, elapsed
    print(f"  [worker {chunk_idx}] LISTO en {elapsed/60:.1f} min")
    return True, chunk_idx, elapsed


def join_chunks(chunk_outputs, output_path, original_video, chunk_dir):
    """Join processed chunks + mux original audio with FFmpeg concat."""
    # Build concat file
    concat_file = str(chunk_dir / "concat.txt")
    with open(concat_file, "w") as f:
        for p in chunk_outputs:
            f.write(f"file '{p}'\n")

    temp_joined = str(chunk_dir / "joined_noaudio.mp4")
    # Concat video chunks
    cmd_concat = [
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_file,
        "-c", "copy",
        temp_joined
    ]
    subprocess.run(cmd_concat, check=True, capture_output=True)

    # Add original audio
    cmd_audio = [
        FFMPEG, "-y",
        "-i", temp_joined,
        "-i", original_video,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "128k",
        "-map", "0:v:0", "-map", "1:a:0",
        "-movflags", "+faststart",
        "-shortest",
        str(output_path)
    ]
    subprocess.run(cmd_audio, check=True, capture_output=True)
    os.remove(temp_joined)
    print(f"[JOIN] Audio mezclado: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Face Swap Rapido — Paralelo + GPU")
    parser.add_argument("--video",   required=True)
    parser.add_argument("--source1", required=True)
    parser.add_argument("--source2", required=True)
    parser.add_argument("--source3", help="Foto persona 3 (opcional)")
    parser.add_argument("--output",  required=True)
    parser.add_argument("--workers", type=int, default=4,
                        help="Chunks paralelos (default: 4 — uno por cada 2 nucleos)")
    parser.add_argument("--gpu", action="store_true",
                        help="Usar AMD GPU via DirectML")
    args = parser.parse_args()

    out_path = Path(args.output)
    chunk_dir = out_path.parent / f"_chunks_{out_path.stem}"
    chunk_dir.mkdir(exist_ok=True)

    total_start = time.time()
    print(f"\n{'='*60}")
    print(f"  NEXIA Face Swap Rapido — {args.workers} workers {'+ GPU DirectML' if args.gpu else '(CPU)'}")
    print(f"  Video: {Path(args.video).name}")
    print(f"  Output: {out_path.name}")
    print(f"{'='*60}\n")

    # 1. Split
    print(f"[1/3] Dividiendo video en {args.workers} chunks...")
    chunks, total_dur = split_video(args.video, chunk_dir, args.workers)
    print(f"  Duracion total: {total_dur:.1f}s — {total_dur/args.workers:.1f}s por chunk\n")

    # 2. Process in parallel
    print(f"[2/3] Procesando {args.workers} chunks en paralelo...")
    chunk_outputs = []
    worker_args = []
    for i, chunk in enumerate(chunks):
        out_chunk = str(chunk_dir / f"swapped_{i:02d}.mp4")
        chunk_outputs.append(out_chunk)
        worker_args.append((chunk, args.source1, args.source2, args.source3, out_chunk, args.gpu, i))

    success_count = 0
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(process_chunk, wa): wa for wa in worker_args}
        for future in as_completed(futures):
            ok, idx, elapsed = future.result()
            if ok:
                success_count += 1

    if success_count < args.workers:
        print(f"[ERROR] Solo {success_count}/{args.workers} chunks completados")
        sys.exit(1)

    # 3. Join
    print(f"\n[3/3] Uniendo chunks y mezclando audio original...")
    join_chunks(chunk_outputs, out_path, args.video, chunk_dir)

    # Cleanup
    for f in chunk_dir.glob("*.mp4"):
        f.unlink()
    for f in chunk_dir.glob("*.txt"):
        f.unlink()
    chunk_dir.rmdir()

    total_elapsed = time.time() - total_start
    size = os.path.getsize(str(out_path)) / 1_000_000
    print(f"\n{'='*60}")
    print(f"  COMPLETADO en {total_elapsed/60:.1f} minutos — {size:.1f} MB")
    print(f"  Output: {out_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
