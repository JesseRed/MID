# MID Task - Quick Start Guide

Choose your version based on your needs:

---

## 🐍 Python Version (High Precision)

**Best for:** Lab computers, precise timing requirements

### Quick Start (3 steps)
```bash
# 1. Install dependencies
conda create -n mid_env python=3.10
conda activate mid_env
conda install -c conda-forge psychopy pyyaml

# 2. Run experiment
python mid_psychopy_pc_yaml.py

# 3. Find data
# Results saved in: data/MID_PC_<participant>_<session>_<timestamp>.csv
```

### System Requirements
- Python 3.10+
- Windows, macOS, or Linux (including WSL)
- ~500 MB disk space

---

## 🌐 JavaScript Version (Web Browser)

**Best for:** Online studies, remote testing, no installation

### Quick Start (1 step)
```bash
# Option 1: Open directly
open mid_psychojs.html

# Option 2: Use local server (recommended)
python -m http.server 8000
# Then open: http://localhost:8000/mid_psychojs.html
```

### Browser Requirements
- Chrome 90+, Firefox 88+, Safari 14+, or Edge 90+
- JavaScript enabled
- WebGL support

---

## 📊 Both Versions Use Same Files

### Configuration
- `mid_config.yml` - All experiment parameters
- `text_content.yml` - German text content
- `images/` - All stimulus images

### Data Output
Both produce identical CSV format with:
- Participant info
- Trial-by-trial data
- Reaction times
- Hit/miss outcomes
- Points earned
- Timing parameters

---

## 🎯 Which Version Should I Use?

### Use Python Version If:
- ✅ Running in a controlled lab environment
- ✅ Need precise timing (< 1ms accuracy)
- ✅ Participants use dedicated computers
- ✅ Comfortable with Python/terminal

### Use JavaScript Version If:
- ✅ Running online studies
- ✅ Remote/distributed testing
- ✅ Participants use their own devices
- ✅ Want no installation for participants
- ✅ Need cross-platform compatibility

### Use Both If:
- ✅ Want pilot testing online, main study in lab
- ✅ Need flexibility for different contexts
- ✅ Want to compare performance across platforms

---

## ⚙️ Customization

Edit `mid_config.yml` to change:
```yaml
# Timing
timings:
  cue_ms: 250                    # Cue duration
  pause1_ms_range: [750, 1250]   # Pre-target delay
  feedback_ms: 1000              # Feedback duration

# Task structure
task:
  n_blocks: 2                    # Number of blocks
  trials_per_block: 36           # Trials per block

# Rewards
conditions:
  - ["WIN_LOW",  1, 1,  3,  0]   # Low reward: 3 cents
  - ["WIN_HIGH", 1, 5, 30,  0]   # High reward: 30 cents
  - ["NEUTRAL",  0, 0,  0,  0]   # Neutral: 0 cents
```

Changes apply to **both** Python and JavaScript versions!

---

## 🆘 Quick Troubleshooting

### Python Version
**Problem:** Keys not detected in WSL  
**Solution:** Run on native Windows/Mac/Linux (not WSL)

**Problem:** Import errors  
**Solution:** `conda activate mid_env`

### JavaScript Version
**Problem:** Images not loading  
**Solution:** Use local server: `python -m http.server 8000`

**Problem:** Keys not detected  
**Solution:** Click experiment window to focus

---

## 📖 Full Documentation

- **Main README**: [README.md](README.md) - Complete documentation
- **PsychoJS README**: [README_PsychoJS.md](README_PsychoJS.md) - Web version details
- **Windows Deployment**: [Windows_Deployment_Guide.md](Windows_Deployment_Guide.md) - Windows setup

---

## 🎮 Test Run

### Python
```bash
conda activate mid_env
python mid_psychopy_pc_yaml.py
# Enter: participant=test, session=001
# Press spacebar when target appears
# Press ESC to exit early
```

### JavaScript
```bash
open mid_psychojs.html
# Fill in participant info
# Press spacebar when target appears
# Complete or close browser tab
```

---

**Ready to run? Pick your version and start testing!** 🚀

