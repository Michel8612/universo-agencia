# ============================================
# INICIAR AGENCIA IA — Script de arranque
# Ejecutar como: powershell -File "iniciar-agencia.ps1"
# ============================================

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Cargar variables de entorno si existe .env
$envFile = "$PSScriptRoot\.env"
if (Test-Path $envFile) {
    Get-Content $envFile | Where-Object { $_ -match "^[A-Z]" -and $_ -notmatch "^#" } | ForEach-Object {
        $parts = $_ -split "=", 2
        [System.Environment]::SetEnvironmentVariable($parts[0].Trim(), $parts[1].Trim(), "Process")
    }
    Write-Host "✅ Variables de entorno cargadas"
}

# Arrancar n8n en background
Write-Host "🚀 Iniciando n8n en http://localhost:5678 ..."
Start-Process powershell -ArgumentList "-NoExit -Command `"n8n start`"" -WindowStyle Minimized

Start-Sleep 3

# Abrir VS Code con el Universo
Write-Host "📂 Abriendo VS Code con el Universo..."
Start-Process "C:\Program Files\Microsoft VS Code\Code.exe" -ArgumentList "`"$PSScriptRoot`""

Write-Host ""
Write-Host "✅ Agencia IA lista:"
Write-Host "   → n8n:     http://localhost:5678"
Write-Host "   → VS Code: abierto con el Universo"
Write-Host ""
Write-Host "Recuerda: Claude Code desde VS Code tiene acceso a todos los mundos."
