@echo off
set BASE=D:\Proyectos claude\mundo-multimedia\proyectos\face-swap
set V1=%BASE%\video1_trigueño_abuelo.mp4
set SCRIPT=D:\Proyectos claude\mundo-multimedia\herramientas\face_swap_video.py
set VIDEO=C:\Users\Romer\Downloads\WhatsApp Video 2026-06-20 at 4.03.42 PM.mp4

echo Esperando que termine Video 1...

:WAIT
if not exist "%V1%" goto WAIT_SLEEP
for %%A in ("%V1%") do if %%~zA LSS 5000000 goto WAIT_SLEEP
:: Video 1 existe y pesa mas de 5 MB = completado
goto START_V2

:WAIT_SLEEP
timeout /t 60 /nobreak >nul
goto WAIT

:START_V2
echo.
echo [OK] Video 1 completado. Iniciando Video 2...
echo.

python "%SCRIPT%" ^
  --video "%VIDEO%" ^
  --source1 "%BASE%\v2_hijo_naranja.jpg" ^
  --source2 "%BASE%\v2_gorra_roja.jpg" ^
  --output  "%BASE%\video2_naranja_gorraroja.mp4" ^
  --fast

echo.
echo ============================================
echo  AMBOS VIDEOS COMPLETADOS
echo  Video 1: %V1%
echo  Video 2: %BASE%\video2_naranja_gorraroja.mp4
echo ============================================
pause
