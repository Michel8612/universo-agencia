@echo off
REM NEXIA - Panel de control local. Doble clic para abrir.
start "" "C:\Program Files\Python312\python.exe" "D:\Proyectos claude\panel.py"
timeout /t 2 >nul
start "" http://127.0.0.1:8090
