# MID Task - PsychoJS (Web Browser) Version

This is the web browser version of the Monetary Incentive Delay (MID) task, implemented in JavaScript using PsychoJS. It corresponds to the Python version (`mid_psychopy_pc_yaml.py`) and shares the same configuration files.

---

## 🌐 Overview

The PsychoJS version allows you to run the MID experiment:
- **In a web browser** (Chrome, Firefox, Safari, Edge)
- **Online** via Pavlovia or any web server
- **Offline** by opening the HTML file locally
- **Without Python installation** on participant computers

---

## 📁 Files

### Core PsychoJS Files
- `mid_psychojs.html` - Main HTML file to open in browser
- `mid_psychojs.js` - JavaScript experiment code
- `mid_psychojs.css` - Styling for the web interface

### Shared Configuration Files
- `mid_config.yml` - Experiment parameters (shared with Python version)
- `text_content.yml` - Text content in German (shared with Python version)
- `images/` - All stimulus images (shared with Python version)

---

## 🚀 Running the Experiment

### Option 1: Local (Offline)

1. **Open in browser**:
   ```bash
   # Simply open the HTML file in your browser
   open mid_psychojs.html
   # or double-click mid_psychojs.html
   ```

2. **Or use a local server** (recommended for better resource loading):
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Then open: http://localhost:8000/mid_psychojs.html
   ```

### Option 2: Online (Pavlovia)

1. **Upload to Pavlovia**:
   - Create a project on [Pavlovia.org](https://pavlovia.org/)
   - Upload all files (HTML, JS, CSS, YAML, images)
   - Set the project to "RUNNING"
   - Share the experiment URL with participants

2. **Or use any web server**:
   - Upload files to your web server
   - Ensure all files maintain the same directory structure
   - Access via the server URL

---

## ✅ Features

### ✓ Same as Python Version
- ✅ YAML-driven configuration
- ✅ Image-based stimuli (cues, target, feedback)
- ✅ Adaptive staircase (1-up/2-down)
- ✅ R-Score rule support
- ✅ Dual feedback (performance + monetary)
- ✅ Randomized timing intervals
- ✅ CSV data export
- ✅ German text interface

### ✓ Web-Specific Features
- ✅ Runs in any modern browser
- ✅ No installation required for participants
- ✅ Automatic CSV download at end
- ✅ Cross-platform (Windows, Mac, Linux, tablets)
- ✅ Online or offline capability

---

## 📊 Data Output

Data is automatically downloaded as a CSV file when the experiment ends:
- **Filename**: `MID_WEB_<participant>_<session>_<timestamp>.csv`
- **Format**: Same as Python version
- **Location**: Browser's download folder

---

## 🔧 Configuration

The PsychoJS version uses the same `mid_config.yml` and `text_content.yml` files as the Python version. Any changes to these files affect both versions.

See the main [README.md](README.md) for detailed configuration documentation.

---

## 🌐 Browser Requirements

### Recommended Browsers
- **Chrome** 90+ (best performance)
- **Firefox** 88+
- **Safari** 14+
- **Edge** 90+

### Required Browser Features
- JavaScript enabled
- WebGL support
- Local storage enabled
- Pop-ups allowed (for data download)

---

## 🔒 Privacy & Security

### Local Mode
- All data stays on the participant's computer
- No data sent to external servers
- CSV download directly to computer

### Online Mode (Pavlovia)
- Data stored on Pavlovia servers
- Complies with GDPR
- Secure HTTPS connection
- See [Pavlovia Privacy Policy](https://pavlovia.org/docs/about/privacy)

---

## 🐛 Troubleshooting

### Images Not Loading
- Ensure all image files are in the `images/` folder
- Check that image paths in `mid_config.yml` are correct
- Use a local web server instead of opening HTML directly

### Performance Issues
- Use Chrome for best performance
- Close other browser tabs
- Disable browser extensions
- Check WebGL support: [webglreport.com](https://webglreport.com/)

### Keys Not Detected
- Click on the experiment window to focus it
- Try refreshing the page
- Check browser console for errors (F12)

---

## 🔄 Python vs JavaScript Versions

| Feature | Python Version | PsychoJS Version |
|---------|---------------|------------------|
| **Runs On** | Local computer | Web browser |
| **Installation** | Python + PsychoPy required | No installation needed |
| **Timing Precision** | Very high (< 1ms) | Good (< 10ms) |
| **Offline Use** | ✅ Yes | ✅ Yes |
| **Online Use** | ❌ No | ✅ Yes |
| **Data Storage** | Local CSV file | Download CSV file |
| **Configuration** | Same YAML files | Same YAML files |
| **Stimuli** | Same images | Same images |

---

## 📝 Development Notes

### Converting Python to JavaScript
The PsychoJS version was created to match the Python version exactly:
- Same trial structure and timing
- Same staircase algorithm
- Same R-Score implementation
- Same data output format
- Same configuration system

### Key Differences
1. **Timing**: JavaScript uses `requestAnimationFrame` for timing (browser-dependent)
2. **File I/O**: CSV download instead of direct file writing
3. **Libraries**: PsychoJS instead of PsychoPy
4. **Async**: Heavy use of Promises and async/await

---

## 🆘 Support

For issues specific to:
- **PsychoJS**: [PsychoJS Forum](https://discourse.psychopy.org/)
- **Pavlovia**: [Pavlovia Support](https://pavlovia.org/docs)
- **This Implementation**: Check main README or create an issue

---

## 👤 Author

Developed by **Prof. Dr. Carsten M. Klingner** (Jena University Hospital)  
PsychoJS version created: 2025-10-08

