@echo off
setlocal
set BASE=D:\Proyectos claude\mundo-multimedia\proyectos\face-swap
set CD=%BASE%\_chunks_dp
set SCRIPT=D:\Proyectos claude\mundo-multimedia\herramientas\face_swap_video.py
set OUT=%BASE%\dia_padre_final.mp4
set FFMPEG=C:\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe
set FFPROBE=C:\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffprobe.exe

echo.
echo ============================================================
echo  NEXIA - DIA DEL PADRE - 4 workers CPU paralelos
echo ============================================================

:: Limpiar temp files viejos
del /f /q "%CD%\swapped_*" 2>nul

:: Lanzar 4 workers independientes (CPU, sin DirectML = sin errores)
echo Lanzando 4 workers...
start "Worker-0" /min python "%SCRIPT%" --video "%CD%\chunk_00.mp4" --source1 "%BASE%\v1_anciano.jpg" --source2 "%BASE%\v2_gorra_roja.jpg" --source3 "%BASE%\v2_hijo_naranja.jpg" --output "%CD%\swapped_00.mp4" --fast
start "Worker-1" /min python "%SCRIPT%" --video "%CD%\chunk_01.mp4" --source1 "%BASE%\v1_anciano.jpg" --source2 "%BASE%\v2_gorra_roja.jpg" --source3 "%BASE%\v2_hijo_naranja.jpg" --output "%CD%\swapped_01.mp4" --fast
start "Worker-2" /min python "%SCRIPT%" --video "%CD%\chunk_02.mp4" --source1 "%BASE%\v1_anciano.jpg" --source2 "%BASE%\v2_gorra_roja.jpg" --source3 "%BASE%\v2_hijo_naranja.jpg" --output "%CD%\swapped_02.mp4" --fast
start "Worker-3" /min python "%SCRIPT%" --video "%CD%\chunk_03.mp4" --source1 "%BASE%\v1_anciano.jpg" --source2 "%BASE%\v2_gorra_roja.jpg" --source3 "%BASE%\v2_hijo_naranja.jpg" --output "%CD%\swapped_03.mp4" --fast

echo 4 workers en marcha. Esperando resultados...
echo (Los 4 chunks corren en paralelo usando todos los nucleos del Ryzen 7)
echo.

:: Esperar a que los 4 chunks esten completos (minimo 3MB cada uno)
:WAIT
timeout /t 60 /nobreak >nul
echo Revisando progreso...
if not exist "%CD%\swapped_00.mp4" goto WAIT
if not exist "%CD%\swapped_01.mp4" goto WAIT
if not exist "%CD%\swapped_02.mp4" goto WAIT
if not exist "%CD%\swapped_03.mp4" goto WAIT
for %%A in ("%CD%\swapped_00.mp4") do if %%~zA LSS 3000000 goto WAIT
for %%A in ("%CD%\swapped_01.mp4") do if %%~zA LSS 3000000 goto WAIT
for %%A in ("%CD%\swapped_02.mp4") do if %%~zA LSS 3000000 goto WAIT
for %%A in ("%CD%\swapped_03.mp4") do if %%~zA LSS 3000000 goto WAIT

echo [OK] Los 4 chunks completados. Uniendo video...

:: Concat list
echo file '%CD%\swapped_00.mp4' > "%CD%\concat.txt"
echo file '%CD%\swapped_01.mp4'>> "%CD%\concat.txt"
echo file '%CD%\swapped_02.mp4'>> "%CD%\concat.txt"
echo file '%CD%\swapped_03.mp4'>> "%CD%\concat.txt"

:: Join sin audio
"%FFMPEG%" -y -f concat -safe 0 -i "%CD%\concat.txt" -c copy "%CD%\joined.mp4" 2>nul

:: Mezclar audio original
set VIDEO=C:\Users\Romer\Downloads\WhatsApp Video 2026-06-20 at 4.03.42 PM.mp4
"%FFMPEG%" -y -i "%CD%\joined.mp4" -i "%VIDEO%" -c:v copy -c:a aac -b:a 128k -map 0:v:0 -map 1:a:0 -movflags +faststart -shortest "%OUT%" 2>nul

:: Cleanup
del /f /q "%CD%\*" 2>nul
rmdir "%CD%" 2>nul

echo.
echo ============================================================
echo  VIDEO LISTO: %OUT%
echo ============================================================
pause
