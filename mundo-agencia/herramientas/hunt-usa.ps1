# Caza de leads desde el servidor de USA (IP fresca, sin limites de OSM)
param([string]$nicho = "restaurantes", [string]$ciudad = "Miami", [string]$pais = "USA", [int]$limite = 40)
$py = "C:\Users\Owner\AppData\Local\Programs\Python\Python312\python.exe"
Set-Location C:\nexia\mundo-ventas\herramientas
& $py scraper-leads.py --nicho $nicho --ciudad $ciudad --pais $pais --solo-con-web --enriquecer --clasificar --limite $limite
