# CLOUDFLARE TUNNEL para n8n NEXIA
# Lanza un túnel temporal y guarda la URL en tunnel-url.txt

$LOG = "D:\Proyectos claude\tunnel-url.txt"
$CF_LOG = "D:\Proyectos claude\tunnel-output.log"

# 1. Verificar si cloudflared existe
$cfPath = $null
$candidates = @(
    "C:\Program Files\Cloudflare\cloudflared\cloudflared.exe",
    "C:\Users\Romer\AppData\Local\Microsoft\WinGet\Packages\Cloudflare.cloudflared_Microsoft.Winget.Source_8wekyb3d8bbwe\cloudflared.exe",
    (Get-Command cloudflared -ErrorAction SilentlyContinue)?.Source
)

foreach ($c in $candidates) {
    if ($c -and (Test-Path $c)) {
        $cfPath = $c
        break
    }
}

# Buscar en PATH también
if (-not $cfPath) {
    try {
        $found = & where.exe cloudflared 2>$null
        if ($found) { $cfPath = $found[0] }
    } catch {}
}

if (-not $cfPath) {
    "cloudflared NO encontrado - instalando con winget..." | Out-File $LOG
    & winget install Cloudflare.cloudflared --accept-source-agreements --accept-package-agreements 2>&1 | Out-File "D:\Proyectos claude\winget-cf.log"

    # Intentar encontrar de nuevo
    Start-Sleep -Seconds 5
    try {
        $found = & where.exe cloudflared 2>$null
        if ($found) { $cfPath = $found[0] }
    } catch {}

    if (-not $cfPath) {
        "ERROR: No se pudo instalar cloudflared. Instala manualmente desde: https://github.com/cloudflare/cloudflared/releases" | Out-File $LOG
        exit 1
    }
}

"cloudflared encontrado en: $cfPath" | Out-File $LOG -Append

# 2. Lanzar el túnel y capturar output
"Lanzando tunel hacia http://127.0.0.1:5678 ..." | Out-File $LOG -Append

# Vaciar log de output anterior
"" | Out-File $CF_LOG

# Lanzar en proceso separado redirigiendo stderr (donde cloudflared escribe la URL)
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $cfPath
$psi.Arguments = "tunnel --url http://127.0.0.1:5678"
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.UseShellExecute = $false
$psi.CreateNoWindow = $true

$process = New-Object System.Diagnostics.Process
$process.StartInfo = $psi

# Capturar output asíncrono
$outputData = New-Object System.Collections.Concurrent.ConcurrentBag[string]
$process.OutputDataReceived += { if ($_.Data) { $outputData.Add($_.Data); $_.Data | Add-Content $CF_LOG } }
$process.ErrorDataReceived += { if ($_.Data) { $outputData.Add($_.Data); $_.Data | Add-Content $CF_LOG } }

$process.Start() | Out-Null
$process.BeginOutputReadLine()
$process.BeginErrorReadLine()

# Guardar PID para poder matar el proceso después
$process.Id | Out-File "D:\Proyectos claude\tunnel.pid"
"PID del tunel: $($process.Id)" | Out-File $LOG -Append

# 3. Esperar hasta encontrar la URL (máx 30 seg)
$url = $null
$maxWait = 30
$elapsed = 0

while (-not $url -and $elapsed -lt $maxWait) {
    Start-Sleep -Seconds 2
    $elapsed += 2

    $lines = Get-Content $CF_LOG -ErrorAction SilentlyContinue
    foreach ($line in $lines) {
        if ($line -match "https://[a-z0-9-]+\.trycloudflare\.com") {
            $url = $matches[0]
            break
        }
    }
}

if ($url) {
    $webhook = "$url/webhook/lead-nexia"
    "URL PUBLICA: $url" | Out-File $LOG -Append
    "WEBHOOK_URL: $webhook" | Out-File $LOG -Append
    "ESTADO: TUNEL ACTIVO" | Out-File $LOG -Append
    Write-Host "TUNEL ACTIVO: $url"
    Write-Host "Webhook: $webhook"

    # Publicar el webhook en la web: reescribe n8n-config.json y hace push.
    # Netlify redeploya solo (auto-deploy en cada push a main) -> el formulario
    # de la web live empieza a disparar el funnel en ~2 min.
    $cfgFile = "D:\Proyectos claude\mundo-ventas\web-nexia\public\n8n-config.json"
    $json = @{
        webhook = $webhook
        _nota   = "Generado por CLOUDFLARE-TUNNEL.ps1. Cambia en cada reinicio del tunel."
    } | ConvertTo-Json
    $json | Out-File -FilePath $cfgFile -Encoding utf8

    Push-Location "D:\Proyectos claude"
    try {
        & git add "mundo-ventas/web-nexia/public/n8n-config.json" 2>&1 | Out-File $LOG -Append
        & git commit -m "chore: actualizar webhook del tunel n8n ($url)" 2>&1 | Out-File $LOG -Append
        & git push 2>&1 | Out-File $LOG -Append
        "PUSH OK: webhook publicado en la web (Netlify redeploya solo)" | Out-File $LOG -Append
        Write-Host "Webhook publicado en la web. Netlify redeploya en ~2 min."
    } catch {
        "AVISO: no se pudo hacer push automatico: $_" | Out-File $LOG -Append
        Write-Host "AVISO: tunel activo pero no se pudo hacer push. Hazlo manual o revisa $LOG"
    } finally {
        Pop-Location
    }
} else {
    "ERROR: No se encontro URL en $maxWait segundos. Revisa tunnel-output.log" | Out-File $LOG -Append
    Write-Host "ERROR: Timeout esperando URL del tunel. Revisa D:\Proyectos claude\tunnel-output.log"
}
