/**
 * MID Task - Electron Desktop Version
 * Works as standalone desktop app with config file editing support
 */

// Global state
let config = null;
let textContent = null;
let expInfo = {};
let csvData = [];
let pointsTotal = 0;
let condMeta = {};
let condStaircase = {};
let rscoreHist = [];
let currentKeys = new Set();

// Initialize
window.addEventListener('DOMContentLoaded', init);

async function init() {
    console.log('Initializing...');
    try {
        await loadConfigs();
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('dialog').classList.remove('hidden');
    } catch (error) {
        console.error('Error loading configs:', error);
        alert('Fehler beim Laden der Konfiguration: ' + error.message);
    }
}

async function loadConfigs() {
    // Load YAML configs using Electron API
    const configResult = await window.electronAPI.readFile('mid_config.yml');
    if (!configResult.success) {
        throw new Error('Failed to load mid_config.yml: ' + configResult.error);
    }
    config = jsyaml.load(configResult.content);
    
    const textResult = await window.electronAPI.readFile('text_content.yml');
    if (!textResult.success) {
        throw new Error('Failed to load text_content.yml: ' + textResult.error);
    }
    textContent = jsyaml.load(textResult.content);
    
    console.log('Config loaded:', config);
    console.log('Text loaded:', textContent);
}

function startExperiment() {
    expInfo.participant = document.getElementById('participant').value || 'test';
    expInfo.session = document.getElementById('session').value || '001';
    
    document.getElementById('dialog').classList.add('hidden');
    document.getElementById('container').classList.remove('hidden');
    
    // Setup keyboard
    setupKeyboard();
    
    // Initialize experiment
    setupExperiment();
    runExperiment();
}

function setupKeyboard() {
    document.addEventListener('keydown', (e) => {
        // ESC key to quit experiment
        if (e.key === 'Escape') {
            if (confirm('Möchten Sie das Experiment wirklich beenden?')) {
                endExperiment();
            }
            return;
        }
        currentKeys.add(e.key);
    });
    
    document.addEventListener('keyup', (e) => {
        currentKeys.delete(e.key);
    });
}

function setupExperiment() {
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
    
    // Initialize staircases
    for (const label of Object.keys(condMeta)) {
        condStaircase[label] = new StaircaseAdaptive(
            config.staircase.initial_ms,
            config.staircase.min_ms,
            config.staircase.max_ms,
            config.staircase.step_ms
        );
    }
    
    // Initialize R-Score
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
    
    // Initialize CSV
    csvData = [
        ['participant', 'session', 'timestamp', 'block', 'trial_index', 'condition',
         'valence', 'magnitude', 'target_ms_pre', 'target_ms_final', 'rt_ms', 'hit',
         'pause1_ms', 'pause2_ms', 'pause3_ms', 'cue_ms', 'feedback_ms',
         'points_change', 'points_total', 'key_pressed', 'rscore_scope', 'rscore_value']
    ];
}

async function runExperiment() {
    // Show title
    await showTextScreen(textContent.title + '\n\n' + textContent.subtitle + '\n\n' + textContent.start_instruction);
    
    // Show instructions
    await showTextScreen(textContent.task_instructions);
    
    // Run blocks
    const nBlocks = config.task.n_blocks || 2;
    const trialsPerBlock = config.task.trials_per_block || 36;
    
    for (let blockIdx = 0; blockIdx < nBlocks; blockIdx++) {
        if (blockIdx > 0) {
            const blockMsg = textContent.block_start
                .replace('{block_num}', blockIdx + 1)
                .replace('{total_blocks}', nBlocks);
            await showTextScreen(blockMsg);
        }
        
        const trials = makeTrials(trialsPerBlock);
        
        for (let trialIdx = 0; trialIdx < trials.length; trialIdx++) {
            await runTrial(trialIdx, blockIdx, trials[trialIdx]);
        }
    }
    
    // Show end message
    const endMsg = textContent.experiment_end.replace('{total_points}', pointsTotal);
    await showTextScreen(endMsg);
    
    // Download CSV
    await downloadCSV();
}

async function runTrial(trialIdx, blockIdx, condLabel) {
    const meta = condMeta[condLabel];
    const stair = condStaircase[condLabel];
    
    // Get timing
    const cueMs = config.timings.cue_ms;
    const pause1Ms = uniformJitter(config.timings.pause1_ms_range);
    const pause2Ms = uniformJitter(config.timings.pause2_ms_range);
    const pause3Ms = uniformJitter(config.timings.pause3_ms_range);
    const feedbackMs = config.timings.feedback_ms;
    
    // Get target duration
    let targetMs = stair.getCurrentDuration();
    const targetMsPre = targetMs;
    
    // Apply R-Score if enabled
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
    
    // Respect max
    const perMax = config.staircase.per_condition_max_ms[condLabel];
    const maxCap = perMax !== undefined ? perMax : config.staircase.max_ms;
    targetMs = Math.min(targetMs, maxCap);
    
    // Phase 1: Cue
    const cueImage = config.visuals.cue_images[meta.magnitude.toString()];
    await showImage(cueImage, cueMs);
    
    // Phase 2: Pause 1
    await showFixation(pause1Ms);
    
    // Phase 3: Target + Response
    const responseData = await showTargetAndGetResponse(targetMs);
    const rt = responseData.rt;
    const keyname = responseData.key;
    
    // Phase 4: Pause 2
    await showFixation(pause2Ms);
    
    // Determine hit/miss
    const hit = rt !== null && rt < targetMs;
    
    // Update staircase
    stair.update(hit);
    
    // Calculate points
    let deltaPoints = 0;
    if (hit) {
        deltaPoints = meta.pointsHit;
    } else {
        deltaPoints = meta.pointsMiss;
    }
    pointsTotal += deltaPoints;
    
    // Phase 5: Performance Feedback
    const perfImage = hit ? 
        config.visuals.performance_feedback_images.hit : 
        config.visuals.performance_feedback_images.miss;
    await showImage(perfImage, feedbackMs);
    
    // Phase 6: Monetary Feedback
    const monetaryLabel = hit ? condLabel : 'NEUTRAL';
    const monetaryImage = config.visuals.monetary_feedback_images[condMeta[monetaryLabel].magnitude.toString()];
    const points = hit ? meta.pointsHit : 0;
    const gainText = `+${points} Cent`;
    await showImageWithText(monetaryImage, gainText, feedbackMs);
    
    // Phase 7: Pause 3
    await showFixation(pause3Ms);
    
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
    csvData.push([
        expInfo.participant, expInfo.session, new Date().toISOString(),
        blockIdx, trialIdx, condLabel,
        meta.valence, meta.magnitude, targetMsPre, targetMs, rt || '', hit ? 1 : 0,
        pause1Ms, pause2Ms, pause3Ms, cueMs, feedbackMs,
        deltaPoints, pointsTotal, keyname || '',
        config.rscore.scope, rscoreValue || ''
    ]);
}

// Display functions
function showTextScreen(text) {
    return new Promise((resolve) => {
        const display = document.getElementById('display');
        display.innerHTML = `<div class="text-screen">${text}</div>`;
        currentKeys.clear();
        
        const checkKey = () => {
            if (currentKeys.size > 0) {
                resolve();
            } else {
                requestAnimationFrame(checkKey);
            }
        };
        checkKey();
    });
}

function showFixation(durationMs) {
    return new Promise((resolve) => {
        const display = document.getElementById('display');
        display.innerHTML = '<div class="fixation">+</div>';
        setTimeout(resolve, durationMs);
    });
}

function showImage(imagePath, durationMs) {
    return new Promise((resolve) => {
        const display = document.getElementById('display');
        display.innerHTML = `<img src="${imagePath}" class="image-stim">`;
        setTimeout(resolve, durationMs);
    });
}

function showImageWithText(imagePath, text, durationMs) {
    return new Promise((resolve) => {
        const display = document.getElementById('display');
        display.innerHTML = `
            <div class="monetary-text">${text}</div>
            <img src="${imagePath}" class="image-stim">
        `;
        setTimeout(resolve, durationMs);
    });
}

function showTargetAndGetResponse(targetMs) {
    return new Promise((resolve) => {
        const display = document.getElementById('display');
        const targetImage = config.visuals.target_image;
        display.innerHTML = `<img src="${targetImage}" class="image-stim">`;
        
        currentKeys.clear();
        const startTime = performance.now();
        let responded = false;
        let rt = null;
        let keyname = null;
        
        const checkResponse = () => {
            const elapsed = performance.now() - startTime;
            
            if (elapsed >= targetMs) {
                resolve({ rt: rt, key: keyname });
                return;
            }
            
            if (!responded && currentKeys.size > 0) {
                responded = true;
                rt = Math.round(elapsed);
                keyname = Array.from(currentKeys)[0];
            }
            
            requestAnimationFrame(checkResponse);
        };
        
        checkResponse();
    });
}

// Utility functions
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

function uniformJitter(range) {
    const [min, max] = range;
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

async function downloadCSV() {
    const csvString = csvData.map(row => row.join(',')).join('\n');
    const timestamp = new Date().toISOString().replace(/[-:]/g, '').replace('T', '-').split('.')[0];
    const filename = `MID_${expInfo.participant}_${expInfo.session}_${timestamp}.csv`;
    
    // Save to data directory using Electron API
    const result = await window.electronAPI.saveCSV(csvString, filename);
    
    if (result.success) {
        console.log('CSV saved to:', result.path);
        alert('Daten gespeichert in: ' + result.path);
    } else {
        console.error('Error saving CSV:', result.error);
        alert('Fehler beim Speichern: ' + result.error);
    }
}

async function endExperiment() {
    // Download CSV with current data
    await downloadCSV();
    
    // Show end message
    const display = document.getElementById('display');
    display.innerHTML = `
        <div class="text-screen">
            Das Experiment wurde beendet.<br><br>
            Ihre Daten wurden gespeichert.<br><br>
            Die Anwendung wird in 3 Sekunden geschlossen.
        </div>
    `;
    
    // Close app after delay
    setTimeout(() => {
        window.electronAPI.quitApp();
    }, 3000);
    
    // Stop any ongoing processes
    throw new Error('Experiment terminated by user');
}

// Staircase class
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
            if (this.consecutiveHits >= 2) {
                this.currentMs = Math.max(this.minMs, this.currentMs - this.stepMs);
                this.consecutiveHits = 0;
            }
        } else {
            this.consecutiveMisses++;
            this.consecutiveHits = 0;
            this.currentMs = Math.min(this.maxMs, this.currentMs + this.stepMs);
            this.consecutiveMisses = 0;
        }
    }
}

