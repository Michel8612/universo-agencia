# Instala el watchdog 24/7 en el servidor de USA (mantiene Flask CRM + Bot Telegram vivos)
$py = "C:\Users\Owner\AppData\Local\Programs\Python\Python312\python.exe"

# 1. Crear el watchdog
$wd = @'
$py = "C:\Users\Owner\AppData\Local\Programs\Python\Python312\python.exe"
function Up($url){ try { return (Invoke-WebRequest $url -TimeoutSec 4 -UseBasicParsing).StatusCode -eq 200 } catch { return $false } }
if (-not (Up "http://127.0.0.1:8080/")) {
    Start-Process -FilePath $py -ArgumentList "C:\nexia\mundo-agencia\api\agencia-api.py" -WindowStyle Hidden
}
$bot = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)" -ErrorAction SilentlyContinue).CommandLine -like "*telegram-bot*"
}
if (-not $bot) {
    Start-Process -FilePath $py -ArgumentList "C:\nexia\mundo-agencia\herramientas\telegram-bot.py" -WindowStyle Hidden
}
'@
[System.IO.File]::WriteAllText("C:\nexia\watchdog-usa.ps1", $wd)
Write-Output "1. Watchdog creado"

# 2. Registrar tarea: al logon + cada 5 minutos
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File C:\nexia\watchdog-usa.ps1"
$tLogon = New-ScheduledTaskTrigger -AtLogOn
$tRepeat = New-ScheduledTaskTrigger -Once -At (Get-Date "2026-01-01T00:00:00") -RepetitionInterval (New-TimeSpan -Minutes 5)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 4)
Register-ScheduledTask -TaskName "nexia-watchdog" -Action $action -Trigger @($tLogon, $tRepeat) -Settings $settings -Force | Out-Null
Write-Output "2. Tarea nexia-watchdog registrada (logon + cada 5 min)"

# 3. Daily campaign (08:00) para llenar el CRM solo
$pyArg = "C:\nexia\mundo-ventas\herramientas\campana-leads.py --combos 12 --por-combo 4 --sin-email"
$actCamp = New-ScheduledTaskAction -Execute $py -Argument $pyArg -WorkingDirectory "C:\nexia\mundo-ventas\herramientas"
$tCamp = New-ScheduledTaskTrigger -Daily -At 8am
$setCamp = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 60)
Register-ScheduledTask -TaskName "nexia-campana-leads" -Action $actCamp -Trigger $tCamp -Settings $setCamp -Force | Out-Null
Write-Output "3. Campana diaria registrada (08:00)"
Write-Output "autostart-done"
