# MID Task - Electron Desktop App

🎯 **Standalone desktop application** for the Monetary Incentive Delay (MID) task that works without a web server.

---

## ✨ Features

- ✅ **No web server required** - runs as a native desktop app
- ✅ **Editable config files** - modify `mid_config.yml` and `text_content.yml` anytime
- ✅ **Automatic data saving** - CSV files saved to `/data` folder
- ✅ **Fullscreen mode** - immersive experiment experience
- ✅ **ESC key support** - quit anytime with confirmation
- ✅ **Windows installer** - easy distribution to participants

---

## 📋 Prerequisites

### For Running in Development:
- **Node.js** (version 16 or higher)
  - Download from: https://nodejs.org/

### For Building Windows Executable:
- Same as above
- Runs on Windows, macOS, or Linux (can build for Windows from any platform)

---

## 🚀 Quick Start (Development)

### 1. Install Dependencies

Open a terminal in the `electron-app` folder and run:

```bash
cd electron-app
npm install
```

This will install Electron and all required dependencies.

### 2. Run the App

```bash
npm start
```

The app will launch in fullscreen mode, ready to run the experiment!

---

## 📦 Building Windows Executable

### Build a Windows Installer

From the `electron-app` folder:

```bash
npm run build
```

This creates a Windows installer in `electron-app/dist/`

**Output files:**
- `MID Task Setup X.X.X.exe` - Installer for participants
- The installer is self-contained and doesn't require Node.js

### Installation on Windows

1. Copy the `.exe` installer to a Windows PC
2. Double-click to install
3. The app will be installed in `C:\Program Files\MID Task\`
4. A desktop shortcut will be created
5. Launch the app and run experiments!

---

## 📁 Folder Structure

```
MID/
├── electron-app/              ← Electron app folder
│   ├── main.js                ← Electron main process
│   ├── preload.js             ← Secure API bridge
│   ├── mid_web_electron.html  ← UI
│   ├── mid_web_electron.js    ← Experiment logic
│   ├── package.json           ← Dependencies & build config
│   ├── README.md              ← This file
│   └── dist/                  ← Build output (after npm run build)
│
├── mid_config.yml             ← Experiment configuration (EDITABLE)
├── text_content.yml           ← Text/instructions (EDITABLE)
├── images/                    ← Stimuli images
│   ├── Taler0.png
│   ├── Taler3.png
│   ├── Taler12.png
│   ├── Target.png
│   └── ...
└── data/                      ← CSV data files (auto-created)
    └── MID_<participant>_<session>_<timestamp>.csv
```

---

## 🎮 How to Use

### Running an Experiment

1. **Launch the app** (development: `npm start`, or use the installed .exe)
2. **Enter participant info:**
   - Participant ID
   - Session number (default: 001)
3. **Click Start**
4. **Follow instructions** and complete the task
5. **Data is automatically saved** to the `data/` folder
6. **ESC key** to quit early (with confirmation)

### Editing Configuration

You can edit the config files **before** launching the app:

**`mid_config.yml`** - Experiment parameters:
- Number of blocks
- Trials per block
- Timing settings
- Staircase parameters
- Point values

**`text_content.yml`** - Instructions and messages:
- Welcome text
- Task instructions
- Block messages
- End messages

**Changes take effect** the next time you launch the app.

---

## 🔧 Development

### File Overview

| File | Purpose |
|------|---------|
| `main.js` | Electron main process - creates window, handles file I/O |
| `preload.js` | Secure bridge between renderer and main process |
| `mid_web_electron.html` | User interface and styling |
| `mid_web_electron.js` | Experiment logic and flow |
| `package.json` | Dependencies and build configuration |

### Modifying the Experiment

1. Edit `mid_web_electron.js` for logic changes
2. Edit `mid_web_electron.html` for UI changes
3. Test with `npm start`
4. Build with `npm run build` when ready

### Debugging

To enable developer tools, edit `main.js` line 20:

```javascript
// Uncomment this line:
mainWindow.webContents.openDevTools();
```

---

## 📊 Data Output

CSV files are saved to: `MID/data/`

**Filename format:** `MID_<participant>_<session>_<timestamp>.csv`

**Columns:**
- `participant` - Participant ID
- `session` - Session number
- `timestamp` - Trial timestamp
- `block` - Block number
- `trial_index` - Trial number
- `condition` - Condition label
- `valence` - Gain/loss/neutral
- `magnitude` - Reward magnitude
- `target_ms_pre` - Target duration before adaptation
- `target_ms_final` - Target duration after adaptation
- `rt_ms` - Reaction time (milliseconds)
- `hit` - Hit (1) or miss (0)
- `points_change` - Points gained/lost
- `points_total` - Total points
- `key_pressed` - Key pressed
- `rscore_value` - Running success rate

---

## 🛠️ Troubleshooting

### "npm not found"
**Solution:** Install Node.js from https://nodejs.org/

### "electron not found" 
**Solution:** Run `npm install` in the `electron-app` folder

### Black screen / Nothing happens
**Solution:** 
- Check the console for errors (`npm start` with devTools enabled)
- Ensure `mid_config.yml` and `text_content.yml` are in the parent directory
- Ensure `images/` folder exists with all required images

### Config changes not applied
**Solution:** Quit and restart the app (configs are loaded on startup)

### Data not saving
**Solution:** 
- Check that the app has write permissions
- The `data/` folder is created automatically in the app's directory
- After installation, data is saved to the installation directory

---

## 🆚 Electron vs. Web Version

| Feature | Electron App | Web Version |
|---------|--------------|-------------|
| **Requires server?** | ❌ No | ✅ Yes (`python -m http.server`) |
| **Editable configs** | ✅ Yes, anytime | ✅ Yes, but server must serve them |
| **Distributable** | ✅ Yes, .exe installer | ❌ Requires setup |
| **File access** | ✅ Direct | ❌ Fetch API (CORS issues) |
| **Data saving** | ✅ Automatic to disk | ⚠️ Browser download |
| **Best for** | ✅ **Production/Distribution** | ✅ Quick testing |

**→ Use Electron for running actual experiments!**

---

## 📝 License

MIT License - feel free to modify and distribute.

---

## 🎉 Ready to Go!

```bash
# Development:
cd electron-app
npm install
npm start

# Build for Windows:
npm run build

# Distribute:
# Copy electron-app/dist/MID Task Setup X.X.X.exe to Windows PCs
```

**Viel Erfolg mit Ihren Experimenten!** 🚀

