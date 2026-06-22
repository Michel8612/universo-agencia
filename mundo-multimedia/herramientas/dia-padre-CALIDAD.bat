@echo off
setlocal
set BASE=D:\Proyectos claude\mundo-multimedia\proyectos\face-swap
set SCRIPT=D:\Proyectos claude\mundo-multimedia\herramientas\face_swap_video.py
set FFMPEG=C:\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe
set FFPROBE=C:\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffprobe.exe
set VIDEO=C:\Users\Romer\Downloads\WhatsApp Video 2026-06-20 at 4.03.42 PM.mp4
set CD=%BASE%\_chunks_calidad
set OUT=%BASE%\dia_padre_CALIDAD.mp4

echo.
echo ============================================================
echo  NEXIA - DIA DEL PADRE - CALIDAD COMPLETA (720x1280)
echo  Sin --fast: resolucion completa, cada frame procesado
echo  GPU DirectML activado para mayor velocidad
echo ============================================================
echo.

:: Limpiar y crear carpeta temporal
if exist "%CD%" rmdir /s /q "%CD%"
mkdir "%CD%"

:: Dividir en 4 chunks (corte exacto por keyframes)
echo [1/3] Dividiendo video en 4 chunks...
for /f %%D in ('"%FFPROBE%" -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "%VIDEO%"') do set DUR=%%D

echo Duracion detectada: %DUR%s
"%FFMPEG%" -y -i "%VIDEO%" -c copy -f segment -segment_time 30 -reset_timestamps 1 "%CD%\chunk_%%02d.mp4" 2>nul
echo Chunks creados.

:: Esperar a que los chunks esten listos
timeout /t 2 /nobreak >nul

:: Contar chunks
set COUNT=0
for %%F in ("%CD%\chunk_*.mp4") do set /a COUNT+=1
echo %COUNT% chunks detectados.

echo.
echo [2/3] Lanzando %COUNT% workers GPU (calidad completa)...
echo NOTA: SIN --fast = 720x1280, cada frame procesado = calidad maxima
echo Estimado: 8-15 minutos con DirectML
echo.

:: Lanzar workers — SIN --fast, CON --gpu
:: Fotos actualizadas: padre_nuevo.jpg (45KB, frontal) + hijo_nuevo.jpg (72KB)
start "Worker-0" /min python "%SCRIPT%" --video "%CD%\chunk_00.mp4" --source1 "%BASE%\padre_nuevo.jpg" --source2 "%BASE%\hijo_nuevo.jpg" --output "%CD%\swapped_00.mp4" --gpu
start "Worker-1" /min python "%SCRIPT%" --video "%CD%\chunk_01.mp4" --source1 "%BASE%\padre_nuevo.jpg" --source2 "%BASE%\hijo_nuevo.jpg" --output "%CD%\swapped_01.mp4" --gpu
start "Worker-2" /min python "%SCRIPT%" --video "%CD%\chunk_02.mp4" --source1 "%BASE%\padre_nuevo.jpg" --source2 "%BASE%\hijo_nuevo.jpg" --output "%CD%\swapped_02.mp4" --gpu
start "Worker-3" /min python "%SCRIPT%" --video "%CD%\chunk_03.mp4" --source1 "%BASE%\padre_nuevo.jpg" --source2 "%BASE%\hijo_nuevo.jpg" --output "%CD%\swapped_03.mp4" --gpu

echo 4 workers GPU en marcha. Esperando resultados...
echo (Puedes ver progreso en las ventanas minimizadas de la barra de tareas)
echo.

:: Esperar a que todos los chunks esten listos (minimo 5MB a full res)
:WAIT
timeout /t 30 /nobreak >nul
echo Revisando progreso...
if not exist "%CD%\swapped_00.mp4" goto WAIT
if not exist "%CD%\swapped_01.mp4" goto WAIT
if not exist "%CD%\swapped_02.mp4" goto WAIT
if not exist "%CD%\swapped_03.mp4" goto WAIT
for %%A in ("%CD%\swapped_00.mp4") do if %%~zA LSS 5000000 goto WAIT
for %%A in ("%CD%\swapped_01.mp4") do if %%~zA LSS 5000000 goto WAIT
for %%A in ("%CD%\swapped_02.mp4") do if %%~zA LSS 5000000 goto WAIT
for %%A in ("%CD%\swapped_03.mp4") do if %%~zA LSS 5000000 goto WAIT

echo [OK] Los %COUNT% chunks completados a CALIDAD COMPLETA.

echo.
echo [3/3] Uniendo chunks y mezclando audio original...

:: Concat list
echo file '%CD%\swapped_00.mp4' > "%CD%\concat.txt"
echo file '%CD%\swapped_01.mp4'>> "%CD%\concat.txt"
echo file '%CD%\swapped_02.mp4'>> "%CD%\concat.txt"
echo file '%CD%\swapped_03.mp4'>> "%CD%\concat.txt"

:: Join chunks
"%FFMPEG%" -y -f concat -safe 0 -i "%CD%\concat.txt" -c copy "%CD%\joined.mp4" 2>nul

:: Add original audio
"%FFMPEG%" -y -i "%CD%\joined.mp4" -i "%VIDEO%" -c:v copy -c:a aac -b:a 128k -map 0:v:0 -map 1:a:0 -movflags +faststart -shortest "%OUT%" 2>nul

:: Limpieza
del /f /q "%CD%\*" 2>nul
rmdir "%CD%" 2>nul

echo.
echo ============================================================
echo  VIDEO FINAL LISTO: %OUT%
echo  Resolucion: 720x1280 (calidad completa)
echo ============================================================
pause
