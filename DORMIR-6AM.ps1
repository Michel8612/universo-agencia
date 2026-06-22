Add-Type -Name PowerMgmt -Namespace Win32 -MemberDefinition '[DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint esFlags);'

[Win32.PowerMgmt]::SetThreadExecutionState(0x80000003) | Out-Null

$objetivo = (Get-Date).Date.AddHours(6)
if ((Get-Date) -gt $objetivo) { $objetivo = $objetivo.AddDays(1) }

$min = [math]::Round(($objetivo - (Get-Date)).TotalMinutes)
Write-Host "Laptop despierta hasta las 6:00 AM. Faltan $min minutos. No cierres esta ventana."

while ((Get-Date) -lt $objetivo) {
    $restantes = [math]::Round(($objetivo - (Get-Date)).TotalMinutes)
    Write-Host "$(Get-Date -Format 'HH:mm') - Faltan $restantes min..."
    Start-Sleep -Seconds 60
}

Write-Host "Son las 6:00 AM. Cerrando Ollama y apagando..."

$proc = Get-Process -Name ollama -ErrorAction SilentlyContinue
if ($proc) {
    Stop-Process -Name ollama -Force
    Write-Host "Ollama detenido. Mañana: ollama pull qwen2.5:14b para reanudar."
}

Start-Sleep -Seconds 10
Stop-Computer -Force
