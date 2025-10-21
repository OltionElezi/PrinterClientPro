@echo off
REM ========================================
REM PrintClientPro - Remove Auto-Start
REM ========================================

echo.
echo ================================================
echo    PrintClientPro - Remove Auto-Start
echo ================================================
echo.

REM Get user's startup folder
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_PATH=%STARTUP_FOLDER%\PrintClientPro.lnk"

REM Check if shortcut exists
if exist "%SHORTCUT_PATH%" (
    echo Found auto-start shortcut at:
    echo %SHORTCUT_PATH%
    echo.
    echo Removing auto-start configuration...
    del "%SHORTCUT_PATH%" 2>nul

    if %errorlevel% equ 0 (
        echo.
        echo ================================================
        echo    SUCCESS! Auto-start removed
        echo ================================================
        echo.
        echo PrintClientPro will no longer start automatically.
        echo.
        echo NOTE: This does NOT uninstall the application.
        echo The program files remain in this folder.
        echo.
        echo To re-enable auto-start:
        echo  - Run: SETUP_AUTOSTART.bat
        echo.
    ) else (
        echo.
        echo ERROR: Failed to delete shortcut.
        echo You may need to run this script as Administrator.
        echo.
    )
) else (
    echo.
    echo No auto-start configuration found.
    echo PrintClientPro is not configured to start automatically.
    echo.
    echo To enable auto-start:
    echo  - Run: SETUP_AUTOSTART.bat
    echo.
)

echo Press any key to exit...
pause >nul
