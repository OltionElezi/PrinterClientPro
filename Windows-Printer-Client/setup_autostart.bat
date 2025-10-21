@echo off
REM ========================================
REM Auto-Start Setup for PrintClientPro
REM ========================================
echo.
echo ========================================
echo   PrintClientPro - Auto-Start Setup
echo ========================================
echo.

REM Get the current directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
set "EXE_PATH=%SCRIPT_DIR%dist\PrintClientPro.exe"

REM Check if the executable exists
if not exist "%EXE_PATH%" (
    echo ERROR: PrintClientPro.exe not found at:
    echo %EXE_PATH%
    echo.
    echo Please ensure the executable is in the dist folder.
    pause
    exit /b 1
)

echo Found executable at:
echo %EXE_PATH%
echo.

REM Get user's startup folder
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

REM Create shortcut in startup folder
echo Creating shortcut in Windows Startup folder...
echo.

REM Use PowerShell to create a proper shortcut
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTUP_FOLDER%\PrintClientPro.lnk'); $Shortcut.TargetPath = '%EXE_PATH%'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%dist'; $Shortcut.Description = 'PrintClientPro - Automatic Printer Client'; $Shortcut.Save()"

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   SUCCESS! Auto-start configured
    echo ========================================
    echo.
    echo PrintClientPro will now start automatically when Windows boots.
    echo.
    echo Shortcut created at:
    echo %STARTUP_FOLDER%\PrintClientPro.lnk
    echo.
    echo To disable auto-start, simply delete the shortcut from:
    echo %STARTUP_FOLDER%
    echo.
) else (
    echo.
    echo ERROR: Failed to create startup shortcut.
    echo Please run this script as Administrator.
    echo.
)

echo.
echo Press any key to exit...
pause > nul
