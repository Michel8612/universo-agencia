@echo off
:: Re-hace Video 2 con el fix de embeddings
:: Matching por identidad biométrica — sin confusión de caras por posición

set BASE=D:\Proyectos claude\mundo-multimedia\proyectos\face-swap
set SCRIPT=D:\Proyectos claude\mundo-multimedia\herramientas\face_swap_video.py
set VIDEO=C:\Users\Romer\Downloads\WhatsApp Video 2026-06-20 at 4.03.42 PM.mp4
set OUT=%BASE%\video2_naranja_gorraroja.mp4

echo.
echo ============================================
echo  NEXIA — Re-haciendo Video 2 con FIX
echo  Personas: naranja + gorra roja
echo ============================================
echo.

python "%SCRIPT%" ^
  --video "%VIDEO%" ^
  --source1 "%BASE%\v2_hijo_naranja.jpg" ^
  --source2 "%BASE%\v2_gorra_roja.jpg" ^
  --output  "%OUT%" ^
  --fast

echo.
echo ============================================
echo  VIDEO 2 COMPLETADO con fix de identidad
echo  Resultado: %OUT%
echo ============================================
pause
