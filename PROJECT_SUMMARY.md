# MID Task - Project Summary

## 📋 Overview

This project contains a complete implementation of the Monetary Incentive Delay (MID) task in **two versions**:

1. **Python/PsychoPy** - For local computers with high timing precision
2. **JavaScript/PsychoJS** - For web browsers, online or offline

Both versions share the same configuration files and produce identical data output.

---

## 📁 Complete File Structure

```
MID/
│
├── 🐍 Python/PsychoPy Version
│   ├── mid_psychopy_pc_yaml.py     # Main experiment script
│   ├── config_loader.py            # Configuration validation
│   └── utils.py                    # Helper functions (staircase, timing)
│
├── 🌐 JavaScript/PsychoJS Version
│   ├── mid_psychojs.html           # Main HTML file (entry point)
│   ├── mid_psychojs.js             # Experiment logic (2000+ lines)
│   └── mid_psychojs.css            # Web interface styling
│
├── ⚙️ Shared Configuration
│   ├── mid_config.yml              # All experiment parameters
│   └── text_content.yml            # German text content
│
├── 🖼️ Stimulus Images
│   └── images/
│       ├── Cue00.png               # Neutral cue
│       ├── Cue03.png               # Low reward cue
│       ├── Cue30.png               # High reward cue
│       ├── Taler3.png              # Low reward anticipation
│       ├── Taler12.png             # High reward anticipation
│       ├── Target.png              # Target stimulus
│       ├── PerformanceFeedbackPositiv.png   # Hit feedback
│       ├── PerformanceFeedbackNegativ.png   # Miss feedback
│       └── schatztruhebw.png       # Monetary feedback (treasure)
│
├── 📖 Documentation
│   ├── README.md                   # Main documentation (360+ lines)
│   ├── README_PsychoJS.md          # Web version details
│   ├── QUICKSTART.md               # Quick start guide
│   ├── Windows_Deployment_Guide.md # Windows deployment
│   ├── Complete_Setup_Guide.md     # Full setup instructions
│   └── PROJECT_SUMMARY.md          # This file
│
├── 🔧 Development Files
│   ├── environment.yml             # Conda environment spec
│   ├── build_windows.sh            # Windows build script
│   ├── install_pip.bat             # Pip installer for Windows
│   ├── run_experiment.bat          # Windows launcher
│   ├── MID_Experiment.spec         # PyInstaller spec (Linux)
│   └── MID_Experiment_Windows.spec # PyInstaller spec (Windows)
│
└── 📊 Data Output
    └── data/                       # CSV files (auto-created)
        └── MID_PC_*.csv            # Trial-by-trial data
```

---

## 🎯 Key Features

### ✅ Both Versions Support
- YAML-driven configuration
- Image-based stimuli (cues, target, feedback)
- Adaptive staircase (1-up/2-down) for ~70% hit rate
- R-Score rule for dynamic difficulty adjustment
- Dual feedback (performance + monetary)
- Randomized timing intervals
- CSV data export
- German text interface
- ESC key to abort safely

### 🐍 Python-Specific
- Very high timing precision (< 1ms)
- Guaranteed 60+ FPS
- Direct CSV file writing
- Works in WSL (with some limitations)
- Full keyboard control

### 🌐 JavaScript-Specific
- Runs in any modern browser
- No installation required
- Online capability (Pavlovia)
- Cross-platform (Windows, Mac, Linux, tablets)
- Automatic CSV download

---

## 📊 Trial Structure (7 Phases)

```
1. Cue Presentation        (250ms)          → Shows reward type
2. Pause 1                 (750-1250ms)     → Anticipation
3. Target + Response       (500ms adaptive) → Press spacebar!
4. Pause 2                 (800-1200ms)     → Pre-feedback delay
5. Performance Feedback    (1000ms)         → Hit or miss
6. Monetary Feedback       (1000ms)         → +30¢, +3¢, or +0¢
7. Pause 3                 (1500-2000ms)    → Inter-trial interval

Total: ~5.8-7.2 seconds per trial
```

---

## ⚙️ Configuration Highlights

### Conditions
- **WIN_HIGH**: 30 cents (high reward)
- **WIN_LOW**: 3 cents (low reward)  
- **NEUTRAL**: 0 cents (neutral)

### Adaptive Timing
- Initial target: 500ms
- Adaptive range: 120-900ms
- Step size: 20ms
- 1-up/2-down staircase

### Task Structure
- 2 blocks × 36 trials = 72 trials total
- ~8-10 minutes total duration
- Practice trials: configurable

---

## 🚀 Quick Start

### Python Version
```bash
conda activate mid_env
python mid_psychopy_pc_yaml.py
```

### JavaScript Version
```bash
open mid_psychojs.html
# or
python -m http.server 8000
```

---

## 📈 Data Output

Both versions produce identical CSV format:

| Column | Description |
|--------|-------------|
| participant, session | Identifiers |
| block, trial_index | Trial position |
| condition | WIN_HIGH, WIN_LOW, NEUTRAL |
| valence, magnitude | Condition properties |
| target_ms_pre, target_ms_final | Target duration (before/after R-Score) |
| rt_ms | Reaction time in milliseconds |
| hit | 1 = success, 0 = miss |
| points_change, points_total | Points earned |
| pause1_ms, pause2_ms, pause3_ms | Actual jitter values |
| rscore_scope, rscore_value | R-Score tracking |

---

## 🔄 Version Comparison

| Aspect | Python | JavaScript |
|--------|--------|------------|
| **Timing Precision** | < 1ms | ~10ms |
| **Platform** | Local | Web browser |
| **Installation** | Required | None |
| **Online Use** | No | Yes |
| **Best For** | Lab studies | Online studies |

---

## 👤 Project Info

**Author**: Prof. Dr. Carsten M. Klingner  
**Institution**: Jena University Hospital  
**Language**: Python 3.10 / JavaScript ES6  
**Frameworks**: PsychoPy / PsychoJS  
**Configuration**: YAML  
**Version**: 2.0 (Dual implementation)  
**Date**: October 2025

---

## 📖 Documentation

- **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)
- **Full Documentation**: See [README.md](README.md)
- **PsychoJS Details**: See [README_PsychoJS.md](README_PsychoJS.md)
- **Windows Deployment**: See [Windows_Deployment_Guide.md](Windows_Deployment_Guide.md)

---

## 🎓 Citation

If you use this implementation in your research, please cite:

```
Klingner, C. M. (2025). Monetary Incentive Delay (MID) Task - 
Dual Implementation (PsychoPy & PsychoJS). 
Jena University Hospital.
```

---

## 📝 License

This project is provided for research and educational purposes.

---

**Both versions are production-ready and fully tested!** 🎉

