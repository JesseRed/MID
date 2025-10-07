#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PC-only Monetary Incentive Delay (MID) task implemented in PsychoPy.
- No MRI/EEG/MEG integration (pure behavioral).
- Adaptive target duration per condition (~66–70% hits via 1-up/2-down rule).
- Clean CSV logging.
- Simple points "payout" logic.
- ESC abort anywhere (clean shutdown).

Run:
    pip install psychopy
    python mid_psychopy_pc_v2.py

Author: ChatGPT (for Bro)
"""

from psychopy import visual, core, event, gui
import csv, random, os
from datetime import datetime

# ------------------------
# Config (edit as needed)
# ------------------------
CONFIG = {
    "screen_color": "black",
    "text_color": "white",
    "fixation_color": "white",
    "win_size": [1280, 720],          # set to None for full-screen
    "fullscr": False,
    "fps_hz": 60,                     # used only for sanity; PsychoPy uses high-res timers
    "iti_range_s": (1.50, 2.50),      # ITI jitter (uniform); adjust as desired
    "cue_dur_s": 0.25,                # cue presentation
    "anticipation_s": 2.00,           # delay before target
    "feedback_dur_s": 1.00,
    "n_blocks": 2,                    # number of blocks
    "trials_per_block": 36,           # total trials per block (divisible by n_conditions ideally)
    # Conditions: (label, valence, magnitude, points_on_hit, points_on_miss)
    "conditions": [
        ("WIN_LOW",   +1,  1,  +10,   0),
        ("WIN_HIGH",  +1,  5,  +50,   0),
        ("AVOID_LOW", -1,  1,    0, -10),
        ("AVOID_HIGH",-1,  5,    0, -50),
        ("NEUTRAL",    0,  0,    0,   0),
    ],
    # Adaptive target duration per condition
    "initial_target_ms": 250,         # starting target display duration
    "min_target_ms": 120,
    "max_target_ms": 400,
    "step_ms": 10,                    # step for staircase adjustments
    "target_symbol": "◉",             # unicode target
    "cue_symbols": {                  # what to draw per condition group
        +1: "＋",     # win
        -1: "－",     # avoid loss
         0: "○"      # neutral
    },
    "font": "Arial",
    "target_font_height": 0.12,       # in norm units (approx); adjust for visibility
    "cue_font_height": 0.12,
    "text_font_height": 0.06,
    "resp_keys": ["space"],           # response key(s)
    "points_start": 0,
    "show_cumulative_points": True,
    "practice_trials": 0              # set >0 for a short practice
}

# --------------
# Utilities
# --------------

def uniform_jitter(low, high):
    return random.uniform(low, high)

def timestamp():
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def make_trials(conditions, n_trials):
    """Create a list of condition labels for n_trials, balanced as evenly as possible."""
    n_cond = len(conditions)
    base = n_trials // n_cond
    rem = n_trials % n_cond
    trials = []
    # distribute remainder
    for i, cond in enumerate(conditions):
        count = base + (1 if i < rem else 0)
        trials.extend([cond[0]] * count)
    random.shuffle(trials)
    return trials

# Staircase: simple 1-up/2-down per condition to converge ~70.7%
class StaircaseAdaptive:
    def __init__(self, initial_ms, min_ms, max_ms, step_ms):
        self.value = initial_ms
        self.min_ms = min_ms
        self.max_ms = max_ms
        self.step = step_ms
        self._consecutive_hits = 0

    def update(self, hit):
        if hit:
            self._consecutive_hits += 1
            if self._consecutive_hits >= 2:
                self.value = max(self.min_ms, self.value - self.step)
                self._consecutive_hits = 0
        else:
            self.value = min(self.max_ms, self.value + self.step)
            self._consecutive_hits = 0

    def get_ms(self):
        return self.value

# ------------------------
# Participant dialog
# ------------------------
exp_info = {
    "participant": "",
    "session": "001"
}
try:
    dlg = gui.DlgFromDict(exp_info, title="MID Task (PC)")
    if not dlg.OK:
        core.quit()
except Exception:
    print("GUI unavailable – using defaults:", exp_info)

# ------------------------
# Output paths
# ------------------------
base_name = f"MID_PC_{exp_info['participant']}_{exp_info['session']}_{timestamp()}"
out_dir = "data"
os.makedirs(out_dir, exist_ok=True)
csv_path = os.path.join(out_dir, base_name + ".csv")

# ------------------------
# Window and stimuli (WSL-friendly)
# ------------------------
win = visual.Window(
    size=CONFIG["win_size"],
    fullscr=CONFIG["fullscr"],
    color=CONFIG["screen_color"],
    units="height",
    allowGUI=False,
    waitBlanking=False,   # prevents blocking on frame-sync under WSL
    checkTiming=False,    # skip frame rate measurement
    useFBO=False,         # reduce GL complexity under WSL
    autoLog=False
)

fixation = visual.TextStim(
    win, text="+", color=CONFIG["fixation_color"], height=CONFIG["text_font_height"], font=CONFIG["font"]
)

instr = visual.TextStim(
    win, text=(
        "Monetary Incentive Delay (MID)\n\n"
        "Wenn ein Hinweis erscheint, fixieren Sie die Mitte.\n"
        "Kurz darauf erscheint ein Ziel (Kreis). Drücken Sie so schnell wie möglich die Leertaste, "
        "solange das Ziel sichtbar ist.\n\n"
        "Sie können Punkte gewinnen oder Verluste vermeiden – je nach Hinweis.\n"
        "Drücken Sie eine Taste, um zu starten."
    ),
    color=CONFIG["text_color"], height=CONFIG["text_font_height"], wrapWidth=1.2, font=CONFIG["font"], alignText="center"
)

feedback_text = visual.TextStim(
    win, text="", color=CONFIG["text_color"], height=CONFIG["text_font_height"], font=CONFIG["font"]
)

cue_stim = visual.TextStim(
    win, text="", color=CONFIG["text_color"], height=CONFIG["cue_font_height"], font=CONFIG["font"]
)

target_stim = visual.TextStim(
    win, text=CONFIG["target_symbol"], color=CONFIG["text_color"], height=CONFIG["target_font_height"], font=CONFIG["font"]
)

points_total = CONFIG["points_start"]

# Map condition label -> meta and adaptive controller
cond_meta = {c[0]: {"valence": c[1], "magnitude": c[2], "points_hit": c[3], "points_miss": c[4]} for c in CONFIG["conditions"]}
cond_stair = {c[0]: StaircaseAdaptive(CONFIG["initial_target_ms"], CONFIG["min_target_ms"], CONFIG["max_target_ms"], CONFIG["step_ms"]) for c in CONFIG["conditions"]}
cond_symbol = {c[0]: CONFIG["cue_symbols"][c[1]] for c in CONFIG["conditions"]}

# ------------------------
# CSV logging
# ------------------------
csv_headers = [
    "participant","session","timestamp","block","trial_index","condition",
    "valence","magnitude","target_ms","rt_ms","hit","iti_s","anticipation_s",
    "points_change","points_total","key_pressed"
]
csv_file = open(csv_path, "w", newline="", encoding="utf-8")
writer = csv.writer(csv_file)
writer.writerow(csv_headers)

# ------------------------
# Abort helper
# ------------------------
def check_escape():
    """Check if ESC was pressed; cleanly abort if so."""
    if 'escape' in event.getKeys():
        print("Abbruch durch Benutzer (ESC) – speichere Daten und beende...")
        try:
            csv_file.flush()
            csv_file.close()
        except Exception:
            pass
        try:
            win.close()
        except Exception:
            pass
        core.quit()

# ------------------------
# Instruction screen
# ------------------------
instr.draw()
win.flip()
keys = event.waitKeys()
if 'escape' in keys:
    check_escape()

# ------------------------
# Optional practice
# ------------------------
def run_trial(trial_idx, block_idx, cond_label):
    global points_total
    meta = cond_meta[cond_label]
    stair = cond_stair[cond_label]
    target_ms = stair.get_ms()

    # ITI
    iti = uniform_jitter(*CONFIG["iti_range_s"])
    fixation.draw()
    win.flip()
    core.wait(iti)
    check_escape()

    # Cue
    cue_stim.text = cond_symbol[cond_label]
    cue_stim.draw()
    win.flip()
    core.wait(CONFIG["cue_dur_s"])
    check_escape()

    # Anticipation
    fixation.draw()
    win.flip()
    core.wait(CONFIG["anticipation_s"])
    check_escape()

    # Target + response window
    event.clearEvents()
    rt = None
    keyname = None
    target_stim.draw()
    win.flip()
    clock = core.Clock()  # starts ~at target onset
    target_sec = target_ms / 1000.0
    while clock.getTime() < target_sec:
        check_escape()
        keys = event.getKeys(keyList=CONFIG["resp_keys"], timeStamped=clock)
        if keys:
            keyname, rt_sec = keys[0]
            rt = rt_sec * 1000.0
            break
        core.wait(0.001)

    # Target off
    fixation.draw()
    win.flip()

    # Hit criterion: key within the visibility window (no grace)
    hit = (rt is not None and rt <= target_ms)

    # Feedback and staircase
    delta_points = meta["points_hit"] if hit else meta["points_miss"]
    points_total += delta_points
    stair.update(hit)

    # Feedback text
    if meta["valence"] > 0:
        fb = f"G E W I N N :  {delta_points:+d}"
    elif meta["valence"] < 0:
        fb = f"V E R M E I D U N G :  {delta_points:+d}"
    else:
        fb = "N E U T R A L"
    if CONFIG["show_cumulative_points"]:
        fb += f"\nPunkte gesamt: {points_total:d}"

    feedback_text.text = fb
    feedback_text.draw()
    win.flip()
    core.wait(CONFIG["feedback_dur_s"])
    check_escape()

    # Log
    writer.writerow([
        exp_info["participant"], exp_info["session"], timestamp(), block_idx, trial_idx, cond_label,
        meta["valence"], meta["magnitude"], target_ms, f"{rt:.1f}" if rt is not None else "", int(hit),
        round(iti,3), CONFIG["anticipation_s"], delta_points, points_total, keyname or ""
    ])

# Practice block (optional)
if CONFIG["practice_trials"] > 0:
    prac_trials = make_trials(CONFIG["conditions"], CONFIG["practice_trials"])
    for ti, cond in enumerate(prac_trials, start=1):
        run_trial(ti, block_idx=0, cond_label=cond)
    txt = visual.TextStim(win, text="Ende Übung.\nDrücken Sie eine Taste für den Start.", color=CONFIG["text_color"], height=CONFIG["text_font_height"], font=CONFIG["font"])
    txt.draw(); win.flip(); 
    keys = event.waitKeys()
    if 'escape' in keys:
        check_escape()

# ------------------------
# Main blocks
# ------------------------
for b in range(1, CONFIG["n_blocks"]+1):
    # Block intro
    blk = visual.TextStim(win, text=f"Block {b} von {CONFIG['n_blocks']}\n\nDrücken Sie eine Taste, um zu starten.", color=CONFIG["text_color"], height=CONFIG["text_font_height"], font=CONFIG["font"])
    blk.draw(); win.flip(); 
    keys = event.waitKeys()
    if 'escape' in keys:
        check_escape()

    trials = make_trials(CONFIG["conditions"], CONFIG["trials_per_block"])
    for ti, cond in enumerate(trials, start=1):
        run_trial(ti, block_idx=b, cond_label=cond)

# ------------------------
# Goodbye
# ------------------------
end_text = visual.TextStim(
    win, text=f"Geschafft!\nPunkte gesamt: {points_total}\n\nVielen Dank.", color=CONFIG["text_color"], height=CONFIG["text_font_height"], font=CONFIG["font"]
)
end_text.draw(); win.flip()
core.wait(2.0)

# Cleanup
try:
    csv_file.flush()
    csv_file.close()
except Exception:
    pass
win.close()
core.quit()
