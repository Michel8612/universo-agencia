# Despliega el bot de leads en USA + actualiza el watchdog (Flask + bot mando + bot leads)
$py = "C:\Users\Owner\AppData\Local\Programs\Python\Python312\python.exe"

# 1. Watchdog actualizado: mantiene Flask + bot de mando + bot de leads
$wd = @'
$py = "C:\Users\Owner\AppData\Local\Programs\Python\Python312\python.exe"
function Up($u){ try { return (Invoke-WebRequest $u -TimeoutSec 4 -UseBasicParsing).StatusCode -eq 200 } catch { return $false } }
function Corre($patron){ Get-Process python -ErrorAction SilentlyContinue | Where-Object { (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)" -ErrorAction SilentlyContinue).CommandLine -like $patron } }
if (-not (Up "http://127.0.0.1:8080/")) { Start-Process -FilePath $py -ArgumentList "C:\nexia\mundo-agencia\api\agencia-api.py" -WindowStyle Hidden }
if (-not (Corre "*telegram-bot.py*")) { Start-Process -FilePath $py -ArgumentList "C:\nexia\mundo-agencia\herramientas\telegram-bot.py" -WindowStyle Hidden }
if (-not (Corre "*bot-leads-telegram*")) { Start-Process -FilePath $py -ArgumentList "C:\nexia\mundo-agencia\herramientas\bot-leads-telegram.py" -WindowStyle Hidden }
'@
[System.IO.File]::WriteAllText("C:\nexia\watchdog-usa.ps1", $wd)
Write-Output "1. Watchdog actualizado (Flask + 2 bots)"

# 2. Arrancar el bot de leads (matar previo si lo hubiera)
Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)" -ErrorAction SilentlyContinue).CommandLine -like "*bot-leads-telegram*"
} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep 2
Start-Process -FilePath $py -ArgumentList "C:\nexia\mundo-agencia\herramientas\bot-leads-telegram.py" -WindowStyle Hidden
Start-Sleep 8

# 3. Verificar
$p = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)" -ErrorAction SilentlyContinue).CommandLine -like "*bot-leads-telegram*"
}
if ($p) { Write-Output "2. Bot de leads VIVO tras 8s (PID $($p.Id)) - OK" }
else {
    Write-Output "2. Bot de leads SE CAYO - foreground para ver error:"
    & $py "C:\nexia\mundo-agencia\herramientas\bot-leads-telegram.py" 2>&1 | Select-Object -First 12
}
Write-Output "deploy-leadbot-done"
