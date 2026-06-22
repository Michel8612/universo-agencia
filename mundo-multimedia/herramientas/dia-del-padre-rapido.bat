@echo off
:: ESPECIAL DIA DEL PADRE — GPU DirectML + 4 chunks paralelos + 3 personas
:: ETA estimada: 10-20 min con AMD GPU integrada

set BASE=D:\Proyectos claude\mundo-multimedia\proyectos\face-swap
set SCRIPT=D:\Proyectos claude\mundo-multimedia\herramientas\face_swap_rapido.py
set VIDEO=C:\Users\Romer\Downloads\WhatsApp Video 2026-06-20 at 4.03.42 PM.mp4
set OUT=%BASE%\dia_padre_final.mp4

echo.
echo ============================================================
echo  NEXIA — DIA DEL PADRE
echo  3 personas: El Padre + Hijo gorra roja + Pelado naranja
echo  GPU DirectML (AMD) + 4 chunks paralelos
echo  ETA: ~10-20 minutos
echo ============================================================
echo.

python "%SCRIPT%" ^
  --video   "%VIDEO%" ^
  --source1 "%BASE%\v1_anciano.jpg" ^
  --source2 "%BASE%\v2_gorra_roja.jpg" ^
  --source3 "%BASE%\v2_hijo_naranja.jpg" ^
  --output  "%OUT%" ^
  --workers 4 ^
  --gpu

echo.
echo ============================================================
echo  Resultado: %OUT%
echo ============================================================
pause
