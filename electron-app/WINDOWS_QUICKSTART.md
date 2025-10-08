# 🚀 Windows Quick Start Guide

## For Windows Users - Super Easy Setup!

---

## Step 1️⃣: Install Node.js

1. Download Node.js from: **https://nodejs.org/**
2. Run the installer
3. Click "Next" through all options (defaults are fine)
4. Restart your computer after installation

---

## Step 2️⃣: Install the App

1. Open the `electron-app` folder
2. **Double-click: `INSTALL.bat`**
3. Wait for installation to complete (first time only)
4. Press any key to close when done

---

## Step 3️⃣: Run the Experiment

**Double-click: `START.bat`**

The app will launch in fullscreen!

---

## 🎮 Using the App

1. Enter **Participant ID**
2. Enter **Session** (default: 001)
3. Click **Start**
4. Follow the instructions
5. Data saves automatically to the `data` folder
6. Press **ESC** to quit anytime

---

## 📝 Edit Settings Before Running

### To change experiment parameters:
1. Open `mid_config.yml` (in the main MID folder, not electron-app)
2. Edit values (trials, timing, points, etc.)
3. Save the file
4. Run the app

### To change text/instructions:
1. Open `text_content.yml` (in the main MID folder)
2. Edit any text
3. Save the file
4. Run the app

---

## 📦 Create Windows Installer (Optional)

Want to distribute to other Windows PCs?

1. **Double-click: `BUILD.bat`**
2. Wait for the build to complete (5-10 minutes)
3. Find the installer in the `dist` folder
4. Copy the `.exe` file to other PCs
5. Install and run!

The installed app doesn't need Node.js on the target PC!

---

## 📁 Where is Everything?

```
MID/
├── electron-app/          ← You are here!
│   ├── INSTALL.bat        ← Run this FIRST
│   ├── START.bat          ← Run this to start app
│   ├── BUILD.bat          ← Build Windows installer
│   └── dist/              ← Installer appears here after BUILD
│
├── mid_config.yml         ← Edit experiment settings
├── text_content.yml       ← Edit instructions
├── images/                ← Experiment images
└── data/                  ← CSV files save here
    └── MID_*.csv
```

---

## 🔧 Troubleshooting

### ❌ "node is not recognized..."
**Problem:** Node.js not installed or not in PATH  
**Solution:** 
1. Install Node.js from https://nodejs.org/
2. Restart your computer
3. Try again

### ❌ "npm install" fails
**Problem:** No internet connection or firewall blocking  
**Solution:**
1. Check internet connection
2. Disable antivirus/firewall temporarily
3. Try running `INSTALL.bat` as Administrator (right-click → Run as Administrator)

### ❌ App shows black screen
**Problem:** Config files not found  
**Solution:**
1. Make sure `mid_config.yml` and `text_content.yml` are in the parent folder (MID/)
2. Make sure `images/` folder exists with all images

### ❌ Data not saving
**Problem:** No write permission  
**Solution:**
1. Run the app as Administrator
2. Or move the MID folder to Documents

---

## ✅ All Done!

You're ready to run experiments!

**Quick Summary:**
1. ✅ Install Node.js (one time)
2. ✅ Double-click `INSTALL.bat` (one time)
3. ✅ Double-click `START.bat` (every time you want to run)
4. ✅ Edit config files anytime between runs

---

## 🆚 What's the Difference?

| Method | Use When |
|--------|----------|
| **START.bat** | Testing, development, you have Node.js |
| **BUILD.bat → Installer** | Distributing to PCs without Node.js |

Both run the same experiment!

---

**Need help? Check the full README.md for details!**

**Viel Erfolg!** 🎉

