@echo off
REM ========================================
REM PrintClientPro - Complete Setup Script
REM ========================================
REM This script configures:
REM 1. Windows Auto-Start (runs on PC boot)
REM 2. Ensures .env configuration file exists
REM 3. Creates all necessary shortcuts
REM ========================================

echo.
echo ================================================
echo    PrintClientPro - Complete Setup Wizard
echo ================================================
echo.

REM Get the directory where this script is located (should be dist folder)
set "DIST_DIR=%~dp0"
set "EXE_PATH=%DIST_DIR%PrintClientPro.exe"
set "ENV_FILE=%DIST_DIR%.env"

REM Check if running from dist folder
echo [1/5] Checking installation directory...
echo Current directory: %DIST_DIR%
echo.

REM Verify executable exists
if not exist "%EXE_PATH%" (
    echo ERROR: PrintClientPro.exe not found!
    echo Expected location: %EXE_PATH%
    echo.
    echo Please ensure this script is in the same folder as PrintClientPro.exe
    pause
    exit /b 1
)
echo    OK - PrintClientPro.exe found
echo.

REM Check/Create .env configuration file
echo [2/5] Checking configuration file (.env)...
if exist "%ENV_FILE%" (
    echo    OK - .env file already exists
    echo    Current configuration will be preserved
) else (
    echo    Creating default .env configuration file...
    (
        echo # WebSocket Server Configuration
        echo SOCKET_URL=https://socket.pss.al
        echo.
        echo # Authentication Parameters (required by Backend-Socket^)
        echo SESSION_ID=printer_client_session_001
        echo CLIENT_USERNAME=printer_client
        echo NIPT=PSSTEST
        echo.
        echo # PDF Converter Configuration
        echo PDF_CONVERTER=wkhtmltopdf
        echo.
        echo # Font Size Configuration (for ReportLab renderer^)
        echo FONT_SCALE=0.95
        echo.
        echo # Logging Configuration
        echo LOG_LEVEL=INFO
        echo LOG_FILE=printer_client.log
        echo.
        echo # Reconnection Settings
        echo RECONNECT_DELAY=5
        echo MAX_RECONNECT_ATTEMPTS=0
    ) > "%ENV_FILE%"
    echo    OK - .env file created with default settings
)
echo.

REM Get user's startup folder
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_PATH=%STARTUP_FOLDER%\PrintClientPro.lnk"

REM Remove old shortcut if exists
echo [3/5] Checking for existing auto-start configuration...
if exist "%SHORTCUT_PATH%" (
    echo    Found existing shortcut - removing old configuration...
    del "%SHORTCUT_PATH%" 2>nul
)
echo    OK - Ready to create new configuration
echo.

REM Create Windows Startup shortcut
echo [4/5] Configuring Windows Auto-Start...
echo    Creating startup shortcut...

powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); $Shortcut.TargetPath = '%EXE_PATH%'; $Shortcut.WorkingDirectory = '%DIST_DIR%'; $Shortcut.Description = 'PrintClientPro - Automatic Printer Client'; $Shortcut.IconLocation = '%EXE_PATH%,0'; $Shortcut.WindowStyle = 1; $Shortcut.Save()"

if %errorlevel% equ 0 (
    echo    OK - Auto-start configured successfully
) else (
    echo    WARNING: Failed to create startup shortcut
    echo    You may need to run this script as Administrator
)
echo.

REM Verify setup
echo [5/5] Verifying installation...
echo.
if exist "%SHORTCUT_PATH%" (
    echo    [OK] Auto-start shortcut created
) else (
    echo    [!!] Auto-start shortcut missing
)

if exist "%ENV_FILE%" (
    echo    [OK] Configuration file exists
) else (
    echo    [!!] Configuration file missing
)

if exist "%EXE_PATH%" (
    echo    [OK] Executable exists
) else (
    echo    [!!] Executable missing
)
echo.

REM Display summary
echo ================================================
echo    SETUP COMPLETE!
echo ================================================
echo.
echo Installation Details:
echo ---------------------
echo  Executable:  %EXE_PATH%
echo  Config File: %ENV_FILE%
echo  Shortcut:    %SHORTCUT_PATH%
echo.
echo What happens now:
echo -----------------
echo  [X] PrintClientPro will start automatically when Windows boots
echo  [X] Configuration is saved in .env file
echo  [X] All files are in this folder: %DIST_DIR%
echo.
echo How to modify configuration:
echo ----------------------------
echo  1. Open the GUI application
echo  2. Click "Configuration" button
echo  3. Edit settings (Server URL, NIPT, etc.)
echo  4. Click "Save" button
echo.
echo  OR manually edit: %ENV_FILE%
echo.
echo To test auto-start without rebooting:
echo --------------------------------------
echo  1. Press Windows Key + R
echo  2. Type: shell:startup
echo  3. Double-click "PrintClientPro" shortcut
echo.
echo To remove auto-start:
echo ---------------------
echo  Run: REMOVE_AUTOSTART.bat (in this folder)
echo.
echo  OR manually delete: %SHORTCUT_PATH%
echo.
echo ================================================

REM Ask if user wants to start the application now
echo.
set /p START_NOW="Do you want to start PrintClientPro now? (Y/N): "
if /i "%START_NOW%"=="Y" (
    echo.
    echo Starting PrintClientPro...
    start "" "%EXE_PATH%"
    echo.
    echo Application started!
    timeout /t 2 /nobreak >nul
) else (
    echo.
    echo You can start PrintClientPro anytime by:
    echo  - Double-clicking PrintClientPro.exe
    echo  - Or it will start automatically on next PC boot
)

echo.
echo Press any key to exit setup...
pause >nul
