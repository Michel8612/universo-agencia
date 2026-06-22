# ============================================================
# ARRANCAR AGENCIA IA — Un solo script para levantar todo
# Ejecutar: powershell -ExecutionPolicy Bypass -File arrancar-agencia.ps1
# ============================================================

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
$BASE = "D:\Proyectos claude"

Write-Host "`n🚀 ARRANCANDO AGENCIA IA..." -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# 1. Verificar Docker
Write-Host "`n[1/4] Verificando Docker..." -ForegroundColor Yellow
$dockerOk = docker info 2>&1 | Select-String "Server Version"
if (-not $dockerOk) {
    Write-Host "❌ Docker no está corriendo. Ábrelo primero." -ForegroundColor Red
    Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    Write-Host "   Abriendo Docker Desktop... espera 30 segundos y vuelve a ejecutar este script." -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ Docker OK" -ForegroundColor Green

# 2. Levantar servicios con Docker Compose
Write-Host "`n[2/4] Levantando servicios (n8n + Ollama + Redis)..." -ForegroundColor Yellow
$composeFile = "$BASE\mundo-ventas\web-agencia\docker-compose.yml"
docker compose -f $composeFile up -d 2>&1 | Select-String "Started|Running|Created|Error"

Start-Sleep 5

# 3. Descargar modelo Ollama si no existe
Write-Host "`n[3/4] Verificando modelo IA local (qwen2.5-coder:7b)..." -ForegroundColor Yellow
$modelExists = docker exec ollama_agencia ollama list 2>&1 | Select-String "qwen2.5-coder"
if (-not $modelExists) {
    Write-Host "   Descargando modelo (4GB, primera vez, tarda ~10 min)..." -ForegroundColor Yellow
    docker exec ollama_agencia ollama pull qwen2.5-coder:7b
} else {
    Write-Host "✅ Modelo qwen2.5-coder ya disponible" -ForegroundColor Green
}

# 4. Abrir VS Code
Write-Host "`n[4/4] Abriendo VS Code con el Universo..." -ForegroundColor Yellow
$vscode = "C:\Program Files\Microsoft VS Code\Code.exe"
if (Test-Path $vscode) { Start-Process $vscode -ArgumentList "`"$BASE`"" }

# Resumen
Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "✅ AGENCIA IA LISTA" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  n8n:         http://localhost:5678" -ForegroundColor White
Write-Host "  Ollama IA:   http://localhost:11434" -ForegroundColor White
Write-Host "  Base datos:  localhost:5432" -ForegroundColor White
Write-Host "  Redis:       localhost:6379" -ForegroundColor White
Write-Host "`n  VS Code abierto con todos los mundos." -ForegroundColor White
Write-Host "  Habla con Claude Code desde VS Code para activar cualquier agente.`n" -ForegroundColor White
