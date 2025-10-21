@echo off
REM Verify that all required files are present
echo ========================================
echo Print Client Pro - File Verification
echo ========================================
echo.

set CURRENT_DIR=%~dp0
set ALL_OK=1

echo Checking for required files...
echo.

REM Check PrintClientPro.exe
if exist "%CURRENT_DIR%PrintClientPro.exe" (
    echo [OK] PrintClientPro.exe found
) else (
    echo [ERROR] PrintClientPro.exe NOT FOUND!
    set ALL_OK=0
)

REM Check wkhtmltopdf.exe
if exist "%CURRENT_DIR%wkhtmltopdf.exe" (
    echo [OK] wkhtmltopdf.exe found
) else (
    echo [ERROR] wkhtmltopdf.exe NOT FOUND!
    echo        This file is REQUIRED for HTML to PDF conversion!
    set ALL_OK=0
)

REM Check SumatraPDF.exe
if exist "%CURRENT_DIR%SumatraPDF.exe" (
    echo [OK] SumatraPDF.exe found
) else (
    echo [ERROR] SumatraPDF.exe NOT FOUND!
    echo        This file is REQUIRED for reliable PDF printing!
    set ALL_OK=0
)

REM Check .env
if exist "%CURRENT_DIR%.env" (
    echo [OK] .env configuration file found
) else (
    echo [WARNING] .env not found (will be created on first run)
)

echo.
echo ========================================

if %ALL_OK%==1 (
    echo Status: ALL REQUIRED FILES PRESENT
    echo You can run PrintClientPro.exe
) else (
    echo Status: MISSING REQUIRED FILES!
    echo Please copy all files from the dist folder
)

echo ========================================
echo.
echo File sizes:
echo.
dir "%CURRENT_DIR%PrintClientPro.exe" 2>nul | find "PrintClientPro.exe"
dir "%CURRENT_DIR%wkhtmltopdf.exe" 2>nul | find "wkhtmltopdf.exe"
dir "%CURRENT_DIR%SumatraPDF.exe" 2>nul | find "SumatraPDF.exe"

echo.
pause
