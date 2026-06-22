@echo off
echo ================================================
echo  NEXIA - Esperar face-swap y generar contenido
echo ================================================
echo.
echo El face-swap esta en proceso. Este script espera
echo a que termine y luego genera los 35 posts.
echo.

:WAIT_LOOP
if exist "D:\Proyectos claude\mundo-multimedia\proyectos\face-swap\video1_trigueño_abuelo.mp4" (
    for %%A in ("D:\Proyectos claude\mundo-multimedia\proyectos\face-swap\video1_trigueño_abuelo.mp4") do (
        if %%~zA GTR 1000000 goto DONE_WAITING
    )
)
echo [%time%] Face-swap aun en proceso... esperando 2 min
timeout /t 120 /nobreak >nul
goto WAIT_LOOP

:DONE_WAITING
echo.
echo [OK] Face-swap completado. Iniciando generacion de contenido...
echo.
python "D:\Proyectos claude\mundo-social-media\herramientas\generar-contenido-lanzamiento.py"
echo.
echo ================================================
echo  Contenido generado en:
echo  D:\Proyectos claude\mundo-social-media\contenido-nexia\
echo ================================================
pause
