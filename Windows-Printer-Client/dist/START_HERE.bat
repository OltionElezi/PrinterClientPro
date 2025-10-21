@echo off
REM ========================================
REM PrintClientPro - Quick Start Menu
REM ========================================

:MENU
cls
echo.
echo ========================================
echo    PrintClientPro - Quick Start Menu
echo ========================================
echo.
echo What would you like to do?
echo.
echo 1. Setup Auto-Start (Configure Windows to start on boot)
echo 2. Remove Auto-Start (Disable automatic startup)
echo 3. Start PrintClientPro Now
echo 4. Open Configuration File (.env)
echo 5. Open Startup Folder
echo 6. View Documentation
echo 7. Exit
echo.
echo ========================================
echo.

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto SETUP
if "%choice%"=="2" goto REMOVE
if "%choice%"=="3" goto START
if "%choice%"=="4" goto CONFIG
if "%choice%"=="5" goto STARTUP_FOLDER
if "%choice%"=="6" goto DOCS
if "%choice%"=="7" goto EXIT

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto MENU

:SETUP
cls
echo.
echo Running Auto-Start Setup...
echo.
call SETUP_AUTOSTART.bat
goto MENU

:REMOVE
cls
echo.
echo Running Auto-Start Removal...
echo.
call REMOVE_AUTOSTART.bat
goto MENU

:START
cls
echo.
echo Starting PrintClientPro...
echo.
start "" "%~dp0PrintClientPro.exe"
echo Application started!
timeout /t 2 >nul
goto MENU

:CONFIG
cls
echo.
echo Opening configuration file...
echo.
if exist "%~dp0.env" (
    notepad "%~dp0.env"
) else (
    echo ERROR: .env file not found!
    echo Please run "Setup Auto-Start" first to create it.
    timeout /t 3 >nul
)
goto MENU

:STARTUP_FOLDER
cls
echo.
echo Opening Windows Startup folder...
echo.
explorer "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
timeout /t 1 >nul
goto MENU

:DOCS
cls
echo.
echo Opening documentation...
echo.
if exist "%~dp0README_AUTOSTART.txt" (
    notepad "%~dp0README_AUTOSTART.txt"
) else (
    echo ERROR: Documentation file not found!
    timeout /t 3 >nul
)
goto MENU

:EXIT
cls
echo.
echo Thank you for using PrintClientPro!
echo.
timeout /t 1 >nul
exit
