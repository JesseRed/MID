@echo off
setlocal enabledelayedexpansion
echo ========================================
echo MID Task - Electron App Installation
echo ========================================
echo.

echo [DEBUG] Starting npm detection...
echo.

REM Check if npm is available (try bundled portable Node.js first)
set "NPM_CMD=npm"
set NPM_FOUND=0

echo [DEBUG] Checking for BUNDLED portable Node.js in current folder...
echo [DEBUG] Current directory = %CD%
echo.

REM First priority: Check for bundled nodejs-portable in current folder
echo [DEBUG] Checking path 1 (BUNDLED): nodejs-portable\npm.cmd
if exist "nodejs-portable\npm.cmd" (
    echo [DEBUG] ✓ Path 1 EXISTS - BUNDLED version found!
    set "NPM_CMD=nodejs-portable\npm.cmd"
    REM Get absolute path for PATH using delayed expansion
    pushd "nodejs-portable" 2>nul
    set "NODEJS_DIR=!CD!"
    popd
    set NPM_FOUND=1
    echo Found BUNDLED portable Node.js in electron-app folder
    echo [DEBUG] NPM_CMD set to: !NPM_CMD!
    echo [DEBUG] NODEJS_DIR set to: !NODEJS_DIR!
    echo [DEBUG] NPM_FOUND = !NPM_FOUND!
    REM Add nodejs-portable to PATH so child processes can find node.exe
    set "PATH=!NODEJS_DIR!;%PATH%"
    echo [DEBUG] Added !NODEJS_DIR! to PATH
) else (
    echo [DEBUG] ✗ Path 1 does not exist (no bundled version)
    echo.
    
    echo [DEBUG] Checking system PATH for npm...
    where npm >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set NPM_FOUND=1
        echo [DEBUG] ✓ Found npm in system PATH
        echo Using system npm
    ) else (
        echo [DEBUG] ✗ npm not found in system PATH
        echo.
        echo [DEBUG] Checking other portable Node.js locations...
        echo [DEBUG] USERPROFILE = %USERPROFILE%
        echo.
        
        REM Try common portable Node.js locations (check user folder)
        REM Direct check without intermediate variables to avoid expansion issues
        echo [DEBUG] Checking path 2: %USERPROFILE%\nodejs-portable\npm.cmd
        if exist "%USERPROFILE%\nodejs-portable\npm.cmd" (
        echo [DEBUG] ✓ Path 2 EXISTS!
        set "NPM_CMD=%USERPROFILE%\nodejs-portable\npm.cmd"
        set "NODEJS_DIR=%USERPROFILE%\nodejs-portable"
        set NPM_FOUND=1
        echo Found portable Node.js in user folder: %USERPROFILE%\nodejs-portable
        echo [DEBUG] NPM_CMD set to: !NPM_CMD!
        echo [DEBUG] NODEJS_DIR set to: !NODEJS_DIR!
        echo [DEBUG] NPM_FOUND = !NPM_FOUND!
        REM Add nodejs-portable to PATH so child processes can find node.exe
        set "PATH=!NODEJS_DIR!;%PATH%"
        echo [DEBUG] Added !NODEJS_DIR! to PATH
        ) else (
            echo [DEBUG] ✗ Path 2 check failed
            echo [DEBUG] Checking if directory exists: %USERPROFILE%\nodejs-portable
        if exist "%USERPROFILE%\nodejs-portable" (
            echo [DEBUG] ✓ Directory exists, listing contents:
            dir /b "%USERPROFILE%\nodejs-portable" 2>nul
            echo [DEBUG] Re-checking npm.cmd with different methods...
            REM Method 1: Try using cd and relative path
            pushd "%USERPROFILE%\nodejs-portable" 2>nul
            if exist "npm.cmd" (
                echo [DEBUG] ✓ Found npm.cmd using cd method!
                set "NPM_CMD=%USERPROFILE%\nodejs-portable\npm.cmd"
                set "NODEJS_DIR=%USERPROFILE%\nodejs-portable"
                set NPM_FOUND=1
                echo Found portable Node.js in user folder: %USERPROFILE%\nodejs-portable
                echo [DEBUG] NPM_CMD set to: !NPM_CMD!
                echo [DEBUG] NODEJS_DIR set to: !NODEJS_DIR!
                echo [DEBUG] NPM_FOUND = !NPM_FOUND!
                REM Add nodejs-portable to PATH so child processes can find node.exe
                set "PATH=!NODEJS_DIR!;%PATH%"
                echo [DEBUG] Added !NODEJS_DIR! to PATH
            ) else (
                REM Method 2: Use dir command to check
                echo [DEBUG] Trying dir command to verify file...
                dir /b "npm.cmd" >nul 2>&1
                if !ERRORLEVEL! EQU 0 (
                    echo [DEBUG] ✓ Found npm.cmd using dir method!
                    set "NPM_CMD=%USERPROFILE%\nodejs-portable\npm.cmd"
                    set "NODEJS_DIR=%USERPROFILE%\nodejs-portable"
                    set NPM_FOUND=1
                    echo Found portable Node.js in user folder: %USERPROFILE%\nodejs-portable
                    echo [DEBUG] NPM_CMD set to: !NPM_CMD!
                    echo [DEBUG] NODEJS_DIR set to: !NODEJS_DIR!
                    echo [DEBUG] NPM_FOUND = !NPM_FOUND!
                    REM Add nodejs-portable to PATH so child processes can find node.exe
                    set "PATH=!NODEJS_DIR!;%PATH%"
                    echo [DEBUG] Added !NODEJS_DIR! to PATH
                )
            )
            popd
        ) else (
            echo [DEBUG] ✗ Directory does not exist
        )
        echo.
        
        if !NPM_FOUND! EQU 0 (
            echo [DEBUG] Checking path 3: ..\nodejs-portable\npm.cmd
            if exist "..\nodejs-portable\npm.cmd" (
                echo [DEBUG] ✓ Path 3 EXISTS!
                set "NPM_CMD=..\nodejs-portable\npm.cmd"
                REM Get absolute path for PATH using delayed expansion
                pushd "..\nodejs-portable" 2>nul
                set "NODEJS_DIR=!CD!"
                popd
                set NPM_FOUND=1
                echo Found portable Node.js in parent folder
                echo [DEBUG] NPM_CMD set to: !NPM_CMD!
                echo [DEBUG] NODEJS_DIR set to: !NODEJS_DIR!
                echo [DEBUG] NPM_FOUND = !NPM_FOUND!
                REM Add nodejs-portable to PATH so child processes can find node.exe
                set "PATH=!NODEJS_DIR!;%PATH%"
                echo [DEBUG] Added !NODEJS_DIR! to PATH
            ) else (
                echo [DEBUG] ✗ Path 3 does not exist
                echo.
                
                echo [DEBUG] Checking path 4: nodejs-portable\npm.cmd (legacy check)
                if exist "nodejs-portable\npm.cmd" (
                    echo [DEBUG] ✓ Path 4 EXISTS! (This should have been caught by path 1)
                    set "NPM_CMD=nodejs-portable\npm.cmd"
                    REM Get absolute path for PATH using delayed expansion
                    pushd "nodejs-portable" 2>nul
                    set "NODEJS_DIR=!CD!"
                    popd
                    set NPM_FOUND=1
                    echo Found portable Node.js in current folder
                    echo [DEBUG] NPM_CMD set to: !NPM_CMD!
                    echo [DEBUG] NODEJS_DIR set to: !NODEJS_DIR!
                    echo [DEBUG] NPM_FOUND = !NPM_FOUND!
                    REM Add nodejs-portable to PATH so child processes can find node.exe
                    set "PATH=!NODEJS_DIR!;%PATH%"
                    echo [DEBUG] Added !NODEJS_DIR! to PATH
                ) else (
                    echo [DEBUG] ✗ Path 4 does not exist
                )
            )
        )
        )
    )
    echo.
)

echo [DEBUG] Before final check: NPM_FOUND = !NPM_FOUND!, NPM_CMD = !NPM_CMD!

REM Check if npm was found - use goto to avoid nested if issues
if "!NPM_FOUND!"=="1" goto npm_found
if "!NPM_FOUND!"=="0" goto npm_not_found

:npm_not_found
echo [DEBUG] NPM_FOUND check failed - showing error message
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
echo OPTION 3: Add Node.js to user PATH (NO admin rights needed!)
echo   1. Press Win+R, type: sysdm.cpl
echo   2. Advanced tab ^> Environment Variables
echo   3. Under "User variables", edit "Path"
echo   4. Add your Node.js folder (e.g., C:\Users\YourName\nodejs-portable)
echo   5. Restart command prompt
echo.
pause
exit /b 1

:npm_found
echo [DEBUG] NPM found, continuing with installation...

REM Verify npm actually works
echo [DEBUG] Verifying npm works...
echo [DEBUG] Attempting to run: !NPM_CMD! --version
call !NPM_CMD! --version
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: npm was found but doesn't work properly.
    echo Path: !NPM_CMD!
    echo Error code: %ERRORLEVEL%
    echo.
    echo [DEBUG] Checking if file exists:
    if exist "!NPM_CMD!" (
        echo [DEBUG] ✓ File exists
    ) else (
        echo [DEBUG] ✗ File does NOT exist at: !NPM_CMD!
    )
    echo.
    echo Please check that Node.js is properly extracted and npm.cmd is executable.
    pause
    exit /b 1
)
echo [DEBUG] ✓ npm verified successfully!
echo.

echo Installing dependencies...
echo This may take a few minutes on first run.
echo.

call !NPM_CMD! install

echo.
echo ========================================
echo Installation complete!
echo ========================================
echo.
echo To run the app, double-click: START.bat
echo To build Windows installer, double-click: BUILD.bat
echo.
pause

