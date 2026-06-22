@echo off
echo Sincronizando entregables con Google Drive NEXIA...
set RCLONE="C:\Users\Romer\AppData\Local\rclone\rclone.exe"
set LOCAL="D:\Proyectos claude\mundo-multimedia\proyectos"
set REMOTE=gdrive-nexia:NEXIA-Agencia/Entregables

%RCLONE% copy %LOCAL% %REMOTE% --progress --exclude "**\debug_*" --exclude "**\*.onnx"
echo.
echo Sincronizacion completada.
pause
