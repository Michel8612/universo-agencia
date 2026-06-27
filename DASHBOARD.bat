@echo off
REM NEXIA - Dashboard del Universo (Node.js). Doble clic para abrir.
start "" "C:\Program Files\nodejs\node.exe" "D:\Proyectos claude\dashboard\server.js"
timeout /t 2 >nul
start "" http://127.0.0.1:3000
