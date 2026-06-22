@echo off
title n8n Agencia IA - NO CERRAR ESTA VENTANA
color 0A

echo.
echo  ================================
echo   n8n AGENCIA IA - ARRANCANDO
echo  ================================
echo.
echo  NO CIERRES ESTA VENTANA
echo  Abre en Edge: http://localhost:5678
echo.

set N8N_BASIC_AUTH_ACTIVE=false
set GENERIC_TIMEZONE=Europe/Madrid
set N8N_LOG_LEVEL=warn

"C:\Program Files\nodejs\node.exe" "C:\Users\Romer\AppData\Roaming\npm\node_modules\n8n\bin\n8n" start

pause
