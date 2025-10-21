@echo off
REM ========================================
REM Remove Auto-Start for PrintClientPro
REM ========================================
echo.
echo ========================================
echo   PrintClientPro - Remove Auto-Start
echo ========================================
echo.

REM Get user's startup folder
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_PATH=%STARTUP_FOLDER%\PrintClientPro.lnk"

REM Check if shortcut exists
if exist "%SHORTCUT_PATH%" (
    echo Found startup shortcut at:
    echo %SHORTCUT_PATH%
    echo.
    echo Removing shortcut...
    del "%SHORTCUT_PATH%"

    if %errorlevel% equ 0 (
        echo.
        echo ========================================
        echo   SUCCESS! Auto-start removed
        echo ========================================
        echo.
        echo PrintClientPro will no longer start automatically.
        echo.
    ) else (
        echo.
        echo ERROR: Failed to delete shortcut.
        echo.
    )
) else (
    echo.
    echo No auto-start shortcut found.
    echo PrintClientPro is not configured to start automatically.
    echo.
)

echo.
echo Press any key to exit...
pause > nul
