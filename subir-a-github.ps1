# ============================================================
# UNIVERSO AGENCIA — Subir proyecto a GitHub
# Ejecutar UNA sola vez desde PowerShell como Administrador
# ============================================================

$TOKEN = "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"
$REPO_NAME = "universo-agencia"
$PROYECTO = "D:\Proyectos claude"

Write-Host "`n[1/4] Creando repositorio privado en GitHub..." -ForegroundColor Cyan

$body = @{
    name        = $REPO_NAME
    description = "Agencia de IA completa - mundos especializados, automatizaciones y servicios"
    private     = $true
    auto_init   = $false
} | ConvertTo-Json

$headers = @{
    Authorization = "token $TOKEN"
    Accept        = "application/vnd.github.v3+json"
}

try {
    $response = Invoke-RestMethod -Uri "https://api.github.com/user/repos" `
        -Method POST -Headers $headers -Body $body -ContentType "application/json"
    $repoUrl = $response.clone_url
    $username = $response.owner.login
    Write-Host "   Repositorio creado: $repoUrl" -ForegroundColor Green
} catch {
    $errorMsg = $_.ErrorDetails.Message | ConvertFrom-Json
    if ($errorMsg.errors[0].message -like "*already exists*") {
        Write-Host "   El repo ya existe, usando el existente..." -ForegroundColor Yellow
        # Obtener username del token
        $me = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers
        $username = $me.login
        $repoUrl = "https://github.com/$username/$REPO_NAME.git"
    } else {
        Write-Host "   Error: $_" -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n[2/4] Inicializando repositorio Git local..." -ForegroundColor Cyan
Set-Location $PROYECTO
git init
git config user.name "michel"
git config user.email "michelmiranda683@gmail.com"
Write-Host "   Git inicializado" -ForegroundColor Green

Write-Host "`n[3/4] Preparando archivos y haciendo primer commit..." -ForegroundColor Cyan
git add .
git commit -m "feat: primer commit - universo agencia IA completa"
Write-Host "   Commit listo" -ForegroundColor Green

Write-Host "`n[4/4] Subiendo a GitHub..." -ForegroundColor Cyan
# Insertar token en la URL para autenticación HTTPS
$remoteUrl = "https://$($TOKEN)@github.com/$username/$REPO_NAME.git"
git branch -M main
git remote add origin $remoteUrl
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n LISTO! Proyecto subido a:" -ForegroundColor Green
    Write-Host "   https://github.com/$username/$REPO_NAME" -ForegroundColor Yellow
    Write-Host "`n Ahora puedes clonar desde cualquier dispositivo con:" -ForegroundColor Cyan
    Write-Host "   git clone https://github.com/$username/$REPO_NAME.git" -ForegroundColor White

    # Borrar el token del remote para no dejarlo expuesto
    git remote set-url origin "https://github.com/$username/$REPO_NAME.git"
    Write-Host "`n[Seguridad] Token removido del remote URL." -ForegroundColor DarkGray
} else {
    Write-Host "`n Error al hacer push. Revisa tu conexion o el token." -ForegroundColor Red
}

# Borrar este script tras ejecutarse (opcional, descomenta si quieres)
# Remove-Item $MyInvocation.MyCommand.Path
