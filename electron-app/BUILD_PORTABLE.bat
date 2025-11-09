@echo off
echo ========================================
echo MID Task - Building Portable Executable
echo ========================================
echo.
echo This creates a standalone .exe that runs WITHOUT npm/Node.js!
echo No installation needed - just copy and run!
echo.

REM Check if npm is available (try system PATH first)
set NPM_CMD=npm
set NPM_FOUND=0
where npm >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set NPM_FOUND=1
    echo Using system npm
) else (
    REM Try common portable Node.js locations
    if exist "%USERPROFILE%\nodejs-portable\npm.cmd" (
        set "NPM_CMD=%USERPROFILE%\nodejs-portable\npm.cmd"
        set NPM_FOUND=1
        echo Found portable Node.js in user folder: %USERPROFILE%\nodejs-portable
    ) else if exist "..\nodejs-portable\npm.cmd" (
        set "NPM_CMD=..\nodejs-portable\npm.cmd"
        set NPM_FOUND=1
        echo Found portable Node.js in parent folder
    ) else if exist "nodejs-portable\npm.cmd" (
        set "NPM_CMD=nodejs-portable\npm.cmd"
        set NPM_FOUND=1
        echo Found portable Node.js in current folder
    )
)

if %NPM_FOUND% EQU 0 (
    echo ERROR: npm is not found.
    echo.
    echo OPTION 1: Install Node.js normally (requires admin rights once)
    echo   - Download from https://nodejs.org/
    echo   - Install and restart terminal
    echo.
    echo OPTION 2: Use portable Node.js (NO admin rights needed!)
    echo   1. Download portable Node.js from:
    echo      https://nodejs.org/dist/v20.11.0/node-v20.11.0-win-x64.zip
    echo      (or latest LTS version)
    echo   2. Extract to: %USERPROFILE%\nodejs-portable
    echo   3. Run this script again
    echo.
    pause
    exit /b 1
)

REM Verify npm actually works
echo Verifying npm...
call %NPM_CMD% --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: npm was found but doesn't work properly.
    echo Path: %NPM_CMD%
    echo.
    echo Please check that Node.js is properly extracted and npm.cmd is executable.
    pause
    exit /b 1
)
echo npm verified successfully!
echo.

REM Check if node_modules exists (dependencies installed)
if not exist "node_modules" (
    echo WARNING: Dependencies not found!
    echo.
    echo Installing dependencies first...
    echo.
    call %NPM_CMD% install
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo ERROR: Failed to install dependencies.
        pause
        exit /b 1
    )
)

echo Building portable executable...
echo This may take several minutes...
echo.

call %NPM_CMD% run build-portable

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Build complete!
    echo ========================================
    echo.
    echo The portable executable is located in: dist\
    echo File: MID Task X.X.X.exe
    echo.
    echo This .exe file:
    echo - Runs WITHOUT npm or Node.js
    echo - Requires NO installation
    echo - Can be copied to any Windows PC
    echo - Runs without admin rights
    echo.
) else (
    echo.
    echo ERROR: Build failed!
    echo.
)

pause

