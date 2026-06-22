# Instalar n8n como servicio de Windows (arranca automatico con el PC)
# Ejecutar como Administrador

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Buscar ruta de node y n8n
$nodePath = (Get-Command node).Source
$n8nPath = "$env:APPDATA\npm\node_modules\n8n\bin\n8n"

Write-Host "Node: $nodePath"
Write-Host "n8n:  $n8nPath"

# Crear script de arranque
$startScript = @"
@echo off
set N8N_BASIC_AUTH_ACTIVE=false
set GENERIC_TIMEZONE=Europe/Madrid
set N8N_LOG_LEVEL=warn
set N8N_USER_FOLDER=D:\Proyectos claude\.n8n
"$nodePath" "$n8nPath" start
"@

$startScript | Out-File "D:\Proyectos claude\n8n-arrancar.bat" -Encoding ASCII
Write-Host "Creado: n8n-arrancar.bat"

# Instalar como tarea programada (alternativa a servicio, no requiere NSSM)
$action = New-ScheduledTaskAction -Execute "D:\Proyectos claude\n8n-arrancar.bat"
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit 0 -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest

Register-ScheduledTask -TaskName "n8n-agencia" -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force

Write-Host ""
Write-Host "n8n configurado para arrancar automaticamente al iniciar sesion."
Write-Host "Para iniciarlo ahora: Start-ScheduledTask -TaskName 'n8n-agencia'"
