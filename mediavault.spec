# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Spec File for MediaVault Scanner v2.0 (GGUF OCR Version)
This file defines how to build the Windows executable.

IMPORTANT NOTES FOR GGUF OCR DEPLOYMENT:
========================================

1. GGUF MODEL FILE IS NOT BUNDLED:
   - Deepseek GGUF model file (~2-7GB) is too large to bundle in executable
   - Model file must be downloaded separately and placed in models/ folder
   - Users can use the download script: scripts/download_model.ps1

2. LLAMA-CPP-PYTHON DEPENDENCIES:
   - llama-cpp-python with GPU support should be pre-installed
   - For NVIDIA CUDA: Build with CMAKE_ARGS="-DLLAMA_CUBLAS=on"
   - For AMD ROCm/HIP: Build with CMAKE_ARGS="-DLLAMA_HIP=on"
   - CPU-only version works but is slower

3. FALLBACK MECHANISM:
   - Application will automatically fall back to Tesseract if GGUF model unavailable
   - Tesseract must still be installed separately by the user

4. RECOMMENDED DEPLOYMENT STRATEGY:
   - Bundle llama-cpp-python in executable (~100-200MB)
   - Provide GGUF model download instructions
   - Include Tesseract installation guide
   - Users install GPU drivers separately (CUDA/ROCm)

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

# Collect llama-cpp-python data files (if any)
try:
    llama_cpp_datas = collect_data_files('llama_cpp')
    datas.extend(llama_cpp_datas)
except:
    print("Warning: Could not collect llama-cpp-python data files")

# Hidden imports that PyInstaller might miss
hiddenimports = [
    'PIL._tkinter_finder',
    'customtkinter',
    'pytesseract',
    'exifread',
    'cv2',
    'numpy',
    'sqlite3',

    # GGUF OCR dependencies
    'llama_cpp',
    'llama_cpp.llama_cpp',

    # Optional GPU support libraries
    'ctypes',
    'ctypes.util',
]

# Collect all submodules
hiddenimports.extend(collect_submodules('customtkinter'))

# Try to collect llama-cpp-python submodules (optional)
try:
    hiddenimports.extend(collect_submodules('llama_cpp'))
except:
    print("Warning: Could not collect llama-cpp-python submodules")

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

        # Exclude old VL-OCR dependencies (not needed for GGUF version)
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

