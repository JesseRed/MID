# Monetary Incentive Delay (MID) Task — PsychoPy (YAML Version)

This repository contains a **PC-only implementation of the Monetary Incentive Delay (MID) task** written in [PsychoPy](https://www.psychopy.org/).  
It is designed for **behavioral use** (no MRI/EEG/MEG integration) and supports **parameter control via YAML configuration**.

---

## 🧠 Overview
 
The MID paradigm measures motivational and reward-related behavior.  
Participants respond as quickly as possible to a brief target to **gain rewards** or **avoid losses** based on pre-cues.

This version is:
- ✅ Fully configurable via `mid_config.yml`
- ✅ Cross-platform (Windows, Linux, macOS; WSL2 tested)
- ✅ Adaptive (1-up / 2-down staircase for ~70% hit rate)
- ✅ Clean CSV logging
- ✅ Supports an *R-Score rule* (dynamic target shortening for high performers)
- ✅ ESC-abort safe (graceful shutdown & log flush)
- ✅ WSL-friendly (no frame-rate sync / PTB-realtime requirements)

---

## 🧩 Structure

```
MID/
│
├── mid_psychopy_pc_yaml.py     # main PsychoPy task script (YAML-driven)
├── mid_config.yml              # all parameters (timing, points, staircase, visuals)
└── data/                       # automatically created folder for CSV log files
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/JesseRed/MID.git
cd MID
```

### 2️⃣ Create a conda environment
```bash
conda create -n mid_env python=3.10
conda activate mid_env
```

### 3️⃣ Install dependencies
```bash
conda install -c conda-forge psychopy pyyaml
```

### 4️⃣ Run the task
```bash
python mid_psychopy_pc_yaml.py --config mid_config.yml
```

---

## 🧾 Configuration (mid_config.yml)

All task parameters are stored in the YAML file.  
You can adapt nearly everything without touching the code.

### 🪟 Window
```yaml
win:
  size: [1280, 720]
  fullscr: false
  screen_color: "black"
  text_color: "white"
  fixation_color: "white"
  font: "Arial"
  waitBlanking: false
  checkTiming: false
  useFBO: false
```

### ⏱ Timing (all in ms)
```yaml
timings:
  cue_ms: 250
  pause1_ms_range: [750, 1250]
  pause2_ms_range: [800, 1200]
  pause3_ms_range: [2000, 3000]
  feedback_ms: 500
```

### 🧮 Staircase (adaptive target duration)
```yaml
staircase:
  initial_ms: 250
  min_ms: 120
  max_ms: 900
  step_ms: 10
  per_condition_max_ms: {}
```

### 🎯 R-Score Rule (performance scaling)
```yaml
rscore:
  enabled: true
  window: 20
  threshold: 75.0
  scale: 0.9
  scope: "global"
```

### 🧍 Task structure
```yaml
task:
  n_blocks: 2
  trials_per_block: 36
  resp_keys: ["space"]
  show_cumulative_points: true
  practice_trials: 0
```

### 💡 Visuals
```yaml
visuals:
  target_symbol: "◉"
  cue_symbols: { "+1": "＋", "-1": "－", "0": "○" }
  target_font_height: 0.12
  cue_font_height: 0.12
  text_font_height: 0.06
```

### 💰 Points and conditions
```yaml
points:
  start: 0

conditions:
  - ["WIN_LOW",    1, 1,  10,  0]
  - ["WIN_HIGH",   1, 5,  50,  0]
  - ["AVOID_LOW", -1, 1,   0, -10]
  - ["AVOID_HIGH",-1, 5,   0, -50]
  - ["NEUTRAL",    0, 0,   0,   0]
```

---

## 🧠 Trial Timeline

### ⏱️ Complete Trial Timing Sequence

Each trial follows a precise 7-phase sequence designed to create anticipation, measure response time, and provide clear feedback:

#### **Phase 1: Cue Presentation**
- **Duration**: `cue_ms = 250ms`
- **What happens**: The cue image appears (e.g., treasure chest for high reward)
- **Purpose**: Signals to participant what type of reward they can earn

#### **Phase 2: Pause 1 (Pre-Target)**
- **Duration**: `pause1_ms_range = [750, 1250]ms` (randomized)
- **What happens**: Fixation cross (+) is shown
- **Purpose**: Variable delay before target appears (anticipation period)

#### **Phase 3: Target Presentation + Response**
- **Duration**: `target_ms` (varies, starts at 500ms, adapts via staircase)
- **What happens**: Target image appears, participant presses spacebar
- **Purpose**: The actual task - quick response to earn reward

#### **Phase 4: Pause 2 (Anticipation)**
- **Duration**: `pause2_ms_range = [800, 1200]ms` (randomized)
- **What happens**: Fixation cross (+) is shown
- **Purpose**: Brief delay before feedback (builds anticipation)

#### **Phase 5: Performance Feedback**
- **Duration**: `feedback_ms = 1000ms`
- **What happens**: Shows if response was fast enough (hit/miss image)
- **Purpose**: Immediate feedback on performance

#### **Phase 6: Monetary Feedback**
- **Duration**: `feedback_ms = 1000ms`
- **What happens**: Shows reward amount (+30 Cent, +3 Cent, +0 Cent) with image
- **Purpose**: Shows how much money was earned

#### **Phase 7: Pause 3 (Post-Feedback)**
- **Duration**: `pause3_ms_range = [1500, 2000]ms` (randomized)
- **What happens**: Fixation cross (+) is shown
- **Purpose**: Processing time before next trial

### 📊 Visual Timeline

```
Trial Start
    ↓
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│    Cue      │  │   Pause 1   │  │   Target    │  │   Pause 2   │  │ Performance │  │  Monetary   │  │   Pause 3   │
│   (250ms)   │  │(750-1250ms) │  │(500ms±)     │  │(800-1200ms) │  │  Feedback   │  │  Feedback   │  │(1500-2000ms)│
│             │  │             │  │             │  │             │  │  (1000ms)   │  │  (1000ms)   │  │             │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
    ↓              ↓              ↓              ↓              ↓              ↓              ↓
  Cue Image    Fixation (+)    Target Image   Fixation (+)   Hit/Miss      Reward Amount   Fixation (+)
  (Treasure)                   (Press Space)                 Image          (+30 Cent)     Next Trial
```

### ⏱️ Total Trial Duration

- **Minimum**: 250 + 750 + 500 + 800 + 1000 + 1000 + 1500 = **5800ms (5.8 seconds)**
- **Maximum**: 250 + 1250 + 500 + 1200 + 1000 + 1000 + 2000 = **7200ms (7.2 seconds)**
- **Average**: ~6.5 seconds per trial

### 🎯 Key Timing Features

1. **Variable Delays**: Pauses 1, 2, and 3 are randomized to prevent anticipation
2. **Adaptive Target**: Target duration changes based on performance (staircase)
3. **Dual Feedback**: Both performance (hit/miss) and monetary (cents earned) feedback
4. **Anticipation**: Pause 2 creates anticipation before feedback
5. **Processing Time**: Pause 3 allows time to process the feedback before next trial

### 📋 Configuration Variables

| Phase | YAML Variable | Default Value | Description |
|-------|---------------|---------------|-------------|
| Cue | `cue_ms` | 250ms | Cue image display duration |
| Pause 1 | `pause1_ms_range` | [750, 1250]ms | Pre-target fixation (randomized) |
| Target | `staircase.initial_ms` | 500ms | Initial target duration (adapts) |
| Pause 2 | `pause2_ms_range` | [800, 1200]ms | Pre-feedback anticipation (randomized) |
| Performance Feedback | `feedback_ms` | 1000ms | Hit/miss feedback duration |
| Monetary Feedback | `feedback_ms` | 1000ms | Reward amount feedback duration |
| Pause 3 | `pause3_ms_range` | [1500, 2000]ms | Post-feedback processing (randomized) |

---

## 📊 Output

Each run produces one CSV file in the `data/` folder:  
`MID_PC_<participant>_<session>_<timestamp>.csv`

### Columns
| Column | Description |
|---------|-------------|
| participant, session | Identifiers |
| block, trial_index | Trial info |
| condition, valence, magnitude | Trial type |
| target_ms_pre, target_ms_final | Target duration before/after scaling |
| rt_ms | Reaction time (ms) |
| hit | 1 = success, 0 = miss |
| points_change, points_total | Point gain/loss |
| pause1_ms…pause3_ms | Actual jitters |
| cue_ms, feedback_ms | Fixed durations |
| key_pressed | Detected key |
| rscore_scope, rscore_value | R-Score settings / last computed hit rate |

---

## 🔒 Safety Features

- **ESC**: Abort anytime → graceful shutdown, file flushed and closed.
- **No PTB realtime thread issues** (suitable for WSL2 and standard Linux).
- **No GPU sync blocking** (`waitBlanking=False`).

---

## 🧰 Developer Notes

### Run with debug prints
```bash
python -u mid_psychopy_pc_yaml.py --config mid_config.yml
```

### Change config file dynamically
```bash
python mid_psychopy_pc_yaml.py --config configs/mid_config_alt.yml
```

### Disable staircase (fixed target)
```yaml
staircase:
  step_ms: 0
  initial_ms: 300
```

---

## 🧩 Possible Extensions

- Add separate **practice.yaml** for short demo runs.  
- Include **response feedback sounds**.  
- Log **trial-wise R-Score evolution**.  
- Export performance summary at the end.  
- Visualize CSV data in a Jupyter notebook.

---

## 👤 Author

Developed by **Prof. Dr. Carsten M. Klingner** (Jena University Hospital)  
Structured with ChatGPT (GPT-5).  
Version: `v2.1-YAML` — 2025-10-07
