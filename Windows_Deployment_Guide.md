# MID Experiment - Windows Deployment Guide

## 🎯 Quick Start (Recommended)

### Option 1: Portable Python (No Admin Rights Required)

1. **Download Portable Python**:
   - Go to: https://www.python.org/downloads/windows/
   - Download "Windows embeddable package (64-bit)"
   - Extract to a folder (e.g., `C:\MID_Experiment\`)

2. **Install Dependencies**:
   ```cmd
   cd C:\MID_Experiment\
   python -m pip install --upgrade pip
   python -m pip install psychopy pyyaml
   ```

3. **Copy Experiment Files**:
   - Copy all files from this directory to `C:\MID_Experiment\`
   - Files needed: `mid_psychopy_pc_yaml.py`, `mid_config.yml`, `text_content.yml`, `config_loader.py`, `utils.py`, `images/` folder

4. **Run Experiment**:
   ```cmd
   cd C:\MID_Experiment\
   python mid_psychopy_pc_yaml.py
   ```

### Option 2: Anaconda Individual (No Admin Rights Required)

1. **Download Anaconda**:
   - Go to: https://www.anaconda.com/products/distribution
   - Download "Individual Edition"
   - Install to user directory (no admin rights needed)

2. **Setup Environment**:
   ```cmd
   conda create -n mid_env python=3.10
   conda activate mid_env
   pip install psychopy pyyaml
   ```

3. **Run Experiment**:
   ```cmd
   python mid_psychopy_pc_yaml.py
   ```

## 🔧 Creating Windows Executable

If you want a single `.exe` file:

1. **Install PyInstaller**:
   ```cmd
   pip install pyinstaller
   ```

2. **Build Executable**:
   ```cmd
   pyinstaller MID_Experiment_Windows.spec
   ```

3. **Find Executable**:
   - Look in `dist/` folder for `MID_Experiment.exe`

## 📁 Required Files

Make sure these files are in the same directory:
- `mid_psychopy_pc_yaml.py` (main experiment)
- `mid_config.yml` (configuration)
- `text_content.yml` (text content)
- `config_loader.py` (config loader)
- `utils.py` (utilities)
- `images/` folder (all image files)

## 🎮 Usage

1. **Start Experiment**: Run the Python script or executable
2. **Enter Participant Info**: Fill in participant ID and session
3. **Follow Instructions**: Read the task instructions
4. **Perform Task**: Press spacebar when target appears
5. **Data Saved**: Results saved to `data/` folder

## ⚠️ Troubleshooting

- **Key Detection Issues**: Make sure you're running on Windows (not WSL)
- **Missing Images**: Ensure `images/` folder is in the same directory
- **Permission Errors**: Use portable Python or install to user directory

## 📊 Data Output

Data is saved as CSV files in the `data/` folder with format:
`MID_PC_[participant]_[session]_[timestamp].csv`
