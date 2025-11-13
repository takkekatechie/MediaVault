# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Spec File for MediaVault Scanner (Enhanced VL-OCR Version)
This file defines how to build the Windows executable.

IMPORTANT NOTES FOR VL-OCR DEPLOYMENT:
======================================

1. MODEL WEIGHTS ARE NOT BUNDLED:
   - Deepseek-VL model weights (~7GB) are too large to bundle
   - Models will be downloaded on first run to user's cache directory
   - Default location: C:\\Users\\<Username>\\.cache\\huggingface\\hub\\

2. PYTORCH/CUDA DEPENDENCIES:
   - PyTorch with CUDA support adds ~2-4GB to executable size
   - Consider distributing without PyTorch and letting users install separately
   - Users can install with: pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

3. FALLBACK MECHANISM:
   - Application will automatically fall back to Tesseract if Deepseek is unavailable
   - Tesseract must still be installed separately by the user

4. RECOMMENDED DEPLOYMENT STRATEGY:
   - Option A: Bundle everything (large ~3-4GB executable)
   - Option B: Bundle without PyTorch, provide installation instructions (smaller ~100MB executable)
   - Option C: Provide Python environment setup script instead of executable

Usage:
    pyinstaller mediavault.spec

The resulting executable will be in the 'dist' folder.
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all necessary data files
datas = []

# Add OpenCV Haar Cascade files
import cv2
cv2_data_path = os.path.dirname(cv2.__file__)
haar_cascade_path = os.path.join(cv2_data_path, 'data', 'haarcascade_frontalface_default.xml')
if os.path.exists(haar_cascade_path):
    datas.append((haar_cascade_path, 'cv2/data'))

# Collect CustomTkinter assets
try:
    ctk_datas = collect_data_files('customtkinter')
    datas.extend(ctk_datas)
except:
    pass

# Collect transformers data files (tokenizers, configs, etc.)
try:
    transformers_datas = collect_data_files('transformers')
    datas.extend(transformers_datas)
except:
    print("Warning: Could not collect transformers data files")

# Collect sentencepiece data
try:
    sentencepiece_datas = collect_data_files('sentencepiece')
    datas.extend(sentencepiece_datas)
except:
    print("Warning: Could not collect sentencepiece data files")

# Hidden imports that PyInstaller might miss
hiddenimports = [
    'PIL._tkinter_finder',
    'customtkinter',
    'pytesseract',
    'exifread',
    'cv2',
    'numpy',
    'sqlite3',

    # VL-OCR dependencies (optional - will gracefully fail if not installed)
    'torch',
    'torchvision',
    'transformers',
    'accelerate',
    'sentencepiece',
    'protobuf',

    # Transformers submodules
    'transformers.models',
    'transformers.models.auto',
    'transformers.tokenization_utils',
    'transformers.tokenization_utils_base',
]

# Collect all submodules
hiddenimports.extend(collect_submodules('customtkinter'))

# Try to collect transformers submodules (optional)
try:
    hiddenimports.extend(collect_submodules('transformers'))
except:
    print("Warning: Could not collect transformers submodules")

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude large unnecessary packages to reduce size
        'matplotlib',
        'scipy',
        'pandas',
        'pytest',
        'setuptools',
        'IPython',
        'jupyter',
        'notebook',

        # Exclude PyTorch for lightweight build
        # Users can install separately if they want Deepseek-VL support:
        # pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
        # pip install transformers accelerate sentencepiece protobuf
        'torch',
        'torchvision',
        'transformers',
        'accelerate',
        'sentencepiece',
    ],
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
    name='MediaVaultScanner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for windowed app (no console window)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add path to .ico file if you have one: icon='icon.ico'
)

# Note: To add an icon, create or download an .ico file and set:
# icon='path/to/icon.ico'

