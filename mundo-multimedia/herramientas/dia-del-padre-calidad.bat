@echo off
:: ESPECIAL DIA DEL PADRE — Calidad maxima
:: Personas: EL PADRE (anciano gafas) + Hijo gorra roja
:: Sin --fast: resolucion completa, todos los frames = swap mas natural

set BASE=D:\Proyectos claude\mundo-multimedia\proyectos\face-swap
set SCRIPT=D:\Proyectos claude\mundo-multimedia\herramientas\face_swap_video.py
set VIDEO=C:\Users\Romer\Downloads\WhatsApp Video 2026-06-20 at 4.03.42 PM.mp4
set OUT=%BASE%\dia_padre_calidad.mp4

echo.
echo ============================================================
echo  NEXIA — ESPECIAL DIA DEL PADRE (Calidad Maxima)
echo  EL PADRE (anciano) + Hijo gorra roja
echo  Sin compresion de resolucion, todos los frames procesados
echo  ETA: 3-4 horas (vale la pena, queda perfecto)
echo ============================================================
echo.

python "%SCRIPT%" ^
  --video   "%VIDEO%" ^
  --source1 "%BASE%\v1_anciano.jpg" ^
  --source2 "%BASE%\v2_gorra_roja.jpg" ^
  --output  "%OUT%" ^
  --scale   1.0 ^
  --skip    1 ^
  --det     640

echo.
echo ============================================================
echo  LISTO: %OUT%
echo  Musica: la del video original (sin cambios)
echo  Faces: embedding matching — sin confusion de identidades
echo ============================================================
pause
