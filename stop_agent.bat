@echo off
taskkill /F /IM pythonw.exe /T 2>nul
echo GameZone Agent stopped.
timeout /t 2 >nul
