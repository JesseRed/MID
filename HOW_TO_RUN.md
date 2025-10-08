# 🎯 MID Task - How to Run

You have **TWO** versions of the MID task. Choose the one that fits your needs:

---

## 🖥️ Option 1: Electron Desktop App (RECOMMENDED for Windows)

**Best for:** Running on Windows PCs, distributing to participants, no server needed

### ✨ Advantages:
- ✅ No web server required
- ✅ Works offline
- ✅ Easy to distribute (Windows installer)
- ✅ Config files can be edited anytime
- ✅ Data saves automatically to disk
- ✅ Native desktop app

### 🚀 Quick Start:

**On Windows:**
1. Go to `electron-app` folder
2. Double-click `INSTALL.bat` (first time only)
3. Double-click `START.bat` to run

**Full instructions:** See `electron-app/WINDOWS_QUICKSTART.md`

---

## 🌐 Option 2: Web Browser Version

**Best for:** Quick testing, running on any OS, when you have Python

### ✨ Advantages:
- ✅ No installation needed (except Python)
- ✅ Works on any OS (Windows, Mac, Linux)
- ✅ Quick setup
- ✅ Good for development/testing

### 🚀 Quick Start:

**From terminal/command prompt:**
```bash
cd /path/to/MID
python -m http.server 8000
```

**Then open in browser:**
```
http://localhost:8000/mid_web.html
```

**Full instructions:** See `WINDOWS_WEB_QUICKSTART.md`

---

## 📊 Comparison Table

| Feature | Electron App | Web Browser |
|---------|--------------|-------------|
| **Requires server** | ❌ No | ✅ Yes |
| **Requires installation** | ✅ Node.js + npm install | ✅ Python |
| **Distributable** | ✅ Yes (.exe installer) | ❌ No |
| **Data saving** | ✅ Auto to disk | ⚠️ Browser download |
| **Editable configs** | ✅ Yes | ✅ Yes |
| **Fullscreen** | ✅ Native | ✅ Browser fullscreen |
| **Best for** | Production use | Testing/development |

---

## 🎓 Which Should I Use?

### Use **Electron App** if:
- ✅ You're running experiments on Windows
- ✅ You want to distribute to multiple PCs
- ✅ You don't want to deal with servers
- ✅ You want automatic data saving
- ✅ You want a professional desktop experience

### Use **Web Version** if:
- ✅ You're just testing
- ✅ You need cross-platform support
- ✅ You already have Python
- ✅ You want quick iterations during development

---

## 📝 Editing Configuration (Both Versions)

Both versions use the **same config files**:

### `mid_config.yml` - Experiment settings
- Number of blocks and trials
- Timing parameters
- Point values
- Staircase settings
- Image paths

### `text_content.yml` - Text and instructions
- Welcome messages
- Task instructions
- Feedback messages

**To edit:**
1. Open the `.yml` files in any text editor
2. Make changes
3. Save
4. Restart the app/reload the page

---

## 📁 Folder Structure

```
MID/
│
├── electron-app/              ← Electron Desktop App
│   ├── INSTALL.bat            ← Windows: Run first
│   ├── START.bat              ← Windows: Run to start
│   ├── BUILD.bat              ← Windows: Build installer
│   ├── WINDOWS_QUICKSTART.md  ← Quick guide
│   └── README.md              ← Full documentation
│
├── mid_web.html               ← Web browser version
├── mid_web.js                 ← Web version logic
├── WINDOWS_WEB_QUICKSTART.md  ← Web version guide
│
├── mid_config.yml             ← Experiment configuration
├── text_content.yml           ← Text/instructions
│
├── images/                    ← Stimuli images
│   ├── Taler0.png
│   ├── Taler3.png
│   ├── Taler12.png
│   └── ...
│
└── data/                      ← CSV output files
    └── MID_*.csv
```

---

## 🚀 Quick Decision Tree

```
Do you need to distribute to multiple Windows PCs?
├─ YES → Use Electron App
│         Go to: electron-app/WINDOWS_QUICKSTART.md
│
└─ NO → Are you just testing/developing?
    ├─ YES → Use Web Version
    │         Go to: WINDOWS_WEB_QUICKSTART.md
    │
    └─ NO → Still use Electron App for production
            Go to: electron-app/WINDOWS_QUICKSTART.md
```

---

## 🎉 Get Started!

**Electron App (Recommended):**
```bash
cd electron-app
# Windows: Double-click INSTALL.bat, then START.bat
# Linux/Mac: npm install, then npm start
```

**Web Version:**
```bash
python -m http.server 8000
# Then open: http://localhost:8000/mid_web.html
```

---

**Both versions work great - choose what fits your workflow!** ✨

