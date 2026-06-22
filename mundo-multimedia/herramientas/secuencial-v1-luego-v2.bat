@echo off
set BASE=D:\Proyectos claude\mundo-multimedia\proyectos\face-swap
set SCRIPT=D:\Proyectos claude\mundo-multimedia\herramientas\face_swap_video.py
set VIDEO=C:\Users\Romer\Downloads\WhatsApp Video 2026-06-20 at 4.03.42 PM.mp4

echo ============================================
echo  NEXIA — Video 1 + Video 2 secuencial
echo  Fix: embedding similarity (no posicion)
echo ============================================
echo.

:: ---- VIDEO 1 ----
echo [1/2] Procesando Video 1 (joven + anciano)...
python "%SCRIPT%" ^
  --video "%VIDEO%" ^
  --source1 "%BASE%\v1_joven_trigueño.jpg" ^
  --source2 "%BASE%\v1_anciano.jpg" ^
  --output  "%BASE%\video1_trigueño_abuelo.mp4" ^
  --fast

if errorlevel 1 (
    echo [ERROR] Video 1 fallo. Revisa la ventana.
    pause
    exit /b 1
)

echo.
echo [OK] Video 1 listo! Iniciando Video 2...
echo.

:: ---- VIDEO 2 ----
echo [2/2] Procesando Video 2 (naranja + gorra roja)...
python "%SCRIPT%" ^
  --video "%VIDEO%" ^
  --source1 "%BASE%\v2_hijo_naranja.jpg" ^
  --source2 "%BASE%\v2_gorra_roja.jpg" ^
  --output  "%BASE%\video2_naranja_gorraroja.mp4" ^
  --fast

echo.
echo ============================================
echo  AMBOS VIDEOS COMPLETADOS con fix embedding
echo  V1: %BASE%\video1_trigueño_abuelo.mp4
echo  V2: %BASE%\video2_naranja_gorraroja.mp4
echo ============================================
pause
