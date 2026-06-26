# Re-aplica rutas al bot, lo reinicia y verifica que sobreviva
$py = "C:\Users\Owner\AppData\Local\Programs\Python\Python312\python.exe"
$bot = "C:\nexia\mundo-agencia\herramientas\telegram-bot.py"

# 1. Ajustar rutas en el bot recien copiado (UTF-8 seguro para no romper emojis)
$c = Get-Content $bot -Raw -Encoding UTF8
$c = $c.Replace("D:\Proyectos claude", "C:\nexia").Replace("C:\Program Files\Python312\python.exe", $py)
$utf8 = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($bot, $c, $utf8)
Write-Output "1. Rutas del bot ajustadas (UTF-8)"

# 2. Matar instancias previas
Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)" -ErrorAction SilentlyContinue).CommandLine -like "*telegram-bot*"
} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep 2

# 3. Arrancar y verificar que sigue vivo tras 8s (si crashea, lo veremos)
Start-Process -FilePath $py -ArgumentList $bot -WindowStyle Hidden
Start-Sleep 8
$p = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)" -ErrorAction SilentlyContinue).CommandLine -like "*telegram-bot*"
}
if ($p) { Write-Output "2. Bot VIVO tras 8s (PID $($p.Id)) - OK" }
else {
    Write-Output "2. Bot SE CAYO - corriendo en foreground para ver el error:"
    & $py $bot 2>&1 | Select-Object -First 15
}
