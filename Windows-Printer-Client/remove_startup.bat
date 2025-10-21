@echo off
REM Remove Print Client Pro from startup
echo Removing Print Client Pro from Windows Startup...

REM Delete shortcut from Startup folder
set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
del "%STARTUP_FOLDER%\PrintClientPro.lnk" 2>nul

REM Delete VBS script
set CURRENT_DIR=%~dp0
del "%CURRENT_DIR%run_hidden.vbs" 2>nul

echo.
echo Print Client Pro has been removed from startup.
echo It will no longer start automatically when Windows boots.
echo.
pause
