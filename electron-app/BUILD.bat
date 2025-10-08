@echo off
echo ========================================
echo MID Task - Building Windows Installer
echo ========================================
echo.
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

