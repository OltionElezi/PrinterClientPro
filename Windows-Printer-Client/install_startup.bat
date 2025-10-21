@echo off
REM Install Print Client Pro to startup
echo Installing Print Client Pro to Windows Startup...

REM Get the current directory
set CURRENT_DIR=%~dp0

REM Create VBS script to run without console window
echo Set WshShell = CreateObject("WScript.Shell") > "%CURRENT_DIR%run_hidden.vbs"
echo WshShell.Run """%CURRENT_DIR%venv\Scripts\python.exe"" ""%CURRENT_DIR%printer_client_tray.py""", 0, False >> "%CURRENT_DIR%run_hidden.vbs"

REM Create shortcut in Startup folder
set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%STARTUP_FOLDER%\PrintClientPro.lnk'); $s.TargetPath = '%CURRENT_DIR%run_hidden.vbs'; $s.WorkingDirectory = '%CURRENT_DIR%'; $s.Description = 'Print Client Pro - Background Service'; $s.Save()"

echo.
echo Print Client Pro has been installed to startup!
echo It will start automatically when Windows boots.
echo.
echo To start it now, run: run_tray.bat
echo.
pause
