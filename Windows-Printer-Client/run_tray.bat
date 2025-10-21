@echo off
REM Run Print Client Pro in system tray
echo Starting Print Client Pro...

REM Get the current directory
set CURRENT_DIR=%~dp0

REM Run the tray application (hidden)
start /B "" "%CURRENT_DIR%venv\Scripts\pythonw.exe" "%CURRENT_DIR%printer_client_tray.py"

echo Print Client Pro is now running in the system tray.
echo Look for the printer icon in your system tray (bottom-right corner).
echo.
timeout /t 3
