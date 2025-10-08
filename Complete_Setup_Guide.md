# Complete MID Experiment Package
# This package includes everything needed to run the experiment

## 🎯 **Quick Start (No Installation Required)**

### **Method 1: Use Pre-built Package**

1. **Download Python with pip**:
   - Go to: https://www.python.org/downloads/windows/
   - Download "Windows installer (64-bit)" (NOT embeddable)
   - Install with "Add Python to PATH" checked
   - Choose "Install just for me" (no admin needed)

2. **Install Dependencies**:
   ```cmd
   pip install psychopy pyyaml
   ```

3. **Run Experiment**:
   ```cmd
   python mid_psychopy_pc_yaml.py
   ```

### **Method 2: Anaconda (Recommended)**

1. **Download Anaconda Individual**:
   - Go to: https://www.anaconda.com/products/distribution
   - Download "Individual Edition"
   - Install to user directory

2. **Setup**:
   ```cmd
   conda create -n mid_env python=3.10
   conda activate mid_env
   pip install psychopy pyyaml
   python mid_psychopy_pc_yaml.py
   ```

### **Method 3: Fix Portable Python**

If you want to use portable Python:

1. **Run the pip installer**:
   - Double-click `install_pip.bat`
   - Wait for pip to install

2. **Install dependencies**:
   ```cmd
   pip install psychopy pyyaml
   ```

3. **Run experiment**:
   ```cmd
   python mid_psychopy_pc_yaml.py
   ```

## 📁 **Required Files**

Make sure these files are in your directory:
- `mid_psychopy_pc_yaml.py`
- `mid_config.yml`
- `text_content.yml`
- `config_loader.py`
- `utils.py`
- `images/` folder
- `install_pip.bat` (if using portable Python)

## 🎮 **Usage**

1. **Start**: Run `python mid_psychopy_pc_yaml.py`
2. **Enter Info**: Participant ID and session
3. **Follow Instructions**: Read task description
4. **Perform Task**: Press spacebar when target appears
5. **Data Saved**: Results in `data/` folder

## ⚠️ **Troubleshooting**

- **"No module named pip"**: Use Method 1 or 2 above
- **Key detection issues**: Make sure you're on Windows (not WSL)
- **Missing images**: Ensure `images/` folder is present
- **Permission errors**: Install to user directory, not system
