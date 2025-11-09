# Running MID Task Without Admin Rights

This guide explains how to run the MID Task application without requiring administrator rights or installing Node.js system-wide.

## 🎯 Two Solutions

### Solution 1: Portable Executable (Recommended - No npm needed at all!)

**Best for:** Running the app on any PC without any setup

1. **Build once** (requires npm only for building):
   - Use `BUILD_PORTABLE.bat` to create a standalone `.exe` file
   - This only needs to be done once (or when you update the app)

2. **Run anywhere**:
   - The `.exe` file in `dist\` folder runs completely standalone
   - No npm, no Node.js, no installation needed
   - Just double-click the `.exe` file
   - Works on any Windows PC without admin rights

**Steps:**
```
1. Build portable: Double-click BUILD_PORTABLE.bat
2. Find executable: Look in dist\ folder
3. Run: Double-click MID Task X.X.X.exe
```

---

### Solution 2: Portable Node.js (No admin rights for npm)

**Best for:** Development or if you need to modify the app

1. **Download Portable Node.js** (no installation needed):
   - Go to: https://nodejs.org/dist/
   - Download the latest LTS version (e.g., `node-v20.11.0-win-x64.zip`)
   - Extract the ZIP file to a folder (e.g., `C:\Users\YourName\nodejs-portable`)

2. **Use the portable scripts**:
   - `BUILD_PORTABLE.bat` - Automatically finds portable Node.js
   - `START_PORTABLE.bat` - Uses portable Node.js to run the app

**Where to extract:**
- `%USERPROFILE%\nodejs-portable` (recommended - your user folder)
- Or `electron-app\nodejs-portable` (in the project folder)
- Or any folder you prefer

**The scripts will automatically find Node.js in these locations:**
- `%USERPROFILE%\nodejs-portable`
- `electron-app\nodejs-portable`
- `MID\nodejs-portable` (parent folder)

---

## 📋 Quick Comparison

| Method | Admin Rights? | npm Needed? | Best For |
|--------|---------------|-------------|----------|
| **Portable .exe** | ❌ No | ❌ No (only to build) | End users, distribution |
| **Portable Node.js** | ❌ No | ✅ Yes (portable) | Development, testing |
| **System Node.js** | ✅ Yes (to install) | ✅ Yes | Development |

---

## 🚀 Recommended Workflow

### For End Users (No Admin Rights):
1. Someone with build access runs `BUILD_PORTABLE.bat` once
2. Distribute the `.exe` file from `dist\` folder
3. Users just double-click the `.exe` - no setup needed!

### For Developers (No Admin Rights):
1. Download portable Node.js to `%USERPROFILE%\nodejs-portable`
2. Use `BUILD_PORTABLE.bat` and `START_PORTABLE.bat`
3. No admin rights needed at any point!

---

## 🔧 Troubleshooting

### "npm is not found" when using BUILD_PORTABLE.bat
- Make sure you extracted portable Node.js to one of these locations:
  - `%USERPROFILE%\nodejs-portable`
  - `electron-app\nodejs-portable`
  - `MID\nodejs-portable`
- Or manually edit `BUILD_PORTABLE.bat` to point to your Node.js location

### Portable executable doesn't start
- Make sure `mid_config.yml` and `text_content.yml` are in the parent MID folder
- The portable exe looks for these files relative to where it's run

### Want to use a different Node.js location?
Edit `BUILD_PORTABLE.bat` and `START_PORTABLE.bat` and change the path checks to your location.

---

## ✅ Summary

**Easiest solution:** Build a portable executable once, then just run the `.exe` file - no npm needed!

**For development:** Use portable Node.js - no admin rights needed!

