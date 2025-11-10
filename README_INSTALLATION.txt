================================================================================
MID TASK - INSTALLATION INSTRUCTIONS
================================================================================

QUICK START:

1. Copy this entire MID folder to C:\
   Result: C:\MID\

2. Go to C:\MID\electron-app\

3. Double-click: INSTALL.bat
   (Wait for installation to complete)

4. Double-click: BUILD_PORTABLE.bat
   (Creates standalone .exe file)

5. Your executable is ready at:
   C:\MID\electron-app\dist\MID Task X.X.X.exe

================================================================================

WHAT'S INCLUDED:

- Bundled Node.js (nodejs-portable folder)
  No separate Node.js installation needed!

- All scripts work automatically from C:\MID\electron-app\

- The .exe file works on any Windows PC without installation

================================================================================

FOR MORE DETAILS:

See: MANUAL_INSTALLATION.md

================================================================================

TROUBLESHOOTING:

Problem: "npm not found"
Solution: Check that nodejs-portable\npm.cmd exists in electron-app folder

Problem: Build fails
Solution: Delete node_modules folder, run INSTALL.bat again

Problem: Electron won't start
Solution: Run INSTALL.bat from C:\MID\electron-app\

================================================================================

That's it! Simple and portable.

