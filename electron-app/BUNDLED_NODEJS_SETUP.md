# Bundled Portable Node.js Setup

## Overview

The electron-app now supports bundled portable Node.js, allowing you to distribute the app with Node.js included - **no installation or admin rights required!**

## How It Works

All batch scripts (BUILD_PORTABLE.bat, INSTALL.bat, START.bat, BUILD.bat, START_PORTABLE.bat) now automatically check for Node.js in this priority order:

1. **BUNDLED** - `electron-app/nodejs-portable/` folder (highest priority)
2. **SYSTEM** - System PATH (if Node.js is installed)
3. **USER FOLDER** - `%USERPROFILE%\nodejs-portable\`
4. **PARENT FOLDER** - `../nodejs-portable/`

## Setup Instructions

### Option 1: Bundled Setup (Recommended for Distribution)

1. Download portable Node.js:
   - https://nodejs.org/dist/v20.11.0/node-v20.11.0-win-x64.zip
   - Or get the latest LTS version from: https://nodejs.org/dist/

2. Extract the contents to: `electron-app/nodejs-portable/`
   
   The folder structure should look like:
   ```
   electron-app/
   ├── nodejs-portable/
   │   ├── node.exe
   │   ├── npm.cmd
   │   ├── npx.cmd
   │   └── (other Node.js files)
   ├── BUILD_PORTABLE.bat
   ├── INSTALL.bat
   └── ...
   ```

3. Run the scripts normally:
   - `INSTALL.bat` - Install dependencies
   - `BUILD_PORTABLE.bat` - Build standalone .exe
   - `START.bat` - Run in development mode

### Option 2: System Installation

Just install Node.js normally from https://nodejs.org/ and the scripts will use the system version.

### Option 3: User Folder

Extract portable Node.js to `%USERPROFILE%\nodejs-portable\` (e.g., `C:\Users\YourName\nodejs-portable\`)

## Benefits of Bundled Setup

✅ **No Admin Rights** - Works without installation privileges  
✅ **Portable** - Copy the entire electron-app folder to any PC  
✅ **Self-Contained** - Everything needed is in one place  
✅ **Version Control** - Lock to a specific Node.js version  
✅ **Easy Distribution** - Share the complete package with colleagues  

## Distribution Package

### Recommended: Copy Entire MID Project to C:\MID

1. **Manually copy** the MID folder to `C:\MID`
2. Go to `C:\MID\electron-app\`
3. Run `INSTALL.bat` (first time only)
4. Run `BUILD_PORTABLE.bat` to create .exe

**Benefits:**
- ✅ Consistent location: `C:\MID` on all machines
- ✅ Easy to find and maintain
- ✅ Includes all experiment files and data
- ✅ Simple backup: just copy `C:\MID`

### Alternative: Share electron-app Only

When sharing just the electron-app:
- Include the entire `electron-app/` folder
- Include the bundled `nodejs-portable/` folder inside it
- Recipients run `INSTALL.bat` first, then `BUILD_PORTABLE.bat`

Recipients can use it immediately without Node.js installation!

## Current Setup Status

Your setup already has:
- ✅ `nodejs-portable/` folder in `electron-app/`
- ✅ Updated batch scripts that detect bundled Node.js

You're ready to go! Just run `BUILD_PORTABLE.bat` and it will use your bundled Node.js.

## Troubleshooting

### "npm is not found" error
- Verify `nodejs-portable/npm.cmd` exists
- Check that you extracted the full Node.js portable package
- Make sure the folder is named exactly `nodejs-portable`

### "npm was found but doesn't work"
- Ensure `node.exe` is in the same folder as `npm.cmd`
- Check that no files are blocked (right-click > Properties > Unblock)
- Re-download and extract the portable Node.js package

### Zone.Identifier files
The `:Zone.Identifier` files you see are Windows security markers from downloads. They're harmless and don't affect functionality.

