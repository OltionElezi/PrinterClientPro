@echo off
REM Build Print Client Pro executable
echo ========================================
echo Building Print Client Pro
echo ========================================
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo.

REM Build executable
echo Building executable with PyInstaller...
venv\Scripts\pyinstaller.exe --clean --noconfirm PrintClientPro.spec

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Executable location: dist\PrintClientPro.exe
echo.
pause
