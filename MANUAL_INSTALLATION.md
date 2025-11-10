# MID Task - Manual Installation Guide

## Simple 3-Step Process

### Step 1: Copy MID Folder to C:\

1. Copy the entire `MID` folder to `C:\`
2. Result should be: `C:\MID\`

```
C:\MID\
├── electron-app\
│   ├── nodejs-portable\    (bundled Node.js)
│   ├── INSTALL.bat
│   ├── BUILD_PORTABLE.bat
│   ├── START.bat
│   └── ...
├── mid_psychopy_pc_yaml.py
├── data\
├── images\
└── ...
```

### Step 2: Install Dependencies

1. Navigate to: `C:\MID\electron-app\`
2. Double-click: **`INSTALL.bat`**
3. Wait for npm to install all dependencies
4. This only needs to be done once

### Step 3: Build or Run

Choose one:

**Option A: Build Portable Executable** (Recommended)
- Double-click: `BUILD_PORTABLE.bat`
- Wait for build to complete
- Find your .exe in: `C:\MID\electron-app\dist\`
- This .exe can run on any Windows PC!

**Option B: Run in Development Mode**
- Double-click: `START.bat`
- App will open in Electron

---

## That's It!

The scripts automatically detect and use the bundled `nodejs-portable` folder, so no Node.js installation is required.

---

## Why C:\MID?

✅ **Fixed Location** - Same path on every machine  
✅ **Easy to Find** - Simple, short path  
✅ **Independent** - Not in user folders that might move  
✅ **Portable** - Easy to backup or copy to other PCs  

---

## Troubleshooting

### "npm not found" error
- Verify `C:\MID\electron-app\nodejs-portable\npm.cmd` exists
- Re-extract the portable Node.js if needed

### Build fails
1. Delete `C:\MID\electron-app\node_modules\` folder
2. Run `INSTALL.bat` again
3. Try `BUILD_PORTABLE.bat` again

### Permission issues
- Some antivirus software may block execution
- Add `C:\MID\` to your antivirus exclusions

---

## Distribution to Other Machines

1. Complete Steps 1-3 above on your machine
2. Copy the entire `C:\MID\` folder to a USB drive or network share
3. On the target machine:
   - Copy to `C:\MID\`
   - Run the .exe from `C:\MID\electron-app\dist\`
   - OR run `START.bat` for development mode
   - (No need to run INSTALL.bat again - node_modules is included!)

**OR** just distribute the .exe file alone - it works standalone!

---

## File Locations

- **Electron App**: `C:\MID\electron-app\`
- **Bundled Node.js**: `C:\MID\electron-app\nodejs-portable\`
- **Built Executable**: `C:\MID\electron-app\dist\MID Task X.X.X.exe`
- **Experiment Data**: `C:\MID\electron-app\data\`
- **PsychoPy Script**: `C:\MID\mid_psychopy_pc_yaml.py`
- **Configuration**: `C:\MID\mid_config.yml`

---

## Next Steps After Installation

Your portable executable is at:
```
C:\MID\electron-app\dist\MID Task X.X.X.exe
```

You can:
- Run it directly from there
- Copy it anywhere on the same PC
- Copy it to other Windows PCs
- Create a desktop shortcut to it

No installation or Node.js required on the target machine!

