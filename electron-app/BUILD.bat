@echo off
echo ========================================
echo MID Task - Building Windows Installer
echo ========================================
echo.

REM Check if npm is available
where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: npm is not found in your system PATH.
    echo.
    echo This usually means Node.js is not installed or not in your PATH.
    echo.
    echo Please do one of the following:
    echo 1. Install Node.js from https://nodejs.org/
    echo 2. Add Node.js to your system PATH environment variable
    echo 3. Restart your command prompt/terminal after installing Node.js
    echo.
    echo Alternatively, use a portable Node.js installation (no admin rights needed):
    echo - Download portable Node.js from: https://nodejs.org/dist/
    echo - Extract to a folder (e.g., C:\nodejs-portable)
    echo - Use BUILD_PORTABLE.bat which can use portable Node.js
    echo.
    pause
    exit /b 1
)

REM Check if node_modules exists (dependencies installed)
if not exist "node_modules" (
    echo WARNING: Dependencies not found!
    echo.
    echo Please run INSTALL.bat first to install required packages.
    echo.
    pause
    exit /b 1
)

echo This will create a Windows installer in the 'dist' folder.
echo Please wait, this may take several minutes...
echo.

call npm run build

echo.
echo ========================================
echo Build complete!
echo ========================================
echo.
echo The installer is located in: dist\
echo File: MID Task Setup X.X.X.exe
echo.
echo You can now distribute this installer to Windows PCs.
echo.
pause

