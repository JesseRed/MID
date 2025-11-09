@echo off
setlocal enabledelayedexpansion
echo ========================================
echo MID Task - Starting Application (Portable)
echo ========================================
echo.

REM Check if portable executable exists
if exist "dist\MID Task*.exe" (
    echo Found portable executable!
    echo Starting application...
    echo.
    
    REM Find the most recent exe file
    for /f "delims=" %%i in ('dir /b /o-d "dist\MID Task*.exe" 2^>nul') do (
        start "" "dist\%%i"
        echo Application started!
        echo.
        pause
        exit /b 0
    )
)

REM If no portable exe, try to use npm
set "NPM_CMD=npm"
where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    REM Try portable Node.js locations (check user folder first)
    if exist "%USERPROFILE%\nodejs-portable\npm.cmd" (
        set "NPM_CMD=%USERPROFILE%\nodejs-portable\npm.cmd"
        set "NODEJS_DIR=%USERPROFILE%\nodejs-portable"
        REM Add nodejs-portable to PATH so electron can find node.exe
        set "PATH=!NODEJS_DIR!;%PATH%"
    ) else if exist "..\nodejs-portable\npm.cmd" (
        set "NPM_CMD=..\nodejs-portable\npm.cmd"
        REM Get absolute path for PATH
        pushd "..\nodejs-portable" 2>nul
        set "NODEJS_DIR=%CD%"
        popd
        REM Add nodejs-portable to PATH so electron can find node.exe
        set "PATH=!NODEJS_DIR!;%PATH%"
    ) else if exist "nodejs-portable\npm.cmd" (
        set "NPM_CMD=nodejs-portable\npm.cmd"
        REM Get absolute path for PATH
        pushd "nodejs-portable" 2>nul
        set "NODEJS_DIR=%CD%"
        popd
        REM Add nodejs-portable to PATH so electron can find node.exe
        set "PATH=!NODEJS_DIR!;%PATH%"
    ) else (
        echo ERROR: No portable executable found and npm is not available.
        echo.
        echo Please either:
        echo 1. Build a portable executable using BUILD_PORTABLE.bat
        echo 2. Install Node.js and use START.bat instead
        echo.
        pause
        exit /b 1
    )
)

REM Check if node_modules exists
if not exist "node_modules" (
    echo WARNING: Dependencies not found!
    echo.
    echo Please run INSTALL.bat first to install required packages.
    echo.
    pause
    exit /b 1
)

echo Starting Electron application...
echo.

call !NPM_CMD! start

pause

