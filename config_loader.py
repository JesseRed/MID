#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Configuration loader for MID task.
Handles loading and setting defaults for YAML configuration files.
"""

import yaml
import os


def load_text_content():
    """Load text content from text_content.yml file."""
    text_file = os.path.join(os.path.dirname(__file__), 'text_content.yml')
    try:
        with open(text_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Warning: Text content file not found: {text_file}")
        print("Using default text content.")
        return get_default_text_content()


def get_default_text_content():
    """Fallback default text content if file is missing."""
    return {
        'title': 'M I D',
        'subtitle': 'Monetary Incentive Delay Task',
        'start_instruction': 'Drücken Sie eine beliebige Taste, um fortzufahren.',
        'task_instructions': 'Aufgabe:\n\nFixieren Sie die Mitte des Bildschirms.\nEin Symbol kündigt an, ob Sie einen grossen Gewinn (+) erzielen können, einen kleinen Gewinn erzielen können (o) oder nichts gewinnen können (-) können.\nWenn der Zielkreis erscheint, drücken Sie so schnell wie möglich die Leertaste.\nJe schneller Sie reagieren, desto mehr Geld können Sie gewinnen.\n\nDrücken Sie eine Taste, um zu starten.',
        'practice_end': 'Ende Übung.\nDrücken Sie eine Taste für den Start.',
        'block_start': 'Block {block_num} von {total_blocks}\n\nDrücken Sie eine Taste, um zu starten.',
        'experiment_end': 'Geschafft!\nPunkte gesamt: {total_points}\n\nVielen Dank.',
        'escape_message': 'Abbruch durch Benutzer (ESC) – speichere Daten und beende...'
    }


def load_config(path):
    """Load YAML config with validation - no defaults, all values must be explicit."""
    with open(path, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f)

    # Load text content
    cfg['text'] = load_text_content()

    # Window defaults (these are OK to have defaults)
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

    # Validate required sections - terminate if missing
    required_sections = {
        'timings': 'Timing configuration',
        'staircase': 'Staircase configuration', 
        'rscore': 'R-Score configuration',
        'task': 'Task configuration',
        'conditions': 'Conditions configuration'
    }
    
    missing_sections = []
    for section, description in required_sections.items():
        if section not in cfg or not cfg[section]:
            missing_sections.append(f"  - {section}: {description}")
    
    if missing_sections:
        print("ERROR: Missing required configuration sections:")
        for section in missing_sections:
            print(section)
        print(f"\nPlease add these sections to your {path} file.")
        print("The program will now terminate.")
        exit(1)
    
    # Validate required fields within each section
    validate_timings(cfg['timings'])
    validate_staircase(cfg['staircase'])
    validate_rscore(cfg['rscore'])
    validate_task(cfg['task'])
    validate_conditions(cfg['conditions'])

    # Visual defaults (these are OK to have defaults)
    cfg.setdefault('visuals', {})
    cfg['visuals'].setdefault('target_image', 'images/Target.png')
    cfg['visuals'].setdefault('cue_images', {"0": "images/Cue00.png", "1": "images/Cue03.png", "5": "images/Cue30.png"})
    cfg['visuals'].setdefault('monetary_feedback_images', {"0": "images/MonetaryFeedbackPositiv00.png", "1": "images/MonetaryFeedbackPositiv03.png", "5": "images/MonetaryFeedbackPositiv30.png"})
    cfg['visuals'].setdefault('performance_feedback_images', {"hit": "images/PerformanceFeedbackPositiv.png", "miss": "images/PerformanceFeedbackNegativ.png"})
    cfg['visuals'].setdefault('text_font_height', 0.05)

    # Points defaults (these are OK to have defaults)
    cfg.setdefault('points', {})
    cfg['points'].setdefault('start', 0)
    
    return cfg


def validate_timings(timings):
    """Validate timings section."""
    required_fields = ['cue_ms', 'pause1_ms_range', 'pause2_ms_range', 'pause3_ms_range', 'feedback_ms']
    missing_fields = [field for field in required_fields if field not in timings]
    
    if missing_fields:
        print("ERROR: Missing required timing fields:")
        for field in missing_fields:
            print(f"  - timings.{field}")
        exit(1)


def validate_staircase(staircase):
    """Validate staircase section."""
    required_fields = ['initial_ms', 'min_ms', 'max_ms', 'step_ms']
    missing_fields = [field for field in required_fields if field not in staircase]
    
    if missing_fields:
        print("ERROR: Missing required staircase fields:")
        for field in missing_fields:
            print(f"  - staircase.{field}")
        exit(1)


def validate_rscore(rscore):
    """Validate rscore section."""
    required_fields = ['enabled', 'window', 'threshold', 'scale', 'scope']
    missing_fields = [field for field in required_fields if field not in rscore]
    
    if missing_fields:
        print("ERROR: Missing required rscore fields:")
        for field in missing_fields:
            print(f"  - rscore.{field}")
        exit(1)


def validate_task(task):
    """Validate task section."""
    required_fields = ['n_blocks', 'trials_per_block', 'resp_keys', 'show_cumulative_points', 'practice_trials']
    missing_fields = [field for field in required_fields if field not in task]
    
    if missing_fields:
        print("ERROR: Missing required task fields:")
        for field in missing_fields:
            print(f"  - task.{field}")
        exit(1)


def validate_conditions(conditions):
    """Validate conditions section."""
    if not isinstance(conditions, list) or len(conditions) == 0:
        print("ERROR: 'conditions' must be a non-empty list")
        exit(1)
    
    for i, condition in enumerate(conditions):
        if not isinstance(condition, list) or len(condition) != 5:
            print(f"ERROR: Condition {i} must be a list with exactly 5 elements: [label, valence, magnitude, points_hit, points_miss]")
            exit(1)
        
        label, valence, magnitude, points_hit, points_miss = condition
        if not isinstance(label, str) or not isinstance(valence, (int, float)) or not isinstance(magnitude, (int, float)):
            print(f"ERROR: Condition {i} has invalid types. Expected: [str, number, number, number, number]")
            exit(1)
