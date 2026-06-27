@echo off
set LOG=D:\Proyectos claude\build-nexia.log
echo === BUILD NEXIA %date% %time% === > "%LOG%"
echo Directorio: D:\Proyectos claude\mundo-ventas\web-nexia >> "%LOG%"
cd /d "D:\Proyectos claude\mundo-ventas\web-nexia"
echo Iniciando npm run build... >> "%LOG%"
"C:\Program Files\nodejs\npm.cmd" run build >> "%LOG%" 2>&1
echo. >> "%LOG%"
echo === FIN BUILD %date% %time% === >> "%LOG%"
