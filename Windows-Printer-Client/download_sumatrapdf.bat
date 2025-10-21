@echo off
REM Download SumatraPDF portable version for bundling
echo Downloading SumatraPDF portable version...
echo.

REM Create temp directory
if not exist "temp_download" mkdir temp_download
cd temp_download

REM Download SumatraPDF portable (64-bit)
echo Downloading from sumatrapdfreader.org...
powershell -Command "Invoke-WebRequest -Uri 'https://www.sumatrapdfreader.org/dl/rel/3.5.2/SumatraPDF-3.5.2-64.zip' -OutFile 'SumatraPDF.zip'"

if %ERRORLEVEL% NEQ 0 (
    echo Download failed!
    pause
    exit /b 1
)

echo.
echo Extracting...
powershell -Command "Expand-Archive -Path 'SumatraPDF.zip' -DestinationPath '.' -Force"

echo.
echo Copying SumatraPDF.exe to dist folder...
copy /Y "SumatraPDF.exe" "..\dist\SumatraPDF.exe"

cd ..
echo.
echo Cleaning up...
rmdir /s /q temp_download

echo.
echo SumatraPDF.exe has been added to the dist folder!
echo.
pause
