# NEXIA — Dia del Padre: Split + 4 procesos independientes + Join
# Evita ProcessPoolExecutor que rompe DirectML

$BASE    = "D:\Proyectos claude\mundo-multimedia\proyectos\face-swap"
$SCRIPT  = "D:\Proyectos claude\mundo-multimedia\herramientas\face_swap_video.py"
$VIDEO   = "C:\Users\Romer\Downloads\WhatsApp Video 2026-06-20 at 4.03.42 PM.mp4"
$FFMPEG  = "C:\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"
$FFPROBE = "C:\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffprobe.exe"
$CD      = "$BASE\_chunks_dp"
$OUT     = "$BASE\dia_padre_final.mp4"

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  NEXIA — DIA DEL PADRE  (PS + GPU DirectML + 4 workers)" -ForegroundColor Cyan
Write-Host "============================================================`n"

# ─── 1. SPLIT ────────────────────────────────────────────────────────
Write-Host "[1/3] Dividiendo video en 4 chunks..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force $CD | Out-Null

# Duracion del video
$dur = [float]($( & $FFPROBE -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VIDEO" ))
$step = $dur / 4
Write-Host "  Duracion: $([math]::Round($dur,1))s — $([math]::Round($step,1))s por chunk"

for ($i = 0; $i -lt 4; $i++) {
    $ss  = $i * $step
    $out = "$CD\chunk_0$i.mp4"
    & $FFMPEG -y -ss $ss -i "$VIDEO" -t $step -c copy -avoid_negative_ts make_zero "$out" 2>$null
    Write-Host "  Chunk $($i+1)/4 → $([math]::Round($ss,1))s - $([math]::Round($ss+$step,1))s"
}

# ─── 2. PROCESAR EN PARALELO ──────────────────────────────────────────
Write-Host "`n[2/3] Lanzando 4 workers con GPU DirectML..." -ForegroundColor Yellow

$procs = @()
for ($i = 0; $i -lt 4; $i++) {
    $args = @(
        $SCRIPT,
        "--video",   "$CD\chunk_0$i.mp4",
        "--source1", "$BASE\v1_anciano.jpg",
        "--source2", "$BASE\v2_gorra_roja.jpg",
        "--source3", "$BASE\v2_hijo_naranja.jpg",
        "--output",  "$CD\swapped_0$i.mp4",
        "--gpu", "--fast"
    )
    # Start-Process lanza proceso independiente (no subprocess) — DML funciona correctamente
    $p = Start-Process python -ArgumentList $args -PassThru -WindowStyle Minimized
    $procs += $p
    Write-Host "  Worker $i iniciado (PID $($p.Id))"
    Start-Sleep -Seconds 5   # escalonar inicializacion GPU para evitar conflictos DML
}

Write-Host "`n  Esperando que terminen los 4 workers (~5-7 min cada uno)..."
Write-Host "  Puedes ver el progreso en las 4 ventanas minimizadas en la barra de tareas`n"

# Esperar a todos
$start = Get-Date
foreach ($p in $procs) {
    $p.WaitForExit()
}
$elapsed = ((Get-Date) - $start).TotalMinutes
Write-Host "  Procesamiento terminado en $([math]::Round($elapsed,1)) min" -ForegroundColor Green

# Verificar que todos produjeron output
$ok = $true
for ($i = 0; $i -lt 4; $i++) {
    $f = "$CD\swapped_0$i.mp4"
    if (!(Test-Path $f) -or (Get-Item $f).Length -lt 100000) {
        Write-Host "  [ERROR] Worker $i no produjo output valido" -ForegroundColor Red
        $ok = $false
    }
}
if (!$ok) { Write-Host "[FALLO] Algunos chunks fallaron. Revisa las ventanas." -ForegroundColor Red; exit 1 }

# ─── 3. JOIN ────────────────────────────────────────────────────────
Write-Host "`n[3/3] Uniendo chunks y mezclando audio original..." -ForegroundColor Yellow

$concatFile = "$CD\concat.txt"
$joined     = "$CD\joined_noaudio.mp4"

# Concat list
"file '$CD\swapped_00.mp4'`nfile '$CD\swapped_01.mp4'`nfile '$CD\swapped_02.mp4'`nfile '$CD\swapped_03.mp4'" | Out-File $concatFile -Encoding utf8

# Concat video
& $FFMPEG -y -f concat -safe 0 -i $concatFile -c copy $joined 2>$null

# Add original audio
& $FFMPEG -y -i $joined -i "$VIDEO" -c:v copy -c:a aac -b:a 128k -map 0:v:0 -map 1:a:0 -movflags +faststart -shortest "$OUT" 2>$null

# Cleanup
Remove-Item $CD -Recurse -Force -ErrorAction SilentlyContinue

$size = [math]::Round((Get-Item $OUT).Length / 1MB, 1)
$totalMin = [math]::Round(((Get-Date) - $start).TotalMinutes, 1)

Write-Host "`n============================================================" -ForegroundColor Green
Write-Host "  COMPLETADO en $totalMin minutos — $size MB" -ForegroundColor Green
Write-Host "  Output: $OUT" -ForegroundColor Green
Write-Host "============================================================`n"
