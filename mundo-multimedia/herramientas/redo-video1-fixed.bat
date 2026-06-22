@echo off
:: Re-hace Video 1 con el fix de embeddings
:: El anciano ya NO recibirá la cara del joven (matching por identidad biométrica, no posición)

set BASE=D:\Proyectos claude\mundo-multimedia\proyectos\face-swap
set SCRIPT=D:\Proyectos claude\mundo-multimedia\herramientas\face_swap_video.py
set VIDEO=C:\Users\Romer\Downloads\WhatsApp Video 2026-06-20 at 4.03.42 PM.mp4
set OUT=%BASE%\video1_trigueño_abuelo.mp4

echo.
echo ============================================
echo  NEXIA — Re-haciendo Video 1 con FIX
echo  Fix: matching por embedding (no posicion)
echo  Cada cara detectada -> mas similar al source
echo ============================================
echo.
echo Output: %OUT%
echo.

python "%SCRIPT%" ^
  --video "%VIDEO%" ^
  --source1 "%BASE%\v1_joven_trigueño.jpg" ^
  --source2 "%BASE%\v1_anciano.jpg" ^
  --output  "%OUT%" ^
  --fast

echo.
echo ============================================
echo  VIDEO 1 COMPLETADO con fix de identidad
echo  Resultado: %OUT%
echo ============================================
pause
