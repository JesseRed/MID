#!/bin/bash
# Build script for Windows executable
# This script creates a Windows-compatible executable using PyInstaller

echo "Creating Windows-compatible MID Experiment executable..."

# Create a spec file for Windows
cat > MID_Experiment_Windows.spec << 'EOF'
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['mid_psychopy_pc_yaml.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('mid_config.yml', '.'),
        ('text_content.yml', '.'),
        ('images', 'images'),
        ('config_loader.py', '.'),
        ('utils.py', '.'),
    ],
    hiddenimports=[
        'psychopy',
        'yaml',
        'csv',
        'random',
        'os',
        'sys',
        'datetime',
        'collections',
        'argparse',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MID_Experiment',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
EOF

echo "Spec file created. To build Windows executable:"
echo "1. Install PyInstaller on Windows: pip install pyinstaller"
echo "2. Run: pyinstaller MID_Experiment_Windows.spec"
echo ""
echo "Or use the portable Python method above."
