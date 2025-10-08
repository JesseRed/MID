/**
 * Monetary Incentive Delay (MID) Task - PsychoJS Version
 * 
 * JavaScript/web browser version of the MID experiment
 * Corresponds to mid_psychopy_pc_yaml.py
 * 
 * Author: Prof. Dr. Carsten M. Klingner
 * Date: 2025-10-08
 */

import * as core from 'https://lib.pavlovia.org/core-2021.2.3.js';
import * as visual from 'https://lib.pavlovia.org/visual-2021.2.3.js';
import * as data from 'https://lib.pavlovia.org/data-2021.2.3.js';
import * as util from 'https://lib.pavlovia.org/util-2021.2.3.js';

// Global variables
let psychoJS;
let win;
let expInfo = {'participant': '', 'session': '001'};
let config;
let trialClock;
let csvData = [];

// Stimuli
let fixation, cueImages = {}, targetStim, performanceFeedbackImages = {}, monetaryFeedbackImages = {}, monetaryGainText = {};

// Staircase and tracking
let condStaircase = {};
let rscoreHist;
let pointsTotal = 0;
let condMeta = {};

/**
 * Initialize the PsychoJS experiment
 */
async function initPsychoJS() {
    // Create PsychoJS instance
    psychoJS = new core.PsychoJS({
        debug: true
    });

    // Open window
    win = new visual.Window({
        psychoJS: psychoJS,
        name: 'win',
        fullscr: false,
        color: new util.Color('black'),
        units: 'height'
    });

    // Schedule the experiment
    psychoJS.schedule(showInfoDialog);
    psychoJS.schedule(loadConfig);
    psychoJS.schedule(setupExperiment);
    psychoJS.schedule(runExperiment);
    psychoJS.schedule(endExperiment);

    return psychoJS.start();
}

/**
 * Show participant info dialog
 */
async function showInfoDialog() {
    return await psychoJS.gui.DlgFromDict({
        dictionary: expInfo,
        title: 'MID Task - Monetary Incentive Delay'
    });
}

/**
 * Load YAML configuration
 */
async function loadConfig() {
    try {
        const response = await fetch('mid_config.yml');
        const yamlText = await response.text();
        config = jsyaml.load(yamlText);
        
        // Load text content
        const textResponse = await fetch('text_content.yml');
        const textYaml = await textResponse.text();
        config.text = jsyaml.load(textYaml);
        
        console.log('Configuration loaded:', config);
        return core.Scheduler.Event.NEXT;
    } catch (error) {
        console.error('Error loading configuration:', error);
        return core.Scheduler.Event.QUIT;
    }
}

/**
 * Setup experiment stimuli and data structures
 */
async function setupExperiment() {
    // Initialize clock
    trialClock = new util.Clock();
    
    // Create condition metadata
    config.conditions.forEach(cond => {
        const [label, valence, magnitude, pointsHit, pointsMiss] = cond;
        condMeta[label] = {
            valence: valence,
            magnitude: magnitude,
            pointsHit: pointsHit,
            pointsMiss: pointsMiss
        };
    });
    
    // Create fixation cross
    fixation = new visual.TextStim({
        win: win,
        text: '+',
        color: new util.Color(config.win.fixation_color || 'white'),
        height: config.visuals.text_font_height || 0.04,
        font: config.win.font || 'Arial'
    });
    
    // Load cue images
    for (const [label, meta] of Object.entries(condMeta)) {
        const magnitude = meta.magnitude;
        const imagePath = config.visuals.cue_images[magnitude.toString()];
        cueImages[label] = new visual.ImageStim({
            win: win,
            image: imagePath,
            size: 0.6
        });
    }
    
    // Load target image
    targetStim = new visual.ImageStim({
        win: win,
        image: config.visuals.target_image,
        size: 0.6
    });
    
    // Load performance feedback images
    performanceFeedbackImages.hit = new visual.ImageStim({
        win: win,
        image: config.visuals.performance_feedback_images.hit,
        size: 0.6
    });
    performanceFeedbackImages.miss = new visual.ImageStim({
        win: win,
        image: config.visuals.performance_feedback_images.miss,
        size: 0.6
    });
    
    // Load monetary feedback images and create text overlays
    for (const [label, meta] of Object.entries(condMeta)) {
        const magnitude = meta.magnitude;
        const imagePath = config.visuals.monetary_feedback_images[magnitude.toString()];
        monetaryFeedbackImages[label] = new visual.ImageStim({
            win: win,
            image: imagePath,
            size: 0.6
        });
        
        // Create monetary gain text
        const points = meta.pointsHit;
        const gainText = points > 0 ? `+${points} Cent` : '+0 Cent';
        monetaryGainText[label] = new visual.TextStim({
            win: win,
            text: gainText,
            color: new util.Color('white'),
            height: 0.1,
            font: config.win.font || 'Arial',
            pos: [0, 0.4],
            bold: true
        });
    }
    
    // Initialize staircases
    for (const label of Object.keys(condMeta)) {
        condStaircase[label] = new StaircaseAdaptive(
            config.staircase.initial_ms,
            config.staircase.min_ms,
            config.staircase.max_ms,
            config.staircase.step_ms
        );
    }
    
    // Initialize R-Score history
    if (config.rscore.scope === 'per_condition') {
        rscoreHist = {};
        for (const label of Object.keys(condMeta)) {
            rscoreHist[label] = [];
        }
    } else {
        rscoreHist = [];
    }
    
    // Initialize points
    pointsTotal = config.points.start || 0;
    
    // Initialize CSV data
    csvData = [['participant', 'session', 'timestamp', 'block', 'trial_index', 'condition',
                'valence', 'magnitude', 'target_ms_pre', 'target_ms_final', 'rt_ms', 'hit',
                'pause1_ms', 'pause2_ms', 'pause3_ms', 'cue_ms', 'feedback_ms',
                'points_change', 'points_total', 'key_pressed', 'rscore_scope', 'rscore_value']];
    
    return core.Scheduler.Event.NEXT;
}

/**
 * Run the main experiment
 */
async function runExperiment() {
    // Show title screen
    await showScreen(config.text.title + '\n\n' + config.text.subtitle + '\n\n' + config.text.start_instruction);
    
    // Show instructions
    await showScreen(config.text.task_instructions);
    
    // Run blocks
    const nBlocks = config.task.n_blocks || 2;
    const trialsPerBlock = config.task.trials_per_block || 36;
    
    for (let blockIdx = 0; blockIdx < nBlocks; blockIdx++) {
        // Show block start message
        if (blockIdx > 0) {
            const blockMsg = config.text.block_start
                .replace('{block_num}', blockIdx + 1)
                .replace('{total_blocks}', nBlocks);
            await showScreen(blockMsg);
        }
        
        // Generate trial list
        const trials = makeTrials(trialsPerBlock);
        
        // Run trials
        for (let trialIdx = 0; trialIdx < trials.length; trialIdx++) {
            const condLabel = trials[trialIdx];
            await runTrial(trialIdx, blockIdx, condLabel);
        }
    }
    
    // Show end message
    const endMsg = config.text.experiment_end.replace('{total_points}', pointsTotal);
    await showScreen(endMsg);
    
    return core.Scheduler.Event.NEXT;
}

/**
 * Run a single trial
 */
async function runTrial(trialIdx, blockIdx, condLabel) {
    const meta = condMeta[condLabel];
    const stair = condStaircase[condLabel];
    
    // Get timing parameters
    const cueMs = config.timings.cue_ms;
    const pause1Ms = uniformJitter(config.timings.pause1_ms_range);
    const pause2Ms = uniformJitter(config.timings.pause2_ms_range);
    const pause3Ms = uniformJitter(config.timings.pause3_ms_range);
    const feedbackMs = config.timings.feedback_ms;
    
    // Get target duration from staircase
    let targetMs = stair.getCurrentDuration();
    
    // Apply R-Score scaling if enabled
    let rscoreValue = null;
    if (config.rscore.enabled) {
        const hist = config.rscore.scope === 'per_condition' ? rscoreHist[condLabel] : rscoreHist;
        if (hist.length >= config.rscore.window) {
            const recentHits = hist.slice(-config.rscore.window);
            rscoreValue = (recentHits.reduce((a, b) => a + b, 0) / recentHits.length) * 100;
            if (rscoreValue >= config.rscore.threshold) {
                targetMs = Math.round(targetMs * config.rscore.scale);
            }
        }
    }
    
    const targetMsPre = stair.getCurrentDuration();
    
    // Respect condition max
    const perMax = config.staircase.per_condition_max_ms[condLabel];
    const maxCap = perMax !== undefined ? perMax : config.staircase.max_ms;
    targetMs = Math.min(targetMs, maxCap);
    
    // Phase 1: Cue
    cueImages[condLabel].setAutoDraw(true);
    await waitFrames(msToFrames(cueMs));
    cueImages[condLabel].setAutoDraw(false);
    
    // Phase 2: Pause 1
    fixation.setAutoDraw(true);
    await waitFrames(msToFrames(pause1Ms));
    fixation.setAutoDraw(false);
    
    // Phase 3: Target + Response
    const responseData = await showTargetAndGetResponse(targetMs);
    const rt = responseData.rt;
    const keyname = responseData.key;
    
    // Phase 4: Pause 2
    fixation.setAutoDraw(true);
    await waitFrames(msToFrames(pause2Ms));
    fixation.setAutoDraw(false);
    
    // Determine hit/miss
    const hit = rt !== null && rt < targetMs;
    
    // Update staircase
    stair.update(hit);
    
    // Calculate points change
    let deltaPoints = 0;
    if (hit) {
        deltaPoints = meta.pointsHit;
    } else {
        deltaPoints = meta.pointsMiss;
    }
    pointsTotal += deltaPoints;
    
    // Phase 5: Performance Feedback
    const perfKey = hit ? 'hit' : 'miss';
    performanceFeedbackImages[perfKey].setAutoDraw(true);
    await waitFrames(msToFrames(feedbackMs));
    performanceFeedbackImages[perfKey].setAutoDraw(false);
    
    // Phase 6: Monetary Feedback
    if (!hit) {
        // Show neutral feedback for misses
        monetaryFeedbackImages['NEUTRAL'].setAutoDraw(true);
        monetaryGainText['NEUTRAL'].setAutoDraw(true);
    } else {
        // Show condition-specific feedback for hits
        monetaryFeedbackImages[condLabel].setAutoDraw(true);
        monetaryGainText[condLabel].setAutoDraw(true);
    }
    await waitFrames(msToFrames(feedbackMs));
    monetaryFeedbackImages[condLabel].setAutoDraw(false);
    monetaryGainText[condLabel].setAutoDraw(false);
    if (!hit) {
        monetaryFeedbackImages['NEUTRAL'].setAutoDraw(false);
        monetaryGainText['NEUTRAL'].setAutoDraw(false);
    }
    
    // Phase 7: Pause 3
    fixation.setAutoDraw(true);
    await waitFrames(msToFrames(pause3Ms));
    fixation.setAutoDraw(false);
    
    // Update R-Score history
    if (config.rscore.scope === 'per_condition') {
        rscoreHist[condLabel].push(hit ? 1 : 0);
        if (rscoreHist[condLabel].length > config.rscore.window) {
            rscoreHist[condLabel].shift();
        }
    } else {
        rscoreHist.push(hit ? 1 : 0);
        if (rscoreHist.length > config.rscore.window) {
            rscoreHist.shift();
        }
    }
    
    // Log data
    const timestamp = new Date().toISOString();
    csvData.push([
        expInfo.participant, expInfo.session, timestamp, blockIdx, trialIdx, condLabel,
        meta.valence, meta.magnitude, targetMsPre, targetMs, rt || '', hit ? 1 : 0,
        pause1Ms, pause2Ms, pause3Ms, cueMs, feedbackMs,
        deltaPoints, pointsTotal, keyname || '',
        config.rscore.scope, rscoreValue || ''
    ]);
}

/**
 * Show target and get response
 */
async function showTargetAndGetResponse(targetMs) {
    return new Promise((resolve) => {
        const startTime = trialClock.getTime();
        let responded = false;
        let rt = null;
        let keyname = null;
        
        // Show target
        targetStim.setAutoDraw(true);
        
        // Set up keyboard listener
        const keyboard = new core.Keyboard({psychoJS: psychoJS});
        keyboard.clearEvents();
        
        const checkResponse = () => {
            const elapsed = (trialClock.getTime() - startTime) * 1000;
            
            if (elapsed >= targetMs) {
                targetStim.setAutoDraw(false);
                keyboard.stop();
                resolve({rt: rt, key: keyname});
                return;
            }
            
            if (!responded) {
                const keys = keyboard.getKeys({keyList: ['space', ...config.task.resp_keys], waitRelease: false});
                if (keys.length > 0) {
                    responded = true;
                    rt = Math.round(elapsed);
                    keyname = keys[0].name;
                }
            }
            
            // Continue checking
            requestAnimationFrame(checkResponse);
        };
        
        keyboard.start();
        checkResponse();
    });
}

/**
 * Show a text screen and wait for keypress
 */
async function showScreen(text) {
    const textStim = new visual.TextStim({
        win: win,
        text: text,
        color: new util.Color('white'),
        height: config.visuals.text_font_height || 0.04,
        font: config.win.font || 'Arial',
        wrapWidth: 1.5
    });
    
    textStim.setAutoDraw(true);
    
    return new Promise((resolve) => {
        const keyboard = new core.Keyboard({psychoJS: psychoJS});
        keyboard.start();
        
        const checkKey = () => {
            const keys = keyboard.getKeys({waitRelease: false});
            if (keys.length > 0) {
                textStim.setAutoDraw(false);
                keyboard.stop();
                resolve();
            } else {
                requestAnimationFrame(checkKey);
            }
        };
        
        checkKey();
    });
}

/**
 * Generate randomized trial list
 */
function makeTrials(nTrials) {
    const labels = Object.keys(condMeta);
    const nCond = labels.length;
    const base = Math.floor(nTrials / nCond);
    const rem = nTrials % nCond;
    
    const trials = [];
    labels.forEach((label, i) => {
        const count = base + (i < rem ? 1 : 0);
        for (let j = 0; j < count; j++) {
            trials.push(label);
        }
    });
    
    // Shuffle
    for (let i = trials.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [trials[i], trials[j]] = [trials[j], trials[i]];
    }
    
    return trials;
}

/**
 * End experiment and save data
 */
async function endExperiment() {
    // Convert CSV data to string
    const csvString = csvData.map(row => row.join(',')).join('\n');
    
    // Download CSV file
    const blob = new Blob([csvString], {type: 'text/csv'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `MID_WEB_${expInfo.participant}_${expInfo.session}_${timestamp()}.csv`;
    a.click();
    
    // Quit PsychoJS
    psychoJS.quit();
    
    return core.Scheduler.Event.NEXT;
}

/**
 * Utility: Generate timestamp
 */
function timestamp() {
    const now = new Date();
    return now.toISOString().replace(/[-:]/g, '').replace('T', '-').split('.')[0];
}

/**
 * Utility: Uniform jitter
 */
function uniformJitter(range) {
    const [min, max] = range;
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * Utility: Convert ms to frames (assuming 60Hz)
 */
function msToFrames(ms) {
    return Math.round(ms / (1000 / 60));
}

/**
 * Utility: Wait for N frames
 */
async function waitFrames(n) {
    return new Promise((resolve) => {
        let count = 0;
        const wait = () => {
            count++;
            if (count >= n) {
                resolve();
            } else {
                requestAnimationFrame(wait);
            }
        };
        wait();
    });
}

/**
 * Staircase Adaptive class
 */
class StaircaseAdaptive {
    constructor(initialMs, minMs, maxMs, stepMs) {
        this.currentMs = initialMs;
        this.minMs = minMs;
        this.maxMs = maxMs;
        this.stepMs = stepMs;
        this.consecutiveMisses = 0;
        this.consecutiveHits = 0;
    }
    
    getCurrentDuration() {
        return this.currentMs;
    }
    
    update(hit) {
        if (hit) {
            this.consecutiveHits++;
            this.consecutiveMisses = 0;
            // 2-down: decrease after 2 consecutive hits
            if (this.consecutiveHits >= 2) {
                this.currentMs = Math.max(this.minMs, this.currentMs - this.stepMs);
                this.consecutiveHits = 0;
            }
        } else {
            this.consecutiveMisses++;
            this.consecutiveHits = 0;
            // 1-up: increase after 1 miss
            this.currentMs = Math.min(this.maxMs, this.currentMs + this.stepMs);
            this.consecutiveMisses = 0;
        }
    }
}

// Start the experiment
initPsychoJS();

