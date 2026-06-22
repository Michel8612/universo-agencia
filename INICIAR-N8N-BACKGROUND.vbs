Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c """ & Chr(34) & "C:\Users\Romer\AppData\Roaming\npm\n8n.cmd" & Chr(34) & " start > C:\Users\Romer\AppData\Local\n8n.log 2>&1""", 0, False
