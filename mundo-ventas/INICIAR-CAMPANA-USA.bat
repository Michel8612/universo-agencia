@echo off
REM ================================================================
REM  NEXIA - Campana de leads USA 24/7 (servidor)
REM  Deja esta ventana abierta (o programala con Task Scheduler).
REM  Auto-reinicio si el proceso terminara por cualquier causa.
REM  Log: mundo-ventas\campana-usa.log
REM ================================================================
cd /d "%~dp0herramientas"
:loop
echo [%date% %time%] Iniciando campana USA... >> "..\campana-usa.log"
python campana-usa.py >> "..\campana-usa.log" 2>&1
echo [%date% %time%] Proceso terminado. Reiniciando en 60s... >> "..\campana-usa.log"
timeout /t 60 /nobreak >nul
goto loop
