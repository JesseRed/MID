@echo off
setlocal enabledelayedexpansion
echo ========================================
echo MID Task - Building Windows Installer
echo ========================================
echo.

REM Check if npm is available (try bundled portable Node.js first)
set "NPM_CMD=npm"
set NPM_FOUND=0

REM First priority: Check for bundled nodejs-portable in current folder
if exist "nodejs-portable\npm.cmd" (
    set "NPM_CMD=nodejs-portable\npm.cmd"
    REM Get absolute path for PATH using delayed expansion
    pushd "nodejs-portable" 2>nul
    set "NODEJS_DIR=!CD!"
    popd
    set NPM_FOUND=1
    echo Found BUNDLED portable Node.js in electron-app folder
    REM Add nodejs-portable to PATH so npm can find node.exe
    set "PATH=!NODEJS_DIR!;%PATH%"
) else (
    REM Try system PATH
    where npm >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set NPM_FOUND=1
        echo Using system npm
    ) else (
        REM Try other portable Node.js locations
        if exist "%USERPROFILE%\nodejs-portable\npm.cmd" (
            set "NPM_CMD=%USERPROFILE%\nodejs-portable\npm.cmd"
            set "NODEJS_DIR=%USERPROFILE%\nodejs-portable"
            set NPM_FOUND=1
            echo Found portable Node.js in user folder: %USERPROFILE%\nodejs-portable
            REM Add nodejs-portable to PATH so npm can find node.exe
            set "PATH=!NODEJS_DIR!;%PATH%"
        ) else if exist "..\nodejs-portable\npm.cmd" (
            set "NPM_CMD=..\nodejs-portable\npm.cmd"
            REM Get absolute path for PATH using delayed expansion
            pushd "..\nodejs-portable" 2>nul
            set "NODEJS_DIR=!CD!"
            popd
            set NPM_FOUND=1
            echo Found portable Node.js in parent folder
            REM Add nodejs-portable to PATH so npm can find node.exe
            set "PATH=!NODEJS_DIR!;%PATH%"
        )
    )
)

if !NPM_FOUND! EQU 0 (
    echo ERROR: npm is not found and no bundled nodejs-portable detected.
    echo.
    echo OPTION 1: Use bundled portable Node.js (RECOMMENDED - NO admin rights!)
    echo   1. Download portable Node.js from:
    echo      https://nodejs.org/dist/v20.11.0/node-v20.11.0-win-x64.zip
    echo      (or latest LTS version)
    echo   2. Extract the contents to: %~dp0nodejs-portable\
    echo      (The folder should contain: node.exe, npm.cmd, etc.)
    echo   3. Run this script again
    echo.
    echo OPTION 2: Install Node.js normally (requires admin rights once)
    echo   - Download from https://nodejs.org/
    echo   - Install and restart terminal
    echo.
    echo Alternatively, use BUILD_PORTABLE.bat to create a standalone .exe
    echo.
    pause
    exit /b 1
)

REM Verify npm actually works
call !NPM_CMD! --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: npm was found but doesn't work properly.
    echo Path: !NPM_CMD!
    echo.
    echo Please check that Node.js is properly extracted and npm.cmd is executable.
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

call !NPM_CMD! run build

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

