# Setup del cerebro NEXIA en el servidor de USA
$py = "C:\Users\Owner\AppData\Local\Programs\Python\Python312\python.exe"

# 1. Ajustar rutas en todos los .py copiados (D:\Proyectos claude -> C:\nexia, y python path)
$old1 = "D:\Proyectos claude"; $new1 = "C:\nexia"
$old2 = "C:\Program Files\Python312\python.exe"; $new2 = $py
Get-ChildItem -Recurse C:\nexia -Filter *.py | ForEach-Object {
    $c = Get-Content $_.FullName -Raw
    $c = $c.Replace($old1, $new1).Replace($old2, $new2)
    [System.IO.File]::WriteAllText($_.FullName, $c)
}
Write-Output "1. Rutas ajustadas"

# 2. Arrancar Flask CRM (8080) si no responde
$flaskUp = $false
try { $flaskUp = (Invoke-WebRequest "http://127.0.0.1:8080/" -TimeoutSec 4 -UseBasicParsing).StatusCode -eq 200 } catch {}
if (-not $flaskUp) {
    Start-Process -FilePath $py -ArgumentList "C:\nexia\mundo-agencia\api\agencia-api.py" -WindowStyle Hidden
    Start-Sleep 5
    Write-Output "2. Flask CRM arrancado"
} else { Write-Output "2. Flask ya estaba arriba" }

# 3. Arrancar bot Telegram (matar instancia previa si la hay)
Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)" -ErrorAction SilentlyContinue).CommandLine -like "*telegram-bot*"
} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep 2
Start-Process -FilePath $py -ArgumentList "C:\nexia\mundo-agencia\herramientas\telegram-bot.py" -WindowStyle Hidden
Start-Sleep 3
Write-Output "3. Bot Telegram arrancado en USA"

# 4. Verificar
$f = $false
try { $f = (Invoke-WebRequest "http://127.0.0.1:8080/" -TimeoutSec 5 -UseBasicParsing).StatusCode -eq 200 } catch {}
Write-Output "Flask CRM: $(if($f){'VIVO'}else{'caido'})"
$bot = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)" -ErrorAction SilentlyContinue).CommandLine -like "*telegram-bot*"
}
Write-Output "Bot Telegram: $(if($bot){'corriendo PID '+$bot.Id}else{'no corre'})"
Write-Output "setup-done"
