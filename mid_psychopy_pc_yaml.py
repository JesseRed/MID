#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MID task (PC-only) — YAML-driven configuration.

Features
- Parameters in YAML (timings, conditions, staircase, points, blocks)
- ESC abort anywhere (clean shutdown)
- Adaptive target duration per condition (1-up/2-down), with optional
  R-Score rule: if recent hit-rate exceeds threshold, scale target duration.
- WSL-friendly window defaults (no frame-rate check, no PTB)

Run:
    python mid_psychopy_pc_yaml.py --config mid_config.yml

Requires:
    pip install psychopy pyyaml
"""

import os, csv, random, argparse
from collections import deque
from datetime import datetime

import yaml
from psychopy import visual, core, event, gui

# ------------------------
# Helpers
# ------------------------

def timestamp():
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def uniform_jitter(lo, hi):
    return random.uniform(lo, hi)

class StaircaseAdaptive:
    """Simple 1-up/2-down staircase to ~70%."""
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
# Load config
# ------------------------

def load_config(path):
    with open(path, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f)

    # sensible defaults if missing
    cfg.setdefault('win', {})
    cfg['win'].setdefault('size', [1280, 720])
    cfg['win'].setdefault('fullscr', False)
    cfg['win'].setdefault('screen_color', 'black')
    cfg['win'].setdefault('text_color', 'white')
    cfg['win'].setdefault('fixation_color', 'white')
    cfg['win'].setdefault('font', 'Arial')
    cfg['win'].setdefault('useFBO', False)
    cfg['win'].setdefault('waitBlanking', False)
    cfg['win'].setdefault('checkTiming', False)

    cfg.setdefault('timings', {})
    # explicit timing spec from user
    cfg['timings'].setdefault('cue_ms', 250)
    cfg['timings'].setdefault('pause1_ms_range', [750, 1250])
    cfg['timings'].setdefault('pause2_ms_range', [800, 1200])
    cfg['timings'].setdefault('pause3_ms_range', [2000, 3000])
    cfg['timings'].setdefault('feedback_ms', 500)

    cfg.setdefault('staircase', {})
    cfg['staircase'].setdefault('initial_ms', 250)
    cfg['staircase'].setdefault('min_ms', 120)
    cfg['staircase'].setdefault('max_ms', 900)  # user mentioned 800/900 -> default 900
    cfg['staircase'].setdefault('step_ms', 10)
    # optional per-condition max override
    cfg['staircase'].setdefault('per_condition_max_ms', {})  # e.g., {"NEUTRAL": 800}

    cfg.setdefault('rscore', {})
    cfg['rscore'].setdefault('enabled', True)
    cfg['rscore'].setdefault('window', 20)       # last N trials (global) to compute %
    cfg['rscore'].setdefault('threshold', 75.0)  # percent
    cfg['rscore'].setdefault('scale', 0.9)       # multiply target_ms by this if above threshold
    cfg['rscore'].setdefault('scope', 'global')  # "global" or "per_condition"

    cfg.setdefault('task', {})
    cfg['task'].setdefault('n_blocks', 2)
    cfg['task'].setdefault('trials_per_block', 36)
    cfg['task'].setdefault('resp_keys', ['space'])
    cfg['task'].setdefault('show_cumulative_points', True)
    cfg['task'].setdefault('practice_trials', 0)

    cfg.setdefault('visuals', {})
    cfg['visuals'].setdefault('target_image', 'images/Target.png')
    cfg['visuals'].setdefault('cue_images', {"0": "images/Cue00.png", "1": "images/Cue03.png", "5": "images/Cue30.png"})
    cfg['visuals'].setdefault('monetary_feedback_images', {"0": "images/MonetaryFeedbackPositiv00.png", "1": "images/MonetaryFeedbackPositiv03.png", "5": "images/MonetaryFeedbackPositiv30.png"})
    cfg['visuals'].setdefault('performance_feedback_images', {"hit": "images/PerformanceFeedbackPositiv.png", "miss": "images/PerformanceFeedbackNegativ.png"})
    cfg['visuals'].setdefault('text_font_height', 0.05)

    cfg.setdefault('points', {})
    cfg['points'].setdefault('start', 0)

    # conditions list: [ [label, valence, magnitude, points_on_hit, points_on_miss], ... ]
    if 'conditions' not in cfg or not cfg['conditions']:
        cfg['conditions'] = [
            ['WIN_LOW', +1, 1, +10, 0],
            ['WIN_HIGH', +1, 5, +50, 0],
            ['AVOID_LOW', -1, 1, 0, -10],
            ['AVOID_HIGH', -1, 5, 0, -50],
            ['NEUTRAL', 0, 0, 0, 0],
        ]
    return cfg

# ------------------------
# Main
# ------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='mid_config.yml', help='Path to YAML config.')
    args = parser.parse_args()

    cfg = load_config(args.config)

    # Participant dialog
    exp_info = {"participant": "", "session": "001"}
    try:
        dlg = gui.DlgFromDict(exp_info, title="MID Task (PC)")
        if not dlg.OK:
            core.quit()
    except Exception:
        print("GUI unavailable – using defaults:", exp_info)

    # Output
    base_name = f"MID_PC_{exp_info['participant']}_{exp_info['session']}_{timestamp()}"
    out_dir = "data"
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, base_name + ".csv")

    # Window
    win = visual.Window(
        size=cfg['win']['size'],
        fullscr=cfg['win']['fullscr'],
        color=cfg['win']['screen_color'],
        units="height",
        allowGUI=False,
        waitBlanking=cfg['win']['waitBlanking'],
        checkTiming=cfg['win']['checkTiming'],
        useFBO=cfg['win']['useFBO'],
        autoLog=False
    )
    # Ensure window presents at least one frame before first draw
    win.flip()

    # Stimuli
    fixation = visual.TextStim(win, text="+", color=cfg['win']['fixation_color'],
                               height=cfg['visuals']['text_font_height'], font=cfg['win']['font'])

    instr = visual.TextStim(
        win,
        text=("Monetary Incentive Delay (MID)\n\n"
              "Fixieren Sie die Mitte.\n"
              "Kurz darauf erscheint ein Ziel (Kreis). Drücken Sie so schnell wie möglich die Leertaste, "
              "solange das Ziel sichtbar ist.\n\n"
              "Sie können Punkte gewinnen oder Verluste vermeiden – je nach Hinweis.\n"
              "Drücken Sie eine Taste, um zu starten."),
        color=cfg['win']['text_color'], height=cfg['visuals']['text_font_height'],
        wrapWidth=1.2, font=cfg['win']['font'], alignText="center"
    )

    feedback_text = visual.TextStim(
        win, text="", color=cfg['win']['text_color'],
        height=cfg['visuals']['text_font_height'], font=cfg['win']['font']
    )

    # Points & Conditions
    points_total = cfg['points']['start']
    cond_meta = {
        c[0]: {"valence": int(c[1]), "magnitude": int(c[2]),
               "points_hit": int(c[3]), "points_miss": int(c[4])}
        for c in cfg['conditions']
    }

    # Map conditions to cue images based on magnitude
    cue_image_map = {int(k): v for k, v in cfg['visuals']['cue_images'].items()}
    cond_cue_image = {label: cue_image_map[meta["magnitude"]] for label, meta in cond_meta.items()}
    
    # Map conditions to monetary feedback images based on magnitude
    monetary_feedback_map = {int(k): v for k, v in cfg['visuals']['monetary_feedback_images'].items()}
    cond_monetary_feedback = {label: monetary_feedback_map[meta["magnitude"]] for label, meta in cond_meta.items()}

    # Load cue images
    cue_images = {}
    for label, image_path in cond_cue_image.items():
        if os.path.exists(image_path):
            cue_images[label] = visual.ImageStim(win, image=image_path)
        else:
            print(f"Warning: Cue image not found: {image_path}")
            # Fallback to text
            cue_images[label] = visual.TextStim(win, text="?", color=cfg['win']['text_color'], height=0.12, font=cfg['win']['font'])
    
    # Load target image
    target_image_path = cfg['visuals']['target_image']
    if os.path.exists(target_image_path):
        target_stim = visual.ImageStim(win, image=target_image_path)
    else:
        print(f"Warning: Target image not found: {target_image_path}")
        # Fallback to text
        target_stim = visual.TextStim(win, text="◉", color=cfg['win']['text_color'], height=0.12, font=cfg['win']['font'])
    
    # Load monetary feedback images
    monetary_feedback_images = {}
    for label, image_path in cond_monetary_feedback.items():
        if os.path.exists(image_path):
            monetary_feedback_images[label] = visual.ImageStim(win, image=image_path)
        else:
            print(f"Warning: Monetary feedback image not found: {image_path}")
            # Fallback to text
            monetary_feedback_images[label] = visual.TextStim(win, text="?", color=cfg['win']['text_color'], height=0.12, font=cfg['win']['font'])
    
    # Load performance feedback images
    performance_feedback_images = {}
    for key, image_path in cfg['visuals']['performance_feedback_images'].items():
        if os.path.exists(image_path):
            performance_feedback_images[key] = visual.ImageStim(win, image=image_path)
        else:
            print(f"Warning: Performance feedback image not found: {image_path}")
            # Fallback to text
            performance_feedback_images[key] = visual.TextStim(win, text="?", color=cfg['win']['text_color'], height=0.12, font=cfg['win']['font'])

    # Staircases (per condition)
    cond_stair = {}
    for label in cond_meta.keys():
        max_ms = cfg['staircase']['per_condition_max_ms'].get(label, cfg['staircase']['max_ms'])
        cond_stair[label] = StaircaseAdaptive(
            initial_ms=cfg['staircase']['initial_ms'],
            min_ms=cfg['staircase']['min_ms'],
            max_ms=max_ms,
            step_ms=cfg['staircase']['step_ms'],
        )

    # R-Score tracking
    if cfg['rscore']['scope'] == 'per_condition':
        rscore_hist = {label: deque(maxlen=cfg['rscore']['window']) for label in cond_meta}
    else:
        rscore_hist = deque(maxlen=cfg['rscore']['window'])

    # CSV logging
    csv_headers = [
        "participant","session","timestamp","block","trial_index","condition",
        "valence","magnitude","target_ms_pre","target_ms_final","rt_ms","hit",
        "pause1_ms","pause2_ms","pause3_ms","cue_ms","feedback_ms",
        "points_change","points_total","key_pressed","rscore_scope","rscore_value"
    ]
    csv_file = open(csv_path, "w", newline="", encoding="utf-8")
    writer = csv.writer(csv_file)
    writer.writerow(csv_headers)

    def check_escape():
        if 'escape' in event.getKeys():
            print("Abbruch durch Benutzer (ESC) – speichere Daten und beende...")
            try:
                csv_file.flush(); csv_file.close()
            except Exception:
                pass
            try:
                win.close()
            except Exception:
                pass
            core.quit()

    def make_trials(n_trials):
        labels = list(cond_meta.keys())
        n_cond = len(labels)
        base = n_trials // n_cond
        rem = n_trials % n_cond
        trials = []
        for i, lab in enumerate(labels):
            count = base + (1 if i < rem else 0)
            trials.extend([lab] * count)
        random.shuffle(trials)
        return trials

    #--------------------
    # Start + Instruction Screens
    # ------------------------

    # 1️⃣ Startscreen (Title)
    start_text = visual.TextStim(
        win,
        text="M I D\n\nMonetary Incentive Delay Task",
        color=cfg['win']['text_color'],
        height=0.15,
        font=cfg['win']['font'],
        alignText="center"
    )
    start_sub = visual.TextStim(
        win,
        text="Drücken Sie eine beliebige Taste, um fortzufahren.",
        color=cfg['win']['text_color'],
        height=cfg['visuals']['text_font_height'],
        font=cfg['win']['font'],
        pos=(0, -0.25)
    )

    # draw both and show for at least a moment
    start_text.draw()
    start_sub.draw()
    win.flip()
    core.wait(0.8)  # ensures frame appears before waiting
    event.clearEvents()
    keys = event.waitKeys(keyList=cfg['task']['resp_keys'] + ['escape'])
    if 'escape' in keys:
        check_escape()

    # 2️⃣ Kurzanleitung
    instruction_text = visual.TextStim(
        win,
        text=(
            "Aufgabe:\n\n"
            "Fixieren Sie die Mitte des Bildschirms.\n"
            "Ein Symbol kündigt an, ob Sie einen gossen Gewinn (+) erzielen können, \n"
            "einen kleinen Gewinn erzielen können (o) oder nichts gewinnen könnne (-) können.\n"
            "Wenn der Zielkreis erscheint, drücken Sie so schnell wie möglich die Leertaste.\n"
            "Je schneller Sie reagieren, desto mehr Geld können Sie gewinnen.\n\n"
            "Drücken Sie eine Taste, um zu starten."
        ),
        color=cfg['win']['text_color'],
        height=cfg['visuals']['text_font_height'],
        wrapWidth=1.2,
        font=cfg['win']['font'],
        alignText="center"
    )
    instruction_text.draw()
    win.flip()
    keys = event.waitKeys(keyList=cfg['task']['resp_keys'] + ['escape'])
    if 'escape' in keys:
        check_escape()


    # Practice (optional)
    def run_trial(trial_idx, block_idx, cond_label):
        nonlocal points_total
        meta = cond_meta[cond_label]
        stair = cond_stair[cond_label]

        # Timing from config
        cue_ms = int(cfg['timings']['cue_ms'])
        p1_lo, p1_hi = cfg['timings']['pause1_ms_range']
        p2_lo, p2_hi = cfg['timings']['pause2_ms_range']
        p3_lo, p3_hi = cfg['timings']['pause3_ms_range']
        fb_ms = int(cfg['timings']['feedback_ms'])

        # Jitters
        pause1_ms = int(uniform_jitter(p1_lo, p1_hi))
        pause2_ms = int(uniform_jitter(p2_lo, p2_hi))
        pause3_ms = int(uniform_jitter(p3_lo, p3_hi))

        # ITI/pause1
        fixation.draw(); win.flip(); core.wait(pause1_ms / 1000.0); check_escape()

        # Cue
        cue_images[cond_label].draw(); win.flip(); core.wait(cue_ms / 1000.0); check_escape()

        # Anticipation == pause2
        fixation.draw(); win.flip(); core.wait(pause2_ms / 1000.0); check_escape()

        # Target duration from staircase
        target_ms_pre = stair.get_ms()

        # R-Score rule
        rscore_value = ''
        if cfg['rscore']['enabled']:
            if isinstance(rscore_hist, dict):  # per_condition
                hist = rscore_hist[cond_label]
                if len(hist) > 0:
                    r = 100.0 * (sum(hist) / len(hist))
                    rscore_value = f"{r:.1f}"
                    if r > cfg['rscore']['threshold']:
                        target_ms = max(cfg['staircase']['min_ms'], int(target_ms_pre * cfg['rscore']['scale']))
                    else:
                        target_ms = target_ms_pre
                else:
                    target_ms = target_ms_pre
            else:  # global
                if len(rscore_hist) > 0:
                    r = 100.0 * (sum(rscore_hist) / len(rscore_hist))
                    rscore_value = f"{r:.1f}"
                    if r > cfg['rscore']['threshold']:
                        target_ms = max(cfg['staircase']['min_ms'], int(target_ms_pre * cfg['rscore']['scale']))
                    else:
                        target_ms = target_ms_pre
                else:
                    target_ms = target_ms_pre
        else:
            target_ms = target_ms_pre

        # respect per-condition max and global max
        per_max = cfg['staircase']['per_condition_max_ms'].get(cond_label, None)
        max_cap = per_max if per_max is not None else cfg['staircase']['max_ms']
        target_ms = min(target_ms, max_cap)

        # Target + response
        event.clearEvents()
        rt = None; keyname = None
        target_stim.draw(); win.flip()
        clock = core.Clock()
        tgt_sec = target_ms / 1000.0
        while clock.getTime() < tgt_sec:
            check_escape()
            keys = event.getKeys(keyList=cfg['task']['resp_keys'], timeStamped=clock)
            if keys:
                keyname, rt_sec = keys[0]
                rt = int(rt_sec * 1000.0)
                break
            core.wait(0.001)

        # Target off
        fixation.draw(); win.flip()

        # Hit criterion
        hit = (rt is not None and rt <= target_ms)

        # Feedback
        delta_points = meta["points_hit"] if hit else meta["points_miss"]
        points_total += delta_points
        stair.update(hit)

        # Show monetary feedback image
        monetary_feedback_images[cond_label].draw(); win.flip(); core.wait(fb_ms / 1000.0); check_escape()
        
        # Show performance feedback image
        perf_key = "hit" if hit else "miss"
        performance_feedback_images[perf_key].draw(); win.flip(); core.wait(fb_ms / 1000.0); check_escape()

        # Pause3 (post-feedback)
        fixation.draw(); win.flip(); core.wait(pause3_ms / 1000.0); check_escape()

        # Update R-Score history
        if isinstance(rscore_hist, dict):
            rscore_hist[cond_label].append(1 if hit else 0)
        else:
            rscore_hist.append(1 if hit else 0)

        # Log
        writer.writerow([
            exp_info["participant"], exp_info["session"], timestamp(), block_idx, trial_idx, cond_label,
            meta["valence"], meta["magnitude"], target_ms_pre, target_ms,
            rt if rt is not None else "", int(hit),
            pause1_ms, pause2_ms, pause3_ms, cue_ms, fb_ms,
            delta_points, points_total, keyname or "",
            cfg['rscore']['scope'], rscore_value
        ])

    # Practice
    if cfg['task']['practice_trials'] > 0:
        labels = [c[0] for c in cfg['conditions']]
        # balance practice trials
        n = cfg['task']['practice_trials']
        per = max(1, n // len(labels))
        prac_trials = []
        for lab in labels:
            prac_trials += [lab] * per
        random.shuffle(prac_trials)
        for ti, cond in enumerate(prac_trials, start=1):
            run_trial(ti, block_idx=0, cond_label=cond)
        txt = visual.TextStim(win, text="Ende Übung.\nDrücken Sie eine Taste für den Start.",
                              color=cfg['win']['text_color'], height=cfg['visuals']['text_font_height'], font=cfg['win']['font'])
        txt.draw(); win.flip()
        keys = event.waitKeys(keyList=cfg['task']['resp_keys'] + ['escape'])
        if 'escape' in keys:
            check_escape()

    # Main blocks
    for b in range(1, cfg['task']['n_blocks'] + 1):
        blk = visual.TextStim(win, text=f"Block {b} von {cfg['task']['n_blocks']}\n\nDrücken Sie eine Taste, um zu starten.",
                              color=cfg['win']['text_color'], height=cfg['visuals']['text_font_height'], font=cfg['win']['font'])
        blk.draw(); win.flip()
        keys = event.waitKeys(keyList=cfg['task']['resp_keys'] + ['escape'])
        if 'escape' in keys:
            check_escape()

        trials = []
        # balanced distribution per block
        labels = [c[0] for c in cfg['conditions']]
        base = cfg['task']['trials_per_block'] // len(labels)
        rem = cfg['task']['trials_per_block'] % len(labels)
        for i, lab in enumerate(labels):
            count = base + (1 if i < rem else 0)
            trials.extend([lab] * count)
        random.shuffle(trials)

        for ti, cond in enumerate(trials, start=1):
            run_trial(ti, block_idx=b, cond_label=cond)

    # Goodbye
    end_text = visual.TextStim(win, text=f"Geschafft!\nPunkte gesamt: {points_total}\n\nVielen Dank.",
                               color=cfg['win']['text_color'], height=cfg['visuals']['text_font_height'], font=cfg['win']['font'])
    end_text.draw(); win.flip(); core.wait(2.0)

    try:
        csv_file.flush(); csv_file.close()
    except Exception:
        pass
    win.close(); core.quit()

if __name__ == "__main__":
    main()
