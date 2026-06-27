# NEXIA — Migrar n8n nativo -> Docker (mas estable, auto-reinicio)
# Ejecutar UNA vez (clic derecho > Ejecutar con PowerShell, o: powershell -ExecutionPolicy Bypass -File n8n-a-docker.ps1)
# Nota: la primera vez descarga la imagen de n8n (~1GB) con tu conexion.

Write-Host "1. Desactivando el watchdog del n8n nativo (para que no pelee con Docker)..."
try { Disable-ScheduledTask -TaskName "n8n-agencia" -ErrorAction Stop | Out-Null; Write-Host "   tarea n8n-agencia desactivada" }
catch { Write-Host "   (no habia tarea n8n-agencia, ok)" }

Write-Host "2. Parando n8n nativo (libera el puerto 5678)..."
Get-Process node -ErrorAction SilentlyContinue | Where-Object {
    (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)" -ErrorAction SilentlyContinue).CommandLine -like "*n8n*"
} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep 3

Write-Host "3. Arrancando n8n en Docker..."
Set-Location "D:\Proyectos claude"
docker compose up -d
Start-Sleep 12
docker compose ps
Write-Host ""
Write-Host "LISTO. n8n en Docker (se reinicia solo). Abre: http://127.0.0.1:5678"
Write-Host "Tus workflows se conservan (se monto tu carpeta C:\Users\Romer\.n8n)."
Write-Host "Si el puerto 5678 no responde en 1 min, mira: docker compose logs -f"
