@echo off
echo ========================================
echo  NEXIA - Deploy a Netlify
echo ========================================
echo.
echo OPCION 1 (automatica): Login + deploy
echo.

cd /d "D:\Proyectos claude\mundo-ventas\web-nexia"

echo Haciendo build de produccion...
call npm run build

echo.
echo Abriendo navegador para login (solo primera vez)...
npx -y netlify-cli login

echo.
echo Desplegando a produccion...
npx netlify-cli deploy --dir out --prod

echo.
echo Si es la primera vez, te preguntara: "Create & configure a new site"
echo Elige: Yes > Tu equipo > Nombre: nexia-ia
echo.
pause
