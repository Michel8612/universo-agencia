@echo off
echo ========================================
echo  NEXIA — Conectar Google Drive
echo ========================================
echo.
echo PASOS:
echo 1. Se abrira el navegador para autenticarte
echo 2. Inicia sesion con el email de la agencia (hola@nexia.io o similar)
echo 3. Autoriza el acceso de rclone
echo 4. Vuelve aqui y pulsa ENTER
echo.
echo Necesitas haber creado antes la cuenta Google de la agencia.
echo.
pause

"C:\Users\Romer\AppData\Local\rclone\rclone.exe" config create gdrive-nexia drive ^
  --drive-use-trash=false ^
  --drive-acknowledge-abuse=true

echo.
echo Si la autenticacion fue bien, prueba con:
echo   rclone ls gdrive-nexia:
echo.
pause
